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
	Imprint one Tiefling Heritage, its blood, and the Resistance it lends.

	The blood is a choice made once: drawn here, only read later.  Its
	Resistance is one of its legacies' (QST-0152), so it is granted after the
	blood is drawn, not from the Heritage alone.
	"""
	from AtlasActorLudi.SpeciesKit.Tieflings.Fiendish_Blood import (
		Draw_Fiendish_Blood,
		)

	Imprint_Heritage(
		target,
		heritage,
		)
	target.fiendish_legacy = heritage.__name__.replace(
		"_",
		" ",
		)
	target.fiendish_blood = Draw_Fiendish_Blood(
		target,
		heritage,
		)
	Grant_Resistance(
		target,
		target.fiendish_blood.resistance,
		)
	target.fiendish_legacy_damage_resistance = (
		target.fiendish_blood.resistance
		)
