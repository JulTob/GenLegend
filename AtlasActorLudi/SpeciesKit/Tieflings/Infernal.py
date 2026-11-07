"""The 2024 Infernal Tiefling Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.Tieflings.traits import (
	Imprint_Fiendish_Heritage,
	)
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Heritage_Yet
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Infernal_Marks


class Infernal(
	Tiefling,
	Heritage,
	Fiendish_Legacy,
	):
	"""A Tiefling Heritage carrying fiery magic."""

	@Pre
	def Only_One_Heritage(
		target,
		):
		return No_Heritage_Yet( target )

	DAMAGE_RESISTANCE = "Fire"
	# Where the looks may suggest the bloodline starts: a name, never described.
	PLACE = "the Nine Hells"
	# The marks this legacy lends to a Tiefling's aspect (``Map_of_Marks``).
	MARKS = Infernal_Marks
	SPELLS = (
		(
			1,
			"Firebolt",
			),
		(
			3,
			"HellishRebuke",
			),
		(
			5,
			"Darkness",
			),
		)

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Fiendish_Heritage(
			target,
			Infernal,
			)
