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
                        <p style="background-color: #9ce39c; border-radius: 3px;"><i class="fa-solid fa-calendar-day" style="color: #585757; margin-right: 8px;"></i>${task.due_by_str}</p>
                    </div>
                    <div class="created-by">
                        <p style="background-color: #9ce39c; border-radius: 3px;"><b>Requested By: </b>${task.requested_by_name}</p>
                    </div>
                </div>
                `;
            } else if (status_group == "Pending") {
                taskContent += `
                <div class="task-content">
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
                        <p style="background-color: #9ce39c; border-radius: 3px;"><b>Requested By: </b>${task.requested_by_name}</p>
                    </div>
                    <div class="assigned-to">
                        <p><b>Assigned To: </b>${task.assigned_to_name}</p>
                    </div>
                </div>
                `;
            } else if (task.requested_by != data_usr) {
                console.log(task.requested_by);
                console.log(data_usr);
                taskContent += `
                <div class="task-content">
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
});