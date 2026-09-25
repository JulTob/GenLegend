# QST-0119 — Shared rule text has no single home, and the lock does not check rules

- **Type:** design / process
- **Priority:** 🟠 high *(it decides what "locked" is worth, for every species after the Aasimar)*
- **Status:** Open
- **Owner:** Julio (the ruling) · Technical Team (the script)
- **Route to:** Julio · Lorekeeper · Technical Team
- **Related:** QST-0113 · QST-0116 · QST-0117 · QST-0094 · `scripts/verify_aasimar_page.py` · `AtlasActorLudi/SpeciesKit/traits.py::Darkvision_Rules`

> Found while running the Dwarf review the way the Aasimar was run. It is not a
> Dwarf finding. It is the first thing the Aasimar's method hits when a second
> species tries to use it, so it should be settled before a third page is locked.

---

## 🔍 Diagnosis (what & where)

`README.md` states the protocol: **a book means locked, and the code adapts to
the book.** `Aasimar.md` is the worked reference and carries the first lock.
`scripts/verify_aasimar_page.py` exists so the claim is mechanical rather than
asserted, and it passes.

Two things are true at the same time, and together they are the problem.

**1. Darkvision's rule text exists in three wordings, one of them on a locked
page.**

| Source | The Darkness clause |
|---|---|
| `traits.py::Darkvision_Rules` (what prints, for every species) | *In Darkness within that range you can see as if it were Dim Light **(**you have Disadvantage on Wisdom (Perception) checks that rely on sight, and **colors are only** shades of gray**)**.* |
| `Aasimar.md` §0 (**locked**) | *In Darkness within that range you **see** as if it were Dim Light**:** you have Disadvantage on Wisdom (Perception) checks that rely on sight, and **you discern colors there only as** shades of gray.* |
| `Dwarf.md` §0 | *In Darkness within that range you can see as if it were Dim Light**:** **within that Darkness** you have Disadvantage [...] and you discern colors there only as shades of gray.* |

The Dwarf page also opens its entry with *"You have Darkvision with a range of
120 feet"*, a sentence the code never prints.

By the protocol, the locked page wins and `Darkvision_Rules` is a defect. But
`Darkvision_Rules` is **shared**: the Aasimar, the Dwarf, the Elf, the Orc, the
Gnome and the Tiefling all print the same function's output at their own range,
and its docstring is a careful piece of work that explains why each of the three
scopes is load-bearing. Adapting it to the Aasimar's colon rewords six species'
sheets to satisfy one page. Adapting it to the Dwarf's is the same move in the
other direction. **One shared function cannot satisfy two differently worded
locked pages, and there are eight species pages left to lock.**

**2. The verify script does not check a single rule.**

It checks the player-facing description byte for byte, that the eight lines reach
`resolution.py`, the nine Ideals row by row, the eight perches, the eleven
plumages, and Size, Size weighting and Speed. It never compares a rule text.

That is precisely the hole QST-0113 fell through the first time: of the defects it
found, **three were drifted rule texts** inside Celestial Revelation, not lines,
and the script written afterwards would not have caught any of the three. It
would catch them re-drifting today only because the option paragraphs happen to
contain their lines. So the lock currently proves the lore and the tables, and
takes the rules on trust, which is the opposite of where the risk is: a line is
authored once and left alone, and a rule is edited every time a constant moves.

## 🎯 Desired outcome

Julio rules on the first; the second follows from it.

**A. Where does shared rule text live?** Three candidates, and this ticket does
not prefer one:

1. **One text, quoted.** `Darkvision_Rules` is the single source, and every
   species page quotes it verbatim at its own range. Pages stop paraphrasing
   rules that are not theirs. Cheapest to verify: the check becomes
   `Darkvision_Rules(range) in page`.
2. **One text per species.** Each page owns its wording and the shared helper
   becomes a default that species with a page override. Most faithful to "the
   page is the authority"; it also means six near-identical strings, and the
   docstring's three scopes have to survive in each.
3. **The page states the rule, the code states the sheet.** A 📕 entry is written
   for a reviewer resolving it at a table, and the sheet is written for a player,
   and they are allowed to differ in wording but never in effect. This is the only
   option that survives the *second* case below, and it costs the byte-for-byte
   check.

**The second case, because it decides between them.** `Dwarf.md` §0 writes
Stonecunning's allowance as the whole table, *"a number of times equal to your
Proficiency Bonus (2 at Levels 1-4, 3 at 5-8, 4 at 9-12, 5 at 13-16, 6 at
17-20)"*. The sheet prints the resolved number for the character holding it,
*"(3)"*. For-Reviewers rule 8 says **a sheet prints resolved numbers rather than
formulas**, so here the code is right and the page is wrong, and "the code adapts
to the page" would be a regression. The Aasimar avoided this by inventing a
notation instead: its legend declares *"Curly brackets {} represent the resolution
of the calculation"* and its rules read **{PB}d4** and **DC {8 + PB + CHA}**. That
convention is on one page and in no standing rule. If option 1 or 2 is chosen,
the brace notation has to become a folder-wide rule and the Dwarf page has to
adopt it.

**B. The script grows a rules check**, whichever way A goes, and becomes
`scripts/verify_species_page.py` taking a species name, so the tenth page costs
an argument rather than a file. Its Aasimar behaviour must not change.

## 🧭 Note

Nothing here says the Aasimar lock was wrong. It says the lock proves what was
hard to get right *once* and not what is easy to get wrong *repeatedly*, and that
the second species is the right moment to find that out rather than the ninth.
