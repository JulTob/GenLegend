"""The Talarian Wings Revelation Shape."""

from TopKit import Imprint
from TopKit import Pre

from AtlasActorLudi.SpeciesKit.Aasimar.Revelations.base import (
	No_Revelation_Yet,
	Imprint_Revelation,
	)
from AtlasActorLudi.SpeciesKit.Aasimar.Revelations.base import (
	Celestial_Revelation,
	)


class Talarian_Wings(Celestial_Revelation):
	"""A radiant Revelation carrying spectral flight."""

	DAMAGE_TYPE = "Radiant"
	FLY_SPEED = "Speed"

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
			Talarian_Wings,
			)
