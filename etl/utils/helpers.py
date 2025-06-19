from datetime import datetime

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

def parse_date(value: str) -> str:
    """
    Attempts to parse and standardize a date string to 'YYYY-MM-DD' format.
    Args:
        value (str): Raw date string
    Returns:
        str: Standardized date string or original value if parsing fails
    """
    if not isinstance(value, str):
        return value

    value = value.strip()
    date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"]

    for fmt in date_formats:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return value  # Return original if no format matched

def normalize_gender(value: str) -> str:
    """
    Standardizes gender values to 'M', 'F', or 'Other'.
    Args:
        value (str): Raw gender string
    Returns:
        str: Standardized gender
    """
    if not isinstance(value, str):
        return "Other"

    val = value.strip().lower()
    if val in {"m", "male"}:
        return "M"
    elif val in {"f", "female"}:
        return "F"
    else:
        return "Other"

REGION_MAP = {
    "northeast": "Northeast",
    "southeast": "Southeast",
    "midwest": "Midwest",
    "southwest": "Southwest",
    "west": "West"
}

def normalize_region(region: str) -> str:
    if not isinstance(region, str):
        return region
    return REGION_MAP.get(region.strip().lower(), region.strip().title())