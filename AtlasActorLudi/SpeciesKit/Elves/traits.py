"""Shared 2024 Elf trait Tags and their sheet projection."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.traits import Darkvision
from AtlasLusoris.FeaturesKit import Trait


class Fey_Ancestry(Trait):
	"""Advantage when avoiding or ending the Charmed condition."""


class Keen_Senses(Trait):
	"""Training in Insight, Perception, or Survival."""

	SKILLS = (
		"Insight",
		"Perception",
		"Survival",
		)


class Trance(Trait):
	"""Elven rest and magical-sleep context."""

	@Imprint
	def Set_Rest(
		target,
		):
		target.needs_sleep = False
		target.magic_sleep_immune = True
		target.long_rest_hours = 4


class Elven_Lineage(Trait):
	"""Shared spellcasting choice contributed by an Elf Heritage."""

	# How far this lineage sees, declared rather than assigned inside an
	# Imprint, so that anything asking "how far does a Shadow Elf see" can read
	# the answer off the Heritage instead of generating one and looking.  The
	# lineages of the deep dark override it; the rest see as far as any Elf.
	DARKVISION_RANGE = Darkvision.RANGE

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
			dice_bag = target.Dice_Bag( "Elven_Lineage.spellcasting_ability" )
			selected = target.Pick(
				Elven_Lineage.SPELLCASTING_ABILITIES,
				dice=dice_bag,
				)

		if selected not in Elven_Lineage.SPELLCASTING_ABILITIES:
			raise ValueError(
				"Elven Lineage spellcasting ability must be "
				"Intelligence, Wisdom, or Charisma."
				)

		target.species_spellcasting_ability = selected


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the lineage ability comes from one Dice Bag
	#-- opened as "Elven_Lineage.spellcasting_ability" with the default key,
	#-- from the three abilities the Trait declares.
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit.Elves import traits
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
		traits.Elven_Lineage( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert opened == [
		(
			"Elven_Lineage.spellcasting_ability",
			{},
			),
		], opened
	assert drawn == [
		traits.Elven_Lineage.SPELLCASTING_ABILITIES,
		], drawn
	assert (
		character.species_spellcasting_ability
		in traits.Elven_Lineage.SPELLCASTING_ABILITIES
		)


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.Elves.traits self-test" )
