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

The house takes 25% of the gross on decided rounds. On a two-way void it takes
the full dropped pool instead — `2·stake(t)`, double the decided-round take at
the same tier. Four-way voids still take nothing (see below).

| Outcome | Frequency | House take at f/1 |
|---------|-----------|-------------------|
| Decided | 88.89% | $1.00 |
| Two-way void | 9.26% | $2.00 |
| Four-way void | 1.85% | $0.00 |

Expected take per f/1 contest is **$1.0741**, an effective rake of **26.85%**
against a 25% headline — the house nets *more* per contest than the 25%
headline suggests, entirely from the two-way-void premium below.

## House cut on a two-way void

The dropped pool (`2·stake(t)`) goes to the house in full; the two tied
entrants' own stakes are untouched by the void, so each still has exactly
`stake(t)` to replay or cash out with no top-up.

| Tier | Stake | Dropped pool → house | Each tied entrant keeps |
|------|-------|-----------------------|--------------------------|
| f/1 | $1 | $2 | $1 |
| f/1.4 | $3 | $6 | $3 |
| f/2 | $9 | $18 | $9 |
| f/2.8 | $27 | $54 | $27 |

This makes the house *more* profitable on a 2-way tie than on a decided round
at the same tier — double, always. An earlier design was rejected for landing
on this exact number (see history below), but on reconsideration the
alternative — a 25%-of-pool cut — leaves 1.5 stakes behind the dropped pool,
which can't cover a full re-entry without fractional credit tallying. Taking
the whole dropped pool keeps every settlement a whole stake, and at 9.26% of
rounds the doubled take is judged an acceptable price for that simplicity.

**History.** An earlier variant tested the mirror-image design — house keeps
the *tied* entrants' stakes while the dropped entrants fund the replay — and
was rejected at the time for this same 26.85% figure and the same
double-on-a-tie incentive. The two designs are revenue-identical (a two-way
split always divides the group's stakes 2-and-2, so either half is worth
`2·stake(t)`); what changed is the judgment that a doubled house take on an
infrequent, non-advancing round is an acceptable, simpler tradeoff, rather than
a trust problem worth $0 of rake to avoid. If this is revisited again, treat
the numbers above as settled and re-litigate the judgment call, not the math.

## Cashing out on a tie doesn't move the rake

A tied entrant can take the stake as a payout instead of replaying. That
amount is always exactly `stake(t)` (invariant 5) — on a two-way void it's the
entrant's own untouched stake, on a four-way void it's the stake returned
outright. Either way, replaying vs. cashing out only affects whether that
entrant's next round happens, not what the house collects: $2×stake(t) on a
two-way void and $0 on a four-way void regardless of the choice made
afterward. No figure in this document changes because of it.

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
