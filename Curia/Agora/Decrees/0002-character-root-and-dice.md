# Decree 0002 — The Character root, the Dice, and the discipline

- **Ratified by:** Julio, 2026-06-23
- **Source:** Dialog 0003 (Q-0006) + Julio's arbitration
- **Status:** active · §2 amended by Decree 0009 (2026-09-24): the root also stores the `features` ledger (`Documenta/Agora/Decrees/0009-the-features-ledger-on-the-character-root.md`)

## Decision

**1. One root: `Character` (refactor, not rebuild).**
There is one root object, **Character**, obtained by *refactoring the existing* `AtlasLusoris/Grimoire_of_Characters.py` — **not** by building a new parallel skeleton. PC and NPC are **tags** on that one Character, never separate classes.

**2. Minimal stored substrate.** The root stores only:
- `name` and `title` — **both required.** Title is not optional: we always generate a `Name, Title` pair ("John Doe, the Person of the Place") as a narrative seed. Title is the *narrative identity*, as core as the name.
- the six `scores` (rolled), `size`, `tier` (level for PCs / CR·level for NPCs), `seed`, and the **Dice** (below).

**3. Everything else is computed or tagged.** Skills, HP, AC, proficiency bonus, modifier — **computed/derived** (the Monk is right; a stored skill is a cache that drifts). Species, class, background, features, equipment, story — **tags**.

**4. The RNG *is* the Dice.** Each Character owns its own seeded RNG, named **Dice**, exposed as a method:
```python
Charlie.Roll(D=6)     # rolls a d6 from Charlie's own Dice (seeded by Charlie.seed)
```
Every mechanism rolls through the Character's Dice — no global `random`, no `app.random`, no module-level seeding. A Character becomes a pure function of its seed (reproducible; the shareable-link feature gains a real guarantee). This absorbs the scattered dice/RNG usage (incl. `AtlasLudus.Map_of_Dice`) into one elegant, thematic abstraction: *every character carries their own dice set.*

**5. `AtlasAlusoris` merges into `AtlasLusoris`.** *Lusoris* is the character domain; *A-lusoris* = *Non-*player is a **tag** (Non/Player), not a parallel Atlas. Fold `AtlasAlusoris` into `AtlasLusoris`; the NPC becomes a Non-tagged Character. (This resolves QST-0005 by **merge**, not rename.)

**6. `AtlasTOP` is removed.** It was unsanctioned bloat (a rogue-agent parallel layer). Its composition (`compose_character`/`compose_npc`, the `kind` stamp) folds directly into the Grimoires using TagKit; the `kind = character/npc` flag becomes the Player/Non role tag. No parallel TOP codebase. (QST-0018.)

## Reasoning
The council converged on instance-RNG for correctness (kills the global shared-state bug, guarantees seed-reproducibility). Julio's refinement makes it *elegant*: the RNG is re-expressed as the game's own abstraction — the Dice each character carries. Title-as-required and skills-as-computed come from play experience and the Monk's minimalism respectively. The Atlas merge and AtlasTOP removal enforce the project's founding discipline (below): TOP exists precisely to avoid "dump everything of a kind in one folder."

## Alternatives not chosen
- **Functional-core-in-one-move / keep-global-seeding** — superseded by instance-Dice.
- **Keep AtlasAlusoris separate / rename** (old QST-0005 options) — superseded by merge.
- **Build a fresh Character skeleton** — rejected; we refactor existing files, never scaffold a parallel codebase.

## Consequences
- **Canon updated:** `Code-Style.md` gains the anti-bloat discipline rule (one purpose per Atlas; refactor existing files; no catch-all folders).
- **QST-0016** reframed as a *refactor* of existing files, spawning sidequests: root `Character` + `name/title/scores/size/tier/seed`; **Dice/`Roll(D=)`**; Player/Non role tags; fold `AtlasAlusoris`→`AtlasLusoris`; one sheet renderer; reproducibility tests.
- **QST-0018** opened: remove `AtlasTOP`, fold composition into the Grimoires.
- **QST-0005** resolved via merge (folded into the above).
