# Dialog 0027 — Self-contained Tags: the Base algebra and the progressive port

- **Question:** How does GenLegend take the latest Tag-Oriented Programming (TopKit 0.2.0a4, released 2026-10-02) and finish its integration so that every Tag is **self-contained**: one file says everything about one thing, the family's laws live once on its Base, and the port lands one family at a time with a gate at every step?
- **Raised by:** Julio, in chat, 2026-10-05 ("check the last version of the Tag Oriented Paradigm repo and analyze and plan a complete implementation with modular integration into GenLegend, making the tags self contained through the Base Algebra and progressive tag implementation")
- **Related Questae:** QST-0144 (this plan's course) · QST-0142 (one Entry, one Chip; stations 1 to 3 landed, 3b in flight as PR #98) · QST-0093 (the optimization course) · QST-0093.10 (Suggest to TopKit) · QST-0093.11 (the patterns, Solved) · QST-0091 and .1 to .4 (one file per thing) · QST-0047 (skills and tools as Tags) · QST-0036 and QST-0093.6 (doctrine drift)
- **Related Decrees and Dialogs:** Decree 0002 (the Character root) · Decree 0005 (affinity steers selection) · Decree 0007 (every change is a proposal) · Decree 0008 (branch discipline) · Decree 0009 (the sheet is read from the Tags) · Dialog 0024 (TOP as a paradigm) · Dialog 0026 (the shared core)
- **Consuls called:** Architecture (Druid) · Contracts (Warlock) · Methods (Wizard) · Simplicity (Monk) · Safety (Paladin) · Testing (Rogue) · Lorekeeper advisory
- **Status:** 🟡 open · a proposal with evidence; every ruling below awaits Julio's word (Modus Operandi)

---

## 🧭 Framing

**What was asked.** Three things in one sentence: read the newest TOP, plan the complete integration, and make each Tag self-contained through "the Base algebra" and a progressive implementation.

**How this Dialog reads "the Base algebra".** TOP's Specification calls itself "a precise algebra: one identity, many layers, clear rules for how the layers meet" (spec, opening). The *Base* is TOP's word for the broader Tag a Shape specializes (spec §0.2), and a Form is the Base-first closure of a Tag (§0.4). So the Base algebra, as used here, is two things at once:

1. **the kernel's operators**: apply, membership, Form, Records that pile up, Reports that inherit, Actions that extend, gates, Imprints, Flags, Pins, Fields and their `|`, `&`, `-` (new in 0.2.0a4);
2. **the family roots of GenLegend** (Role, Species, Guild, Training, Trait, Feat, Background, Invocation, Weapon Mastery, Item, Spell): one Base per family, where the family's laws are written once, so that every Shape below it declares only its own facts.

A Tag is **self-contained** when its file says everything about one thing (identity, Bases, gates, facts, choices, what it prints, what it tells others, what it wants, its teardown) and when adding one touches no other file but the load boundary. That is QST-0091's goal, measured.

If Julio meant something else by "Base algebra" (for instance the Field algebra alone, or a new module named Base), question 1 below asks, and the plan bends to the answer.

**Constraints from Canon.**
- Decree 0002: the root stays minimal; everything else is computed or tagged.
- Decree 0009: a Character's features are its Tags; `Find_Build( char )` reads them; choices are Tags made inside the Imprint of the Tag that offers them; reading is pure; port, don't adapt.
- Decree 0007 and the Modus Operandi: this is a proposal; nothing lands without Julio's word; one topic at a time.
- Decree 0008: one station per branch; the gates before any merge.
- QST-0093.11 rulings: sources that differ only in values are one Tag with inputs; sources that differ in behaviour are a Base plus Shapes; a file per hand-written Tag; factories keep their table files; pin PyPI releases only.
- QST-0142 rulings: one Entry, one Chip, Markdown text; one branch and one PR per family; unify everything and do not stop halfway; the Guild Kits shape (3b): one folder per Guild, one file per design unit, linked by Tag; every ability is a Tag awakened by level; lasting effects are Flags.
- TagKit Doctrine: depend on upstream, never vendor; when TopKit is the blocker, Suggest to TopKit.

**A good answer must satisfy.**
1. Every Tag file is readable alone and adding one is one file plus one line at a load boundary (QST-0091's fixture, per axis).
2. The laws a family shares are written once, on its Base, and the Shapes inherit them through the Form.
3. Nothing is listed twice: every catalogue is derived from the declarations.
4. Nothing asks a name: rules ask Tags or Flag words.
5. The newest TopKit is used where it helps and pinned as a release.
6. Every step lands green on the standing gates (fingerprint, sheet snapshot, wide sweep, replay, equipment, kit self-tests) with every intended change named.

**Out of scope.** The NonPlayer path (Decree 0004); the class fantasies and prose (their own Dialogs); the Affinity machine's numbers (ruled in QST-0142, question 5); any local patch of TopKit (Doctrine).

---

## 🔎 Evidence

Measured on 2026-10-05 against `main` at `eb4ad99` and upstream `main` at `ce35726`. **(V)** marks a fact checked by running it in this session.

### 1. Upstream: what 0.2.0a4 brings

- **(V)** PyPI holds `topkit` 0.2.0a3 and 0.2.0a4; 0.2.0a4 is the latest, released 2026-10-02, and the first release through Trusted Publishing. GenLegend pins 0.2.0a3.
- **(V)** 0.2.0a4 requires **Python 3.12 or later** (`pyproject.toml`; 0.2.0a3 said 3.10). GenLegend's container and CI already run 3.14, but `requirements.txt` still says "Python 3.10+" and the Makefile still accepts 3.10 and 3.11.

What changed between the pin and the release, and what each change is worth here:

| 0.2.0a4 feature | Specification | What it replaces or enables in GenLegend |
|---|---|---|
| **A Flag's words**: `@Flag( "Martial Arts" )` makes `"Martial Arts" in char` true beside the class name | STEP-SPEC-17, §1.8 | The 3b ruling "lasting effects are Flags" keyed them by class name (`MartialArts`) because words did not exist yet. Now the word can be the display name, and a rule written as data reads as the rulebook does. |
| **A late Flag takes the `in` seat** | STEP-SPEC-17 (fixed with it) | Closes QST-0093.10 §1. The "Role first" ordering in `CharactersKit` stays right but is no longer load-bearing; its comment goes. |
| **Field algebra**: `Wizard \| Fighter`, `Wizard & Fighter`, `Wizard - Sworn`, on sound, defective and whole Fields, lazily; Pins combine too | STEP-SPEC-13, §2.5 | Sweeps and gates over populations of Characters in one line (`~Player \| ~Guild` is the repair queue); catalogue intersections over Pin Fields (`Available & Player_Handbook_2024`). |
| **A condition is read on the Agent by its name**: `char.Rank_Reached` | STEP-SPEC-14, §2.5 | A gate readable as a plain boolean. Also a **new refusal**: a condition may not share its name with a Record, an Action, a host member or a value the Agent holds. |
| **One seat, one meaning** for Flags | STEP-SPEC-7 amended | A Flag is refused on a host that already answers `in`. `Character` does not; `Spell` does not (see §4 below). |
| **Deletion in layers**; `Scope` Rips only what it applied; rollback keeps the composition door closed | STEP-SPEC-18, §0.7, §3.2 | Correctness fixes; nothing in GenLegend relies on the old behaviour. |
| **Performance**: three leaks fixed; memory per Character down 19 to 34 per cent for Forms of 1 to 6 Tags; keywords, `bool( agent )` and Field walks 53 to 75 per cent faster; tagging 12 per cent | `PERFORMANCE-2026-09-24.md` | Free. Decree 0009 accepted 5.6 ms per Tag on 0.2.0a1; the price fell. |

Three things this Dialog first listed as "not yet upstream". **Corrected by Julio, 2026-10-05**: two of them are not gaps at all.

| Item | What the Dialog first said | Julio's correction | What it means here |
|---|---|---|---|
| A Report holding a plain value | "upstream lacks `Report.Of( value )`; `Report_Of` is a workaround, 69 sites (V)" | *"The first one is supposed to be just a normal report."* | A plain value written as class data on a Tag **already is** a Report in effect: readable on the Tag, never on the Character (probe, §4). Only a function or a Tag class stored as class data turns into an Action on the Character, and that is the one case that needs a Report builder or a Pin Record. Of the 69 sites, almost all wrap plain strings, numbers and tuples **(V)** and can be plain class data; the few that wrap a Tag or a reader stay Reports or become Pin Records. No upstream change is asked. |
| A Base's gate guarding every Shape | "upstream lacks it; one `@Pre` line on each of 36 Shapes is a workaround" | *"The Pre is not a workaround, is the intended explicit behaviour. Explicit over magic. You just need to use a root tag that has no calls themselves, but the shapes branch. … there is no creature that is 'Species', species should not tag, but Elf does tag and also adds the agent to the base Species."* | The root is organisation: nobody applies `Species( char )`. The Shape is where the tagging happens, so the Shape is where the question "is this Character already one of this family?" is asked. The 36 lines are the design, not a debt. No upstream change is asked. |
| **Trials**: `with Try( char ):` undoes a whole draft on a late refusal | STEP-SPEC-15, at Brief, with three questions open for the Director (the noun, how deep the undo goes, a handle form) | *"trials sound like a function + with?"* Yes: a function returning a context manager; on entry it keeps the Character's TOP state, on an exception it Rips what the block applied and restores the state. | The only item that stays upstream. `Character.Accept` retries candidate by candidate meanwhile; `_attempt_player` regenerates. The Director's three answers are the next step, then a branch. |

### 2. GenLegend: where the integration stands

- **The walk exists.** `Charts_of_Build.Find_Build` reads `ENTRIES` and `CHIPS` from every carried Tag's Form, Base first, own declarations only (QST-0093.14, QST-0142 station 1). **(V)** Its self-test passes on 0.2.0a3 and 0.2.0a4.
- **QST-0142 stations 1, 2 and 3 landed** (#94, #95, #97): one Entry, one Chip, Markdown text, Guild Training printing from the build. **Station 3b is in flight**: PR #98 holds the Monk as the first Guild folder (`AtlasOfGuilds/Monk_Kit/`, `Core_Kit` plus four Warrior kits, `flag=True` for lasting effects); twelve Guilds remain.
- **The TopKit surface in use (V)**, counted on import lines: `Pre` 55, `Imprint` 55, `Tag` 26, `Record` 7, `Action` 6, `Underlay` 5, `Flag` 4, `Tags` 3, `Post` 3, `Pin` 3, `Report` 2, `Form` 2. Three files pin (`SpeciesKit/declarations`, `BackgroundKit`, `Grimoire_of_Guilds`). Nothing uses Field algebra, condition members, Flag words, `Scope`, `Rip` or `Outline`.
- **Hand-kept registries (V): 11.** `_TRAINING_DECLARATIONS`, `_GUILD_DECLARATIONS`, `_FIGHTING_STYLE_DECLARATIONS`, `_GENERAL_FEAT_DECLARATIONS`, `_EPIC_BOON_DECLARATIONS`, `_INVOCATION_DECLARATIONS`, `_CRAFT_DECLARATIONS`, `_ORDER_TAGS`, `_MANEUVER_TAGS`, `_MASTERY_TAGS` (declared twice in one file), `_SPECIALIZATION_TAGS_BY_GUILD`. Species alone derive their catalogue from a Pin Field (`Available[:]`).
- **Names as keys (V).** Files naming a Species outside `SpeciesKit`: Goliath 15, Aasimar 13, Tiefling 19, Dragonborn 21. Files naming a Guild outside its kit and training: Paladin 27, Monk 29, Wizard 44, Rogue 28. Direct comparisons: `char_class ==` 10, `.subclass ==` 17, `.background ==` 5, `_bears(` 12.
- **Choices still made outside the offering Tag (V).** Imprints that apply another Tag: 1. Fighting Styles, Invocations, Metamagic (PR #86), Maneuvers and spells are still drawn by outer rites (`after=` hooks, `Apply_*` functions), the pattern Decree 0009 point 4 retires.
- **The legacy store still breathes.** `char.features` is written in 8 files (26 lines); `_SOURCE_PLACES` still guesses a section from a string in `character_sheet.py`; `app.random` is imported in 34 files.
- **Factories.** `Make_Specialization` 55 sites, `Make_Training` 27 wrappers, `Make_Background` one factory for 76 Backgrounds, `Make_Guild` 13. Each writes its constants into the class namespace through `Report_Of`.

### 3. The dry run: GenLegend on 0.2.0a4 (V)

Two virtual environments on Python 3.12, one with `topkit==0.2.0a3` and one with `topkit==0.2.0a4`, the same GenLegend tree (`eb4ad99`), the same commands:

| Rite | 0.2.0a3 | 0.2.0a4 |
|---|---|---|
| `import app.main` + `summon_player( seed=42, level=1 )` | OK, "Nikolas Amexafa" | OK, the same Character |
| `verify_player_replay` | exact | exact |
| Self-tests: CharactersKit, Unarmored_Defense, Charts_of_Build, TrainingKit, Charts_of_Printing, GuildKit, SpeciesKit, FeatKit | 8 of 8 pass | 8 of 8 pass |
| Self-tests: BackgroundKit, SpellsKit | fail (see §4) | fail, same lines |
| Fingerprint, default grid (52 Characters), saved on a3 and checked on a4 | *(baseline)* | **52 of 52 identical** |
| Sheet snapshot, default grid (52 Players and 20 light NonPlayers), saved on a3 and checked on a4 | *(baseline)* | **72 of 72 read the same** |
| Quick sweep (78 cells: every Guild at levels 1 and 5, three seeds) on a4 | | **78 of 78**, 0 failure signatures, 27 s |

So the pin move changes no Character and no sheet on the default grid, and the first new rule of 0.2.0a4 that could bite (a condition named like a Record or a host member) did not fire on any of the 78 cells. The wide grid (273) and the wide sweep (1164) are the pin station's own gate before its PR opens.

### 4. Probes on 0.2.0a4: the behaviours the plan leans on (V)

One script, run on the 0.2.0a4 environment, one assertion per behaviour the stations below depend on:

| Behaviour | Result |
|---|---|
| A Flag's words on a **factory-made** Tag (`type( … )`), applied by hand, after a non-Flag Tag: `"Martial Arts" in char` | True; the class name answers too; an unlisted word is False |
| A `SECTION` Report on a root is read on every Shape; a Shape refines it with `inherited` | `Lesson.SECTION == "Guild"`; the refining Shape sees the Base's value |
| The `Only_One` helper: a `@Pre` written by a function, renamed, assigned on the Shape | the second Shape is refused as `Precondition.Only_One_Species`; the first stays; nothing partial |
| A Base's own `@Pre` gating a second Shape (QST-0093.10 §3) | **still not re-run**: upstream STEP idea B is still needed |
| `Report( value )` (QST-0093.10 §2) | **still refused** (`@Report marks a builder`): `Report_Of` stays until upstream |
| A Pin over factory-made Tags; its Records as Reports; Pin Fields combine (`Declared_Lesson - Core`) | the Field lists both lessons; `Rage.GUILD`, `Frenzy.MIN_LEVEL` read on the Tags; the difference lists one |
| The repair queue over Characters (`~Player`), the sound view, a union of whole Fields | the broken one is queued, the sound one walks, the union counts three |
| A condition read on the Agent by name (`char.Has_Name`) | True on the sound Character, False on the defective one |

### 5. Two stale self-tests, not product defects

- `SpellsKit.__main__` asserts `"evocation" in bolt`: the 0.1 case-insensitive name probe. Since 0.2.0a2 only a Flag answers `in`, exactly by name or word. The product never asks a spell that question; the test does. The fix is the test, or marking `School` and the list Tags `@Flag` with words, if that probe is wanted.
- `BackgroundKit._test_meta_fields` expects 87 audiences; the catalogue moved on. A count typed by hand in a test is the same drift as a registry typed by hand.

Both fail identically on 0.2.0a3, so neither is the pin's.

**Where the evidence was gathered.** The TOP repository was read at `main` (`ce357267`, "Merge pull request #25, trusted-publishing", 2026-10-02): `CHANGELOG.md`, `pyproject.toml`, `spec/SPECIFICATION.md` rings 0 to 2, `TopKit/GUIDE.md`, `TopKit/FIELDS.md`, STEP-SPEC-13 to 18, `examples/dnd_character.py`. The pinned 0.2.0a3 and the released 0.2.0a4 were both installed from PyPI into Python 3.12 environments; GenLegend's own rites ran on each. The probe script of §4 is not committed; it is reproducible from the table.

---

## 🗣️ Deliberation

*Each Consul signs every line and argues from one principle. Objections are constructive. The Council designs; it does not solve.*

Architecture Consul (Druid): Start with the thing that is already right, because the plan should copy it, not invent beside it. The Species family is the one axis that is self-contained today: a Species is a class whose Form is its Traits and its Creature Type (`class Orc( Species, Humanoid, Adrenaline_Rush, Darkvision, Relentless_Endurance )`), the generator metadata is a **Pin** (`Player_Handbook_2024( Orc, weight=80, size_options=…, speed=30 )`), and the catalogue is the Pin's Field (`Available[:]`). No registry, no `Report_Of`, one file per people. That is the Base algebra working: the laws on `Species` and on the Pin, the facts in the Orc's file. Every other family still keeps a hand-written list and writes its constants into a namespace dictionary. The plan is to make every family look like Species.

Methods Consul (Wizard): I agree, and I name the one law the Species family does *not* yet keep, so we do not copy a flaw. A Trait that differs only by a value is written as a Shape per Species: the Orc's `Darkvision` is a class over the common `Darkvision` with `RANGE = 120`. Julio's own rule (QST-0093.11, 2a) says the opposite: sources that differ only in data are **one Tag with inputs**. `Darkvision( char, range=120 )` is the shape that rule asks for, and `Unarmored_Defense( char, ability="CON", shield_allowed=True )` already proves it. But an input must travel with a call, and a Base in a Form is applied without one. So the rule has a consequence the Council must state plainly: **a Tag that takes inputs cannot be a Base; it is granted by the Species' Imprint.** Both are TOP; they answer different questions.

Contracts Consul (Warlock): Then write the rule down, because this is exactly where a contributor guesses. I propose two composition modes and one sentence deciding between them.

- **Base** (in the Form, applied with the Shape): when the relation is *is-a* and nothing varies. Heritage of Species, Specialization of Guild, Origin Feat of Feat, a Trait with no inputs. The Base's gates, Reports and Entries come along; the walk prints the Base first; re-applying is a no-op so two sources of one Base are one grant.
- **Grant** (applied by an Imprint, Decree 0009 point 4): when the relation is *gives* and something varies or is drawn. `Unarmored_Defense( char, ability=… )`, a Fighting Style chosen from a pool, a spell, a Weapon Mastery. The granted Tag is a leaf of its own, carries its inputs as Records, prints its own Entry, and the first source wins.

The sentence: **fixed, no inputs, no draw: a Base; otherwise: a grant from the Imprint.** It is dumb on purpose. A contributor can hold it in one hand. *(Withdrawn as a rule by Julio, 2026-10-05: "No hard rules if the design is elegant, simple, easy to expand and to read, and it works." The two modes stay as a description of the mechanisms, not as law.)*

Simplicity Consul (Monk): I accept both modes and object to one word in the question: *algebra* invites machinery. The Base algebra must stay **shallow**: one root per family and one Shape level below it (Species to Heritage, Guild to Specialization, Feat to its four kinds). The Guide's own table says it: pile up on Records with `stored`, do not chain Tags by inheritance to share a list. If a station proposes a third level of Bases, it is building a class tree with TOP's words. Measure the Form depth of every Tag at each station; the number should not grow.

Architecture Consul (Druid): Agreed, and that gives the plan its first concrete artefact. Twelve roots repeat the same gate today, `Character_Only`, in twelve files (Role, Training, Trait, Feat, Invocation, Species, Creature_Type, Guild, Ability_Leaning, Armor_Training, Weapon_Training, Weapon_Mastery). One Base, `Of_Character`, written once in the Character's own kit, carries it; every root is a Shape of it. *(Refused by Julio, 2026-10-05: "seems overly simplistic to just use one base for all, also having Tag as the universal base." The roots keep their own gates.)* That is the smallest possible Base algebra and it deletes eleven copies of one law. The home is `CharactersKit`, which already holds the Character, its Dice and the Role Tags: the Character's own kit is where the law "this Tag is worn by Characters" belongs. A new `Compass_of_Tags` module is the alternative if Julio wants the roots apart from the root object.

Contracts Consul (Warlock): Two more laws belong on the family root and nowhere else. **Where it prints:** a `SECTION` Report on the root (`Training.SECTION = Section.GUILD`, `Trait.SECTION = Section.SPECIES`), so an Entry needs no `section=` of its own; the walk fills it from the declaring Tag's Form the way it fills `level` from `MIN_LEVEL` today. **How many:** the one-of-a-kind rule. Julio ruled (QST-0093.11, 1) that it is one line on each Shape until TopKit can hold it on the Base. I keep that ruling and only propose a helper that writes the line, so the 36 copies have one author: `Only_One_Species = Only_One( Species )`. The real cure is upstream (STEP idea B, QST-0093.10 §3); the helper is the receipt we delete the day it lands.

Methods Consul (Wizard): The catalogues. The Species pattern is a Pin whose Records land as Reports on the Tag; the Field is the list. Every other family keeps a Python list and fills its class namespace with `Report_Of` because, after 0.2.0a2, a Report must be built by a function. A Pin solves both at once: `Declared_Lesson( Rage, guild=Barbarian, level=1 )` lands `Rage.GUILD`, `Rage.MIN_LEVEL` as Reports, with validation in the Pin's Records, and `Declared_Lesson[:]` is the catalogue. `Make_Training` stays, as Julio ruled, the row builder for a table file; it only stops writing its own dictionary and pins instead. Measured: that retires most of the 69 `Report_Of` sites and all 11 registries, family by family, with no change to any Character.

Safety Consul (Paladin): Everything above is structural, and structural means the fingerprint must not move. I ask for one rule across the whole course: a station either **changes nothing** (fingerprint 273 identical, sheet snapshot 343 identical) or **declares its change** before it lands, as station 3 did when pure readers moved the dice. The pin move first, alone, on its own branch, because every later station will be measured on the new kernel, and a diff that mixes a kernel change with a port cannot be read. The dry run says the pin changes nothing at the smoke; the fingerprint and the sheet snapshot will say the rest before the PR is opened.

Testing Consul (Rogue): And the course needs the gate it does not have yet: the **one-file fixture** QST-0091 asks for. A script declares a throwaway homebrew Species, a Lesson and a Background at run time, in one file each, and asserts that the picker lists them, the sweep builds them at three levels, and the seed replays. Until a family passes it, its port is not complete, whatever the sheet looks like. Also: two self-tests are red on `main` today for reasons that have nothing to do with the product (§4 of the evidence). Red that everyone learns to ignore is the one thing a gate must never be. They are fixed in the pin station or deleted.

Lorekeeper (Elf Sage), advisory: One word on words. The 3b ruling made lasting effects Flags and had to accept class names as the keyword, `MartialArts`, because 0.2.0a3 had no other spelling. 0.2.0a4 gives a Flag its words. The rulebook says *Martial Arts*, *Darkvision*, *Evasion*; a rule written as data should read the rulebook's words, and a Flag can carry the display name as its word and the class name beside it. Kinship already works that way in spirit (`"Dwarven" in char`); make it the law for every lasting effect, and stop any map from spelling a Tag's name.

Simplicity Consul (Monk): Last, the order. Six stations are structural and small; the family ports are large and already ruled (QST-0142 stations 3b to 11). I propose the structural stations go **first and fast**, each a day's work with an identical fingerprint, so every family port after them is written once in the final shape. The exception is 3b, which is in flight for the Monk and touches the same `TrainingKit` lines: let it finish its first Guild, then let the structural stations land, then the other twelve Guilds in the final shape.

Safety Consul (Paladin): One objection to that: PR #86 (the Sorcerer) and PR #98 (the Monk) both edit files the structural stations will touch, and #86 is already in conflict with `main`. A structural station that lands under an open port makes that port's merge a second port. The Council should ask Julio which of the open PRs land before the course starts, and hold the structural stations that touch their files until then. Everything else can go.

Architecture Consul (Druid): Accepted. The convergence is: copy Species, two modes and one sentence, a shallow algebra with one root Base and two Reports, Pins for every catalogue, words for every lasting effect, the pin move first and alone, the one-file fixture as each family's closing gate, and the open PRs ordered by Julio before the structural stations touch their files.

---

## ✅ Convergence check
- [x] Every called Consul has spoken.
- [x] Every objection has been answered or carried to Julio as a question below (the Paladin's on open PRs is question 9).
- [x] Concrete proposals with code sketches are on the table (below).

---

## 🕊️ Vox report

Vox: the Council agrees with the direction and gives it a shape small enough to hold.

### Common ground

1. **The Species family is the reference.** It is the one axis that already is self-contained: Form of Traits, a Pin for the generator metadata, the catalogue from the Pin's Field. The plan copies it to every family.
2. **Two composition modes, one sentence.** Fixed, no inputs, no draw: a Base. Otherwise: a grant from the Imprint.
3. **The Base algebra is shallow and small.** One root Base, `Of_Character`, carrying the gate twelve files repeat; two Reports on each family root, `SECTION` and the one-of-a-kind helper; one Shape level below a root.
4. **Catalogues are Pin Fields.** `Make_*` factories keep their tables and pin instead of writing namespaces; the 11 registries and most of the 69 `Report_Of` sites go.
5. **Lasting effects are Flags with words.** The word is the rulebook's name.
6. **The pin moves first, alone, and is measured.** 0.2.0a4 on Python 3.12 or later.
7. **Each family port closes with the one-file fixture.**

### The Base algebra, stated

**Layer 0, the operators (what TopKit gives).** The laws GenLegend builds on, with the GenLegend use of each. Nothing here is new machinery; it is the kernel, named.

| Operator | Spelling | Law | GenLegend use |
|---|---|---|---|
| apply | `Rage( char, **inputs )` | Bases first; inputs by name to gates, Records and Imprints; **re-applying an active Tag does nothing** | "the first source wins" for Unarmored Defense, Darkvision, a Feat granted twice |
| membership | `char in Rage`; `isinstance( char, Rage )` for history | monotonic until Rip | every `if char in Mage` that replaced a string |
| Form | `Form( Necromancer ) == ( Guild, Wizard, Necromancer )` | Base-first closure; a Shape is an Agent of every Base | the walk's order; a Specialization applies its Guild |
| Records pile up | `def spells( agent, stored ): return ( stored or [] ) + [ "Light" ]` | the author writes the merge: `+`, `max`, `\|` | spells, languages, hit points, speed, darkvision range: several Tags, one name |
| Reports inherit | `def hit_die( tag, inherited )` | one value per Tag, shared by the Field, refined by a Shape | hit die, saves, `SECTION`, source metadata |
| Actions extend | `@Action @Underlay def Describe( agent, underlay )` | the Underlay is captured at application | the Guild description stack (`extends` / `crunches`) |
| gates | `@Pre` relaxes backward; `@Post` strengthens forward; failures carry the check's name | atomic refusal before anything changes | `Accept` by named refusal; synergy (`agent in Wizard`); one of a kind |
| the writing | `@Imprint`, may apply further Tags | runs after commit; a failed Imprint leaves the Tag | choices made inside the offering Tag (Decree 0009, 4) |
| words | `@Flag( "Martial Arts" )`; `"Martial Arts" in char`; `Keyword( char, … )` | a word is a keyword, never membership; exact match | rules as data; lasting effects; Kinship; Roles |
| Pins | `@Pin class Declared_Lesson`; `Declared_Lesson( Rage, guild=… )`; `Declared_Lesson[:]` | a Pin's Records land as Reports on the Tag; its Field is a population of Tags | catalogues, sources, generator metadata |
| populations | `Guild[:]`, `~Guild`, `Wizard \| Fighter`, `Player - Sworn` | lazy, ordered, identity-keyed; a Tag in an operator seat is its sound population | sweeps, repair queues, catalogue intersections over Pins |
| teardown | `@Rip`, `Scope( char, Tag )` | Rip is the only exit; contributions and conditions are sticky | a Tag that writes host state undoes it here, nowhere else |

**Layer 1, the family roots (where the laws live once).** Each root declares, once, the five laws every Shape beneath it obeys:

| Law | How it is written on the root | Today | Target |
|---|---|---|---|
| who wears it | the root is a Shape of `Of_Character` | `Character_Only` in 12 files | one gate, one file |
| how many | `Only_One( Root )` on each exclusive Shape (ruling 1), or a budget gate on the root (`Guild_Budget`) | 36 hand-written lines, one budget gate | one helper writes the lines; upstream STEP idea B deletes them |
| where it prints | `@Report def SECTION( tag )` on the root | `section=` on every Entry | the walk reads the Form's nearest `SECTION` |
| what its choices draw from | a Dice Bag named by the Tag: `char.Dice_Bag( f"{tag.__name__}.{choice}" )` | purposes derived from `module.function` (196 sites, Decree 0005) | explicit, stable under file moves |
| which words it answers to | `@Flag( "Display Name" )` where the effect lasts | class names (3b) | the rulebook's words |

| Family root | Today | Shapes below it | Catalogue today | Catalogue target |
|---|---|---|---|---|
| `Role` (Flag) | `CharactersKit` | Player, NonPlayer | the two classes | unchanged |
| `Species` | `SpeciesKit/bases.py` | one per people; `Heritage` one level below | `Available[:]` (Pin) | unchanged: the reference |
| `Guild` (Flag) | `Grimoire_of_Guilds` | one per class via `Make_Guild`; Specializations one level below | `_GUILD_DECLARATIONS`, `GUILDS`, `_SPECIALIZATION_TAGS_BY_GUILD` | `Declared_Guild[:]`; the Specialization catalogue is the class tree under each Guild |
| `Training` | `TrainingKit` | one per lesson via `Make_Training` | `_TRAINING_DECLARATIONS`, `TRAININGS` | `Declared_Lesson[:]` |
| `Trait` | `FeaturesKit` | Species traits | none needed | unchanged |
| `Feat` | `FeaturesKit`, `FeatKit` | Origin, Fighting Style, General, Epic Boon | three lists in `FeatKit` | `Declared_Feat[:]` with a `KIND` Report |
| `Invocation` | `InvocationKit` | one per invocation | `_INVOCATION_DECLARATIONS` | `Declared_Invocation[:]` |
| `Background` | `BackgroundKit` | one per Background via `Make_Background` | `Background_Audience[:]` (Pin) | unchanged: already a Pin |
| `Weapon_Mastery` | `Map_of_Weapon_Masteries` | one per weapon | `_MASTERY_TAGS` (declared twice) | the Field of the root, `Weapon_Mastery[:]`-style read of its Shapes through a Pin |
| `Craft`, `Sworn` (Orders), `Maneuver`, `Metamagic` | their kits | one per option | four more lists | Pins |

**Layer 2, the self-contained Tag (the contract a file keeps).** Seven slots, in this order, so every Tag file reads the same way:

1. **identity**: the class name, `NAME` for display, `@Flag( words )` when the effect lasts;
2. **Bases**: its Form, one level deep;
3. **gates**: `@Pre` for synergy and for one of a kind; `@Post` for what it promises;
4. **facts**: `@Record` from inputs (per Character), `@Report` for constants (per Tag), or a Pin declaration beneath the class;
5. **choices**: one `@Imprint` that draws from the Tag's own Dice Bag and **applies the chosen Tags**;
6. **what it prints**: `ENTRIES` and `CHIPS`, Markdown and readers, nothing stored;
7. **what it wants**: its opinion tables for the Affinity machine (`KNOWS`, `WANTS`, `SHUNS`, QST-0142 question 5), and `@Rip` only when it wrote host state.

Nothing outside the file names the Tag: catalogues read a Pin Field, rules read a word, the sheet reads the walk.

### Code sketches

Illustrative, not final spelling. Tabs, the cascade, pins for comments.

```python
#-- AtlasActorLudi/CharactersKit.py : the Base algebra's root, beside Role.

class Of_Character( Tag ):
	"""Every GenLegend Tag is worn by a Character. The gate is written once."""

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


def Only_One(
		family,
		):
	"""
	The one-of-a-kind gate a Shape declares (QST-0093.11, ruling 1).

	Written by a helper so the 36 lines have one author; deleted the day
	TopKit guards a family on its Base (QST-0093.10, STEP idea B).
	"""
	@Pre
	def Only_One_Of(
			target,
			):
		return target not in family

	Only_One_Of.__name__ = f"Only_One_{family.__name__}"
		#-- The failure is caught by this name: Precondition.Only_One_Species.
	return Only_One_Of
```

```python
#-- AtlasActorLudi/SpeciesKit/bases.py : the family root declares its laws once.

class Species( Of_Character ):
	"""A Character's lineage and physical form."""

	@Report
	def SECTION(
			tag,
			):
		return Section.SPECIES
			#-- Every Species Entry prints here unless it says otherwise.
```

```python
#-- AtlasActorLudi/SpeciesKit/Orcs/__init__.py : one file, one people.
#-- Fixed traits are Bases; a trait with a value is granted from the Imprint.

@Flag( "Orc" )
class Orc(
		Species,
		Humanoid,
		Adrenaline_Rush,
		Relentless_Endurance,
		):
	"""A determined Humanoid shaped for endurance."""

	Only_One_Species = Only_One( Species )

	ENTRIES = (
			Entry(
					"Orc",
					Orc_Description,
					flavor="",
					level=0,
					),
			)
				#-- No section=: the walk reads Species.SECTION.

	@Imprint
	def Grant_Darkvision(
			target,
			):
		Darkvision(
				target,
				range=120,
				)
			#-- One Darkvision Tag for every people; the range is the input.


Player_Handbook_2024(
		Orc,
		weight=80,
		size_options=( "Medium", ),
		speed=30,
		)
	#-- The Pin: metadata as Reports on the Tag; the catalogue is Available[:].
```

```python
#-- AtlasLusoris/AtlasOfGuilds/Fighter_Kit/Core_Kit.py : a lesson that offers a choice.
#-- Decree 0009 point 4: the choice is made inside the Imprint, as a Tag.

Fighting_Style = Make_Training(
		name="Fighting Style",
		guild=Fighter,
		min_level=1,
		on_sheet=False,
		)


@Imprint
def Choose_A_Style(
		target,
		):
	pool = tuple(
			style
			for style in Declared_Fighting_Style[:]
			if target not in style
			)
		#-- Respect what the Character already holds (Decree 0009, 6).
	target.Accept(
			pool,
			dice=target.Dice_Bag( "Fighting_Style.choice" ),
			)
		#-- Accept applies the first candidate whose gate says yes.


Fighting_Style.Choose_A_Style = Choose_A_Style
	#-- Or declared inside Make_Training's namespace; the point is the home.
```

```python
#-- AtlasLusoris/TrainingKit.py : the catalogue is a Pin Field, not a list.

@Pin
class Declared_Lesson( Tag ):
	"""Every lesson the generator knows. Records land as Reports on the lesson."""

	@Pre
	def Lesson_Tag_Only(
			target,
			):
		return (
				isinstance( target, type )
				and issubclass( target, Training )
				and target is not Training
				)

	@Record
	def GUILD(
			target,
			*,
			guild,
			):
		return guild
			#-- The Guild Tag, never its name.

	@Record
	def MIN_LEVEL(
			target,
			*,
			min_level=1,
			) -> int:
		if min_level < 1:
			raise ValueError( "A lesson is gained at level 1 or later." )
		return min_level


def Lessons_Of(
		guild,
		):
	"""The catalogue, read from the Field: nothing is listed twice."""
	return tuple(
			lesson
			for lesson in Declared_Lesson[:]
			if lesson.GUILD is guild
			)
```

```python
#-- scripts/sweep_player.py, on 0.2.0a4 : the repair queue is one expression.

broken = tuple(
		~Player | ~Guild
		)
	#-- Every Character kept by the sweep whose promise broke, whichever Tag made it.
assert not broken, f"{len( broken )} defective Characters"
```

### The stations (the progressive port)

Each station is one branch and one PR (Decree 0008), gated by the fingerprint (wide grid, 273), the sheet snapshot (343), the wide sweep (1164), the replay, `verify_equipment` and the kit self-tests. A structural station reads **identical**; a port names every difference as intended. The order is a proposal; question 9 asks Julio to confirm it against the open PRs.

| # | Station | Questa | What lands | What it deletes | Gate reads |
|---|---|---|---|---|---|
| 0 | **The pin moves to 0.2.0a4** · *landed 2026-10-05* | QST-0144.1 | `topkit==0.2.0a4`; Python floor 3.12 in `requirements.txt`, the Makefile and the README; the "Role first" comment retired; the two stale self-tests repaired (the spell one exposed a missing one-school gate, now on each School and Level) | nothing else | identical: 273, 343, 1164, equipment, replay |
| 1 | **The family roots** *(revised 2026-10-05: no universal Base)* | QST-0144.2 | Each root keeps its explicit gate; `Report_Of` sites that wrap a plain value become plain class data, the few that wrap a Tag or a reader stay Reports; the `Only_One` helper only if ruling 5 says so | most of the 69 `Report_Of` sites | identical |
| 2 | **Where it prints** | QST-0144.3 | `SECTION` Report on each family root; the walk fills a missing `section` from the Form; `section=` removed where it equals the root's | per-Entry `section=` where redundant | identical (sheet 343) |
| 3 | **Words** · *landed 2026-10-05, declared difference* | QST-0144.4 | `@Flag( "Display Name" )` on 28 Species and Heritages; the Alignment leaves; every Guild, Specialization and Background by name; Gender pronouns as words; readers follow per family | the string comparisons counted in the evidence, one family at a time | **declared**: dormant word probes answer again (stories, legacy feats) |
| 4 | **Catalogues are Pin Fields** | QST-0144.5 | `Declared_Lesson`, `Declared_Feat`, `Declared_Invocation`, `Declared_Guild`, and the small ones (Masteries, Crafts, Orders, Maneuvers, Metamagic); `Make_*` pins instead of writing namespaces; `choices()` reads Fields | the 11 registries; most of the 69 `Report_Of` sites; `Map_of_Species`, `classes()`, `subclasses()` (QST-0091) | identical |
| 5 | **Choices inside the offering Tag** | QST-0144.6 | Fighting Style, Invocations, Metamagic, Maneuvers and spell picks move into the Imprint of the Tag that offers them; pools respect what the Character holds; Dice Bags named by the Tag | the `after=` hooks and outer `Apply_*` rites; derived Dice purposes | **declared diff**: draws move, as station 3 of QST-0142 did |
| 6 | **The one-file fixture** | QST-0144.7 | `scripts/verify_one_file.py`: a homebrew Species, Lesson and Background declared at run time, listed by the picker, built at levels 1, 5 and 20, replayed | nothing | new gate, green |
| 7+ | **The family ports, in the final shape** | QST-0142 3b to 11 · QST-0091.1 to .4 | Guild Kits for the twelve remaining Guilds; Species (Darkvision as one Tag with `range=`); Backgrounds; Feats; Proficiencies (QST-0047); Progression; Magic; Combatant; Inventarium; retire `char.features` | each family's legacy path, in the same PR | per station, as QST-0142 rules |
| ∞ | **Doctrine and upstream** · *closed 2026-10-05* | QST-0093.6 · QST-0093.10 | Julio deletes the Doctrine; the TopKit Guides, the Specification and the code are the authorities. STEP ideas A and B are **withdrawn**; nothing is owed upstream. GenLegend's generator remains the use case for STEP-SPEC-15 (Trials), Julio's own STEP | `Accept`'s retry loop, once Trials land | none |

**The Doctrine, resynced (proposed text for Julio's Canon edit, QST-0036)** *(superseded 2026-10-05: Julio deletes the Doctrine instead; the table stays as the record of what had drifted)*:

| Doctrine says today | 0.2.0a4 says | Note |
|---|---|---|
| `Expectation` | `@Pre` (`Precondition`), failures caught by name | relaxes backward |
| `Condition` | `@Post` (`Postcondition`); `@Requirement` for both | strengthens forward; a failed Post leaves the Tag, the Agent is defective |
| `Exclusion` | a `@Pre` on each Shape (ruling 1); STEP idea B upstream | no primitive exists |
| `Final` / `Sealed` | none | a Pin can mark a Tag (`Deprecated`), never seal it |
| Augmentation / Extension / Mutation | a new name; `@Underlay`; a replacement without it (diagnosed) | the three modes are real, under the kernel's words |
| `from TagKit import` | `from TopKit import` | the distribution is `topkit` |
| "AtlasTOP is our layer" | removed: Decree 0002 §6 | composition helpers live in the Kit that owns the axis |

### Risks the Council could not remove

- **The straddle.** Until station 7+ ends, `char.features` and the walk both feed the sheet. Every stalled week is "a paradigm half-adopted" (Dialog 0024). The structural stations are small on purpose so the straddle does not widen.
- **The new refusal in 0.2.0a4.** A condition named like a Record, an Action or a host attribute is refused at the door. The dry run did not meet one; the wide sweep on 0.2.0a4 decides, and the pin station fixes any by renaming the condition.
- **`Report_Of` is mostly unnecessary** (Julio's correction, Evidence §1): a plain value is already class data on the Tag. It stays only where a Tag or a reader must be held as a Report rather than become an Action on the Character.
- **Flag words on factory-made Tags.** `Flag( "Martial Arts" )( training_tag )` is the decorator applied by hand. Verified on 0.2.0a4 (Evidence §4); the risk left is only that a word collides with another family's word on purpose or by accident, which is the alias behaviour upstream accepted and ours to keep straight.
- **The Accept loop and Trials.** Until STEP-SPEC-15 lands, a refused late Tag is retried candidate by candidate, never undone as a draft. That is the behaviour today; the plan does not worsen it.

---

## 🗣️ Julio's answers, first round (2026-10-05, in chat)

Recorded as given; the body above is the proposal of record and is corrected inline where it was wrong. Items marked *pending* were explained again in plainer words and await his answer.

- **Ruling 1, "Base algebra": confirmed.** *"I meant the base and shapes, yeah. the family laws."* And on the Council's call for simplicity: *"being simple is a virtue. But we shouldn't force simplicity. We may need more tags and parallel and synergic compositions. Individual rules are simple, but they compose into a structure I call 'algebra' because it's something born like set algebra is. Your reading on algebra is right."* So the Monk's "one Shape level, measure the depth" is a smell test, not a law.
- **Ruling 2, the pin: yes.** *"last version in topkit and python. yes."* TopKit 0.2.0a4, Python floor 3.12.
- **Ruling 3, "fixed, no inputs, no draw: a Base; otherwise a grant": withdrawn as a rule.** *"I don't get it. Is that a ruling? a design pattern? It's unclear. … No hard rules if the design is elegant, simple, easy to expand and to read, and it works."* It stays in the Dialog only as a description of the two ways one Tag brings another along (in the class line, or applied from the Imprint), never as a rule a reviewer enforces.
- **Ruling 4, a universal root Base: no.** *"Do we need a universal base? these are very different features. I get some patterns are shared, but seems overly simplistic to just use one base for all, also having Tag as the universal base."* `Of_Character` is dropped from the plan. Each family root keeps its own explicit gate; whether the twelve gates call one shared predicate is *pending*.
- **Ruling 5, the `Only_One` helper: pending**, explained again in chat. Given ruling 4 and "explicit over magic", the Vox recommendation is now to keep the 36 explicit lines and drop the helper.
- **Ruling 6, words: yes, and widened.** *"lasting identities should become flags to use in spaces like the names and titles. Also gender, alignment... those can mark to set titles and backstory. 'Effects' like dizzy or poisoned should not be tags, but records. Identity is tags (ser/estar in the guide)."* So Species, Guild, Background, Gender and Alignment are Flags with words that the name, title and backstory maps may read; a passing condition is a Record, never a Tag.
- **Ruling 7, catalogues as Pins: approved.** *"I approve replacing the 11 registries. In general, if it improves the code, the readability, and the dnd-sheet-architecture, I'm happy to try. Work as hard as it needs."*
- **Ruling 8, choices inside the offering Tag and named Dice Bags: pending**, explained again in chat.
- **Ruling 9, the open PRs: port the design, rewrite the code.** *"mostly those pr's importance lays in the fantasy, not the specific code. Bring in the description, design principles, and all the lore and flavor stuff, but the code can be rewritten."*
- **Ruling 10, upstream: pending.** Julio wrote *"draft the two STEP"*, but his corrections above dissolve STEP ideas A and B. Which two he means is asked in chat.
- **Ruling 11, the Doctrine text: pending**, explained again in chat.
- **Ruling 12, scope: confirmed, with one condition.** *"as long as we have a functional gear and item system. It can be edited for improvements, if you have suggestions."*
- **A standing rule, restated:** *"Modules must be self testing in main."* Every module keeps a `__main__` self-test; the two stale ones are repaired in the pin station.
- **Darkvision, the worked example: a Tag, and a family.** *"Darkvision as a tag makes sense, as it is a status you may want to check with a flag, for example when deciding gear. It can also shape into FiendishVision for the 'full vision in the dark' of an invocation, or for the fiend's sight."* So `Darkvision` is a Flag Tag with its range as the input, and a Shape such as `Fiendish_Sight( Darkvision )` is a Darkvision too, so `"Darkvision" in char` stays true for it.

## 🗣️ Julio's answers, second round (2026-10-05, in chat)

- **The two mechanisms are the Guide's patterns, and the line between them is classification.** *"`class Orc( Species, Darkvision )` would make an Orc a shape of DarkVision. That would be wrong conceptually, so the Darkvision tag applies in imprint. Shapes implies classification, so a subtag is a subcategory contained... Darkvision is 'orthogonal', so to say, to species, but it is granted by orc, so it should be called inside the imprint."* So: a Base is a category the Shape belongs to (an Orc **is** a Humanoid, a Species); anything the Tag merely **gives** is applied from its Imprint (an Orc gives Darkvision). Two consequences for the family ports, named here so they are not forgotten: today `class Orc( Species, Humanoid, Adrenaline_Rush, Darkvision, Relentless_Endurance )` makes an Orc a Shape of its three Traits, and `Make_Background` makes a Background a Shape of its Origin Feat (`type( name, ( Background, origin_feat ), … )`). Both are grants, not classifications, and move into the Imprint when their family is ported (QST-0142 stations 4 and 5).
- **Ruling 4b: each root keeps its own gate.** *"it's just two lines to assert character and it's clearer."* No shared predicate.
- **Ruling 5: the 36 Shape gates stay hand-written.** *"explicit over magic. If I make a new class, I'd need to see the patterns."*
- **Ruling 8: every pick of a Character goes through the Character's own RNG, the Dice Bag.** *"All choices from the character should be made by the RNG they carry, nicknamed the dice bag. Everything else is in transit to being refactored or plain wrong. Personal random statuses allows for parallel creation without conflicts. Also, it provides consistency."* So the story engine's `random.choice` and the legacy feat builders' `random.sample` are wrong by this ruling and are refactored to the Character's Dice when their families are ported. Whether a Dice Bag's *purpose name* may change (which moves the draws once) is asked again in chat, since his "no" may have read the proposal as a second RNG.
- **Ruling 10: no STEP is owed.** *"if you think topkit should have a nice step, you can suggest it as a step."* The two STEP ideas were withdrawn by his corrections; nothing is missing upstream today except Trials, which is his own STEP-SPEC-15.
- **Ruling 11: the Doctrine is deleted.** *"I'm deleting the Doctrine. Is outdated. Reference the guide."* and *"just reference the guides as the authorities on topkit, and the code itself."* `Curia/Canon/TagKit-Doctrine.md` is retired by Julio; the authorities on TOP are the TopKit Guide, the Fields and Contracts Guides, the Specification, and GenLegend's own code. Thirty-four documents in `Curia/` and `Documenta/` still cite the Doctrine; they are history and are not rewritten. The "Doctrine resync" station of this Dialog (and QST-0093.6, QST-0036) is closed by the deletion.

## 🔎 Found while landing station 3 (2026-10-05): the words wake dormant rules

Making the identities Flags was planned as a change that prints nothing new. It printed a great deal, because the legacy code already asked Characters for words. The story engine (`AtlasEpica/Charts_of_The_Monomyth.If`) tests every table row with `word in hero`; `AtlasEpica/Map_of_Stories` carries 1347 rows conditioned on a Species or Guild word; the legacy feat and boon builders ask `"Fighter" in char`. All of it was written for TagKit 0.1, which answered any Tag by name, and all of it has been silently False since the 0.2 move. The words bring the authored behaviour back: on the wide grid 294 of 343 sheets change their story paragraph and 5 of 273 fingerprints move, all one Fighter line's legacy feat picks; equipment, replay and the 1164-cell sweep are unchanged. QST-0144.4 records the mechanism and the counts as a **declared difference, accepted by Julio** the same day (*"it's good that the stories generated are more specific and rich"*; and *"Gender should flag 'He'/'She'/'They'"*). The lesson for the Doctrine: a probe that nothing answers is not a refusal, it is silence; a word must be declared before it is asked.

## 🗣️ Julio's answers, third round (2026-10-05, in chat)

- **Ruling 8, second half: a Dice Bag is named by the Tag that offers the choice.** *"Apply the suggested Dice Bag. more consistent."* So a choice draws from `char.Dice_Bag( f"{Tag.__name__}.{choice}" )`, the row of Layer 1 above, and the purposes written today by hand (`identity.species.Elf.keen_senses`, `training.monk.open_hand.bullet`, `wizard.spellbook`) or derived from the calling `module.function` (the migration Decree 0005 left open) are renamed as each choice moves into its Tag. A renamed purpose moves its draws once; that is station 5's declared difference, accepted in advance by this ruling. Decree 0005's own rule stands: a purpose is a stable string that no file move or rename can change.

- **Station 5 measured the same night.** Four readers, a merge and two critics inventoried every live choice site on the branch after station 4: 104 of them, 49 through a named Dice Bag, 14 through a purpose derived from the caller's stack frame (a bare `Accept` always derives the same purpose, so all bare Accepts of a Character share one stream), 38 through the random module or `app.random` under `Isolated_Legacy_RNG` (one shared stream in draw order, the coupling that moved station 3's fingerprints), 2 through a private `random.Random`. QST-0144.6 carries the inventory and a four-commit plan; five questions are asked in chat before it runs.

## 🗣️ Julio's answers, fourth round (2026-10-06, in chat)

- **Station 5 in full.** *"The legacy should also be fix, yeah."* *"Sounds right"* (every Tag-owned purpose renamed at once). *"yes"* (Species Traits and Background Origin Feats are grants from the Imprint). *"Fix the Dice Bag by magic, bypass, or private streams, and ask clarifications if anything is strange."* So the frame-derived purposes, the shared-stream draws and the private streams all go in one declared difference, and the inventory's eight strange findings (QST-0144.6) are handled as proposed there.
- **Where a Tag-owned choice lives.** *"Tag-owned choices should be at tag level or helper functions inside the tag file."* A choice is made on the Tag (Imprint or Action) or by a helper in the file that declares the Tag; never by an outer rite in another file. That is the rule of station 5's second pass, the move.

## ⚖️ Rulings needed from Julio

Numbered so an answer can say "1: yes, 2: no". *(Three rounds answered above; station 3's difference accepted; the Dice Bag names ruled. Open: whether the Species and Background ports move their Traits and Origin Feats from Bases into Imprints as the second-round reading implies.)*

1. **"Base algebra."** Is the reading above right: the kernel's operators plus one root Base per family carrying the family's laws, kept shallow? Or did you mean something narrower (the Field algebra of 0.2.0a4) or something new (a module named Base)?
2. **The pin.** Move to `topkit==0.2.0a4` now, alone, on its own branch, with the Python floor at 3.12? The dry run says it changes nothing at the smoke and the replay; the fingerprint and sheet snapshot results are recorded in QST-0144.1.
3. **Two modes, one sentence.** "Fixed, no inputs, no draw: a Base. Otherwise: a grant from the Imprint." Do you ratify it? Its first consequence is Darkvision: one Tag, `Darkvision( char, range=120 )`, granted by each Species' Imprint, instead of a Shape per people.
4. **The home of the root Base.** `Of_Character` and `Only_One` in `CharactersKit` (no new module, beside Role), or a new `AtlasActorLudi/Compass_of_Tags.py`?
5. **`Only_One`.** Keep ruling 1 (a line per Shape) but let one helper write the line, or leave the 36 lines as they are until upstream?
6. **Words.** The word of a lasting effect is its display name (`"Martial Arts" in char`), the class name answering too because the name always flags. Agree? And should Species, Guild and Background names be words as well, so that no map ever spells `"Paladin"` again?
7. **Catalogues as Pins.** Approve replacing the 11 registries with Pin declarations, Species-style, `Make_*` keeping its table files and pinning instead of writing a namespace?
8. **Choices inside the offering Tag, and Dice Bags named by the Tag.** This moves draws and changes every affected seed once, as station 3 of QST-0142 did. Accept the declared diff, and when: before or after the family ports?
9. **Order against the open PRs.** Which of #98 (Monk Kit, 3b), #86 (Sorcerer, in conflict), #96 (Druid prose), #99 (Vercel) land before station 1 touches `TrainingKit`, `Grimoire_of_Guilds` and `FeaturesKit`? Stations 0 and 6 touch none of their files and can go first either way.
10. **Upstream.** Shall the agent draft the two STEP ideas (A: a Report's value form; B: a Base guards its family) as issues for you to file, and a note endorsing STEP-SPEC-15 (Trials) with GenLegend's generator as the use case? This session could read the TopKit repository but had no write access to it.
11. **The Doctrine.** Do you want the resync table above turned into the full `TagKit-Doctrine.md` text for your ratification (Canon is yours to edit), or does it ride QST-0093.6 as planned?
12. **Scope.** The NonPlayer path stays parked (Decree 0004) and the Combatant and Inventarium stations keep their QST-0142 rulings unchanged. Confirm.

→ Awaiting Julio's decision. To be recorded as Decree 0010 if ratified, or sent back for more deliberation.
