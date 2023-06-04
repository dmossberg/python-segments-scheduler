class Segment:
  def __init__(self, start_time: int, end_time: int):
    """
    A Segment object represents a segment of time with a start and end time.

    Args:
        start_time (int): The start time of the segment
        end_time (int): The end time of the segment

    Raises:
        TypeError: If the start_time argument is not an integer
        TypeError: If the end_time argument is not an integer
        ValueError: If the start_time argument is greater than the end_time argument
    """
    if not isinstance(start_time, int):
      raise TypeError("Argument 'start_time' must be an integer")
    if not isinstance(end_time, int):
      raise TypeError("Argument 'end_time' must be an integer")
    if start_time > end_time:
      raise ValueError("Argument 'start_time' must be less than or equal to 'end_time'")

    self.start_time = start_time
    self.end_time = end_time