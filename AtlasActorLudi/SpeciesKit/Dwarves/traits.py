"""The 2024 Dwarf trait Tags."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.traits import Darkvision as Common_Darkvision
from AtlasLusoris.FeaturesKit import Trait


class Darkvision(Common_Darkvision):
	"""Dwarven Darkvision extending to 120 feet."""

	RANGE = 120

	@Imprint
	def Set_Dwarf_Range(
		target,
		):
		target.darkvision = max(
			int(
				getattr(
					target,
					"darkvision",
					0,
					)
				),
			Darkvision.RANGE,
			)


class Dwarven_Resilience(Trait):
	"""Resistance to Poison, and defiance of the Poisoned condition."""

	RESISTANCE = "Poison"
	SAVE_ADVANTAGE_CONDITION = "Poisoned"

	@Imprint
	def Set_Dwarven_Resilience(
		target,
		):
		# Granted, not merely recorded: the Resistance goes on the sheet's own
		# list, so anything that reads resistances finds it without knowing a
		# Dwarf was involved.
		current = tuple(
			getattr(
				target,
				"damage_resistances",
				(),
				) or ()
			)
		target.damage_resistances = tuple(
			dict.fromkeys(
				(
					*current,
					Dwarven_Resilience.RESISTANCE,
					)
				)
			)
		# The 2024 wording is about the *condition*, not about poison as a
		# damage source: the save covers avoiding it and shrugging it off.
		target.dwarven_resilience_save_condition = (
			Dwarven_Resilience.SAVE_ADVANTAGE_CONDITION
			)
		target.dwarven_resilience_save_advantage = True


class Dwarven_Toughness(Trait):
	"""One more Hit Point, at first level and at every level after."""

	HIT_POINTS_PER_LEVEL = 1

	@Imprint
	def Set_Dwarven_Toughness(
		target,
		):
		target.dwarven_toughness_hit_points_per_level = (
			Dwarven_Toughness.HIT_POINTS_PER_LEVEL
			)
		# Granted, not merely recorded.  Contributions are kept by name so that
		# re-imprinting cannot double them and a second source cannot silently
		# replace the first: the sheet reads the sum.
		sources = dict(
			getattr(
				target,
				"bonus_health_sources",
				{},
				) or {}
			)
		sources[
			"Dwarven Toughness"
			] = Dwarven_Toughness.HIT_POINTS_PER_LEVEL
		target.bonus_health_sources = sources
		target.bonus_health_per_level = sum(
			sources.values()
			)
		# Granted, not merely recorded.  Contributions are kept by name so that
		# re-imprinting cannot double them and a second source cannot silently
		# replace the first: the sheet reads the sum.
		sources = dict(
			getattr(
				target,
				"bonus_health_sources",
				{},
				) or {}
			)
		sources[
			"Dwarven Toughness"
			] = Dwarven_Toughness.HIT_POINTS_PER_LEVEL
		target.bonus_health_sources = sources
		target.bonus_health_per_level = sum(
			sources.values()
			)


class Stonecunning(Trait):
	"""Tremorsense borrowed from whatever stone is underfoot."""

	ACTION = "Bonus Action"
	SENSE = "Tremorsense"
	RANGE = 60
	DURATION_MINUTES = 10
	# Natural or worked, and touching counts: a hand on the wall is enough.
	REQUIRES_STONE_CONTACT = True
	USES = "PB"
	RECOVERY = "Long Rest"

	@Imprint
	def Set_Stonecunning(
		target,
		):
		target.stonecunning_action = Stonecunning.ACTION
		target.stonecunning_sense = Stonecunning.SENSE
		target.stonecunning_range = Stonecunning.RANGE
		target.stonecunning_duration_minutes = (
			Stonecunning.DURATION_MINUTES
			)
		target.stonecunning_requires_stone_contact = (
			Stonecunning.REQUIRES_STONE_CONTACT
			)
		target.stonecunning_use_scaling = "Proficiency Bonus"
		target.stonecunning_recovery = Stonecunning.RECOVERY
