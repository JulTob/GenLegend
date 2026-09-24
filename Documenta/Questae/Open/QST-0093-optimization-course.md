# QST-0093 — The optimization course: from the recovered tree to TagKit 0.2.0a3 and one file per thing

- **Type:** design · chore/cleanup
- **Priority:** 🟠 high
- **Status:** Open (the course; each station is a sidequest with its own gate)
- **Owner:** unclaimed (minted by Claude on Julio's word, 2026-09-06)
- **Route to:** Architecture (Druid) · Safety (Paladin) · Workshop (Artificer) · Methods (Wizard) · Julio
- **Parent:** —
- **Sidequests:** QST-0093.1 · .2 · .3 · .4 · .5 · .6 · .7 · .8 · .9
- **Related:** QST-0091 (one file per thing) · QST-0042 · QST-0036 · QST-0052 · Decree 0002 · Decree 0004 · Decree 0008 · the TagKit 0.2 Integration Plan (2026-09-06, re-evaluated below)

> Minted under `Documenta/` (Julio, 2026-09-06: "Pins have been reintegrated into TOP. Re-evaluate the migration. Plan an optimization course through questae.")

---

## 🔍 Diagnosis (what & where)

**Re-evaluation after Pins returned.** Upstream PR #4 (`Pins: Tags as Targets`, STEP-SPEC-9, TagKit 0.2.0a3, head `e53659f`, 106 tests green, mergeable) restores Tags as Targets: a Tag marked `@Pin` applies to Tags only; its Records land as Reports on the pinned Tag; membership, Fields, gates, Rip and views all work with the Tag in the Agent's seat. Proven on 2026-09-06 against the SpeciesKit declaration pattern in a scratch venv: `@Pin` on `Declared_Species`, keyword-only inputs (`def WEIGHT(tag, *, weight=0)`), `Available[:]` as the catalogue, Reports inherited by Heritages, membership not inherited, the root refused by name (`Species_Tag_Only`).

Consequences for the migration plan of 2026-09-06:

- **The one design step is gone.** "Pins become Reports and a class-tree catalogue" is replaced by a mechanical step: mark the declaration Pins `@Pin` (SpeciesKit's `Declared_Species`, BackgroundKit's `Background_Audience`; a Shape of a Pin is a Pin) and move Record inputs to keyword-only (26 input lines in SpeciesKit, none in BackgroundKit's audiences). QST-0081's "catalogues are Pin Fields" stands.
- **Everything else in the plan holds:** `Has` → `in` (9 sites), `X = Report(v)` → `@Report def X(tag)` (6 sites, one inside the Guild bytecode), `Tag.Rip` → `del Tag[agent]` (4), one `Label()` caller, `@Flag` for the 66 string probes, ten `@Post` sites re-read for the no-rollback rule.
- **Nothing bump-coupled can land before the bump.** `@Report def`, `@Pin`, `@Flag`, `del Tag[agent]` do not exist on the pinned 0.2.0a1; only `Has` → `in` runs on both. So the migration is one questa on one branch, taken when PR #4 merges, and the stations before it are the ones independent of the TagKit version.
- **The Player path is clean.** The wide sweep of 2026-09-06 (1,164 requests, summon + project + render) has zero failures after QST-0092. The course optimises structure, not correctness.

## 🧾 Evidence

- `gh pr view 4 -R JulTob/Tag_Oriented_Programming`: OPEN, MERGEABLE, "STEP-SPEC-9 at Vetting; the Director sets Cleared".
- Dry run under 0.2.0a3 with `Has` shimmed: SpeciesKit still refuses (`@Pin` mark missing, inputs positional), GuildKit and BackgroundKit fail on `Report(value)` (the first inside `Grimoire_of_Guilds`' bytecode); SpellsKit, FeaturesKit, AlignmentKit, GendersKit, Items, Adventure import.
- `git show 65edc0f:AtlasLusoris/GuildKit.py` (2,997 lines) and `git show 06b93a5:AtlasInventarium/Map_of_Gear_Titles.py` (1,980 lines) cover the two Player-path bytecode shims' public APIs name for name.

## 🎯 Desired outcome

The course, in order. Each station is one questa branch, gated by compile, smoke, the 78-cell sweep, the wide sweep, and the replay rite, fast-forwarded into `main` when green.

| Station | Questa | Needs | Ready |
|---|---|---|---|
| 1 | QST-0093.1 Guild body back to source (65edc0f) | nothing | now |
| 2 | QST-0093.2 Gear Titles back to source (06b93a5) | nothing | now |
| 3 | QST-0093.3 Delete what nothing imports | nothing | now |
| 4 | QST-0093.4 Standing gates: the wide sweep in `scripts/`, in Make, in CI | nothing | now |
| 5 | QST-0093.5 The pin moves to 0.2.0a3 | stations 1 and 2; PR #4 merged | when Julio merges upstream |
| 6 | QST-0093.6 Doctrine resync (closes QST-0036) | station 5's vocabulary | with station 5; Julio ratifies |
| 7 | QST-0093.7 Cut the Player path loose from legacy `AtlasAlusoris/` | stations 1 and 2 | now |
| 8 | QST-0093.8 One deploy path | Julio's target decision | after the decision |
| 9 | QST-0093.9 One Documenta | nothing | now |
| 10 | QST-0093.10 Suggest to TopKit: three findings from the pin | Julio files §2 and §3 upstream | §1 fixed in 0.2.0a4 `main` |
| 11 | QST-0093.11 Applying TopKit: the patterns | nothing | Solved 2026-09-24 |
| 12 | QST-0093.12 Unarmored Defense is one Tag | nothing | landed; four questions open |
| 13 | QST-0093.13 Tag factories are made: `Build_` becomes `Make_` | station 5 | Solved 2026-09-24 |
| 14 | QST-0093.14 The build walk, first slice | Decree 0009 | landed (Chips only); five questions open |
| then | QST-0091.1 to .4 implementation, one axis at a time | station 5 | after the bump |

Stations 1, 2, 3, 4, 7 and 9 need no upstream change and no decision beyond "go". Stations 5 and 6 wait for the merge. Station 8 waits for the target.

## 🧭 Notes for the Agora / implementer

- One station per branch; never two stations in one commit. Close before you open (Decree 0008).
- Station 5 pins the **merge commit** of PR #4 on upstream `main`, never the PR head: the Doctrine pins upstream commits deliberately, and a PR head can be rewritten.
- Station 3 is the only deletion pass; it stops at what has zero importers. Anything with one importer is a fold, not a deletion, and belongs to station 7 or to QST-0091.
- After station 5, QST-0091.1 (Species) is the first axis, with the naming design (names as Species Reports) as its first sidequest if Julio mints it.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** —
- **Practice/preference to remember:** —

---

## 🏛️ Council

> Safety Consul (Paladin): Four stations can run today with zero risk to the product; run them before the one that waits on upstream, so the bump lands on source, not on bytecode.
> Architecture Consul (Druid): Pins returning is the paradigm keeping a promise it had made in STEP-SPEC-1. The catalogue design was right; only the mark was missing.
> Workshop Consul (Artificer): Station 4 first among the free ones: every later station is cheaper to prove once the wide sweep is one command.
> Methods Consul (Wizard): Bump-coupled changes are one branch, one commit, one gate. Splitting them makes the tree lie about which TagKit it runs on.

**Weighting:** reach 3 × severity 2 = **6** · council leaning: `build` (stations 1 to 4, 7, 9) · `needs a Dialog` (station 8) · `defer` (5 and 6 until upstream merges)
