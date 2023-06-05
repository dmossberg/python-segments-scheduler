"""Profiler: find_minimum_points_in_time with large number of segments"""
import cProfile
import random
from segment_scheduler.segment import Segment
from segment_scheduler.scheduler import find_minimum_points_in_time

if __name__ == "__main__":
    segments = []
    for _ in range(1000000):
        r1 = random.randint(0, 100000)
        r2 = random.randint(0, 100000)

        # make sure r1 is less or equal than r2
        if r1 > r2:
            r1, r2 = r2, r1

        segments.append(Segment(r1, r2))

    pr = cProfile.Profile()
    pr.enable()

    points_in_time = find_minimum_points_in_time(segments)

    pr.disable()
    pr.print_stats(sort='cumtime')

    print(f"{points_in_time} (length of time points: {len(points_in_time)})")
