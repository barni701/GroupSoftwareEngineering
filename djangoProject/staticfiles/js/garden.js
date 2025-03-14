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