"""The shared 2024 Orc Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Orcs.traits import Adrenaline_Rush
from AtlasActorLudi.SpeciesKit.Orcs.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Orcs.traits import Relentless_Endurance
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species


class Orc(
	Species,
	Humanoid,
	Adrenaline_Rush,
	Darkvision,
	Relentless_Endurance,
	):
	"""A determined Humanoid shaped for endurance."""

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Orc,
			size,
			)
