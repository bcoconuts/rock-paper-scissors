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
    "r": {"name": "Rock", "beats": "s", "win_action": ["Crushes", "Annihilates", "Breaks", "Pulverizes"], "loss_action": ["is Covered by", "is Surrounded by", "is Consumed by"]},
    "p": {"name": "Paper", "beats": "r", "win_action": ["Covers", "Envelops", "Blocks Out", "Encapsulates"], "loss_action": ["is Sliced by", "is Ripped In Two by", "is Stabbed by"]},
    "s": {"name": "Scissors", "beats": "p", "win_action": ["Decapitates", "Chops", "Cleaves Through", "Shears Through"], "loss_action": ["is Dismantled by", "is Discombobulated by", "is Dulled by"]},
}
WIN_WEIGHT = {
    "standard": 1,
    "none": 0
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
        if not response.isalpha():
            print(alpha_error_msg)
        elif response in invalid_choices:
            print(random.choice(unique_error_msg))
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
    for p1, p2 in itertools.permutations(player_sheet.keys(), 2):
        player_sheet[p1][f"Wins v {p2}"] = 0
        player_sheet[p1][f"Losses v {p2}"] = 0


def create_player_sheet(players: int) -> dict[str, dict[str, int | str]]:
    player_sheet = collect_player_names(players)
    setup_score_tracking(player_sheet)
    return player_sheet


# ================================
# CORE GAME & LOGIC
# ================================


def get_attacks(player_sheet: dict) -> dict:
    round_dict = copy.deepcopy(player_sheet)
    round_dict[CPU][ATTACK] = random.choice(list(WEAPONS.keys()))

    prompt_start = "\nChoose your Weapon."
    prompt_end, valid_keys = construct_prompt_and_keys(WEAPONS)

    for k in list(round_dict.keys())[:-1]:
        weapon_choice = get_valid_response(valid_keys, f"\n{k}! {prompt_start} {prompt_end}")
        round_dict[k][ATTACK] = weapon_choice

    return round_dict


def determine_round_outcome(round_dict: dict) -> None:
    attacks = {k: v[ATTACK] for k, v in round_dict.items()}
    for (name_p1, attack_p1), (name_p2, attack_p2) in itertools.permutations(attacks.items(), 2):
        if attack_p1 == attack_p2:
            continue
        elif WEAPONS[attack_p1]["beats"] == attack_p2:
            round_dict[name_p1][f"Wins v {name_p2}"] += WIN_WEIGHT["standard"]
        else:
            round_dict[name_p1][f"Losses v {name_p2}"] += WIN_WEIGHT["standard"]


def adjust_full_game_sheet(full_game_sheet: dict, round_dict: dict) -> None:
    for overall_stats, round_stats in zip(full_game_sheet.values(), round_dict.values()):
        for k in overall_stats.keys():
            if not isinstance(overall_stats[k], int):
                continue
            elif k in round_stats:
                overall_stats[k] += round_stats[k]


def check_game_over_status(game_type: str, wins_reqd: int, full_game_sheet: dict[str, dict]) -> bool:
    if GAME_TYPE[game_type]["name"] == "Free For All":
        return check_game_over_ffa(wins_reqd, full_game_sheet)
    elif GAME_TYPE[game_type]["name"] == "All vs CPU":
        return check_game_over_allvcpu(wins_reqd, full_game_sheet)
    else:
        return True


def check_game_over_ffa(wins_reqd: int, full_game_sheet: dict) -> bool:
    for stats in full_game_sheet.values():
        win_sum = sum([wins for k, wins in stats.items() if k.startswith("Win")])
        if win_sum >= wins_reqd:
            return False
    return True


def check_game_over_allvcpu(wins_reqd: int, full_game_sheet: dict) -> bool:
    if any(v >= wins_reqd for v in full_game_sheet[CPU].values()):
        return False
    else:
        return True


def play_game_loop(game_type: str, wins_reqd: int, player_sheet: dict) -> dict:
    full_game_sheet = copy.deepcopy(player_sheet)
    round_number = 0
    running = True
    while running:
        round_number += 1
        round_dict = get_attacks(player_sheet)
        determine_round_outcome(round_dict)
        display_round_results(game_type, round_number, round_dict)
        adjust_full_game_sheet(full_game_sheet, round_dict)
        running = check_game_over_status(game_type, wins_reqd, full_game_sheet)
    return full_game_sheet


# ================================
# RESULTS DISPLAY
# ================================


def display_round_results(game_type: str, round_number: int, round_dict: dict) -> None:
    # if GAME_TYPE[game_type]["name"] == "Free For All":
    #     return display_round_results_ffa(round_dict)
    if GAME_TYPE[game_type]["name"] == "All vs CPU":
        return display_round_results_allvcpu(round_number, round_dict)


def display_round_results_allvcpu(round_number: int, round_dict: dict) -> None:
    result_end = f"{CPU}'s {WEAPONS[round_dict[CPU][ATTACK]]['name']}"
    print(f"\nRound {round_number} Results!:")

    for player, result in round_dict.items():
        player_weapon = f"{WEAPONS[result[ATTACK]]['name']}"
        if result.get(f"Losses v {CPU}", None) == WIN_WEIGHT["none"] and result.get(f"Wins v {CPU}", None) == WIN_WEIGHT["none"]:
            print(f"{player}'s {player_weapon} ties with {result_end}")
            print("Draw!\n")
        elif result.get(f"Wins v {CPU}", None) == WIN_WEIGHT["standard"]:
            result_start = f"{random.choice(WEAPONS[result[ATTACK]]['win_action'])}"
            print(f"{player}'s {player_weapon} {result_start} {result_end}")
            print(f"{player} Wins!\n")
        elif result.get(f"Losses v {CPU}", None) == WIN_WEIGHT["standard"]:
            result_start = f"{random.choice(WEAPONS[result[ATTACK]]['loss_action'])}"
            print(f"{player}'s {player_weapon} {result_start} {result_end}")
            print(f"{player} Loses!\n")


# ================================
# MAIN LOOP
# ================================


def main():
    running = True
    while running:
        players, game_type, wins_reqd = get_game_settings()
        player_sheet = create_player_sheet(players)
        full_game_sheet = play_game_loop(game_type, wins_reqd, player_sheet)
        print(full_game_sheet)
        # display_per_game_results(record, size)
        running = play_new_game_choice()

if __name__ == "__main__":
    main()


# ================================
# DEBUG
# ================================

