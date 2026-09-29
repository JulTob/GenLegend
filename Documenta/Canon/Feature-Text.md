# 📜 Feature Text — how a sheet entry is written

*The prose a player actually reads: Species traits, class lessons, feats,
invocations, patron paragraphs. `Code-Style.md` governs the code; this governs
the text that code emits.*

Its one inherited principle, from that document's Spirit:

> **Explicit beats magical.**

> **Julio's ruling, 2026-09-24 (QST-0142):**
> - **One Entry** is a title, a flavor line and the rules text (`AtlasVenustas.Entry( title, rules, flavor )`). Its section and level are metadata that do not print.
> - **One Chip** is a symbol, a label and a value.
> - **Text is Markdown, never HTML**, so every medium prints from it: `f"{entry:html}"`, `f"{entry:md}"`, `f"{entry:json}"`.
> - **Several short Entries beat one long one.**
>
> The HTML examples below describe feature text as it was written before that ruling. Each QST-0142 station converts its family's text to Markdown. The rules about *what* to write (breaks, voice, projection, what a sheet states) still hold.

---

## Breaks are written, never inferred

A Feature that carries several labelled parts must put an explicit `<br>` in
front of every label that follows other text. In the source, where the author
writes it.

```python
DESCRIPTION = (
	"<b>Thieves' Cant.</b> You know Thieves' Cant. "
	"<br><b>Instrumental Training.</b> You gain proficiency with a Musical "
	"Instrument of your choice. "
	"<br><b>Cause a Scene.</b> When you take the Help action to aid an ally's "
	"attack roll, the enemy you distract can be within 30 feet of you."
	)
```

The first label opens the description and takes no break. Every later one does.

**Do not infer them at render time.** This was tried and reverted the same day.
The heuristic was "a bolded run ending in a full stop is a sub-heading, so break
before it", and across 652 sampled features it was *right every time* — 91
period-terminated labels, all genuine, against 113 emphasis bolds (`<b>1d6</b>`,
`<b>4</b>`, `<b>Charisma</b>`) it correctly left alone. It was still wrong,
for three reasons worth keeping:

1. **It read as correct and shipped a corruption.** `Lodge_of_Spells.py` writes
   spell tables as `<tr><td>🟡 <b>Yellow.</b> Failed Save: 12d6 Lightning
   damage.</td></tr>`. The rule inserts a line break inside a table cell. A
   sweep of *rendered feature descriptions* never sees it, because that text is
   a spell body, not a Feature.
2. **The author cannot see it.** Whoever writes the next description has no way
   to know a break will appear, and no way to say "not here."
3. **It is a guess about intent.** Julio's rule: *"inserting automatic breaks
   can break the style in unexpected places. Explicit is better."*

### Two traps found while doing it properly

**A source line is not a rendered line.** Descriptions are concatenated string
literals, so a label at the start of a *source* line is usually mid-sentence in
the *rendered* text. A scan of source lines reported 212 sites needing breaks;
the real number, measured from rendered output, was about 18. Derive the list
from what a reader sees, not from how the literal is typed.

**Some Features have two descriptions.** `Crafter` carries a static
`DESCRIPTION` *and* a second built during `awaken` that names the tools actually
rolled. The resolved one is what reaches the sheet. Fix both, or the constant
looks right in source while the page is unchanged. Grep the feature's name, do
not assume one definition.

**Templated Features take the break once.** The `Sign of the …` Order feats are
generated from one builder in `OrderKit.py`; editing the template covers every
Order rather than each of the generated variants.

### Checking it

A Feature renders as a run-on when two `<b>Label.</b>` runs appear with no
`<br>`, `</li>`, or paragraph break between them. Sweep generated characters
across guilds, species and levels and read the *descriptions*, not the source.
The catalogue was at zero across 759 sampled Features when this was written.

---

## The rest of the settled rules

Short, because each is already argued somewhere else.

**Dice notation, not sentences.** `1d12 + 2`, `1d8 - 1`, or the bare die at
exactly `+0`. Never "roll 1d12 and add 2", and never let a negative modifier
render as "add -2". Branch on the sign: see `_signed_die` in
`AtlasActorLudi/SpeciesKit/Goliaths/resolution.py`.

**Resolve what the sheet already knows.** A feature that says "a number of times
equal to your Proficiency Bonus" should show the number too: *"4 times (equal to
your Proficiency Bonus)"*. The reader is holding the sheet; make it checkable at
a glance.

**No open-choice language.** This is a generator, not a builder. Every pick was
made by a seeded Dice Bag before the page existed, so nothing may read as though
a decision is still pending. Not *"three skills of your choice"* but the three
skills, named. Where a placeholder must be granted before the choice resolves,
overwrite it afterwards through `_update_feature_description`, as `Skillful` and
`Skilled` do in `FeaturesKit.py`.

The exception is a choice genuinely re-made at the table every time the feature
is used, such as an Aasimar picking a Celestial Revelation on each
transformation. Those stay open because the rules keep them open.

**Chips are lookups, prose is the entry.** A chip is what a player reaches for
mid-combat: one label, one value. Anything that needs a sentence belongs in the
description.

---

## Where the voice rules live

How the prose *sounds* (second person, inspiration line before the rule, no
em-dashes, traits as taught rather than inherited) is a separate matter from how
it is formatted, and is being settled per-Species and per-Guild as the entries
are written. See `QST-0062` for the outstanding voice sweep, and the design
comments above `FIEND_DESCRIPTION` in `AtlasLusoris/AtlasOfGuilds/WarlockKit.py`
for a worked example of recording *why* a paragraph is written the way it is.

---

## An Entry is a projection, not a snapshot

*Recorded 2026-08-21, after a Barbarian printed a save DC two points low for six levels.*

A Feature's `description`, and every Chip value, may be a callable taking the
Character. **It is resolved when the sheet is read, not when the Feature is
granted.**

### Why

Features are granted in level order, so anything granted early freezes before
anything granted later can change the numbers underneath it. Intimidating
Presence is a level-14 Barbarian feature that quotes a Strength-based save DC.
Primal Champion is a level-20 capstone that adds +4 Strength. Resolving the
Entry at grant time meant the level-20 sheet advertised **DC 16 when the real
DC was 18**, and the same trap was waiting for the Monk's capstone.

This was invisible while the text read *"DC 8 plus your Strength modifier and
Proficiency Bonus"*, because a formula is never stale. It only appeared once
the house rule about resolved numbers was applied. Printing a number is a
promise that the number is current.

### The invariant this rests on

**An Entry callable must be a pure read.** It may look at anything on the
Character. It must decide nothing.

Anything that draws, picks, or assigns belongs in `apply`, which runs once,
guarded against re-entry, and against a named Dice Bag. An Entry that decides
will silently re-decide every time the sheet is rendered.

One did. The Druid's Primal Order drew `Pick(("Magician", "Warden"))` from the
shared stream inside its Entry, with no guard, so a Druid could change Order
between two reads of the same sheet. It now settles in `apply` the way the
Cleric's Blessed Strikes already did.

### How to apply

- Writing an Entry that needs a number: read it, resolve it, print it.
- Writing an Entry that needs a *choice*: put the choice in `apply`, record it
  on the Character, and have the Entry read the record. `_primal_knowledge_entry`
  and `_apply_primal_skill` in `Map_of_Barbarian_Training.py` are the pattern.
- `Feature` refuses a callable without a `subject` rather than rendering empty,
  so the mistake surfaces at the construction site.
- Entries that top up an accumulating record (weapon masteries) are fine, as
  long as the top-up is a no-op once the quota is met.

## A sheet states what the character has, not what a player may elect

*Recorded 2026-08-27, after verifying the Eldritch Knight against the 2024 text.*

Rulebook sentences of the form **"whenever you gain a [Class] level, you can
replace X with Y"** are not written on a generated sheet, and their absence is
not a gap.

### Why

A sheet from this project describes one finished character. Retraining clauses
describe an election a player makes at a table between sessions, and in a
generator that election has already happened, invisibly, inside a Dice Bag.
Printing *"you may replace one of these cantrips"* on a sheet that nobody will
level up offers a choice which does not exist, in the one register where every
other line is a fact about the character.

Julio, refusing the clause when it was offered as a rules omission:

> For a character written in a generator, choosing doesn't happen, so we don't
> offer that here.

### The distinction that decides it

Sort every "you can replace" sentence into one of two piles.

- **An election at level-up.** Cut it. The generator already chose.
- **A decision made during play.** Keep it. The character really does make it,
  and the sheet is the only place they would read about it.

The second pile is larger than it looks and must survive the sweep intact:
replacing an attack with a cantrip (War Magic), with a Flurry (Monk), or with a
breath (Dragonborn) is an action in a round. Swapping a known Wild Shape form,
a Hunter's Prey option, or Banneret's Polyglot language on a Long Rest is a
decision taken mid-adventure. None of these are retraining.

Constraints that merely *sound* like elections stay too, because they state what
the character has: the Warlock's invocation prerequisites, and that an
invocation cannot be taken twice.

### How to apply

- Auditing a class against the rulebook: expect to find these missing, and do
  not restore them. Seven were deliberately removed on 2026-08-27, across Bard
  Spellcasting, Magical Secrets and Additional Magical Secrets, Sorcerer
  Metamagic (current and legacy), Warlock Mystic Arcanum and Eldritch
  Invocations.
- The removal is silent **to the reader of the sheet**, not to the repository.
  This section is the record; do not add apology comments at the sites.
- The same instinct governs [resolved numbers](#) and
  `upgrade features actualize the parent`: an entry carries what is true now,
  owned in exactly one place, with nothing hypothetical attached.
