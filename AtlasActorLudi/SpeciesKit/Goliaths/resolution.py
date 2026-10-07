"""Resolve Goliath rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature
from AtlasVenustas import Chip


def _proficiency_bonus(
	target,
	) -> int:
	return int(
		getattr(
			target,
			"proficiency_bonus",
			2,
			)
		)


def _constitution_modifier(
	target,
	) -> int:
	scores = getattr(
		target,
		"AS",
		None,
		)
	constitution = int(
		getattr(
			scores,
			"CON",
			10,
			)
		)

	return (
		constitution
		- 10
		) // 2


def _resolve_giant_heritage(
	target,
	):
	from AtlasActorLudi.SpeciesKit.Goliaths import Current_Giant_Heritage
	from AtlasActorLudi.SpeciesKit.Goliaths import GOLIATH_GIANT_HERITAGES

	current = Current_Giant_Heritage( target )

	if current is not None:
		return current

	#-- Named by the Trait the six outcomes share, Giant_Heritage, the way
	#-- Keen_Senses names the Elf's skill and Versatile the Human's feat.
	dice_bag = target.Dice_Bag( "Giant_Heritage.choice" )
	selected = target.Pick(
		GOLIATH_GIANT_HERITAGES,
		dice=dice_bag,
		)
	selected( target )

	return selected


# The favour a Goliath carries, named by the giant it came down from.  The
# Species entry says a Goliath "knows which giant it came from the way other
# people know a surname", so each of these speaks about the ancestor and never
# about the Goliath's temperament.
ANCESTRY_LINES = {
	"Clouds_Jaunt": (
		"The favour you carry came down from a Cloud Giant, and it was "
		"never quite where anyone looked for it."
		),
	"Fires_Burn": (
		"The favour you carry came down from a Fire Giant, and it has not "
		"forgotten the forge."
		),
	"Frosts_Chill": (
		"The favour you carry came down from a Frost Giant, and it arrives "
		"the way cold does, without announcing itself."
		),
	"Hills_Tumble": (
		"The favour you carry came down from a Hill Giant, and what it puts "
		"down stays down."
		),
	"Stones_Endurance": (
		"The favour you carry came down from a Stone Giant, and stone does "
		"not move aside for you either."
		),
	"Storms_Thunder": (
		"The favour you carry came down from a Storm Giant, and it answers "
		"weather with weather."
		),
	}


def _signed_die(
	die: str,
	modifier: int,
	) -> str:
	"""
	Standard dice notation: ``1d12 + 2``, ``1d12 - 1``, or bare ``1d12`` at +0.

	Spelling this out as "roll 1d12 and add {modifier}" reads oddly the moment
	the modifier is negative -- "add -1" is not how anyone at the table says
	it -- and it is more words than the rulebook ever uses for the same rule.
	"""
	if modifier > 0:
		return f"{die} + {modifier}"

	if modifier < 0:
		return f"{die} - {abs(modifier)}"

	return die


def _project_giant_heritage(
	target,
	heritage,
	) -> None:
	proficiency = _proficiency_bonus( target )
	constitution_modifier = _constitution_modifier( target )
	reduction_dice = getattr(
		heritage,
		"REDUCTION_DICE",
		None,
		)
	effect = heritage.EFFECT.format(
		constitution_modifier=constitution_modifier,
		reduction_roll=(
			_signed_die(
				reduction_dice,
				constitution_modifier,
				)
			if reduction_dice
			else ""
			),
		)
	chip_value = heritage.CHIP_VALUE.format(
		constitution_modifier=constitution_modifier,
		)
	target.giant_heritage_uses = proficiency
	target.giant_heritage_effect = effect

	if getattr(
		heritage,
		"ABILITY",
		None,
		) == "CON":
		target.giant_heritage_ability_modifier = constitution_modifier

	Project_Species_Feature(
		target,
		f"Giant Ancestry: {heritage.DISPLAY}",
		(
			f"{ANCESTRY_LINES.get(heritage.__name__, '')} "
			f"<b>{heritage.ACTIVATION}.</b> {effect[:1].upper()}{effect[1:]} "
			f"You can do this {proficiency} times, and you regain all "
			f"expended uses "
			f"when you finish a {heritage.RECOVERY}."
			),
		chips=(
			Chip(
				"🗿",
				"Giant Ancestry Uses",
				proficiency,
				),
			Chip(
				heritage.CHIP_ICON,
				heritage.CHIP_LABEL,
				chip_value,
				),
			),
		level=heritage.LEVEL,
		)


def _project_powerful_build(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Goliaths import Powerful_Build

	Project_Species_Feature(
		target,
		"Powerful Build",
		(
			"You were made smaller than your ancestors, never lighter. You "
			"have Advantage on ability checks you make to end the Grappled "
			"condition, and you count as one size larger when determining "
			"your carrying capacity."
			),
		chips=(
			Chip(
				"💪",
				"Carrying Size",
				"+1 category",
				),
			),
		level=1,
		)


def _project_large_form(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Goliaths import Large_Form

	if target.level < Large_Form.LEVEL:
		return

	if target not in Large_Form:
		Large_Form( target )

	transformed_speed = (
		int(
			getattr(
				target,
				"speed",
				35,
				)
			)
		+ Large_Form.SPEED_BONUS
		)
	target.large_form_speed = transformed_speed
	Project_Species_Feature(
		target,
		"Large Form",
		(
			"For a few minutes you are the size your ancestors never stopped "
			f"being. As a {Large_Form.ACTION}, and if there is room for you, "
			f"you become {Large_Form.SIZE} for "
			f"{Large_Form.DURATION_MINUTES} minutes, and you can end it "
			"early with no action required. "
			"While you are, you have Advantage on Strength checks and your "
			f"Speed becomes {transformed_speed} feet. Once you use this "
			"trait, you can't use it again until you finish a "
			f"{Large_Form.RECOVERY}."
			),
		chips=(
			Chip(
				"🗿",
				"Large Form Uses",
				Large_Form.USES,
				),
			Chip(
				"💨",
				"Large Form Speed",
				transformed_speed,
				),
			),
		level=Large_Form.LEVEL,
		)


def Resolve_Goliath_Features(
	target,
	) -> None:
	"""Project only the Goliath features already gained at this level."""
	from AtlasActorLudi.SpeciesKit.Goliaths import Goliath

	if target not in Goliath:
		return

	heritage = _resolve_giant_heritage( target )

	_project_giant_heritage(
		target,
		heritage,
		)
	_project_powerful_build( target )
	_project_large_form( target )


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the Giant Heritage comes from one Dice Bag
	#-- opened as "Giant_Heritage.choice" with the default key, over every
	#-- heritage the Goliath declares; a second ask opens nothing.
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit import Apply_Species
	from AtlasActorLudi.SpeciesKit.Goliaths import Current_Giant_Heritage
	from AtlasActorLudi.SpeciesKit.Goliaths import GOLIATH_GIANT_HERITAGES
	from AtlasActorLudi.SpeciesKit.Goliaths import Goliath

	opened = []
	drawn = []
	original_dice_bag = Character.Dice_Bag
	original_pick = Character.Pick

	def recording_dice_bag(
		char,
		purpose,
		**key,
		):
		opened.append(
			(
				purpose,
				key,
				)
			)
		return original_dice_bag(
			char,
			purpose,
			**key,
			)

	def recording_pick(
		char,
		ledger,
		weights=None,
		**options,
		):
		drawn.append(
			tuple(
				ledger
				)
			)
		return original_pick(
			char,
			ledger,
			weights,
			**options,
			)

	Character.Dice_Bag = recording_dice_bag
	Character.Pick = recording_pick
	try:
		character = Character(
			seed=7,
			)
		Apply_Species(
			character,
			Goliath,
			)
		#-- The Species itself leaves nothing to chance (one Size, no
		#-- Heritage), so every bag recorded below is the resolver's.
		assert opened == [], opened
		heritage = _resolve_giant_heritage( character )
		again = _resolve_giant_heritage( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert again is heritage
	assert Current_Giant_Heritage( character ) is heritage
	assert opened == [
		(
			"Giant_Heritage.choice",
			{},
			),
		], opened
	assert drawn == [
		tuple(
			GOLIATH_GIANT_HERITAGES
			),
		], drawn


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.Goliaths.resolution self-test" )
