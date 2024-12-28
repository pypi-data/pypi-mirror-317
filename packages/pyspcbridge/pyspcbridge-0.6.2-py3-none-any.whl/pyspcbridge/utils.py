def _load_enum(enum, value, default=None):
    """Parse an enum with fallback."""
    try:
        return enum(value)
    except ValueError:
        return default
