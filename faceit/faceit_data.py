import json

import requests
import threading
import logging


class FaceitData:
    """The Data API for Faceit"""

    def __init__(self, api_token):
        """Contructor

        Keyword arguments:
        api_token -- The api token used for the Faceit API (either client or server API types)
        """
        self.thread_local = threading.local()
        self.api_token = api_token
        self.base_url = "https://open.faceit.com/data/v4"

        self.headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.api_token)

        }

    # Matches

    def get_session(self):
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session


    def match_stats(self, match_id=None):
        """Retrieve match details

        Keyword arguments:
        match_id -- The ID of the match
        """

        if match_id is None:
            logging.info("match_id cannot be nothing")
        else:
            api_url = "{}/matches/{}/stats".format(self.base_url, match_id)
            session = self.get_session()
            with session.get(api_url, headers=self.headers) as res:
                if res.status_code is 200:
                    return json.loads(res.content.decode('utf-8'))
                else:
                    return None

    # Players

    def player_details(self, nickname=None, game=None, game_player_id=None):
        """Retrieve player details

        Keyword arguments:
        nickname -- The nickname of the player of Faceit
        game -- A game on Faceit
        game_player_id -- The ID of a player on a game's platform
        """

        api_url = "{}/players".format(self.base_url)
        if nickname is not None:
            api_url += "?nickname={}".format(nickname)
        if game_player_id is not None:
            if nickname is not None:
                api_url += "&game_player_id={}".format(game_player_id)
            else:
                api_url += "?game_player_id={}".format(game_player_id)
        if game is not None:
            api_url += "&game={}".format(game)

        # print(api_url)
        session = self.get_session()
        with session.get(api_url, headers=self.headers) as res:
            if res.status_code is 200:
                return json.loads(res.content.decode('utf-8'))
            else:
                return None

    def player_id_details(self, player_id=None):
        """Retrieve player details

        Keyword arguments:
        player_id -- The ID of the player
        """
        if player_id is None:
            logging.info("The player_id cannot be nothing!")
        else:
            api_url = "{}/players/{}".format(self.base_url, player_id)

            session = self.get_session()
            with session.get(api_url, headers=self.headers) as res:
                if res.status_code is 200:
                    return json.loads(res.content.decode('utf-8'))
                else:
                    return None

    def player_matches(self, player_id=None, game=None, from_timestamp=None, to_timestamp=None,
                       starting_item_position=0, return_items=1):
        """Retrieve all matches of a player

        Keyword arguments:
        player_id -- The ID of a player
        game -- A game on Faceit
        from_timestamp -- The timestamp (UNIX time) as a lower bound of the query. 1 month ago if not specified
        to_timestamp -- The timestamp (UNIX time) as a higher bound of the query. Current timestamp if not specified
        starting_item_position -- The starting item position (Default is 0)
        return_items -- The number of items to return (Default is 20)
        """
        if player_id is None:
            logging.info("The player_id cannot be nothing")
        else:
            if game is None:
                logging.info("The game cannot be nothing!")
            else:
                api_url = "{}/players/{}/history".format(self.base_url, player_id)
                if from_timestamp is None:
                    if to_timestamp is None:
                        api_url += "?game={}&offset={}&limit={}".format(
                            game, starting_item_position, return_items)
                    else:
                        api_url += "?to={}".format(to_timestamp)
                else:
                    api_url += "?from={}".format(from_timestamp)

                session = self.get_session()
                with session.get(api_url, headers=self.headers) as res:
                    if res.status_code is 200:
                        return json.loads(res.content.decode('utf-8'))
                    else:
                        return None

    def player_stats(self, player_id=None, game_id=None):
        """Retrieve the statistics of a player

        Keyword arguments:
        player_id -- The ID of a player
        game_id -- A game on Faceit
        """
        if player_id is None:
            logging.info("The player_id cannot be nothing")
        else:
            if game_id is None:
                logging.info("The game_id cannot be nothing!")
            else:
                api_url = "{}/players/{}/stats/{}".format(
                    self.base_url, player_id, game_id)

                session = self.get_session()
                with session.get(api_url, headers=self.headers) as res:
                    if res.status_code is 200:
                        return json.loads(res.content.decode('utf-8'))
                    else:
                        return None
