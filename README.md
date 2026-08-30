# Snapstakes

A peer-judged photography contest with escalating stakes.

Pay $1, enter one photograph, and join a group of four. Everyone ranks everyone
else's frame — you can't vote for your own. The highest score takes the pot minus
the house share, then chooses: cash out, or roll the winnings into a higher tier
against other winners. The pot triples at every stop.

There's a second draw beyond the money. A rolling Hall of Fame on the home page
displays high-tier winning photographs, which is its own reason to enter for
photographers who want the work seen.

> **Status: design and prototype.** No backend, no accounts, no real payments.
> `prototype/index.html` is a self-contained demo with simulated opponents and
> mocked money. Nothing here processes a real transaction.

## The ladder

| Stop | Stake | Gross pot | House (25%) | Winner nets |
|------|-------|-----------|-------------|-------------|
| f/1 | $1 | $4 | $1 | **$3** |
| f/1.4 | $3 | $12 | $3 | **$9** |
| f/2 | $9 | $36 | $9 | **$27** |
| f/2.8 | $27 | $108 | $27 | **$81** |
| f/4 | $81 | $324 | $81 | **$243** |
| f/5.6 | $243 | $972 | $243 | **$729** |
| f/8 | $729 | $2,916 | $729 | **$2,187** |

You can stop at any stop. Nothing forces you up the ladder.

## Scoring

A 1st is worth **15** points, a 2nd **5**, a 3rd **3** — the whole-number form of
1, ⅓ and ⅕ after multiplying by their LCM of 15.

Every ballot therefore spends exactly 23 points, and a four-entrant round always
distributes exactly 92. That number is printed on every results screen. Because
each ballot's spend is fixed, altering a single vote breaks the sum, so anyone can
verify a round by hand in a few seconds.

Integers are used end to end. In an earlier build the two arms of a real tie
evaluated to `2.3333333333333335` and `2.333333333333333` — equal in mathematics,
one bit apart in binary floating point. An exact comparison would have silently
declared a winner and skipped the tie entirely. There are no floats in the
settlement path now.

## Ties are part of the game

Two photographs can finish level. When they do the round is void and each tied
entrant chooses: **replay the same stop** — same stakes, fresh opponents, never
rematched against each other — or **cash out on the spot** instead. A tie never
costs you your position on the ladder either way.

- **Two-way tie (9.26% of rounds).** The house takes both dropped entrants'
  stakes in full. Each tied entrant's own stake is untouched by the void, so it
  covers a re-entry precisely — or, if a tied entrant cashes out instead, pays
  that same amount out as their prize. This makes the house take double what it
  takes on a decided round at the same tier — a deliberate tradeoff so every
  settlement stays a whole stake (see `docs/economics.md`).
- **Four-way tie (1.85%).** There are no dropped entrants to fund anything, so the
  house returns all four stakes and takes nothing. It absorbs the cost. A tied
  entrant can bank that returned stake instead of playing again.
- **Three-way ties cannot happen.** Not a rule — an arithmetic fact of ranking
  three photographs. Verified across all 1,296 possible ballot profiles.

Ties are never resolved by a coin flip.

## Why four-way ties can't be designed away

In all 24 four-way profiles, every entrant collects exactly one 1st, one 2nd and
one 3rd. Each total is therefore `f(1st) + f(2nd) + f(3rd)` — the same sum for
*any* choice of point values. Tested against 1/⅐/1/13, 1/(1/101)/(1/10007),
1/½/(1/1000) and deliberately irregular sets: every one produced exactly 24.

1.85% is a floor, not a tuning problem. The design accepts it and prices it in.

## Running things

```bash
open prototype/index.html          # no build step, no dependencies

python3 analysis/tie_rates.py      # all 1,296 profiles, exhaustively
python3 analysis/group_size.py     # tie rates for group sizes 3-8
python3 analysis/weighting.py      # score-weighted voting sweep
```

Analysis scripts are standard library only. No installs.

The prototype fetches placeholder imagery from `picsum.photos`, so photos need
network access to render; everything else works offline. Demo controls on the
entry page force either kind of tie, since ties are only 11% of rounds and are
otherwise tedious to observe.

## Documentation

- [`CLAUDE.md`](CLAUDE.md) — project context, invariants, settled decisions
- [`docs/mechanics.md`](docs/mechanics.md) — rules and scoring spec
- [`docs/economics.md`](docs/economics.md) — ladder, rake, tie funding
- [`docs/analysis.md`](docs/analysis.md) — the tie research, with numbers

## Not built yet

Backend, accounts, real payments, photo moderation, anti-collusion, matchmaking,
persistent Hall of Fame. Real-money operation would require licensed payment
processing and jurisdiction-specific legal review — a contest where entrants pay
to compete for a pooled prize is regulated very differently depending on where the
players are, and none of that is addressed here.
