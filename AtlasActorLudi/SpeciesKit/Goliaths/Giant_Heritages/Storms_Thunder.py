"""The Storm's Thunder Giant Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Giant_Heritage,
	)
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Imprint_Giant_Heritage,
	)


class Storms_Thunder(Giant_Heritage):
	"""A Storm Giant boon carrying reactive Thunder damage."""

	DISPLAY = "Storm's Thunder"
	GIANT_KIND = "Storm Giant"
	ACTIVATION = "Reaction after taking damage"
	RANGE = 60
	DAMAGE_DICE = "1d8"
	DAMAGE_TYPE = "Thunder"
	EFFECT = (
		"when you take damage from a creature within 60 feet, you can use "
		"your Reaction to deal 1d8 Thunder damage to that creature."
		)
	CHIP_LABEL = "Storm's Thunder"
	CHIP_VALUE = "1d8 Thunder / 60 ft"
	CHIP_ICON = "⛈️"

	@Imprint
	def Set_Giant_Heritage(
		target,
		):
		Imprint_Giant_Heritage(
			target,
			Storms_Thunder,
			)
		target.giant_heritage_range = Storms_Thunder.RANGE
		target.giant_heritage_damage_dice = (
			Storms_Thunder.DAMAGE_DICE
			)
		target.giant_heritage_damage_type = (
			Storms_Thunder.DAMAGE_TYPE
			)
