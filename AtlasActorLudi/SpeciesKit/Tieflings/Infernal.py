"""The 2024 Infernal Tiefling Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.Tieflings.traits import (
	Imprint_Fiendish_Heritage,
	)


class Infernal(
	Tiefling,
	Heritage,
	Fiendish_Legacy,
	):
	"""A Tiefling Heritage carrying fiery magic."""

	DAMAGE_RESISTANCE = "Fire"
	HERITAGE_DESCRIPTION = (
		"Yours is the aspect of the Nine Hells: fire and brimstone. Your horns are black like onyx, your eyes are black except for a golden fiery iris, and your fur is either black or a bright color that resembles a flame, in both cases with a metallic, almost golden, shine to it. You also have a tail with an arrow shape at the end."
		)
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
