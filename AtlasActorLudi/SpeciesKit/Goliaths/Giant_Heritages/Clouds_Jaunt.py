"""The Cloud's Jaunt Giant Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Giant_Heritage,
	)
from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages.base import (
	Imprint_Giant_Heritage,
	)


class Clouds_Jaunt(Giant_Heritage):
	"""A Cloud Giant boon carrying short-range teleportation."""

	DISPLAY = "Cloud's Jaunt"
	GIANT_KIND = "Cloud Giant"
	ACTIVATION = "Bonus Action"
	TELEPORT_DISTANCE = 30
	EFFECT = (
		"you magically teleport up to 30 feet to an unoccupied space "
		"you can see."
		)
	CHIP_LABEL = "Jaunt Distance"
	CHIP_VALUE = "30 ft"
	CHIP_ICON = "☁️"

	@Imprint
	def Set_Giant_Heritage(
		target,
		):
		Imprint_Giant_Heritage(
			target,
			Clouds_Jaunt,
			)
		target.giant_heritage_teleport_distance = (
			Clouds_Jaunt.TELEPORT_DISTANCE
			)
