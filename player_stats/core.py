from collections import namedtuple

import requests
import pandas as pd

from .helpers.player_sorting import sort_fname, sort_lname
from .helpers.stat_parser import game_data

class AllPlayers:
    '''A class containing methods for getting nba player data from the codegib
    API and analyzing that data.

    Args:
    None required.
    '''


    def __init__(self):
        _url = 'https://www.codegib.com/api/nba_players'
        self.all_players = requests.get(_url).json()
        self.players_to_analyze = set()


    def search_player_name(self, name):
        '''Search by first name or by last name
        Note: Cannot search by both

        Args:
        name 		 First or last name of player

        Returns:
        players		 A list containing names that match search

        '''
        players = []
        all_players = self.all_players.copy()

        for player in all_players:
            if name.lower() in [part.lower() for part in player.split(' ')]:
                players.append(player)

        return players


    def add_players_to_analyze(self, players):
        '''Add players to the 'players_to_analyze' list

        Args:
        players         An iterable of player names to add (list, tuple, set)
        '''

        if isinstance(players, (list, tuple, set)):
            self.players_to_analyze.update(players)

        return print("The 'players_to_analyze' has been updated.")


    def get_player_stats(self, players=None):
        '''Get stats for all players provided in a list

        Args:
        players         A list of names matching player names provided from
                        NBA players api
                        Default: None (replaces this with 'players_to_analyze')

        Returns:

        '''

        if not players:
            players = self.players_to_analyze.copy()

        _api_url = 'https://www.codegib.com/api/nba_stats'
        player_stats = [requests.get(
                            _api_url, params={ 'player': player }
                        ).json() for player in players]

        self.player_stats = player_stats

        return print("The 'player_stats' json object has been saved.")


    def convert_json_to_pandas(self):
        '''Converts the 'player_stats' json object to a pandas dataframe
        '''

        cols = [
            'player','date','type','home','opponent','team','assists',
            'blocks', 'd_rebounds', 'fg_att', 'fg_made', 'fouls', 'ft_att',
            'ft_made', 'minutes', 'o_rebounds', 'plus_minus', 'points',
            'rebounds', 'steals', 'three_pts_att', 'three_pts_made',
            'turnovers'
        ]

        df = pd.DataFrame(columns=cols)
        to_convert = self.player_stats

        df = pd.concat([
            pd.DataFrame(game_data(name, date, stats))\
            for player in to_convert\
            for name,games in player.items() for game in games\
            for date,stats in game.items()
        ], ignore_index=True)

        self.player_stats = df
        self._get_player_action()

        return print("The 'player_stats' has been saved as a dataframe.")


    def drop_preseason(self):
        mask = self.player_stats['type'] != 'Preseason'
        self.player_stats = self.player_stats.loc[mask]

        self._get_player_action() # overwrite player action with new stats

        return print('Dropped preseason stats')


    def drop_playoffs(self):
        mask = self.player_stats['type'] != 'Playoffs'
        self.player_stats = self.player_stats.loc[mask]

        self._get_player_action() # overwrite player action with new stats

        return print('Dropped playoff stats')


    def drop_regular_season(self):
        mask = self.player_stats['type'] != 'Regular'
        self.player_stats = self.player_stats.loc[mask]

        self._get_player_action() # overwrite player action with new stats

        return print('Dropped regular season stats')


    def _get_player_action(self):
        aggregator = {
            'minutes': ['count', 'sum']
        }

        action = self.player_stats.groupby('player').agg(aggregator)

        PlayerAction = namedtuple('PlayerAction', ('total_games', 'total_minutes'))
        self.player_action = {
            k: PlayerAction(v[0], v[1]) for k,v in action.iterrows()
        }

    def averages_per_player(self):
        pass
