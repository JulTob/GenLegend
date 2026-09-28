# QST-0142 — One Entry, one Chip: the sheet prints the build

- **Type:** architecture · port (Decree 0009) · campaign
- **Priority:** 🔴 high *(Julio: "We better start then. It's a lot of work to do but it should be worth it.")*
- **Status:** Working — station 1 (the foundation) in progress
- **Owner:** unclaimed
- **Route to:** Architecture (Druid) · Presentation (Bard) · Contracts (Warlock) · Simplicity (Monk)
- **Parent:** QST-0093 · **Related:** Decree 0009 · QST-0093.14 · QST-0141 (#71) · QST-0093.7

---

## 🔍 Diagnosis (what & where)

The sheet has two columns (Julio, 2026-09-24):

- **the big column holds Entries**: a title, a flavor line, and the rules text;
- **the small column holds Chips**: a symbol, a label, a value.

That concept was settled months ago, before the wipe, and got lost. Today the codebase has **several shapes for each idea**:

- **Entries:**
  - `FeaturesKit.Feature` (title, description, source, level, chips, narrative);
  - `AtlasVenustas.Entry` (title, definition, description, speech, symbol, kind). It is a string of HTML, and its `.md()` drops the `description` field;
  - a duplicate `Entry` in `AtlasVenustas/VenustasKit.py`.
- **Chips:** `(label, value)`, `(label, value, symbol)` and `Chip( symbol, label, value )` (QST-0141).
- **Text:** about 1,240 lines of feature text carry HTML tags, so nothing can print cleanly as Markdown or JSON.

Scale, for the record: about 350 `Feature(...)`, 354 `Entry(...)`, 284 `chips=` and 870 `description=` sites across about 60 modules.

## ✅ Julio's rulings (2026-09-24)

1. **One Entry concept:** `title / flavor / rules`. Everything else is metadata that does not print (section, level).
2. **One Chip concept:** symbol, label, value.
3. **Text is Markdown, with no HTML tags.** Each medium is a printer. The call reads `f"{entry:html}"`, `f"{entry:md}"` or `f"{entry:json}"`.
4. **Several short Entries**, not one long one. A Background becomes *Background* and *Hook*.
5. **The sheet prints from the build** (`Find_Build`).
6. **Section order:** Species, Background, Guild, Feats, Proficiencies, Equipment, Backstory, Magic, Others.
7. **Unify everything, and do not stop halfway.** Classes, Progression and Features are refactored into TopKit on the way.
8. **One branch and one PR per family.** Each family is ported completely and deletes the old path it replaces. The design stays "black box invariant": a family's outside behaviour does not change unless a rule was wrong.
9. **Draconic Resilience:** its own Tag, 2024 formula (landed in PR #92).
10. **Player sheet first;** NPCs when we get there.

## 🗣️ Julio's answers, second round (2026-09-24)

- **Markdown title of an Entry is `###`.** The sheet's name is `#` and its sections are `##`, so an Entry sits one step below its section.
- **Inventarium layout: A, the ledger.** It fits the project's style. Rings are capped at 10 **inside the generator only**, never printed as "1/10". Attunement stays a separate tick, 3 at most.
- **Focus by tool proficiency: approved.** For casters who also fight, the focus goes on equipment they already carry, so it never costs a fighting-style slot: a holy symbol on the Shield, runes carved in the sword, or a ring that needs no attunement.
- **Weapon properties are Bases** of the weapon kind: `Two_Handed`, `Heavy`, `Martial`, `Weapon`, and so on.
- **Proposed by Julio, under evaluation:** fighting archetypes (Blade and Board, Hard Hitter, Infiltrator, Tank, Magician, Spellsword…). An archetype is drawn at random among the ones the build can use, and it decides the hands and the ready weapon. The Fighting Style and feats must agree with it: Great Weapon Fighting → a great weapon; Dueling or Defense → a Shield; Pact of the Blade → a one-handed martial weapon without Thrown. Styles and feats that conflict exclude each other. The specific weapon stays random within the archetype (the "constellation effect").
- **Open:** how the sheet shows where the AC comes from, so a new player does not add a Ring of Protection twice.

## 🧭 The stations (one PR each, in order)

| # | Family | What it does | Deletes |
|---|---|---|---|
| 1 | **Foundation** | `Entry( title, rules, flavor, *, section, level )` and `Chip( symbol, label, value )` as plain data, with Markdown text and readers (functions of the Character). `__format__` prints `html`, `md`, `json`. `Section` in the approved order. `Find_Build` reads `ENTRIES` and `CHIPS`. The **sheet snapshot gate**: every Character on the wide grid printed to Markdown, saved and compared. | The HTML-string `Entry` and `Chip`, and the duplicate in `VenustasKit`. Every existing `Entry(...)` site moves to the new class in this station. |
| 2 | **Chips, one shape** ✅ | Every `(label, value[, symbol])` tuple becomes a `Chip`. | `_normalize_chip_pairs`' duck-typing, `chip_label` in `verify_equipment` (closes QST-0141 part B). |
| 3 | **Guild Training** | Training Tags declare `ENTRIES` and `CHIPS` in Markdown. The Guild section prints from the build. | Training's `grant(...)` into `char.features`. |
| 4 | **Species** | The same, for Species and Heritage. | Species `Trait` features. |
| 5 | **Background** | *Background* and *Hook* as two Entries; Origin Feats. | Background features. |
| 6 | **Feats** | General Feats, Fighting Styles, Epic Boons, Invocations. | Their `Feature` objects. |
| 7 | **Proficiencies** | Skills, tools, armour and weapon lines read from Tags. | The `Unarmed_*` skill bridge (QST-0093.12 question 4). |
| 8 | **Progression** | Level-ups, Ability Score Improvements, hit points as Tags. | `Map_of_Classes`, `Codex_of_Progression`, `Grimoire_of_Features` (with QST-0093.7). |
| 9 | **Magic** | Spellcasting, focus, spells section. | The old spell `Entry` use. |
| 9b | **Combatant** | The fighting archetypes (Blade-and-Board, Hard-Hitter, Infiltrator, Tank, Magician, Spellsword…). Chosen after the Guild; Styles, Feats, Pact and Masteries follow it; the weapon is drawn at random from the overlap of every filter. The gates + weights matrix. | The per-Guild hand-written weapon picks. |
| 10 | **Inventarium** | `char.inventarium`, `Map_of_Wearing`, grips (hands in pairs), attunement 3, rings 10, focus slot, the chosen print layout. | `char.belongings` and `Loadout`'s hand-written slots. |
| 11 | **Retire `char.features`** | Nothing left writes to it. | `FeaturesKit.Feature`, `grant`. |
| later | **NPC sheet** | NPC Entries already use the new class after station 1; their sheet is ported last. | — |

**Gates for every station:**
- fingerprint (wide grid, 273 Characters);
- the sheet snapshot (new in station 1);
- wide sweep 1164/1164;
- replay;
- `verify_equipment`;
- kit self-tests.

Every difference in the fingerprint or the snapshot must be named in the PR as intended.

## ❓ Questions to answer

Open as of 2026-09-24:

1. **Hands policy** (station 10): 1 Shield first, 2 Weapon first, or 3 By build? See the mock-up page "The Inventarium".
2. **Inventarium layout** (station 10): A ledger, B paper doll, C armed / worn / packed, or a mix?
3. **Focus by tool proficiency** (station 10): keep the proposed table as the rule?
4. **Spells' metadata line** (station 1 moves it, station 9 designs it). Today a spell's `Entry` carries its school and casting time in the `description` field. Station 1 moves that line to `flavor` so the sheet does not change. Should station 9 give spells their own card shape?
5. **The choice algebra — RULED (Julio, 2026-09-28): the Affinity machine.** One mechanism for the Combatant pick, the weapon pick, and later picks of this kind. Julio chose Bayesian updating over hard filters, and one machine over bespoke code per draw.
   - **Every option carries an affinity: a number from 0 to 1** — how strongly this build believes in the option.
   - **A pure 0 is a hard fact and it is absorbing** (Julio: "a pure 0 is also a valid entry, for the ones you cannot learn at all"). No proficiency, gated out: affinity 0, forever. No witness and no threshold-lowering revives it. A zero prior stays zero whatever the evidence.
   - **Everything learnable starts at 0.5**, the no-opinion prior.
   - **Each feature is a witness, not a manager.** Its module declares only its own opinion table, option → opinion in [0,1]; silence is 0.5. This is the modularity Julio's matrices asked for: no god object, the combiner never knows which features exist.
   - **Opinions combine by Bayes' rule**: multiply the odds, `odds(a) = a / (1 − a)`, then back to an affinity. In log-odds space this is plain addition — "add or subtract" and "a matrix per feature" were the same answer. A pure 1 is as absorbing as a pure 0, so 1 is reserved for grants; enthusiasm caps near 0.9.
   - **The draw**: keep options at affinity ≥ 0.5; none pass → halve the threshold (0.25, 0.125, …) until a non-zero option passes. All zero is a loud, named error. Among the passers the **Character's own dice** draw, weighted by affinity (default; Julio may rule uniform-above-threshold instead).
   - **When**: at creation, in **tagging order** (Julio, 2026-09-28) — a choice is drawn when the Tag that forces it applies; the weapon draw happens at outfitting, after every witness Tag is in place. Printing never draws (Decree 0009, point 7).
   - **Refined the same day — two verbs, two operations (Julio):** *"Knowing would be additions to the weapon vector ((a+b)/2 or a max operation) and wanting a bayesian update… the fact 1 is absorbing can also be used in favor… it could keep a weapon inside the choices or crunch other rules (pact weapons not needing proficiency?)."* Settled form:
     - **Knowing = `max`** (chosen over the average: averaging can forget — learning a weapon a second time, worse, must not lower it; max is monotone and idempotent, the same law as re-applying an active Tag). Knowing **can lift a 0**: Pact of the Blade simply *knows* the blade into the pool, no proficiency needed — the rule is crunched by the operation, not by an exception.
     - **Wanting = Bayes**, applied after knowing. Here 0 stays 0 and 1 stays 1 — and a 1 works *in favor*: affinities are independent beliefs, not a shared distribution, so a 1 pins its option into the pool without silencing the others; the draw still chooses among every passer.
     - Both folds are commutative, so **the affinities do not depend on the order the Tags were applied**; nothing is stored, the vector is computed at draw time (pure). Tagging order decides only which dice are consumed when.
     - **The math is a hidden layer** (Julio): Tags speak verbs — `Knows`, `Wants`, `Shuns`, `Grants` — with named strengths behind them; only the kit does odds arithmetic. A feature author writes a sentence, never a formula.
6. **Spells — RULED (Julio, 2026-09-28): one global known-set per Character.** The same vocabulary as the weapons: a feature **allows** spells (affinity above 0 in the pool) or **grants** them (fixed, outside the draw). Grants resolve first; every pick draws from allowed minus already known, so a granted spell never wastes a pick — whichever feature is picking (a domain grant removes the spell from a later feat's picks too). Never a duplicate on the sheet.
7. **Station 3's dice — RULED (Julio, 2026-09-28): accept the changed draws.** Making the readers pure moves dice rolls from print time to creation time, and 69 of the 273 grid Characters read differently (18 Paladins and 18 Rangers draw another style or ability, 21 Wizards other spells, 6 Draconic Sorcerers show the Scaled AC chip they always deserved, 6 Fighters shift a mastery draw) — all equally legal. Julio accepted the changes; each sheet is named in the station's PR. No compatibility shim.

## 🛠️ Station 1, the foundation (branch `julio_cl/qst-0142-foundation`)

- **`AtlasVenustas/Compass_of_Features.py`**: `Section` (the approved order); `Entry( title, rules, flavor, *, section, level )`; `Chip( symbol, label, value, *, kind )`.
  - Both are frozen dataclasses whose text may be a reader.
  - `.Read( character )` returns the same shape with plain text.
  - Printing an unread one raises `Unread_Text`.
- **`AtlasVenustas/Charts_of_Printing.py`**: `f"{x:html}"`, `f"{x:md}"`, `f"{x:json}"`, `f"{x:plain}"`.
  - HTML is made from Markdown by `markdown-it-py`, which Shiny already installs.
  - The Entry HTML keeps the markup the sheet always used.
- **The old HTML-string `Entry` and `Chip` are gone** from `Scriba`, and the unused `VenustasKit.py` copy is deleted. Every site moved:
  - `definition=` → `rules=`;
  - `description=` → `flavor=`;
  - a hook's `.definition` → `.rules`;
  - `extra_class="magic-chip"` → `kind="magic"`;
  - `__str__` methods that returned an `Entry` now return `f"{entry:html}"`.
- **`Find_Build`** reads `ENTRIES` as well as `CHIPS`. An Entry with no level takes its Tag's `MIN_LEVEL`.
- **Gates.** `scripts/verify_sheet_text.py` is the new sheet snapshot: 273 Players and 70 light NonPlayers, compared as visible text. `scripts/verify_equipment.py` reads a chip's label properly.

**The NonPlayer maps are a text builder until their station.** `AtlasPugna` and the NonPlayer magic in `Map_of_Magic` never kept Entries: they glue their text with `+` and `join`, nest one entry inside another's text, and call string methods on it. They now call `AtlasScriptum.Map_of_Formats.Entry_Text( title, rules, flavor )`, which returns exactly the markup the old string-shaped `Entry` made. It is a text builder, labelled as such, and it goes when the NonPlayer station ports those maps.
- Full NonPlayers cannot be generated today (QST-0134), so a probe called each map directly on light NonPlayers (30 each, stand-in attributes, same seeds) on the base and on this branch.
- Senses, Movement, Resistances, Condition Immunities, Legendary Actions, Martial Abilities, Attack and Special Attack produce byte-identical text.
- NonPlayer spells differ only in whitespace, and in the order they come out of a Python `set` (which depends on the text's hash): the same spells, in another order.

**What changed on the sheet (declared).** 17 of 343 sheets read differently, all for one old bug.
- A spell's `.string` put its text after a newline and a tab. The sheet's Markdown renderer read that as a code block.
- So the spell printed in a monospace box with its `<b>` and `<br>` tags showing, and swallowed the next spell's heading.
- Now each spell's text reads as prose. Every other sheet is identical.

**Found on the way (not this station's to fix):**
- `verify_equipment`'s 195 known failures were 100 fake "duplicate chip `<`" findings, from reading an HTML string's first character, plus **95 real ones hidden among them**: Monks, Bards, Rangers, Druids and Clerics "wield untrained" implements (Oath Mace, Warden's Staff, Hexbolt Wand, Beguiler's Rapier). The same 95 fail on the base. Station 10 (Inventarium) owns them.
- **NonPlayer text is not reproducible.** Some NonPlayer text draws from Python's shared generator and from `app.random`'s private one, not from the Character's own Dice. The gate pins both.

## 🛠️ Station 2, Chips in one shape (branch `julio_cl/qst-0142-chips`)

- **118 chip tuples** in 23 modules (Training maps, Species, Origin Feats, Fighting Styles, OrderKit, the species spellcasting chips) became `Chip( symbol, label, value )`. They were rewritten through Python's syntax tree, not by text search.
- **Symbols move to the source.** The symbols the sheet used to add at print time (`_FEATURE_CHIP_EMOJI`, with `✦` for the rest) are now written in each declaration, and the table is deleted. The two Bard chips that declared an empty symbol now say `✦`.
- **One reader.** `FeaturesKit` stores and projects a Chip and refuses anything else by name (`Not_A_Chip`). The two copies of the sheet's chip normalizer become one, `shared.Feature_Chip_Triples`, which reads a Chip, its dictionary form after `to_dict`, and, until the NonPlayer station, the NonPlayer `Chip_Grant`.
- **The checks read `chip.label`:** `GearKit` and `verify_equipment` read the label directly, with no tuple branch.
- **Result:** all 343 sheets read the same, and the fingerprint is identical. Closes QST-0141 part B and QST-0081.4.

## 🎯 Desired outcome

One Entry, one Chip, one text format. Every Tag declares what it prints. The sheet, the Markdown test print and the JSON API all come from `Find_Build`. `char.features` and the legacy class engines are gone.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** —
- **Practice/preference to remember:** —
