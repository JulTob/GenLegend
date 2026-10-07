"""The shared 2024 Dragonborn Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Breath_Weapon
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Draconic_Ancestry
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Draconic_Flight
from AtlasActorLudi.SpeciesKit.kinship import Dragon as Kin_Dragon
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Dragonborn" )
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

	TONGUE = "Draconic"
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
			Dragonborn,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Dragonborn, "TONGUE", None ) == "Draconic"
	assert Dragonborn.TONGUE in standard_languages
	print( "OK: SpeciesKit.Dragonborn.base self-test (TONGUE Draconic)" )
