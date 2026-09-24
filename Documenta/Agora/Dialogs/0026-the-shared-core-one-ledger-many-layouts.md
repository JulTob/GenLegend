# Dialog 0026 — The shared core: one grant ledger, many layouts

- **Question:** Should the core Character be restructured around what every Character shares (the Dice, the Chips, the Entries), with the visual package printing Chips and Entries in a declared order, section by section? Is "tags = flags + chips + entries" the right algebra?
- **Raised by:** Julio, in chat, 2026-09-23
- **Related Questae:** QST-0016 · QST-0016.5 (one sheet renderer) · QST-0020 (features with TOP) · QST-0021 (Venustas) · QST-0077 (sheet order, Solved) · QST-0078 · QST-0069 · QST-0081.1 · QST-0081.2 · QST-0081.4 · QST-0093.5 (the a3 pin)
- **Related Decrees and Dialogs:** Decree 0002 (the Character root) · Decree 0004 (player first) · Decree 0007 (every change is a proposal) · Dialog 0024 (TOP as a paradigm) · Dialog 0025 (the ledger is the writer, the sheet its projection)
- **Consuls called:** none convened. An agent panel stood in (six readers, three designers, three judges); see Deliberation. Julio may convene the Agora on any open ruling below.
- **Status:** 🟢 converged in the panel · awaiting Julio's rulings R1 to R5

---

## 🧭 Framing

**Julio's proposal, in his words.** *"There IS a core shareable by all characters: the rng, the chips, and the entries. We could design the Entry and Chip objects and their printing methods, and for printing the character just print the chips list in a determined way (at the visual package), respecting order to control presentation, and the same for the entries: a small dictionary of lists with Species, Background, Guild, then Proficiencies, Spells, and Others. That way we can add visual differentiation to the sections. The same patterns come up over and over again: tags = flags + chips + entries."*

**Constraints from Canon.**
- Decree 0002 §2 to §3: the root stores name, title, scores, size, tier, seed and the Dice; "everything else is computed or tagged"; "a stored skill is a cache that drifts".
- Feature-Text canon: "Chips are lookups, prose is the entry. A Feature with a chip and no prose is a record." And: "An Entry is a projection, not a snapshot"; an Entry callable must be a pure read.
- TagKit Doctrine: domain axes as Tags, never string checks; one source of truth per type.
- Code-Style: `narrative=True` is declared, "not an inference from the prose or source name"; presentation components do not own production rules.
- QST-0021:63: Venustas does not import Atlas domain code.
- QST-0077 (Solved): the ratified reading order, seven slots.

**A good answer must satisfy.**
1. One Chip model and one Entry model, shared by Player and NonPlayer.
2. No section decided by reading a string.
3. A number printed at level 20 is the level-20 number (the Intimidating Presence lesson).
4. The same Entries can print as a player sheet and as a stat block.
5. Same seed, same sheet.
6. It can land in small steps, each green.

**Out of scope.** The NPC half of the work (parked by Decree 0004; designed here, verified later). Replacing the string copies of Tags (`species`, `char_class` …) and the caches that only `to_dict` reads.

---

## 🔎 What the code does today (evidence)

Measured on 2026-09-23 against TagKit 0.2.0a1. **(V)** marks a fact checked directly while writing this Dialog; the rest were measured by the panel, which cites path:line for each.

**Chips and Entries.**
- **(V)** Two copies of Chip and Entry exist: `AtlasVenustas/VenustasKit.py` and `AtlasVenustas/Scriba.py`. Nothing in the repository references `VenustasKit.py`.
- Both are `str` subclasses that build their HTML once, in `__new__`. If an attribute changes later, the HTML does not follow. A Chip given a function as its value stores the text `<function …>` in its HTML (`Scriba.py:583-613`).
- At least nine Chip-like or Entry-like shapes feed the sheet: the Scriba Chip and Entry, `FeaturesKit.Feature`, three legacy `Grimoire_of_Features` classes, the NPC `Chip_Spec` / `Chip_Grant` / `Feature_Grant`, plain tuples, and hard-coded stat chips.
- Chips are mostly tuples: 284 tuples against 10 Chip objects at runtime. The tuple order is `(label, value, symbol)`; Chip's is `(symbol, label, value)`.
- **(V)** On the seed-5, level-20 Sorcerer the rendered rail shows **Sorcery Points twice**. Three producers feed the rail (stat chips, feature chips, spellcaster chips) and nothing shares a key.
- The Scriba `kind` field was meant "for sheet placement" (`Scriba.py:15-16`). Nothing reads it.

**Placement.**
- **(V)** `app/components/character_sheet.py:244-262` decides a feature's section by the first characters of its `source` string (`_SOURCE_PLACES`).
- **(V)** Over seeds 1 to 8 at levels 1, 5, 11 and 20: **55 of 595 features (9.2%)** match no prefix. All 55 have `source=None`. They fall silently into the Class "Level features" bucket. (The panel's wider run: 204 of 2028, 10.1%.)
- The sheet has about 22 decision points for placement and order. None reads a Tag or an enum.
- The data already knows where things came from: the training ledger records `Provenance(source="Guild", locator="Bard")`. The sheet ignores it and guesses from strings, which is why a Bard's instruments print under the Background.

**State on the Character ("flags").**
- **(V)** The seed-42, level-5 Paladin carries 54 instance attributes.
- Census of 540 characters: 185 distinct attribute names, only 7 of them root fields under Decree 0002. **107 of 185 (58%) are never read by production code.**
- 24 per-feature families (`adrenaline_rush_*`, `stonecunning_*` …) hold 108 attributes. 78 of them copy a constant the Tag already declares: `char.Adrenaline_Rush.ACTION` equals `char.adrenaline_rush_action`.
- Literal True/False flags are rare: 15 observed, all fixed per Tag, 14 never read.

**The NPC side.**
- The NPC tactical path already works the way Julio describes: a catalogue entry becomes a Tag (the flag) that files one frozen `Feature_Grant` (the Entry) and optional `Chip_Grant`s, each with a stable `key`. The NPC sheet groups them by **activation** (Trait, Action, Bonus Action, Reaction), like a 5e stat block.
- The player sheet groups by **origin** (Species, Background, Class). Fed NPC grants, it put all of them in Other.

**Reproducibility.**
- **(V)** `summon_player(seed=42, level=5)` gives four different second languages under four `PYTHONHASHSEED` values (Common Sign Language, Orc, Halfling, Elvish). Cause: `lang_set.pop()` on a `set` at `AtlasLudus/Map_of_Languages.py:1333`. The replay rite does not catch it, because it compares two summons in one process.

**TagKit 0.2.0a1.**
- Tag membership (`char in Tag`, `Has`, `isinstance` for history) is already a complete flag system. A Tag with no body is a marker.
- TagKit has no way to collect data from every Tag on a target, and no sections or order. Public, frozen, non-callable class data on a Tag is a Report; a bare callable placed there becomes an Action.
- One flat namespace per Character: a second Record with the same name overwrites the first without warning.
- On the Paladin, 31 of 47 active Tags declare no entry, and 4 of 18 entries have no Tag of the same name. The relation is 0..n both ways.

---

## 🗣️ Deliberation

*Held as an agent panel, not a council. Six readers mapped the ground (inventory, render paths, TagKit, the state census, the design record, the NPC side). Three designers each built one design against ten required cases. Three judges scored all three, each through one lens.*

### The three designs

**A. Rail and Book (Julio's proposal, as strong as it can be made).** The root gains a `Chip_Rail` (ordered, keyed) and an `Entry_Book` (`{Section: tuple[Entry]}` over Species, Background, Guild, Proficiencies, Spells, Others). Tags fill both through one grant function. Values are functions read once after generation. Venustas prints.

**B. Projection (Tags declare, the sheet reads).** The root stays as Decree 0002 defines it. Each Tag declares its Chips and Entries as frozen recipes (Reports). A sheet walks the Character's active Tags, collects their declarations, reads them, and hands them to a layout in Venustas. Nothing about the sheet is stored.

**C. Facets (one grant ledger, many layouts).** The root gains one append-only `Grant_Ledger` of frozen Entry records, beside `training`. Each Entry carries its Chips and three typed facets: **origin** (who granted it), **kind** (what it is), **activation** (when it is used). Layouts in Venustas are declarative: "group by origin in this order", or "group by activation".

### The judges

| Lens | A | B | C | Winner |
|---|---|---|---|---|
| Principles and Canon | 5 | **8** | 6.5 | B |
| Correctness and failure modes | 6 | 6 | **7** | C |
| Migration cost and risk | 4.5 | 6 | **7.5** | C |

**All three judges found the same structural flaw in A.** Its stored dictionary mixes two axes. Species, Background and Guild say **who** granted an entry; Proficiencies and Spells say **what** it is. A Tiefling's legacy cantrip is both a Species grant and a Spell, so under A its author must choose a shelf, for every layout that will ever exist. The NPC stat block wants a third axis (activation) and would need a second dictionary. And because the section is stamped on every grant, any re-ruling of the sheet order means editing hundreds of grant sites instead of one line of a layout.

**All three judges also agreed on the formula.** It is true of a **Tag**, not of the Character, and it is off by one term:
- **Flags** need no store. Tag membership already is the flag.
- **Chips** are not a separate list. Each Chip belongs to an Entry (Feature-Text: a chip with no prose is a record). A separate rail list would be a fourth rail producer, beside the three that already print Sorcery Points twice.
- **Decisions** are missing. Choices drawn once from a named Dice Bag (weapon masteries, a Tiefling's spellcasting ability) are Records the Entry text reads.

**Where the judges split: store the grants (C) or derive them (B)?**
- *For B (the Principles judge):* a stored ledger can be rebuilt from membership plus declarations, so under Decree 0002 §3 it is a cache. It also outlives a Rip, so after one it disagrees with membership.
- *For C (the Correctness and Migration judges):*
  - About a quarter of today's entries have no Tag to declare them: ASI feats, Fighting Style picks, Invocations. B needs those turned into late-applied Tags, and each late Tag re-runs every visible Precondition (about 5.6 ms on the finished Paladin, measured on 0.2.0a1). *(Corrected 2026-09-24: the panel also said TagKit forbids applying a Tag inside an Imprint. That is true only of the pinned 0.2.0a1. Upstream removed the guard in 0.2.0a2, and TopKit 0.2.0a3 and 0.2.0a4 allow it, verified by running a Fighter Imprint that applies a Fighting Style.)*
  - B's walk depends on TagKit internals on 0.2.0a1 (flattening `Forms()`, reading `__dict__`, unwrapping `Report`), and the a3 pin rewrites Report declarations. *(Corrected 2026-09-24: TopKit's public `Tags(agent)` now returns the active leaf Tags in application order, so the walk no longer needs the internals. Reading each Tag's own declarations may still need care.)*
  - Per-character content (Magic Initiate's chosen spells) is a decision, not a derivation.
  - The `training` ledger is the ratified precedent: *"the ledger is the writer, the sheet its projection"* (Dialog 0025).

**The synthesis takes C and grafts B's answers to its two weak points.**
1. The ledger holds **recipes** (the Entry with its reading functions), never resolved numbers or HTML. It records what was granted, not what it says, so it cannot drift like a stored skill.
2. At read time, only grants whose Tag the Character still carries are shown (`character in entry.grantor`). A Rip drops them from the sheet; the ledger keeps the history.

---

## ✅ Convergence check

- [x] Every required case answered with a mechanism: late-level drift, Species spells, player sheet vs stat block, unknown section, duplicates, one number for rule and Chip, several output formats, reproducibility, adding a Species or Guild, the attribute sprawl.
- [x] Every objection answered or carried to Julio as a ruling (R1 is the B-versus-C split).
- [x] A concrete proposal with a code sketch is on the table.

---

## 🕊️ Vox report

Vox: The panel agrees with Julio's direction and changes three details of its shape.

### Common ground (Julio was right)

1. **There is a shared core.** The Dice are already on it (Decree 0002 §4). Grants belong beside them.
2. **Chip and Entry must be designed objects.** Nine shapes, a swapped argument order and two copies of the same class show what happens without one.
3. **Order and visual difference belong to the visual package.** The sheet should never infer a section from a string.
4. **The pattern repeats.** Every Tag contributes the same three kinds of thing, and the NPC path already proves it.

### The three changes

1. **Chips live inside Entries.** One store, not two. The rail is every Chip of the placed Entries, in section order. Vitals (AC, HP, Speed …) become chip-only Entries, which Feature-Text already calls records.
2. **The dictionary of sections is a layout, built when printing.** Each Entry stores its facts (origin, kind, activation, level). A layout says which facet makes the headings. The player sheet groups by origin, the stat block by activation, from the same Entries.
3. **The objects do not print themselves.** Chip and Entry are plain frozen records in the model. Printer functions in Venustas turn them into HTML, Markdown or plain text. Printing on the object is what baked `<function …>` into today's Chip.

### The proposed algebra

```
Tag       = membership (the flag)  +  decisions (Records)  +  0..n Entries
Entry     = facts (key, title, text, origin, kind, activation, level)  +  0..n Chips
Character = Dice  +  training ledger  +  grant ledger
Sheet     = Print( Place( Find_Sheet( character ), layout ), form )
```

Operators, kept few on purpose:
- `ledger + entry` grants. The same Entry twice is a no-op. A Shape refines what its Base granted (Orc Darkvision over Darkvision). Two unrelated grantors of one key raise `Grant_Conflict`, naming both.
- `ledger[ query ]` selects.
- `key in ledger` asks.
- `&`, `|`, `~` build facet queries, and only inside layouts: `Origin.SPECIES & ~Kind.SPELL`.

A grouping operator (`ledger | Origin`) was considered and refused: `|` already means "or" inside queries. Grouping is the named function `Place`.

### Code sketch

Illustrative, not final spelling. Module names follow the Conventions taxonomy: `Compass_of_` holds types, `Charts_of_` holds algorithms, `Lodge_of_` holds curated closed sets.

```python
#-- AtlasActorLudi/Compass_of_Grants.py : the shared vocabulary.  Model only: no HTML, no Venustas.

class Origin( Facet ):
	"""Who granted it."""
	SPECIES = "Species"
	BACKGROUND = "Background"
	ORDER = "Secret Order"
	GUILD = "Guild"
	FEAT = "Feat"
	ROLE = "Role"
	UNPLACED = "Unplaced"
		#-- The legacy adapter only.  Its count must fall to zero.

class Kind( Facet ):
	"""What it is."""
	STORY = "Story"
	TRAIT = "Trait"
	FEAT = "Feat"
	INVOCATION = "Invocation"
	PROFICIENCY = "Proficiency"
	SPELL = "Spell"
	STATISTIC = "Statistic"

class Activation( Facet ):
	"""When it is used.  Moved up from the NPC side."""
	ACTION = "Action"
	BONUS_ACTION = "Bonus Action"
	REACTION = "Reaction"


@dataclass( frozen=True, slots=True, kw_only=True )
class Chip:
	"""One lookup for the rail: one label, one value."""
	key: str
	label: str
	value: object
		#-- A literal, or a named pure function of the Character.
	symbol: str = ""


@dataclass( frozen=True, slots=True, kw_only=True )
class Entry:
	"""One thing a Character was granted."""
	key: str
	title: str
	text: object = ""
	origin: Origin
	kind: Kind
	level: int
	activation: tuple = ()
		#-- Empty means "not declared".  Never a guess such as Passive.
	chips: tuple = ()
	narrative: bool = False
	grantor: type | None = None
		#-- The Tag class.  Stamped by Grant, never typed by an author.


@dataclass( frozen=True, slots=True )
class Grant_Ledger:
	"""Every Entry a Character was granted, in the order granted."""
	entries: tuple = ()

	def __add__(
			ledger,
			entry: Entry,
			) -> "Grant_Ledger":
		held = ledger.Find( entry.key )
		if held is None:
			return ledger.Appended( entry )
		if held == entry:
			return ledger
				#-- The same grant twice changes nothing.
		if issubclass( entry.grantor, held.grantor ):
			return ledger.Replaced( held, entry )
				#-- A Shape refines what its Base granted.
		raise Grant_Conflict(
				key=entry.key,
				first=held.grantor,
				second=entry.grantor,
				)

	def __getitem__(
			ledger,
			query,
			) -> tuple:
		return tuple(
				entry
				for entry in ledger.entries
				if query.Holds( entry )
				)
```

```python
#-- AtlasActorLudi/SpeciesKit/Orcs/traits.py : a Tag declares its Entry once, and grants it in one line.

def Adrenaline_Rush_Uses(
		character,
		) -> int:
	"""The one source of this number.  The rule and the Chip both call it."""
	return Proficiency_Bonus( character.level )

def Adrenaline_Rush_Text(
		character,
		) -> str:
	uses = Adrenaline_Rush_Uses( character )
	return f"Dash as a Bonus Action and gain Temporary Hit Points, {uses} times per Short or Long Rest."

class Adrenaline_Rush( Trait ):
	ENTRY = Entry(
			key="adrenaline_rush",
			title="Adrenaline Rush",
			text=Adrenaline_Rush_Text,
			origin=Origin.SPECIES,
			kind=Kind.TRAIT,
			level=1,
			activation=( Activation.BONUS_ACTION, ),
			chips=(
					Chip(
							key="adrenaline_rush_uses",
							label="Adrenaline Rush",
							value=Adrenaline_Rush_Uses,
							symbol="💨",
							),
					),
			)
		#-- Frozen and not callable, so TagKit keeps it a Report, never an Action.

	@Imprint
	def Grant_Adrenaline_Rush(
			target,
			):
		Grant(
				target,
				Adrenaline_Rush.ENTRY,
				grantor=Adrenaline_Rush,
				)
```

```python
#-- AtlasActorLudi/Charts_of_Grants.py : the one writer and the one reader.

def Grant(
		character,
		entry: Entry,
		*,
		grantor: type,
		) -> Entry:
	"""The only writer of character.grants."""
	stamped = replace(
			entry,
			grantor=grantor,
			)
	character.grants = character.grants + stamped
	return stamped

def Find_Sheet(
		character,
		) -> tuple:
	"""Read every live grant once.  Changes nothing on the Character."""
	before = Fingerprint( character )
	live = Live_Grants( character )
		#-- Only grants whose Tag the Character still carries.
	read = tuple(
			Read_Entry( entry, character )
			for entry in live
			)
	Refuse_Change(
			before,
			Fingerprint( character ),
			)
		#-- Dice state, Pick counters, app.random, attribute names.  Raises Impure_Reading.
	return read
```

```python
#-- AtlasVenustas/Lodge_of_Layouts.py : which facet makes the headings.

LISTED = Kind.SPELL | Kind.PROFICIENCY | Kind.STATISTIC
	#-- Kinds with a Section of their own, whoever granted them.

PLAYER_SHEET = (
		Section( title="Vitals", claims=Kind.STATISTIC ),
		Section( title="Species", claims=Origin.SPECIES & ~LISTED ),
		Section( title="Background", claims=( Origin.BACKGROUND | Origin.ORDER ) & ~LISTED ),
		Section( title="Guild", claims=Origin.GUILD & ~LISTED ),
		Section( title="Proficiencies", claims=Kind.PROFICIENCY ),
		Section( title="Spells", claims=Kind.SPELL ),
		)
	#-- Whatever no Section claims prints under a visible "Others".  Origin.FEAT waits on ruling R3.

NPC_STAT_BLOCK = (
		Section( title="Vitals", claims=Kind.STATISTIC ),
		Section( title="Actions", claims=Activation.ACTION ),
		Section( title="Bonus Actions", claims=Activation.BONUS_ACTION ),
		Section( title="Reactions", claims=Activation.REACTION ),
		Section( title="Spellcasting", claims=Kind.SPELL ),
		)
```

```python
#-- AtlasVenustas/Scriba.py : printers.  They read the vocabulary and decide no rule.

def Print_Sheet(
		sheet: tuple,
		layout: tuple,
		form: Form,
		) -> str:
	placed = Place( sheet, layout )
	rail = Print_Rail( placed, form )
	body = Print_Sections( placed, form )
	return Join_Page( rail, body, form )
```

`Place` puts each Entry in exactly one Section. Two Sections claiming one Entry is a named error, not a silent first match. Inside a Section: narrative first, then level gained, then grant order.

### How the required cases land

| Case | Mechanism |
|---|---|
| A capstone changes a number an earlier Entry prints | Entry text and Chip values are named functions, read once after generation (`Find_Sheet`). The level-20 sheet reads level-20 Strength. |
| A Species grants a spell | `origin=SPECIES, kind=SPELL`. The layout decides: the player sheet lists it under Spells (sub-grouped by origin if wanted); a Species-lore layout could show it under Species. One grant, no duplicate. |
| Player sheet vs stat block | Two layouts over the same read Entries. |
| An Entry with no known section | Cannot be built: `origin`, `kind` and `level` are required. Legacy objects pass through a read-time adapter as `Origin.UNPLACED` and print under a visible "Others", with a count the migration drives to zero. |
| The same grant twice | `ledger + entry` is a no-op for an equal Entry; a Shape refines its Base; unrelated grantors raise, naming both. A static test checks every declared key once. |
| One number for a rule and a Chip | One named function in the Tag's own module (`Adrenaline_Rush_Uses`). The prefixed attribute copies are deleted. |
| HTML, Markdown, plain | `Print_Sheet( sheet, layout, form )`. Nothing builds HTML when a record is created. |
| Same seed, same sheet | Reading is checked pure (dice state, Pick counters, `app.random`, attribute names). A two-process gate under different `PYTHONHASHSEED` values must print the same sheet. |
| A new Species or Guild | Its own files only: the Tag declares its Entries. No sheet table to update. |
| The 54-attribute sprawl | The display families go (about 21 on the seed-42 Paladin; 108 attributes across the census). The Tag-copy strings and live mechanical facts stay for later questae. |

### Proposed order of work

Each step lands green on its own. Structural steps keep the character fingerprint identical; intended changes land alone, with the diff declared up front.

1. **Cleanups that change nothing.** Delete `AtlasVenustas/VenustasKit.py` (no references).
2. **A determinism gate before any baseline.** Replace `set.pop()` at `Map_of_Languages.py:1333` with a Dice Bag draw over a sorted list (a declared diff). Make the replay rite compare two subprocesses under different `PYTHONHASHSEED` values. Add a sheet fingerprint: section, key, read text, and chip keys with values per Entry.
3. **Wait for the a3 pin (QST-0093.5).** It rewrites Report declarations and changes Postcondition rollback. Re-verify on a3 that a frozen record on a Tag is a Report, before declaring Entries on 400 Tags.
4. **The vocabulary** (`Compass_of_Grants`, `Charts_of_Grants`), with the algebra laws as `__main__` self-tests. No callers yet.
5. **Printers, layouts, and a read-time adapter** for today's `char.features`. The new layout must reproduce today's placement exactly (a census comparison), and then the intended fixes (a visible Others, Invocations, level-0 ordering) land as one-line layout edits.
6. **First slice: Fighter's Second Wind**, the reference named in Current-State. Grant it natively; delete `second_wind_uses` and `second_wind_uses_max`.
7. **One family at a time.** Species one species per commit; Training through the `Build_Training` factory with a per-Tag opt-in; Backgrounds; Orders; Vitals. A family that grants natively stops calling `carry()` in the same commit, so no Entry is ever produced twice.
8. **Feats and Invocations get their own questa.** Wiring `FeatKit` and `InvocationKit` off `app.random` changes every character's feats.
9. **When the adapter count reaches zero**, delete the adapter, `char.features`, `_SOURCE_PLACES` and the tuple chips.

The NPC half waits for Decree 0004 to lift. Full NPC generation fails today; only `light=True` NPCs build.

### Risks the panel could not remove

- **A half-finished migration.** Two stores (`features` and `grants`) during steps 5 to 9. The read-time adapter keeps the old path rendering exactly as today if the work stalls, but every stalled week is "a paradigm half-adopted".
- **Purity is a check, not a type.** A reading function that calls `Pick` changes its answer on every read while leaving `char.dices` untouched. The fingerprint must include the Pick counters.
- **Loud failures.** Duplicates that are silent today (two Sorcery Points chips) become errors. During the bridge they are reported through Minion, not raised, until the census count is zero.
- **Compound activations.** Bastion, or Adrenaline Rush's Dash, has more than one activation. `activation` is a tuple; a stat block places by the first.
- **Speed and other shared numbers.** Several contributors to one number (a Species sets speed, the Monk adds to it) need one aggregating function and one Chip, not several Chips.

---

## ⚖️ Rulings needed from Julio

**R1. Store the grants, or derive them?**
- *Proposal:* amend Decree 0002 §2 to add `grants` beside `dices`. The root already carries `training` the same way.
- *Alternative:* keep the root as ratified and derive every sheet by walking Tags (Design B). This is purer. On 0.2.0a1 it needed choice Tags applied late and TagKit internals. TopKit (0.2.0a2 onward) removes both obstacles: an Imprint may apply a choice Tag, and `Tags(agent)` lists active Tags in order. What remains against B is the cost of Preconditions re-run per Tag (unmeasured on TopKit) and per-character content such as chosen spells. **After the a3 pin, R1 is closer than the panel scored it, and should be re-judged on TopKit before it is ruled.**

**R2. Where does the vocabulary live?**
- *Proposal:* a domain-owned, types-only `Compass_of_Grants` that Venustas may import, as a narrow exception to QST-0021:63.
- *Alternative:* keep the printers in `app/components/`, which ties Markdown export to Shiny.

**R3. The section list against QST-0077.** Julio's list differs from the ratified seven slots:
- It has no Equipment and no Backstory. The proposal keeps both as fixed layout blocks after Spells.
- It renames slot 7 "Magic / Focus / Special Resource" to "Spells". That would settle QST-0078 without saying so.
- It adds "Others". The proposal says yes: a visible Others.
- It has no home for Feats (ASI feats, Epic Boons). The options are their own section, or placing them under Guild.
- The live renderer also nests tools under Background and spells under Class. No questa records that change. Is it intended?

**R4. Sequence after the a3 pin?** The proposal says yes: steps 1 and 2 now, the rest after QST-0093.5.

**R5. What does "flags" mean to you?** The panel read it as Tag membership, which needs no store. If you meant something else, such as conditions or statuses that change during play, those are TagKit Records, and this Dialog should say so.

→ Awaiting Julio's decision. To be recorded as a Decree amending Decree 0002 (if R1 is taken), with a Questa under QST-0020 and QST-0016.
