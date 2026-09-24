# QST-0091 — One file per thing: a Species, a Guild, a Specialization, a Background, and the Level itself

- **Type:** design
- **Priority:** 🟠 high *(the structural goal every content questa should serve)*
- **Status:** Open — awaiting the Agora on the declaration shapes
- **Owner:** unclaimed (minted by Claude on Julio's word, 2026-09-06)
- **Route to:** Architecture (Druid) · Methods (Wizard) · Contracts (Warlock) · Simplicity (Monk) · Lorekeeper
- **Parent:** —
- **Sidequests:** QST-0091.1 (Species) · QST-0091.2 (Guild and Specialization) · QST-0091.3 (Level and multiclass) · QST-0091.4 (Background)
- **Related:** Decree 0002 · Canon/Code-Style "repeat patterns modularly" · TagKit-Doctrine rule 6 · QST-0016 · QST-0020 · QST-0031 · QST-0035 · QST-0042 · QST-0047 · the TagKit 0.2 Integration Plan (2026-09-06)

> Minted under `Documenta/` (Julio, 2026-09-06). Julio's words: "Species: adding one should be one file. That is the perfect goal. But not just for Species. For Class, known level (and apply the multiclass synergies too), and also backgrounds."

---

## 🔍 Diagnosis (what & where)

The Doctrine promises that new content "slots into the existing Tag structure the same way existing content does", and that touching five unrelated files to add a race is a smell. Measured on 2026-09-06, every content axis still touches several. The numbers below count files a contributor must edit or that hard-code the name.

| Axis | Adding one today touches | The kernel that is already right |
|------|--------------------------|----------------------------------|
| **Species** | its package, a declaration Pin, `catalog.py`, the `__init__` re-exports, the hand-written dispatch in `resolution.py`, the legacy `Map_of_Species` dict, and flavour maps keyed by the species *name* (14 files mention Goliath outside SpeciesKit) | the Species Form with Traits as bases and one `Set_Physiology` Imprint |
| **Guild** | `Make_Guild` (bytecode today), `AtlasOfGuilds/__init__` list, `Scroll_of_Constants.classes()`, `Codex_of_Progression` mapping, `Grimoire_of_Health` table **and** string ladder, `TrainingKit` module list, `Grimoire_of_Spellcasters` (a `Spellcaster` subclass, slot and prepared tables, an `elif _bears` ladder, an HTML block), a legacy `Training/<Guild>.py` if-ladder, an `AtlasOfTraining/Map_of_<Guild>_Training.py`; 28 files name Paladin outside its kit | `Make_Guild`'s single declaration of hit die, saves, armour, weapons, vocation, leanings |
| **Specialization** | its kit (right), plus `Scroll_of_Constants.subclasses()`, `SUBCLASS_CASTING_ABILITY`, the legacy `Training/<Guild>.py` ladder keyed on `Subclass == "Evoker"`, and `Map_of_<Guild>_Training` gated on a `path=` string | FighterKit: FEATURES, CHOICES, RESOURCES as Reports on the Tag; TrainingKit materializes them |
| **Level** | each Guild's per-level features are an if-ladder in `Training/<Guild>.py`; the universal levels (feats at 4, 8, 12, 16, boon at 19) are repeated in every ladder (80 call sites); hit dice live in three places; proficiency bonus in `Map_of_Scores`; spell slots per caster class inside `Grimoire_of_Spellcasters` | `guild_hit_die`, `Join_Guild(levels=)` and the per-Guild level ledger in the Guild source |
| **Multiclass** | `Join_Guild` and `Multiclassed` exist and `Make_Guild` records `multiclass_gains`, but the generator never multiclasses, `Training/Multiclass.py` is a two-class stub, and no Guild declares its multiclass prerequisites or caster progression (full, half, third, pact) | the per-Guild level ledger |
| **Background** | `Make_Background` is one call (right), yet 12 files name Farmer or Hermeticist outside BackgroundKit: stories, titles, gear, materials, familiars, the sheet, and the legacy `Map_of_Backgrounds` | `Make_Background`: abilities, skills, tools, Origin Feat, prose, audiences, source, in one call |

Two cross-cutting causes explain most rows:

1. **Catalogues listed twice.** A Species is declared and then listed in `Map_of_Species`; a Guild is declared and then listed in `classes()`, `HIT_DIE_TABLE`, `Codex_of_Progression`; a Specialization is declared and then listed in `subclasses()`. Every second list drifts (the Ranger list already has).
2. **Names as keys.** Flavour, gear and story maps ask `if species == "Goliath"` or `"Paladin" in character` instead of asking a Tag. Adding a thing then means finding every string that spells it.

## 🧾 Evidence

- Measurements above: `grep -rlw Goliath`, `grep -rlw Paladin`, `grep -rlwE 'Hermeticist|Farmer'` across `Atlas*` and `app` on `main` at `cd80225`.
- `Training/Ranger.py` fell back to `Scroll_of_Constants.SUBCLASSES["Ranger"]`, a list that lacks Fey Wanderer and names Horizon Walker; the Guild's real catalogue is `Specialization_Choices("Ranger")` (QST-0089).
- `Grimoire_of_Health.hit_dice` is a twelve-branch string ladder beside `HIT_DIE_TABLE` and `guild_hit_die`: three sources of one number.
- `Codex_of_Progression.get_class_progression` is a hand-written `mapping` of thirteen names to thirteen classes.
- The Player generator calls `Apply_Guild` once and never `Join_Guild(levels=)`: multiclass is declared machinery with no producer.
- The two axes closest to the goal, Background and the Fighter Specializations, are exactly the two written as declarations on the Tag.

## 🎯 Desired outcome

**Adding a thing is one file, and at most one import line at the load boundary.** Concretely, for each axis a fixture proves it:

- a homebrew Species declared in one new file appears in the picker, builds across the sweep, and replays;
- a homebrew Guild declared in one new file (with its Specializations in the same kit) does the same, including hit die, saves, spell slots and per-level features;
- a homebrew Background declared in one new file does the same;
- a Level is declared once: the universal levels (feats, boon, proficiency bonus) in one place, each Guild's per-level grants as data on its Tag, and a multiclass Character's level table as the composition of its Guild ledgers under the 2024 multiclass rules (prerequisites, gains on a dip, caster progression, no stacking of Extra Attack).

Nothing is listed twice: every catalogue is derived from the declarations. Nothing asks a name: flavour and gear ask Tags (Kinship, Vocation, Flags).

## 🧭 Notes for the Agora / implementer

- **This questa decides shapes, not code.** Each sidequest ends with a declaration shape for its axis and a Dialog entry; Julio decrees; implementation questae follow per axis.
- **Constraints from Canon:** refactor the files that exist, never a parallel layer (Decree 0002, Code-Style); the next file must be predictable from the last; catalogues derive from declarations (Doctrine rule 6; Pin Fields are that derivation, and TagKit 0.2.0a3 restores Pins under STEP-SPEC-9).
- **TagKit 0.2 gives the vocabulary:** Reports on the Tag that inherit through `(tag, inherited)` are how a Specialization extends its Guild's FEATURES and a Heritage extends its Species' Reports; Records that pile up through `(agent, stored)` are how spells, languages and hit points compose across Species, Guild and Background; `@Flag` is how flavour asks a word. Pins are back in 0.2.0a3 (`@Pin`, keyword-only inputs): a catalogue is a Pin Field read with `Available[:]`, exactly as QST-0081 designed it.
- **Order:** Species and Background first (closest to done), then Guild with its Specializations, then Level and multiclass (needs the Guild shape settled). The TagKit 0.2 migration (steps 1 to 7 of the Integration Plan) precedes the Guild and Level work because `Make_Guild` is still bytecode and Pins block the Species catalogue.
- **Do not** start by deleting the legacy ladders. Declare first, prove coverage with `training_covers()`, retire each ladder the day its coverage is complete.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** —
- **Practice/preference to remember:** —

---

## 🏛️ Council

> Architecture Consul (Druid): The goal is one sentence and the diagnosis is one table. Every row where the count is above one has the same two causes: a second list, or a name used as a key. Fix the causes, not the rows.
> Methods Consul (Wizard): Background and FighterKit already are the shape; do not invent a third. Measure each axis against those two and copy what they do right.
> Contracts Consul (Warlock): "One file" is only true if the file can promise its own soundness: a homebrew Guild that declares no saves must be refused at declaration, not discovered at level five. Preconditions on the declaration, not on the sheet.
> Simplicity Consul (Monk): A level table is data. Thirteen if-ladders that all say "at 4, a feat" are thirteen chances to disagree. One place for the universal levels, one tuple per Guild, and the ladders go.
> Lorekeeper (Elf Sage): Names are for people; Tags are for rules. When a title map wants "the dwarven kind", it wants Kinship, not the string "Dwarf". Julio built Kinship for exactly this; use it before asking for anything new.

**Weighting:** reach 3 × severity 2 = **6** · council leaning: `needs a Dialog` (four shapes to decree; then `build` per axis)
