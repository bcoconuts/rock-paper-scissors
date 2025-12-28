''' rock, paper, scissors game '''


import random


GAME_SIZE = {"q": 1, "s": 3, "m": 5, "l": 7} #quick, small, medium, large
# BEST_OF_SIZE = GAME_SIZE.values() * 2 - 1
WEAPON_NAME = {"r": "Rock", "p": "Paper", "s": "Scissors"}
WEAPON = ["r", "p", "s"]
BEATS = {"r": "s", "p": "r", "s": "p"}


def get_valid_response(valid_choices: set[str], prompt: str, error_msg: str = "Invalid Input") -> str:
    while True:
        response = input(prompt).strip().lower()
        if response not in valid_choices:
            print(random.choice(error_msg))
        else:
            return response


def determine_winner(player_attack: str, cpu_attack:str) -> bool:
    if BEATS[player_attack] == cpu_attack:
        player_result = 1
        cpu_result = 0
        return player_result, cpu_result
    elif player_attack == cpu_attack:
        player_result = 0
        cpu_result = 0
        return player_result, cpu_result
    else:
        player_result = 0
        cpu_result = 1
        return player_result, cpu_result


def get_clash_result(player_attacks: dict, cpu_attack: str) -> dict:
    clash_result = {}
    for key in player_attacks:
        player_result, cpu_result = determine_winner(player_attacks[key], cpu_attack)
        clash_result[f"{key}"] = player_result
    clash_result["CPU"] = cpu_result
    return clash_result


def play_new_game_choice() -> bool:
    response = get_valid_response(["y", "n"], "New Game? [Y]es or [N]o?: ")
    if response == "y":
        return True
    else:
        return False


def get_game_size() -> int:
    while True:
        size = get_valid_response(["q", "s", "m", "l"], "\n[Q]uick Play? [S]mall? [M]edium? [L]arge?: ")
        return GAME_SIZE[size]


def get_players() -> int:
    while True:
        players = int(get_valid_response(["1", "2", "3"], "How many players are playing against me (CPU)? [1], [2], or [3]?: "))
        return players
      

def set_up_score_sheet(players: int) -> dict:
    score_sheet = {}
    for p in range(1, players + 1):
        score_sheet[f"Player_{p}"] = 0
    score_sheet["CPU"] = 0
    return score_sheet


def get_player_attacks(players: int) -> dict:
    player_attacks = {}
    for p in range(1, players + 1):
        player_attacks[f"Player_{p}"] = get_valid_response(WEAPON, f"Player_{p}\nChoose your weapon. [R]ock, [P]aper, or [S]cissors?: ")
    return player_attacks


def adjust_score_sheet(score_sheet: dict, clash_result: dict) -> dict:
    for key in clash_result:
        score_sheet[key] += clash_result[key]
    return score_sheet


def play_game_loop(size: int, players: int, score_sheet: dict) -> dict:
    while max(score_sheet.values()) < size:
        cpu_attack = random.choice(WEAPON)
        player_attacks = get_player_attacks(players)
        clash_result = get_clash_result(player_attacks, cpu_attack)
        score_sheet = adjust_score_sheet(score_sheet, clash_result)

    return score_sheet


# def display_per_game_results(record, size):
#     user_wins = record[0]
#     cpu_wins = record[1]
#     best_of_size = size + 2
#     if user_wins > cpu_wins:
#         print(f"Nice Job. In a best of {best_of_size} round, you beat me {user_wins} times!\n")
#     else:
#         print(f"Better luck next time. In a best of {best_of_size} round, I beat you {cpu_wins} times!\n")


# def display_total_results(all_user_wins, all_cpu_wins, all_sizes):
#     pass


def main():
    while play_new_game_choice():
        size = get_game_size()
        players = get_players()
        score_sheet = set_up_score_sheet(players)
        score_sheet = play_game_loop(size, players, score_sheet)
        print(score_sheet)
        # display_per_game_results(record, size)

if __name__ == "__main__":
    main()
