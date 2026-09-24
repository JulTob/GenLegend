"""The shared 2024 Dragonborn Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Breath_Weapon
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Draconic_Ancestry
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Draconic_Flight
from AtlasActorLudi.SpeciesKit.kinship import Dragon as Kin_Dragon
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species


class Dragonborn(
	Species,
	Humanoid,
	Kin_Dragon,
	Darkvision,
	Draconic_Ancestry,
	Breath_Weapon,
	Draconic_Flight,
	):
	"""A Humanoid shaped like a dragon."""

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
