''' rock, paper, scissors game '''


import random


# ================================
# CONFIGURATION
# ================================

MAX_PLAYERS = 3
GAME_TYPE = {"f": "Free For All", "a": "All vs CPU"}
DIFFICULTIES = {
    "q": {"name": "Quick Play", "wins": 1, "best_of": 1},
    "e": {"name": "Easy", "wins": 2, "best_of": 3},
    "m": {"name": "Medium", "wins": 3, "best_of": 5},
    "h": {"name": "Hard", "wins": 4, "best_of": 7}
}
WEAPONS = {
    "r": {"name": "Rock", "beats": "s"},
    "p": {"name": "Paper", "beats": "r"},
    "s": {"name": "Scissors", "beats": "p"},
}


# ================================
# UTILITY
# ================================


def get_valid_response(valid_choices: set, prompt: str, error_msg: list = ["Invalid Input"]) -> str:
    while True:
        response = input(prompt).strip().lower()
        if response not in valid_choices:
            print(random.choice(error_msg))
        else:
            return response


# ================================
# CORE GAME & LOGIC
# ================================

def play_game_loop(size: int, players: int, score_sheet: dict) -> dict:
    while max(score_sheet.values()) < size:
        cpu_attack = random.choice(WEAPON)
        player_attacks = get_player_attacks(players)
        clash_result = get_clash_result(player_attacks, cpu_attack)
        score_sheet = adjust_score_sheet(score_sheet, clash_result)

    return score_sheet


def determine_winner(player_attack: str, cpu_attack:str) -> int:
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


def get_player_attacks(players: int) -> dict:
    player_attacks = {}
    for p in range(1, players + 1):
        player_attacks[f"Player_{p}"] = get_valid_response(WEAPON, f"Player_{p}\nChoose your weapon. [R]ock, [P]aper, or [S]cissors?: ")
    return player_attacks


# ================================
# SCOREKEEPING
# ================================


def adjust_score_sheet(score_sheet: dict, clash_result: dict) -> dict:
    for key in clash_result:
        score_sheet[key] += clash_result[key]
    return score_sheet


def set_up_score_sheet(players: int) -> dict:
    score_sheet = {}
    for p in range(1, players + 1):
        score_sheet[f"Player_{p}"] = 0
    score_sheet["CPU"] = 0
    return score_sheet


# ================================
# GAME SETTINGS
# ================================


def play_new_game_choice() -> bool:
    response = get_valid_response({"y", "n"}, "New Game? [Y]es or [N]o?: ")
    if response == "y":
        return True
    else:
        return False


def get_players() -> int:
    choices_with_brackets = [f"[{i}]" for i in range(1, MAX_PLAYERS + 1)]
    
    valid_keys = [str(i) for i in range(1, MAX_PLAYERS + 1)]
    
    main_text = ", ".join(choices_with_brackets[:-1])
    options_text = f"{main_text}, or {choices_with_brackets[-1]}"
    prompt = f"\nHow many players are playing against me (CPU)? {options_text}?: "

    return int(get_valid_response(valid_keys, prompt))


def get_game_type(players) -> str:
    if players == 1:
        return None
    else:    
        options_list = [f"[{k.upper()}]{v[1:]}" for k, v in GAME_TYPE.items()]
        options_text = "? Or ".join(options_list)
        prompt = f"\n{options_text}?: "

        return get_valid_response(GAME_TYPE, prompt)


def get_game_size() -> int:
    options_list = [f"[{k.upper()}]{v['name'][1:]}" for k, v in DIFFICULTIES.items()]

    options_text = "? ".join(options_list)
    prompt = f"\n{options_text}?: "

    return get_valid_response(DIFFICULTIES, prompt)


# ================================
# MAIN LOOP
# ================================


def main():
    while play_new_game_choice():
        players = get_players()
        game_type = get_game_type()
        size = get_game_size()
        score_sheet = set_up_score_sheet(players)
        score_sheet = play_game_loop(size, players, score_sheet)
        print(score_sheet)
        # display_per_game_results(record, size)

if __name__ == "__main__":
    main()
