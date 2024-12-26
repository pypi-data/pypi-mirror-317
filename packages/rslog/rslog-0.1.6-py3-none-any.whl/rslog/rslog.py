import inspect
from datetime import datetime
from .special_strings import error_strings, success_strings, warning_strings

def rslog(message: str) -> None:
    # TODO: Detect if we are running inside a packaged app or not, dont log to console if we are

    if not message:
        return

    # Get the current time in HH:MM:SS format
    timestamp = datetime.now().strftime("%H:%M:%S")
    # Get the name of the calling function
    caller_name = inspect.stack()[1].function

    if caller_name == "<module>":
        caller_name = "main"

    # ANSI escape codes for colors
    yellow = "\033[93m"
    green = "\033[92m"
    red = "\033[91m"
    orange = "\033[33m"
    reset = "\033[0m"

    # Check if the message contains the word "error" (case-insensitive)
    if any(error_string in message.lower() for error_string in error_strings):
        # Make the whole message red
        colored_message = f"{red}{message}{reset}"
    # Check if the message contains the word "warning" (case-insensitive)
    elif any(warning_string in message.lower() for warning_string in warning_strings):
        # Make the whole message orange
        colored_message = f"{orange}{message}{reset}"
    # Check if the message contains the word "success" (case-insensitive)
    elif any(success_string in message.lower() for success_string in success_strings):
        # Make the whole message green
        colored_message = f"{green}{message}{reset}"
    else:
        # Make the whole message the default color
        colored_message = message

    # print the colored timestamp, caller's name, and the message
    print(
        f"{yellow}[{timestamp}]{reset} {green}[{caller_name}]{reset} {colored_message}"
    )
