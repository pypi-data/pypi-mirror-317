DEFAULT_STOP_HHMM = ''
DEFAULT_MIN_DELAY_SECONDS = 120
DEFAULT_MAX_DELAY_SECONDS = 180
DEFAULT_MIN_NUM_WORDS = 1
DEFAULT_MAX_NUM_WORDS = 10
DEFAULT_SHOW_TIMESTAMP = False

HELP_STOP_HHMM = f"Automatically stop the simulation at the provided time, example '1700'.\nDefault: {DEFAULT_STOP_HHMM if DEFAULT_STOP_HHMM else 'Empty'}"
HELP_MIN_DELAY_SECONDS = f"Minimum delay seconds between each new line.\nDefault: {DEFAULT_MIN_DELAY_SECONDS}"
HELP_MAX_DELAY_SECONDS = f"Maximum delay seconds between each new line.\nDefault: {DEFAULT_MAX_DELAY_SECONDS}"
HELP_MIN_NUM_WORDS = f"Minimum number of words to type per line.\nDefault: {DEFAULT_MIN_NUM_WORDS}"
HELP_MAX_NUM_WORDS = f"Maximum number of words to type per line.\nDefault: {DEFAULT_MAX_NUM_WORDS}"
HELP_SHOW_TIMESTAMP = f"Type out the timestamp in front of the line to keep track of the time.\nDefault: {DEFAULT_SHOW_TIMESTAMP}"
