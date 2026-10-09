"""Tests for pure helper functions in run_tracking.py."""

from run_tracking import color_for_id


def test_color_for_id_deterministic() -> None:
    """Kiểm tra color_for_id luôn trả về cùng một màu cho cùng một track_id."""
    color1 = color_for_id(1)
    color2 = color_for_id(1)
    assert color1 == color2
    assert len(color1) == 3
    assert all(64 <= c <= 254 for c in color1)


def test_color_for_id_different_ids() -> None:
    """Kiểm tra hai track_id khác nhau sinh ra hai màu khác nhau."""
    color1 = color_for_id(1)
    color2 = color_for_id(2)
    assert color1 != color2
