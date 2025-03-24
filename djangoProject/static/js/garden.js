function submitPlantSeedForm(form, seedId) {
    var select = form.querySelector('select[name="plot_id"]');
    if (!select) {
        alert("No empty plot selected. Please create a new plot first.");
        return false;
    }
    var plotId = select.value;
    if (!plotId) {
        alert("No empty plot selected. Please create a new plot first.");
        return false;
    }
    form.action = '/garden/plant/' + plotId + '/' + seedId + '/';
    return true;
}
window.submitPlantSeedForm = submitPlantSeedForm;


function updateProgressBars() {
    const bars = document.querySelectorAll('.progress-bar');
    console.log("Found", bars.length, "progress bars");
    bars.forEach(bar => {
        // Retrieve the planted time and growth duration (in seconds) from data attributes.
        const plantedAt = bar.getAttribute('data-planted-at');
        const growthDuration = parseFloat(bar.getAttribute('data-growth-duration'));
        if (plantedAt && growthDuration) {
            const plantedDate = new Date(plantedAt);
            const now = new Date();
            const elapsed = (now - plantedDate) / 1000; // elapsed seconds
            let progress = (elapsed / growthDuration) * 100;
            if (progress > 100) {
                progress = 100;
            }
            bar.style.width = progress + '%';
            bar.setAttribute('aria-valuenow', progress);
            bar.innerText = Math.floor(progress) + '%';
        }
    });
}

// Update the progress bars every second.
setInterval(updateProgressBars, 1000);