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


// Modal animation for crate opening
// Show the crate opening animation modal for a single open.
function showCrateOpeningAnimation(callback) {
    const modal = document.getElementById("crate-modal");
    const crateImg = document.getElementById("crate-animation");
    const message = document.getElementById("crate-message");

    // Show modal and reset animation state.
    modal.style.display = "block";
    crateImg.classList.remove("opening");
    message.innerText = "Opening crate...";

    // Start animation after a short delay.
    setTimeout(() => {
        crateImg.classList.add("opening");
    }, 100);

    // Hide modal after animation completes (1.1 seconds), then call callback.
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
            // Display aggregated rewards in a modal.
            showBulkRewardModal(data.rewards);
            // Update crate count on the page.
            const crateElem = document.querySelector(`[data-crate-type="${crateType}"] h3`);
            if (crateElem) {
                crateElem.innerText = crateElem.innerText.replace(/\(x\d+\)/, `(x${data.remaining})`);
            }
        } else {
            document.getElementById("inventory-message").innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error bulk opening crates:", err));
}

// Function to show the reward modal with details
function showRewardModal(rewardInfo) {
    const rewardModal = document.getElementById("reward-modal");
    const rewardDetails = rewardModal.querySelector('.modal-content');

    let html = `<h3>You Obtained:</h3>`;
    html += `<p><strong>Item:</strong> ${rewardInfo.item}</p>`;
    html += `<p><strong>Rarity:</strong> ${rewardInfo.rarity}</p>`;
    if (rewardInfo.farm_currency_awarded !== undefined) {
        html += `<p><strong>Farm Currency Awarded:</strong> ${rewardInfo.farm_currency_awarded}</p>`;
    }
    html += `<button type="button" onclick="closeRewardModal()">Close</button>`;

    rewardDetails.innerHTML = html;
    rewardModal.style.display = "block";
}

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

// Filter inventory items by name
function filterItems() {
    const query = document.getElementById("itemSearch").value.toLowerCase();
    const cards = document.querySelectorAll(".inventory-card");
    cards.forEach(card => {
        const name = card.getAttribute("data-name").toLowerCase();
        card.style.display = name.includes(query) ? "block" : "none";
    });
}

// Sort inventory items based on selected criteria
function sortItems() {
    const sortBy = document.getElementById("sortItems").value;
    const grid = document.getElementById("inventory-grid");
    let cards = Array.from(document.querySelectorAll(".inventory-card"));

    cards.sort((a, b) => {
        if (sortBy === "name") {
            return a.getAttribute("data-name").localeCompare(b.getAttribute("data-name"));
        } else if (sortBy === "rarity") {
            return parseInt(a.getAttribute("data-rarity")) - parseInt(b.getAttribute("data-rarity"));
        } else if (sortBy === "quantity") {
            return parseInt(b.getAttribute("data-quantity")) - parseInt(a.getAttribute("data-quantity"));
        }
    });

    // Clear and reappend sorted cards
    grid.innerHTML = "";
    cards.forEach(card => grid.appendChild(card));
}


function craftItem(recipeId) {
    fetch(`/crafting/craft/${recipeId}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById("crafting-message");
        if (data.success) {
            messageDiv.innerText = data.message;
            // Optionally, update inventory UI here
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error crafting item:", err));
}

function showDetailsPopup(crateKey) {
    console.log("showDetailsPopup called with key:", crateKey); // Debug line
    const hiddenDetails = document.getElementById(`details-${crateKey}`);
    if (hiddenDetails) {
        console.log("Hidden details found:", hiddenDetails.innerHTML); // Debug line
        showDetailsModal(hiddenDetails.innerHTML);
    } else {
        console.error("No details found for crate:", crateKey);
    }
}

function showDetailsModal(detailsInfo) {
    const detailsModal = document.getElementById("details-modal");
    const detailsContent = detailsModal.querySelector('.modal-content');

    let html = `<h3>Crate Details:</h3>`;
    html += detailsInfo;
    html += `<button type="button" onclick="closeDetailsModal()">Close</button>`;

    detailsContent.innerHTML = html;
    detailsModal.style.display = "block";
}

function closeDetailsModal() {
    document.getElementById("details-modal").style.display = "none";
}

function bulkBuyCrate(crateType) {
    // Get the quantity from the input field
    const quantityInput = document.getElementById(`bulk-quantity-${crateType}`);
    const quantity = quantityInput ? quantityInput.value : 1;

    // Prepare form data for the POST request
    const formData = new FormData();
    formData.append('quantity', quantity);

    fetch(`/crates/buy/bulk/${crateType}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById("buy-message");
        if (data.success) {
            messageDiv.innerText = data.message;
            // Optionally, update the crate count on the UI without reloading
            location.reload();
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error bulk buying crate:", err));
}

function showItemDetails(itemId) {
    // Get the modal and its content container
    const modal = document.getElementById("item-detail-modal");
    const content = document.getElementById("item-detail-content");

    // Build the content – this is a placeholder.
    // Replace with an AJAX request or more complex logic as needed.
    let html = `<h3>Item Details</h3>`;
    html += `<p><strong>Item ID:</strong> ${itemId}</p>`;
    html += `<p>Additional details about this item will be loaded here.</p>`;
    html += `<button type="button" onclick="closeItemDetailModal()">Close</button>`;

    // Set the content and display the modal
    content.innerHTML = html;
    modal.style.display = "block";
}

function closeItemDetailModal() {
    document.getElementById("item-detail-modal").style.display = "none";
}

function sellItem(itemId) {
    console.log("sellItem called for item:", itemId);
    // Get the quantity from the input field
    const qtyInput = document.getElementById(`sell-quantity-${itemId}`);
    const quantity = qtyInput ? qtyInput.value : 1;

    const formData = new FormData();
    formData.append('quantity', quantity);

    // Update URL if your sell endpoint is under a different prefix (e.g., '/crates/items/sell/' vs. '/items/sell/')
    fetch(`/crates/items/sell/${itemId}/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Use a dedicated element for sell messages
        const messageDiv = document.getElementById("sell-message");
        if (data.success) {
            messageDiv.innerText = data.message;
            // Optionally, update the UI without reloading the page.
            location.reload();
        } else {
            messageDiv.innerText = "Error: " + data.error;
        }
    })
    .catch(err => console.error("Error selling item:", err));
}
window.sellItem = sellItem;