"""
What a Wizard's Spellbook physically is.

A true name cannot be held by a symbol; a mark only carries you back to one.
Nothing in that requires vellum. So the book is drawn per Character as an
extension of what they already are: a cartographer's spells are roads, a
jeweller's are stones, a cook's are recipes.

Two rules govern the pool.

**It stays losable.** The book is always an object somebody could take, burn,
soak or steal. That vulnerability is written into the Wizard's own rules, which
is why they are told to keep a spare, and a book made of memory or muscle would
quietly hand one Wizard an immunity the others pay for.

**A page is always a page.** Every form names its own unit, so the rules text
above it ("six level 1 spells", "add two spells") keeps meaning what it says
whether a page is a stone, a stave or a sheet of papyrus.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Spellbook_Form:
	"""One way a book can be. ``opening`` completes 'Your Spellbook is ...'."""

	tool: str | None
	opening: str


# Drawn when the Wizard is proficient with the tool that explains the object.
CRAFTED_FORMS: tuple[Spellbook_Form, ...] = (
	Spellbook_Form(
		"Cartographer's Tools",
		"a folded map, each road a page and every spell a way back to "
		"somewhere you have already stood",
		),
	Spellbook_Form(
		"Woodworker's Tools",
		"a ring of wooden tablets bound with cord, each tablet a page cut "
		"deep enough to read in the dark",
		),
	Spellbook_Form(
		"Weaver's Tools",
		"a long sash, each band of its border a page worked in thread",
		),
	Spellbook_Form(
		"Glassblower's Tools",
		"a string of glass beads, each bead a page with one gesture held "
		"inside it",
		),
	Spellbook_Form(
		"Jeweler's Tools",
		"a necklace of amethysts, each stone a page holding the memory of a "
		"spell as it went the first time",
		),
	Spellbook_Form(
		"Smith's Tools",
		"a sheaf of steel leaves on a ring, each leaf a page struck rather "
		"than written",
		),
	Spellbook_Form(
		"Leatherworker's Tools",
		"a leather book, each face a page tooled into the hide",
		),
	Spellbook_Form(
		"Calligrapher's Supplies",
		"a codex on good vellum, each page exactly what a page is supposed "
		"to be",
		),
	Spellbook_Form(
		"Potter's Tools",
		"a bag of fired tokens, each token a page pressed while the clay was "
		"still soft",
		),
	Spellbook_Form(
		"Mason's Tools",
		"a slate in a wooden frame, each face a page chiselled shallow",
		),
	Spellbook_Form(
		"Painter's Supplies",
		"a folding screen, each panel a page, and not one word on any of them",
		),
	Spellbook_Form(
		"Cook's Utensils",
		"a recipe book, each page a spell written as a method, and you do not "
		"find that funny",
		),
	Spellbook_Form(
		"Alchemist's Supplies",
		"a plate book of emblems, each plate a page that means more than it "
		"shows",
		),
	Spellbook_Form(
		"Herbalism Kit",
		"a bundle of papyrus interleaved with pressed leaves, each sheet a "
		"page that still smells of the field it came from",
		),
	Spellbook_Form(
		"Brewer's Supplies",
		"a ledger of batches, each entry a page, the spells filed in among "
		"the beers",
		),
	Spellbook_Form(
		"Cobbler's Tools",
		"a pair of boots, each lining a page stitched where nobody looks",
		),
	Spellbook_Form(
		"Tinker's Tools",
		"a device of sliding plates, each plate a page that lines up only "
		"one way",
		),
	Spellbook_Form(
		"Forgery Kit",
		"somebody else's book, each page a page you added without asking",
		),
	Spellbook_Form(
		"Disguise Kit",
		"a book of household accounts, each page a page nobody has ever "
		"asked to see twice",
		),
	Spellbook_Form(
		"Poisoner's Kit",
		"a case of labelled vials, each label a page, the writing very small",
		),
	Spellbook_Form(
		"Thieves' Tools",
		"a roll of tools, each pocket a page, the marks scratched inside the "
		"leather",
		),
	Spellbook_Form(
		"Woodworker's Tools",
		"a plank of open grain, each ring a page, the spell read out of "
		"grain, joint, strain and scar",
		),
	Spellbook_Form(
		"Alchemist's Supplies",
		"a book of equivalences, each page a page that costs something to "
		"turn",
		),
	Spellbook_Form(
		"Brewer's Supplies",
		"a rack of stoppered bottles, each bottle a page that is not "
		"finished fermenting",
		),
	Spellbook_Form(
		"Dragonchess Set",
		"a board and its pieces, each piece a page, the spell held in where "
		"it is allowed to go",
		),
	Spellbook_Form(
		"Playing Card Set",
		"a deck, each card a page, and you never shuffle it",
		),
	)

# Drawn alongside the crafted forms, never instead of them: a people suggests,
# it does not decide.  Keyed on race, so a Tiefling reads Fiend and an Aasimar
# reads Celestial, which is how the Character carries them.
LINEAGE_FORMS: dict[str, str] = {
	"Dwarf":
		"a ledger bound in metal, each entry a page, filed between a debt "
		"and a grudge",
	"Gnome":
		"a clockwork barrel that turns one page at a time, and only "
		"forwards",
	"Giant":
		"a stone too heavy to carry and a satchel of rubbings taken from "
		"it, each rubbing a page",
	"Orc":
		"a saddle blanket, each woven band a page, because no camp is "
		"permanent",
	"Halfling":
		"a recipe book, each page a spell written as a method, with three "
		"generations of marginalia arguing in the margins",
	"Fiend":
		"a book nobody taught you to keep, each page a page you worked out "
		"alone and in the wrong order",
	"Human":
		"a book in a dozen hands, each page a page somebody gave you",
	"Elf":
		"a book you began before you had a name, each page a page out of a "
		"century you no longer entirely remember",
	"Celestial":
		"a book of marks you did not choose, each page a page that was "
		"already there",
	"Dragon":
		"a book of proverbs, each page a page you have refused to translate",
	}


# Any Musical Instrument answers the same way: the spell as a piece to be
# played. Named apart because there are nine of them and one sentence covers
# all nine.
INSTRUMENT_FORM = Spellbook_Form(
	None,
	"a score, each stave a page, every spell written as a piece to be played",
	)

# Drawn when no proficiency explains the object. Deliberately ordinary: most
# Wizards carry a book, and the strange ones should stay strange.
PLAIN_FORMS: tuple[Spellbook_Form, ...] = (
	Spellbook_Form(
		None,
		"a codex of ninety-nine pages and one loose leaf you have never dared "
		"bind in",
		),
	Spellbook_Form(
		None,
		"a birch-bark bundle, each strip a page, curling at the edges",
		),
	Spellbook_Form(
		None,
		"a wax tablet in a wooden cover, each face a page you have written "
		"over more times than you can count",
		),
	Spellbook_Form(
		None,
		"a sheaf of palm leaves cut through and threaded on a cord, each leaf "
		"a page",
		),
	Spellbook_Form(
		None,
		"an ordinary book, water-stained along the bottom, each page a page",
		),
	)


def Character_Tools(
		char,
		) -> frozenset[str]:
	"""Every tool this Character is trained with, by its public name."""
	names = set()
	for batch in getattr(
			getattr(
				char,
				"training",
				None,
				),
			"gains",
			(),
			):
		for grant in getattr(
				batch,
				"grants",
				(),
				):
			name = getattr(
					getattr(
						grant,
						"capability",
						None,
						),
					"name",
					None,
					)
			if name:
				names.add(
					name
					)
	return frozenset(
		names
		)


def _a_language(
		char,
		) -> str:
	"""
	One language this Character actually knows, for a form that names one.

	Common is skipped when there is anything else, because a book written in
	the language everybody reads is not saying much about its writer.
	"""
	try:
		known = [
			name
			for name in char.languages.names()
			if name
			]
	except Exception:
		return "Common"
	choices = [
		name
		for name in known
		if name != "Common"
		] or known or [
		"Common",
		]
	return char.Pick(
			choices,
			dice=char.Dice_Bag(
				"wizard.spellbook.hand",
				version="1",
				namespace="GenLegendLusoris",
				),
			)


def Draw_Spellbook(
		char,
		) -> str:
	"""
	Settle what this Wizard's book is, once.

	Called from the Spellbook lesson's ``apply``, never from its Entry: an
	Entry that draws would re-draw on every read of the sheet, which is the
	Primal Order mistake recorded in Canon/Feature-Text.
	"""
	standing = getattr(
			char,
			"spellbook_form",
			None,
			)
	if standing:
		return standing

	tools = Character_Tools(
			char
			)
	pool = [
		form
		for form in CRAFTED_FORMS
		if form.tool in tools
		]
	if any(
			name.endswith(
				(
					"Flute",
					"Lute",
					"Lyre",
					"Horn",
					"Drum",
					"Viol",
					"Shawm",
					"Bagpipes",
					"Dulcimer",
					),
				)
			for name in tools
			):
		pool.append(
			INSTRUMENT_FORM
			)
	if not pool:
		pool = list(
			PLAIN_FORMS
			)

	form = char.Pick(
			pool,
			dice=char.Dice_Bag(
				"wizard.spellbook",
				version="1",
				namespace="GenLegendLusoris",
				),
			)
	char.spellbook_form = form.opening
	return form.opening
