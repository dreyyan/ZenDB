from typing import Optional, List
from .console_utils import error_message, press_to_continue

# [ METHOD ]: Get a 'string' input from the user
def get_str(field: str, restrictions: Optional[List[str]]) -> str:
    str_input: str = input(f"Enter {field} (or press Enter to exit): ").strip()

    # return a blank string if user presses 'Enter' key
    if not str_input:
        return ""
    
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
        user_input = input(f"Enter {field}: ").strip()

        try:
            int_input = int(user_input)
        except ValueError:
            error_message("Invalid input, please enter a valid number")
            press_to_continue()
            continue

        # check restrictions
        if restrictions:
            if "required" in restrictions and user_input == "":
                error_message(f"{field} must not be blank (required)")
                press_to_continue()
                continue

        return int_input