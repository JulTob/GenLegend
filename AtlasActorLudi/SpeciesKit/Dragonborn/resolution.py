"""Resolve Dragonborn rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Breath_Weapon
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Darkvision
from AtlasActorLudi.SpeciesKit.Dragonborn.traits import Draconic_Flight
from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature


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


def Resolve_Dragonborn_Features(
		target,
		) -> None:
	"""
	Project the Dragonborn Tags into readable Entries and Chips.

	Rules as the rulebook writes them: second person, present tense, numbers
	resolved where the sheet already knows them.
	"""
	from AtlasActorLudi.SpeciesKit.Dragonborn import Dragonborn
	from AtlasActorLudi.SpeciesKit.Dragonborn.Map_of_Ancestors import (
		draconic_ancestor,
		)

	if target not in Dragonborn:
		return

	ancestor, damage = draconic_ancestor( target )
	level = int(
		getattr(
			target,
			"level",
			1,
			)
		)
	proficiency = _proficiency_bonus( target )
	scores = getattr(
		target,
		"AS",
		None,
		)
	constitution = int(
		getattr(
			scores,
			Breath_Weapon.SAVE_ABILITY,
			10,
			)
		)
	save_dc = (
		8
		+ proficiency
		+ (
			constitution
			- 10
			) // 2
		)
	dice = Breath_Weapon.dice( level )
	target.breath_weapon_save_dc = save_dc
	target.breath_weapon_dice = dice
	target.breath_weapon_uses = proficiency

	# A record, not a paragraph.
	Project_Species_Feature(
		target,
		"Darkvision",
		"",
		chips=(
			(
				"Darkvision",
				f"{int(getattr(target, 'darkvision', Darkvision.RANGE))} ft",
				"👁️",
				),
			),
		level=1,
		)
	Project_Species_Feature(
		target,
		"Draconic Ancestry",
		(
			f"Your lineage stems from a {ancestor} Dragon. You have "
			f"Resistance to {damage} damage, and it is the damage type of "
			"your other draconic traits."
			),
		chips=(
			(
				"Draconic Ancestry",
				ancestor,
				"🐉",
				),
			(
				"Resistances",
				damage,
				"🛡️",
				),
			),
		level=1,
		)
	Project_Species_Feature(
		target,
		"Breath Weapon",
		(
			# "Burn" stays put for every ancestor, including the Silver one who
			# freezes you.  It rhymes with Dragonborn, and a saying is a
			# stereotype: a proverb being wrong about your particular dragon is
			# how proverbs work.  Do not key this to the damage type.
			"*An ancient saying: Never exasperate a Dragonborn, for they "
			"will sigh and you will burn.*\n\n"
			"When you take the Attack action on your turn, you can replace one "
			"of your attacks with an exhalation in a "
			f"{Breath_Weapon.CONE}-foot Cone or a "
			f"{Breath_Weapon.LINE_LENGTH}-foot Line that is "
			f"{Breath_Weapon.LINE_WIDTH} feet wide, choosing the shape each "
			"time. Each creature in that area makes a Dexterity saving throw "
			f"against DC {save_dc}, taking {dice}d{Breath_Weapon.DIE} "
			f"{damage} damage on a failed save and half as much on a "
			f"successful one. You can use this trait {proficiency} times, and "
			f"you regain all expended uses when you finish a "
			f"{Breath_Weapon.RECOVERY}."
			),
		chips=(
			(
				"Breath Weapon",
				f"{dice}d{Breath_Weapon.DIE} {damage}",
				"🔥",
				),
			(
				"Breath Save DC",
				save_dc,
				"🎯",
				),
			(
				"Breath Uses",
				proficiency,
				"💨",
				),
			),
		level=1,
		)

	if level < Draconic_Flight.LEVEL:
		return

	fly_speed = int(
		getattr(
			target,
			"speed",
			30,
			)
		)
	target.draconic_flight_speed = fly_speed
	Project_Species_Feature(
		target,
		"Draconic Flight",
		(
			f"As a {Draconic_Flight.ACTION}, you sprout spectral wings on your "
			f"back, made of Spectral {damage} energy. They last "
			f"for {Draconic_Flight.DURATION_MINUTES} minutes, or until you "
			"retract them (no action required) or have the Incapacitated "
			f"condition. During that time you have a Fly Speed of {fly_speed} "
			"feet. Once you use this trait, you can't use it again until you "
			f"finish a {Draconic_Flight.RECOVERY}."
			),
		chips=(
			(
				"Draconic Flight",
				f"{fly_speed} ft",
				"🪽",
				),
			),
		level=Draconic_Flight.LEVEL,
		)
