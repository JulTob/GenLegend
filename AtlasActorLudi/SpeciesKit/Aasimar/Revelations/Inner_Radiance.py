"""The Inner Radiance Revelation Shape."""

from TopKit import Imprint
from TopKit import Pre

from AtlasActorLudi.SpeciesKit.Aasimar.Revelations.base import (
	No_Revelation_Yet,
	Imprint_Revelation,
	)
from AtlasActorLudi.SpeciesKit.Aasimar.Revelations.base import (
	Celestial_Revelation,
	)


class Inner_Radiance(Celestial_Revelation):
	"""A radiant Revelation carrying a searing aura."""

	DAMAGE_TYPE = "Radiant"
	BRIGHT_LIGHT_RADIUS = 10
	DIM_LIGHT_ADDITIONAL_RADIUS = 10
	AURA_RADIUS = 10

	@Pre
	def Only_One_Revelation(
		target,
		):
		return No_Revelation_Yet( target )

	@Imprint
	def Set_Revelation(
		target,
		):
		Imprint_Revelation(
			target,
			Inner_Radiance,
			)
