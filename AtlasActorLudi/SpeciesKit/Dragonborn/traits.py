"""The 2024 Dragonborn trait Tags."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.traits import Darkvision as Common_Darkvision
from AtlasLusoris.FeaturesKit import Trait


class Darkvision(Common_Darkvision):
	"""Draconic Darkvision, at the common sixty feet."""

	RANGE = 60


class Draconic_Ancestry(Trait):
	"""One dragon in the line, and the damage everything else inherits."""

	@Imprint
	def Set_Draconic_Ancestry(
		target,
		):
		from AtlasActorLudi.SpeciesKit.Dragonborn.Map_of_Ancestors import (
			draconic_ancestor,
			)

		ancestor, damage = draconic_ancestor( target )
		target.draconic_ancestor = ancestor
		target.draconic_damage = damage
		# Granted, not merely recorded.  The old implementation named the
		# Resistance in prose and never put it on the sheet's own list.
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
					damage,
					)
				)
			)


class Breath_Weapon(Trait):
	"""The exhalation, in a cone or a line, replacing one attack."""

	CONE = 15
	LINE_LENGTH = 30
	LINE_WIDTH = 5
	SAVE_ABILITY = "CON"
	DIE = 10
	RECOVERY = "Long Rest"

	@staticmethod
	def dice(
			level: int,
			) -> int:
		"""One die, and one more at 5, 11 and 17."""
		return (
			1
			+ (
				level >= 5
				)
			+ (
				level >= 11
				)
			+ (
				level >= 17
				)
			)

	@Imprint
	def Set_Breath_Weapon(
		target,
		):
		target.breath_weapon_cone = Breath_Weapon.CONE
		target.breath_weapon_line = Breath_Weapon.LINE_LENGTH
		target.breath_weapon_recovery = Breath_Weapon.RECOVERY


class Draconic_Flight(Trait):
	"""Spectral wings, made of the same energy as the breath."""

	LEVEL = 5
	ACTION = "Bonus Action"
	DURATION_MINUTES = 10
	USES = 1
	RECOVERY = "Long Rest"

	@Imprint
	def Set_Draconic_Flight(
		target,
		):
		target.draconic_flight_action = Draconic_Flight.ACTION
		target.draconic_flight_duration_minutes = (
			Draconic_Flight.DURATION_MINUTES
			)
		target.draconic_flight_recovery = Draconic_Flight.RECOVERY
