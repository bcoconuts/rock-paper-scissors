''' rock, paper, scissors game - barebones '''

import random


def _get_valid_weapon(prompt: str, error_msg: str = "Invalid Input") -> str:
    """Get valid input from user.
    
    Repeatedly prompts until user enters desired value.
    
    Args:
        prompt: The message displayed to the user.
        error_msg: Message shown for invalid input.
    
    Returns:
        A string: 'r' (rock), 'p' (paper), or 's' (scissors).
    """
    while True
        weapon = input(prompt).strip().lower()
        if weapon not in ("r", "p", "s"):
            print(random.choice(error_msg))
        else:
            return weapon


def _get_valid_new_game_response(prompt: str, error_msg: str = "Invalid Input") -> str:
    """Get valid input from user.
    
    Repeatedly prompts until user enters desired value.
    
    Args:
        prompt: The message displayed to the user.
        error_msg: Message shown for invalid input.
    
    Returns:
        A string: 'y' (yes), or 'n' (no).
    """
    while True
        new_game_response = input(prompt).strip().lower()
        if new_game_response not in ("y", "n"):
            print(random.choice(error_msg))
        else:
            return new_game_response


def get_game_settings():
    #TODO


def play_game_loop(size):
    #TODO


def display_per_game_results(wins, losses, size)
    #TODO


def display_total_results(all_wins, all_losses, all_sizes)
    #TODO


def main():
    while True
        new_game_response = _get_valid_new_game_response("New Game? (y/n): ")
        if new_game_response == y:
            size = get_game_settings()
            wins, losses = play_game_loop(size)
            all_wins, all_losses, all_sizes = display_per_game_results(wins, losses, size)
        else:
            break
    display_total_results(all_wins, all_losses, all_sizes)


if __name__ == "__main__":
    main()
