# QST-0066 — Feat availability is a second copy of the Preconditions

- **Type:** refactor
- **Priority:** 🟠 high
- **Status:** Open
- **Owner:** unclaimed
- **Route to:** Technical Team
- **Parent:** —
- **Sidequests:** —
- **Related:** QST-0058 (recover from a failed draw) · QST-0065 · `AtlasLusoris/FeatKit.py`

---

## 🔍 Diagnosis (what & where)

`Make_General_Feat` declares a feat's admission rules as `@Pre` gates:
`Rank_Reached`, `Ability_Met`, `Spellcasting_Met`, `Prerequisite_Met`, and now
`Not_Redundant`.

`available_general_feats` (`FeatKit.py` ~line 926) then **re-implements every
one of those gates by hand** as a filter over `_GENERAL_FEAT_DECLARATIONS`:
min level, repeatable-and-owned, `ABILITY_ANY` against `ABILITY_MIN`,
`REQUIRES_SPELLCASTING`, `REQUIRES_FEAT_ANY`, `REQUIRES_WEAPON_MASTERY`.

Two copies of one truth, and nothing ties them together. A gate added to the
builder is invisible to the selector until somebody remembers to add a matching
filter, and the failure is silent in one direction and fatal in the other:

- gate exists, filter missing → the selector offers a feat the Tag will refuse,
  and a refused `@Pre` **raises**, so generation dies rather than picks again;
- filter exists, gate missing → the rule is unenforced anywhere else.

`available_epic_boons` and `available_fighting_styles` have the same shape.

## 🧾 Evidence

**It has already happened, twice, in one sitting.**

1. `Not_Redundant` (the gate that stops Lightly Armored being handed to a
   Character already trained in armour) was written into `Make_General_Feat`
   but **never added to the Tag's `namespace` dict**, so it was dead code. It
   was reported as verified on the strength of a check that only restated the
   Character's armour training and never exercised the gate.

2. Once registered, it fired — and the selector was still offering the feat.
   Measured before the recovery loop existed: **Lightly Armored appeared in
   `available_general_feats` for 50 of 60 Barbarians.** Every one of those
   would have raised `TagPreconditionError` on application.

Related and separate, found in the same pass and **already fixed**: the ASI
preamble regex matched only `"Increase your …"`, so **Ability Score
Improvement** and **Skill Expert** (which say `"Increase one ability score …"`)
printed the instruction *and* the result on the sheet.

Audit that came out clean, for the record: **547 feat entries across 74
distinct feats — zero printed an ability the feat is not permitted to raise.**
The ASI resolution machinery itself is sound.

## 🎯 Desired outcome

One statement of a feat's admission rules, and one only.

`available_*` should answer "would this Tag accept this Character?" by asking
the Tag, not by restating its gates. A new `@Pre` should be correct in both
selection and application the moment it is written, with nothing to remember.

Whatever survives should also make the two `available_*` siblings
(`epic_boons`, `fighting_styles`) stop carrying their own copies.

## 🧭 Notes for the Agora / implementer

- **Do not weaken the Preconditions.** Same instruction as QST-0058: the `@Pre`
  is the backstop, and it is what makes recovery possible. Catch it, never
  remove it.
- An interim recovery already exists. `_take_first_that_applies` in `FeatKit.py`
  walks the shuffled pool and drops any candidate whose `@Pre` refuses, so a
  stale filter can no longer crash generation. **It treats the symptom.** The
  duplication is still there and will drift again.
- **Check against QST-0058 before building.** That questa prescribes
  `@guardian` on every draw. `_take_first_that_applies` is a hand-rolled
  equivalent for one seam, and the two approaches differ: `@guardian` retries
  the *draw* (the next dice-bag roll), while this walks an already-ordered pool.
  For feats the pool walk is arguably better, because the order is a stable
  shuffle and re-rolling would spend dice for no reason. Decide whether these
  converge or stay deliberately different, and say which in the resolution.
- Does TagKit expose a way to test Preconditions **without applying**? If it
  does, `available_*` becomes a one-line filter and this questa is small. If it
  does not, that is the thing to build, and it likely belongs in TagKit rather
  than here.
- Ordering constraint: `_stable_available` shuffles from a named Dice Bag so
  the pool is stable per Character. Any rewrite must keep the draw
  reproducible.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** —
- **Moved to Solved:** —

---

## ⚗️ Reward (separate dialog — do not fill during implementation)

- **Reward file:** *(pending distillation dialog)*
- **Distilled:** *(pending)*

---

## 🏛️ Council
*(unheard — routed, not yet convened)*

**Weighting:** reach ⟨3⟩ × severity ⟨2⟩ = **6** · council leaning: `build`
*(Reach 3: every feat, boon and fighting style passes through these selectors.
Severity 2: correctness, but the interim recovery keeps it out of a player's
face.)*
