"""The shared 2024 Tiefling trait Tags."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.physiology import Imprint_Heritage
from AtlasLusoris.FeaturesKit import Grant_Resistance
from AtlasLusoris.FeaturesKit import Trait


class Fiendish_Legacy(Trait):
	"""Spellcasting context shared by every Tiefling Heritage."""

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
			dice_bag = target.Dice_Bag( "Fiendish_Legacy.spellcasting_ability" )
			selected = target.Pick(
				Fiendish_Legacy.SPELLCASTING_ABILITIES,
				dice=dice_bag,
				)

		if selected not in Fiendish_Legacy.SPELLCASTING_ABILITIES:
			raise ValueError(
				"Fiendish Legacy spellcasting ability must be "
				"Intelligence, Wisdom, or Charisma."
				)

		target.species_spellcasting_ability = selected


class Otherworldly_Presence(Trait):
	"""Thaumaturgy cast through Fiendish Legacy spellcasting."""

	SPELLS = (
		(
			1,
			"Thaumaturgy",
			),
		)

	@Imprint
	def Set_Otherworldly_Presence(
		target,
		):
		target.otherworldly_presence_spell = "Thaumaturgy"


def Imprint_Fiendish_Heritage(
	target,
	heritage,
	) -> None:
	"""Imprint one Tiefling Heritage and its resistance atomically."""
	Imprint_Heritage(
		target,
		heritage,
		)
	Grant_Resistance(
		target,
		heritage.DAMAGE_RESISTANCE,
		)
	target.fiendish_legacy = heritage.__name__.replace(
		"_",
		" ",
		)
	target.fiendish_legacy_damage_resistance = (
		heritage.DAMAGE_RESISTANCE
		)


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the lineage ability comes from one Dice Bag
	#-- opened as "Fiendish_Legacy.spellcasting_ability" with the default key,
	#-- from the three abilities the Trait declares.
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit.Tieflings import traits
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
		traits.Fiendish_Legacy( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert opened == [
		(
			"Fiendish_Legacy.spellcasting_ability",
			{},
			),
		], opened
	assert drawn == [
		traits.Fiendish_Legacy.SPELLCASTING_ABILITIES,
		], drawn
	assert (
		character.species_spellcasting_ability
		in traits.Fiendish_Legacy.SPELLCASTING_ABILITIES
		)


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.Tieflings.traits self-test" )
