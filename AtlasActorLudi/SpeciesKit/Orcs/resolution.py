"""Resolve Orc rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature
from AtlasActorLudi.SpeciesKit.traits import Darkvision_Rules
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


def _project_adrenaline_rush(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Orcs import Adrenaline_Rush

	proficiency = _proficiency_bonus( target )
	target.adrenaline_rush_temporary_hit_points = proficiency
	target.adrenaline_rush_uses = proficiency
	Project_Species_Feature(
		target,
		"Adrenaline Rush",
		(
			"*The winds of your storm are hard to catch, rider. Run, be "
			"free, and run.*\n\n"
			"You can take the "
			f"{Adrenaline_Rush.DASH_ACTION} action as a "
			f"{Adrenaline_Rush.ACTION}, and when you do you gain "
			f"{proficiency} Temporary Hit Points. You can do this "
			f"{proficiency} times, and you regain all expended uses when you "
			"finish a Short or Long Rest."
			),
		chips=(
			Chip(
				"💨",
				"Adrenaline Rush Uses",
				proficiency,
				),
			Chip(
				"💚",
				"Rush Temporary HP",
				proficiency,
				),
			),
		level=1,
		)


def _project_darkvision(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Orcs import Darkvision

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
		(
			"*The ride does not end at nightfall, and neither does your "
			"watch.*\n\n"
			+ Darkvision_Rules(
				darkvision_range,
				)
			),
		chips=(
			Chip(
				"👁️",
				"Darkvision",
				f"{darkvision_range} ft",
				),
			),
		level=1,
		)


def _project_relentless_endurance(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Orcs import Relentless_Endurance

	Project_Species_Feature(
		target,
		"Relentless Endurance",
		(
			"*Do not fall, rider! Be strong! Carry on!*\n\n"
			"When you are reduced to 0 Hit Points but not killed outright, "
			"you can drop to 1 Hit Point instead. Once you use this trait, "
			"you can't use it again until you finish a "
			f"{Relentless_Endurance.RECOVERY}."
			),
		chips=(
			Chip(
				"❤️‍🔥",
				"Relentless Endurance",
				"1 / Long Rest",
				),
			),
		level=1,
		)


def Resolve_Orc_Features(
	target,
	) -> None:
	"""Project the Orc Tags into readable Entries and Chips."""
	from AtlasActorLudi.SpeciesKit.Orcs import Orc

	if target not in Orc:
		return

	_project_adrenaline_rush( target )
	_project_darkvision( target )
	_project_relentless_endurance( target )
