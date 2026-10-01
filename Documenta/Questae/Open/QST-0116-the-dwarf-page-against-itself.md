# QST-0116 — Five places where the Dwarf page contradicts itself or the code

- **Type:** lore / copy
- **Priority:** 🟠 high
- **Status:** Open
- **Owner:** Julio (only)
- **Route to:** Julio · Lorekeeper
- **Related:** QST-0094 · QST-0117 · QST-0118 · QST-0119 · `Documenta/Canon/Mythos/Dwarf.md` · `Documenta/Canon/Mythos/Aasimar.md` (locked)

> Opened 2026-09-12, first pass of the Dwarf review, run the way the Aasimar was
> run: every claim read out of the implementation rather than from memory.
> Nothing on the page was edited. Only Julio edits a book.

---

## 🔍 Diagnosis (what & where)

The Dwarf page is the second-best chapter 0 in the folder and it already knows
most of what is wrong with it: §0's *Unratified* list is fifteen items long and
honest. These five are different. They are places where the page disagrees with
**itself**, or with a page that is already locked, so no ratification is needed
to settle them. Somebody just has to pick the surviving sentence.

**1. §2 calls Darkvision "the deepest on the roster". §0 forbids exactly that
sentence, and the code agrees with §0.**

§0 states it plainly:

> the ranking the page has been making is wrong: 120 feet is the longest range on
> the roster but not the Dwarf's alone [...] Whatever is written must say "as
> deep as anyone's", never "the deepest".

§2 then writes it anyway:

> **Physical traits.** Darkvision to 120 feet (the deepest on the roster) [...]

The code settles the fact. `Dwarves/traits.py:12` is 120; so is `Orcs/traits.py:37`;
so are `Elves/Drow.py:19`, `Elves/Dark_Elf.py:19` and `Elves/Shadow_Elf.py:26`.
Five ranges tie. §2 is the defect, and it is one parenthesis wide.

**2. The Dwarven Resilience line exists in two wordings, and they disagree.**

| Where | The line |
|---|---|
| §0, under the rule | *Every dwarf grows up tasting the mine air and the smelter's fumes. What did not kill your people taught them.* |
| §9, the ratification table | *Every dwarf grows up tasting the mine air and the smelter's fumes. What did not kill our ancestors does not poison us.* |

QST-0094 proposed the §9 wording. Somebody rewrote the second sentence when it
was carried into §0, and the two copies have sat side by side since. They are
not the same claim: *taught them* is the taught-not-inherited law speaking, and
*does not poison us* is the mechanic restated, which For-Reviewers §7 rule 1
spends the sentence on. The other three lines are identical in both places.

QST-0117 cannot wire four lines while one of them is two lines.

**3. §3 quotes the species entry, and the quotation is not what the entry says.**

§3 opens on what reads as a verbatim quotation:

> *"Our people ruled the world once. Then the Great Mountain fell, the Gilded Era
> ended with it [...]"*

`Dwarves/__init__.py:19` says **Guilded** Era. §0 already flags the spelling in
its *Unratified* list, so the page knows; §3 quietly corrects it inside quotation
marks, which is the one place a page may not correct anything. Either the entry's
spelling is a typo and the code changes, or *Guilded* is the joke (a guild era
that was also gilded, which for this people would be a good joke) and §3 must
quote it. It cannot be both.

**4. §2's list of the Aasimar's metals is three short, and the Aasimar page is
locked.**

§2 reads:

> The Aasimar's talaria shine like metals (black iron, gold, red iron, silver,
> verdigris, bronze) and confirm nothing

`Aasimar.md` §0 tables nine Ideals, and the metal column now holds **black iron,
gold, red iron, silver, verdigris, pearl, tin, bronze, brass**. Tin arrived with
Hope's laurel and brass with Harmony (QST-0111). Pearl is not a metal and never
was, which is worth a decision of its own, but the Dwarf page is missing tin and
brass either way. A locked page outranks an unlocked one, so this is the Dwarf's
sentence to update, not the Aasimar's table.

**5. §0 accuses §8 of an error, and §0 is the one that is stale.**

§0's *Unratified* list, on Darkvision:

> The decisions log in §8 is wrong here and should be corrected now: QST-0094
> records the Aasimar as chip-only by design and lists the convention as still
> open (Elf, Orc, Gnome, Dwarf and Tiefling print the rule; Aasimar and
> Dragonborn print the chip)

QST-0094 has not said that since 2026-09-11. It now reads:

> Elf, Orc, Gnome, Dwarf, Tiefling and now **Aasimar** print the rule under an
> italic line [...] **Dragonborn is the last one printing a bare chip**, and it is
> the whole of what is left of this question

And §8, the log being accused, already carries the current reading: *"settled
print, with a line for the Aasimar, which settles the convention if applied
here."* So §8 is right, §0 is quoting a ticket that has moved, and the
instruction to correct §8 should be struck rather than followed.

What is actually left of this for the Dwarf is small and worth stating as
decided. The Aasimar's settled shape is **rule, line, chip**. The Dwarf prints
rule and chip and no line, so once QST-0117 lands the four lines the Dwarf holds
the same shape as the locked page, and the open half of the question belongs to
the Dragonborn and not to this page at all. §8's row can move from *Awaiting
ratification* to *Decided*.

## 🎯 Desired outcome

Julio rules on each. All five are page-only, and four of the five are one
sentence:

1. §2 loses *"the deepest on the roster"* for §0's *"as deep as anyone's"*.
2. One Resilience line survives. QST-0117 wires whichever it is.
3. *Guilded* or *Gilded*, once, and §3 quotes what the code says.
4. §2's metals follow the locked table, and pearl is called what it is.
5. §0's Darkvision paragraph is restated against the current QST-0094, and §8's
   row moves to *Decided*.

## 🧭 Note

Item 2 is the only one that reaches the sheet, and it blocks QST-0117.
