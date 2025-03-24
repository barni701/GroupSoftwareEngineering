function upgradeBuilding(buildingId) {
    console.log("Upgrade triggered for building", buildingId);

    // Adjust the URL according to your URL configuration.
    fetch(`/farm/buildings/${buildingId}/upgrade/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Upgrade response:", data);
        const messageDiv = document.getElementById("upgrade-message");
        if (data.success) {
            messageDiv.innerText = data.message;
            // Optionally reload the page to reflect changes
            setTimeout(() => location.reload(), 1500);
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => {
        console.error("Error upgrading building:", err);
        const messageDiv = document.getElementById("upgrade-message");
        messageDiv.innerText = "Error upgrading building: " + err.message;
    });
}
window.upgradeBuilding = upgradeBuilding;