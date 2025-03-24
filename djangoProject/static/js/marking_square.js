// Function to get CSRF token from cookies (Django security requirement)
function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length, cookie.length);
            break;
        }
    }
    return cookieValue;
}

// Make AJAX Request for marking square
function markBingoSquare(challengeID) {
    fetch("/games/mark-square/", {
        method: "POST",
        headers: {
        "X-CSRFToken": getCSRFToken(),  // Django requires CSRF protection
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ challenge: challengeID })  // Send the actual variable, not a string literal
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data.message);  // Log server response
    })
    .catch(error => console.error("Error marking square:", error));
}