"""The shared 2024 Goliath Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Goliaths.traits import Powerful_Build
from AtlasActorLudi.SpeciesKit.kinship import Giant as Kin_Giant
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Goliath", "Titan" )
class Goliath(
	Species,
	Humanoid,
	Kin_Giant,
	Powerful_Build,
	):
	"""A giant-descended Humanoid."""

	TONGUE = "Giant"
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
			Goliath,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Goliath, "TONGUE", None ) == "Giant"
	assert Goliath.TONGUE in standard_languages
	print( "OK: SpeciesKit.Goliaths.base self-test (TONGUE Giant)" )
