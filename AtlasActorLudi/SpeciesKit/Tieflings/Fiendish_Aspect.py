"""
Fiendish Aspect — how a Tiefling's blood shows, made by a collapse.

The aspect is a wave of ten slots: a structure (the order the sentences come
in) and nine parts of the look.  Each part's candidates are the marks the
blood's legacies lend (``Map_of_Marks``); the collapse (``SpeciesKit.collapse``)
fills the most constrained slot first, with the Character's own dice, and
three rules narrow the rest as it goes:

1. **No word twice.**  Two marks sharing a key never sit in one aspect: no
   gold iris under a gold sheen, no red fur marked with red.
2. **The pattern and its second colour agree.**  A two-colour pattern needs an
   accent; a one-colour pattern forbids one; and the other way round.
3. **A mixed blood shows both legacies.**  When only one slot could still show
   the legacy nothing has shown yet, that slot must show it.

The hells stay hidden.  The page never describes one; it only suggests where
the bloodline starts, naming the legacy that lent the most of the look (the
Heritage, on a tie).  That the blood is two legacies is structure, like the
Aasimar's two Ideals, and never said.

How it is *said* is a second draw: each sentence of the chosen structure is a
symbol of a generative grammar (``Grammar_of_Aspect``, on
``SpeciesKit.grammar``), rewritten once with the Character's dice, the marks
slotted in as its lexicon.  The sentences are kept, so reading never rolls.

Nothing here is mechanical.  Fiendish Legacy carries the rules; this carries
the aspect.
"""

from __future__ import annotations

from dataclasses import dataclass

from AtlasActorLudi.SpeciesKit.collapse import ABSENT
from AtlasActorLudi.SpeciesKit.collapse import Collapse
from AtlasActorLudi.SpeciesKit.collapse import Slot
from AtlasActorLudi.SpeciesKit.grammar import Derive
from AtlasActorLudi.SpeciesKit.Tieflings.Grammar_of_Aspect import GRAMMAR
from AtlasActorLudi.SpeciesKit.Tieflings.Map_of_Marks import ROSTER
	#-- Importing the map is what fills the Pins below with marks.
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Coat
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Coat_Pattern
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Eyes
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Horn_Material
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Horn_Shape
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Marks_Of
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Scent
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Sheen
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Structure
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Tail


if not ROSTER:
	raise ImportError(
			"Fiendish_Aspect: the Map of Marks declared no marks."
			)


# The slots that are parts of the look, and the part each draws from.  The
# accent is a second coat colour, so it draws from Coat too.
LOOK_SLOTS = (
		( "horn_shape", Horn_Shape ),
		( "horn_material", Horn_Material ),
		( "eyes", Eyes ),
		( "coat", Coat ),
		( "pattern", Coat_Pattern ),
		( "accent", Coat ),
		( "sheen", Sheen ),
		( "scent", Scent ),
		( "tail", Tail ),
		)


@dataclass(
		frozen=True,
		)
class Fiendish_Aspect:
	"""One Tiefling's look, collapsed once and kept, with the words it is said in."""

	structure: type
	horn_shape: type
	horn_material: type
	eyes: type
	coat: type
	pattern: type
	accent: object
		#-- A coat mark, or ABSENT for a one-colour pattern.
	sheen: type
	scent: type
	tail: object
		#-- A tail mark, or ABSENT.
	# The legacy the looks suggest, named and never described.
	suggested: type
	# The structure's sentences, derived once by the grammar.
	sentences: tuple[str, ...]

	def paragraph(
			self,
			) -> str:
		return " ".join( self.sentences )


# ---------------------------------------------------------------------------
# Who lends what.
# ---------------------------------------------------------------------------

def _lent_by_blood(
		mark,
		legacies,
		) -> tuple:
	"""The legacies of this blood that lend the mark (none for ABSENT)."""
	if mark is ABSENT:
		return ()
	return tuple(
			legacy
			for legacy in legacies
			if mark in legacy.MARKS
			)


def _shows(
		mark,
		legacies,
		):
	"""
	The one legacy a mark shows, or None.

	A mark lent by both legacies of a mixed blood (a plain pattern) shows
	neither: it could have come from either.
	"""
	lenders = _lent_by_blood(
			mark,
			legacies,
			)
	if len( lenders ) == 1:
		return lenders[0]
	return None


def _keys(
		mark,
		) -> tuple[str, ...]:
	if mark is ABSENT:
		return ()
	return mark.KEYS


def _is_two_colour(
		pattern,
		) -> bool:
	"""A pattern that names a second colour in its template."""
	return "{b}" in pattern.TEXT


# ---------------------------------------------------------------------------
# The slots and their first candidates.
# ---------------------------------------------------------------------------

def _lent_marks(
		part,
		legacies,
		) -> tuple:
	return tuple(
			mark
			for mark in Marks_Of( part )
			if _lent_by_blood(
					mark,
					legacies,
					)
			)


def _some_legacy_lends_none(
		part,
		legacies,
		) -> bool:
	return any(
			not any(
					mark in legacy.MARKS
					for mark in Marks_Of( part )
					)
			for legacy in legacies
			)


def _candidates(
		name: str,
		part,
		legacies,
		) -> tuple:
	marks = _lent_marks(
			part,
			legacies,
			)
	if name == "accent":
		return ( *marks, ABSENT )
	if name == "tail" and _some_legacy_lends_none(
			part,
			legacies,
			):
		return ( *marks, ABSENT )
	return marks


def _slots(
		legacies,
		) -> tuple[Slot, ...]:
	structure = Slot(
			"structure",
			Marks_Of( Structure ),
			)
	look = tuple(
			Slot(
					name,
					_candidates(
							name,
							part,
							legacies,
							),
					)
			for name, part in LOOK_SLOTS
			)
	return ( structure, *look )


# ---------------------------------------------------------------------------
# The three rules.
# ---------------------------------------------------------------------------

def _narrow(
		domains,
		name: str,
		keep,
		):
	"""The domains with one slot narrowed to the candidates ``keep`` accepts."""
	narrowed = dict( domains )
	narrowed[name] = tuple(
			candidate
			for candidate in domains[name]
			if keep( candidate )
			)
	return narrowed


def _no_word_twice(
		drawn,
		domains,
		):
	"""Rule 1: an open slot loses every candidate sharing a key with a drawn mark."""
	used = {
			key
			for mark in drawn.values()
			for key in _keys( mark )
			}
	for name in domains:
		if name in drawn:
			continue
		domains = _narrow(
				domains,
				name,
				lambda candidate: not set( _keys( candidate ) ) & used,
				)
	return domains


def _accent_follows_pattern(
		drawn,
		domains,
		):
	"""Rule 2: a two-colour pattern has an accent, a one-colour one has none."""
	if "pattern" in drawn and "accent" not in drawn:
		if _is_two_colour( drawn["pattern"] ):
			return _narrow(
					domains,
					"accent",
					lambda accent: accent is not ABSENT,
					)
		return _narrow(
				domains,
				"accent",
				lambda accent: accent is ABSENT,
				)
	if "accent" in drawn and "pattern" not in drawn:
		wants_two = drawn["accent"] is not ABSENT
		return _narrow(
				domains,
				"pattern",
				lambda pattern: _is_two_colour( pattern ) == wants_two,
				)
	return domains


def _contradiction(
		domains,
		):
	"""Domains the collapse will read as a contradiction (one slot emptied)."""
	emptied = dict( domains )
	first = next( iter( emptied ) )
	emptied[first] = ()
	return emptied


def _both_legacies_show(
		legacies,
		):
	"""Rule 3, for one blood: a mixed blood shows both of its legacies."""

	def rule(
			drawn,
			domains,
			):
		if len( legacies ) < 2:
			return domains
		shown = {
				_shows(
						mark,
						legacies,
						)
				for mark in drawn.values()
				}
		missing = [
				legacy
				for legacy in legacies
				if legacy not in shown
				]
		if not missing:
			return domains
		for legacy in missing:
			could_show = [
					name
					for name in domains
					if name not in drawn
					and any(
							_shows(
									candidate,
									legacies,
									) is legacy
							for candidate in domains[name]
							)
					]
			if not could_show:
				return _contradiction( domains )
			if len( could_show ) == 1:
				domains = _narrow(
						domains,
						could_show[0],
						lambda candidate, legacy=legacy: _shows(
								candidate,
								legacies,
								) is legacy,
						)
		return domains

	return rule


# ---------------------------------------------------------------------------
# The suggested origin, and the collapse itself.
# ---------------------------------------------------------------------------

def _most_shown(
		drawn,
		legacies,
		):
	"""The legacy that lent the most of the look; the Heritage on a tie."""
	counts = {
			legacy: 0
			for legacy in legacies
			}
	for mark in drawn.values():
		legacy = _shows(
				mark,
				legacies,
				)
		if legacy is not None:
			counts[legacy] += 1
	best = max( counts.values() )
	return next(
			legacy
			for legacy in legacies
			if counts[legacy] == best
			)
		#-- Legacies are in blood order, Heritage first, so it wins ties.


def _fur(
		drawn,
		) -> str:
	"""The coat, the pattern and the accent, as one phrase."""
	accent = ""
	if drawn["accent"] is not ABSENT:
		accent = drawn["accent"].TEXT
	return drawn["pattern"].TEXT.format(
			a=drawn["coat"].TEXT,
			b=accent,
			)


def _text_or_nothing(
		mark,
		) -> str:
	if mark is ABSENT:
		return ""
	return mark.TEXT


def _lexicon(
		drawn,
		suggested,
		) -> dict[str, str]:
	"""The words the grammar slots in, from the marks the collapse chose."""
	return {
			"horn_shape": drawn["horn_shape"].TEXT,
			"horn_material": drawn["horn_material"].TEXT,
			"eyes": drawn["eyes"].TEXT,
			"fur": _fur( drawn ),
			"sheen": drawn["sheen"].TEXT,
			"scent": drawn["scent"].TEXT,
			"tail": _text_or_nothing( drawn["tail"] ),
			"place": suggested.PLACE,
			}


def _open_voice_dice(
		target,
		):
	"""The Dice Bag the grammar derives the sentences with."""
	return target.Dice_Bag(
			"identity.species.Tiefling.fiendish_blood.voice",
			version="1",
			namespace="GenLegendActor",
			)


def _derive_sentences(
		target,
		structure,
		lexicon,
		) -> tuple[str, ...]:
	"""Each of the structure's sentences, derived; empty ones dropped."""
	dice = _open_voice_dice( target )
	sentences = [
			Derive(
					target,
					GRAMMAR,
					sentence,
					lexicon,
					dice,
					)
			for sentence in structure.SENTENCES
			]
	return tuple(
			sentence
			for sentence in sentences
			if sentence.strip()
			)


def _open_aspect_dice(
		target,
		):
	"""The Dice Bag the aspect is collapsed with, apart from every other."""
	return target.Dice_Bag(
			"identity.species.Tiefling.fiendish_blood.aspect",
			version="1",
			namespace="GenLegendActor",
			)


def Collapse_Aspect(
		target,
		legacies,
		) -> Fiendish_Aspect:
	"""Collapse this blood's aspect, once, with the Character's own dice."""
	drawn = Collapse(
			target,
			_slots( legacies ),
			(
					_no_word_twice,
					_accent_follows_pattern,
					_both_legacies_show( legacies ),
					),
			_open_aspect_dice( target ),
			)
	suggested = _most_shown(
			drawn,
			legacies,
			)
	sentences = _derive_sentences(
			target,
			drawn["structure"],
			_lexicon(
					drawn,
					suggested,
					),
			)
	return Fiendish_Aspect(
			structure=drawn["structure"],
			horn_shape=drawn["horn_shape"],
			horn_material=drawn["horn_material"],
			eyes=drawn["eyes"],
			coat=drawn["coat"],
			pattern=drawn["pattern"],
			accent=drawn["accent"],
			sheen=drawn["sheen"],
			scent=drawn["scent"],
			tail=drawn["tail"],
			suggested=suggested,
			sentences=sentences,
			)
