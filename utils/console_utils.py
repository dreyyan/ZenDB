# Imports: Utilities


# Imports: Standard
import os, time, sys, shutil
from typing import Optional

""" UTILITY: Display UI """
# UTILITY: Display text with a typing effect
def character_delay_animation(string_input, delay_seconds: Optional[float] = None):
    for char in string_input:
        print(char, end="", flush=True)

        if delay_seconds:
            time.sleep(delay_seconds)
    print()

# [ UTILITY ]: Display 'symbol' 'n' times
def display_format(n: int, symbol: str) -> None:
    print(symbol * n)

# UTILITY: Display function name in the main menu
def display_function(index, function_name, delay_seconds: Optional[float] = None):
    print(f"[{index}] {function_name}")
    if delay_seconds:
        time.sleep(0.1)

# UTILITY: Display header for the interface with appropriate formatting
def display_header(title_name: str, interface_name: str, width: Optional[int] = None, symbol: str = "=", delay_seconds: Optional[float] = None):
    if width is None:
        width = shutil.get_terminal_size((80, 20)).columns

    text = f"{title_name}: [ {interface_name} ]"
    total_symbol_space = width - len(text)
    left_symbols = total_symbol_space // 2
    right_symbols = total_symbol_space - left_symbols

    print(f"{symbol * left_symbols} {text} {symbol * right_symbols}")
    
    if delay_seconds:
        time.sleep(delay_seconds)

# UTILITY: Display formatted success message to the user
def success_message(message):
    print(f"[SUCCESS] {message}", flush=True)

# UTILITY: Display formatted informational message to the user
def info_message(message):
    print(f"[INFO] {message}", flush=True)

# UTILITY: Display formatted error message to the user
def error_message(message):
    print(f"[ERROR] {message}", flush=True)

# UTILITY: Display formatted error message to the user /w delay
def error_message_with_delay(message, delay_seconds: float):
    print(f"[ERROR] {message}", end="", flush=True)

    if delay_seconds:
        time.sleep(delay_seconds)

    sys.stdout.write('\033[1A') # Move cursor up 1 line
    sys.stdout.write('\r\033[K\n\r\033[K\033[1A') # Clear error input and error message
    sys.stdout.flush()

# UTILITY: Insert 'n' spaces
def insert_spaces(n):
    print(' ' * (n + 1), end="")
    
# UTILITY: Display text with a line effect
def line_delay_animation(string_input, delay_seconds: Optional[float] = None):
    print(string_input)

    if delay_seconds:
        time.sleep(delay_seconds)

""" UTILITY: Helper UI """
# [ UTILITY ]: Clear console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# [ UTILITY ]: Press any key to continue
def press_to_continue():
    input("Press any key to continue...")

# [ UTILITY ]: Center string
def display_center(string: str, width: int, symbol: str = " "):
    print(string.center(width, symbol))