# Analysis

Everything here was established by computation, not intuition. Scripts are in
`analysis/` and use only the standard library. Every number below is reproducible.

## Summary of findings

1. Ties occur in **11.11%** of four-player rounds — 1 in 9, not an edge case.
2. **Three-way ties are structurally impossible.** Zero across all 1,296 profiles.
3. **Four-way ties cannot be eliminated by any scoring scheme.** 1.85% is a floor.
4. **The unit-fraction scheme does not reduce ties.** Every weighting gives 11.11%.
5. **Two thirds of ties are provably unbreakable** by any neutral rule.
6. Score-weighted voting resolves 100% of what is resolvable — and 0% of the rest.
7. Weighting strength must be **re-tuned per group size** or it corrupts results.

## The tie rate

Each of four judges ranks the other three, giving `(3!)^4 = 1296` ballot profiles.
Exhaustive enumeration:

| Outcome | Count | Share |
|---------|-------|-------|
| Clean winner | 1,152 | 88.89% |
| Two-way tie | 120 | 9.26% |
| **Three-way tie** | **0** | **0.00%** |
| Four-way tie | 24 | 1.85% |

The absence of three-way ties is what keeps the rules simple: every tie is either
a pair or the whole group, so two branches cover every case.

## Point values don't affect the tie rate

The unit fractions 1, ⅓, ⅕ were originally chosen on the theory that distinct
prime denominators would prevent sums from colliding. They do prevent collisions
between *different* placement multisets — but ties don't arise that way.

| Scheme | 2-way | 4-way | Total |
|--------|-------|-------|-------|
| 1, ⅓, ⅕ (shipped) | 120 | 24 | 11.11% |
| 1, ⅐, 1/13 | 120 | 24 | 11.11% |
| 1, 1/101, 1/10007 | 120 | 24 | 11.11% |
| 1, ½, 1/1000 | 120 | 24 | 11.11% |
| Irregular 97, 31, 7 | 120 | 24 | 11.11% |
| Borda 3, 2, 1 | 312 | 24 | 25.93% |

Identical, because ties happen when two entrants receive the *same multiset* of
placements. Same multiset means same sum under any function. The fractions are
worth keeping for interpretability, but they were never doing the job they were
picked for.

A corollary: **placement-count tiebreaks are useless.** Tied entrants always share
an identical count of 1sts, 2nds and 3rds, so "most first-place votes" can never
separate them.

## Why four-way ties are irreducible

In all 24 four-way profiles, every entrant collects exactly one 1st, one 2nd and
one 3rd. Each total is therefore:

```
f(1st) + f(2nd) + f(3rd)
```

The same sum for all four, for **any** function f. The tie is not produced by the
arithmetic, so no arithmetic can dissolve it. Such ballot patterns exist at every
group size, so this is a structural property of rank-based peer judging, not a
quirk of four players.

## Why most ties resist tiebreaking

The rigorous test: does a relabeling of players exist that permutes the tied
entrants among themselves and leaves the entire ballot profile unchanged? If so
the tied entrants are literally indistinguishable, and any rule that treats
players equally must return a tie.

| | Count | Share of ties |
|---|-------|---------------|
| Provably symmetric (unbreakable) | 96 | 66.7% |
| Asymmetric (in principle breakable) | 48 | 33.3% |

Two conventional tiebreaks were tested against all 144:

- **Head-to-head among tied entrants: resolves 0%.** In a two-way tie only two
  judges rank both tied players, so the comparison is always 1–1.
- **Consensus alignment** (which tied entrant's own ballot best matches the final
  order): **resolves 0%.**

This is what pushed the design away from tiebreaking and toward replay.

## Score-weighted voting

Weighting a judge's vote by their own score is circular — weight depends on score
depends on weight — making it a fixed-point problem, essentially PageRank applied
to a photo contest. It was explored seriously and then removed.

**It works, and hits the theoretical ceiling.** It resolved all 48 asymmetric ties
and none of the 96 symmetric ones. That 0 is not a defect; it is the maximum any
ballot-based rule can achieve.

**It is strategy-proof.** Across every ballot a judge could substitute, there were
zero cases where a judge's own ballot changed their own weight. Weight comes only
from other players' votes, so self-dealing is impossible by construction.

**But strength must be tuned per group size.** This is the trap:

| k | Tie rate | Decided rounds overturned |
|---|----------|---------------------------|
| 0 | 11.11% | 0.00% |
| 0.02 | 7.41% | 0.00% |
| 0.10 | 7.41% | 0.00% |
| 0.20 | 7.41% | 0.00% |
| 0.50 | 7.41% | 2.08% |
| 1.00 | 7.41% | 50.00% |

The tie benefit is all-or-nothing — any k above zero captures the full gain —
while distortion climbs continuously. At four players anything up to k=0.2 is
free. **At five players the safe ceiling collapses to about 0.02**, and the k=0.15
that was safe at four overturns roughly 3% of legitimate winners at five.

That near-miss is the reason `CLAUDE.md` insists on re-running the analysis after
any structural change. A constant validated under one configuration silently
became wrong under another.

## Group size

| Size | Profiles | Tie rate | Symmetric share |
|------|----------|----------|-----------------|
| 3 | 8 | 25.00% | — |
| **4** | **1,296** | **11.11%** | **66.7%** |
| 5 | 7,962,624 | 5.25% | ~0% |
| 6 | sampled | 2.27% | — |
| 7 | sampled | 0.83% | — |
| 8 | sampled | 0.28% | — |

Five players is interesting for more than the halved rate: sampling 400 tied
five-player rounds found **zero** symmetric ones. The pathological configurations
still exist — a perfect five-cycle gives all five entrants 176 points under the
scaled fractions — but they essentially never arise by chance. Combined with light
weighting, five-player groups reach a 0.02% tie rate.

The project reverted to four players anyway, once ties became desirable game
content rather than a defect to engineer away. Five-player groups also need 25%
more liquidity to fill.

## The floating-point near-miss

In the v3 prototype, a genuine two-way tie evaluated to:

```
2.3333333333333335
2.333333333333333
```

Mathematically equal. One ULP apart in binary floating point. An exact `===`
comparison would have declared a winner and skipped the void entirely — silently,
with no error, on roughly 9% of rounds.

The prototype used a `1e-9` tolerance and caught it. v3.1 removed the problem at
the root by scaling to integers, where `===` is exact and the settlement path has
no floats in it at all. Integer scoring reproduces the fractional distribution
exactly: 1,152 / 120 / 0 / 24, verified across all 1,296 profiles.

The general lesson: in a system that moves money on an equality comparison, exact
arithmetic is not a preference.
