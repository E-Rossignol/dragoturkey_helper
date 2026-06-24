def reverse_text(s: str) -> str:
    if s is None:
        return ""
    return s[::-1]


def swap_case(s: str) -> str:
    if s is None:
        return ""
    return s.swapcase()
