String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

async function renderSortedTasks(sort_by) {
    const status_to_item = ["Pending", "Not Started", "In Progress", "Done"];
    let taskList = [];
    const response = await fetch("/api/get_tasks_sorted", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ sort_method: sort_by })
    });
    const data = await response.json();
    for (const status_group of Object.keys(data.tasks)) {
        let taskContent = ``;
        for (const task of data.tasks[status_group]) {
            if (status_group == "Pending") {
                taskContent += `
                <div class="task-content" onclick="showTask('${task.task_id_encoded}')">
                    <h2 class="task-title">${task.title}</h2>
                    <div class="description">
                        <p>${task.description}</p>
                    </div>
                    <div class="due-date">
                        <p><i class="fa-solid fa-calendar-day" style="color: #585757; margin-right: 8px;"></i>${task.due_by_str}</p>
                    </div>
                    <div class="created-by">
                        <p><b>Requested By: </b>${task.requested_by_name}</p>
                    </div>
                    <div class="assigned-to">
                        <p><b>Assigned To: </b>${task.assigned_to_name}</p>
                    </div>
                    <button class="assign-worker" onclick="assignWorker(event,'${task.task_id_encoded}')">Assign Worker</button>
                </div>
                `;
            } else {
                taskContent += `
                <div class="task-content confirmed" onclick="showTask('${task.task_id_encoded}')">
                    <h2 class="task-title">${task.title}</h2>
                    <div class="description">
                        <p>${task.description}</p>
                    </div>
                    <div class="due-date">
                        <p><i class="fa-solid fa-calendar-day" style="color: #585757; margin-right: 8px;"></i>${task.due_by_str}</p>
                    </div>
                    <div class="created-by">
                        <p><b>Requested By: </b>${task.requested_by_name}</p>
                    </div>
                    <div class="assigned-to">
                        <p><b>Assigned To: </b>${task.assigned_to_name}</p>
                    </div>
                </div>
                `;
            }
            taskList.push(task);
        }
        document.getElementsByClassName("section-content")[status_to_item.indexOf(status_group)].insertAdjacentHTML("afterbegin", taskContent);
    }
}
document.addEventListener("DOMContentLoaded", async function() {
    await renderSortedTasks("due_by");

    $(".confirmed").draggable({
        revert: "invalid",
        helper: "clone",
        start: function(event, ui) {
            $(this).addClass("dragging-shadow");
            ui.helper.css("width", $(this).outerWidth());
        },
        stop: function(event, ui) {
            $(this).removeClass("dragging-shadow");
        }
    });

    $(".section-content.confirmed-section").droppable({
        accept: ".confirmed",
        drop: function(event, ui) {
            $(this)
                .append(ui.draggable.css("position", "static"));
                $(this).css("background", "transparent");
                const onclickEnc = ui.draggable[0].onclick;
                const encryptedTID = String(onclickEnc).split("showTask")[1].replace(/[()}'\n]/g, "");
                //get id of dropped location parent element
                const status = $(this).parent().attr("id").split("-").slice(2).join(" ").toProperCase();
                fetch("/api/change_status_drag", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"encoded_value": encryptedTID, "new_status": status})
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        },
        over: function(event, ui) {
            $(this).css("background", "lightgrey");
        },
        out: function(event, ui) {
            $(this).css("background", "transparent");
        }
    });
});

function assignWorker(event, task_id_encrypted) {
    event.stopPropagation();
    document.getElementById("overlay").style.display = "block";
    document.getElementById("assign-worker-prompt").style.display = "block";
    let form = document.getElementById("assign-worker-form");
    const hidden_in = document.createElement("input");
    hidden_in.value = task_id_encrypted;
    hidden_in.name = "task_id_encrypted";
    hidden_in.type = "hidden";

    form.appendChild(hidden_in);
}


let suggestions = [];
fetch('/api/get_workers', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
})
    .then(response => response.json())
    .then(data => {
        suggestions = data.worker_names;
    });

const inputField = document.getElementById('worker');
const suggestionsContainer = document.getElementById('autocomplete-suggestions');

inputField.addEventListener('input', () => {
    const query = inputField.value.toLowerCase();
    suggestionsContainer.innerHTML = '';

    if (query) {
    const filteredSuggestions = suggestions.filter(item =>
        item.toLowerCase().includes(query)
    );

    filteredSuggestions.forEach(suggestion => {
        const suggestionElement = document.createElement('div');
        suggestionElement.textContent = suggestion;
        suggestionElement.classList.add('autocomplete-suggestion');
        suggestionElement.addEventListener('click', () => {
        inputField.value = suggestion;
        suggestionsContainer.innerHTML = '';
        });
        suggestionsContainer.appendChild(suggestionElement);
    });
    }
});

// Close suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (e.target !== inputField) {
    suggestionsContainer.innerHTML = '';
    }
});

function deleteTask() {
    const taskIdEncrypted = document.querySelector('input[name="task_id_encrypted"]').value;
    fetch('/api/delete_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ encoded_value: taskIdEncrypted })
    });
    exitPrompt();
    document.querySelector(`div[onclick="showTask('${taskIdEncrypted}')`).remove();
}