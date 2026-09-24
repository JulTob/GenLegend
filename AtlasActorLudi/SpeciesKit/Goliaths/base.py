"""The shared 2024 Goliath Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Goliaths.traits import Powerful_Build
from AtlasActorLudi.SpeciesKit.kinship import Giant as Kin_Giant
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species


class Goliath(
	Species,
	Humanoid,
	Kin_Giant,
	Powerful_Build,
	):
	"""A giant-descended Humanoid."""

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
