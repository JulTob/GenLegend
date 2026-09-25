"""Resolve Dwarf rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature
from AtlasActorLudi.SpeciesKit.traits import Darkvision_Rules


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


def _project_darkvision(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Dwarves import Darkvision

	darkvision_range = int(
		getattr(
			target,
			"darkvision",
			Darkvision.RANGE,
			)
		)
	Project_Species_Feature(
		target,
		"Darkvision",
		Darkvision_Rules(
			darkvision_range
			),
		chips=(
			(
				"Darkvision",
				f"{darkvision_range} ft",
				"👁️",
				),
			),
		level=1,
		)


def _project_dwarven_resilience(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Dwarves import Dwarven_Resilience

	Project_Species_Feature(
		target,
		"Dwarven Resilience",
		(
			f"You have Resistance to {Dwarven_Resilience.RESISTANCE} damage. "
			"You also have Advantage on saving throws you make to avoid or "
			f"end the {Dwarven_Resilience.SAVE_ADVANTAGE_CONDITION} condition."
			),
		chips=(
			(
				"Poison Resistance",
				"Resistant",
				"🧪",
				),
			),
		level=1,
		)


def _project_dwarven_toughness(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Dwarves import Dwarven_Toughness

	level = int(
		getattr(
			target,
			"level",
			1,
			)
		)
	gained = level * Dwarven_Toughness.HIT_POINTS_PER_LEVEL
	Project_Species_Feature(
		target,
		"Dwarven Toughness",
		(
			"Your Hit Point maximum increases by "
			f"{Dwarven_Toughness.HIT_POINTS_PER_LEVEL}, and it increases by "
			f"{Dwarven_Toughness.HIT_POINTS_PER_LEVEL} again whenever you gain "
			f"a level: +{gained} at Level {level}."
			),
		chips=(
			(
				"Toughness HP",
				f"+{gained}",
				"❤️",
				),
			),
		level=1,
		)


def _project_stonecunning(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Dwarves import Stonecunning

	proficiency = _proficiency_bonus( target )
	target.stonecunning_uses = proficiency
	Project_Species_Feature(
		target,
		"Stonecunning",
		(
			f"As a {Stonecunning.ACTION}, you gain {Stonecunning.SENSE} with a "
			f"range of {Stonecunning.RANGE} feet for "
			f"{Stonecunning.DURATION_MINUTES} minutes. You must be on a stone "
			f"surface or touching a stone surface to use this "
			f"{Stonecunning.ACTION}. The stone can be natural or worked. You can "
			f"use this {Stonecunning.ACTION} a number of times equal to your "
			f"Proficiency Bonus ({proficiency}), and you regain all expended "
			f"uses when you finish a {Stonecunning.RECOVERY}."
			),
		chips=(
			(
				"Stonecunning Uses",
				proficiency,
				"🪨",
				),
			(
				"Tremorsense",
				f"{Stonecunning.RANGE} ft",
				"📿",
				),
			),
		level=1,
		)


def Resolve_Dwarf_Features(
	target,
	) -> None:
	"""Project the Dwarf Tags into readable Entries and Chips."""
	from AtlasActorLudi.SpeciesKit.Dwarves import Dwarf

	if target not in Dwarf:
		return

	_project_darkvision( target )
	_project_dwarven_resilience( target )
	_project_dwarven_toughness( target )
	_project_stonecunning( target )
