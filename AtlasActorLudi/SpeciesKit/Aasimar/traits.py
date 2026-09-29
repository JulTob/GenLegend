"""The 2024 Aasimar trait Tags."""

from TopKit import Imprint

from AtlasLusoris.FeaturesKit import Grant_Resistance
from AtlasLusoris.FeaturesKit import Trait


class Celestial_Resistance(Trait):
	"""Resistance carried from an Upper Planes spark."""

	DAMAGE_TYPES = (
		"Necrotic",
		"Radiant",
		)

	@Imprint
	def Set_Resistances(
		target,
		):
		Grant_Resistance(
			target,
			*Celestial_Resistance.DAMAGE_TYPES,
			)


class Healing_Hands(Trait):
	"""Healing magic carried by an Aasimar."""

	ACTION = "Magic"
	DIE = 4
	USES = 1
	RECOVERY = "Long Rest"


class Light_Bearer(Trait):
	"""The Light cantrip with Charisma spellcasting."""

	SPELLS = (
		(
			1,
			"Light",
			),
		)
	SPELLCASTING_ABILITY = "CHA"

	@Imprint
	def Set_Spellcasting_Ability(
		target,
		):
		target.species_spellcasting_ability = (
			Light_Bearer.SPELLCASTING_ABILITY
			)
