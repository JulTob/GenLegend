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
			dice_bag = target.Dice_Bag(
				"identity.species.Tiefling.fiendish_legacy.ability",
				version="2024",
				namespace="GenLegendActor",
				)
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
	"""
	Imprint one Tiefling Heritage, its blood, and its resistance atomically.

	The blood and its aspect are a choice made once: drawn here, only read
	later.  The blood is drawn before anything is imprinted, so a wave that
	cannot collapse leaves the Character untouched instead of half-adorned
	(a collapse failure raises before the Heritage, the Resistance or the
	legacy labels are written).
	"""
	from AtlasActorLudi.SpeciesKit.Tieflings.Fiendish_Blood import (
		Draw_Fiendish_Blood,
		)

	blood = Draw_Fiendish_Blood(
		target,
		heritage,
		)
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
	target.fiendish_blood = blood
	# Raw and unformatted: it may still hold {full_name}, since the name is
	# settled after the Species.  The Species projection owns the fill
	# (``Name_Slots``); anything else that prints it must fill it the same way.
	target.heritage_description = blood.aspect.paragraph()
