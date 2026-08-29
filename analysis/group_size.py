#!/usr/bin/env python3
"""Tie rates for group sizes 3 through 8.

Sizes 3-5 are small enough to enumerate exactly: a group of n has ((n-1)!)^n
ballot profiles (8, 1,296, and 7,962,624 respectively). Sizes 6-8 blow past
that (120^6 and up), so those rows are Monte Carlo estimates instead —
labelled as such in the output, with a fixed seed so they're reproducible.

The scoring weights generalize the shipped 1, 1/3, 1/5 pattern to n-1 ranks
(1, 1/3, 1/5, 1/7, ...), scaled to integers via their LCM so equality
comparisons stay exact. At n=4 this reduces to the shipped 15/5/3 scheme.
"""

import itertools
import math
import random
from collections import Counter

EXACT_SIZES = (3, 4, 5)
SAMPLED_SIZES = (6, 7, 8)
SAMPLE_COUNT = 200_000
SEED = 42


def integer_points(n):
    denominators = [2 * i + 1 for i in range(n - 1)]  # 1, 3, 5, 7, ...
    lcm = math.lcm(*denominators)
    return tuple(lcm // d for d in denominators)


def exact_counts(n):
    points = integer_points(n)
    players = list(range(n))
    per_judge_perms = [list(itertools.permutations([p for p in players if p != j])) for j in players]
    counts = Counter()
    total = 0
    for profile in itertools.product(*per_judge_perms):
        scores = [0] * n
        for j, ranking in enumerate(profile):
            for pos, player in enumerate(ranking):
                scores[player] += points[pos]
        top = max(scores)
        counts[scores.count(top)] += 1
        total += 1
    return counts, total


def sampled_counts(n, samples, seed):
    points = integer_points(n)
    players = list(range(n))
    rng = random.Random(seed)
    counts = Counter()
    for _ in range(samples):
        scores = [0] * n
        for j in players:
            opponents = [p for p in players if p != j]
            rng.shuffle(opponents)
            for pos, player in enumerate(opponents):
                scores[player] += points[pos]
        top = max(scores)
        counts[scores.count(top)] += 1
    return counts, samples


def main():
    print(f"{'size':>4}  {'profiles':>12}  {'method':>8}  {'tie rate':>9}")
    for n in EXACT_SIZES:
        counts, total = exact_counts(n)
        clean = counts.get(1, 0)
        tie_rate = 1 - clean / total
        print(f"{n:>4}  {total:>12,}  {'exact':>8}  {tie_rate:>9.2%}")

    for n in SAMPLED_SIZES:
        counts, total = sampled_counts(n, SAMPLE_COUNT, SEED)
        clean = counts.get(1, 0)
        tie_rate = 1 - clean / total
        print(f"{n:>4}  {total:>12,}  {'sampled':>8}  {tie_rate:>9.2%}")

    print(
        "\nSampled rows use a fixed seed "
        f"({SEED}) and {SAMPLE_COUNT:,} draws each, so they're reproducible "
        "but carry sampling noise unlike the exact rows."
    )


if __name__ == "__main__":
    main()
