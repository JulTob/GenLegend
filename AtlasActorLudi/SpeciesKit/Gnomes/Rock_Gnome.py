"""The 2024 Rock Gnome Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Gnomes.base import Gnome
from AtlasActorLudi.SpeciesKit.Gnomes.traits import Gnomish_Lineage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage


class Rock_Gnome(
	Gnome,
	Heritage,
	Gnomish_Lineage,
	):
	"""A Gnome Heritage with cantrips and clockwork devices."""

	HERITAGE_DESCRIPTION = (
		"""Your family took the city offer and filled a workshop with it. Lenses, springs, a bird that sings on the hour and has done since your great-grandfather wound it. You were taught that anything can be observed, taken apart, solved and improved, that most things should be, and that the shame is not in breaking it but in failing to make something out of the pieces."""
		)
	SPELLS = (
		(
			1,
			"Mending",
			),
		(
			1,
			"Prestidigitation",
			),
		)
	DEVICE_LIMIT = 3
	DEVICE_ARMOR_CLASS = 5
	DEVICE_HIT_POINTS = 1
	DEVICE_DURATION_HOURS = 8
	DEVICE_CASTING_MINUTES = 10
	DEVICE_ACTIVATION = "Bonus Action"
	DEVICE_DISMANTLE_ACTION = "Utilize"
	DEVICE_REQUIRES_TOUCH = True

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			Rock_Gnome,
			)
