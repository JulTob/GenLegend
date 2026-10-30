# QST-0152 — A mixed Tiefling casts from both legacies

- **Type:** rule change (📒, proposed) · generator
- **Priority:** 🟡 medium *(Julio, 2026-10-30: "... combining horns, colors, eyes, and in this case spells from both legacies")*
- **Status:** Working — waiting for Julio's ruling on the open questions
- **Owner:** unclaimed
- **Route to:** Rules (Paladin) · Simplicity (Monk)
- **Parent:** QST-0151 (the blood and its face) · **Related:** `Documenta/Canon/Mythos/Tiefling.md` §0

---

## 🔍 Diagnosis

QST-0151 gives every Tiefling a blood of one or two legacies, but only the face
reads it. Julio asked for the spells to mix too. The published rule (2024
Fiendish Legacy) gives one legacy's three spells, so this is a house rule and
costs rules compatibility: a 📒 once ratified.

## 🧭 The rule, as built

- The three legacy spells still arrive at character levels 1, 3 and 5: a
  cantrip, a level 1 spell, a level 2 spell. Nothing about levels, free casts,
  recharge or spellcasting ability changes.
- **Each of the three places is lent by one legacy of the blood.** A pure blood
  keeps its legacy's three spells, exactly as today. A mixed blood draws one of
  the six patterns in which **both** legacies lend at least one place, so by
  character level 5 a mixed Tiefling casts from both hells. Before level 5 it
  may show only one, because the spells still arrive by level: at level 1 there
  is only the cantrip, and patterns such as (0, 0, 1) add the second legacy's
  spell only at level 5. Example: Chthonic and Infernal,
  pattern (Infernal, Chthonic, Infernal): *Fire Bolt*, *False Life*, *Darkness*.
- **The Resistance stays the Heritage's** (the first legacy). Julio's list was
  horns, colours, eyes and spells; Resistance was not on it.
- The entry is titled with the blood: *Fiendish Legacy: Chthonic and Infernal*.

## 🏗️ How it is built

- `SPELL_WEAVES` in `Tieflings/Fiendish_Blood.py`: the six patterns, written
  out one per line, so a reader sees every possible outcome without running
  anything.
- The pattern is drawn in the same Imprint as the face, from **its own** Dice
  Bag (`identity.species.Tiefling.fiendish_blood.spells`), so the face and the
  spells can each change without moving the other (Decree 0002).
- `Fiendish_Blood.spells` gives `(level, spell key)` rows in the same shape as
  a legacy's `SPELLS`, so `Resolve_Tiefling_Features` reads the blood instead
  of the Heritage and nothing else in it changes.

## ⚖️ Evaluation (Decree 0007)

- **Against the rules:** balance is unchanged in count and level (one cantrip,
  one level 1, one level 2, each free once per Long Rest). The power of the
  individual spells differs between legacies, but every combination is made of
  spells some published Tiefling already gets at that level. The cost is
  compatibility: a mixed Tiefling cannot be rebuilt from the 2024 book alone.
- **Against the canon:** the page says "the legacy is power, not impairment";
  a blood of two hells widening what a Tiefling can do keeps to it.
- **Against TOP:** the Heritage Tag stays the single source of the rules it
  owns (Resistance, the one-Heritage gate); the blood is a drawn choice made
  once in an Imprint and only read afterwards.

## ❓ Open, for Julio

1. Ratify the rule (then the canon page gains its first 📒), or keep it as a
   generator option.
2. Should the Resistance mix as well (one of the two, drawn)? Today it does not.
3. Should the six patterns be weighted toward the Heritage (say, the Heritage
   always lends the cantrip)? Today they are uniform.
