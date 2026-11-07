# QST-0152 — A mixed Tiefling's rules come from both legacies

- **Type:** rule change (📒, proposed) · generator
- **Priority:** 🟡 medium *(Julio, 2026-10-30: "... combining horns, colors, eyes, and in this case spells from both legacies"; 2026-10-31: "Do not force that each legacy gives one spell. Let the dice choose." and "Resistances should be included on the generator. Only one must be chosen.")*
- **Status:** Working — built as Julio ruled; awaiting ratification as a 📒
- **Owner:** unclaimed
- **Route to:** Rules (Paladin) · Simplicity (Monk)
- **Parent:** QST-0151 (the blood and its aspect) · **Related:** `Documenta/Canon/Mythos/Tiefling.md` §0

---

## 🔍 Diagnosis

QST-0151 gives every Tiefling a blood of one or two legacies, but only the
aspect reads it. Julio asked for the rules to mix too. The published rule
(2024 Fiendish Legacy) gives one legacy's Resistance and three spells, so this
is a house rule and costs rules compatibility: a 📒 once ratified.

## 🧭 The rule, as built

- **The spells.** The three legacy spells still arrive at character levels 1,
  3 and 5: a cantrip, a level 1 spell, a level 2 spell. Each place is lent by
  a legacy of the blood, one draw per place, as the dice fall. Nothing forces
  a mixed blood to cast from both (Julio, 2026-10-31): a mixed blood lends all
  three from one legacy one time in four. A pure blood keeps its legacy's own
  three spells, exactly as the published rule.
- **The Resistance.** One damage Resistance, never two, lent by one legacy of
  the blood, drawn. A pure blood keeps its legacy's own.
- Nothing else changes: free casts (one per levelled spell per Long Rest),
  casting with slots, the spellcasting ability and its alignment with the
  Guild, and Thaumaturgy.
- **The blood stays hidden** (QST-0151, ruling 2). The entry keeps its
  published title, *Fiendish Legacy: Chthonic*, after the Heritage; it never
  names the second legacy. What it lists is simply what this Tiefling has.

Example, level 5, a Chthonic Tiefling whose blood is Chthonic and Infernal:
*Fire Bolt*, *False Life*, *Darkness*, and Resistance to Fire, all under
*Fiendish Legacy: Chthonic*.

## 🏗️ How it is built

- `Tieflings/Fiendish_Blood.py`: the blood gains `spell_lenders` (one legacy
  per place) and `resistance_lender`. `spells` returns `(level, spell key)`
  rows in the same shape as a legacy's own `SPELLS`, finding each row by its
  level, never by its position (`_spell_at_level` fails loudly on a legacy
  missing a level). `resistance` is the lender's `DAMAGE_RESISTANCE`.
- The places and the Resistance draw from **their own** Dice Bag,
  `identity.species.Tiefling.fiendish_blood.rules`, apart from the legacies'
  and the aspect's, so the rules and the look can each change without moving
  the other (Decree 0002). Places first, then the Resistance.
- `Imprint_Fiendish_Heritage` draws the blood first, then grants the Resistance
  it lends. `Resolve_Tiefling_Features` reads `blood.spells` and
  `blood.resistance`; nothing reads a Heritage's own `SPELLS` or
  `DAMAGE_RESISTANCE` directly any more.

## ⚖️ Evaluation (Decree 0007)

- **Against the rules:** balance is unchanged in count and level (one
  Resistance, one cantrip, one level 1, one level 2, each levelled spell free
  once per Long Rest). Every combination is made of a Resistance and spells
  some published Tiefling already gets at that level. The cost is
  compatibility: a mixed Tiefling cannot be rebuilt from the 2024 book alone.
- **Against the canon:** "the legacy is power, not impairment"; a blood of two
  hells widening what a Tiefling may be keeps to it. The blood stays hidden on
  the page.
- **Against TOP:** the Heritage Tag stays identity and the one-Heritage gate;
  each legacy's rules stay plain class data on its own Tag; the blood is a
  choice made once in an Imprint and only read afterwards.

## ❓ Open, for Julio

1. Ratify the rule as a 📒, or keep it as a generator option.
2. ~~Should the Heritage always lend something?~~ **Ruled (Julio,
   2026-11-01): no.** A blood is two hells and only two; the Resistance, the
   spells, the look and the rumoured origin all fall at random between them,
   so a Chthonic on the sheet may resist Fire and cast Fire Bolt. "That chaos
   is part of the charm."
3. "You know the spells of your legacy" stays as written: the legacy is the
   blood. Reword?
4. ~~Lean the draws toward the Heritage (for example, the cantrip)?~~
   **Answered by the same ruling (2026-11-01): no, uniform.** So a mixed
   blood lends all three spells from one legacy one time in four (each
   place is a coin toss between the two legacies), and half of those times
   it is the *other* legacy. Then the spells read like a pure blood of that other
   legacy under this Heritage's title, and the Resistance agrees with them
   half the time. That is intended: the blood stays hidden, and a sheet may
   mislead. A weighted first draw would cost one line, if Julio ever wants
   the Heritage to lean.
