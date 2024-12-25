import re
from typing import Callable, List
from .color_print import print_error


def get_number_from_user(
    input_text: str = "Vložte číslo: ",
    error_message: str = "Špatný vstup, zkuste znova!",
    conditions: List[Callable[[float], bool]] = [],
) -> float:
    """
    Prompts the user for a number input and validates it against optional conditions.

    :param input_text: The prompt text to display when asking for input (default is in Czech: "Vložte číslo").
    :param error_message: The error message to display in red in case of invalid input (default is in Czech: "Špatný vstup, zkuste znova!").
    :param conditions: A list of boolean conditions to validate the number against. If any condition fails, the error message is shown.
    :return: The valid number entered by the user.
    """
    while True:
        try:
            # prompt the user and attempt to convert the input to a float
            number = float(input(input_text))

            # validate against conditions if provided
            if not all(condition(number) for condition in conditions):
                print_error(error_message)
                continue

            # return the valid number
            return number
        except ValueError:
            print_error(error_message)


def get_string_from_user(
    input_text: str,
    error_message: str = "Špatný vstup, zkuste znova!",
    conditions: List[Callable[[str], bool]] = [],
) -> str:
    """
    Prompts the user to input a string and validates it against specified conditions.

    :param input_text: The text to display when prompting the user for input.
    :param error_message: The error message to display in red in case of invalid input (default is in Czech: "Špatný vstup, zkuste znova!").
    :param conditions: A list of functions that each take a string and return a boolean. If any condition fails, the error message is shown.
    :return: A valid string that satisfies all the specified conditions.
    """
    while True:
        try:
            # prompt the user to enter a string
            string = input(input_text)

            # validate against conditions if provided
            if not all(condition(string) for condition in conditions):
                print_error(error_message)
                continue

            # return the valid string
            return string
        except ValueError:
            print_error(error_message)


def is_not_empty(string: str) -> bool:
    return bool(string.strip())


def is_alpha_only(string: str) -> bool:
    return string.isalpha()


def has_digits(string: str) -> bool:
    return any(char.isdigit() for char in string)


def has_no_digits(string: str) -> bool:
    return not has_digits(string)


def has_special_characters(string: str) -> bool:
    return bool(re.search(r"[^a-zA-Z0-9\s]", string))


def has_no_special_characters(string: str) -> bool:
    return not has_special_characters(string)

def is_valid_utf8(string: str) -> bool:
    try:
        string.encode("utf-8")
        return True
    except UnicodeEncodeError:
        return False
