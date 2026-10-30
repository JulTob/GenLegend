"""
Fiendish Blood — which hells a Tiefling carries, and how they show.

Every Tiefling has one Heritage Tag (Abyssal, Chthonic or Infernal), and that
Tag keeps every rule it carries today.  The blood is the face: a second legacy
is drawn from the whole list at uniform random, and the same legacy may come up
twice.  That is a pure blood, neither rarer nor commoner than any particular
pair, which is the Aasimar's rule for its two Ideals (``Map_of_Ideals``).

A mixed blood splits across three parts, drawn apart:

- the **horns** come from one of the two legacies,
- the **eyes** come from one of the two, drawn on their own,
- the **fur** takes a colour from each, woven by one of the patterns below.

A tail shows when either legacy carries one.  Each legacy keeps its own face
as plain class data on its Tag (``ORIGIN``, ``HORNS``, ``EYES``, ``FUR``,
``TAIL``); this module only draws and composes, and it reads nothing else.

A mixed blood also mixes the **legacy spells** (QST-0152, a house rule).  The
three spells arrive at levels 1, 3 and 5 as before, and each of the three
places is lent by one of the two legacies, by one of the patterns in
``SPELL_WEAVES``.  Every pattern there uses both legacies, so a mixed blood
always casts from both hells.  A pure blood keeps its legacy's three spells.
The Resistance stays the Heritage's.

The draw happens once, in the Heritage's Imprint, from one named Dice Bag that
does not depend on the level, so a level-up never hands anybody a different
face.  Reading the blood afterwards never rolls.

The face is drawn from one Dice Bag and the spells from another, so either can
change without moving the other.
"""

from __future__ import annotations

from dataclasses import dataclass


# How two colours share one coat.  {a} is the first legacy's colour, {b} the
# second's; the draw picks the arrangement.
FUR_WEAVES = (
	"{a}, spotted with {b}",
	"{a}, striped with {b}",
	"{a}, fading to {b} at the ends",
	"{a} along your back, and {b} beneath",
	"{a}, with a mask of {b} around your eyes",
	"{a}, with a line of {b} down your spine",
	)

# And how one colour wears the coat alone.
SINGLE_FUR_WEAVES = (
	"{a}",
	"{a}, darker along your back",
	"{a}, paler beneath",
	)

# Which legacy lends each of the three spells, by place: the level 1 cantrip,
# the level 3 spell, the level 5 spell.  0 is the Heritage and 1 the second
# legacy.  These are the six patterns that use both; the two that use only
# one legacy are left out on purpose, so a mixed blood always shows in its
# magic.
SPELL_WEAVES = (
	( 0, 0, 1 ),
	( 0, 1, 0 ),
	( 0, 1, 1 ),
	( 1, 0, 0 ),
	( 1, 0, 1 ),
	( 1, 1, 0 ),
	)

# A pure blood: all three places from its one legacy.
SINGLE_SPELL_WEAVE = ( 0, 0, 0 )


@dataclass(
		frozen=True,
		)
class Fiendish_Blood:
	"""One Tiefling's visible descent, drawn once and kept."""

	# One legacy for a pure blood, two for a mixed one; the Heritage first.
	legacies: tuple[type, ...]
	horns: str
	eyes: str
	fur: str
	tail: str
	# The legacy that lends each spell place, in level order (1, 3, 5).
	spell_lenders: tuple[type, ...]

	@property
	def mixed(
			self,
			) -> bool:
		return len( self.legacies ) > 1

	@property
	def names(
			self,
			) -> tuple[str, ...]:
		return tuple(
				legacy.__name__
				for legacy in self.legacies
				)

	@property
	def spells(
			self,
			) -> tuple[tuple[int, str], ...]:
		"""The legacy spells as ``(level, spell key)`` rows, like ``SPELLS``."""
		return tuple(
				lender.SPELLS[place]
				for place, lender in enumerate( self.spell_lenders )
				)

	@property
	def title(
			self,
			) -> str:
		"""The Fiendish Legacy entry's name: ``Abyssal``, or ``Abyssal and Infernal``."""
		return " and ".join( self.names )

	def opening(
			self,
			) -> str:
		"""The line that names the hells, before the body is described."""
		if self.mixed:
			first = self.legacies[0].ORIGIN
			second = self.legacies[1].ORIGIN
			return f"Two hells meet in your blood: {first}, and {second}."
		origin = self.legacies[0].ORIGIN
		return f"Yours is the aspect of {origin}."

	def paragraph(
			self,
			) -> str:
		"""The whole face, in one fixed order: hells, horns, eyes, fur, tail."""
		sentences = [
				self.opening(),
				self.horns,
				self.eyes,
				f"Your fur shines like metal: {self.fur}.",
				]
		if self.tail:
			sentences.append( self.tail )
		return " ".join( sentences )


def _open_blood_dice(
		target,
		):
	"""The one Dice Bag every part of the blood is drawn from."""
	return target.Dice_Bag(
			"identity.species.Tiefling.fiendish_blood",
			version="1",
			namespace="GenLegendActor",
			)


def _draw_legacies(
		target,
		heritage,
		dice,
		) -> tuple[type, ...]:
	"""The Heritage, then a second legacy from the whole list (it may repeat)."""
	from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling

	pool = list( Tiefling.HERITAGES )
	if heritage not in pool:
		raise ValueError(
				f"{heritage!r} is not a Tiefling legacy."
				)
	second = target.Pick(
			pool,
			dice=dice,
			)
	if second is heritage:
		return ( heritage, )
	return (
			heritage,
			second,
			)


def _draw_part(
		target,
		legacies,
		part: str,
		dice,
		) -> str:
	"""One part of the face: which legacy lends it, then which of its lines."""
	lender = target.Pick(
			list( legacies ),
			dice=dice,
			)
	options = getattr( lender, part )
	if not options:
		raise ValueError(
				f"{lender.__name__} declares no {part}."
				)
	return target.Pick(
			list( options ),
			dice=dice,
			)


def _draw_fur(
		target,
		legacies,
		dice,
		) -> str:
	"""A colour from each legacy, woven together; one colour for a pure blood."""
	first_colour = target.Pick(
			list( legacies[0].FUR ),
			dice=dice,
			)
	if len( legacies ) == 1:
		weave = target.Pick(
				list( SINGLE_FUR_WEAVES ),
				dice=dice,
				)
		return weave.format( a=first_colour )
	second_colour = target.Pick(
			list( legacies[1].FUR ),
			dice=dice,
			)
	weave = target.Pick(
			list( FUR_WEAVES ),
			dice=dice,
			)
	return weave.format(
			a=first_colour,
			b=second_colour,
			)


def _open_spell_dice(
		target,
		):
	"""The Dice Bag the spell pattern is drawn from, apart from the face's."""
	return target.Dice_Bag(
			"identity.species.Tiefling.fiendish_blood.spells",
			version="1",
			namespace="GenLegendActor",
			)


def _draw_spell_lenders(
		target,
		legacies,
		) -> tuple[type, ...]:
	"""Which legacy lends each spell place; both appear when the blood is mixed."""
	if len( legacies ) == 1:
		weave = SINGLE_SPELL_WEAVE
	else:
		weave = target.Pick(
				list( SPELL_WEAVES ),
				dice=_open_spell_dice( target ),
				)
	return tuple(
			legacies[index]
			for index in weave
			)


def _find_tail(
		legacies,
		) -> str:
	"""The first tail any legacy of the blood carries, or none."""
	for legacy in legacies:
		if legacy.TAIL:
			return legacy.TAIL
	return ""


def Draw_Fiendish_Blood(
		target,
		heritage,
		) -> Fiendish_Blood:
	"""
	Draw this Tiefling's blood, once and for life.

	Called from the Heritage's Imprint.  The order of the draws below is part
	of the replay contract: reordering them hands every Tiefling a new face.
	"""
	dice = _open_blood_dice( target )
	legacies = _draw_legacies(
			target,
			heritage,
			dice,
			)
	horns = _draw_part(
			target,
			legacies,
			"HORNS",
			dice,
			)
	eyes = _draw_part(
			target,
			legacies,
			"EYES",
			dice,
			)
	fur = _draw_fur(
			target,
			legacies,
			dice,
			)
	return Fiendish_Blood(
			legacies=legacies,
			horns=horns,
			eyes=eyes,
			fur=fur,
			tail=_find_tail( legacies ),
			spell_lenders=_draw_spell_lenders(
					target,
					legacies,
					),
			)
