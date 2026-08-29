#!/usr/bin/env python3
"""Exhaustive enumeration over all 1,296 ballot profiles for a 4-player round.

Each of the 4 judges ranks the other 3 entrants 1st/2nd/3rd, so there are
(3!)^4 = 1,296 possible ballot profiles. This script enumerates every one of
them (no sampling) and reproduces the headline numbers in docs/analysis.md:

  - the clean / two-way / three-way / four-way winner distribution
  - that the tie rate is invariant to the choice of scoring weights (except
    Borda, which is worse)
  - the share of ties that are *provably* symmetric (unbreakable by any
    neutral rule)
  - that a two-way tie's only head-to-head judges always split 1-1
  - that a simple "consensus alignment" tiebreak resolves 0% of ties

Standard library only, exact arithmetic via fractions.Fraction — no floats,
matching CLAUDE.md invariant 3.
"""

import itertools
from collections import Counter
from fractions import Fraction

N = 4  # group size this script is about; see group_size.py for other sizes

SHIPPED_POINTS = (Fraction(15), Fraction(5), Fraction(3))  # 1, 1/3, 1/5 scaled


def all_profiles():
    """Yield every ballot profile as a tuple indexed by judge.

    profile[j] is a 3-tuple of the other three players in the order judge j
    ranked them (1st, 2nd, 3rd).
    """
    players = list(range(N))
    per_judge_perms = []
    for j in players:
        opponents = [p for p in players if p != j]
        per_judge_perms.append(list(itertools.permutations(opponents)))
    yield from itertools.product(*per_judge_perms)


def scores_for(profile, points):
    scores = [Fraction(0)] * N
    for j, ranking in enumerate(profile):
        for pos, player in enumerate(ranking):
            scores[player] += points[pos]
    return scores


def classify(scores):
    """Return how many players share the top score (1 = clean winner)."""
    top = max(scores)
    return sum(1 for s in scores if s == top)


def tie_distribution(points):
    counts = Counter()
    for profile in all_profiles():
        counts[classify(scores_for(profile, points))] += 1
    return counts


def apply_perm(profile, perm):
    """Relabel every player in `profile` according to `perm` (a tuple where
    perm[i] is the new label for player i)."""
    new_profile = [None] * N
    for j, ranking in enumerate(profile):
        new_profile[perm[j]] = tuple(perm[x] for x in ranking)
    return tuple(new_profile)


def automorphisms(profile):
    """All player relabelings that leave the profile exactly unchanged."""
    return [perm for perm in itertools.permutations(range(N)) if apply_perm(profile, perm) == profile]


def is_symmetric_tie(profile, tied):
    """True if some automorphism of the profile nontrivially permutes the
    tied players among themselves — i.e. the tie is unbreakable by any rule
    that treats players equally."""
    for perm in automorphisms(profile):
        if any(perm[t] != t for t in tied):
            return True
    return False


def head_to_head_split(profile, a, b):
    """For the two judges who are neither a nor b, which do they rank
    higher? Returns (votes_for_a, votes_for_b)."""
    votes_a = votes_b = 0
    for j, ranking in enumerate(profile):
        if j in (a, b):
            continue
        votes_a += ranking.index(a) < ranking.index(b)
        votes_b += ranking.index(b) < ranking.index(a)
    return votes_a, votes_b


def consensus_alignment(profile, scores, candidate):
    """How well `candidate`'s own ballot agrees with the final pairwise
    order, restricted to pairs not involving `candidate` (since nobody
    ranks themselves). Higher = candidate's taste matched the room."""
    own_ranking = profile[candidate]
    agreements = 0
    others = [p for p in range(N) if p != candidate]
    for a, b in itertools.combinations(others, 2):
        ballot_prefers_a = own_ranking.index(a) < own_ranking.index(b)
        final_prefers_a = scores[a] > scores[b]
        if scores[a] == scores[b]:
            continue  # no signal from a pair the final order can't separate
        agreements += ballot_prefers_a == final_prefers_a
    return agreements


def main():
    # --- 1. Headline distribution, shipped scoring (15/5/3) -------------
    dist = tie_distribution(SHIPPED_POINTS)
    total = sum(dist.values())
    print(f"Shipped scoring (15/5/3) over {total} profiles:")
    for winners, label in ((1, "Clean winner"), (2, "Two-way tie"), (3, "Three-way tie"), (4, "Four-way tie")):
        count = dist.get(winners, 0)
        print(f"  {label:<15} {count:>5}  ({count / total:.2%})")

    assert dist[1] == 1152, dist[1]
    assert dist[2] == 120, dist[2]
    assert dist.get(3, 0) == 0
    assert dist[4] == 24, dist[4]
    print("  Matches CLAUDE.md's proven facts: 1152 / 120 / 0 / 24.\n")

    # --- 2. Does the scoring scheme change the tie rate? ----------------
    schemes = {
        "shipped 15/5/3 (1, 1/3, 1/5)": SHIPPED_POINTS,
        "1, 1/7, 1/13": (Fraction(1), Fraction(1, 7), Fraction(1, 13)),
        "1, 1/101, 1/10007": (Fraction(1), Fraction(1, 101), Fraction(1, 10007)),
        "1, 1/2, 1/1000": (Fraction(1), Fraction(1, 2), Fraction(1, 1000)),
        "irregular 97/31/7": (Fraction(97), Fraction(31), Fraction(7)),
        "Borda 3/2/1": (Fraction(3), Fraction(2), Fraction(1)),
    }
    print("Scoring scheme comparison:")
    print(f"  {'scheme':<32}{'2-way':>7}{'4-way':>7}{'total tie %':>13}")
    for name, points in schemes.items():
        d = tie_distribution(points)
        two = d.get(2, 0)
        four = d.get(4, 0)
        pct = (two + four) / total
        print(f"  {name:<32}{two:>7}{four:>7}{pct:>12.2%}")
    print()

    # --- 3. Symmetric (unbreakable) share of ties, shipped scheme -------
    symmetric = 0
    tied_profiles = 0
    two_way_profiles = []
    for profile in all_profiles():
        scores = scores_for(profile, SHIPPED_POINTS)
        top = max(scores)
        tied = [p for p in range(N) if scores[p] == top]
        if len(tied) < 2:
            continue
        tied_profiles += 1
        if len(tied) == 2:
            two_way_profiles.append((profile, tied, scores))
        if is_symmetric_tie(profile, tied):
            symmetric += 1
    print(f"Symmetric ties: {symmetric} / {tied_profiles} ({symmetric / tied_profiles:.1%})\n")

    # --- 4. Head-to-head tiebreak on two-way ties ------------------------
    splits = Counter()
    for profile, tied, _scores in two_way_profiles:
        a, b = tied
        va, vb = head_to_head_split(profile, a, b)
        splits[(va, vb)] += 1
    resolved = sum(c for (va, vb), c in splits.items() if va != vb)
    print("Head-to-head tiebreak on two-way ties (votes among the two non-tied judges):")
    for (va, vb), c in sorted(splits.items()):
        print(f"  {va}-{vb} split: {c} profiles")
    print(f"  Resolves {resolved} / {len(two_way_profiles)} ({resolved / len(two_way_profiles):.0%})\n")

    # --- 5. Consensus-alignment tiebreak on all ties ---------------------
    resolved = 0
    for profile in all_profiles():
        scores = scores_for(profile, SHIPPED_POINTS)
        top = max(scores)
        tied = [p for p in range(N) if scores[p] == top]
        if len(tied) < 2:
            continue
        alignments = {t: consensus_alignment(profile, scores, t) for t in tied}
        if len(set(alignments.values())) > 1:
            resolved += 1
    print(f"Consensus-alignment tiebreak resolves {resolved} / {tied_profiles} ({resolved / tied_profiles:.0%})")


if __name__ == "__main__":
    main()
