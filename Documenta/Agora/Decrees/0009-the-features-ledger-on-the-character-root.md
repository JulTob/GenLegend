# Decree 0009 — The `features` ledger joins the Character root

- **Ratified by:** Julio, in chat, 2026-09-24
- **Source:** Dialog 0026 (Q-0035), ruling R1
- **Amends:** Decree 0002 §2 (the minimal stored substrate)
- **Status:** active

## Decision

**1. The Character root stores one `features` ledger.** Every Character, Player or NonPlayer, carries a `features` ledger beside its Dice and its `training` ledger. It is the record of what the Character was granted: its Entries and Chips.

**2. The ledger stores recipes, never finished text.** A grant holds its title, its facets (origin, kind, activation, level) and its values as literals or as functions that read the Character. It never holds a resolved number or pre-built HTML. The sheet reads the ledger once, after generation, so a level-20 capstone still changes a number that a level-14 feature prints. This keeps Decree 0002 §3 ("a stored skill is a cache that drifts") and the Feature-Text rule "an Entry is a projection, not a snapshot".

**3. One writer.** Grants enter the ledger through one function, which stamps the granting Tag. Nothing else writes to it.

**4. The vocabulary lives in `Compass_of_Features`** (Dialog 0026, R2): one types-only module the domain owns and Venustas may import.

Decree 0002 §2 now reads: the root stores `name`, `title`, the six `scores`, `size`, `tier`, `seed`, the Dice, the `training` ledger and the `features` ledger.

## Reasoning

The `training` ledger already set the pattern Julio approved in Dialog 0025: "the ledger is the writer, the sheet its projection". A shared ledger gives every Character one place for its features. It replaces today's nine Chip and Entry shapes, and it ends section placement by string prefix (about 9% of features currently fall through it).

## Alternatives not chosen

- **Derive the sheet by walking Tags, storing nothing** (Dialog 0026, Design B). It is purer, and TopKit removed its two obstacles. It was not chosen because per-character choices still need storing, and one visible ledger is simpler to read, count and test.
- **A section-keyed dictionary on the Character** (Design A). Not chosen: sections are a layout choice, and the same features must also print as an NPC stat block.

## Consequences

- `char.features` already names the legacy list of Feature objects. A behaviour-neutral step renames that list and re-points its readers before the ledger takes the name.
- The migration follows Dialog 0026 "Proposed order of work"; its sequencing against the TopKit pin (R4) is still open.
