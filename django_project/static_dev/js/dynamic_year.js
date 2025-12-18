document.addEventListener('DOMContentLoaded', function() {
    var yearElement = document.getElementById('display-year');
    if (!yearElement) return;
    var serverDate = new Date(yearElement.dataset.serverDateIso);
    if (isNaN(serverDate.getTime())) {
        console.error("The server date could not be recognized.");
        return;
    }
    var localDate = new Date();
    const MILLISECONDS_IN_ONE_DAY = 24 * 60 * 60 * 1000;
    if (Math.abs(localDate.getTime() - serverDate.getTime()) < MILLISECONDS_IN_ONE_DAY) {
        yearElement.innerText = localDate.getFullYear();
    }
});