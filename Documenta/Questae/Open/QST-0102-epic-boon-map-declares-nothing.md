# QST-0102 — `Map_of_Epic_Boons` declares nothing, so the gated boon path is dead

- **Type:** bug / architecture
- **Priority:** 🟠 high
- **Status:** Open
- **Owner:** unclaimed
- **Route to:** Technical Team · Architecture (Druid)
- **Related:** QST-0101 · QST-0091.3 · `AtlasLusoris/AtlasOfFeats/Map_of_Epic_Boons.py`

---

## 🔍 Diagnosis (what & where)

`Map_of_Epic_Boons.py` is nineteen lines. It imports `Make_Epic_Boon` and never
calls it. All twelve boon names are bound to `None`.

The consequence runs downstream: `_EPIC_BOON_DECLARATIONS` stays empty, so
`all_epic_boons()` and `available_epic_boons()` return nothing, and the whole
TagKit boon path is dead, including its real level-19 precondition.

The texts that do reach a sheet live in `Grimoire_of_Features` instead, drawn by
`ApplyEpicBoon`, which uses the global `random` and prints "Epic Boom!".

## 🧾 Evidence

- The twelve `None` bindings are the entire file body.
- The level-19 gate exists only on the dead path, so nothing enforces it on the
  live one.

## 🎯 Desired outcome

1. The twelve boons are declared with `Make_Epic_Boon`, or the file is deleted
   and the live path becomes the record.
2. The level-19 precondition is enforced wherever the draw actually happens.
3. `ApplyEpicBoon` draws from the Character's own Dice (Decree 0002) and stops
   printing to the console.
