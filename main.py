''' rock, paper, scissors game '''


import random


# ================================
# CONFIGURATION
# ================================

MAX_PLAYERS = 3
NEW_GAME_CHOICES = {
    "y": {"name": "Yes"}, #yes must appear in first slot
    "n": {"name": "No"}
}
GAME_TYPE = {
    "f": {"name": "Free For All"}, #default game type must appear in first slot
    "a": {"name": "All vs CPU"}
}
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


def construct_prompt_ending(keys: list[str]) -> str:
    keys_with_brackets = [f"[{i[0].upper()}]{i[1:]}" if len(i) > 1 else f"[{i.upper()}]" for i in keys]
    main_text = ", ".join(keys_with_brackets[:-1])
    if len(keys_with_brackets) == 2:
        main_text = main_text.__add__(" or")
    elif len(keys_with_brackets) > 2:
        main_text = main_text.__add__(", or")
    prompt_end = f"{main_text} {keys_with_brackets[-1]}?: "
    return prompt_end


def construct_prompt_and_keys(selection: int | dict) -> tuple[str, set[str]]:
    '''returns a list of tuple from a dictionary where the key == "name"
    '''    
    if type(selection) == int:
        valid_input_list = [str(i) for i in range(1, selection + 1)]
        prompt_end = construct_prompt_ending(valid_input_list)
        valid_keys = set(valid_input_list)
        return prompt_end, valid_keys
    else:
        valid_input_list = [f"{selection[k]['name']}" for k in selection] # pyright: ignore[reportIndexIssue, reportGeneralTypeIssues]
        prompt_end = construct_prompt_ending(valid_input_list)
        valid_keys = set(i[0].lower() for i in valid_input_list)
        return prompt_end, valid_keys


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
        for p in range(1, players + 1)
    score_sheet["CPU"] = 0
    return score_sheet


# ================================
# GAME SETTINGS
# ================================


def get_players() -> int:
    prompt_start = "\nHow many players are playing against me (CPU)?"
    prompt_end, valid_keys = construct_prompt_and_keys(MAX_PLAYERS)

    response = int(get_valid_response(valid_keys, f"{prompt_start} {prompt_end}"))
    return response


def get_game_type(players) -> str:  
    if players == 1:
        game_types = [f"{k}" for k in GAME_TYPE]
        return game_types[0]
    else:
        prompt_start = "\nWhat kind of game would you like to play?"
        prompt_end, valid_keys = construct_prompt_and_keys(GAME_TYPE)

        response = get_valid_response(valid_keys, f"{prompt_start} {prompt_end}")
        return response


def get_game_size() -> int:
    prompt_start = "\nWant something fast or challenging?"
    prompt_end, valid_keys = construct_prompt_and_keys(DIFFICULTIES)

    response = get_valid_response(valid_keys, f"{prompt_start} {prompt_end}")
    return DIFFICULTIES[response]["wins"]


def play_new_game_choice() -> str:
    prompt_start = "\nNew game?"
    prompt_end, valid_keys = construct_prompt_and_keys(NEW_GAME_CHOICES)

    response = get_valid_response(valid_keys, f"{prompt_start} {prompt_end}")
    return response

def get_game_settings():
    new_game_choice_list = [f"{k}" for k in NEW_GAME_CHOICES]
    new_game = play_new_game_choice()
    if new_game == new_game_choice_list[0]:
        players = get_players()
        game_type = get_game_type(players)
        wins_reqd = get_game_size()
        return players, game_type, wins_reqd
    else:
        return


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
