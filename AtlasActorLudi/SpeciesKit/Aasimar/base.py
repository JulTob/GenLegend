"""The shared 2024 Aasimar Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Aasimar.traits import Celestial_Resistance
from AtlasActorLudi.SpeciesKit.Aasimar.traits import Healing_Hands
from AtlasActorLudi.SpeciesKit.Aasimar.traits import Light_Bearer
from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.kinship import Celestial as Kin_Celestial
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasActorLudi.SpeciesKit.traits import Darkvision
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


class Aasimar(
	Species,
	Humanoid,
	Kin_Celestial,
	Darkvision,
	Celestial_Resistance,
	Healing_Hands,
	Light_Bearer,
	):
	"""A Humanoid carrying an Upper Planes spark."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Aasimar,
			size,
			)
