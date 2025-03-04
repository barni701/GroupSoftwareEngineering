// CSRF token helper function (standard Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function buyCrate(crateType) {
    fetch(`/crates/buy/${crateType}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById("buy-message");
        if (data.success) {
            messageDiv.innerText = data.message;
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error buying crate:", err));
}

// Open a single crate
function openSingleCrate(crateType) {
    fetch(`/crates/open/${crateType}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById("inventory-message");
        if (data.success) {
            messageDiv.innerText = `You received: ${data.reward.item} (${data.reward.rarity})`;
            // Optionally, update the UI to reflect new crate quantities (e.g., reload the page)
            location.reload();
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error opening crate:", err));
}

// Bulk open crates of a given type
function bulkOpenCrates(crateType) {
    fetch(`/crates/bulk_open/${crateType}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById("inventory-message");
        if (data.success) {
            let summary = "Bulk Opened Rewards:\n";
            data.rewards.forEach(reward => {
                summary += `${reward.item} (${reward.rarity})\n`;
            });
            messageDiv.innerText = summary;
            // Optionally, update the UI to reflect new crate quantities
            location.reload();
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error bulk opening crates:", err));
}