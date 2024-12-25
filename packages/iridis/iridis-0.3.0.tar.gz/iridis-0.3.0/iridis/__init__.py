from .color import Color
from .color_print import (
    print_error,
    print_rainbow,
    print_title,
    print_with_color,
)
from .utils import (
    get_number_from_user,
    get_string_from_user,
    has_special_characters,
    has_no_special_characters,
    has_digits,
    has_no_digits,
    is_alpha_only,
    is_not_empty,
)

# Define the public API
__all__ = [
    "Color",
    "print_error",
    "print_rainbow",
    "print_title",
    "print_with_color",
    "get_number_from_user",
    "get_string_from_user",
    "has_special_characters",
    "has_no_special_characters",
    "has_digits",
    "has_no_digits",
    "is_alpha_only",
    "is_not_empty",
]
