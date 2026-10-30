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
	# The face this legacy lends a Tiefling, as plain class data.  A second
	# legacy may lend some of it too: see ``Fiendish_Blood``.
	ORIGIN = "the Abyss, where demons have no shape of their own"
	HORNS = (
		"Your horns are twisted and spiky, and no two of their points match.",
		"Your horns grow twisted and uneven, one always a little longer than the other.",
		"Your horns are a crooked tangle of spikes, never growing the same way twice.",
		)
	EYES = (
		"Your eyes could pass for ordinary, if they did not change colour with your feelings.",
		"Your eyes look ordinary until something moves you, and then their colour moves with it.",
		)
	# Colours only, so two legacies can share one coat.  The Abyss gives the
	# brightest of them, and the hardest to hide.
	FUR = (
		"electric blue",
		"acid green",
		"bright violet",
		"vivid magenta",
		)
	TAIL = ""
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
