def is_valid_type(value: any, expected_type: type) -> tuple[bool, str | None]:
    """
    Checks whether a given value matches the expected data type.
    Args:
        value (any): The value to validate.
        expected_type (str): Expected type as a string ("int", "float", "str").
    Returns:
        bool: True if the value matches the expected type or is a valid coercion, False otherwise.
    """
    try:
        expected_type(value)
        if expected_type == int and not float(value).is_integer():
            return False, "Non-integer value"
        return True, None
    except (ValueError, TypeError):
        return False, f"Invalid type: expected {expected_type.__name__}"