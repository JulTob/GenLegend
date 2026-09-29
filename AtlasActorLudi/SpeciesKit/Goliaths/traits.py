"""Shared 2024 Goliath trait Tags."""

from TopKit import Imprint
from TopKit import Pre

from AtlasLusoris.FeaturesKit import Trait


class Powerful_Build(Trait):
	"""Giant strength applied to grappling and carrying capacity."""

	GRAPPLE_ESCAPE_TEST = "Ability Check"
	CARRYING_SIZE_BONUS = 1

	@Imprint
	def Set_Powerful_Build(
		target,
		):
		target.grapple_escape_advantage = True
		target.carrying_size_bonus = Powerful_Build.CARRYING_SIZE_BONUS


class Large_Form(Trait):
	"""The level-five Goliath growth transformation."""

	LEVEL = 5
	ACTION = "Bonus Action"
	SIZE = "Large"
	DURATION_MINUTES = 10
	END_ACTION = "No Action"
	STRENGTH_CHECK_ADVANTAGE = True
	SPEED_BONUS = 10
	USES = 1
	RECOVERY = "Long Rest"

	@Pre
	def Goliath_Only(
		target,
		):
		from AtlasActorLudi.SpeciesKit.Goliaths import Goliath

		return target in Goliath

	@Pre
	def Gained_At_Level_Five(
		target,
		):
		return int(
			getattr(
				target,
				"level",
				1,
				)
			) >= Large_Form.LEVEL

	@Imprint
	def Set_Large_Form(
		target,
		):
		target.large_form_action = Large_Form.ACTION
		target.large_form_size = Large_Form.SIZE
		target.large_form_duration_minutes = Large_Form.DURATION_MINUTES
		target.large_form_end_action = Large_Form.END_ACTION
		target.large_form_strength_check_advantage = (
			Large_Form.STRENGTH_CHECK_ADVANTAGE
			)
		target.large_form_speed_bonus = Large_Form.SPEED_BONUS
		target.large_form_uses = Large_Form.USES
		target.large_form_recovery = Large_Form.RECOVERY
