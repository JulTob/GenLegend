"""The Frost's Chill Giant Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Giant_Heritage,
	)
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Imprint_Giant_Heritage,
	)
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import No_Giant_Heritage_Yet


class Frosts_Chill(Giant_Heritage):
	"""A Frost Giant boon carrying Cold damage and hindrance."""

	@Pre
	def Only_One_Giant_Heritage(
		target,
		):
		return No_Giant_Heritage_Yet( target )

	DISPLAY = "Frost's Chill"
	GIANT_KIND = "Frost Giant"
	ACTIVATION = "Damaging Attack-Roll Hit"
	DAMAGE_DICE = "1d6"
	DAMAGE_TYPE = "Cold"
	SPEED_REDUCTION = 10
	DURATION = "Start of this Character's next turn"
	EFFECT = (
		"when you hit a target with an attack roll and deal damage, you "
		"deal an extra 1d6 Cold damage and reduce that target's Speed by "
		"10 feet until the start of your next turn."
		)
	CHIP_LABEL = "Frost's Chill"
	CHIP_VALUE = "1d6 Cold / −10 ft"
	CHIP_ICON = "❄️"

	@Imprint
	def Set_Giant_Heritage(
		target,
		):
		Imprint_Giant_Heritage(
			target,
			Frosts_Chill,
			)
		target.giant_heritage_damage_dice = Frosts_Chill.DAMAGE_DICE
		target.giant_heritage_damage_type = Frosts_Chill.DAMAGE_TYPE
		target.giant_heritage_speed_reduction = (
			Frosts_Chill.SPEED_REDUCTION
			)
		target.giant_heritage_effect_duration = Frosts_Chill.DURATION
