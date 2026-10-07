"""The shared 2024 Dwarf Species Shape."""

from TopKit import Flag
from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.Dwarves.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Dwarves.traits import Dwarven_Resilience
from AtlasActorLudi.SpeciesKit.Dwarves.traits import Dwarven_Toughness
from AtlasActorLudi.SpeciesKit.Dwarves.traits import Stonecunning
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Dwarf" )
class Dwarf(
	Species,
	Humanoid,
	Darkvision,
	Dwarven_Resilience,
	Dwarven_Toughness,
	Stonecunning,
	):
	"""
	Dwarves are a Humanoid species with a cultural basis in historical Iberian
	and Hispanic cultures. They are deeply familial, living in clans, and they
	worship gold and metals, both physical metals and soul-metals. Their
	religion observes the lives of the Saints: Ancestors with pure metallic
	souls.
	"""

	TONGUE = "Dwarvish"
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
			Dwarf,
			size,
			)


if __name__ == "__main__":
	#-- The tongue is plain class data a reader can take with getattr, and
	#-- it sits on the 2024 table it belongs to (QST-0144.10).
	from AtlasLudus.Map_of_Languages import (
			rare_languages,
			standard_languages,
			)
	assert getattr( Dwarf, "TONGUE", None ) == "Dwarvish"
	assert Dwarf.TONGUE in standard_languages
	print( "OK: SpeciesKit.Dwarves.base self-test (TONGUE Dwarvish)" )
