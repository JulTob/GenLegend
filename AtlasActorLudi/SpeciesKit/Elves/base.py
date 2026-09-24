"""The shared 2024 Elf Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.kinship import Fey as Kin_Fey
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasActorLudi.SpeciesKit.Elves.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Elves.traits import Fey_Ancestry
from AtlasActorLudi.SpeciesKit.Elves.traits import Keen_Senses
from AtlasActorLudi.SpeciesKit.Elves.traits import Trance
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


class Elf(
	Species,
	Humanoid,
	Kin_Fey,
	Darkvision,
	Fey_Ancestry,
	Keen_Senses,
	Trance,
	):
	"""A 2024 Elf with fey ancestry."""

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
			Elf,
			size,
			)
