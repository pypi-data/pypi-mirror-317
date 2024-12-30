def is_valid_id(s: str) -> bool:
    """
    Checks the string for matching the pattern: A-Za-z, 0-9, _
    """
    # use a small hack to avoid performing additional checks
    s = s.replace("_", "A")
    return s.isascii() and s.isalnum()
