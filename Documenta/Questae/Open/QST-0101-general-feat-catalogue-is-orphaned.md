# QST-0101 — The General feat catalogue is orphaned from the live generator

- **Type:** architecture / bug
- **Priority:** 🟠 high
- **Status:** Open
- **Owner:** unclaimed
- **Route to:** Architecture (Druid) · Methods (Wizard)
- **Related:** QST-0066 · QST-0093 (one file per thing) · `AtlasLusoris/FeatKit.py`

---

## 🔍 Diagnosis (what & where)

There are two General feat paths and the live one is not the good one.

**The gated path.** `FeatKit` holds `Make_General_Feat`, real preconditions, a
level-4 gate and prerequisite checking, over the 44 declarations in
`Map_of_General_Feats.py`. `Apply_General_Feats` and `available_general_feats`
are called by exactly one thing in the repository: `FeatKit`'s own self-test.
**Nothing outside `AtlasLusoris/AtlasOfFeats/` imports `FeatKit` at all.**

**The live path.** Every class training module calls `ApplyRandomFeats` in
`Grimoire_of_Features`, which draws from a different catalogue with a different
gate.

So the prerequisite logic the project wrote is exercised only by its own test,
and the feats a player actually receives come from elsewhere.

## 🧾 Evidence

- Call-site grep: `ApplyRandomFeats` is called from Fighter, Paladin, Rogue,
  Monk, Warlock, Cleric and Artificer training.
- `FeatKit` has no importer outside its own folder.

## 🎯 Desired outcome

1. One catalogue and one draw, with the gates that already exist.
2. Decide which path is the record: the TagKit one is the project's declared
   direction, so most likely `FeatKit`.
3. The retired path is deleted rather than left as a second answer.
