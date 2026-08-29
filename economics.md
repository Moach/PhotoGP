# Economics

## The ladder

Four entrants each stake `3^(n-1)` at tier n. The house takes 25% of the gross,
and the winner's net is exactly `3^n` — so each stop triples the one below.

| Stop | Tier | Stake | Gross pot | House (25%) | Winner nets |
|------|------|-------|-----------|-------------|-------------|
| f/1 | 1 | $1 | $4 | $1 | $3 |
| f/1.4 | 2 | $3 | $12 | $3 | $9 |
| f/2 | 3 | $9 | $36 | $9 | $27 |
| f/2.8 | 4 | $27 | $108 | $27 | $81 |
| f/4 | 5 | $81 | $324 | $81 | $243 |
| f/5.6 | 6 | $243 | $972 | $243 | $729 |
| f/8 | 7 | $729 | $2,916 | $729 | $2,187 |

The identity `4·3^(n-1) − 3^(n-1) = 3·3^(n-1) = 3^n` holds at every tier, so the
numbers stay whole all the way up. No rounding anywhere in the payout path.

## House revenue

The house takes 25% of the gross on **decided rounds only**. Voids take nothing.

| Outcome | Frequency | House take at f/1 |
|---------|-----------|-------------------|
| Decided | 88.89% | $1.00 |
| Two-way void | 9.26% | $0.00 |
| Four-way void | 1.85% | $0.00 |

Expected take per f/1 contest is **$0.8889**, an effective rake of **22.2%**
against a 25% headline. The gap is the price of the tie mechanic, and it is
deliberate: the alternative designs all leaked trust instead of margin.

## Why voids take no rake

An earlier variant let the house keep the tied entrants' stakes while the dropped
entrants funded the replay. It was self-consistent, but it pushed the realized
rake to 26.85% against a 25% headline — and, worse, made the house *more*
profitable on tied rounds than decided ones.

That is an incentive the house should not have. A player who works out that ties
pay the operator double has a reason to distrust every close result. Taking zero
on voids costs about 2.8 percentage points of realized rake and removes the
suspicion entirely. Cheap at the price.

## Cost of the four-way carve-out

Four-way ties are 1.85% of rounds and the house absorbs all four stakes' worth of
forgone rake. At f/1 that is $0.0185 per contest — a 1.85% dent in revenue.

This is the price of a case that provably cannot be designed away (see
`docs/analysis.md`). It buys a clean promise: a tie never costs a player their
position, in any branch, with no exceptions to explain.

## Replay volume

A replay can itself tie, so contests occasionally run long:

| Consecutive ties | Probability | Roughly |
|------------------|-------------|---------|
| 1 | 11.11% | 1 in 9 |
| 2 | 1.23% | 1 in 81 |
| 3 | 0.14% | 1 in 729 |
| 4 | 0.015% | 1 in 6,561 |

Expected rounds per resolved contest: **1.125**. Plan for ~12.5% more round volume
than contest volume when sizing matchmaking and queue depth.

## Liquidity

Four-player groups fill faster than five-player ones, which was a live
consideration when group size was briefly raised to five. Above f/1 the pool is
constrained by how many winners exist at each tier, so the upper stops will fill
slowly at low traffic. Tier-1 volume divided by roughly 4 per tier gives a rough
sense of the ceiling on how many groups the top stops can form.

## Not modelled

Payment processing fees, chargebacks, photo storage and delivery, moderation cost,
fraud and collusion losses, customer support, and any regulatory or licensing
overhead. The rake figures above are gross of all of it.
