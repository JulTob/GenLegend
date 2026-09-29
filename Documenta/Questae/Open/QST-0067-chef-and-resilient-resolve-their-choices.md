# QST-0067 — Chef and Resilient must resolve, record and print their choices

- **Type:** bug / feature mechanics
- **Priority:** 🟠 high
- **Status:** Open
- **Owner:** unclaimed
- **Route to:** Technical Team
- **Related:** QST-0065 · QST-0066 · `AtlasLusoris/AtlasOfFeats/Map_of_General_Feats.py`

---

## 🔍 Diagnosis (what & where)

Two General feats still read as though the player has a pick to make, in a
generator where every pick has already been made.

**Resilient** (`Map_of_General_Feats.py` ~line 455) declares
`asi=('STR','DEX','CON','INT','WIS','CHA')` and nothing else. Its catalogue
text says *"Choose one ability score in which you lack saving throw
proficiency. Increase that score by 1 … and you gain proficiency in that
ability's saving throws."*

The ability increase resolves correctly through `_sheet_feat_description`, so
the sheet does say *"Your Wisdom was increased by 1."* But:

- the **saving throw proficiency is never granted**, only described;
- the saving-throw table on the sheet therefore does not reflect it;
- the RAW constraint *"in which you lack saving throw proficiency"* is not
  enforced, so the feat can land on a save the Character already has.

**Chef** (~line 258) grants Cook's Utensils through `_Fixed_Training` and prints
a generic summary. It does not print the resolved ability, the number of
creatures fed (4 + Proficiency Bonus), or the number of treats (Proficiency
Bonus). It is also offered to Characters who already hold Cook's Utensils,
where the tool half of the feat grants nothing.

## 🧾 Evidence

Keen Mind in the same file already shows the pattern this needs:

	training=_Choice_Training(
		(Arcana, History, Investigation, Nature, Religion),
		"feat.Keen_Mind.training",
		),
	training_record="keen_mind",
	describe_training=_Describe_Resolved_Choice,

Choice drawn from a named Dice Bag, recorded, and printed as the resolved
answer. Neither Chef nor Resilient uses any of it.

Julio's framing, 2026-08-24:

> Resilient should also choose the ability score and display to the user
> something more informative with the choice made like "Your {score} was
> increased by 1, and you gain proficiency on {score} Saving Throws". The
> saving throw table should reflect the choice too.

and for Chef, the resolved shape he wants:

> ***Ability Score Increase.*** Increased your {stat} by 1.
> ***Cook's Utensils.*** You gain proficiency with Cook's Utensils.
> ***Replenishing Meal.*** … enough for 4 plus your Proficiency Bonus …
> ***Bolstering Treats.*** … a number of treats equal to your Proficiency Bonus …

## 🎯 Desired outcome

- Resilient draws one save it does **not** already have, grants the proficiency
  for real, and the saving-throw table shows it.
- Chef prints its resolved ability and its two resolved counts.
- Chef becomes unavailable to a Character who already has Cook's Utensils.
- Both read in the past tense for what was settled, and stay present tense for
  what is used at the table.

## 🧭 Notes for the Agora / implementer

- **Grant it, do not merely say it.** `Grant_Resistance` exists in
  `FeaturesKit.py` because a feature that only *describes* a resistance reads
  correctly and plays wrong; that bug was found four times. A save proficiency
  is the same trap and wants the same treatment.
- The unavailability half is now cheap: `Make_General_Feat` takes
  `redundant_if`, and `_take_first_that_applies` drops a refused candidate and
  tries the next, so a Precondition is handled gracefully by the selector.
- Resolved counts belong in the Entry **and** as Chips, per
  `Documenta/Canon/Project-Model.md`.
- Entries are projections now (`FeaturesKit.Feature`): a callable description
  resolves against the Character when the sheet is read. The *choice*, however,
  must still be settled once in `apply`, guarded, against a named Dice Bag —
  an Entry may read but never decide.

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

**Weighting:** reach ⟨1⟩ × severity ⟨3⟩ = **3** · council leaning: `build`
*(Reach 1: two feats. Severity 3: Resilient currently describes a proficiency
it never grants, which is a correctness fault on the sheet.)*
