"""
Fiendish Aspect — how a Tiefling's blood shows, made by a collapse.

The aspect is a **presentation**, not an inventory: it dwells on a few things
and says them well.  It is a wave of ten slots: a structure (which few things
are said, and in what order) and nine parts of the look.  Each part's
candidates are the marks the blood's legacies lend (``Map_of_Marks``), and
``ABSENT`` for a part left unsaid.  The collapse (``SpeciesKit.collapse``)
fills the most constrained slot first, with the Character's own dice, and four
rules narrow the rest as it goes:

1. **Say only what the structure presents.**  Once the structure is drawn,
   every part it does not say stays empty and every part it says must be
   filled; and the other way round, a part already drawn rules out the
   structures that disagree with it (a structure that says the tail is never
   drawn for a blood with no tail).
2. **No word twice.**  Two marks sharing a key never sit in one aspect: no
   gold iris under a gold sheen, no red fur marked with red.
3. **The pattern and its second colour agree.**  A two-colour pattern needs an
   accent; a one-colour pattern forbids one; and the other way round.
4. **A mixed blood shows both legacies,** in what is said.  When only one slot
   could still show the legacy nothing has shown yet, that slot must show it.

The hells stay hidden.  The page never describes one; it only repeats a
rumour of where the bloodline starts, naming one of the blood's two legacies,
drawn, whatever the look says (Julio, 2026-11-01: "It's all rumours and
heresy, and that chaos is part of the charm").  That the blood is two
legacies is structure, like the Aasimar's two Ideals, and never said.

How it is *said* is a second draw: each sentence of the structure is a symbol
of a generative grammar (``Grammar_of_Aspect``, on ``SpeciesKit.grammar``),
rewritten once with the Character's dice; the marks are its lexicon, and the
marks said on their own bring sentences of their own.  The sentences are
kept, so reading never rolls.

Nothing here is mechanical.  Fiendish Legacy carries the rules; this carries
the aspect.
"""

from __future__ import annotations

import re

from dataclasses import dataclass

from AtlasActorLudi.SpeciesKit.collapse import ABSENT
from AtlasActorLudi.SpeciesKit.collapse import Collapse
from AtlasActorLudi.SpeciesKit.collapse import Slot
from AtlasActorLudi.SpeciesKit.grammar import Derive
from AtlasActorLudi.SpeciesKit.Tieflings.Grammar_of_Aspect import GRAMMAR
from AtlasActorLudi.SpeciesKit.Tieflings.Map_of_Marks import ROSTER
	#-- Importing the map is what fills the Pins below with marks.
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Bearing
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
		( "bearing", Bearing ),
		)

# Which slots each sentence symbol says.  A structure says the slots of the
# symbols in its sentences, and no others.
SLOTS_SAID_BY = {
		"HORNS": ( "horn_shape", "horn_material" ),
		"EYES": ( "eyes", ),
		"FUR": ( "coat", "pattern", "accent", "sheen" ),
		"TAIL": ( "tail", ),
		"SCENT": ( "scent", ),
		"BEARING": ( "bearing", ),
		"CLOSE": (),
		"PLACE": (),
		"PLACE_OPENING": (),
		}

# Slots that may stay empty even when said: the accent of a one-colour coat.
EMPTY_WHEN_SAID = ( "accent", )

# Lexical items the grammar leaves in place for the naming pass to fill: the
# aspect is drawn before the Character has a name.  Only {full_name}: {name}
# is unsafe for Tieflings until #124 (Name_Slots and titles) is settled.  When
# #124 lands, revisit this tuple; the grammar self-test fails on any kept item
# that no production uses.
KEPT_FOR_NAMING = ( "full_name", )

_SYMBOL = re.compile(
		r"\{([A-Z_]+)\}"
		)


@dataclass(
		frozen=True,
		)
class Fiendish_Aspect:
	"""One Tiefling's look, collapsed once and kept, with the words it is said in."""

	structure: type
	# Each part is a mark, or ABSENT when this presentation does not say it.
	horn_shape: object
	horn_material: object
	eyes: object
	coat: object
	pattern: object
	accent: object
	sheen: object
	scent: object
	tail: object
	bearing: object
	# The legacy the rumour names: one of the blood's two, never described.
	suggested: type
	# The structure's sentences, derived once by the grammar.
	sentences: tuple[str, ...]

	def paragraph(
			self,
			) -> str:
		return " ".join( self.sentences )


# ---------------------------------------------------------------------------
# Who lends what, and what a structure says.
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


def Slots_Said(
		structure,
		) -> tuple[str, ...]:
	"""The look slots a structure says, read from its sentence symbols."""
	said = []
	for sentence in structure.SENTENCES:
		for symbol in _SYMBOL.findall( sentence ):
			said.extend( SLOTS_SAID_BY[symbol] )
	return tuple( said )


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
					(
							*_lent_marks(
									part,
									legacies,
									),
							ABSENT,
							),
					)
			for name, part in LOOK_SLOTS
			)
	return ( structure, *look )


# ---------------------------------------------------------------------------
# The four rules.
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


def _fits(
		structure,
		name: str,
		value,
		) -> bool:
	"""Whether a value of a look slot agrees with what the structure says."""
	said = name in Slots_Said( structure )
	if not said:
		return value is ABSENT
	if name in EMPTY_WHEN_SAID:
		return True
	return value is not ABSENT


def _say_only_what_is_presented(
		drawn,
		domains,
		):
	"""Rule 1: the structure and the look slots agree on what is said."""
	look = [
			name
			for name, _part in LOOK_SLOTS
			]
	if "structure" in drawn:
		structure = drawn["structure"]
		for name in look:
			if name in drawn:
				continue
			domains = _narrow(
					domains,
					name,
					lambda value, name=name: _fits(
							structure,
							name,
							value,
							),
					)
		return domains

	def could_say(
			structure,
			) -> bool:
		return all(
				any(
						_fits(
								structure,
								name,
								value,
								)
						for value in domains[name]
						)
				for name in look
				)

	return _narrow(
			domains,
			"structure",
			could_say,
			)


def _no_word_twice(
		drawn,
		domains,
		):
	"""Rule 2: an open slot loses every candidate sharing a key with a drawn mark."""
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
	"""Rule 3: a two-colour pattern has an accent, a one-colour one has none."""
	pattern = drawn.get(
			"pattern",
			ABSENT,
			)
	if pattern is not ABSENT and "accent" not in drawn:
		if _is_two_colour( pattern ):
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
		if drawn["accent"] is ABSENT:
			return _narrow(
					domains,
					"pattern",
					lambda pattern: pattern is ABSENT or not _is_two_colour( pattern ),
					)
		return _narrow(
				domains,
				"pattern",
				lambda pattern: pattern is not ABSENT and _is_two_colour( pattern ),
				)
	return domains


def _contradiction(
		domains,
		):
	"""
	Domains the collapse will read as a contradiction: the structure emptied.

	Which slot is emptied does not change what happens next: any empty slot
	sends the whole wave back to its first state, drawing on from the same
	dice.  The structure is named because it is what failed: the presentation
	drawn so far cannot show both legacies.  The collapse's error names this
	slot and this rule, if it never recovers.
	"""
	emptied = dict( domains )
	emptied["structure"] = ()
	return emptied


def _both_legacies_show(
		legacies,
		):
	"""Rule 4, for one blood: a mixed blood shows both of its legacies."""

	def both_legacies_show(
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

	return both_legacies_show


# ---------------------------------------------------------------------------
# The rumoured origin, the words, and the collapse itself.
# ---------------------------------------------------------------------------

def _draw_rumour(
		target,
		legacies,
		):
	"""
	Which of the blood's legacies the rumours name, drawn on its own dice.

	Not the one that shows most: a Tiefling who looks demonic may still be
	whispered to come from Hades itself.  Within the blood's two hells,
	anything goes.
	"""
	return target.Pick(
			list( legacies ),
			dice=target.Dice_Bag(
					"identity.species.Tiefling.fiendish_blood.rumour",
					version="1",
					namespace="GenLegendActor",
					),
			)


def _text_or_nothing(
		mark,
		):
	if mark is ABSENT:
		return ""
	return mark.TEXT


def _fur(
		drawn,
		) -> str:
	"""The coat, the pattern and the accent, as one phrase (nothing if unsaid)."""
	if drawn["pattern"] is ABSENT:
		return ""
	return drawn["pattern"].TEXT.format(
			a=_text_or_nothing( drawn["coat"] ),
			b=_text_or_nothing( drawn["accent"] ),
			)


def _phrase_or_nothing(
		mark,
		) -> str:
	if mark is ABSENT:
		return ""
	return mark.PHRASE


# _capitalised and _lowered change only the first character, so they assume
# every text they touch opens on a plain ASCII letter (no quote, no ellipsis,
# no accented capital).  The marks self-test enforces it for every clause and
# phrase a horn shape, eyes, scent, tail or bearing brings.

def _capitalised(
		text,
		):
	"""The same words, opening a sentence (each realisation, for a tuple)."""
	if isinstance( text, tuple ):
		return tuple(
				_capitalised( one )
				for one in text
				)
	if not text:
		return text
	return text[0].upper() + text[1:]


def _lowered(
		text,
		):
	"""The same words, inside a sentence (each realisation, for a tuple)."""
	if isinstance( text, tuple ):
		return tuple(
				_lowered( one )
				for one in text
				)
	if not text:
		return text
	return text[0].lower() + text[1:]


def _omen_or_nothing(
		mark,
		) -> str:
	if mark is ABSENT:
		return ""
	return mark.OMEN


def _lexicon(
		drawn,
		suggested,
		) -> dict:
	"""The words the grammar slots in, from the marks the collapse chose."""
	return {
			"horns": _text_or_nothing( drawn["horn_shape"] ),
			"horn_phrase": _phrase_or_nothing( drawn["horn_shape"] ),
			"horn_phrase_cap": _capitalised(
					_phrase_or_nothing( drawn["horn_shape"] ),
					),
			"horn_material": _text_or_nothing( drawn["horn_material"] ),
			"eyes": _text_or_nothing( drawn["eyes"] ),
			"eyes_phrase": _phrase_or_nothing( drawn["eyes"] ),
			"eyes_phrase_cap": _capitalised(
					_phrase_or_nothing( drawn["eyes"] ),
					),
			"fur": _fur( drawn ),
			"sheen": _text_or_nothing( drawn["sheen"] ),
			"scent": _text_or_nothing( drawn["scent"] ),
			"scent_phrase": _phrase_or_nothing( drawn["scent"] ),
			"omen": _omen_or_nothing( drawn["scent"] ),
			"tail": _text_or_nothing( drawn["tail"] ),
			"tail_lc": _lowered(
					_text_or_nothing( drawn["tail"] ),
					),
			"bearing": _text_or_nothing( drawn["bearing"] ),
			"bearing_lc": _lowered(
					_text_or_nothing( drawn["bearing"] ),
					),
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
					keep=KEPT_FOR_NAMING,
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
					_say_only_what_is_presented,
					_no_word_twice,
					_accent_follows_pattern,
					_both_legacies_show( legacies ),
					),
			_open_aspect_dice( target ),
			)
	suggested = _draw_rumour(
			target,
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
			bearing=drawn["bearing"],
			suggested=suggested,
			sentences=sentences,
			)
