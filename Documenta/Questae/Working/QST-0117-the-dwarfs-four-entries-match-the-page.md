# QST-0117 — The Dwarf's four entries, as the page states them

- **Type:** code / lore-fidelity
- **Priority:** 🟠 high *(user-visible sheet text)*
- **Status:** Working (the two defects landed; the four lines await Julio)
- **Owner:** Claude
- **Route to:** Technical Team · Lorekeeper · Julio
- **Parent:** QST-0094
- **Related:** QST-0113 (the same work on the Aasimar) · QST-0116 · QST-0119 · `Documenta/Canon/Mythos/Dwarf.md` §0 · `AtlasActorLudi/SpeciesKit/Dwarves/`

---

## 🔍 Diagnosis (what & where)

`Dwarf.md` §0 states four rules and four lines. The sheet carries the four rules
and none of the lines. Read off a generated Dwarf at levels 1 and 5, projected
through `Resolve_Dwarf_Features`, 2026-09-12.

**1. Not one of the four lines reaches the sheet.**

The Aasimar's eight were wired on 2026-09-11 (QST-0113) in the house format:
`*line*`, a blank line, then the rule. The Dwarf's four are authored, sit on the
page under their rules, and are marked *(authored, not wired)* there. Nothing
projects them, so a Dwarf sheet is four paragraphs of rulebook and no voice.

Read across the roster, 2026-09-12: the Aasimar, Elf, Halfling, Orc and
Dragonborn print an italic line; the Gnome and the Goliath print authored prose
instead, which QST-0094 recorded as the second convention; **the Dwarf and the
Tiefling print neither.** The two are not in the same position, though, and that
is the point of this ticket. The Tiefling's lines have never been written. The
Dwarf's are written, sit on its page, and are one commit of four strings away.

| Entry | The page's line | The sheet |
|---|---|---|
| Darkvision | *The mines taught our eyes to work where the lamps do not reach.* | nothing |
| Dwarven Resilience | two wordings, see QST-0116 | nothing |
| Dwarven Toughness | *A dwarf is built like a ledger: every year adds a line, and none is ever struck out.* | nothing |
| Stonecunning | *Lay a hand on the stone and listen. The mountain still keeps our accounts.* | nothing |

**2. ~~Stonecunning put the stone contact on the wrong thing.~~ Fixed
2026-09-12.**

The sheet read *"You must be on a stone surface or touching a stone surface to
use this **Tremorsense**"*, which a table reads as a condition on keeping the
sense for its ten minutes rather than on starting it. Ten minutes is a long time
to hold a wall. The published rule and §0 both put it on the Bonus Action.
`Dwarves/resolution.py:119` interpolated `Stonecunning.SENSE` where it meant
`Stonecunning.ACTION`, so the defect was one constant wide. The page names this
one itself:

> This is a projection to correct in `Dwarves/resolution.py`, not a house rule

**3. ~~`Dwarven_Toughness` published its contribution twice.~~ Fixed
2026-09-12.**

`Dwarves/traits.py` carried the same eleven lines back to back, comment and all:
read `bonus_health_sources`, set the Dwarf's key, sum, then do it again. The
by-name dictionary made it idempotent, so nothing on any sheet was ever wrong,
which is exactly why it survived. This is the same defect QST-0113 found in
`Aasimar/resolution.py`, in the same shape, so it is worth saying out loud that
**a duplicated block in this codebase is a copy-paste signature to grep for after
a vault restore**, not a coincidence.

## 🧾 Evidence

- `Resolve_Dwarf_Features` on a bare Dwarf, levels 1 and 5: four entries, no
  italic line in any description, before and after.
- `bonus_health_sources` is `{'Dwarven Toughness': 1}` before and after the
  de-duplication, so the removal is provably behaviour-preserving.
- `python -m AtlasActorLudi.SpeciesKit` cannot run in this checkout: it dies in
  `AtlasLusoris/Grimoire_of_Guilds.py:34` on `ValueError: bad marshal data`,
  a version-locked `.pyc` bootstrap, on the Elf path and before the Dwarf. It
  fails identically on a clean tree. QST-0076's territory, recorded here because
  it is why the house self-test could not sign this change off.

## 🎯 Desired outcome

1. ~~Stonecunning's stone contact is on the Bonus Action.~~ Landed.
2. ~~The duplicated block is gone.~~ Landed.
3. All four lines reach the sheet in the house format, **once Julio has ruled
   which Resilience line is the line** (QST-0116, item 2). One commit, four
   strings, no logic.

## 🧭 Notes for the implementer

The wiring is one prefix per entry, exactly as the Aasimar does it:

```python
	"*Lay a hand on the stone and listen. The mountain still keeps our accounts.*\n\n"
```

**One thing to decide before writing them, and it is not mechanical.**
For-Reviewers rule 3 asks for second person and no collective *we*, and three of
the four lines say *our*: our eyes, our ancestors, our accounts. That is not a
defect here. The rule reads *"no collective 'we' for a people with no shared
culture"*, and the Dwarf is the people who most plainly have one: QST-0094
ratified the species entry's first person plural (*"Dwarves. We remember."*) for
that reason. But the species entry is the people talking about themselves, and a
feature line is the project talking to one player about their own body. *The
mines taught our eyes* puts the reader inside a clan they have not been given
yet. *The mines taught your eyes to work where the lamps do not reach* costs
nothing and lands on the person holding the sheet.

Julio's call, and it is the same call for all four at once.
