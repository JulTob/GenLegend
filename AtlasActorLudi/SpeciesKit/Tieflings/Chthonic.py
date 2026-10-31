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
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Chthonic_Marks


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
	# Where the looks may suggest the bloodline starts: a name, never described.
	PLACE = "Hades"
	# The marks this legacy lends to a Tiefling's aspect (``Map_of_Marks``).
	MARKS = Chthonic_Marks
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
