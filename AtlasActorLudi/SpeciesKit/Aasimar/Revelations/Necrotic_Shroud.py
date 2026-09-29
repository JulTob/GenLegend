"""The Necrotic Shroud Revelation Shape."""

from TopKit import Imprint
from TopKit import Pre

from AtlasActorLudi.SpeciesKit.Aasimar.Revelations.base import (
	No_Revelation_Yet,
	Imprint_Revelation,
	)
from AtlasActorLudi.SpeciesKit.Aasimar.Revelations.base import (
	Celestial_Revelation,
	)


class Necrotic_Shroud(Celestial_Revelation):
	"""A necrotic Revelation carrying a frightening shroud."""

	DAMAGE_TYPE = "Necrotic"
	RADIUS = 10
	SAVE_ABILITY = "CHA"
	CONDITION = "Frightened"
	EXCLUDES_ALLIES = True

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
			Necrotic_Shroud,
			)
