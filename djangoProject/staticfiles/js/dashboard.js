function showXpGain(amount) {
    let xpElement = document.getElementById("xp-gain");
    xpElement.textContent = `+${amount} XP`;
    xpElement.style.opacity = "1";
    xpElement.style.transform = "translateY(-20px)";

    setTimeout(() => {
        xpElement.style.opacity = "0";
        xpElement.style.transform = "translateY(0)";
    }, 800);
}

// Example: Simulating XP gain (replace this with actual updates)
setTimeout(() => showXpGain(50), 2000);

function updateCurrency(newAmount) {
    let currencyElement = document.getElementById("currency-balance");
    let oldAmount = parseFloat(currencyElement.textContent);
    let currentAmount = oldAmount;

    let animation = setInterval(() => {
        if (currentAmount < newAmount) {
            currentAmount += Math.ceil((newAmount - oldAmount) / 10);
        } else if (currentAmount > newAmount) {
            currentAmount -= Math.ceil((oldAmount - newAmount) / 10);
        } else {
            clearInterval(animation);
        }
        currencyElement.textContent = currentAmount.toFixed(2);
    }, 50);
}

// Example: Simulating a currency change (replace with actual updates)
setTimeout(() => updateCurrency(500), 3000);

function highlightRankUp(rank) {
    let row = document.querySelector(`tr:nth-child(${rank + 1})`);
    if (row) {
        row.classList.add("rank-up");
        setTimeout(() => row.classList.remove("rank-up"), 1000);
    }
}

// Example: Simulating a leaderboard change
setTimeout(() => highlightRankUp(2), 4000);