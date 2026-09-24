"""Resolve Aasimar rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.Aasimar.traits import Celestial_Resistance
from AtlasActorLudi.SpeciesKit.Aasimar.traits import Healing_Hands
from AtlasActorLudi.SpeciesKit.Aasimar.traits import Light_Bearer
from AtlasActorLudi.SpeciesKit.magic import Resolve_Species_Spells
from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature
from AtlasActorLudi.SpeciesKit.traits import Darkvision
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


def _revelation_options(
		target,
		) -> tuple[str, tuple]:
	"""
	All three transformations, because the choice is made at the table.

	The rules say "choose the option each time you transform", so no Aasimar
	*has* a Revelation: they have three, and pick one per use.  Selecting one
	at generation and printing only that was a rules bug.
	"""
	from AtlasActorLudi.SpeciesKit.Aasimar import Inner_Radiance
	from AtlasActorLudi.SpeciesKit.Aasimar import Necrotic_Shroud
	from AtlasActorLudi.SpeciesKit.Aasimar import Talarian_Wings

	proficiency = _proficiency_bonus( target )
	fly_speed = int(
		getattr(
			target,
			"speed",
			30,
			)
		)
	scores = getattr(
		target,
		"AS",
		None,
		)
	charisma = int(
		getattr(
			scores,
			Necrotic_Shroud.SAVE_ABILITY,
			10,
			)
		)
	save_dc = (
		8
		+ proficiency
		+ (
			charisma
			- 10
			) // 2
		)
	target.celestial_revelation_fly_speed = fly_speed
	target.celestial_revelation_save_dc = save_dc
	target.celestial_revelation_aura_damage = proficiency
	# Facts shared by all three options, published rather than only narrated.
	# There is deliberately no ``damage_type``: the type follows the option, and
	# the option is chosen each time the Aasimar transforms.
	target.celestial_revelation_extra_damage = proficiency
	target.celestial_revelation_uses = Talarian_Wings.USES
	target.celestial_revelation_duration_minutes = (
		Talarian_Wings.DURATION_MINUTES
		)
	target.celestial_revelation_end_action = "No Action"
	target.celestial_revelation_aura_radius = Inner_Radiance.AURA_RADIUS
	target.celestial_revelation_condition = Necrotic_Shroud.CONDITION

	return (
		(
			"<b>Talarian Wings.</b> <i>Something in you answers the sky's "
			"calling.</i> You spread your talaria into fully grown wings. "
			"Until the transformation ends you have a Fly Speed of "
			f"{fly_speed} feet. Your extra damage is Radiant. "
			"<b>Inner Radiance.</b> <i>Your inner spark becomes an aurora of "
			"pure light.</i> Your eyes shine brightly and your halo grows "
			"into a bright aurora. For the duration you shed "
			f"Bright Light in a {Inner_Radiance.BRIGHT_LIGHT_RADIUS}-foot "
			"radius and Dim Light for an additional "
			f"{Inner_Radiance.DIM_LIGHT_ADDITIONAL_RADIUS} feet, and at the "
			"end of each of your turns each creature within "
			f"{Inner_Radiance.AURA_RADIUS} feet of you takes {proficiency} "
			"Radiant damage. Your extra damage is Radiant. "
			"<b>Necrotic Shroud.</b> <i>The brighter the light, the darker "
			"the shadow.</i> Your eyes briefly become pools of darkness and "
			"your aureola collapses like a Dark Sun. "
			"Creatures other than your allies within "
			f"{Necrotic_Shroud.RADIUS} feet of you must succeed on a Charisma "
			f"saving throw (DC {save_dc}) or have the Frightened condition "
			"until the end of your next turn. Your extra damage is Necrotic."
			),
		(
			Chip(
				"🌟",
				"Revelation Uses",
				Talarian_Wings.USES,
				),
			Chip(
				"✨",
				"Revelation Damage",
				f"+{proficiency}",
				),
			Chip(
				"🪽",
				"Revelation Fly Speed",
				fly_speed,
				),
			Chip(
				"🌑",
				"Shroud Save DC",
				save_dc,
				),
			),
		)


def _project_revelation(
		target,
		) -> None:
	from AtlasActorLudi.SpeciesKit.Aasimar import Talarian_Wings

	if int(
		getattr(
			target,
			"level",
			1,
			)
		) < Talarian_Wings.LEVEL:
		return

	options, chips = _revelation_options( target )
	proficiency = _proficiency_bonus( target )
	Project_Species_Feature(
		target,
		"Celestial Revelation",
		(
			"*Be not afraid, for you bear a star.*\n\n"
			f"You can transform "
			f"as a {Talarian_Wings.ACTION} using one of the options below, "
			"choosing the option each time you transform. The transformation "
			f"lasts for {Talarian_Wings.DURATION_MINUTES} minute or until you "
			"end it (no action required). Once you transform, you can't do so "
			f"again until you finish a {Talarian_Wings.RECOVERY}. Once on each "
			"of your turns before the transformation ends, you can deal "
			f"{proficiency} extra damage to one target when you deal damage "
			"to it with an attack or a spell, of the type named by the option "
			f"you chose. {options}"
			),
		chips=chips,
		level=Talarian_Wings.LEVEL,
		)


def _project_descent(
	target,
	) -> None:
	from AtlasActorLudi.SpeciesKit.Aasimar.Map_of_Ideals import celestial_marks

	mark = celestial_marks( target )
	# No chip.  A chip is what you reach for mid-combat, and nobody looks up
	# their great-grandparent to roll initiative.  The paragraph is the whole
	# feature; the mark itself stays on the Character for anything that wants it.
	Project_Species_Feature(
		target,
		"Celestial Descent",
		mark.paragraph(),
		level=1,
		)


def Resolve_Aasimar_Features(
		target,
		) -> None:
	"""
	Project only the Aasimar features already gained at this level.

	Every rule and every line here is quoted from ``Canon/Mythos/Aasimar.md`` §0,
	which is the authority: where this file and that page disagree, this file is
	wrong.  The page settles the liberties (talaria and aureola in place of
	metallic freckles and glowing eyes, Talarian Wings in place of Heavenly
	Wings, and a halo that collapses where the published Shroud grew wings), and
	the numbers are resolved rather than left as "equal to your Proficiency
	Bonus" when the sheet already knows what that is.
	"""
	from AtlasActorLudi.SpeciesKit.Aasimar import Aasimar

	if target not in Aasimar:
		return

	_project_descent( target )
	proficiency = _proficiency_bonus( target )
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
			"*Darkness cannot hide the truth from you.*\n\n"
			+ Darkvision_Rules(
				darkvision_range
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
	Project_Species_Feature(
		target,
		"Celestial Resistance",
		(
			"*Life flows through you. Death passes over you.*\n\n"
			"You have Resistance to Necrotic damage and Radiant damage."
			),
		chips=(
			Chip(
				"🛡️",
				"Resistances",
				"Necrotic, Radiant",
				),
			),
		level=1,
		)
	target.healing_hands_action = Healing_Hands.ACTION
	target.healing_hands_dice_count = proficiency
	target.healing_hands_die = Healing_Hands.DIE
	target.healing_hands_uses = Healing_Hands.USES
	target.healing_hands_recovery = Healing_Hands.RECOVERY
	Project_Species_Feature(
		target,
		"Healing Hands",
		(
			"*Life finds your way.*\n\n"
			f"As a {Healing_Hands.ACTION} action, you touch a creature and "
			f"roll {proficiency}d{Healing_Hands.DIE}. The creature regains a "
			"number of Hit Points equal to the total rolled. Once you use "
			"this trait, you can't use it again until you finish a "
			f"{Healing_Hands.RECOVERY}."
			),
		chips=(
			Chip(
				"🫴",
				"Healing Hands",
				f"{proficiency}d{Healing_Hands.DIE}",
				),
			Chip(
				"💛",
				"Healing Hands Uses",
				Healing_Hands.USES,
				),
			),
		level=1,
		)
	Resolve_Species_Spells(
		target,
		Light_Bearer.SPELLS,
		)
	target.species_spell_free_casts = {}
	Project_Species_Feature(
		target,
		"Light Bearer",
		(
			"*There is always a spark of light inside of you. "
			"Relentless.*\n\n"
			"You know the Light cantrip. Charisma is your spellcasting "
			"ability for it."
			),
		chips=(
			Chip(
				"🪄",
				"Spellcasting Ability",
				"Charisma",
				),
			),
		level=1,
		)
	_project_revelation( target )
