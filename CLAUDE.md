# CLAUDE.md

Context for Claude Code working in this repository.

## What this is

**Snapstakes** is a peer-judged photography contest with escalating stakes. A player pays $1,
submits one photograph, and is grouped with three other entrants. Each judges the other three;
nobody can vote for their own frame. The winner takes the pot minus a house share, then chooses
to cash out or roll the winnings into a higher tier against other winners.

A secondary draw is prestige: a rolling Hall of Fame on the home page displays high-tier winning
photographs, which matters to photographers who want their work seen.

Status: **design + single-file prototype.** No backend, no real payments, no auth. The prototype
in `prototype/index.html` is vanilla HTML/CSS/JS with no build step. Open it in a browser.

## Settled parameters — do not change without re-running the analysis

| Parameter | Value | Notes |
|---|---|---|
| Group size | 4 | Was briefly 5; reverted deliberately (see below) |
| House rake | 25% | On decided rounds only; voids take nothing |
| Scoring | 15 / 5 / 3 | Integer form of 1, ⅓, ⅕ (LCM 15) |
| Tier ladder | 7 stops, f/1 → f/8 | Winner nets 3ⁿ: $3, $9, $27, $81, $243, $729, $2,187 |
| Vote weighting | **off** | Explored and removed; see "Rejected approaches" |
| Tie resolution | replay, never random | See "Tie handling" |

## Invariants

These must hold. If a change breaks one, the change is wrong.

1. **Round total is always 92.** Every ballot spends 15 + 5 + 3 = 23; four ballots distribute
   23 × 4 = 92. The results screen prints this checksum. It is also a tamper-evidence property:
   altering a single vote breaks the sum, so a player can verify a round by hand.
2. **Score range is 9 to 45.** A clean sweep is 15 × 3 judges = 45. Last on every card is 3 × 3 = 9.
3. **Settlement uses integers only.** No floating point anywhere in scoring, tie detection, or
   payout. Tie comparison is exact `===`, never an epsilon.
4. **gross − house = net** at every tier. `4·3ⁿ⁻¹ − 3ⁿ⁻¹ = 3ⁿ`.
5. **Half the dropped pool equals exactly one stake**, at every tier. Two dropped entrants
   contribute 2·3ⁿ⁻¹; split two ways gives 3ⁿ⁻¹, which is precisely the re-entry stake. This is
   what makes two-way tie replays self-funding with no top-up and no shortfall.
6. **Ties are never resolved randomly.** No coin flips, ever.

## Proven facts — settled, do not re-litigate

These were established by exhaustive enumeration over all 1,296 ballot profiles (`analysis/`).
Re-deriving them is wasted work; the scripts are committed so results can be reproduced.

- **Tie distribution at 4 players:** 88.89% clean winner, 9.26% two-way tie, 1.85% four-way tie.
- **Three-way ties are structurally impossible.** Zero occurrences across all 1,296 profiles.
  Every tie is a pair or the whole group. This is why the tie rules need only two branches.
- **Four-way ties cannot be eliminated by any scoring scheme.** In all 24 four-way profiles every
  entrant receives exactly one 1st, one 2nd and one 3rd, so each total is f(1st)+f(2nd)+f(3rd) —
  the same sum for any choice of f. Tested against 1/⅐/1/13, 1/(1/101)/(1/10007), 1/½/(1/1000)
  and irregular sets: all produced exactly 24. **1.85% is a hard floor.**
- **The unit-fraction scheme does not reduce ties.** Every weighting tested gives exactly 11.11%
  total ties. Borda (3/2/1) is worse at 27.78%. The fractions are chosen for interpretability,
  not tie avoidance.
- **Placement-count tiebreaks are useless.** Tied entrants always share an identical multiset of
  placements, so "most first-place votes" can never separate them.
- **Head-to-head and consensus-alignment tiebreaks resolve 0%.** In a two-way tie only two judges
  rank both tied entrants, and that comparison is always 1–1.
- **66.7% of four-player ties are provably symmetric** — a relabeling of players maps the ballot
  profile to itself, so no neutral rule can prefer one entrant over the other.

## Rejected approaches and why

Do not reintroduce these without new evidence.

- **Score-weighted vote power** (a judge's weight scales with their own score). Works, and is
  strategy-proof — weight comes only from others' votes, so it cannot be self-dealt. But the
  strength constant must be tuned per group size: k=0.15 is safe at 4 players and overturns 2.8%
  of legitimate winners at 5. Removed when ties became a designed feature rather than a defect.
- **Five-player groups.** Drop ties to 5.29%, and crucially none are symmetric, so weighting then
  reaches 0.02%. Reverted because ties are now desirable game content, and 5-player groups need
  25% more liquidity to fill.
- **Cardinal 0–100 ratings** instead of ranking. Reaches 0.96% ties alone. Rejected as slower and
  more deliberate than tap-to-rank, and unnecessary once ties became a feature.
- **Random tiebreak.** The original prototype did this. It is the thing the whole design exists to
  eliminate.

## Tie handling

A tie is a designed outcome, not a failure. In both branches a tied entrant chooses: replay the
same tier (never dropping a stop), or cash out on the spot instead.

- **Two-way (9.26%)** — round void. The two dropped entrants' stakes are split between the two who
  tied, funding each re-entry exactly (invariant 5). House takes no share. The tied entrants are
  barred from being matched against each other again.
- **Four-way (1.85%)** — round void. No dropped entrants exist to fund anything, so the house
  returns all four stakes and takes no rake. Costs ~$0.0185 per contest, a 1.85% revenue dent.
- **No cap on consecutive voids.** Expected volume is 1.125 rounds per contest; three consecutive
  ties is 1 in 729. A cap would fire almost never and confuse more people than it helps.
- **Cash out instead of replaying.** Either tied entrant may take the funded/returned amount as a
  final payout rather than re-entering. That amount is always exactly one stake at the tied tier —
  the same money invariant 5 already earmarks for a re-entry, paid out instead of staked. This
  changes no invariant and no rake figure: replaying and cashing out draw on the identical pool,
  so house revenue on a void is $0 either way. The payout is framed as the entrant's prior-tier
  win (`netAmount(t-1)`), since the tied round itself never decided a winner; at f/1 there is no
  prior win, so cashing out just returns the entry fee.

## Layout

```
CLAUDE.md            this file
README.md            human-facing overview
docs/mechanics.md    game rules and scoring spec
docs/economics.md    ladder, rake, tie funding
docs/analysis.md     tie research findings, with numbers
analysis/*.py        exhaustive enumeration scripts (stdlib only)
prototype/index.html v3.1 single-file prototype
```

## Commands

```bash
python3 analysis/tie_rates.py     # exhaustive enumeration over all 1,296 profiles
python3 analysis/group_size.py    # tie rates for group sizes 3-8
python3 analysis/weighting.py     # score-weighted voting sweep
open prototype/index.html         # no build step, no dependencies
```

Analysis scripts use only the standard library and `fractions.Fraction` for exact arithmetic.
No pip installs needed.

## Prototype notes

- Mocked throughout: payments, opponents, and payouts. Nothing touches real money.
- State is in-memory. A refresh resets the run. This is intentional for a demo.
- `picsum.photos` supplies placeholder imagery, so it needs network to render photos.
- Demo controls on the entry page force a two-way or four-way tie, since ties are only 11% of
  rounds and would otherwise be tedious to observe.
- Browser storage APIs are deliberately not used.

## Working style for this project

- Claims about rates, ties, and economics get verified by computation, not asserted. Every number
  in the docs traces to a script in `analysis/`.
- Tradeoffs are documented explicitly rather than silently resolved.
- When a structural change is made (group size, scoring, rake), re-run the analysis — constants
  tuned for one configuration have repeatedly turned out to be wrong for another.

## Not yet built

Backend, accounts, real payments, photo moderation, anti-collusion, matchmaking and queueing,
persistent Hall of Fame. Real-money operation would need licensed payment processing and
jurisdiction-specific legal review; neither is addressed here.
