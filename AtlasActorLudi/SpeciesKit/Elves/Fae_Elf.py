"""
The Fae Elf Heritage Shape.

Published as the Lorwyn Elf in *Lorwyn: First Light*, and renamed here for the
same reason the setting renamed everything else: the elves who stayed by the
crossings are not a plane's local variant, they are the branch that never came
across.
"""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage
from AtlasActorLudi.SpeciesKit.Elves.traits import Elven_Lineage

from AtlasActorLudi.SpeciesKit.Elves.base import Elf


class Fae_Elf(
	Elf,
	Heritage,
	Elven_Lineage,
	):
	"""An Elf Heritage carrying the magic of the Feywild crossings."""

	HERITAGE_DESCRIPTION = (
		"""Our kind is a bridge between the Courts of the Fae and the mortal world. Our people stayed close to the crossings into the Feywild, and we remain touched by their magic. Fae Elves are usually polite, friendly, and more open to emotion than other elves. Our ears are exquisitely long, sometimes as long as our arms, and we are the most beautiful of all elvenkind, even with our charms off and terrible morning hair. We consult the Archfey and their Warlocks in dire times."""
		)
	SPELLS = (
		(
			1,
			"ThornWhip",
			),
		(
			3,
			"Command",
			),
		(
			5,
			"Silence",
			),
		)
	CANTRIP_LIST = "Druid"
	DEFAULT_CANTRIP = "ThornWhip"

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			Fae_Elf,
			)
		target.fae_elf_cantrip = Fae_Elf.DEFAULT_CANTRIP
