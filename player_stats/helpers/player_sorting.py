def sort_fname(player_list):
    player_list.sort(key = lambda player: player.split(' ')[0])
    return player_list

def sort_lname(player_list):
    player_list.sort(key = lambda player: player.split(' ')[1])
    return player_list
