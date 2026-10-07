"""
The Draconic Ancestors, and what each one breathes.

Ten dragons, five damage types.  The table is the whole of the rule: an
ancestor is chosen, and every other draconic trait reads its damage type from
here.  Nothing else about the dragon is mechanical.
"""

from __future__ import annotations


# Ancestor to damage type, exactly as the Draconic Ancestors table gives it.
DRACONIC_ANCESTORS = {
	"Black": "Acid",
	"Blue": "Lightning",
	"Brass": "Fire",
	"Bronze": "Lightning",
	"Copper": "Acid",
	"Gold": "Fire",
	"Green": "Poison",
	"Red": "Fire",
	"Silver": "Cold",
	"White": "Cold",
	}


def draconic_ancestor(
		char,
		) -> tuple[str, str]:
	"""
	This Character's ancestor and its damage type, drawn once and kept.

	The bag is named and level-free, so a Dragonborn does not change colour on
	levelling up any more than a familiar changes species.
	"""
	standing = getattr(
		char,
		"draconic_ancestor",
		None,
		)

	if standing:
		return (
			standing,
			DRACONIC_ANCESTORS[
				standing
				],
			)

	dice = char.Dice_Bag( "Draconic_Ancestry.ancestor" )
	ancestor = char.Pick(
		list(
			DRACONIC_ANCESTORS
			),
		dice=dice,
		)
	char.draconic_ancestor = ancestor
	char.draconic_damage = DRACONIC_ANCESTORS[
		ancestor
		]

	return (
		ancestor,
		char.draconic_damage,
		)


__all__ = (
	"DRACONIC_ANCESTORS",
	"draconic_ancestor",
	)


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the ancestor comes from one Dice Bag opened
	#-- as "Draconic_Ancestry.ancestor" with the default key, over the whole
	#-- table; a second ask returns the standing ancestor and opens nothing.
	from AtlasActorLudi.CharactersKit import Character

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
		character = Character(
			seed=7,
			)
		ancestor, damage = draconic_ancestor( character )
		again = draconic_ancestor( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert again == (
		ancestor,
		damage,
		)
	assert DRACONIC_ANCESTORS[
		ancestor
		] == damage
	assert opened == [
		(
			"Draconic_Ancestry.ancestor",
			{},
			),
		], opened
	assert drawn == [
		tuple(
			DRACONIC_ANCESTORS
			),
		], drawn


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.Dragonborn.Map_of_Ancestors self-test" )
