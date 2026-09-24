# Decree 0009 — The sheet is read from the Tags

- **Ratified by:** Julio, in chat, 2026-09-24
- **Source:** Dialog 0026 (Q-0035), ruling R1
- **Status:** active
- **Supersedes:** the same day's first ruling on R1 (a `features` ledger on the Character root), withdrawn before it landed. Decree 0002 stays as ratified: the root is not amended.

## Decision

**1. A Character's features are its Tags.** Each Tag declares what it gives (its Entries and Chips) as plain class data in its own module. Nothing about the sheet is stored on the Character.

**2. The sheet is a walk.** To print a Character, ask TopKit which Tags it carries (`Tags( char )`, in application order). For each Tag, visit its Form, meaning the Tag and the Bases it specializes, Base first. Read only what each Tag itself declared (its own `__dict__`, never inherited). Resolve every value at that moment against the Character. A layout in the visual package groups and orders the result.

**3. Applying a Shape applies its Bases.** `Necromancer( charlie )` makes Charlie a Wizard and a Guild member too. The walk prints Guild, then Wizard, then Necromancer, because Bases come first.

**4. Choices are Tags.** A choice (Fighting Style, Invocation, Feat, a spell) is made once, inside the Imprint of the Tag that offers it, and applied as a Tag. TopKit allows an Imprint to apply another Tag (0.2.0a2 onward). What truly cannot be a Tag is a Record written once, in the same Imprint.

**5. Choices are stable across levels.** Each batch of choices draws from a named Dice Bag, seeded from the Character's seed and the batch's purpose and level (`char.Dice_Bag( "fighting_style" )`, `"invocations.5"`). A level-5 Character therefore makes exactly the choices its level-4 self made, plus the level-5 ones. Building level by level is the proof: the Tags of a level-4 build are a subset of the level-5 build's Tags for the same seed.

**6. Choices respect what the Character already holds.** A choice pool leaves out anything the Character already carries (`spell not in char`): an Aasimar Wizard already knows Light, so Light is not a Wizard cantrip choice. When a Tag later grants something already chosen (a Fiend patron granting Command to a Warlock who chose it), the granting Tag's Imprint gives the choice back and chooses again, in small steps, one Tag at a time.

**7. Reading is pure.** A text or Chip function may read anything and decide nothing. Every roll is a choice, and every choice happens in an Imprint (point 4).

**8. Port, don't adapt.** Legacy features are ported into Tags, family by family. No adapter keeps the old shapes alive.

**9. Vocabulary, sections and flags** follow Dialog 0026 R2, R3 and R5: `Compass_of_Features`; sections Species, Background, Guild, Feats, Proficiencies, Equipment, Backstory, Magic (spells, focus, special resources), Others; flags are TopKit `@Flag` Tags.

## Reasoning

Julio: *"I like the library card design. It is elegant... the project is a flagship of Tag Oriented Programming, so it is the TOP solution."* The Tags already are the record of what a Character is, so a stored copy could only drift from them. The walk gives one source of truth per feature, local changes for new content, automatic removal on Rip, and a Markdown sheet that is current by construction. The cost measured on 0.2.0a1, about 5.6 ms per applied Tag, is affordable for one Character per click. Julio: *"Speed without control means crashing even harder."*

## Alternatives not chosen

- **A `features` ledger on the root** (Dialog 0026, Design C). Ruled earlier the same day, then withdrawn in favour of the walk. A stored ledger duplicates what the Tags already say.
- **A section-keyed dictionary on the Character** (Design A). Sections are a layout choice, not a fact about the Character.

## Consequences

- The work needs TopKit: nested Imprints arrive in 0.2.0a2. It follows the pin (QST-0093.5).
- Within a section the layout orders entries by the level gained, not by walk order. A Base's level-5 feature must not print ahead of its Shape's level-3 feature.
- `char.features` and the legacy Feature classes are retired as their families are ported.
