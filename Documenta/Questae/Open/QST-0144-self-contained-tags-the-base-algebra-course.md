# QST-0144 — Self-contained Tags: the Base algebra course

- **Type:** design · tagkit · campaign
- **Priority:** 🟠 high *(every family port after it is written once, in the final shape)*
- **Status:** Open — stations 0 to 4 landed on PR #102 (2026-10-05), every gate identical or declared; stations 5 and up on the rulings below
- **Owner:** unclaimed (minted by Claude on Julio's word, 2026-10-05)
- **Route to:** Architecture (Druid) · Contracts (Warlock) · Methods (Wizard) · Simplicity (Monk) · Safety (Paladin) · Testing (Rogue) · Julio
- **Parent:** —
- **Sidequests:** QST-0144.1 (the pin) · .2 (plain Reports) · .4 (words) · .5 (Pin catalogues), landed · QST-0144.6 (choices inside the Tag; Dice Bags named by the Tag), Open with its inventory · .3 and .7 to be minted
- **Related:** Dialog 0027 · QST-0142 (one Entry, one Chip; stations 1 to 3 landed, 3b in flight) · QST-0093 (the optimization course) · QST-0093.10 (Suggest to TopKit) · QST-0093.11 (the patterns) · QST-0091 and .1 to .4 (one file per thing) · QST-0047 · QST-0036 · Decree 0009

> Minted under `Documenta/` (Julio, 2026-10-05: "analyze and plan a complete implementation with modular integration into GenLegend, making the tags self contained through the Base Algebra and progressive tag implementation").

---

## 🔍 Diagnosis (what & where)

GenLegend has adopted Tag-Oriented Programming but still straddles two shapes. One family, Species, is self-contained: its Form is its Traits, its generator metadata is a Pin, its catalogue is the Pin's Field, and adding a people is one file. Every other family keeps a hand-written list beside its declarations, writes its constants into a class namespace through `Report_Of`, makes its choices in an outer rite instead of inside the Tag that offers them, and is still named as a string somewhere else in the tree. The laws a family shares (who may wear it, how many, where it prints, what it draws from, which words it answers to) are repeated per Shape or per file instead of written once on the family's Base.

Upstream moved while this straddle stood. TopKit 0.2.0a4 (PyPI, 2026-10-02) brings the three things the standing rulings were waiting for: a Flag's words (the 3b ruling "lasting effects are Flags" had to key them by class name), the late-Flag fix (QST-0093.10 §1), and the Field algebra; and it raises the Python floor to 3.12. GenLegend pins 0.2.0a3 and still documents Python 3.10.

Measured on `main` at `eb4ad99`, 2026-10-05 (details and counts in Dialog 0027, Evidence):

| Symptom | Count |
|---|---|
| Hand-kept registries beside Tag declarations | 11 |
| `Report_Of( value )` sites (a workaround for a Report with no value form) | 69 in 11 files |
| Copies of the `Character_Only` gate on family roots | 12 files |
| One-of-a-kind gates written per Shape (ruling 1, QST-0093.11) | 36 |
| Files naming a Species outside `SpeciesKit` (Goliath / Aasimar / Tiefling / Dragonborn) | 15 / 13 / 19 / 21 |
| Files naming a Guild outside its kit and training (Paladin / Monk / Wizard / Rogue) | 27 / 29 / 44 / 28 |
| Direct string comparisons on identity (`char_class ==`, `.subclass ==`, `.background ==`, `_bears(`) | 10 / 17 / 5 / 12 |
| Imprints that apply another Tag (choices made inside the offering Tag, Decree 0009 point 4) | 1 |
| Files still writing `char.features` | 8 |

## 🧾 Evidence

- The upstream delta a3 to a4, feature by feature, with what each one replaces here: Dialog 0027, Evidence §1.
- **The dry run (2026-10-05).** GenLegend `eb4ad99` on Python 3.12, `topkit==0.2.0a3` against `topkit==0.2.0a4`: the smoke (seed 42, level 1) summons the same Character; the replay rite is exact on both; eight kit self-tests pass on both; the same two fail on both at the same lines (stale tests, Dialog 0027 §4); the **fingerprint is identical on 52 of 52** Characters of the default grid; the **sheet snapshot reads the same on 72 of 72** sheets; the **quick sweep is 78 of 78** on a4 with no failure signature.
- The Species reference: `AtlasActorLudi/SpeciesKit/declarations.py` (the Pin), `catalog.py` (`Available[:]`), `Orcs/` (one file per people).
- The 3b ruling and its Monk folder: QST-0142, PR #98 (`AtlasOfGuilds/Monk_Kit/`, `flag=True` keyed by class name because 0.2.0a3 had no words).
- Upstream still lacks the two things QST-0093.10 §2 and §3 ask for (a Report's value form; a Base's gate guarding its family), and holds Trials (STEP-SPEC-15) at Brief with "a character generator that builds a sheet in steps" as its motivating case.

## 🎯 Desired outcome

Every Tag file is self-contained: identity and words, Bases, gates, facts, choices, what it prints, what it wants, its teardown. The family's laws are written once on its Base and inherited through the Form. Every catalogue is a Pin Field. No map spells a Tag's name. TopKit is pinned to its newest release and used where it helps. The port lands one station at a time, each on the standing gates, each either identical or with its difference declared. Adding a Species, a Guild, a lesson or a Background is one file and one line at a load boundary, proven by a fixture.

## 🧭 The stations (one branch, one PR each)

| # | Station | Questa | Needs | Gate reads |
|---|---|---|---|---|
| 0 | The pin moves to 0.2.0a4; Python floor 3.12; the two stale self-tests fixed | QST-0144.1 | nothing | identical (wide grid before the PR) |
| 1 | The root Base `Of_Character` in `CharactersKit`; the twelve roots become its Shapes; the `Only_One` helper | QST-0144.2 | rulings 1, 4, 5; the open PRs ordered (ruling 9) | identical |
| 2 | `SECTION` Report on each family root; the walk fills a missing section from the Form | QST-0144.3 | station 1 | identical (sheet 343) |
| 3 | Words: `@Flag( "Display Name" )` for every lasting effect; maps read words, not names | QST-0144.4 | station 0; ruling 6 | identical |
| 4 | Catalogues are Pin Fields: `Declared_Lesson`, `Declared_Feat`, `Declared_Invocation`, `Declared_Guild`, the small ones | QST-0144.5 | station 1; ruling 7 | identical |
| 5 | Choices inside the offering Tag; Dice Bags named by the Tag | QST-0144.6 | station 4; ruling 8 (given in full, 2026-10-05: *"Apply the suggested Dice Bag. more consistent"*) | declared diff, accepted in advance |
| 6 | The one-file fixture, `scripts/verify_one_file.py` | QST-0144.7 | station 4 | new gate, green |
| 7+ | The family ports in the final shape: QST-0142 stations 3b to 11, QST-0091.1 to .4 | existing questae | stations 1 to 6 | per station |
| 8 | The non-player path opens (Julio, 2026-10-06): the monster module fixed; Races, Archetypes and non-player Features as Tags with Pin Fields and Flags; every draw through the non-player's own Dice Bag; the sheet read from Tags | QST-0144.8 (to mint on the inventory) | station 5; the inventory | non-player fingerprint and sheet, declared |
| 9 | Names and titles read the words (Julio, 2026-10-06): one readable program each, input a Character and a Dice Bag; the words choose the curated list (the Maps), the methods (Markov, entropy, composition) make the name from it; testable with plain lists; the name files reviewed first | QST-0144.9 (the review, then the design) | station 3; station 5 | declared (names and titles move) |
| 10 | The 2024 language rules, checked against the program; the disagreements fixed (Julio, 2026-10-06: "fix the Origin Feats and the languages") | QST-0144.10 (the comparison, then the fix) | station 5 pass 1 (same file) | declared (languages move) |
| ∞ | ~~Doctrine resync~~ closed: Julio deletes the Doctrine (2026-10-05); the TopKit Guides, the Specification and the code are the authorities. Nothing is owed upstream | QST-0093.6 · QST-0093.10 | — | none |

## 🧭 Notes for the Agora / implementer

- **This questa decides shapes, not code.** The twelve rulings are listed in Dialog 0027; implementation sidequests are minted per station after Julio's word (Modus Operandi).
- **Copy Species.** Measure each family against `SpeciesKit`; do not invent a third shape.
- **Two modes, one sentence:** fixed, no inputs, no draw: a Base; otherwise: a grant from the Imprint.
- **Shallow.** One root per family, one Shape level below it. Measure Form depth at every station; it must not grow.
- **Structural stations read identical** (fingerprint 273, sheet 343, sweep 1164, replay, equipment, self-tests). A station that moves a draw declares its diff first, as QST-0142 station 3 did.
- **Never patch TopKit locally.** A blocker is a Suggest-to-TopKit questa; the workaround lives in the Kit that owns the axis and names the questa that deletes it. The authorities on TOP are the TopKit Guides, the Specification and the code (the Doctrine is deleted, 2026-10-05).
- **Do not** start the structural stations under an open PR that edits the same files (#98, #86) until Julio orders the landings.

---

## ❓ Questions to answer before any station runs

The twelve rulings at the foot of Dialog 0027, numbered the same way: 1 the meaning of "Base algebra" · 2 the pin · 3 two modes, one sentence · 4 the home of the root Base · 5 the `Only_One` helper · 6 words · 7 catalogues as Pins · 8 choices inside the Tag and named Dice Bags · 9 the order against the open PRs · 10 upstream filing · 11 the Doctrine text · 12 scope.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** —
- **Practice/preference to remember:** —

---

## 🏛️ Council

> Architecture Consul (Druid): The reference exists and it is ours: Species. Every station is "make this family look like Species", and the plan should be judged by whether a stranger can see that in each PR.
> Contracts Consul (Warlock): Laws on the Base, facts on the Shape. A law written per Shape is a law nobody can change in one place.
> Methods Consul (Wizard): A Pin is the value form of a Report that upstream has not given us yet, and it is the better answer: the declaration validates itself and the Field is the list.
> Simplicity Consul (Monk): Six small structural stations before any large port. Then the ports are written once. The opposite order writes every family twice.
> Safety Consul (Paladin): The pin first and alone. A kernel change under a port makes the diff unreadable, and the dry run already says the kernel change is clean.
> Testing Consul (Rogue): A family is not ported until a homebrew member of it builds from one file. That fixture is the only definition of "self-contained" a machine can check.

**Weighting:** reach 3 × severity 2 = **6** · council leaning: `needs a Dialog` (Dialog 0027 is open; `build` station 0 on Julio's "go")
