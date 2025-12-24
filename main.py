''' rock, paper, scissors game - barebones '''


import random


QUICK = 1
EASY = 3
MEDIUM = 5
HARD = 7


def _get_valid_weapon(prompt: str, error_msg: str = "Invalid Input") -> str:
    """Get valid input from user.
    
    Repeatedly prompts until user enters desired value.
    
    Args:
        prompt: The message displayed to the user.
        error_msg: Message shown for invalid input.
    
    Returns:
        A string: 'r' (rock), 'p' (paper), or 's' (scissors).
    """
    while True:
        weapon = input(prompt).strip().lower()
        if weapon not in ("r", "p", "s"):
            print(random.choice(error_msg))
        else:
            return weapon


def _get_valid_yes_no(prompt: str, error_msg: str = "Invalid Input") -> str:
    """Get valid input from user.
    
    Repeatedly prompts until user enters desired value.
    
    Args:
        prompt: The message displayed to the user.
        error_msg: Message shown for invalid input.
    
    Returns:
        A string: 'y' (yes), or 'n' (no).
    """
    while True:
        response = input(prompt).strip().lower()
        if response not in ("y", "n"):
            print(random.choice(error_msg))
        else:
            return response


def _get_valid_difficulty(prompt: str, error_msg: str = "Invalid Input") -> str:
    """Get valid input from user.
    
    Repeatedly prompts until user enters desired value.
    
    Args:
        prompt: The message displayed to the user.
        error_msg: Message shown for invalid input.
    
    Returns:
        A string: 'q' (quick), e' (easy), 'm' (medium), or 'h' (hard).
    """
    while True:
        difficulty = input(prompt).strip().lower()
        if difficulty not in ("q", "e", "m", "h"):
            print(random.choice(error_msg))
        else:
            return difficulty


def _get_clash_result(user_attack: str, cpu_attack: str) -> tuple:
    """Check which input/attack wins the game.
    
    Args:
        prompt: The input message displayed to the user, used to collect the user's weapon.
        cpu_weapon: CPU's weapon.
    
    Returns:
        A tuple: (User win (1, 0), CPU win (0, 1), or Draw (0, 0)).
    """
    if user_attack == cpu_attack:
        print("Draw!")
        clash_result = (0, 0)
        return clash_result
    elif user_attack == "r" and cpu_attack == "p":
        print("I Win!!! Paper beats Rock")
        clash_result = (0, 1)
        return clash_result
    elif user_attack == "r" and cpu_attack == "s":
        print("You Win... Rock beats Scissors")
        clash_result = (1, 0)
        return clash_result
    elif user_attack == "p" and cpu_attack == "r":
        print("You Win... Paper beats Rock")
        clash_result = (1, 0)
        return clash_result
    elif user_attack == "p" and cpu_attack == "s":
        print("I Win!!! Scissors beats Paper")
        clash_result = (0, 1)
        return clash_result
    elif user_attack == "s" and cpu_attack == "r":
        print("I Win!!! Rock beats Scissors")
        clash_result = (0, 1)
        return clash_result
    else:
        print("You Win... Scissors beats Paper")
        clash_result = (1, 0)
        return clash_result


def get_game_settings() -> int:
    """User selects what size game they would like to play. Best of X + 2.
    
    Args: n/a
    
    Returns:
        An int: Size of game (best of x + 2).
    """    
    while True:
        difficulty = _get_valid_difficulty("\n[Q]uick Play? [E]asy? [M]edium? [H]ard?: ")
        if difficulty == "q":
            size = QUICK
            return size
        elif difficulty == "e":
            size = EASY
            return size
        elif difficulty == "m":
            size = MEDIUM
            return size
        else:
            size = HARD
            return size


def play_game_loop(size):
    record = (0, 0)
    cpu_weapons = ["r", "p", "s"]
    while record[0] < size and record[1] < size:
        cpu_attack = random.choice(cpu_weapons)
        user_attack = _get_valid_weapon("\nChoose your weapon. [R]ock, [P]aper, or [S]cissors?: ")
        clash_result = _get_clash_result(user_attack, cpu_attack)
        record = (record[0] + clash_result[0], record[1] + clash_result[1])
        
    return record


def display_per_game_results(record, size):
    user_wins = record[0]
    cpu_wins = record[1]
    best_of_size = size + 2
    if user_wins > cpu_wins:
        print(f"Nice Job. In a best of {best_of_size} round, you beat me {user_wins} times!\n")
    else:
        print(f"Better luck next time. In a best of {best_of_size} round, I beat you {cpu_wins} times!\n")


def display_total_results(all_user_wins, all_cpu_wins, all_sizes):
    pass


def main():
    while True:
        response = _get_valid_yes_no("New Game? [Y]es or [N]o?: ")
        if response == "y":
            size = get_game_settings()
            record = play_game_loop(size)
            display_per_game_results(record, size)
        else:
            break

if __name__ == "__main__":
    main()
