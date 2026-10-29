# TOP Review — 2026-10-29 — One Character, two identity ledgers

Commissioned by Julio in chat ("adapt GenLegend to the TOP paradigm. Open
small PRs for each change, and review the functionality for a cohesive
design"), not the scheduled Monday pass. Ruled by his word of the same day:
QST-0144 was closed for being too big; every change is a small step,
progressive and reviewable.

## 1. Files read

The Player path end to end, against the paradigm's own sources:

- **The law:** `spec/SPECIFICATION.md`, `TopKit/GUIDE.md`, `CONTRACTS.md`,
  the Wiki chapters 1.0 to 1.6 and the Director's Rulings register of
  `JulTob/Tag_Oriented_Programming`; the pinned TopKit 0.2.0a3 source in the
  venv, probed call by call; Decrees 0002, 0004, 0007, 0008, 0009; QST-0093.11;
  QST-0142.
- **The code:** GuildKit, TrainingKit, Grimoire_of_Guilds, the 13 Guild kits,
  the 13 Training maps, CharactersKit, Grimoire_of_Characters,
  Grimoire_of_Spellcasters, SpeciesKit whole, BackgroundKit surfaces, FeatKit,
  FeaturesKit, ProficiencyKit, SkillsKit, Grimoire_of_Skills, AlignmentKit,
  GendersKit, scores and saves, AtlasInventarium, Map_of_Weapon_Masteries,
  AtlasLudus, app/random, Charts_of_Build, AtlasVenustas, the sheet
  components, and the gates in `scripts/`.
- **The in-flight work:** PRs #98, #99, #102 (now closed), #104, #105, #106,
  and every open issue, so nothing already minted was minted twice.

Method: one reader per region, findings refuted against the cited lines and
by live probes in the venv before anything below was written.

## 2. The finding

**The Character keeps its identity twice, and the second ledger is the one
most of the code reads.** Membership in the Tags is the truth TOP defines:
`char in Wizard` answers correctly on main, because Guild is a `@Flag` Tag.
But every identity Imprint also mirrors itself into a plain attribute —
`char.char_class`, `subclass`, `specialization`, `species`, `heritage`,
`creature_type`, `background`, `alignment`, `gender` — and the mirrors, not
the Tags, feed the big dispatches:

- `set_Skills` is a 260-line `elif char.character_class == "..."` ladder
  (`Grimoire_of_Characters.py:742-1003`);
- hit points go through `health_dice( char.char_class )` (`:346,:355`);
- the legacy Progression keys a dict by the class string
  (`Map_of_Classes/Codex_of_Progression.py:22-48`);
- the Spellcasters Grimoire picks its Python class by comparing
  `char_class`/`subclass` strings in `_bears` (`:2615-2631`), under a
  docstring that wrongly claims membership does not answer;
- race and subrace derive from `species_to_race_and_subrace( char.species )`
  (`:441-456`), the exact drift #68 names.

Decree 0002 ratified a root of seven stored things; a summoned Character
carries about sixty plain attributes. Every string gate is a place where the
two ledgers can disagree, and the paradigm's answer is already in the tree:
the Tags know. The cohesive design is one ledger — membership — read
everywhere, with the mirrors retired one reader at a time.

## 3. Evidence

- Probe on main: for a summoned Wizard, `"Wizard" in char` is True and
  `char in GUILDS["Wizard"]` is True, so no string dispatch is necessary.
- Probe: applying a second Guild flips `primary_ability()` and fires
  `TagOverwriteWarning` twice (#117): the per-Guild Actions crush, they do
  not compose.
- The counts and `file:line` for each dispatch are in the issues and PR
  bodies linked below; each was re-read at the cited lines before filing.

## 4. The plan, as small points

Landed this pass, one PR each, gates run before and after:

1. **PR #107** — two Dark Gifts crashed generation on an import that never
   existed (QST-0095): 7 of 200 seeded Humans failed; now 0. Plus Julio's
   review ask: a gift teaches a tongue the Character does not speak yet.
2. **PR #108** — Path lessons gate on the Specialization Shape, never on the
   `char.subclass` string (QST-0139's gate half; removes one mirror reader).
3. **PR #109** — Map_of_Weapon_Masteries defined its first half twice; the
   dead halves are gone, 142 lines, behaviour identical by construction.
4. **PR #110** — the Fighter map said three things three times (two helpers
   tripled, three flavour lines pasted thrice and printed thrice).
5. **PR #111** — the Cleric's Divine Order and Blessed Strikes roll on the
   Character's own Dice, the last two Training draws outside Decree 0002.
6. **PR #112** — SpeciesKit recovery debris: eight never-imported files.
7. **PR #113** — FighterKit's self-test gate runs instead of crashing.

Next small steps, in order of value over risk, each one PR when Julio says go:

8. `spellcaster()` dispatches by membership; `_bears` goes (~70 lines).
9. Hit points from the Guild's hit die Report (#42; closes #27 with it).
10. `apply_species_features` and race/subrace read `Current_Species` (#68).
11. Off-sheet lessons declare `on_sheet=False` themselves; the
    `OFF_SHEET_TRAININGS` name list goes (also frees the Warlock's Pact
    Magic chips that the list silences today).
12. The Celestial patron draws once in the Shape's Imprint, not inside the
    description reader at render time (Decree 0009 §7).
13. The eleven hand-written `SPECIALIZATIONS = (...)` tuples read the
    Guild's catalogue, as Fighter and Warlock already do.
14. Pin catalogues for Guilds, Specializations and Lessons replace the
    hand-kept registries, one registry per PR (re-landing #102's station 4
    in steps).

## 5. Questions for Julio

1. The mirrors: may each later PR delete a mirror attribute once its last
   reader asks membership, or do you want every mirror kept until one big
   cut? (Small steps suggest the former.)
2. Issue #114: is the Elf lineage rule "the drawn ability" (the Entry is
   wrong) or "the best mental score" (the draw is wrong)?
3. Issue #117: what should `primary_ability` answer on a two-Guild
   Character, once multiclass lands?
4. Issue #119: when Extra Attack becomes one Tag, does the prose unify or
   stay per-Guild?
5. The Wiki of Tag_Oriented_Programming documents behaviours newer than the
   pinned 0.2.0a3 (`in` is raw membership on a3, `@Flag` takes no words, no
   null Underlay, `Tags()` returns leaves only, `@Rip` on a Record is
   silently ignored, a TagError in an Imprint rolls the whole call back).
   Worth a QST-0093.10 addendum upstream, so an author reading the Wiki
   against the a3 pin is not misled?

## 6. The issue quests

Opened this pass: #114 (Elf lineage ability), #115 (Druid get_stats
NameError), #116 (four red self-test gates), #117 (primary_ability
overwrite), #118 (the Questa ledger collides), #119 (Extra Attack as one
Tag). Already minted and confirmed, not re-filed: #44, #47, #68, #90, #91,
#42, #43, #37/#34 and the QST-0142 stations.

## Where the design is already one design

Worth saying plainly: SpeciesKit's Shapes and gates, AlignmentKit's axis
Preconditions, GendersKit, Unarmored_Defense and Draconic_Resilience,
GearKit's `Equipped` Tag with AC derived at read time, and the build walk in
Charts_of_Build are the paradigm done right, and they are the pattern every
step above copies. The two-ledger seam, the legacy Progression that still
feeds all 13 Guilds, and the 3,200-line Spellcasters hierarchy whose class
names collide with the Guild Tags are where the rent is still paid twice.
