function addTaskPrompt() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("add-task-prompt").style.display = "block";
}

function exitPrompt() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("add-task-prompt").style.display = "none";
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
}

// function tasksByName