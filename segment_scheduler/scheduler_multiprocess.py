import multiprocessing
import itertools
import os
from typing import List
from .segment import Segment
from .scheduler import find_minimum_points_in_time_sorted

MIN_CHUNK_SIZE = 1000

def find_minimum_points_in_time(segments: List['Segment']) -> List[int]:
    """
      Given a list of segments, find the minimum number of points in time that
      will cover all segments. As the segment processing is CPU-bound, this
      method uses multiprocessing to parallelize the processing of segments.

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

    # Get number of CPU cores on the current machine
    num_cores = multiprocessing.cpu_count()

    # Split the list of segments into num_cores chunks in order
    # to parallelize the processing of segments
    chunks = __split_list_in_chunks(sorted_segments, num_cores)

    # Create a lock to synchronize access to the points_in_time list
    lock = multiprocessing.Lock()

    # Create a shared manager object
    manager = multiprocessing.Manager()

    # Create a shared list
    shared_points_in_time = manager.dict()

    # Run each chunk in a background process
    processes = []
    for chunk in chunks:
        # Get the index of the current chunk
        index = chunks.index(chunk)

        process = multiprocessing.Process(
            target=__process_chunk, args=(chunk, index, shared_points_in_time, lock))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Concatenate the points_in_time lists from each process and check for
    # points in time that overlap between processes
    combined_points_in_time: List[int] = []

    # Copy the shared points_in_time inmutable dict to a mutable dict
    points_in_time = shared_points_in_time.copy()

    for i in range(len(points_in_time)):
        print(f"Process {i}: {points_in_time[i]}")

    for i in range(len(points_in_time)):
        if i == len(points_in_time) - 1:
            combined_points_in_time.extend(points_in_time[i])
            break

        if len(points_in_time[i]) == 0:
            continue

        # Add all points in time from the current process except the last one
        subset = points_in_time[i][:-1]
        combined_points_in_time.extend(subset)

        # Get the last point in time from the current process
        last_point_in_time_current = points_in_time[i][-1]

        # Remove the last point in time from the list
        points_in_time[i].remove(last_point_in_time_current)

        # Get the first point in time from the next process
        first_point_in_time_next = points_in_time[i + 1][0]

        # Remove the last point in time from the list
        points_in_time[i + 1].remove(first_point_in_time_next)

        if last_point_in_time_current == first_point_in_time_next:
            combined_points_in_time.append(last_point_in_time_current)
            continue

        # Get all Segments that overlap with the last point in time
        last_overlapping_segments = __get_overlapping_segments(
            chunks[i], last_point_in_time_current, True)

        # Get all Segments that overlap with the first point in time
        first_overlapping_segments = __get_overlapping_segments(
            chunks[i + 1], first_point_in_time_next)

        # print(f"Last overlapping [{i}]: ")
        # for segment in last_overlapping_segments:
        #     print(f"Segment({segment.start_time}, {segment.end_time})")

        # print(f"First overlapping [{i+1}]:")
        # for segment in first_overlapping_segments:
        #     print(f"Segment({segment.start_time}, {segment.end_time})")

        # Concatenate the two list of overlapping segments
        overlapping_segments = last_overlapping_segments + first_overlapping_segments

        # print(f"last_overlapping_segments segments: ")
        # for segment in last_overlapping_segments:
        #     print(f"Segment({segment.start_time}, {segment.end_time})")

        # print(f"first_overlapping_segments segments: ")
        # for segment in first_overlapping_segments:
        #     print(f"Segment({segment.start_time}, {segment.end_time})")

        overlapping_points_in_time = find_minimum_points_in_time_sorted(overlapping_segments)
        # print(f"Optimized points in time: {overlapping_points_in_time}")

        for point in overlapping_points_in_time:
            if len(points_in_time[i + 1]) == 0:
                combined_points_in_time.append(point)
                continue
            if point < points_in_time[i + 1][0]:
                combined_points_in_time.append(point)

    return combined_points_in_time


def __get_overlapping_segments(segments: List['Segment'], point_in_time: int, descending_order: bool = False) -> List['Segment']:
    """
      Given a list of segments and a point in time, return a list of segments
      that overlap with the point in time.

      Args:
          segments (List[Segment]): A list of segments
          point_in_time (int): A point in time
          descending_order (bool): If True, the list of segments will be evaluated in descending order

      Returns:
          List[Segment]: A list of segments that overlap with the point in time

      Raises:
          TypeError: If the segments argument is not a list
          TypeError: If the segments argument is not a list of Segment objects
          TypeError: If the point_in_time argument is not an integer

      Examples:
          >>> __get_overlapping_segments([
          ...     Segment(1, 3),
          ...     Segment(2, 5),
          ...     Segment(4, 6)
          ... ], 3)
          [Segment(1, 3), Segment(2, 5)]
    """
    # Check if segments is a list
    if not isinstance(segments, list):
        raise TypeError("Segments must be a list")

    # Check if segments is a list of Segment objects
    for segment in segments:
        if not isinstance(segment, Segment):
            raise TypeError("Segments must be a list of Segment objects")

    # Check if point_in_time is an integer
    if not isinstance(point_in_time, int):
        raise TypeError("point_in_time must be an integer")

    overlapping_segments = []

    if descending_order:
        for i in range(len(segments) - 1, 0, -1):
            segment = segments[i]

            if segment.start_time <= point_in_time and segment.end_time >= point_in_time:
                overlapping_segments.insert(0, segment)
            else:
                break
        
        return overlapping_segments

    for segment in segments:
        if segment.start_time <= point_in_time and segment.end_time >= point_in_time:
            overlapping_segments.append(segment)
        else:
            break

    return overlapping_segments


def __process_chunk(sorted_segments: List['Segment'], index, points_in_time: dict, lock):
    # Print the start_time and end_time of each segment in the chunk
    print(f"Chunk: {index}, Count: {len(sorted_segments)}, Low: {sorted_segments[0].end_time}, High: {sorted_segments[-1].end_time}, PID: {os.getpid()}")
    # for segment in sorted_segments:
    #     print(
    #         f"Segment({segment.start_time}, {segment.end_time}) | PID: {os.getpid()}")

    chunk_points_in_time = find_minimum_points_in_time_sorted(sorted_segments)

    with lock:
        points_in_time[index] = chunk_points_in_time


def __split_list_in_chunks(
        sorted_list: list,
        max_num_chunks: int,
        min_chunk_size: int = MIN_CHUNK_SIZE):
    """
        Split a list into chunks.

        Args:
            sorted_list (list): A list of sorted elements
            max_num_chunks (int): The maximum number of chunks
            min_chunk_size (int): The minimum size of a chunk

        Returns:
            list: A list of chunks

        Raises:
            TypeError: If the sorted_list argument is not a list
            TypeError: If the max_num_chunks argument is not an integer
            TypeError: If the min_chunk_size argument is not an integer
            ValueError: If the max_num_chunks argument is less than 1
            ValueError: If the min_chunk_size argument is less than 1
    """
    chunk_size = len(sorted_list) // max_num_chunks

    while chunk_size < min_chunk_size and max_num_chunks > 1:
        max_num_chunks -= 1
        chunk_size = len(sorted_list) // max_num_chunks

    remaining_elements = len(sorted_list) % max_num_chunks
    chunks = []
    slicer_index = 0

    for i in range(max_num_chunks):
        iteration_chunk_size = chunk_size
        if remaining_elements > 0:
            iteration_chunk_size += 1
            remaining_elements -= 1

        chunks.append(list(itertools.islice(
            sorted_list,
            slicer_index,
            slicer_index + iteration_chunk_size)))
        
        slicer_index += iteration_chunk_size

    return chunks
