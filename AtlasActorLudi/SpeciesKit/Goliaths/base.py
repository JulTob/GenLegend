"""The shared 2024 Goliath Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Goliaths.traits import Powerful_Build
from AtlasActorLudi.SpeciesKit.kinship import Giant as Kin_Giant
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


class Goliath(
	Species,
	Humanoid,
	Kin_Giant,
	Powerful_Build,
	):
	"""A giant-descended Humanoid."""

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
			Goliath,
			size,
			)
