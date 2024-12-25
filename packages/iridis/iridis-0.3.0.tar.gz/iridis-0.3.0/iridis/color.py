from enum import Enum


class Color(Enum):
    # Regular colors
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"

    # Bold colors
    BOLD_BLACK = "\033[1;30m"
    BOLD_RED = "\033[1;31m"
    BOLD_GREEN = "\033[1;32m"
    BOLD_YELLOW = "\033[1;33m"
    BOLD_BLUE = "\033[1;34m"
    BOLD_PURPLE = "\033[1;35m"
    BOLD_CYAN = "\033[1;36m"
    BOLD_WHITE = "\033[1;37m"

    # High-intensity colors
    HIGH_INT_BLACK = "\033[0;90m"
    HIGH_INT_RED = "\033[0;91m"
    HIGH_INT_GREEN = "\033[0;92m"
    HIGH_INT_YELLOW = "\033[0;93m"
    HIGH_INT_BLUE = "\033[0;94m"
    HIGH_INT_PURPLE = "\033[0;95m"
    HIGH_INT_CYAN = "\033[0;96m"
    HIGH_INT_WHITE = "\033[0;97m"

    # Bold high-intensity colors
    BOLD_HIGH_INT_BLACK = "\033[1;90m"
    BOLD_HIGH_INT_RED = "\033[1;91m"
    BOLD_HIGH_INT_GREEN = "\033[1;92m"
    BOLD_HIGH_INT_YELLOW = "\033[1;93m"
    BOLD_HIGH_INT_BLUE = "\033[1;94m"
    BOLD_HIGH_INT_PURPLE = "\033[1;95m"
    BOLD_HIGH_INT_CYAN = "\033[1;96m"
    BOLD_HIGH_INT_WHITE = "\033[1;97m"

    # Reset
    RESET = "\033[0m"
