"""The 2024 Halfling trait Tags."""

from TopKit import Imprint

from AtlasLusoris.FeaturesKit import Trait


class Brave(Trait):
	"""Courage against the Frightened condition."""

	TEST = "Saving Throw"
	CONDITION = "Frightened"
	PURPOSES = (
		"Avoid",
		"End",
		)
	ADVANTAGE = True

	@Imprint
	def Set_Brave(
		target,
		):
		target.frightened_saving_throw_advantage = Brave.ADVANTAGE
		target.brave_condition = Brave.CONDITION
		target.brave_purposes = Brave.PURPOSES


class Halfling_Nimbleness(Trait):
	"""Movement through the spaces of larger creatures."""

	MINIMUM_RELATIVE_SIZE = 1
	CAN_STOP_IN_SPACE = False

	@Imprint
	def Set_Nimbleness(
		target,
		):
		target.creature_space_passage_size_difference = (
			Halfling_Nimbleness.MINIMUM_RELATIVE_SIZE
			)
		target.can_stop_in_passed_creature_space = (
			Halfling_Nimbleness.CAN_STOP_IN_SPACE
			)


class Luck(Trait):
	"""A mandatory reroll after a natural 1 on a D20 Test."""

	TEST = "D20 Test"
	TRIGGER_ROLL = 1
	MUST_USE_NEW_ROLL = True

	@Imprint
	def Set_Luck(
		target,
		):
		target.luck_test = Luck.TEST
		target.luck_trigger_roll = Luck.TRIGGER_ROLL
		target.luck_must_use_new_roll = Luck.MUST_USE_NEW_ROLL


class Naturally_Stealthy(Trait):
	"""Access to Hide while obscured by a larger creature."""

	ACTION = "Hide"
	MINIMUM_RELATIVE_SIZE = 1

	@Imprint
	def Set_Natural_Stealth(
		target,
		):
		target.naturally_stealthy_action = Naturally_Stealthy.ACTION
		target.hide_obscuring_creature_size_difference = (
			Naturally_Stealthy.MINIMUM_RELATIVE_SIZE
			)
