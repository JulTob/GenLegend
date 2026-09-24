"""The Fire's Burn Giant Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Giant_Heritage,
	)
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Imprint_Giant_Heritage,
	)


class Fires_Burn(Giant_Heritage):
	"""A Fire Giant boon carrying additional Fire damage."""

	DISPLAY = "Fire's Burn"
	GIANT_KIND = "Fire Giant"
	ACTIVATION = "Damaging Attack-Roll Hit"
	DAMAGE_DICE = "1d10"
	DAMAGE_TYPE = "Fire"
	EFFECT = (
		"when you hit a target with an attack roll and deal damage, you "
		"deal an extra 1d10 Fire damage to that target."
		)
	CHIP_LABEL = "Fire's Burn"
	CHIP_VALUE = "1d10 Fire"
	CHIP_ICON = "🔥"

	@Imprint
	def Set_Giant_Heritage(
		target,
		):
		Imprint_Giant_Heritage(
			target,
			Fires_Burn,
			)
		target.giant_heritage_damage_dice = Fires_Burn.DAMAGE_DICE
		target.giant_heritage_damage_type = Fires_Burn.DAMAGE_TYPE
