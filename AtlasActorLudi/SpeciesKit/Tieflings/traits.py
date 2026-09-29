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
