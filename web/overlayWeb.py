import webbrowser

from functions import config_functions, webHandler
from dearpygui import core

from guiHandling.colorHandling import get_data_from_colors
from main import get_values_to_safe_faceit
from web.webFunctions import create_js


def open_browser_and_fill_with_content():
    print('open browser function')
    NewFaceit_List = []
    NewMatch_List = []
    mode = "d"
    head_family = ""
    head_4 = ""
    head_5 = ""

    f = open('FaceitOverlay.html', 'w')
    HEADER_List, TEXT_List, BUT_ACTIVE_List, BG_List, OUTLINE_List, COL_List = get_data_from_colors()
    FACEIT_List, MATCH_List, acName = get_values_to_safe_faceit()
    acEloGoal = config_functions.get_elo_goal_from_db()
    winLoss = config_functions.get_win_loss()

    if int(winLoss[0][0]) == 1:
        mode = "d"
    if int(winLoss[0][1]) == 1:
        mode = "w"
    for x in FACEIT_List:
        x_str = str(x)
        NewFaceit_List.append(x_str.lower())
    for x in MATCH_List:
        x_str = str(x)
        NewMatch_List.append(x_str.lower())

    print(NewFaceit_List)
    create_js(NewFaceit_List, NewMatch_List, acName, mode, acEloGoal)
    bgimage = core.get_value("##BgImage")
    fsize, ffamily, bg = webHandler.get_parameters_from_dpg()

    head = """
    <html><head>
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@500&amp;display=swap" rel="stylesheet"> 
        <script src="refresh.js"></script>
        <style>
              body {
                margin: 0;
        """
    if ffamily:
        head_family = f"""
                font-family: {ffamily};
        """
    head_1 = """
            }
            .circles {
                display: flex;
              
            }
            .circle-with-text {
    """
    head_2 = f"""
              background: rgba({BG_List});
              justify-content: center;
              align-items: center;
              border-radius: 100%;
              border: 3px solid rgba({OUTLINE_List}) ;
              text-align: center;
              margin: 5px 20px;
              font-size: 15px;
              padding: 15px;
              display: flex;
              height: 1080px;
              width: 1080px;
              background-size: cover;
              color: rgba({TEXT_List});
    """
    head_3 = """
            }
            .multi-line-text {
    """
    if fsize:
        head_4 = f"""
                font-size: {fsize}px;
        """
    else:
        head_5 = """
                font-size: 64px;
    """
    head_6 = """
            }
        </style>
        </head>
    """
    body = f"""
    <body>
    <div class="circles">
      <div class="circle-with-text multi-line-text" id="data">
    """
    if bgimage:
        body = f"""
        <body>
        <div class="circles">
        <div class="circle-with-text multi-line-text" id="data" style="background-image: url({bgimage});">
        """
    body_load = """
        Loading Data...
    """
    b_end = """
      </div>
    </div>
  </body>
</html>
"""
    t = head + head_family + head_1 + head_2 + head_3 + head_4 + head_5 + head_6 + body + body_load + b_end
    f.write(t.replace("[", "").replace("]", ""))
    f.close()

    webbrowser.open_new_tab('FaceitOverlay.html')
