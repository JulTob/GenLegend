"""The 2024 Drow Elf Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage
from AtlasActorLudi.SpeciesKit.Elves.traits import Elven_Lineage

from AtlasActorLudi.SpeciesKit.Elves.base import Elf


class Drow(
	Elf,
	Heritage,
	Elven_Lineage,
	):
	"""An Elf Heritage with deeper Darkvision and drow magic."""

	DARKVISION_RANGE = 120

	HERITAGE_DESCRIPTION = (
		"""Our people went to the Underdark, and stayed, and built something others feared: a meritocracy. We thrived through unity, faith and strategy while others poisoned our legend. Now we defend a peace that others take for granted. We took after darkness: cunning, calm, and welcoming. Our hair is silvery, and our skin looks like the various stones of our homeland. Our own consult the priest and the cleric in times of tension, because by then everything short of a miracle has already been tried."""
		)
	SPELLS = (
		(
			1,
			"DancingLights",
			),
		(
			3,
			"FaerieFire",
			),
		(
			5,
			"Darkness",
			),
		)

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			Drow,
			)
		target.darkvision = Drow.DARKVISION_RANGE
