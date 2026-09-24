"""
The Shadow Elf Heritage Shape.

Published as the Shadowmoor Elf in *Lorwyn: First Light*.  Renamed here because
the setting already has a Shadow realm of its own: the Shadow Background calls
it the place where the Fae are made of dream and shadows are made of nightmare,
and these are the elves who live on that side of it.
"""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage
from AtlasActorLudi.SpeciesKit.Elves.traits import Elven_Lineage

from AtlasActorLudi.SpeciesKit.Elves.base import Elf


class Shadow_Elf(
	Elf,
	Heritage,
	Elven_Lineage,
	):
	"""An Elf Heritage with deeper Darkvision and the magic of the Shadow."""

	DARKVISION_RANGE = 120

	HERITAGE_DESCRIPTION = (
		"""Our kind took what was left: the Shadow realm. We are a bridge to that world, and it feels scary at times, but it's home. Nightmares come true in the Shadow realm, so we learnt to be stoic, reflective and analytic, to discern dream from thought. Our skin is some shade of grey, including perfect white and pitch black, and our eyes are all white. When hardship comes, we consult the oracles and mystics, and the wise Monks who follow the way of Shadows."""
		)
	SPELLS = (
		(
			1,
			"StarryWisp",
			),
		(
			3,
			"Heroism",
			),
		(
			5,
			"GentleRepose",
			),
		)

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			Shadow_Elf,
			)
		target.darkvision = Shadow_Elf.DARKVISION_RANGE
