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
			dice_bag = target.Dice_Bag(
				"identity.species.Gnome.lineage.spellcasting_ability",
				version="2024",
				namespace="GenLegendActor",
				)
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
