''' rock, paper, scissors game '''


import itertools
import random
import copy


# ================================
# CONFIGURATION
# ================================

CPU = "CPU"
ATTACK = "Attack"
SINGLE_PLAYER = 1
MAX_PLAYERS = 3
DEFAULT_CHOICES = {
    "game_type": "f", # free for all set as default game type value
    "new_game_choice": "y" # yes set as default new_game_choice value
}
NEW_GAME_CHOICES = {
    "y": {"name": "Yes"},
    "n": {"name": "No"}
}
GAME_TYPE = {
    "f": {"name": "Free For All"},
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
OUTCOMES = {
    "win": 1,
    "draw": 0,
    "loss": -1
}


# ================================
# UTILITY
# ================================

def get_valid_response(valid_choices: set, prompt: str, case=str.lower) -> str:
    error_msg = [
        "Invalid Input.",
        "Try Again.",
        "Alright, No More Monkey Business!"
    ]
    while True:
        response = case(input(prompt).strip())
        if response not in valid_choices:
            print(random.choice(error_msg))
        else:
            return response


def get_unique_alpha_response(invalid_choices: set, prompt: str, case=str.lower) -> str:
    unique_error_msg = [
        "Already Taken!",
        "That cant be right. I already have that one!"
    ]
    alpha_error_msg = "Must be alphabetical only. No numbers or special chars."
    while True:
        response = case(input(prompt).strip())
        if response in invalid_choices and response.isalpha():
            print(random.choice(unique_error_msg))
        elif not response.isalpha():
            print(alpha_error_msg)
        else:
            return response


def construct_prompt_ending(keys: list[str]) -> str:
    keys_with_brackets = [f"[{i[0].upper()}]{i[1:]}" if len(i) > 1 else f"[{i.upper()}]" for i in keys]
    main_text = ", ".join(keys_with_brackets[:-1])
    if len(keys_with_brackets) == 2:
        main_text = main_text + " or"
    elif len(keys_with_brackets) > 2:
        main_text = main_text + ", or"
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
        valid_input_list = [selection[k]['name'] for k in selection] # pyright: ignore[reportIndexIssue, reportGeneralTypeIssues]
        prompt_end = construct_prompt_ending(valid_input_list)
        valid_keys = set(i[0].lower() for i in valid_input_list)
        return prompt_end, valid_keys


def play_new_game_choice() -> bool:
    prompt_start = "\nNew game?"
    prompt_end, valid_keys = construct_prompt_and_keys(NEW_GAME_CHOICES)

    response = get_valid_response(valid_keys, f"{prompt_start} {prompt_end}")

    if response == DEFAULT_CHOICES["new_game_choice"]:
        return True
    else:
        return False


# ================================
# CORE GAME & LOGIC
# ================================


# def get_free_for_all_results():
#     pass


# def play_game_loop(size: int, players: int, score_sheet: dict) -> dict:
#     while max(score_sheet.values()) < size:
#         cpu_attack = random.choice(WEAPON)
#         player_attacks = get_player_attacks(players)
#         clash_result = get_clash_result(player_attacks, cpu_attack)
#         score_sheet = adjust_score_sheet(score_sheet, clash_result)

#     return score_sheet


# def get_clash_result(player_attacks: dict, cpu_attack: str) -> dict:
#     clash_result = {}
#     for key in player_attacks:
#         player_result, cpu_result = determine_winner(player_attacks[key], cpu_attack)
#         clash_result[f"{key}"] = player_result
#     clash_result["CPU"] = cpu_result
#     return clash_result


def get_attacks(score_sheet: dict) -> dict:
    round_dict = copy.deepcopy(score_sheet)
    round_dict[CPU][ATTACK] = random.choice(list(WEAPONS.keys()))

    prompt_start = "\nChoose your Weapon."
    prompt_end, valid_keys = construct_prompt_and_keys(WEAPONS)

    for k in list(round_dict.keys())[:-1]:
        weapon_choice = get_valid_response(valid_keys, f"\n{k}! {prompt_start} {prompt_end}")
        round_dict[k][ATTACK] = weapon_choice

    return round_dict


def determine_round_outcome(round_dict: dict) -> dict:
    attacks = {k: v[ATTACK] for k, v in round_dict.items()}
    for (name_p1, attack_p1), (name_p2, attack_p2) in itertools.combinations(attacks.items(), 2):
        if attack_p1 == attack_p2:
            continue
        elif WEAPONS[attack_p1]["beats"] == attack_p2:
            round_dict[name_p1][f"Wins v {name_p2}"] += OUTCOMES["win"]
        else:
            round_dict[name_p1][f"Wins v {name_p2}"] += OUTCOMES["loss"]
    return round_dict

# def adjust_score_sheet():
#     pass


# ================================
# GAME SETUP
# ================================


def collect_player_names(players: int) -> dict[str, dict[str, int | str]]:
    player_sheet = {}
    name_set = set()
    for p in range(1, players + 1):
        name = get_unique_alpha_response(name_set, f"\nWhat is Player {p}'s name?: ", str.title)
        player_sheet[name] = {}
        name_set.add(name)
    player_sheet[CPU] = {}

    return player_sheet


def setup_score_tracking(player_sheet: dict[str, dict[str, int | str]]) -> None:
    for p1, p2 in itertools.combinations(player_sheet.keys(), 2):
        player_sheet[p1][f"Wins v {p2}"] = 0

def setup_attack_tracking(player_sheet: dict[str, dict[str, int | str]]) -> None:
    for k in player_sheet:
        player_sheet[k][ATTACK] = ""

def create_score_sheet(players: int) -> dict[str, dict[str, int | str]]:
    score_sheet = collect_player_names(players)
    setup_score_tracking(score_sheet)
    return score_sheet

# ================================
# GAME SETTINGS
# ================================


def get_players() -> int:
    prompt_start = "\nHow many players are playing against me (CPU)?"
    prompt_end, valid_keys = construct_prompt_and_keys(MAX_PLAYERS)

    response = int(get_valid_response(valid_keys, f"{prompt_start} {prompt_end}"))
    return response


def get_game_type(players: int) -> str:  
    if players == SINGLE_PLAYER:
        return DEFAULT_CHOICES["game_type"]
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


def get_game_settings():
    players = get_players()
    game_type = get_game_type(players)
    wins_reqd = get_game_size()
    return players, game_type, wins_reqd


# ================================
# MAIN LOOP
# ================================


def main():
    running = True
    while running:
        players, game_type, wins_reqd = get_game_settings()
        score_sheet = create_score_sheet(players)
        attack_dict = get_attacks(score_sheet)
        print(determine_round_outcome(attack_dict))
        # display_per_game_results(record, size)
        running = play_new_game_choice()

if __name__ == "__main__":
    main()
