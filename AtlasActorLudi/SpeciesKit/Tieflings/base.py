"""The shared 2024 Tiefling Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.kinship import Fiend as Kin_Fiend
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Otherworldly_Presence

# The common Darkvision, at its shared 60-foot range: no Heritage extends it.
from AtlasActorLudi.SpeciesKit.traits import Darkvision
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Tiefling" )
class Tiefling(
	Species,
	Humanoid,
	Kin_Fiend,
	Darkvision,
	Otherworldly_Presence,
	):
	"""A Humanoid carrying a fiendish legacy."""

	TONGUE = "Infernal"
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
			Tiefling,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Tiefling, "TONGUE", None ) == "Infernal"
	assert Tiefling.TONGUE in rare_languages
	print( "OK: SpeciesKit.Tieflings.base self-test (TONGUE Infernal)" )
