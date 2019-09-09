def game_data(player_name, date, values):
    game_data = {
        'player': [player_name],
        'date': [date],
        'type': [values['game_info']['game_type']],
        'home': [values['game_info']['home']],
        'opponent': [values['game_info']['opponent']],
        'team': [values['game_info']['team']],
        'assists': [values['game_stats']['assists']],
        'blocks': [values['game_stats']['blocks']],
        'd_rebounds': [values['game_stats']['d_rebounds']],
        'fg_att': [values['game_stats']['fg_att']],
        'fg_made': [values['game_stats']['fg_made']],
        'fouls': [values['game_stats']['fouls']],
        'ft_att': [values['game_stats']['ft_att']],
        'ft_made': [values['game_stats']['ft_made']],
        'minutes': [values['game_stats']['minutes']],
        'o_rebounds': [values['game_stats']['o_rebounds']],
        'plus_minus': [values['game_stats']['plus_minus']],
        'points': [values['game_stats']['points']],
        'rebounds': [values['game_stats']['rebounds']],
        'steals': [values['game_stats']['steals']],
        'three_pts_att': [values['game_stats']['three_pts_att']],
        'three_pts_made': [values['game_stats']['three_pts_made']],
        'turnovers': [values['game_stats']['turnovers']]
    }
    return game_data
