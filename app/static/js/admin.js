async function renderSortedTasks(sort_by) {
    const response = await fetch("/get_tasks_sorted", {
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
                    <p>${task.requested_by_name}</p>
                </div>
            </div>
            `;
        }
        document.getElementsByClassName("section-content")[0].insertAdjacentHTML("afterbegin", taskContent);
    }
}
document.addEventListener("DOMContentLoaded", function() {
    renderSortedTasks("due_by");
});
