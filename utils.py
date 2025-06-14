def selection_sort(game_list, reverse=False):
    n = len(game_list)
    for i in range(n):
        idx = i
        for j in range(i+1, n):
            if (game_list[j] < game_list[idx]) != reverse:
                idx = j
        game_list[i], game_list[idx] = game_list[idx], game_list[i]
    return game_list

def sort_by_length(game_list):
    n = len(game_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if len(game_list[j]) > len(game_list[j+1]):
                game_list[j], game_list[j+1] = game_list[j+1], game_list[j]
    return game_list

def search_game(game_list, target):
    for game in game_list:
        if game.lower() == target.lower():
            return game
    return None
