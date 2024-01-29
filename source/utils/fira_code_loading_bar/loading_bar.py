"""
Module for generating loading bars.

This module provides a function, generate_loading_bar, for creating loading bars
based on the current progress.
"""


def generate_loading_bar(current_value: float, total_value: float, bar_length: int = 100) -> str:
    """
    Generate a loading bar string based on the current progress.

    Args:
        current_value (float): The current value of the progress.
        total_value (float): The total value representing the completion of the task.
        bar_length (int, optional): The length of the loading bar. Default is 100.

    Returns:
        str: A string representation of the loading bar reflecting the current progress.

    """
    start_empty_char = "\uEE00"
    mid_empty_char = "\uEE01"
    end_empty_char = "\uEE02"

    start_filled_char = "\uEE03"
    mid_filled_char = "\uEE04"
    end_filled_char = "\uEE05"

    progress: float = (current_value / total_value) * bar_length

    # building the string
    loading_bar = start_empty_char + \
        (mid_empty_char * (bar_length - 2)) + end_empty_char

    # filling the string correctly
    string_list = list(loading_bar)

    # +1 to ensure it gets filled (i dont fully comprehend nor care why this fix is needed)
    for i_char in range(int(progress+1)):
        char: str = string_list[i_char]
        if char == start_empty_char:
            string_list[i_char] = start_filled_char
        elif char == mid_empty_char:
            string_list[i_char] = mid_filled_char
        elif char == end_empty_char:
            string_list[i_char] = end_filled_char

    return ''.join(string_list)
