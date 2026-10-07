"""The shared 2024 Orc Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Orcs.traits import Adrenaline_Rush
from AtlasActorLudi.SpeciesKit.Orcs.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Orcs.traits import Relentless_Endurance
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Orc", "Ork" )
class Orc(
	Species,
	Humanoid,
	Adrenaline_Rush,
	Darkvision,
	Relentless_Endurance,
	):
	"""A determined Humanoid shaped for endurance."""

	TONGUE = "Orc"
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
			Orc,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Orc, "TONGUE", None ) == "Orc"
	assert Orc.TONGUE in standard_languages
	print( "OK: SpeciesKit.Orcs.base self-test (TONGUE Orc)" )
