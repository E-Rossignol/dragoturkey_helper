import pytest

from text_utils import reverse_text, swap_case


def test_reverse_text():
    assert reverse_text("abc") == "cba"
    assert reverse_text("") == ""
    assert reverse_text(None) == ""


def test_swap_case():
    assert swap_case("AbC") == "aBc"
    assert swap_case("") == ""
    assert swap_case(None) == ""
