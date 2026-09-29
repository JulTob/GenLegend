"""The 2024 Chthonic Tiefling Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.Tieflings.traits import (
	Imprint_Fiendish_Heritage,
	)
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Heritage_Yet


class Chthonic(
	Tiefling,
	Heritage,
	Fiendish_Legacy,
	):
	"""A Tiefling Heritage carrying necrotic magic."""

	@Pre
	def Only_One_Heritage(
		target,
		):
		return No_Heritage_Yet( target )

	DAMAGE_RESISTANCE = "Necrotic"
	HERITAGE_DESCRIPTION = (
		"Yours is the aspect of Hades, the most neutral of hells. No fire, no pain, only darkness. Your eyes are black except in the iris, which may be a vibrant color. Your fur takes sometimes the colors of animals like foxes, wolves and bulls, and sometimes the tones of a corpse. Either way you look uncanny to the eyes, but it's relatively easy to pass as human. Your horns look like ivory, bone, or metal, and stay close to your head, like a crown or a tiara."
		)
	SPELLS = (
		(
			1,
			"ChillTouch",
			),
		(
			3,
			"FalseLife",
			),
		(
			5,
			"RayOfEnfeeblement",
			),
		)

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Fiendish_Heritage(
			target,
			Chthonic,
			)
