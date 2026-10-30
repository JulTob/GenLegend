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

The draw happens once, in the Heritage's Imprint, from one named Dice Bag that
does not depend on the level, so a level-up never hands anybody a different
face.  Reading the blood afterwards never rolls.

Nothing here is mechanical.  Fiendish Legacy carries the rules; this carries
the face.
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
	def title(
			self,
			) -> str:
		"""The sheet's heading: ``Abyssal``, or ``Abyssal and Infernal``."""
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
			)
