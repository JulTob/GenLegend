"""The shared 2024 Halfling Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Halflings.traits import Brave
from AtlasActorLudi.SpeciesKit.Halflings.traits import Halfling_Nimbleness
from AtlasActorLudi.SpeciesKit.Halflings.traits import Luck
from AtlasActorLudi.SpeciesKit.Halflings.traits import Naturally_Stealthy
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species


class Halfling(
	Species,
	Humanoid,
	Brave,
	Halfling_Nimbleness,
	Luck,
	Naturally_Stealthy,
	):
	"""A small, fortunate, and naturally stealthy Humanoid."""

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Halfling,
			size,
			)
