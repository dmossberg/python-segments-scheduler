from segment_scheduler.segment import Segment
import pytest

def test_constructor_valid_input():
    # Arrange
    expected = Segment

    # Act
    actual = Segment(1, 3)

    # Assert
    assert isinstance(actual, expected)
    assert actual.start_time == 1
    assert actual.end_time == 3

def test_constructor_invalid_input_types():
    # Arrange
    expected = TypeError

    # Assert
    with pytest.raises(expected):
        Segment("a", 1)

    with pytest.raises(expected):
        Segment(1, "b")

    with pytest.raises(expected):
        Segment(0.5, 3)

    with pytest.raises(expected):
        Segment(1, 0.5)

    with pytest.raises(expected):
        Segment(None, 1)

    with pytest.raises(expected):
        Segment(1, None)

def test_constructor_invalid_input_values():
    # Arrange
    expected = ValueError

    # Assert
    with pytest.raises(expected):
        Segment(5, 3)