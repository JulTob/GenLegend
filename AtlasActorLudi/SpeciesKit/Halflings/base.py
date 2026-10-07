"""The shared 2024 Halfling Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Halflings.traits import Brave
from AtlasActorLudi.SpeciesKit.Halflings.traits import Halfling_Nimbleness
from AtlasActorLudi.SpeciesKit.Halflings.traits import Luck
from AtlasActorLudi.SpeciesKit.Halflings.traits import Naturally_Stealthy
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Halfling", "Hobbit" )
class Halfling(
	Species,
	Humanoid,
	Brave,
	Halfling_Nimbleness,
	Luck,
	Naturally_Stealthy,
	):
	"""A small, fortunate, and naturally stealthy Humanoid."""

	TONGUE = "Halfling"
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
			Halfling,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Halfling, "TONGUE", None ) == "Halfling"
	assert Halfling.TONGUE in standard_languages
	print( "OK: SpeciesKit.Halflings.base self-test (TONGUE Halfling)" )
