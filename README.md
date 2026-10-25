# py_disjoint_interval_set

A set of non-overlapping intervals that maintains sorted disjoint invariants automatically, supporting insertion, deletion, and overlap queries over half-open `[start, end)` ranges.

```python
from py_disjoint_interval_set import DisjointIntervalSet

ds = DisjointIntervalSet()
ds.insert(1, 5)
ds.insert(10, 20)
ds.insert(4, 12)   # bridges the gap, merging into [1, 20)
print(ds.intervals())  # [(1, 20)]
print(ds.overlaps(15, 25))  # True
ds.delete(8, 12)
print(ds.intervals())  # [(1, 8), (12, 20)]
```

## Why this exists

Managing a collection of intervals that must never overlap is a recurring need in scheduling, resource allocation, and range indexing. The hard part is not storing them; it is keeping them disjoint and sorted after every mutation. This library encapsulates that invariant so callers do not re-implement merge logic each time.

The trade-off is simplicity over performance: intervals are stored in a sorted list and operations are `O(n)` per call. For a few thousand intervals this is fine and the code stays auditable. For millions of intervals you want an augmented interval tree, which is out of scope here.

## Edge cases

- All ranges are half-open `[start, end)`. An insertion with `start == end` is a no-op (an empty interval contributes nothing). `start > end` raises `ValueError`.
- Adjacent intervals are always merged: inserting `[5, 10)` into a set containing `[1, 5)` yields `[1, 10)`. This is a deliberate decision — if you need to distinguish touching-but-separate intervals, this is not the right structure.
- `overlaps` returns `True` if any part of the query range intersects any stored interval, including single-point contact at the closed end (e.g. query `[5, 6)` overlaps stored `[1, 5)` is `False`; query `[4, 5)` against `[1, 5)` is `True`).

## Exported names

- `DisjointIntervalSet` — the main class.
- `DisjointIntervalSet.intervals()` — returns a list of `(start, end)` tuples, sorted by `start`.
- `DisjointIntervalSet.insert(start, end)` — insert a range, merging as needed.
- `DisjointIntervalSet.delete(start, end)` — remove the range from all stored intervals, splitting those it bisects.
- `DisjointIntervalSet.overlaps(start, end)` — `True` if the query range intersects any stored interval.
- `DisjointIntervalSet.__len__()` — number of disjoint intervals currently stored.
- `DisjointIntervalSet.__contains__(point)` — `True` if `point` lies inside any stored interval.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
