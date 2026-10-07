"""Shared 2024 Gnome trait Tags."""

from TopKit import Imprint

from AtlasLusoris.FeaturesKit import Trait


class Gnomish_Cunning(Trait):
	"""Advantage on Intelligence, Wisdom, and Charisma saving throws."""


class Gnomish_Lineage(Trait):
	"""Shared spellcasting choice contributed by a Gnome Heritage."""

	SPELLCASTING_ABILITIES = (
		"INT",
		"WIS",
		"CHA",
		)

	@Imprint
	def Choose_Spellcasting_Ability(
		target,
		):
		selected = getattr(
			target,
			"species_spellcasting_ability",
			None,
			)

		if selected is None:
			dice_bag = target.Dice_Bag( "Gnomish_Lineage.spellcasting_ability" )
			selected = target.Pick(
				Gnomish_Lineage.SPELLCASTING_ABILITIES,
				dice=dice_bag,
				)

		if selected not in Gnomish_Lineage.SPELLCASTING_ABILITIES:
			raise ValueError(
				"Gnomish Lineage spellcasting ability must be "
				"Intelligence, Wisdom, or Charisma."
				)

		target.species_spellcasting_ability = selected


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the lineage ability comes from one Dice Bag
	#-- opened as "Gnomish_Lineage.spellcasting_ability" with the default key,
	#-- from the three abilities the Trait declares.
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit.Gnomes import traits
		#-- The catalog's module: under ``python -m`` this file loads twice,
		#-- and the Tag the Heritages carry is the catalog's, not the twin's.

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
		traits.Gnomish_Lineage( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert opened == [
		(
			"Gnomish_Lineage.spellcasting_ability",
			{},
			),
		], opened
	assert drawn == [
		traits.Gnomish_Lineage.SPELLCASTING_ABILITIES,
		], drawn
	assert (
		character.species_spellcasting_ability
		in traits.Gnomish_Lineage.SPELLCASTING_ABILITIES
		)


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.Gnomes.traits self-test" )
