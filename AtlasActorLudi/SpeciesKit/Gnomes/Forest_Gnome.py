"""The 2024 Forest Gnome Heritage Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.Gnomes.base import Gnome
from AtlasActorLudi.SpeciesKit.Gnomes.traits import Gnomish_Lineage
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage


class Forest_Gnome(
	Gnome,
	Heritage,
	Gnomish_Lineage,
	):
	"""A Gnome Heritage with illusion and animal-speaking magic."""

	HERITAGE_DESCRIPTION = (
		"""Your family never took the city offer, but put down roots in the forest nearby. You grew up past the last farm where the wood begins, on speaking terms with everything in it. The fae, they say, are nearer out there. Some of it rubbed off."""
		)
	SPELLS = (
		(
			1,
			"MinorIllusion",
			),
		(
			1,
			"SpeakWithAnimals",
			),
		)
	FREE_CAST_SPELL = "SpeakWithAnimals"
	FREE_CASTS = "PB"

	@Imprint
	def Set_Heritage(
		target,
		):
		Imprint_Heritage(
			target,
			Forest_Gnome,
			)
