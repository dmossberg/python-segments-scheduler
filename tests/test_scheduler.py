from segment_scheduler.segment import *
from segment_scheduler.scheduler import *
import pytest

def test_challenge_case_one_point_in_time():
    # Arrange
    segments = [Segment(1, 3), 
                Segment(2, 5), 
                Segment(3, 6)]
    
    expected = [3]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected
    
def test_challenge_case_two_points_in_time():
    # Arrange
    segments = [Segment(1, 3), 
                Segment(2, 5), 
                Segment(6, 7)]
    
    expected = [3, 7]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_no_overlapping_points():
    # Arrange
    segments = [
        Segment(1, 2),
        Segment(3, 4),
        Segment(5, 6),
    ]
    
    expected = [2, 4, 6]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_no_overlapping_points_descending_order():
    # Arrange
    segments = [
        Segment(5, 6),
        Segment(3, 4),
        Segment(1, 2),
    ]
    
    expected = [2, 4, 6]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_all_overlapping_segments():
    # Arrange
    segments = [
        Segment(1, 5),
        Segment(2, 6),
        Segment(3, 7),
        Segment(4, 8),
        Segment(5, 9)
    ]
    
    expected = [5]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_same_high_value():
    # Arrange
    segments = [
        Segment(1, 5),
        Segment(2, 5),
        Segment(3, 5),
        Segment(4, 5),
        Segment(5, 5)
    ]
    
    expected = [5]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_same_low_value():
    # Arrange
    segments = [
        Segment(1, 1),
        Segment(1, 2),
        Segment(1, 3),
        Segment(1, 4),
        Segment(1, 5)
    ]
    
    expected = [1]

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_empty_list(): 
    # Arrange
    segments = []
    
    expected = []

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_none_input():
    # Arrange
    segments = None
    
    expected = []

    # Act
    actual = find_minimum_points_in_time(segments)

    # Assert
    assert actual == expected

def test_list_of_invalid_type_raises_exception():
    # Arrange
    segments: List[str] = ["1", "2", "3"] 
    
    expected = TypeError

    # Act
    with pytest.raises(expected):
      find_minimum_points_in_time(segments)


def test_all_elements_have_valid_type():
    # Arrange
    segments = [
        Segment(1, 1),
        Segment(1, 2),
        "invalid_element",
        Segment(1, 4),
        Segment(1, 5)
    ]
    
    expected = TypeError

    # Act
    with pytest.raises(expected):
      find_minimum_points_in_time(segments)