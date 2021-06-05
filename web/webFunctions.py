import logging

from config import DBNAME
from database import sqlite3db
from functions import config_functions


def get_web():
    """
    Get the refresh time from the DB.
    return : int from DB
    """
    web_only = False
    web_app = False
    logging.info("start get_Web")
    iRv = config_functions.check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_WEB
            """)
    if iRv > 0:
        web_only_read = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT web_only FROM CFG_WEB
                                """)
        web_app_read = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT web_app FROM CFG_WEB
                                """)
        if web_only_read[0][0] == 1:
            web_only = True
        if web_app_read[0][0] == 1:
            web_app = True

    web = web_only, web_app
    return web


def create_js(faceit, match, user, mode, goal):
    logging.info("start Create JS")
    f = open('refresh.js', 'w')
    cons = f"""
    let user = "{user}"
    let mode = "{mode}"
    const url = 'https://illupy.ch:5000/api/v1/csgo/faceit/user/'
    let FaceitList = {faceit}
    let MatchList = {match}
    let acEloGoal = "{goal}"
    
    """
    getapi = """
    async function getApiData() {
    // HTTPREQUEST NEW
    api_url = `${url}${user}/${mode}`;
    const response = await fetch(api_url)
        .then(resolved => {
            var data = resolved.json();
            return data
        }).then(data => {
            build_body(data);
        })
        .catch(rejected => {
            console.log(rejected)
        });
    } 
    """
    build_body = """
    function build_body(data) {
    let elo,
        rank,
        eloGoal,
        eloToday,
        winStreak,
        winLoss,
        totMatches,
        totMatchesWon,
        lastGame,
        ackd,
        eloDiff,
        kills,
        deaths,
        body = "";
    if (FaceitList[1] == "true") {
        let rank = `Rank:\t${data["Faceit-Api"].rank}`
        body = rank
    }
    if (FaceitList[0] == "true") {
        console.log('inside')
        let elo = `<br>Elo:\t${data["Faceit-Api"].elo}`
        body = body + elo
    }
    if (acEloGoal) {
        let eloGoal = `<br>Elo Goal:\t${acEloGoal}`
        body = body + eloGoal
    }
    if (FaceitList[2] == "true") {
        let eloToday = `<br>Elo Today:\t${data["Faceit-Api"]["Elo Today"]}`
        body = body + eloToday
    }
    if (FaceitList[3] == "true") {
        let winStreak = `<br>Win Streak:\t${data["Faceit-Api"]["Win Streak"]}`
        body = body + winStreak
    }
    if (mode == 'd') {
        let winLoss = `<br>Win/Loss per Day:\t${data["Faceit-Api"].Win} / ${data["Faceit-Api"].Loss}`
        body = body + winLoss
    }
    if (mode == 'w') {
        let winLoss = `<br>Win/Loss per Week:\t${data["Faceit-Api"].Win} / ${data["Faceit-Api"].Loss}`
        body = body + winLoss
    }  
    if (FaceitList[4] == "true") {
        let totMatches = `<br>Total Matches:\t${data["Faceit-Api"]["Total Matches"]}`
        body = body + totMatches
    }
    if (FaceitList[5] == "true") {
        let totMatchesWon = `<br>Total Matches Won:\t${data["Faceit-Api"]["Matches Won"]}`
        body = body + totMatchesWon
    }
    if (MatchList[0] == "true") {
        let lastGame = `<br><br>Last Game:\t${data["Faceit-Api"]["Last Game"].Map.charAt(0).toUpperCase() +  data["Faceit-Api"]["Last Game"].Map.slice(1)} ${data["Faceit-Api"]["Last Game"].Result} ${data["Faceit-Api"]["Last Game"].Score}`
        body = body + lastGame
    }
    if (MatchList[3] == "true") {
        let ackd = `<br>K/D:\t${data["Faceit-Api"]["Last Game"]["K/D"]}`
        body = body + ackd
    }
    if (MatchList[4] == "true") {
        let eloDiff = `<br>Elo Diff:\t${data["Faceit-Api"]["Last Game"]["Elo Diff"]}`
        body = body + eloDiff
    }
    if (MatchList[5] == "true") {
        let kills = `<br>Kills:\t${data["Faceit-Api"]["Last Game"]["Kills"]}`
        body = body + kills
    }
    if (MatchList[6] == "true") {
        let deaths = `<br>Deaths:\t${data["Faceit-Api"]["Last Game"]["Deaths"]}`
        body = body + deaths
    }
    
    document.getElementById("data").innerHTML = body;
    }
    """
    start_js = """
    getApiData();

    setInterval(function() {
        getApiData()
    }, 30000)
    """

    js = cons + getapi + build_body + start_js
    f.write(js)
    f.close()
