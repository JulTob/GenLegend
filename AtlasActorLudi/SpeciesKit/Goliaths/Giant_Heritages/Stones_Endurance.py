"""The Stone's Endurance Giant Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Giant_Heritage,
	)
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Imprint_Giant_Heritage,
	)


class Stones_Endurance(Giant_Heritage):
	"""A Stone Giant boon carrying reactive damage reduction."""

	DISPLAY = "Stone's Endurance"
	GIANT_KIND = "Stone Giant"
	ACTIVATION = "Reaction after taking damage"
	REDUCTION_DICE = "1d12"
	ABILITY = "CON"
	EFFECT = (
		"when you take damage, you can use your Reaction to roll "
		"{reduction_roll}, reducing that damage by the total."
		)
	CHIP_LABEL = "Stone's Endurance"
	CHIP_VALUE = "1d12 {constitution_modifier:+d}"
	CHIP_ICON = "🪨"

	@Imprint
	def Set_Giant_Heritage(
		target,
		):
		Imprint_Giant_Heritage(
			target,
			Stones_Endurance,
			)
		target.giant_heritage_reduction_dice = (
			Stones_Endurance.REDUCTION_DICE
			)
		target.giant_heritage_ability = Stones_Endurance.ABILITY
