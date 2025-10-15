"""Small text utility functions used by the UI pages."""

def reverse_text(s: str) -> str:
    """Return the reversed string. Handles None gracefully."""
    if s is None:
        return ""
    return s[::-1]


def swap_case(s: str) -> str:
    """Swap upper/lower case for the given string. Handles None gracefully."""
    if s is None:
        return ""
    return s.swapcase()
