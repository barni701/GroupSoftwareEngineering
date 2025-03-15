function updateXPWidget() {
    fetch('/users/xp_status/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('xp-level').innerText = data.level;
            const progressElem = document.getElementById('xp-progress');
            progressElem.value = data.current_progress;
            progressElem.max = data.required_xp;
            document.getElementById('xp-text').innerText = `${data.current_progress} / ${data.required_xp} XP`;
        })
        .catch(error => console.error("Error updating XP widget:", error));
}

// Update XP widget every 10 seconds (adjust interval as needed)
setInterval(updateXPWidget, 10000);