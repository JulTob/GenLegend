"""The shared 2024 Gnome Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.kinship import Fey as Kin_Fey
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Gnomes.traits import Gnomish_Cunning
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasActorLudi.SpeciesKit.traits import Darkvision
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


class Gnome(
	Species,
	Humanoid,
	Kin_Fey,
	Darkvision,
	Gnomish_Cunning,
	):
	"""A small magical Humanoid."""

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
			Gnome,
			size,
			)
