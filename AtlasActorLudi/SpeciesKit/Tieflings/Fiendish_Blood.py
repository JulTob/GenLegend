"""
Fiendish Blood — which legacies a Tiefling carries.

Every Tiefling has one Heritage Tag (Abyssal, Chthonic or Infernal), and that
Tag keeps every rule it carries today.  The blood adds a second legacy, drawn
from the whole list at uniform random; the same legacy may come up twice,
which makes a pure blood, neither rarer nor commoner than any particular pair.
That is the Aasimar's rule for its two Ideals (``Map_of_Ideals``).

The blood is structure, and it stays hidden: the page never says a Tiefling
carries two hells.  What shows is the **aspect** (``Fiendish_Aspect``), the
look both legacies lend, collapsed once from their marks.

The draw happens once, in the Heritage's Imprint, from named Dice Bags that do
not depend on the level, so a level-up never hands anybody a different aspect.
Reading the blood afterwards never rolls.
"""

from __future__ import annotations

from dataclasses import dataclass

from AtlasActorLudi.SpeciesKit.Tieflings.Fiendish_Aspect import Collapse_Aspect
from AtlasActorLudi.SpeciesKit.Tieflings.Fiendish_Aspect import Fiendish_Aspect


@dataclass(
		frozen=True,
		)
class Fiendish_Blood:
	"""One Tiefling's legacies and the aspect they lend, drawn once and kept."""

	# One legacy for a pure blood, two for a mixed one; the Heritage first.
	legacies: tuple[type, ...]
	aspect: Fiendish_Aspect

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


def _open_blood_dice(
		target,
		):
	"""The Dice Bag the second legacy is drawn from."""
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


def Draw_Fiendish_Blood(
		target,
		heritage,
		) -> Fiendish_Blood:
	"""
	Draw this Tiefling's blood, once and for life.

	Called from the Heritage's Imprint.  The replay contract, in one place:
	every draw of the blood has a Dice Bag of its own, each fresh for its
	purpose, so changing one draw never moves another.

	- ``identity.species.Tiefling.fiendish_blood``: the second legacy (here).
	- ``identity.species.Tiefling.fiendish_blood.rumour``: the place the
	  aspect suggests (opened in ``Collapse_Aspect``).
	- ``identity.species.Tiefling.fiendish_blood.aspect``: the collapse of the
	  look (opened in ``Collapse_Aspect``).
	- ``identity.species.Tiefling.fiendish_blood.voice``: the words the
	  grammar derives (opened in ``Collapse_Aspect``).
	"""
	legacies = _draw_legacies(
			target,
			heritage,
			_open_blood_dice( target ),
			)
	return Fiendish_Blood(
			legacies=legacies,
			aspect=Collapse_Aspect(
					target,
					legacies,
					),
			)
