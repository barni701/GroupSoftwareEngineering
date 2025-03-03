function openCrate(crateElement) {
    const crateId = crateElement.getAttribute("data-id");

    // Show modal with animation
    document.getElementById("crate-modal").style.display = "flex";
    document.getElementById("reward-text").innerText = "Opening...";

    setTimeout(() => {
        fetch(`/crates/open/${crateId}/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("reward-text").innerText =
                `You received: ${data.reward.materials.join(", ")} + ${data.reward.farm_currency_bonus} FarmCoins!`;
        })
        .catch(error => console.error("Error:", error));
    }, 2000);
}

function closeModal() {
    document.getElementById("crate-modal").style.display = "none";
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}