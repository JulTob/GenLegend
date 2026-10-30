# QST-0151 — A Tiefling's face mixes two legacies

- **Type:** feature · lore (📗) · generator
- **Priority:** 🟡 medium *(Julio, 2026-10-30: "a tiefling creator equivalent to the aasimar: each legacy mixing two options aleatory and combine them to produce a unique character combining horns, colors, eyes, and in this case spells from both legacies")*
- **Status:** Working — the face lands here; the spells are QST-0152
- **Owner:** unclaimed
- **Route to:** Lore (Bard) · Simplicity (Monk)
- **Related:** `Documenta/Canon/Mythos/Tiefling.md` §0 "The variable detail" · `AtlasActorLudi/SpeciesKit/Aasimar/Map_of_Ideals.py` (the model) · QST-0152 (the spells)

---

## 🔍 Diagnosis

The Tiefling canon (§0, "The variable detail") says it plainly: *"The body is
not drawn. Each legacy carries one fixed `HERITAGE_DESCRIPTION` paragraph,
printed verbatim, so the fur, the horns and the eyes are the same sentences on
every Abyssal sheet ever generated. [...] Whether the Tiefling should gain the
same apparatus [as the Aasimar] is a real design question and nobody has asked
it yet."* Julio has now asked it.

## 🧭 What this questa does

A Tiefling keeps its one Heritage Tag (Abyssal, Chthonic or Infernal), and that
Tag keeps every rule it carries today: the Resistance, the spells, the gate
that allows only one. The new part is the **blood**, which is the face:

1. **Two legacies.** The first is the Heritage. The second is drawn from the
   whole list at uniform random, and may be the same one again. A repeat is a
   *pure* blood, and it is neither rarer nor commoner than any particular pair.
   This is the Aasimar's rule for its two Ideals, kept identical on purpose.
   About two Tieflings in three come out mixed.
2. **Three parts, drawn apart.** The horns come from one of the two legacies;
   the eyes come from one of the two, drawn on their own; the fur takes a
   colour from each and weaves them by one of six patterns (*fox red, striped
   with onyx black*). A pure blood wears one colour, in one of three patterns.
3. **A tail** shows when either legacy carries one (today only Infernal does).
4. **The paragraph** heads the Tiefling's own entries, titled with the hells
   it names (*Abyssal*, or *Chthonic and Infernal*), in the place where the
   Heritage paragraph printed until now.

## 🏗️ How it is built (and why)

- **Each legacy carries its own face as plain class data** on its Tag:
  `ORIGIN`, `HORNS`, `EYES`, `FUR`, `TAIL`. This follows Decree 0009 (a Tag
  declares its own data) and the TOP Guide (no side table of Tags kept outside
  TOP). It replaces `HERITAGE_DESCRIPTION` on the three Tiefling legacies; the
  old sentences survive as the first option in each list wherever they could
  be split into parts.
- **`Tieflings/Fiendish_Blood.py`** draws and composes, and reads nothing but
  the legacy Tags. The second legacy is drawn from `Tiefling.HERITAGES`, the
  Species' own declared list, so a fourth legacy would join the draw by being
  declared and nothing else.
- **The draw happens once, in the Heritage's Imprint**
  (`Imprint_Fiendish_Heritage`), from one named Dice Bag,
  `identity.species.Tiefling.fiendish_blood`, that does not depend on the
  level (Decree 0002: every roll through the Character's own Dice; Decree
  0009: a choice is made once in an Imprint; reading is pure). A level-up never
  changes the face. The bag is new and independent, so no other draw moves.
- **Reading never rolls.** `Resolve_Tiefling_Features` prints
  `target.fiendish_blood`, and nothing else.

## 📏 Measured

- SpeciesKit self-test green, with one new test
  (`_test_tiefling_blood_mixes_two_legacies`, 60 seeds: the first legacy is the
  Heritage, every part comes from a legacy of the blood, the Entry prints the
  paragraph) and the level-stability test extended to the face.
- Fingerprint and sheet snapshot: only Tiefling sheets move, and only in their
  Heritage paragraph and its title. Numbers in the PR body.

## ❓ Open, for Julio

1. **Resistance.** The blood mixes the face only. The Resistance stays the
   Heritage's, so a Chthonic-and-Infernal Tiefling resists Necrotic only.
   Mixing it too would be a rule change; say if you want it.
2. **Voices.** The Aasimar's paragraph has four arrangements and three voices
   so two Aasimar at one table do not read alike. This baseline has one fixed
   order. Worth a follow-up once the lines are settled.
3. **Passing.** The canon says Chthonic is the easiest to pass as human and
   Abyssal the hardest to hide. The face does not say so yet; a mixed blood
   would need a rule for which one wins.
