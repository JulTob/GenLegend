"""The 2024 Human Species Shape."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.declarations import Player_Handbook_2024
from AtlasActorLudi.SpeciesKit.physiology import Imprint_Species
from AtlasLusoris.FeaturesKit import Resourceful
from AtlasLusoris.FeaturesKit import Grant_Versatile
from AtlasLusoris.FeaturesKit import ORIGIN_FEATS
from AtlasLusoris.FeaturesKit import Skillful
from AtlasLusoris.FeaturesKit import Versatile


class Human(
	Species,
	Humanoid,
	Resourceful,
	Skillful,
	Versatile,
	):
	"""
	2024 Human species.

	Human Tag.

	- Underlay:
		- Species (base)
			A tagged Human has a Species: Human.
		- Humanoid
			A Human is a Humanoid. General game classification.

		Applied Features:
		- Resourceful
		- Skillful
		- Versatile
	"""

	@Imprint
	def Set_Physiology(
		target,
		size=None,
		):
		Imprint_Species(
			target,
			Human,
			size,
			)


Player_Handbook_2024(
	Human,
	weight=120,
	size_options=(
		"Medium",
		"Small",
		),
	size_weights=(
		95,
		5,
		),
	speed=30,
	description=(
		"""Humans. The wonderful wanderers. There is nowhere humans are not, and nowhere humans wouldn't go. In worlds full of monsters, magic, and dangers, our people learned not just to survive but to thrive. And it is all thanks to the power of friendship. We befriend most species, and coexist with them. We trade, we help each other, we build relationships and even marriages. Humans tend to organize, making institutions and orders part of our legacy. There is always a human "kingdom" a couple of days' walk away.

Think of what kinds of organizations {name} may belong to, such as guilds, schools, or militias."""
		),
	)


def Resolve_Human_Features(
	target,
	) -> None:
	"""Resolve Human choices once the finished sheet owns its ledgers."""
	if target not in Human:
		return

	if getattr(
		target,
		"_versatile_origin_feat",
		None,
		) is not None:
		return

	dice_bag = target.Dice_Bag(
		"identity.species.Human.versatile",
		version="2024",
		namespace="GenLegendActor",
		)
	feat = target.Pick(
		tuple(
			ORIGIN_FEATS.values()
			),
		dice=dice_bag,
		)

	Grant_Versatile(
		target,
		feat,
		)
