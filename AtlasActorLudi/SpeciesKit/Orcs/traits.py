"""The 2024 Orc trait Tags."""

from TopKit import Imprint

from AtlasActorLudi.SpeciesKit.traits import Darkvision as Common_Darkvision
from AtlasLusoris.FeaturesKit import Trait


class Adrenaline_Rush(Trait):
	"""A swift Dash carrying a surge of Temporary Hit Points."""

	ACTION = "Bonus Action"
	DASH_ACTION = "Dash"
	TEMPORARY_HIT_POINTS = "PB"
	USES = "PB"
	RECOVERY = (
		"Short Rest",
		"Long Rest",
		)

	@Imprint
	def Set_Adrenaline_Rush(
		target,
		):
		target.adrenaline_rush_action = Adrenaline_Rush.ACTION
		target.adrenaline_rush_dash_action = Adrenaline_Rush.DASH_ACTION
		target.adrenaline_rush_temporary_hit_point_scaling = (
			"Proficiency Bonus"
			)
		target.adrenaline_rush_use_scaling = "Proficiency Bonus"
		target.adrenaline_rush_recovery = Adrenaline_Rush.RECOVERY


class Darkvision(Common_Darkvision):
	"""Orcish Darkvision extending to 120 feet."""

	RANGE = 120

	@Imprint
	def Set_Orc_Range(
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


class Relentless_Endurance(Trait):
	"""Defiance after falling to 0 Hit Points."""

	TRIGGER_HIT_POINTS = 0
	RESULT_HIT_POINTS = 1
	REQUIRES_NOT_KILLED_OUTRIGHT = True
	USES = 1
	RECOVERY = "Long Rest"

	@Imprint
	def Set_Relentless_Endurance(
		target,
		):
		target.relentless_endurance_trigger_hit_points = (
			Relentless_Endurance.TRIGGER_HIT_POINTS
			)
		target.relentless_endurance_result_hit_points = (
			Relentless_Endurance.RESULT_HIT_POINTS
			)
		target.relentless_endurance_requires_survivable_damage = (
			Relentless_Endurance.REQUIRES_NOT_KILLED_OUTRIGHT
			)
		target.relentless_endurance_uses = Relentless_Endurance.USES
		target.relentless_endurance_recovery = (
			Relentless_Endurance.RECOVERY
			)
