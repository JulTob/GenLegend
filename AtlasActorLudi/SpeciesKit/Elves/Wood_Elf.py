"""The 2024 Wood Elf Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage
from AtlasActorLudi.SpeciesKit.Elves.traits import Elven_Lineage

from AtlasActorLudi.SpeciesKit.Elves.base import Elf
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Heritage_Yet


class Wood_Elf(
	Elf,
	Heritage,
	Elven_Lineage,
	):
	"""An Elf Heritage with greater speed and primal magic."""

	@Pre
	def Only_One_Heritage(
		target,
		):
		return No_Heritage_Yet( target )

	SPEED = 35
	HERITAGE_DESCRIPTION = (
		"""Our forebears stayed where the trees were. We adapted and became like the woods: pensive, observant, direct. Our kind look hairier than other elves, and some have little stag horns. Some still paint their faces, and we consult our druids first in important matters."""
		)
	SPELLS = (
		(
			1,
			"Druidcraft",
			),
		(
			3,
			"Longstrider",
			),
		(
			5,
			"PassWithoutTrace",
			),
		)

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			Wood_Elf,
			)
		target.speed = Wood_Elf.SPEED
