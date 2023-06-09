"""This module contains the function to find the minimum number
of points in time"""
import logging
import timeit
from typing import List
from .segment import Segment


def find_minimum_points_in_time(segments: List['Segment']) -> List[int]:
    """
      Given a list of segments, find the minimum number of points in time that
      will cover all segments.

      This function has a linear time complexity of O(n) where n is the number
      of segments in the list.

      Args:
          segments (List[Segment]): A list of segments

      Returns:
          List[int]: A list of integers representing the minimum number of
          points in time that will cover all segments.

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
    logger = logging.getLogger(__name__)

    # If the list of segments is empty, return an empty list
    if not segments:
        return []

    # Check if segments is a list
    if not isinstance(segments, list):
        raise TypeError("Segments must be a list")

    try:
        start_time = timeit.default_timer()

        segments.sort(key=lambda s: s.end_time)

        end_time = timeit.default_timer()
        count = len(segments)
        time_taken = (end_time - start_time) * 1000
        logger.debug(
          "Sorted %d segments in %f ms",
          count, time_taken)

    # Sort function will raise an AttributeError if the list of segments
    # contains an object that doesn't have an end_time attribute, i.e.
    # it's not a Segment object
    except AttributeError as err:
        error_message = str(err)
        logger.error("AttributeError occurred: %s", error_message)

        if "object has no attribute 'end_time'" in error_message:
            raise TypeError("Segments must be a list of Segment objects")

    points_in_time = []
    current_time: int = None

    start_time = timeit.default_timer()
    for segment in segments:

        # Validate that the segment is a Segment object
        if not isinstance(segment, Segment):
            logger.error(
                "Encountered invalid element in the list of type != Segment")
            raise TypeError(
                "All elements in the list must be of type Segment")

        # If the points in time list is empty, add the end_time value of the
        # first segment to it and store a reference to be compared with
        # subsequent segments
        if not points_in_time:
            points_in_time.append(segment.end_time)
            current_time = segment.end_time
            continue

        # If the segment doesn't overlap with the current point in  time,
        # we add a new point in time to the list and update the reference
        if segment.start_time > current_time:
            points_in_time.append(segment.end_time)
            current_time = segment.end_time

    end_time = timeit.default_timer()
    count = len(segments)
    time_taken = (end_time - start_time) * 1000
    logger.debug(
        "Computed minimum points in time for %d segments in %f ms",
        count, time_taken)

    return points_in_time
