# Mechanics

## Round structure

A round is four entrants, one photograph each, at a single tier.

1. **Entry.** A player stakes the tier amount and submits one photograph. At f/1
   the stake is $1; at higher stops it is the winnings carried up from below.
2. **Grouping.** Four entrants at the same tier form a group. At f/1 they come
   from the open queue; above f/1 every member is a winner from the tier below.
3. **Judging.** Each entrant ranks the other three: 1st, 2nd, 3rd. Nobody sees or
   ranks their own frame. Rankings are locked once submitted.
4. **Settlement.** Points are totalled. Highest total wins.
5. **Decision.** The winner cashes out or advances one stop, carrying the winnings
   as the stake for the next tier.

## Scoring

| Placement | Points | Fraction |
|-----------|--------|----------|
| 1st | 15 | 1 |
| 2nd | 5 | ⅓ |
| 3rd | 3 | ⅕ |

The integers are the unit fractions scaled by their LCM of 15. Ordering and
ratios are identical; the arithmetic is exact.

Derived constants:

| Quantity | Value | Why |
|----------|-------|-----|
| Ballot spend | 23 | 15 + 5 + 3, identical on every ballot |
| Round total | 92 | 23 × 4 judges |
| Maximum score | 45 | 15 × 3 judges — ranked 1st by everyone |
| Minimum score | 9 | 3 × 3 judges — ranked last by everyone |

**The 92 checksum.** Because every ballot spends exactly 23, a valid round always
totals 92. The results screen prints the sum. Any tampering with an individual
vote breaks it, which makes each round hand-verifiable without trusting the
operator. This falls out of the fixed-budget structure for free.

**Integers only.** No floating point touches a score, a tie comparison, or a
payout. Tie detection is exact equality, never an epsilon. This is not stylistic —
see `docs/analysis.md` for the near-miss that motivated it.

## Ties

Ties are a designed outcome. In every branch a tied entrant chooses: replay the
same tier — ladder position preserved, never dropping a stop — or cash out on
the spot instead, taking the funded or returned amount as a final payout. See
"Cashing out on a tie" below.

### Two-way tie — 9.26% of rounds

Round is void. The two dropped entrants' stakes are split between the two who
tied, which funds each re-entry exactly:

| Tier | Stake | Dropped pool | Each tied player receives | Re-entry costs |
|------|-------|--------------|---------------------------|----------------|
| f/1 | $1 | $2 | $1 | $1 |
| f/1.4 | $3 | $6 | $3 | $3 |
| f/2 | $9 | $18 | $9 | $9 |
| f/2.8 | $27 | $54 | $27 | $27 |

Half the dropped pool equals one stake at every tier, so the mechanism is
self-funding with no top-up and no shortfall. The house takes no share of a void.
The two tied entrants are barred from being rematched against each other.

### Four-way tie — 1.85% of rounds

Round is void. No dropped entrants exist to fund a replay, so the house returns
all four stakes and takes no rake. All four replay the stop.

Every entrant in such a round received one 1st, one 2nd and one 3rd, so all four
totals are 15 + 5 + 3 = 23. This is why no scoring scheme can separate them.

### Three-way ties

Impossible. Zero occurrences across all 1,296 ballot profiles. The tie rules need
only two branches.

### Cashing out on a tie

A void gives each tied entrant two options, not one:

- **Replay** — same stake, same photograph, fresh opponents, tier held.
- **Cash out** — take the money as a payout and end the run there.

The cash-out amount is exactly one stake at the tied tier in both branches: the
two-way split and the four-way refund both resolve to `stake(t)` (invariant 5),
which is precisely what a re-entry would have cost. Cashing out simply pays that
same amount out instead of re-staking it — no top-up, no shortfall, no change to
house revenue on the void (still $0 either way).

Framing: `stake(t) == netAmount(t-1)` for every tier above f/1, so the payout is
presented as the entrant's win from the tier they last actually decided. At f/1
there is no prior tier, so cashing out just returns the $1 entry fee rather than
banking a win.

### Repeated voids

No cap. A replay can itself tie, but expected volume is 1.125 rounds per resolved
contest and three consecutive ties is 1 in 729. A cap would fire almost never and
add a rule most players would never encounter but would still have to read.

Ties are never resolved randomly.

## Judging constraints

- A player cannot rank their own photograph.
- Rankings are locked on submission.
- A ranking must be complete — all three placed — before it can be submitted.
- Previous tie contenders are excluded from a player's next group.

## Advancement

A winner may cash out or advance. Advancing carries the full winnings as the next
tier's stake, against three other winners from that tier. The photograph stays the
same for the whole run. There are seven stops, f/1 through f/8; f/8 is terminal
and its winner must cash out.
