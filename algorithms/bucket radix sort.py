import math
from typing import Callable, Iterable, List, Sequence, TypeVar

T = TypeVar("T")


def get_num_buckets(n: int, strategy: str = "sqrt", base: int = 10) -> int:
    """
    Decide the number of buckets based on common heuristics.

    Parameters
    ----------
    n : int
        Number of items to be bucketed.
    strategy : str, optional
        Heuristic to use. Common options:
        - "sqrt"  : ⌊sqrt(n)⌋ buckets (very common for generic bucket sort).
        - "n"     : n buckets (degenerates to something like counting sort).
        - "logn"  : ⌊log2(n)⌋ buckets.
        - "radix" : use `base` buckets, suitable for radix sort per-digit.
    base : int, optional
        Base for the "radix" strategy (normally 10).

    Returns
    -------
    int
        Number of buckets to use (≥ 0).
    """
    if n <= 0:
        return 0

    strategy = strategy.lower()

    if strategy == "sqrt":
        return max(1, int(math.sqrt(n)))
    if strategy in ("n", "linear"):
        return n
    if strategy in ("logn", "log", "log2"):
        return max(1, int(math.log2(n)))
    if strategy == "radix":
        return max(1, base)

    raise ValueError(f"Unknown bucket strategy: {strategy!r}")


def bucket_sort(
    items: Sequence[T],
    key: Callable[[T], int],
    num_buckets: int,
    *,
    in_bucket_sort: Callable[[List[T]], List[T]] | None = None,
) -> List[T]:
    """
    Stable bucket-based (counting-style) sort.

    This function cares about the *bucket index* given by `key(item)`.
    By default it does not sort within each bucket (pure counting-style
    behavior), which is ideal for radix-sort passes.

    If you want to sort inside each bucket (classic bucket sort for,
    say, floats in [0, 1)), pass an `in_bucket_sort` function, e.g.:

        bucket_sort(data, key=bucket_index, num_buckets=k,
                    in_bucket_sort=sorted)

    Parameters
    ----------
    items : Sequence[T]
        Iterable of items to sort.
    key : Callable[[T], int]
        Function mapping each item to an integer bucket index in
        [0, num_buckets - 1].
    num_buckets : int
        Number of buckets.
    in_bucket_sort : Callable[[List[T]], List[T]] | None, optional
        If provided, this function is applied to each bucket list
        *individually* before concatenation. Common choices are
        `sorted` or a custom in-bucket sorting algorithm.

    Returns
    -------
    List[T]
        New list containing the items in bucketed order.
    """
    if num_buckets <= 0:
        return list(items)

    buckets: List[List[T]] = [[] for _ in range(num_buckets)]

    for item in items:
        idx = key(item)
        if not 0 <= idx < num_buckets:
            raise ValueError(
                f"Bucket index {idx} out of range for num_buckets={num_buckets}"
            )
        buckets[idx].append(item)

    result: List[T] = []
    for bucket in buckets:
        if in_bucket_sort is not None:
            bucket = in_bucket_sort(bucket)
        result.extend(bucket)

    return result


def radix_sort(
    items: Iterable[int],
    base: int = 10,
) -> List[int]:
    """
    LSD radix sort for non-negative integers, implemented via bucket_sort.

    Parameters
    ----------
    items : Iterable[int]
        Non-negative integers to sort.
    base : int, optional
        Numeric base (radix). Default is 10 (decimal).

    Returns
    -------
    List[int]
        The sorted list of integers.

    Notes
    -----
    - This implementation is stable.
    - It assumes all numbers are >= 0. You can adapt it by separating
      negatives and positives if needed.
    """
    arr = list(items)
    if not arr:
        return arr
    if base <= 1:
        raise ValueError("base must be >= 2")

    max_val = max(arr)
    if max_val < 0:
        raise ValueError("radix_sort only supports non-negative integers")

    # Number of buckets per digit (0..base-1). This is exactly the
    # "radix" strategy for get_num_buckets.
    num_buckets = get_num_buckets(base, strategy="radix", base=base)

    exp = 1  # base^0, then base^1, base^2, ...
    while max_val // exp > 0:
        # For each digit position, perform a stable bucket_sort by that digit.
        def digit_key(x: int, exp: int = exp, base: int = base) -> int:
            return (x // exp) % base

        arr = bucket_sort(arr, key=digit_key, num_buckets=num_buckets)
        exp *= base

    return arr


__all__ = ["get_num_buckets", "bucket_sort", "radix_sort"]

