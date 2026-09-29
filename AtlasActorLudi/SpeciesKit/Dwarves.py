"""The 2024 Dwarf Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.declarations import Player_Handbook_2024
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species


class Dwarf(
	Species,
	Humanoid,
	):
	"""A resilient Humanoid with an affinity for stone."""

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Dwarf,
			size,
			)


Player_Handbook_2024(
	Dwarf,
	weight=100,
	size_options=(
		"Medium",
		),
	speed=30,
	)
