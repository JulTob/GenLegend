"""The High Elf Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage
from AtlasActorLudi.SpeciesKit.Elves.traits import Elven_Lineage
from AtlasActorLudi.SpeciesKit.Elves.base import Elf


class High_Elf(
	Elf,
	Heritage,
	Elven_Lineage,
	):
	"""An Elf Heritage with adaptable arcane magic."""

	HERITAGE_DESCRIPTION = (
		"""The ships were ours. Our kind explored, found magic, found commerce, found crafts. We are still of the ice: patient, cold, adaptive. Our hair is golden, and our skin, whatever its tone, is cold to the touch. We find our answers among the magi and the wizards."""
		)
	SPELLS = (
		(
			1,
			"Prestidigitation",
			),
		(
			3,
			"DetectMagic",
			),
		(
			5,
			"MistyStep",
			),
		)
	CANTRIP_LIST = "Wizard"
	DEFAULT_CANTRIP = "Prestidigitation"

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			High_Elf,
			)
		target.high_elf_cantrip = High_Elf.DEFAULT_CANTRIP
