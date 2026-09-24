"""The shared 2024 Tiefling Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.kinship import Fiend as Kin_Fiend
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Otherworldly_Presence

# The common Darkvision, at its shared 60-foot range: no Heritage extends it.
from AtlasActorLudi.SpeciesKit.traits import Darkvision


class Tiefling(
	Species,
	Humanoid,
	Kin_Fiend,
	Darkvision,
	Otherworldly_Presence,
	):
	"""A Humanoid carrying a fiendish legacy."""

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Tiefling,
			size,
			)
