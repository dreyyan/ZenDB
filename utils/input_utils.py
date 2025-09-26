from typing import Optional, List
from .console_utils import error_message, press_to_continue

# [ METHOD ]: Get a 'string' input from the user
def get_str(field: str, restrictions: Optional[List[str]]) -> str:
    str_input: str = input(f"Enter {field}: ").strip()

    # check if there are restrictions
    if restrictions:
        # validate user input based on specified restrictions
        # REQUIRED: Blank input
        if "required" in restrictions and str_input == "":
            error_message(f"{field} must not be blank (required)")
            press_to_continue()

    return str_input

# [ METHOD ]: Get an 'integer' input from the user
def get_int(field: str, restrictions: Optional[List[str]] = None) -> int:
    while True:
        user_input: int = int(input(f"Enter {field}: ").strip())

        # check if there are restrictions
        if restrictions:
            # validate user input based on specified restrictions
            # REQUIRED: Blank input
            if "required" in restrictions and not user_input:
                error_message(f"{field} must not be blank (required)")
                press_to_continue()
                continue

        # convert string input to integer to accept 0 as valid input
        try:
            int_input: int = int(user_input)
            return int_input
        except ValueError: # ERROR: Input mismatch
            error_message("Invalid input, please enter a valid number")
            press_to_continue()