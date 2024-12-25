from .color import Color

def print_with_color(*values: object, color: Color) -> None:
    """
    Prints the given values in a specified color.

    :param values: The values to print.
    :param color: The color to use for the text, specified by a Color Enum.
    """
    print(f"{color.value}{' '.join(map(str, values))}{Color.RESET.value}")


def print_error(*values: object) -> None:
    """
    Prints the given values in red to indicate an error message.

    :param values: The values to print, which represent an error message.
    """
    print_with_color(*values, color=Color.RED)


def print_title(*values: object) -> None:
    """
    Prints the given values in green to indicate a title or header.

    :param values: The values to print, representing the title or header text.
    """
    print_with_color(*values, color=Color.GREEN)


def print_rainbow(*values: object) -> None:
    """
    Prints the provided values in a rainbow color pattern, grouping characters
    based on the length of the text (excluding spaces) divided by the number of rainbow colors.

    :param values: The values to be printed, each group of characters colored sequentially in rainbow colors.
    """
    rainbow_colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE]
    text = " ".join(map(str, values))

    # Remove spaces for the color application logic.
    non_space_chars = [char for char in text if char != " "]
    group_size = max(1, len(non_space_chars) // len(rainbow_colors))  # Ensure at least one character per group.

    colored_text = []
    non_space_index = 0  # Tracks position in non-space characters.

    for char in text:
        if char == " ":
            # Append spaces as-is without color.
            colored_text.append(char)
        else:
            # Determine the color for non-space characters.
            color_index = (non_space_index // group_size) % len(rainbow_colors)
            colored_text.append(f"{rainbow_colors[color_index].value}{char}")
            non_space_index += 1

    print("".join(colored_text) + Color.RESET.value)
