// CSRF helper function
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

// Buy a crate
function buyCrate(crateType) {
    fetch(`/crates/buy/${crateType}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById("buy-message");
        if (data.success) {
            messageDiv.innerText = data.message;
            // Optionally update the UI via location.reload() or DOM manipulation
            location.reload();
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error buying crate:", err));
}

// Show details popup modal
function showDetailsPopup(crateKey) {
    const detailsDiv = document.getElementById(`details-${crateKey}`);
    const detailsModal = document.getElementById("details-modal");
    detailsModal.querySelector('.modal-content').innerHTML = `
        <h3>Crate Details</h3>
        ${detailsDiv.innerHTML}
        <button type="button" onclick="closeDetailsPopup()">Close</button>
    `;
    detailsModal.style.display = "block";
}

function closeDetailsPopup() {
    document.getElementById("details-modal").style.display = "none";
}

// Modal animation for crate opening
function showCrateOpeningAnimation(callback) {
    const modal = document.getElementById("crate-modal");
    const crateImg = document.getElementById("crate-animation");
    const message = document.getElementById("crate-message");
    modal.style.display = "block";
    crateImg.classList.remove("opening");
    message.innerText = "Opening crate...";
    setTimeout(() => { crateImg.classList.add("opening"); }, 100);
    setTimeout(() => {
        modal.style.display = "none";
        if (callback) callback();
    }, 1100);
}

// Updated openSingleCrate function
function openSingleCrate(crateType) {
    showCrateOpeningAnimation(() => {
        fetch(`/crates/open/${crateType}/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Instead of updating a text element, show the reward modal
                showRewardModal(data.reward);
                // Also update the displayed crate quantity on the inventory page
                const crateElem = document.querySelector(`[data-crate-type="${crateType}"] h3`);
                if (crateElem) {
                    crateElem.innerText = crateElem.innerText.replace(/\(x\d+\)/, `(x${data.remaining})`);
                }
            } else {
                const messageDiv = document.getElementById("inventory-message");
                messageDiv.innerText = "Error: " + data.error;
            }
        })
        .catch(err => console.error("Error opening crate:", err));
    });
}

// Bulk open crates
function bulkOpenCrates(crateType) {
    fetch(`/crates/bulk_open/${crateType}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Display aggregated rewards in a modal popup
            showBulkRewardModal(data.rewards);
            // Optionally, update crate counts on the page
            const crateElem = document.querySelector(`[data-crate-type="${crateType}"] h3`);
            if (crateElem) {
                crateElem.innerText = crateElem.innerText.replace(/\(x\d+\)/, `(x${data.remaining})`);
            }
        } else {
            const messageDiv = document.getElementById("inventory-message");
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error bulk opening crates:", err));
}

// Function to show the reward modal with details
function showRewardModal(rewardInfo) {
    const rewardModal = document.getElementById("reward-modal");
    const rewardDetails = document.getElementById("reward-details");

    // Create a clear layout for the reward details
    let html = `<p><strong>Item:</strong> ${rewardInfo.item}</p>`;
    html += `<p><strong>Rarity:</strong> ${rewardInfo.rarity}</p>`;
    if (rewardInfo.farm_currency_awarded !== undefined) {
        html += `<p><strong>Farm Currency Awarded:</strong> ${rewardInfo.farm_currency_awarded}</p>`;
    }
    rewardDetails.innerHTML = html;
    rewardModal.style.display = "block";
}

// Function to close the reward modal
function closeRewardModal() {
    document.getElementById("reward-modal").style.display = "none";
}


// Updated function to show bulk open rewards in a modal popup
function showBulkRewardModal(aggregatedRewards) {
    const rewardModal = document.getElementById("reward-modal");
    const rewardDetails = rewardModal.querySelector('.modal-content');
    let html = "<h3>Bulk Opened Rewards</h3><ul>";
    aggregatedRewards.forEach(reward => {
        html += `<li><strong>${reward.item}</strong> (${reward.rarity}) x${reward.count}`;
        if (reward.farm_currency_awarded !== undefined) {
            html += ` – Total Farm Currency: ${reward.farm_currency_awarded}`;
        }
        html += `</li>`;
    });
    html += "</ul>";
    html += `<button type="button" onclick="closeRewardModal()">Close</button>`;
    rewardDetails.innerHTML = html;
    rewardModal.style.display = "block";
}