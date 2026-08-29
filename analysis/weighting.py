#!/usr/bin/env python3
"""Score-weighted voting sweep — the rejected approach described in
CLAUDE.md's "Rejected approaches" section.

A judge's vote is weighted by their own score, which is itself a function of
other judges' (weighted) votes. That circularity makes it a fixed-point
problem: this script resolves it by iterating "recompute scores from current
weights, then recompute weights from those scores" to convergence, for every
k in the sweep, over all 1,296 profiles at group size 4.

For each k it reports:
  - the resulting tie rate
  - what share of otherwise-clean (single-winner) rounds change winner
    under weighting — the "decided rounds overturned" column

This is a fresh implementation, not a recovered original: the exact
fixed-point formula behind the historical 7.41% / 2.08% / 50.00% figures in
docs/analysis.md wasn't preserved in this repo. The qualitative story it
reproduces — small k is free, large k is destructive — is what matters here;
treat exact percentages as this script's own, not a verification of those
numbers.
"""

import itertools
from fractions import Fraction

N = 4
POINTS = (Fraction(15), Fraction(5), Fraction(3))
K_VALUES = (Fraction(0), Fraction(2, 100), Fraction(10, 100), Fraction(20, 100), Fraction(50, 100), Fraction(1))
ITERATIONS = 80


def all_profiles():
    players = list(range(N))
    per_judge_perms = [list(itertools.permutations([p for p in players if p != j])) for j in players]
    yield from itertools.product(*per_judge_perms)


def baseline_scores(profile):
    scores = [Fraction(0)] * N
    for j, ranking in enumerate(profile):
        for pos, player in enumerate(ranking):
            scores[player] += POINTS[pos]
    return scores


def weighted_scores(profile, k):
    """Iterate the weight/score fixed point to (approximate) convergence."""
    weight = [Fraction(1)] * N
    scores = baseline_scores(profile)
    for _ in range(ITERATIONS):
        scores = [Fraction(0)] * N
        for j, ranking in enumerate(profile):
            for pos, player in enumerate(ranking):
                scores[player] += weight[j] * POINTS[pos]
        mean_score = sum(scores) / N
        if mean_score == 0:
            break
        weight = [max(Fraction(0), 1 + k * (scores[j] - mean_score) / mean_score) for j in range(N)]
    return scores


def classify(scores):
    top = max(scores)
    return sum(1 for s in scores if s == top)


def main():
    profiles = list(all_profiles())
    baselines = {p: baseline_scores(p) for p in profiles}
    clean_profiles = [p for p in profiles if classify(baselines[p]) == 1]

    print(f"{'k':>6}  {'tie rate':>9}  {'decided rounds overturned':>26}")
    for k in K_VALUES:
        ties = 0
        overturned = 0
        for profile in profiles:
            wscores = weighted_scores(profile, k)
            if classify(wscores) > 1:
                ties += 1
        for profile in clean_profiles:
            wscores = weighted_scores(profile, k)
            if classify(wscores) == 1:
                base_winner = baselines[profile].index(max(baselines[profile]))
                new_winner = wscores.index(max(wscores))
                if new_winner != base_winner:
                    overturned += 1
            else:
                overturned += 1  # a clean round that became a tie is also a changed outcome

        tie_rate = ties / len(profiles)
        overturn_rate = overturned / len(clean_profiles)
        print(f"{float(k):>6.2f}  {tie_rate:>9.2%}  {overturn_rate:>26.2%}")


if __name__ == "__main__":
    main()
