# ❓ Questions for the Agora

> The open queue. Anyone — Julio, a Consul, or an Agent — may add a question. Each becomes a Dialog in `Dialogs/` and, once settled, a Decree in `Decrees/`.

## How to add a question

Append a row. Keep it to one line; detail goes in the Dialog file.

| # | Question | Raised by | Consuls called | Dialog | Status |
|---|----------|-----------|----------------|--------|--------|

---

## Open

| # | Question | Raised by | Consuls called | Dialog | Status |
|---|----------|-----------|----------------|--------|--------|
| Q-0001 | Character display: keep dynamic boxes for Skills/Scores, or move to a 5e.tools-style Markdown "character sheet" styled by CSS? | Julio | Architecture (Druid), Understanding (Bard), Readability (Barbarian), Flow (Sorcerer); Design-Team + Lorekeeper advisory | `Dialogs/0001-character-sheet-vs-boxes.md` | 🟡 needs framing |
| Q-0002 | Resolve `AtlasLusoris` vs `AtlasAlusoris` near-collision — rename, alias, or leave documented? | Curia (eval) | Architecture (Druid), Readability (Barbarian) | — | 🕓 queued |
| Q-0003 | ~~TagKit paradigm: settle the decorator style / open questions~~ | Curia (eval) | — | — | 🔵 closed — invalid premise: TagKit is settled & upstream (see QST-0006) |
| Q-0004 | Flask → Shiny: confirm full removal of Flask and the retirement of `app/routes.py` and templates. | Curia (eval) | Architecture (Druid), Ecosystem (Ranger), Workshop (Artificer), Flow (Sorcerer) | — | 🕓 queued |
| Q-0005 | How should we run the QST-0007 file-by-file diagnostic sweep — order, method, and how findings branch into questae/sidequests? | Julio | Full council (Bard, Druid, Artificer, Ranger, Monk, Rogue, Sorcerer, Wizard, Lorekeeper) | `Dialogs/0002-how-to-run-the-diagnostic-sweep.md` | 🔵 settled → Decree 0001 |
| Q-0006 | What is the minimal Character the generator builds, and how are the RNG & core mechanisms instantiated so PC/NPC diverge by tags? | Julio | Bard, Lorekeeper, Druid, Wizard, Sorcerer, Paladin, Warlock, Monk, Rogue | `Dialogs/0003-minimal-character-and-rng.md` | 🔵 settled → Decree 0002 |
| Q-0007 | The Minions: are they sound, and where should they go — kept, evolved into a Log System, and/or deployment error reporting? | Julio | Full council | `Dialogs/0004-evaluate-the-minions.md` | 🔵 settled → Decree 0003 |
| Q-0008 | Character sheet toolbar (`.character-reforge`): how should layout be owned — inline CSS tweaks, Scroll_of_Styles only, or a Venustas Kit with a single contract? | Julio (via Agent) | Architecture (Druid), Workshop (Artificer), Simplicity (Monk), Flow (Sorcerer), Readability (Barbarian) | `Dialogs/0005-character-reforge-toolbar-layout.md` | 🟡 open |
| Q-0009 | Characteristics grid (`stat-flow`): uniform chips, thematic order, Level box — flex vs grid, label contract? | Julio (via Agent) | Readability (Barbarian), Architecture (Druid), Simplicity (Monk), Lorekeeper | `Dialogs/0006-characteristics-grid-layout.md` | 🟢 converged — awaiting Julio |
| Q-0010 | Title map: how should generated titles become thematic, deterministic narrative identity without leaking lusor internals? | Julio (via Agent) | Understanding (Bard), Architecture (Druid), Contracts (Warlock), Methods (Wizard), Simplicity (Monk), Testing (Rogue), Lorekeeper | `Dialogs/0007-title-map-as-narrative-identity.md` | 🟡 open |
| Q-0010 | Migration order & safety rail for the Character-root refactor (QST-0016.1–.6, QST-0027): what sequence, and what proves each step unbroken? | Julio | Safety (Paladin), Architecture (Druid), Simplicity (Monk), Contracts (Cleric), Methods (Wizard) | `Dialogs/0007-migration-order-and-safety.md` | 🟡 open |
| Q-0011 | Which actualized former-Archetype Backgrounds should be renamed, shared with Players, or mechanically adjusted? | Julio | Julio's product review first | `Dialogs/0008-background-metatop-content-review.md` | 🟡 implemented proposal awaiting review |
| Q-0012 | Which later official Background sources and setting-specific options should the default generators expose? | Julio | Julio's product review first | `Dialogs/0009-official-background-catalogue-review.md` | 🟡 implemented catalogue awaiting review |
| Q-0013 | Should ability scores follow interests the build declares for its **goal level** (counting what the finished character actually uses) rather than a class's static preference order? | Julio | Architecture (Druid), Methods (Wizard), Contracts (Warlock), Flow (Sorcerer), Testing (Rogue), Simplicity (Monk), Lorekeeper | `Dialogs/0010-build-interests-and-goal-level.md` | 🟢 converged — awaiting Julio |
| Q-0013 | Should ability scores follow interests the build declares for its **goal level** (counting what the finished character actually uses) rather than a class's static preference order? | Julio | Architecture (Druid), Methods (Wizard), Contracts (Warlock), Flow (Sorcerer), Testing (Rogue), Simplicity (Monk), Lorekeeper | `Dialogs/0010-build-interests-and-goal-level.md` | 🟢 converged — awaiting Julio |
| Q-0034 | Tools: how does a tool get one authored identity, so the sheet, menus, training ledger and its bridge cannot disagree? (QST-0116) | Agent (Claude), from Julio's review 2026-09-13 | Architecture (Druid), Contracts (Warlock), Repair (Cleric), Simplicity (Monk), Testing (Rogue); Lorekeeper advisory | `Dialogs/0025-one-identity-for-a-tool.md` | 🔵 decided by Julio 2026-09-14 (QST-0116 Solved) |
| Q-0035 | The shared core: should the Character hold one grant ledger (Entries and Chips) beside the Dice, with sections built by layouts in the visual package? Is "tags = flags + chips + entries" the algebra? (QST-0020, QST-0016) | Julio, in chat 2026-09-23 | Agent panel stood in (six readers, three designs, three judges); Agora on request | `Dialogs/0026-the-shared-core-one-ledger-many-layouts.md` | 🟢 converged in panel — awaiting Julio (R1–R6) |

---

## Field notes for open threads

- **For Dialog 0010 / Q-0013 (build interests):** Julio raises **True Strike** as the answer to the
  MAD-caster problem, and it is the sharpest example yet of a *countable interest*. The 2024 cantrip
  makes one weapon attack using the spellcasting ability for **both attack and damage**, so a
  character holding it needs no Strength or Dexterity to fight. Verified against this codebase's own
  lists: True Strike is on **Warlock, Wizard, Sorcerer, Bard, Artificer, Eldritch Knight and Arcane
  Trickster** — and **not** on Paladin, which has no cantrips at all in 2024. So it is decisive for
  the pact variants (an Occultist holding it attacks with Intelligence) and for the gish subclasses,
  while a Charisma-forward Paladin still needs Magic Initiate or a background cantrip to reach it.
  This turns "is this half-caster contested?" from a tuning constant into evidence the build already
  carries, and strengthens the case for option B over a chosen softmax temperature.
  *(Agent, session 2026-08-18)*

- **For Dialog 0010 / Q-0013 (build interests):** Julio raises **True Strike** as the answer to the
  MAD-caster problem, and it is the sharpest example yet of a *countable interest*. The 2024 cantrip
  makes one weapon attack using the spellcasting ability for **both attack and damage**, so a
  character holding it needs no Strength or Dexterity to fight. Verified against this codebase's own
  lists: True Strike is on **Warlock, Wizard, Sorcerer, Bard, Artificer, Eldritch Knight and Arcane
  Trickster** — and **not** on Paladin, which has no cantrips at all in 2024. So it is decisive for
  the pact variants (an Occultist holding it attacks with Intelligence) and for the gish subclasses,
  while a Charisma-forward Paladin still needs Magic Initiate or a background cantrip to reach it.
  This turns "is this half-caster contested?" from a tuning constant into evidence the build already
  carries, and strengthens the case for option B over a chosen softmax temperature.
  *(Agent, session 2026-08-18)*

- **For Dialog 0003 / QST-0016 (RNG):** verified 2026-07-09 — `NPC(seed=7)` twice in one process yields *different* names. Mixed RNG sources (`app.random` in the Grimoires, stdlib `random` in `Map_of_Names`) defeat seed reproducibility today. Share-links and list-reopening now avoid regeneration because of this; the minimal-Character design should make the seed the single spine. *(Agent, session 2026-07-09)*

## Settled → see `Decrees/`

*(none yet)*
