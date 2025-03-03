console.log("Crates.js loaded successfully!");

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
            console.log("API Response:", data); // Debugging output

            if (data.success && data.reward) {
                document.getElementById("reward-text").innerText =
                    `You received: ${data.reward.materials.join(", ")} + ${data.reward.farm_currency_bonus} FarmCoins!`;
            } else {
                document.getElementById("reward-text").innerText = "Error: No rewards found.";
                console.error("Unexpected API response:", data);
            }
        })
        .catch(error => console.error("Fetch error:", error));
    }, 2000);
}

function closeModal() {
    document.getElementById("crate-modal").style.display = "none";
}

function buyCrate(crateType) {
    console.log(`Buying crate: ${crateType}`);

    fetch(`/crates/buy/${crateType}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response received:", data);
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Fetch error:", error));
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