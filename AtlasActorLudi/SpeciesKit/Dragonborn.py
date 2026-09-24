"""The 2024 Dragonborn Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.declarations import Player_Handbook_2024
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species


class Dragonborn(
	Species,
	Humanoid,
	):
	"""A Humanoid with draconic ancestry."""

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Dragonborn,
			size,
			)


Player_Handbook_2024(
	Dragonborn,
	weight=100,
	size_options=(
		"Medium",
		),
	speed=30,
	)
