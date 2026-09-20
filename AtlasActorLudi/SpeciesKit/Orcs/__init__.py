"""The modular 2024 Orc Species Atlas."""

from AtlasActorLudi.SpeciesKit.Orcs.base import Orc
from AtlasActorLudi.SpeciesKit.Orcs.traits import Adrenaline_Rush
from AtlasActorLudi.SpeciesKit.Orcs.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Orcs.traits import Relentless_Endurance
from AtlasActorLudi.SpeciesKit.declarations import Player_Handbook_2024


Player_Handbook_2024(
	Orc,
	weight=80,
	size_options=(
		"Medium",
		),
	speed=30,
	description=(
		"""Orcs. The children of the horizon. Your people were on the plains first. Then the dwarves came for the gold underneath, the humans came to call it discovery, and the elves promised trade and brought curses. No orc was asked.

The old wisdom says the plains are open to everyone, and riders must travel. Now all orcs are riders and no camp is safe. The new peoples fence the plains and attack when your beasts pass through the old ways. We are called raiders instead of riders. We ride further, carry more and go without longer. Every soul walks a wind path, and we orcs carry our own through the storm. If we fall, we carry on.

Think of why {name} left the Orc Camp, and what would bring them back."""
		),
	)


from AtlasActorLudi.SpeciesKit.Orcs.resolution import Resolve_Orc_Features


__all__ = (
	"Adrenaline_Rush",
	"Darkvision",
	"Orc",
	"Relentless_Endurance",
	"Resolve_Orc_Features",
	)
