"""
Fighter Training Tags — 2024 PHB core + all Fighter Specializations.

Thought pattern
	1. Core lessons belong to the Fighter Guild (no path).
	2. Specialization lessons point to their Guild Shape and awaken only
	   when the Character carries that Shape.
	3. Mutable resources live as Character Records and concise Chips.
	   Full rules remain Entries.
	4. ASI / Epic Boon stay on legacy Progression.
	5. Fighting Styles stay in legacy (feat-pick workflow).
"""

from __future__ import annotations

from AtlasInventarium.ToolsKit import (
	ARTISAN_TOOLS as _ARTISAN_TOOL_DEFINITIONS,
	)
from AtlasLusoris.AtlasOfGuilds.FighterKit import (
	Apply_Battle_Master_Choices,
	ARTISAN_TOOLS,
	Banneret,
	BattleMaster,
	Champion,
	EldritchKnight,
	FIGHTER_SKILLS,
	Fighter,
	MANEUVERS,
	PsiWarrior,
	)
from AtlasLusoris.TrainingKit import Build_Training
from AtlasLusoris.FeaturesKit import grant


GUILD = "Fighter"
CORE_SOURCE = "Training: Fighter"
BATTLE_MASTER = BattleMaster
BANNERET = Banneret
CHAMPION = Champion
ELDRITCH_KNIGHT = EldritchKnight
PSI_WARRIOR = PsiWarrior


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _resource(
		owner,
		name: str,
		char,
		) -> str:
	resource = next(
		resource
		for resource in owner.RESOURCES
		if resource.name == name
		)
	return resource.at(
		_rank(
			char
			)
		)


def _second_wind_uses(
		char,
		) -> int:
	return int(
		_resource(
			Fighter,
			"Second Wind",
			char,
			)
		)


def _weapon_masteries(
		char,
		) -> int:
	choice = next(
		choice
		for choice in Fighter.CHOICES
		if choice.name == "Weapon Mastery"
		)
	return choice.total_at(
		_rank(
			char
			)
		)


def _action_surge_uses(
		char,
		) -> int:
	return int(
		_resource(
			Fighter,
			"Action Surge",
			char,
			)
		)


def _indomitable_uses(
		char,
		) -> int:
	return int(
		_resource(
			Fighter,
			"Indomitable",
			char,
			)
		)


def _superiority_dice(
		char,
		) -> str:
	return _resource(
		BattleMaster,
		"Superiority Dice",
		char,
		)


def _psionic_energy_dice(
		char,
		) -> str:
	return _resource(
		PsiWarrior,
		"Psionic Energy Dice",
		char,
		)


def _core(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return Build_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			source=CORE_SOURCE,
			)


def _path(
		path_shape,
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return Build_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			path=path_shape,
			source=f"Training: Fighter ({path_shape.NAME})",
			apply=apply,
			)


def _battle_master(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			BATTLE_MASTER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _champion(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			CHAMPION,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _eldritch_knight(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			ELDRITCH_KNIGHT,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _psi_warrior(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			PSI_WARRIOR,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


# ---------------------------------------------------------------------------
# Callable entry helpers
# ---------------------------------------------------------------------------


def _second_wind_entry(
		char,
		) -> str:
	uses = _second_wind_uses(char)
	# Resolved, not quoted as a formula.  The rulebook must serve every
	# Fighter at once; a generated sheet knows this one's level.
	return (
		"*You don't stay down. You fight.*\n\n"
		"As a <i>Bonus Action</i>, you can regain Hit Points equal to "
		f"<b>1d10 + {_rank( char )}</b>. "
		f"You can use this feature <b>{uses}</b> times. "
		"You regain one expended use when you finish a <i>Short Rest</i>, "
		"and you regain all expended uses when you finish a <i>Long Rest</i>."
		)


def _weapon_mastery_entry(
		char,
		) -> str:
	from AtlasLusoris.Map_of_Weapon_Masteries import weapon_mastery_entry
	return weapon_mastery_entry(
			char,
			lead=(
				"You trained. The weapon feels like an extension, not a tool."
				),
			)


def _weapon_mastery_chip(
		char,
		) -> str:
	from AtlasLusoris.Map_of_Weapon_Masteries import weapon_mastery_chip
	return weapon_mastery_chip(
			char
			)


def _extra_attack_entry(
		char,
		) -> str:
	level = _rank(char)
	if level >= 20:
		count = "four times"
	elif level >= 11:
		count = "three times"
	else:
		count = "twice"
	return (
		"*Your training made you formidable in combat.*\n\n"
		f"You can attack <b>{count}</b> instead of once whenever you "
		"take the Attack action on your turn."
		)


def _indomitable_entry(
		char,
		) -> str:
	level = _rank(char)
	if level >= 17:
		uses_text = "three times"
	elif level >= 13:
		uses_text = "twice"
	else:
		uses_text = "once"
	return (
		"*You don't fall down.*\n\n"
		"If you fail a saving throw, you can reroll it with a bonus of "
		f"<b>+{level}</b>. You must use the new roll."
		f"<br>You can use this feature <b>{uses_text}</b> per Long Rest."
		)


def _action_surge_entry(
		char,
		) -> str:
	level = _rank(char)
	# One lead for both branches, so the flavour cannot drift between them.
	lead = (
		"*It may be adrenaline, it may be bloodlust, it may be strategy. "
		"Whichever it is, you are unstoppable.*\n\n"
		)

	if level >= 17:
		return lead + (
			"On your turn, you can take one additional action, except "
			"the Magic action. You can use this feature <b>twice</b> "
			"per Short or Long Rest. You can use it only once per turn."
			)
	return lead + (
		"On your turn, you can take one additional action, except "
		"the Magic action. Once you use this feature, you can't do "
		"so again until you finish a <i>Short or Long Rest</i>."
		)


def _refresh_pool(
		char,
		*,
		current_name: str,
		maximum_name: str,
		maximum: int,
		) -> None:
	current = getattr(
		char,
		current_name,
		None,
		)
	previous_maximum = getattr(
		char,
		maximum_name,
		None,
		)
	setattr(
		char,
		maximum_name,
		maximum,
		)
	if current is None or previous_maximum is None:
		setattr(
			char,
			current_name,
			maximum,
			)
		return
	setattr(
		char,
		current_name,
		min(
				int(
						current
						),
				maximum,
				),
		)


def _apply_second_wind(
		char,
		) -> None:
	_refresh_pool(
		char,
		current_name="second_wind_uses",
		maximum_name="second_wind_uses_max",
		maximum=_second_wind_uses(
				char
				),
		)


def _apply_action_surge(
		char,
		) -> None:
	_refresh_pool(
		char,
		current_name="action_surge_uses",
		maximum_name="action_surge_uses_max",
		maximum=_action_surge_uses(
				char
				),
		)


def _apply_indomitable(
		char,
		) -> None:
	_refresh_pool(
		char,
		current_name="indomitable_uses",
		maximum_name="indomitable_uses_max",
		maximum=_indomitable_uses(
				char
				),
		)


def _dice_pool(
		value: str,
		) -> tuple[int, int]:
	count, die = value.lower().split(
		"d",
		maxsplit=1,
		)
	return (
		int(
			count
			),
		int(
			die
			),
		)


def _apply_combat_superiority(
		char,
		) -> None:
	selected = Apply_Battle_Master_Choices(
		char
		)
	count, die = _dice_pool(
		_superiority_dice(
			char
			)
		)
	char.superiority_die = die
	_refresh_pool(
		char,
		current_name="superiority_dice",
		maximum_name="superiority_dice_max",
		maximum=count,
		)

	existing = {
		getattr(
				feature,
				"name",
				None,
				)
		for feature in getattr(
				char,
				"features",
				(),
				)
		}
	for maneuver in selected:
		if maneuver.NAME in existing:
			continue
		grant(
			char,
			name=maneuver.NAME,
			description=maneuver.DESCRIPTION,
			source="Training: Fighter (Battle Master Maneuver)",
			level=3,
			)


_SKILL_ATTRIBUTES = {
	"Acrobatics": "Acrobatics",
	"Animal Handling": "Animal_Handling",
	"Athletics": "Athletics",
	"History": "History",
	"Insight": "Insight",
	"Intimidation": "Intimidation",
	"Perception": "Perception",
	"Persuasion": "Persuasion",
	"Survival": "Survival",
	}

# Student of War's tool names to their sheet attributes, from ToolsKit's one
# catalog (QST-0116): the old hand-kept copy listed each collapsed tool twice.
_TOOL_ATTRIBUTES = {
	tool.name: tool.legacy_attribute
	for tool in _ARTISAN_TOOL_DEFINITIONS
	}


def _untrained_choice(
		char,
		*,
		options: tuple[str, ...],
		attributes: dict[str, str],
		bag_purpose: str,
		) -> str:
	ordered = list(
		options
		)
	char.Dice_Bag(
		bag_purpose,
		version="1",
		namespace="GenLegendFighter",
		).shuffle(
			ordered
			)
	for name in ordered:
		proficiency = getattr(
			char.skills,
			attributes[
				name
				],
			)
		if getattr(
			proficiency,
			"proficiency_level",
			0,
			) < 1:
			return name
	return ordered[0]


def _apply_student_of_war(
		char,
		) -> None:
	Apply_Battle_Master_Choices(
		char
		)
	char.battle_master_skill = _untrained_choice(
		char,
		options=FIGHTER_SKILLS,
		attributes=_SKILL_ATTRIBUTES,
		bag_purpose="fighter.battle_master.student.skill",
		)
	char.battle_master_tool = _untrained_choice(
		char,
		options=ARTISAN_TOOLS,
		attributes=_TOOL_ATTRIBUTES,
		bag_purpose="fighter.battle_master.student.tool",
		)
	getattr(
		char.skills,
		_SKILL_ATTRIBUTES[
			char.battle_master_skill
			],
		).set_proficiency()
	getattr(
		char.skills,
		_TOOL_ATTRIBUTES[
			char.battle_master_tool
			],
		).set_proficiency()


def _student_of_war_entry(
		char,
		) -> str:
	return (
		"*Every battle is determined by one thing: preparation. "
		"And you are ready.*\n\n"
		"You gain proficiency with "
		f"<b>{char.battle_master_tool}</b> and "
		f"<b>{char.battle_master_skill}</b>."
		)


def _combat_superiority_entry(
		char,
		) -> str:
	maneuvers = ", ".join(
		getattr(
				char,
				"maneuvers",
				(),
				)
		)
	return (
		"*Every battle is a cosmos. You are the sun.*\n\n"
		"Your maneuvers use "
		f"<b>{_superiority_dice(char)}</b> Superiority Dice, restored "
		"after a Short or Long Rest. A maneuver save is "
		f"<b>DC {_maneuver_save_dc( char )}</b>."
		f"<br><b>Known maneuvers:</b> {maneuvers}."
		)


def _combat_superiority_update(
		die: int,
		) -> object:
	"""
	Build the entry for one of the two Superiority upgrades.

	These are not features in their own right. They are an actualization of
	Combat Superiority: the same pool, larger. So each one says what it changed
	and stops, and the live count stays in the single entry that owns it.

	Both other ways of writing it are worse. Spelled out as a total, it goes
	stale: "a total of 5" is still printed on an 18th-level sheet holding six.
	Resolved live, it contradicts itself, because "became d10s" and "you have
	6d12" are both true and read as an error side by side.
	"""
	def entry(
			char,
			) -> str:
		return (
			f"Your Superiority Dice became <b>d{die}s</b>, and you gained "
			"one more."
			)
	return entry


def _combat_superiority_update(
		die: int,
		) -> object:
	"""
	Build the entry for one of the two Superiority upgrades.

	These are not features in their own right, they are an actualization of
	Combat Superiority: the same pool, larger. So they say what changed and
	nothing else, and the live count stays in the one entry that owns it.
	Written out longhand they went stale, because "a total of 5" is still
	printed on an 18th-level sheet that is holding six.
	"""
	def entry(
			char,
			) -> str:
		count, current = _dice_pool(
			_superiority_dice(
				char
				)
			)
		return (
			f"Your Superiority Dice became <b>d{die}s</b>, and you gained "
			"one more. "
			f"You have <b>{count}d{current}</b> now, and a maneuver save is "
			f"<b>DC {_maneuver_save_dc( char )}</b>."
			)
	return entry


def _combat_superiority_update(
		die: int,
		) -> object:
	"""
	Build the entry for one of the two Superiority upgrades.

	These are not features in their own right, they are an actualization of
	Combat Superiority: the same pool, larger. So they say what changed and
	nothing else, and the live count stays in the one entry that owns it.
	Written out longhand they went stale, because "a total of 5" is still
	printed on an 18th-level sheet that is holding six.
	"""
	def entry(
			char,
			) -> str:
		count, current = _dice_pool(
			_superiority_dice(
				char
				)
			)
		return (
			f"Your Superiority Dice became <b>d{die}s</b>, and you gained "
			"one more. "
			f"You have <b>{count}d{current}</b> now, and a maneuver save is "
			f"<b>DC {_maneuver_save_dc( char )}</b>."
			)
	return entry


def _apply_psionic_power(
		char,
		) -> None:
	count, die = _dice_pool(
		_psionic_energy_dice(
			char
			)
		)
	char.psionic_energy_die = die
	_refresh_pool(
		char,
		current_name="psionic_energy_dice",
		maximum_name="psionic_energy_dice_max",
		maximum=count,
		)


def _apply_telekinetic_master(
		char,
		) -> None:
	from AtlasMagia.Lodge_of_Spells import Telekinesis

	names = {
		getattr(
				spell,
				"name",
				None,
				)
		for spell in getattr(
				char,
				"known_spells",
				(),
				)
		}
	if Telekinesis.name not in names:
		char.known_spells.append(
			Telekinesis
			)
	char.telekinesis_spellcasting_ability = PsiWarrior.MAGIC.ability
	char.telekinesis_uses_slot = PsiWarrior.MAGIC.uses_slot
	char.telekinesis_uses_components = PsiWarrior.MAGIC.uses_components
	char.telekinesis_requires_concentration = (
		PsiWarrior.MAGIC.requires_concentration
		)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Fighting_Style = _core(
		name="Fighting Style",
		min_level=1,
		description=(
			"You have a specific style of fighting as your specialty. "
			"Choose a Fighting Style feat, such as Defense or Great Weapon "
			"Fighting. You can't take the same Fighting Style feat more "
			"than once, even if you get to choose again."
			),
		)

Second_Wind = _core(
		name="Second Wind",
		min_level=1,
		description=_second_wind_entry,
		chips=(
				("2nd Wind Uses", _second_wind_uses),
				),
		apply=_apply_second_wind,
		)

Weapon_Mastery = _core(
		name="Weapon Mastery",
		min_level=1,
		description=_weapon_mastery_entry,
		chips=(
				("Weapon Masteries", _weapon_mastery_chip),
				),
		)

Action_Surge = _core(
		name="Action Surge",
		min_level=2,
		description=_action_surge_entry,
		chips=(
				(
					"Action Surge Uses",
					_action_surge_uses,
					),
				),
		apply=_apply_action_surge,
		)

Tactical_Mind = _core(
		name="Tactical Mind",
		min_level=2,
		description=(
			"*You have a mind for tactics on and off the battlefield.*\n\n"
			"When you fail an ability check, you can expend a use of "
			"your Second Wind to push yourself toward success. Rather "
			"than regaining Hit Points, you roll 1d10 and add the number "
			"rolled to the ability check, potentially turning it into a "
			"success. If the check still fails, this use of Second Wind "
			"isn't expended."
			),
		)

Extra_Attack = _core(
		name="Extra Attack",
		min_level=5,
		description=_extra_attack_entry,
		)

Tactical_Shift = _core(
		name="Tactical Shift",
		min_level=5,
		description=(
			"*You know how to move through the enemy's line.*\n\n"
			"Whenever you activate your Second Wind with a Bonus Action, "
			"you can move up to half your Speed without provoking "
			"Opportunity Attacks."
			),
		)

Indomitable = _core(
		name="Indomitable",
		min_level=9,
		description=_indomitable_entry,
		chips=(
				(
					"Indomitable Uses",
					_indomitable_uses,
					),
				),
		apply=_apply_indomitable,
		)

Tactical_Master = _core(
		name="Tactical Master",
		min_level=9,
		description=(
			"*Your weapon is just an extension of your arm.*\n\n"
			"When you attack with a weapon whose mastery property you "
			"can use, you can replace that property with the Push, Sap, "
			"or Slow property for that attack."
			),
		)

Studied_Attacks = _core(
		name="Studied Attacks",
		min_level=13,
		description=(
			"*You study your opponents and learn from each attack you make.*\n\n"
			"If you make an attack roll against a creature and miss, you "
			"have Advantage on your next attack roll against that creature "
			"before the end of your next turn."
			),
		)


# ---------------------------------------------------------------------------
# Battle Master (3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


Combat_Superiority = _battle_master(
		name="Combat Superiority",
		min_level=3,
		description=_combat_superiority_entry,
		chips=(
				(
					"Superiority Dice",
					_superiority_dice,
					),
				),
		apply=_apply_combat_superiority,
		)

Student_of_War = _battle_master(
		name="Student of War",
		min_level=3,
		description=_student_of_war_entry,
		apply=_apply_student_of_war,
		)

Know_Your_Enemy = _battle_master(
		name="Know Your Enemy",
		min_level=7,
		description=(
			# The feature's own name is the first half of the sentence, which
			# is why this one opens on "Then".
			"*Then know yourself, and a hundred battles hold nothing to "
			"fear.*\n\n"
			"As a Bonus Action, study a creature you can see within 30 feet. "
			"You learn all of its damage Immunities, Resistances, and "
			"Vulnerabilities. You can do so once per Long Rest, and can "
			"restore the use by expending a Superiority Die."
			),
		)

Improved_Combat_Superiority = _battle_master(
		name="Improved Combat Superiority",
		min_level=10,
		description=_combat_superiority_update( 10 ),
		# No chip: Combat Superiority owns the number, and its callable
		# already returns 5d10 at this rank. A second declaration put a
		# stale duplicate on the rail.
		)

Relentless = _battle_master(
		name="Relentless",
		min_level=15,
		description=(
			"*Mind, blade and body have the same purpose.*\n\n"
			"Once per turn when you use a maneuver, you can roll <b>1d8</b> "
			"instead of expending a Superiority Die."
			),
		)

Ultimate_Combat_Superiority = _battle_master(
		name="Ultimate Combat Superiority",
		min_level=18,
		description=_combat_superiority_update( 12 ),
		# No chip — see Improved Combat Superiority above.
		)


# ---------------------------------------------------------------------------
# Champion (3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Banneret — Forgotten Realms: Heroes of Faerun (2024)
# ---------------------------------------------------------------------------


def _banneret(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			BANNERET,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _maneuver_save_dc(
		char,
		) -> int:
	"""
	A Battle Master maneuver's save DC, resolved.

	RAW lets the Character choose Strength or Dexterity each time, so the
	sheet prints the better of the two: nobody elects the worse modifier, and
	printing a formula where every other DC on the sheet is a number is what
	the house rule forbids.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	best = max(
			int(
				getattr(
					scores,
					"str_mod",
					0,
					) or 0
				),
			int(
				getattr(
					scores,
					"dex_mod",
					0,
					) or 0
				),
			)
	proficiency = int(
			getattr(
				char,
				"proficiency_bonus",
				2,
				) or 2
			)
	return 8 + proficiency + best


def _psionic_save_dc(
		char,
		) -> int:
	"""
	A Psi Warrior's Telekinetic Thrust save DC, resolved.

	Every other DC on the sheet is a number, and this one was a formula: the
	reader was being asked to add up their own proficiency and Intelligence
	while the sheet already knew both.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	intelligence = int(
			getattr(
					scores,
					"int_mod",
					0,
					) or 0
			)
	proficiency = int(
			getattr(
				char,
				"proficiency_bonus",
				2,
				) or 2
			)
	return 8 + proficiency + intelligence


def _psionic_save_dc(
		char,
		) -> int:
	"""
	A Psi Warrior's Telekinetic Thrust save DC, resolved.

	Every other DC on the sheet is a number, and this one was a formula: the
	reader was being asked to add up their own proficiency and Intelligence
	while the sheet already knew both.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	intelligence = int(
			getattr(
					scores,
					"int_mod",
					0,
					) or 0
			)
	proficiency = int(
			getattr(
				char,
				"proficiency_bonus",
				2,
				) or 2
			)
	return 8 + proficiency + intelligence


def _psionic_save_dc(
		char,
		) -> int:
	"""
	A Psi Warrior's Telekinetic Thrust save DC, resolved.

	Every other DC on the sheet is a number, and this one was a formula: the
	reader was being asked to add up their own proficiency and Intelligence
	while the sheet already knew both.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	intelligence = int(
			getattr(
					scores,
					"int_mod",
					0,
					) or 0
			)
	proficiency = int(
			getattr(
				char,
				"proficiency_bonus",
				2,
				) or 2
			)
	return 8 + proficiency + intelligence


def _constitution_modifier(
		char,
		) -> int:
	scores = getattr(
			char,
			"AS",
			None,
			)
	return int(
			getattr(
					scores,
					"con_mod",
					0,
					) or 0
			)


def _charisma_modifier(
		char,
		) -> int:
	"""The Charisma modifier, floored at 1 where a feature says minimum one."""
	scores = getattr(
			char,
			"AS",
			None,
			)
	return int(
			getattr(
					scores,
					"cha_mod",
					0,
					) or 0
			)


def _rallied_allies(
		char,
		) -> int:
	"""How many allies a Banneret can lift at once: Charisma modifier, min 1."""
	return max(
			1,
			_charisma_modifier(
					char
					),
			)


def _allies_phrase(
		char,
		) -> str:
	"""``1 ally`` or ``3 allies`` — the count, agreeing with its noun."""
	count = _rallied_allies(
			char
			)
	return f"<b>{count}</b> all{'y' if count == 1 else 'ies'}"


def _emanation(
		char,
		) -> int:
	"""30 feet, widened to 60 by Inspiring Commander at level 18."""
	return 60 if _rank( char ) >= 18 else 30


def _group_recovery_entry(
		char,
		) -> str:
	return (
		"***We** don't stay down.*\n\n"
		"When you use your Second Wind to regain Hit Points, you can "
		f"choose up to {_allies_phrase( char )} within a "
		f"<b>{_emanation( char )}-foot Emanation</b> originating from "
		"yourself. Each of them regains "
		f"<b>1d4 + {_rank( char )}</b> Hit Points. Once you use this "
		"ability, you can't use it again until you finish a Short or "
		"Long Rest."
		)


def _rallying_surge_entry(
		char,
		) -> str:
	return (
		"***We** will push through.*\n\n"
		"When you use your Action Surge, you can choose up to "
		f"{_allies_phrase( char )} within a "
		f"<b>{_emanation( char )}-foot Emanation</b> originating from "
		"yourself. Each of them can immediately take a Reaction to use "
		"one of the following options."
		"<br><b>Attack.</b> The ally makes one attack with a weapon or "
		"an Unarmed Strike."
		"<br><b>Move.</b> The ally moves up to half its Speed without "
		"provoking Opportunity Attacks."
		)


def _shared_resilience_entry(
		char,
		) -> str:
	return (
		"***We** don't fall.*\n\n"
		"When an ally you can see within 60 feet of yourself fails a "
		"saving throw, you can take a Reaction to expend a use of your "
		"Indomitable feature. The ally immediately rerolls the saving "
		f"throw with a bonus of <b>+{_rank( char )}</b>, and must use "
		"the new roll."
		)


Knightly_Envoy = _banneret(
		name="Knightly Envoy",
		min_level=3,
		description=(
			"*A blade opens one kind of door. Manners open the rest.*\n\n"
			"<b>Comprehension.</b> You can cast <i>Comprehend Languages</i> "
			"but only as a Ritual. Charisma is your spellcasting ability "
			"for it."
			"<br><b>Polyglot.</b> You know one additional language. When "
			"you finish a Long Rest, you can replace it with another "
			"language you have heard, seen signed, or read in the past 24 "
			"hours."
			"<br><b>Well Spoken.</b> You are proficient in one of Insight, "
			"Intimidation, Persuasion, or Performance."
			),
		)

Group_Recovery = _banneret(
		name="Group Recovery",
		min_level=3,
		description=_group_recovery_entry,
		chips=(
				(
					"Rallied Allies",
					_rallied_allies,
					"\U0001F6E1",
					),
				),
		)

Team_Tactics = _banneret(
		name="Team Tactics",
		min_level=7,
		description=(
			"***We** hold the line.*\n\n"
			"When you use Group Recovery, each chosen ally has Advantage "
			"on D20 Tests until the start of your next turn."
			),
		)

Rallying_Surge = _banneret(
		name="Rallying Surge",
		min_level=10,
		description=_rallying_surge_entry,
		)

Shared_Resilience = _banneret(
		name="Shared Resilience",
		min_level=15,
		description=_shared_resilience_entry,
		)

Inspiring_Commander = _banneret(
		name="Inspiring Commander",
		min_level=18,
		description=(
			"***We** will be victorious.*\n\n"
			"<b>Bolstered Rally.</b> The area of effect for both Group "
			"Recovery and Rallying Surge is now a <b>60-foot Emanation</b>."
			"<br><b>Unshakable Bravery.</b> You have Immunity to the "
			"Charmed and Frightened conditions."
			),
		)


# The Champion's Entries thread Eye of the Tiger, because the level 18 feature
# is named Survivor and so was the band.  Each line is written to stand on its
# own as sports-hype for a reader who does not catch it, which is what keeps
# the joke free rather than exclusionary.  Do not flatten them.
Improved_Critical = _champion(
		name="Improved Critical",
		min_level=3,
		description=(
			"*Take your time. Take your chances.*\n\n"
			"Your attack rolls with weapons and Unarmed Strikes can score "
			"a <b>Critical Hit on a roll of 19 or 20</b> on the d20."
			),
		)

Remarkable_Athlete = _champion(
		name="Remarkable Athlete",
		min_level=3,
		description=(
			"*Rising up to the challenge.*\n\n"
			"Thanks to your athleticism, you have <b>Advantage on "
			"Initiative rolls and Strength (Athletics) checks</b>."
			"<br>In addition, immediately after you score a Critical Hit, "
			"you can move up to half your Speed without provoking "
			"Opportunity Attacks."
			),
		)

Additional_Fighting_Style = _champion(
		name="Additional Fighting Style",
		min_level=7,
		# NOTE: this Entry never reaches a sheet.  TrainingKit._awaken_training
		# suppresses "Additional Fighting Style" on purpose, because the second
		# Fighting Style feat the Character actually picks (Dueling, Defense,
		# and so on) prints its own Entry, and a generic "you gain another
		# style" line would sit above it saying nothing.  The flavour line is
		# kept against the day that suppression is lifted; it is not live.
		description=(
			"*Time for plan B.*\n\n"
			"You gain another Fighting Style feat of your choice."
			),
		)

Heroic_Warrior = _champion(
		name="Heroic Warrior",
		min_level=10,
		description=(
			"*Rising up, back in the arena.*\n\n"
			"The thrill of battle drives you toward victory. During "
			"combat, you can give yourself <b>Heroic Inspiration</b> "
			"whenever you start your turn without it."
			),
		)

Superior_Critical = _champion(
		name="Superior Critical",
		min_level=15,
		description=(
			"*You have the will and the skill to survive.*\n\n"
			"Your attack rolls with weapons and Unarmed Strikes can now "
			"score a Critical Hit on a roll of <b>18–20</b> on the d20."
			),
		)

Survivor = _champion(
		name="Survivor",
		min_level=18,
		description=lambda char: (
			"*Go the distance. Get back on your feet.*\n\n"
			"You attain the pinnacle of resilience in battle."
			"<br><b>Defy Death.</b> You have Advantage on Death Saving "
			"Throws. Moreover, when you roll 18–20 on a Death Saving "
			"Throw, you gain the benefit of rolling a 20 on it."
			"<br><b>Heroic Rally.</b> At the start of each of your turns, "
			"you regain "
			f"<b>{5 + _constitution_modifier( char )}</b> Hit Points "
			"if you are Bloodied and have at least 1 Hit Point."
			),
		)


# ---------------------------------------------------------------------------
# Eldritch Knight (3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


Spellcasting_EK = _eldritch_knight(
		name="Spellcasting",
		min_level=3,
		description=(
			"You augment your martial prowess with the ability to cast "
			"Wizard spells. At level 3 you know two Wizard cantrips and "
			"prepare three level 1 Wizard spells. Intelligence is your "
			"spellcasting ability, and you can use an Arcane Focus."
			),
		)

War_Bond = _eldritch_knight(
		name="War Bond",
		min_level=3,
		description=(
			"*A wizard needs a pen. You need something mightier.*\n\n"
			"*A wizard needs a pen. You need something mightier.*\n\n"
			"*A wizard needs a pen. You need something mightier.*\n\n"
			"You learn a ritual that creates a magical bond between "
			"yourself and one weapon. You perform the ritual over 1 hour "
			"(possible during a Short Rest). The bond fails if another "
			"Fighter is bonded to that weapon, or if it is a magic item "
			"to which someone else is attuned. Once bonded, you can't be "
			"disarmed of that weapon unless you have the Incapacitated "
			"condition. If it's on the same plane of existence, you can "
			"summon it as a <i>Bonus Action</i>."
			"<br>You can have up to <b>two bonded weapons</b>, but can "
			"summon only one at a time. Bonding a third weapon breaks "
			"one existing bond of your choice."
			),
		)

War_Magic = _eldritch_knight(
		name="War Magic",
		min_level=7,
		description=(
			"*Swinging the wand, or swinging the blade. You know the moves "
			"for both.*\n\n"
			"When you take the Attack action on your turn, you can replace "
			"one of the attacks with a casting of one of your Wizard "
			"cantrips that has a casting time of an action."
			),
		)

Eldritch_Strike = _eldritch_knight(
		name="Eldritch Strike",
		min_level=10,
		description=(
			"*You know how to find a magical weak spot. That's your best trick.*\n\n"
			"*You know how to find a weak spot.*\n\n"
			"*You know how to find a weak spot.*\n\n"
			"When you hit a creature with an attack using a weapon, that "
			"creature has <b>Disadvantage on the next saving throw</b> it "
			"makes against a spell you cast before the end of your "
			"next turn."
			),
		)

Arcane_Charge = _eldritch_knight(
		name="Arcane Charge",
		min_level=15,
		description=(
			"*You are not sure how it works, but it works like a charm.*\n\n"
			"*You are not sure how it works, but it works like a charm.*\n\n"
			"*You are not sure how it works, but it works like a charm.*\n\n"
			"When you use your Action Surge, you can <b>teleport up to "
			"30 feet</b> to an unoccupied space you can see. You can "
			"teleport before or after the additional action."
			),
		)

Improved_War_Magic = _eldritch_knight(
		name="Improved War Magic",
		min_level=18,
		description=(
			"*The tricks have outgrown the bag.*\n\n"
			"When you take the Attack action on your turn, you can replace "
			"<b>two</b> of the attacks with a casting of one of your "
			"level 1 or level 2 Wizard spells that has a casting time "
			"of an action."
			),
		)


# ---------------------------------------------------------------------------
# Psi Warrior (3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


def _psionic_power_entry(
		char,
		) -> str:
	return (
		"*May the power be in you.*\n\n"
		f"You have <b>{_psionic_energy_dice(char)}</b> Psionic Energy Dice "
		"that fuel your powers. You regain one expended die after a Short "
		"Rest and all expended dice after a Long Rest."
		"<br><b>Protective Field.</b> When you or a creature you can see "
		"within 30 feet takes damage, you can take a Reaction to expend "
		"one Psionic Energy Die, roll it, and reduce the damage by the "
		"number rolled plus your Intelligence modifier (minimum 1)."
		"<br><b>Psionic Strike.</b> Once per turn after a weapon damages "
		"a target within 30 feet, you can expend "
		"one Psionic Energy Die, rolling it to deal <b>Force damage</b> "
		"to the target equal to the roll plus your Intelligence modifier."
		"<br><b>Telekinetic Movement.</b> As a Magic action, move one Large "
		"or smaller loose object or willing creature within 30 feet up to "
		"30 feet. This is free once per Short or Long Rest; expending a "
		"Psionic Energy Die restores the use."
		)


Psionic_Power = _psi_warrior(
		name="Psionic Power",
		min_level=3,
		description=_psionic_power_entry,
		chips=(
				(
					"Psionic Energy Dice",
					_psionic_energy_dice,
					),
				),
		apply=_apply_psionic_power,
		)

def _telekinetic_adept_entry(
		char,
		) -> str:
	return (
		"*You master yourself, then you master your surroundings, then "
		"you master others.*\n\n"
		"<b>Psi-Powered Leap.</b> As a Bonus Action, you gain a "
		"Fly Speed equal to twice your Speed until the end of the "
		"current turn. This is free once per Short or Long Rest; "
		"expending a Psionic Energy Die restores the use."
		"<br><b>Telekinetic Thrust.</b> When you deal damage with your "
		"Psionic Strike, you can force the target to make a Strength "
		f"saving throw against <b>DC {_psionic_save_dc( char )}</b>. "
		"On a failed save, you can knock the target Prone or move it "
		"up to 10 feet in any direction horizontally."
		)


Telekinetic_Adept = _psi_warrior(
		name="Telekinetic Adept",
		min_level=7,
		description=_telekinetic_adept_entry,
		chips=(
				(
					"Psionic Save DC",
					_psionic_save_dc,
					),
				),
		)

Guarded_Mind = _psi_warrior(
		name="Guarded Mind",
		min_level=10,
		description=(
			"*You mastered your mind, so no one else has dominion over "
			"it.*\n\n"
			"You have <b>Resistance to Psychic damage</b>. Moreover, "
			"if you start your turn Charmed or Frightened, you can expend "
			"one Psionic Energy Die (no action required) to end every "
			"effect on yourself giving you those conditions."
			),
		)

Bulwark_of_Force = _psi_warrior(
		name="Bulwark of Force",
		min_level=15,
		description=(
			"*Your power is the shield. You are the protector, the "
			"guardian, the first one standing.*\n\n"
			"As a Bonus Action, choose creatures (including yourself) "
			"within 30 feet of you up to your Intelligence modifier "
			"(minimum 1). Each chosen creature gains <b>Half Cover</b> "
			"for 1 minute or until you have the Incapacitated condition."
			"<br>Once you use this feature, you can't do so again until "
			"you finish a Long Rest unless you expend a Psionic Energy Die "
			"(no action required) to restore your use of it."
			),
		)

Telekinetic_Master = _psi_warrior(
		name="Telekinetic Master",
		min_level=18,
		description=(
			"*Power is the most ancient rule.*\n\n"
			"You always have <i>Telekinesis</i> prepared and can cast "
			"it without a spell slot or components using Intelligence. "
			"It still requires Concentration. While concentrating on it, "
			"you can make one weapon attack as a Bonus Action on each turn."
			"<br>The slotless casting returns after a Long Rest; expending "
			"a Psionic Energy Die restores it sooner."
			),
		apply=_apply_telekinetic_master,
		)
