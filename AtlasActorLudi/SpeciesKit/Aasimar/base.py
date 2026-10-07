"""The shared 2024 Aasimar Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.Aasimar.traits import Celestial_Resistance
from AtlasActorLudi.SpeciesKit.Aasimar.traits import Healing_Hands
from AtlasActorLudi.SpeciesKit.Aasimar.traits import Light_Bearer
from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.kinship import Celestial as Kin_Celestial
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasActorLudi.SpeciesKit.traits import Darkvision
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Aasimar" )
class Aasimar(
	Species,
	Humanoid,
	Kin_Celestial,
	Darkvision,
	Celestial_Resistance,
	Healing_Hands,
	Light_Bearer,
	):
	"""A Humanoid carrying an Upper Planes spark."""

	TONGUE = "Celestial"
		#-- The Species' own tongue, plain data (QST-0144.10): Rare, so it
		#-- adds no faces at creation and waits for a later ruling.

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
			Aasimar,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Aasimar, "TONGUE", None ) == "Celestial"
	assert Aasimar.TONGUE in rare_languages
	print( "OK: SpeciesKit.Aasimar.base self-test (TONGUE Celestial)" )
