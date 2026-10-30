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
	# The face this legacy lends a Tiefling, as plain class data.  A second
	# legacy may lend some of it too: see ``Fiendish_Blood``.
	ORIGIN = "Hades, where there is no fire and no pain, only darkness"
	HORNS = (
		"Your horns look like ivory, and stay close to your head like a crown.",
		"Your horns look like bone, and stay close to your head like a tiara.",
		"Your horns look like dark metal, and stay close to your head like a crown.",
		)
	EYES = (
		"Your eyes are black, all but the iris, which is a vivid violet.",
		"Your eyes are black, all but the iris, which is a vivid green.",
		"Your eyes are black, all but the iris, which is a vivid blue.",
		)
	# The colours of foxes, wolves and bulls, or the tones of a corpse.
	FUR = (
		"fox red",
		"wolf grey",
		"bull brown",
		"corpse grey",
		)
	TAIL = ""
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
