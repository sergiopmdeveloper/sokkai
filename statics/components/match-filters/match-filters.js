/**
 * Set the league filter
 * @param {string} league
 */
function setLeagueFilter(league) {
    const leagueFilterElement = document.querySelector("#league-filter");
    const leagueInput = document.querySelector("#league")

    leagueFilterElement.innerHTML = league;
    leagueInput.value = league;
}
