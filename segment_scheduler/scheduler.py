from typing import List
from .segment import Segment

def find_minimum_points_in_time(segments: List['Segment']) -> List[int]:
  """
    Given a list of segments, find the minimum number of points in time that
    will cover all segments.

    Args:
        segments (List[Segment]): A list of segments

    Returns:
        List[int]: A list of integers representing the minimum number of points in time
        that will cover all segments.

    Raises:
        TypeError: If the segments argument is not a list
        TypeError: If the segments argument is not a list of Segment objects

    Examples:
        >>> find_minimum_points_in_time([
        ...     Segment(1, 3),
        ...     Segment(2, 5),
        ...     Segment(3, 6)
        ... ])
        [3]

        >>> find_minimum_points_in_time([
        ...     Segment(4, 7),
        ...     Segment(1, 3),
        ...     Segment(2, 5),
        ...     Segment(5, 6)
        ... ])
        [3, 6]
  """
  # If the list of segments is empty, return an empty list
  if not segments:
    return []

  # Check if segments is a list
  if not isinstance(segments, list):
    raise TypeError("Segments must be a list")

  # Sort the list of segments by their end value
  sorted_segments: List['Segment'] = []

  try:
    sorted_segments = sorted(segments, key=lambda s: s.end_time)

  except AttributeError as err:
    if "object has no attribute 'end_time'" in str(err):
      raise TypeError("Segments must be a list of Segment objects")
    
  return find_minimum_points_in_time_sorted(sorted_segments)


def find_minimum_points_in_time_sorted(sorted_segments: List['Segment']) -> List[int]:
  """
    Given a sorted list of segments, find the minimum number of points in time that
    will cover all segments.

    Args:
        segments (List[Segment]): A list of segments

    Returns:
        List[int]: A list of integers representing the minimum number of points in time
        that will cover all segments.

    Raises:
        TypeError: If the segments argument is not a list
        TypeError: If the segments argument is not a list of Segment objects

    Examples:
        >>> find_minimum_points_in_time([
        ...     Segment(1, 3),
        ...     Segment(2, 5),
        ...     Segment(3, 6)
        ... ])
        [3]

        >>> find_minimum_points_in_time([
        ...     Segment(4, 7),
        ...     Segment(1, 3),
        ...     Segment(2, 5),
        ...     Segment(5, 6)
        ... ])
        [3, 6]
  """
  # Initialize a list to store the minimum number of points in time
  points_in_time = []
  current_time: int = None

  # Loop through the sorted segments
  for i in range(len(sorted_segments)):
      
      # Get the current segment
      segment = sorted_segments[i]

      # Validate that the segment is a Segment object
      if not isinstance(segment, Segment):
        raise TypeError("All elements in the list must be Segment objects")
  
      # If the points in time list is empty, add the end_time value of the current segment to it.
      # This is the smallest end_time in the list of segments passed in.
      if not points_in_time:
        points_in_time.append(segment.end_time)

        # Store the point in time to be compared with the subsequent segments
        current_time = segment.end_time

        # Continue to the next segment
        continue

      # If the current segment doesn't overlap with the current point in time, we add a new 
      # point in time to the list and update the current point in time to the new value
      if segment.start_time > current_time:

        # Add the end_time value of the current segment to the list of points in time
        points_in_time.append(segment.end_time)

        # Update the point in time to the end_time value of the current segment
        current_time = segment.end_time

  return points_in_time