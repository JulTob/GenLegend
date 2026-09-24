"""The 2024 Abyssal Tiefling Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.Tieflings.traits import (
	Imprint_Fiendish_Heritage,
	)
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Heritage_Yet


class Abyssal(
	Tiefling,
	Heritage,
	Fiendish_Legacy,
	):
	"""A Tiefling Heritage carrying poisonous magic."""

	@Pre
	def Only_One_Heritage(
		target,
		):
		return No_Heritage_Yet( target )

	DAMAGE_RESISTANCE = "Poison"
	HERITAGE_DESCRIPTION = (
		"You descend from demons, chaotic beings with no defined shape. The chaos of the abyss reflects in your metallic fur of bright color, with spots and lines, sometimes shifting and moving from place to place or changing shape each time you wake up. Your colors are the most intense of all Tieflings, but also the hardest to hide. Your horns are twisted and spiky, most times uneven. Your eyes could look normal, if they didn't change color with your emotions."
		)
	SPELLS = (
		(
			1,
			"PoisonSpray",
			),
		(
			3,
			"RayofSickness",
			),
		(
			5,
			"HoldPerson",
			),
		)

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Fiendish_Heritage(
			target,
			Abyssal,
			)
