"""The 2024 Infernal Tiefling Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.Tieflings.traits import (
	Imprint_Fiendish_Heritage,
	)
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Heritage_Yet


class Infernal(
	Tiefling,
	Heritage,
	Fiendish_Legacy,
	):
	"""A Tiefling Heritage carrying fiery magic."""

	@Pre
	def Only_One_Heritage(
		target,
		):
		return No_Heritage_Yet( target )

	DAMAGE_RESISTANCE = "Fire"
	# The face this legacy lends a Tiefling, as plain class data.  A second
	# legacy may lend some of it too: see ``Fiendish_Blood``.
	ORIGIN = "the Nine Hells, all fire and brimstone"
	HORNS = (
		"Your horns are black like onyx, and sit close to your head like a crown.",
		"Your horns are black like onyx, polished, and close to your head like a crown.",
		)
	EYES = (
		"Your eyes are black, all but a golden iris that burns like a coal.",
		"Your eyes are black, but the iris is gold and seems to flicker like fire.",
		)
	# Black, or a bright colour that resembles a flame.
	FUR = (
		"onyx black",
		"flame red",
		"flame orange",
		"ember gold",
		)
	TAIL = "You also have a tail, ending in an arrow-shaped tip."
	SPELLS = (
		(
			1,
			"Firebolt",
			),
		(
			3,
			"HellishRebuke",
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
		Imprint_Fiendish_Heritage(
			target,
			Infernal,
			)
