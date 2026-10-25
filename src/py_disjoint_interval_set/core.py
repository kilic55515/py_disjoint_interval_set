"""Core implementation of a disjoint interval set over half-open ranges."""

from typing import List, Tuple


class DisjointIntervalSet:
    """A set of non-overlapping, sorted half-open intervals [start, end).

    Invariants maintained after every public mutation:
      1. No two stored intervals overlap or touch (adjacent intervals are merged).
      2. Intervals are sorted by start ascending.
      3. Every stored interval satisfies start < end.

    Representing intervals as half-open is the key choice: it makes "touches but
    does not overlap" equivalent to "adjacent and should be merged", which removes
    a whole class of off-by-one ambiguity that plagues closed-interval sets.
    """

    def __init__(self) -> None:
        self._intervals: List[Tuple[int, int]] = []

    def __len__(self) -> int:
        return len(self._intervals)

    def __contains__(self, point: int) -> bool:
        # Linear scan is acceptable given the stated scope. A bisect-based check
        # would be faster but adds index arithmetic that obscures the logic.
        for start, end in self._intervals:
            if start <= point < end:
                return True
        return False

    def intervals(self) -> List[Tuple[int, int]]:
        """Return a shallow copy of the stored intervals as a list of tuples."""
        return list(self._intervals)

    def insert(self, start: int, end: int) -> None:
        """Insert [start, end), merging overlapping and adjacent intervals."""
        if start > end:
            raise ValueError("start must be <= end")
        if start == end:
            return

        # Find all intervals that overlap or touch [start, end). Because the
        # stored list is sorted and disjoint, the affected range is contiguous.
        # We compute the new merged span and the slice of old intervals to
        # replace, then splice in a single replacement.
        new_start = start
        new_end = end

        # Leftmost index whose interval overlaps or touches [start, end).
        left = 0
        while left < len(self._intervals) and self._intervals[left][1] < start:
            left += 1

        # Rightmost+1 index whose interval overlaps or touches [start, end).
        right = left
        while right < len(self._intervals) and self._intervals[right][0] <= end:
            right += 1

        if left < right:
            # Merge the span with all affected existing intervals.
            new_start = min(new_start, self._intervals[left][0])
            new_end = max(new_end, self._intervals[right - 1][1])

        self._intervals[left:right] = [(new_start, new_end)]

    def delete(self, start: int, end: int) -> None:
        """Remove [start, end) from all stored intervals, splitting as needed."""
        if start > end:
            raise ValueError("start must be <= end")
        if start == end:
            return

        new_intervals: List[Tuple[int, int]] = []
        for iv_start, iv_end in self._intervals:
            if iv_end <= start or iv_start >= end:
                # No overlap with the deletion range; keep as-is.
                new_intervals.append((iv_start, iv_end))
                continue
            # There is some overlap. Preserve the non-overlapping left part...
            if iv_start < start:
                new_intervals.append((iv_start, start))
            # ...and the non-overlapping right part.
            if iv_end > end:
                new_intervals.append((end, iv_end))

        self._intervals = new_intervals

    def overlaps(self, start: int, end: int) -> bool:
        """Return True if [start, end) intersects any stored interval."""
        if start > end:
            raise ValueError("start must be <= end")
        if start == end:
            return False
        for iv_start, iv_end in self._intervals:
            # Half-open overlap test: two ranges [a, b) and [c, d) overlap iff
            # a < d and c < b.
            if iv_start < end and start < iv_end:
                return True
        return False
