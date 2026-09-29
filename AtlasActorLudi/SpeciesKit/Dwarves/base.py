"""The shared 2024 Dwarf Species Shape."""

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
