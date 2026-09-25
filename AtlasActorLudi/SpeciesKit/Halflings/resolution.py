"""Resolve Halfling rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature


def _project_brave(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Halflings import Brave

	Project_Species_Feature(
		target,
		"Brave",
		(
			"*You were brave enough to leave home. You can handle this.*\n\n"
			"You have Advantage on saving throws you make to avoid or end "
			"the Frightened condition."
			),
		chips=(
			(
				"Frightened Saves",
				"Advantage",
				"🛡️",
				),
			),
		level=1,
		)


def _project_nimbleness(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Halflings import Halfling_Nimbleness

	Project_Species_Feature(
		target,
		"Halfling Nimbleness",
		(
			"*This is just like child's play. Try not to get caught. You "
			"may die.*\n\n"
			"You can move through the space of any creature that is at "
			"least one size larger than you, though you can't stop "
			"there."
			),
		level=1,
		)


def _project_luck(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Halflings import Luck

	Project_Species_Feature(
		target,
		"Luck",
		(
			"*Halflings are said to be the luckiest people alive. You hope "
			"so.*\n\n"
			"When you roll a 1 on the d20 of a D20 Test, you can roll the "
			"die again, and you must use the new roll."
			),
		level=1,
		)


def _project_natural_stealth(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Halflings import Naturally_Stealthy

	Project_Species_Feature(
		target,
		"Naturally Stealthy",
		(
			"*You read in your stories that halflings can become "
			"invisible. You often wish it were true.*\n\n"
			"You can take the Hide action even when you are obscured only "
			"by a creature that is at least one size larger than "
			"you."
			),
		level=1,
		)


def Resolve_Halfling_Features(
	target,
	) -> None:
	"""Project the Halfling Tags into readable Entries and Chips."""
	from AtlasActorLudi.SpeciesKit.Halflings import Halfling

	if target not in Halfling:
		return

	_project_brave( target )
	_project_nimbleness( target )
	_project_luck( target )
	_project_natural_stealth( target )
