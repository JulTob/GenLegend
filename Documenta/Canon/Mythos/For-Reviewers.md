# 👁 For Reviewers: how to read this folder

> 📜 **Settled.** No chapter is still in flow. 📜 1 · 📚 2 · 📔 4

*Orientation for anyone brought in to review these pages: a person, or another
model. Read this first. It states what the folder is, the rules the pages were
written against, and what a useful objection looks like here. Written
2026-09-09.*

---

## 📔 1. What you are reading

Analysis of a Dungeons & Dragons 2024 **character generator**: a program that
produces a finished, playable character sheet from a seed. There are no player
choices at the table. Every pick was already made by seeded dice before the
page existed, and the same seed always produces the same person.

These pages are **design and literary criticism written for the project's
author**. They ask, element by element, whether each part of the generator has
a coherent fantasy, whether it is original or borrowed, and whether it is well
told.

**What they are not.** Not player-facing text. Not documentation of how the
code works. Not a specification. Nothing in them is implemented, and every
proposal in them is waiting on the author's decision.

**One page is the exception, and it is the one to read first.**
[Aasimar](Aasimar.md) is 🔒 **locked** as of 2026-09-11, the first page to be, and
locked inverts the paragraph above. It *is* implemented, and it is the authority
over its own code: where `SpeciesKit/Aasimar/` and that page disagree, the code is
wrong and the code changes. `scripts/verify_aasimar_page.py` checks that claim
mechanically and passes. It is also the **worked reference** for the shape the
other species pages are growing into, so read its chapter 0 before judging
another one. Objections to it are still wanted, but they land as Questae against
a lock rather than as edits, and only Julio edits it.

---

## 📔 2. The rules the pages are written against

Judge the material by these, not by general fantasy-writing advice. Several of
them invert the usual advice on purpose.

1. **Death of the Author.** The deep lore exists so the writing stays
   consistent between hands. It is never explained to the player. A player may
   work a mechanism out from the text; nobody in the fiction ever confirms it.
   **Advice to "explain the lore more" is wrong here** and will be discarded.
2. **One register per voice.** Each class and each people has a single
   consistent register: the Fighter is a training memoir, the Warlock is a
   contract, the Barbarian is a chant, the Rogue is a shared picaresque. Mixing
   registers inside one piece is a defect.
3. **Second person throughout, and no collective "we"** for a people with no
   shared culture. Species prose states identity and drive; it never restates
   the rules the feature entries already carry.
4. **Traits are taught, gifted or suffered, never morally inherited.** The rule
   guards against monoculture and moral determinism. Plainly physical traits
   (darkvision, size) may be biological.
5. **Loaded names stay in the pool.** A character titled "Justiciar" who is not
   just is a story, not a bug.
6. **No em-dashes** in authored text. The author is a native Spanish speaker
   writing in English, and corrections to grammar and idiom are welcome as long
   as the voice survives.
7. **Never state a real-world parallel on a species page.** A species that is
   explicitly one real group becomes a mascot and stops being a people.
   Backgrounds are the exception, because a player *chooses* a background, so
   specificity there is a gift rather than an imposition.
8. **A sheet states what the character has**, never a choice still pending, and
   prints resolved numbers rather than formulas.

Flavor is in italic. This includes descriptions, lore and hooks. 
---

## 📔 3. What a useful objection looks like

Blunt and specific, quoting the line being judged. In order of value:

- **Where the analysis is wrong or overreaching.** A claim that reads well and
  does not survive the text it cites.
- **Where a "finding" is a cliché restated**, or where the pages praise
  something ordinary as though it were an achievement.
- **Literary and mythic sources missed or misattributed.**
- **Contradictions between pages.** There are 49 of them and they were written
  over one long cycle.
- **The drafted prose lines.** Which are good, which are trying too hard, and
  which break the register they claim to be in. The `Lines-Annex` gathers all
  of them in one place.
- **The three structural claims**, which are the load-bearing ones:
  1. the written backgrounds run a four-beat form whose hook is always a debt
     (`Backgrounds-Written`);
  2. the six spellcasting classes form a set of six relationships to the source,
     taken, granted, lent, contracted, performed, had;
  3. a "lineage" means something different in each people, and the ranking of
     those meanings matches how well each people is written (`Lineages`).

If those three survive a hostile read, the framework stands.

---

## 📔 4. Reading it remotely

The repository is public. A single page can be fetched raw:

```
https://raw.githubusercontent.com/JulTob/DnD/main/Documenta/Canon/Mythos/README.md
```

Swap the filename at the end for any page. While this work is still on its
branch and not merged, replace `main` with the branch name:

```
https://raw.githubusercontent.com/JulTob/DnD/Julio_Cl/fantasy-worldbuilding-analysis-4241c5/Documenta/Canon/Mythos/README.md
```

The folder itself browses at
`https://github.com/JulTob/DnD/tree/main/Documenta/Canon/Mythos`.

**On size.** The folder is about 145,000 words, which is roughly 190,000
tokens. Do not attempt it in one pass. Take one group per sitting:

| Group | Pages | Words |
|---|---|---|
| **Orientation and findings** | `README`, `Lenses`, `Repairs-Ledger`, `Agora-Questions-Proposed`, `Wiring-Plan`, `Voices-at-the-Table` | ~11k |
| **Peoples** | the ten peoples, `Lineages`, `Celestials` | ~31k |
| **Guilds, martial** | Barbarian, Fighter, Monk, Paladin, Ranger, Rogue, `Guilds-Registers-Names-Devices` | ~29k |
| **Guilds, casters** | Artificer, Bard, Cleric, Druid, Sorcerer, Warlock, Wizard | ~28k |
| **Backgrounds and Orders** | `Backgrounds-Written`, `Backgrounds-Official`, `Orders`, `Relationships`, `Draft-Tables` | ~20k |
| **Engines** | `Feats`, `Spells-and-Invocations`, `Stories-and-Titles`, `Names`, `Places`, `Equipment-and-Masteries`, `NPCs-and-Villains`, `Sheet-Alignment-Languages`, `Brand-Voice`, `Bard-and-Sorcerer-Lines` | ~17k |

`Lines-Annex` is a generated index of every drafted line with no argument in
it. Skip it unless you are specifically judging the lines.

**Where to start.** Backgrounds and Orders. The backgrounds are the strongest
prose in the project and they carry two of the three structural claims, so a
hostile read there tells you the most about whether the rest is trustworthy.

---

## 📚 4b. The four layers

Before objecting that a detail is arbitrary, check which layer it sits in.
Each element page opens with a `0. Rules` chapter (see the README) sorting its
content into four layers: a **fixed point**
(marked 📕 inherited from the 2024 rules, 📙 an aesthetic change, or 📒 a rule we
changed), an
**supportive lore** 📘 (chosen so a fixed point has a body: replaceable, never
deletable), **deep lore** 📗 (design that supports the fantasy rather than a
rule, and the place a later hand is licensed to play), and a **sugar line** (the
italic line on the sheet, freely rewritable inside its register).

The commonest wrong objection to this project is "cut this detail, it is not
needed." Run the test first: remove it and ask whether a rule is left with
nothing to say for itself.

## 📚 5. The canon these pages defer to

Four documents outside this folder are settled law, and the pages cite them
rather than arguing with them. A reviewer should know they exist before
objecting to something they explain:

- `Documenta/Canon/Cultural-Inspirations.md` : one culture key is one culture,
  never fused; which people holds which key.
- `Documenta/Canon/Dragons-and-the-Overcoming.md` : a dragon is a state a
  person reaches, not a species.
- `Documenta/Canon/Elves-and-the-Dreaming.md` : elf lineages are cultures that
  drift, not bloodlines.
- `Documenta/Canon/Tieflings-and-the-Shift.md` : belief made the fiends; a
  tiefling is born to ordinary parents and has no culture of their own.

Decisions are recorded as Decrees in `Documenta/Agora/Decrees/` and
`Curia/Agora/Decrees/`, and open questions become Dialogs. A choice that lives
only in a chat log does not exist.

---

## 📜 6. Belief is the only mechanism

*The setting's general law. Read it before objecting that a people's
metaphysics is inconsistent with another's: they are not competing
explanations, they are different kinds of belief.*

**All magic is belief.** Anything else is physics, and physics is not fantasy.

What differs between the powers of this world is not whether belief made them.
It is **how** belief made them, and **whose** belief it was.

**Two ways a thing becomes real.** By **manifestation**, when one person's
belief puts something into the world. By **actualization**, when a collective's
belief does. Every order of being sits somewhere on that line, and where it sits
is its nature.

| Power | The belief that makes it | What it is like as a result |
|---|---|---|
| **Fae and Elves** | The Dreaming | Dream-natured: soft, drifting, reshaped by what is dreamt |
| **Celestials** | Philosophical belief, and virtue | Well defined, the way an idea is well defined, and powerful in proportion to the goodness they are held to have |
| **Dragons** | A single will imposed on itself | Nietzsche's overcoming: a person who believes themselves into a superior being |
| **Titans** | Animist belief in the personality of nature | Nature with a temper, older than any order laid over it |
| **Gods** | A believed **order imposed on** nature by a personal deity | Rule rather than substance: a shape the world is told to hold |
| **Fiends** | The same engine turned to name an enemy | Made lower by being called lower |

**Before any of them there were primates who began to imagine.** They built
their dreams, their nightmares, their hopes and their pictures of themselves, by
accident, by pure actualization. That is as far back as the setting goes, and it
is deliberately not a creation myth.

**No order is ever stated between the classes of being.** Nothing is prior to
anything. A reviewer who finds an ordering anywhere in these pages has found a
defect, not a rule.

**Mystery is kept on purpose.** The Dwarven saint may be an ancestor watching by
their own will, or a manifestation raised by the living, or a soul attuning to a
metal believed real and therefore real. The setting never picks. A mechanism
that can be confirmed stops being a mechanism and becomes a rule.

### What this corrects

Two canon documents still carry a table calling the Aasimar *"Platonic Ideals,
prior to the gods, fixed and incapable of compromise"* against the Elf's
*"Jungian collective dreaming"*, and describe the contrast as a joke about the
elves being the only people shaped by what everyone imagines. That table
predates this law and is wrong twice: every people is shaped by belief, and no
ordering exists. It should become a table of **kinds of belief** rather than of
philosophies.

---

## 📜 7. How a flavour line is written

Every feature entry on a sheet is one rule and, above it, one italic sentence.
The sentence is the only place the project speaks to the player in its own voice,
and it is the part a reviewer is most likely to judge by the wrong standard. Four
rules govern it. Each was learned by getting it wrong first, on the Aasimar,
whose eight lines were drafted and redrafted until the rules below fell out of
the failures.

1. **A line teaches the fantasy, not the mechanic.** The player can read the
   rule; it is printed directly underneath. The line exists to inspire a trope or
   an archetype. A line that explains what the feature does has spent the one
   sentence it had.
2. **No mechanical detail in a line.** *"For a minute"* is obvious to any player
   after a single use, and putting it in the line costs the sentence that could
   have inspired. Durations, dice, ranges and recharges belong to the rule.
3. **A tell is an emotional reaction, not a logical step and not an
   environmental reading.** Where a feature reports on its carrier, the irony is
   that the feeling moves the thing being reported on, and never the other way.
   *"It dims when you are not being honest"* is a tell. *"It is dim in sunlight"*
   is weather, and *"it fades as your reasons run out"* is an argument.
4. **Write the emotion the way the emotion actually behaves.** Hope is the one
   that catches people out, so it is the worked example: hope is not
   desperation. Hope goes on against all odds. It comforts, it warms, it says
   stand up again. It is a faro for the future, a *try again tomorrow* sign, and
   the line it earned is *"It is faint when you wake up, but brighter as you get
   tired."*

**What this means for an objection.** "This line does not explain the feature"
is not a finding; it is rule 1 working. "This line would read better with the
duration in it" is rule 2 inverted and will be discarded. A useful objection
about a line says that it teaches the wrong fantasy, that it names a mechanic,
that it reads as an instruction rather than a reaction, or that the feeling in it
is not how that feeling behaves.
