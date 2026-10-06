# QST-0118 — Two leftovers in the Dwarf kit, and one of them disagrees

- **Type:** code / hygiene
- **Priority:** 🟡 normal *(one of the two can mislead a later hand)*
- **Status:** Open
- **Owner:** unclaimed
- **Route to:** Technical Team · Julio (item 2 is authored text)
- **Related:** QST-0115 (the same sweep on the Aasimar) · QST-0091.1 (Species: one file) · QST-0072 (recovery) · QST-0117

---

## 🔍 Diagnosis (what & where)

Two files found reading `SpeciesKit/Dwarves/` against the page. Neither is
visible on a sheet, so neither was folded into QST-0117. The second is worse
than the Aasimar's equivalent and should not be treated as the same ticket twice.

**1. `AtlasActorLudi/SpeciesKit/Dwarves.py` is dead, and it defines a second
`Dwarf`.**

The flat module and the `Dwarves/` package sit in the same directory. Python
resolves the package, so every importer gets the package: `SpeciesKit/__init__.py:68`,
`catalog.py:9`, `resolution.py:102`. Nothing reaches the flat file at all.

It is not an empty stub. It declares its own `class Dwarf(Species, Humanoid)`
with a docstring (*"A resilient Humanoid with an affinity for stone"*), its own
`Set_Physiology`, and its own `Player_Handbook_2024` registration with the same
weight, size and speed. What it does **not** have is the four traits. A later
hand who finds it, reads it, and adds a trait there will have written correct
code that changes nothing on any sheet, and the search that would explain why is
the one nobody runs. `Dragonborn.py` is in the same state; every other package
species (Aasimar, Elves, Gnomes, Goliaths, Halflings, Orcs, Tieflings) has no
flat twin, so these two are the residue of QST-0091.1 rather than a convention.

**2. `Dwarves/__init__.py.source-partial` is an older draft of the species
entry, not a copy of it.**

QST-0115 found the Aasimar's `.source-partial` byte-identical to its
`__init__.py` and left it because deleting a tracked file is not a thing to do in
passing. The Dwarf's is **different text**, and the difference is the exact thing
QST-0094 decided:

| | `__init__.py` (shipping) | `.source-partial` |
|---|---|---|
| Voice | *"Dwarves. **We** remember. **Our** people ruled the world once."* | *"Dwarves. **They** remember. **Your** people ruled the world once."* |
| Metal | *"Metal is holy to **our** people. Everything **we** dwarves ever built, **we** built..."* | *"Metal is holy to **your** people. Everything the dwarves ever built, **they** built..."* |
| Greed | *"They do not understand. Gold never corrupts."* | *"**Greed is not the only reason.** Gold never corrupts."* |

So the repository tracks, beside the ratified first-person entry, a full
second-person alternative with a sentence the shipping text does not contain.
Nothing imports it and nothing ever will, because the name is not a module name.
It reads as a source of truth and it is not one. That is the failure mode
QST-0115 named for `glow_from`: *a field that states something the generator does
not do is worse than absent, because a later hand will trust it.*

## 🎯 Desired outcome

1. `SpeciesKit/Dwarves.py` leaves the tree, and `Dragonborn.py` with it if the
   same reading holds there. Under QST-0091.1 the package is the one file.
2. `.source-partial` leaves the index. Before it does, Julio reads the three rows
   above once: *"Greed is not the only reason"* is a sentence that was written and
   then dropped, and this ticket is the last place it exists. If it is wanted, it
   belongs in the entry or on `Dwarf.md`, not in an unimported file.

## 🧭 Note

Deleting tracked files is the kind of change this project has been burned by
(QST-0072, and the whole `.recovery-vault`). Both deletions are one commit, they
are provable (no importer, no module name), and they should be their own commit
with nothing else in it.
