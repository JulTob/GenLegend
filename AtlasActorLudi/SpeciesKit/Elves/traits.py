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
			dice_bag = target.Dice_Bag(
				"identity.species.Elf.lineage.spellcasting_ability",
				version="2024",
				namespace="GenLegendActor",
				)
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
