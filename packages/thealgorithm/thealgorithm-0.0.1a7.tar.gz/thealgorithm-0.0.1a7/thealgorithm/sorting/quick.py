from collections.abc import MutableSequence


def partition(seq: MutableSequence, left: int, right: int, reverse: bool) -> int:
    slow = pivot = left

    for fast in range(left + 1, right + 1):
        if (seq[fast] >= seq[pivot]) if reverse else (seq[fast] <= seq[pivot]):
            slow += 1
            seq[slow], seq[fast] = seq[fast], seq[slow]

    seq[pivot], seq[slow] = seq[slow], seq[pivot]
    return slow


def quick(seq: MutableSequence, left: int, right: int, reverse: bool = False) -> None:
    if left < right:
        pivot = partition(seq, left, right, reverse)
        quick(seq, left, pivot - 1, reverse)
        quick(seq, pivot + 1, right, reverse)
