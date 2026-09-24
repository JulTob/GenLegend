"""The Hill's Tumble Giant Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Giant_Heritage,
	)
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Imprint_Giant_Heritage,
	)
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import No_Giant_Heritage_Yet


class Hills_Tumble(Giant_Heritage):
	"""A Hill Giant boon carrying a forceful knockdown."""

	@Pre
	def Only_One_Giant_Heritage(
		target,
		):
		return No_Giant_Heritage_Yet( target )

	DISPLAY = "Hill's Tumble"
	GIANT_KIND = "Hill Giant"
	ACTIVATION = "Damaging Attack-Roll Hit"
	MAXIMUM_TARGET_SIZE = "Large"
	CONDITION = "Prone"
	EFFECT = (
		"when you hit a Large or smaller creature with an attack roll and "
		"deal damage, you can give that target the Prone condition."
		)
	CHIP_LABEL = "Hill's Tumble"
	CHIP_VALUE = "Large or smaller → Prone"
	CHIP_ICON = "⛰️"

	@Imprint
	def Set_Giant_Heritage(
		target,
		):
		Imprint_Giant_Heritage(
			target,
			Hills_Tumble,
			)
		target.giant_heritage_maximum_target_size = (
			Hills_Tumble.MAXIMUM_TARGET_SIZE
			)
		target.giant_heritage_condition = Hills_Tumble.CONDITION
