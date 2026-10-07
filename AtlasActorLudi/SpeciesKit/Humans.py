"""The 2024 Human Species Shape."""

from TopKit import Flag
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
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Human" )
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

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )

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

	dice_bag = target.Dice_Bag( "Versatile.choice" )
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


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the Versatile feat comes from one Dice Bag
	#-- opened as "Versatile.choice" with the default key, over every Origin
	#-- Feat as before; a second ask opens nothing.
	import AtlasActorLudi.SpeciesKit.Humans as catalog
		#-- The catalog's module: under ``python -m`` this file loads twice,
		#-- and the Species the catalog applies is its own, not the twin's.
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills
	from AtlasActorLudi.Map_of_Scores import PB
	from AtlasActorLudi.SpeciesKit import Apply_Species

	character = Character(
		seed=7,
		)
	Apply_Species(
		character,
		catalog.Human,
		)
	character.AS = AbilityScores(
		STR=10,
		DEX=12,
		CON=14,
		INT=16,
		WIS=15,
		CHA=13,
		character=character,
		)
	character.proficiency_bonus = PB( character.level )
	character.skills = Char_Skills(
		character,
		character.AS,
		character.proficiency_bonus,
		)
	character.base_health = 10
	character.known_spells = []

	opened = []
	drawn = []
	original_dice_bag = Character.Dice_Bag
	original_pick = Character.Pick

	def recording_dice_bag(
		char,
		purpose,
		**key,
		):
		opened.append(
			(
				purpose,
				key,
				)
			)
		return original_dice_bag(
			char,
			purpose,
			**key,
			)

	def recording_pick(
		char,
		ledger,
		weights=None,
		**options,
		):
		drawn.append(
			tuple(
				ledger
				)
			)
		return original_pick(
			char,
			ledger,
			weights,
			**options,
			)

	Character.Dice_Bag = recording_dice_bag
	Character.Pick = recording_pick
	try:
		catalog.Resolve_Human_Features( character )
		opened_once = list( opened )
		drawn_once = list( drawn )
		catalog.Resolve_Human_Features( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	feats = tuple(
		ORIGIN_FEATS.values()
		)
	#-- The first bag and the first draw are Versatile's; what follows is
	#-- the granted feat's own, and belongs to the feat.
	assert opened_once[ 0 ] == (
		"Versatile.choice",
		{},
		), opened_once
	assert drawn_once[ 0 ] == feats, drawn_once
	assert opened == opened_once, opened
	assert character._versatile_origin_feat in feats


if __name__ == "__main__":
	_test_dice_purpose()
	assert getattr( Human, "TONGUE", None ) is None
		#-- A Human has no Species tongue: the creation picks roll the plain
		#-- d12 (QST-0144.10).
	print( "OK: SpeciesKit.Humans self-test" )
