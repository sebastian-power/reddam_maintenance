String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

async function renderSortedTasks(sort_by) {
    const status_to_item = ["Pending", "Not Started", "In Progress", "Done"];
    const usr_res = await fetch("/api/current_user", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    });
    const id_json = await usr_res.json();
    const data_usr = id_json.user_id;
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
            if (status_group == "Pending" && task.requested_by == data_usr) {
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
                    <button class="assign-worker" onclick="assignWorker(event,this,'${task.task_id_encoded}')">Self Assign</button>
                </div>
                `;
            } else if (status_group == "Pending") {
                taskContent += `
                <div class="task-content nono">
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
                    <button class="assign-worker" onclick="assignWorker(event,this,'${task.task_id_encoded}')">Self Assign</button>
                </div>
                `;
            } else if (task.requested_by == data_usr) {
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
                </div>
                `;
            } else if (task.assigned_to == data_usr) {
                taskContent += `
                <div class="task-content OgBiH" onclick="showTask('${task.task_id_encoded}')">
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
                        <p style="background-color: #9ce39c; border-radius: 3px;"><b>Assigned To: </b>${task.assigned_to_name}</p>
                    </div>
                </div>
                `;
            } else if (task.requested_by != data_usr) {
                taskContent += `
                <div class="task-content nono">
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

function assignWorker(event, task_div_button, task_id_encrypted) {
    event.stopPropagation();
    fetch('/api/assign_worker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ encoded_value: task_id_encrypted })
    });
    document.getElementsByClassName("section-content")[1].insertAdjacentElement("afterbegin", task_div_button.parentNode);
    task_div_button.remove();

}

document.addEventListener("DOMContentLoaded", async function() {
    await renderSortedTasks("due_by");

    $(".OgBiH").draggable({
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
        accept: ".OgBiH",
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