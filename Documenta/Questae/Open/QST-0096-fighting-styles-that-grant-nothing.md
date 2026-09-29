# QST-0096 — Blessed Warrior and Druidic Warrior grant no cantrips

- **Type:** bug
- **Priority:** 🔴 urgent *(the feat's entire payload is missing)*
- **Status:** Open
- **Owner:** unclaimed
- **Route to:** Technical Team · Lorekeeper
- **Related:** QST-0026.1 (spell render paths) · `AtlasLusoris/AtlasOfFeats/Map_of_Fighting_Styles.py`

---

## 🔍 Diagnosis (what & where)

`Make_Fighting_Style` accepts an optional `apply=` callable and invokes it when
the style awakens. Neither **Blessed Warrior** nor **Druidic Warrior** passes
one.

Both feats exist to grant cantrips: Blessed Warrior gives two Cleric cantrips to
a Paladin, Druidic Warrior two Druid cantrips to a Ranger. Awakening either one
grants a paragraph of text and nothing else. No cantrip is added, no
spellcasting ability is recorded, and the sheet states a benefit the Character
does not have.

The ten other Fighting Styles are unaffected: their benefits are passive and
their text is the whole implementation.

## 🧾 Evidence

- `Map_of_Fighting_Styles.py`: neither declaration passes `apply=`.
- The legacy copy of Druidic Warrior in `Grimoire_of_Features` at least sampled
  two Druid cantrips from the spell lists and rendered them, so the current
  implementation is a regression against the code it replaced.

## 🎯 Desired outcome

1. Both styles pass an `apply=` that grants the cantrips and records the
   spellcasting ability.
2. The cantrips appear in the Magic section, per QST-0069's rule that
   feat-granted spells do not print inside the feature.
3. A generated Paladin with Blessed Warrior and a Ranger with Druidic Warrior
   each show two cantrips on the sheet.
