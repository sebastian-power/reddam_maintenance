function addTaskPrompt() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("add-task-prompt").style.display = "block";
}

function exitPrompt() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("add-task-prompt").style.display = "none";
    document.getElementById("edit-task-prompt").style.display = "none";
    document.getElementById("assign-worker-prompt").style.display = "none";
}


async function showTask(task_id_encrypted) {
    const response = await fetch("/get_task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ encoded_value: task_id_encrypted })
    });
    const data = await response.json();
    console.log(data.title)
    document.getElementById("overlay").style.display = "block";
    document.getElementById("edit-task-prompt").style.display = "block";
    document.getElementById("title_edit").value = data.title;
    document.getElementById("description_edit").value = data.description;
    document.getElementById("due_by_edit").value = new Date(data.due_by).toISOString().split('Z')[0];
    let form = document.getElementById("edit-task-form");
    const hidden_in = document.createElement("input");
    hidden_in.value = task_id_encrypted;
    hidden_in.name = "task_id_encrypted";
    hidden_in.type = "hidden";

    form.appendChild(hidden_in);
    

}

