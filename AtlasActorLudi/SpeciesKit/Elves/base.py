"""The shared 2024 Elf Species Shape."""

from TopKit import Flag
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


@Flag( "Elf" )
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

	TONGUE = "Elvish"
		#-- The Species' own tongue, plain data (QST-0144.10): Standard, so
		#-- it weighs SPECIES_TONGUE_FACES more on the two creation picks.

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


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Elf, "TONGUE", None ) == "Elvish"
	assert Elf.TONGUE in standard_languages
	print( "OK: SpeciesKit.Elves.base self-test (TONGUE Elvish)" )
