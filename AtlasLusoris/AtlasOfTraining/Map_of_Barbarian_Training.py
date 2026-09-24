"""
Barbarian Training Tags — 2024 PHB core + all Paths.

Thought pattern
	1. Core lessons belong to the Barbarian Guild (no Path).
	2. Path lessons set ``path=…`` and awaken only for that Path.
	3. Numbers (Rage uses, Rage damage, Weapon Masteries) live as Chips
	   and in callable Entries — not as separate Tag members.
	4. ASI / Epic Boon stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
		Unarmored_Armour_Class,
		)


GUILD = "Barbarian"
CORE_SOURCE = "Training: Barbarian"
BERSERKER = "Berserker"
WILD_HEART = "Wild Heart"
WORLD_TREE = "World Tree"
ZEALOT = "Zealot"

# Barbarian Features table (2024) — Rages / Rage Damage / Weapon Mastery
_RAGE_USES = (
		0,
		2, 2, 3, 3, 3, 4, 4, 4, 4, 4,
		4, 5, 5, 5, 5, 5, 6, 6, 6, 6,
		)
_RAGE_DAMAGE = (
		0,
		2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
		3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
		)
_WEAPON_MASTERIES = (
		0,
		2, 2, 2, 3, 3, 3, 3, 3, 3, 4,
		4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
		)


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _table_at(
		table: tuple,
		char,
		) -> int:
	level = max(
			1,
			min(
					20,
					_rank(
							char
							),
					),
			)
	return table[level]


def _rage_uses(
		char,
		) -> int:
	return _table_at(
			_RAGE_USES,
			char,
			)


def _strength_save_dc(
		char,
		) -> int:
	"""
	DC 8 plus Strength modifier plus Proficiency Bonus, resolved.

	The rulebook prints the formula because it must serve every character at
	once.  A generated sheet knows the Character, so it prints the number.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	# ``AS`` publishes the three-letter names and a matching ``str_mod``.  It
	# does NOT answer to "Strength": asking for that returns the default and
	# every DC silently comes out as though the Barbarian had a 10.
	modifier = getattr(
			scores,
			"str_mod",
			None,
			)

	if modifier is None:
		modifier = (
			int(
				getattr(
					scores,
					"STR",
					10,
					)
				)
			- 10
			) // 2
	proficiency = int(
			getattr(
				char,
				"proficiency_bonus",
				2,
				)
			)
	return 8 + proficiency + int( modifier )


def _rage_damage(
		char,
		) -> int:
	return _table_at(
			_RAGE_DAMAGE,
			char,
			)


def _weapon_masteries(
		char,
		) -> int:
	return _table_at(
			_WEAPON_MASTERIES,
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
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			source=CORE_SOURCE,
			)


def _path(
		path_name: str,
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			path=path_name,
			source=f"Training: Path of the {path_name}",
			)


def _berserker(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			BERSERKER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


def _rage_entry(
		char,
		) -> str:
	uses = _rage_uses(
			char
			)
	bonus = _rage_damage(
			char
			)
	return (
		"You can imbue yourself with a primal power called <b>Rage</b>, "
		"a force that grants you extraordinary might and resilience. "
		"You can enter it as a <i>Bonus Action</i> if you aren't wearing "
		"Heavy armor."
		f"<br>You can enter your Rage <b>{uses}</b> times. "
		"You regain one expended use when you finish a <i>Short Rest</i>, "
		"and you regain all expended uses when you finish a <i>Long Rest</i>."
		"<br>While active, your Rage follows these rules:"
		"<ul>"
		"<li><b>Damage Resistance.</b> You have Resistance to Bludgeoning, "
		"Piercing, and Slashing damage.</li>"
		"<li><b>Rage Damage.</b> When you make an attack using Strength "
		"— with a weapon or an Unarmed Strike — and deal damage, "
		f"add <b>+{bonus}</b> to that damage.</li>"
		"<li><b>Strength Advantage.</b> You have Advantage on Strength "
		"checks and Strength saving throws.</li>"
		"<li><b>No Concentration or Spells.</b> You can't maintain "
		"Concentration, and you can't cast spells.</li>"
		"<li><b>Duration.</b> The Rage lasts until the end of your next "
		"turn, and it ends early if you don Heavy armor or have the "
		"Incapacitated condition. You can extend it for another round by "
		"making an attack roll against an enemy, forcing an enemy to make "
		"a saving throw, or taking a Bonus Action to extend the Rage. "
		"You can maintain a Rage for up to 10 minutes.</li>"
		"</ul>"
		)


def _mastery_text(
		mastery: str,
		char,
		) -> str:
	"""One mastery property's rules line, with its DC resolved."""
	from AtlasLusoris.Map_of_Weapon_Masteries import mastery_blurb
	return mastery_blurb(
			mastery,
			char,
			)


def _weapon_mastery_entry(
		char,
		) -> str:
	from AtlasLusoris.Map_of_Weapon_Masteries import weapon_mastery_entry
	return weapon_mastery_entry(
			char
			)


def _weapon_mastery_chip(
		char,
		) -> str:
	from AtlasLusoris.Map_of_Weapon_Masteries import weapon_mastery_chip
	return weapon_mastery_chip(
			char
			)


def _brutal_strike_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	die = "2d10" if level >= 17 else "1d10"
	two = (
			" You can use two different Brutal Strike effects whenever "
			"you use this feature."
			if level >= 17
			else ""
			)
	options = (
		"<br><b>Forceful Blow.</b> The target is pushed 15 feet straight "
		"away from you. You can then move up to half your Speed straight "
		"toward the target without provoking Opportunity Attacks."
		"<br><b>Hamstring Blow.</b> The target's Speed is reduced by "
		"15 feet until the start of your next turn. A target can be "
		"affected by only one Hamstring Blow at a time — the most recent one."
		)
	if level >= 13:
		options += (
			"<br><b>Staggering Blow.</b> The target has Disadvantage on "
			"the next saving throw it makes, and it can't make Opportunity "
			"Attacks until the start of your next turn."
			"<br><b>Sundering Blow.</b> Before the start of your next turn, "
			"the next attack roll made by another creature against the "
			"target gains a +5 bonus to the roll. An attack roll can gain "
			"only one Sundering Blow bonus."
			)
	return (
		"*You focus not on hitting, but on brutally ending the combat.*\n\n"
		"If you use Reckless Attack, you can forgo any Advantage on one "
		"Strength-based attack roll of your choice on your turn. The "
		"chosen attack roll mustn't have Disadvantage. If it hits, the "
		f"target takes an extra <b>{die}</b> damage of the same type dealt "
		"by the weapon or Unarmed Strike, and you can cause one Brutal "
		f"Strike effect of your choice.{two}"
		f"<br>You have the following effect options:{options}"
		)


def _apply_primal_champion(
		char,
		) -> None:
	abilities = getattr(
			char,
			"abilities",
			None,
			)
	if abilities is None:
		return
	from AtlasLusoris.Grimoire_of_Features import raise_stat
	raise_stat(
			char,
			"STR",
			4,
			cap=25,
			)
	raise_stat(
			char,
			"CON",
			4,
			cap=25,
			)


def _frenzy_entry(
		char,
		) -> str:
	dice = _rage_damage(
			char
			)
	return (
		"*Your fury is the eye of the storm, and you strike like "
		"thunder.*\n\n"
		"If you use Reckless Attack while your Rage is active, you deal "
		"extra damage to the first target you hit on your turn with a "
		"Strength-based attack. To determine the extra damage, roll "
		f"<b>{dice}d6</b> and add them together. The damage has the same "
		"type as the weapon or Unarmed Strike used for the attack."
		)


Rage = _core(
		name="Rage",
		min_level=1,
		description=_rage_entry,
		chips=(
				("Rage Uses", _rage_uses),
				("Rage Damage", _rage_damage),
				),
		)

def _unarmored_defense_entry(
		char,
		) -> str:
	armour_class = Unarmored_Armour_Class( char )

	return (
			"*You trust your reflexes more than any material.*\n\n"
			"While you aren't wearing any armor, your base Armor Class "
			f"equals <b>{armour_class}</b> (10 + Dexterity modifier + "
			"Constitution modifier). You can use a Shield and still gain "
			"this benefit."
			)


Unarmored_Defense = _core(
		name="Unarmored Defense",
		min_level=1,
		description=_unarmored_defense_entry,
		chips=(
				("Unarmored AC", Unarmored_Armour_Class, "🛡️"),
				),
		)

Weapon_Mastery = _core(
		name="Weapon Mastery",
		min_level=1,
		description=_weapon_mastery_entry,
		chips=(
				("Weapon Masteries", _weapon_mastery_chip),
				),
		)

Danger_Sense = _core(
		name="Danger Sense",
		min_level=2,
		description=(
			"*You can sense when things aren't as they should be, giving "
			"you an edge against perils.*\n\n"
			"You have Advantage on Dexterity saving throws unless you have "
			"the Incapacitated condition."
			),
		)

Reckless_Attack = _core(
		name="Reckless Attack",
		min_level=2,
		description=(
			"*You can throw aside all concern for defense to attack with "
			"increased ferocity.*\n\n"
			"When you make your first attack roll on "
			"your turn, you can decide to attack recklessly. Doing so "
			"gives you Advantage on attack rolls using Strength until the "
			"start of your next turn, but attack rolls against you have "
			"Advantage during that time."
			),
		)

# The level-1 Barbarian skill list, exactly as the Core Barbarian Traits table
# gives it.  Primal Knowledge draws its extra proficiency from the same list.
BARBARIAN_SKILLS = (
	"Animal Handling",
	"Athletics",
	"Intimidation",
	"Nature",
	"Perception",
	"Survival",
	)


def Grant_Primal_Knowledge_Skill(
		char,
		) -> None:
	"""
	Take Primal Knowledge's extra skill, and record which one it was.

	The Guild grants a Barbarian two skills; this feature grants the third.  The
	rule lives here, with the feature that owns it, but it cannot run from the
	feature's ``apply`` hook: Trainings are applied long before the character
	builder assigns class skills, so ``char.skills`` does not exist yet at that
	point.  The builder calls this instead, at the moment the other two are
	granted.

	Recording the name is the whole point.  The entry can then say which skill
	was gained rather than offering the reader a choice the generator already
	made on their behalf.
	"""
	skills = getattr(
		char,
		"skills",
		None,
		)

	if skills is None or getattr( char, "primal_knowledge_skill", None ):
		return

	untrained = [
		name
		for name in BARBARIAN_SKILLS
		if getattr(
			getattr(
				skills,
				name.replace( " ", "_" ),
				None,
				),
			"proficiency_level",
			0,
			) < 1
		]

	if not untrained:
		char.primal_knowledge_skill = ""
		return

	chosen = char.Pick(
		untrained,
		dice=char.Dice_Bag(
			"barbarian.primal_knowledge",
			version="1",
			namespace="GenLegendTraining",
			),
		)
	getattr(
		skills,
		chosen.replace( " ", "_" ),
		).set_proficiency()
	char.primal_knowledge_skill = chosen


def _primal_knowledge_entry(
		char,
		) -> str:
	# Past tense, because the pick already happened.  The second half stays in
	# the present and stays open: choosing to make a check with Strength is a
	# decision taken at the table, every time, and resolving it would be wrong.
	#
	# Three states, deliberately distinguished.  A recorded name is printed; an
	# empty string means we looked and the Character was already trained in all
	# six; a missing attribute means this ran outside the normal build, and must
	# not be reported as though it were the second case.
	gained = getattr(
		char,
		"primal_knowledge_skill",
		None,
		)

	lead = (
		"*Your path as a Barbarian keeps teaching you what you need.*\n\n"
		)

	if gained:
		opening = f"You learnt <b>{gained}</b>. "
	elif gained == "":
		opening = (
			"You were already trained in every skill a Barbarian learns, so "
			"your Rage sharpened what you had. "
			)
	else:
		opening = "Your Rage taught you one more of a Barbarian's skills. "

	return (
		lead
		+ opening
		+ "In addition, while your Rage is active, you can channel primal "
		"power when you attempt certain tasks. Whenever you make an ability "
		"check using Acrobatics, Intimidation, Perception, Stealth, or "
		"Survival, you can make it as a Strength check even if it normally "
		"uses a different ability. When you use this ability, your Strength "
		"represents primal power coursing through you, honing your agility, "
		"bearing, and senses."
		)


Primal_Knowledge = _core(
		name="Primal Knowledge",
		min_level=3,
		description=_primal_knowledge_entry,
		)

Extra_Attack = _core(
		name="Extra Attack",
		min_level=5,
		description=(
			"*Your skills in combat grow as you walk your path.*\n\n"
			"You can attack twice instead of once whenever you take the "
			"Attack action on your turn."
			),
		)

Fast_Movement = _core(
		name="Fast Movement",
		min_level=5,
		description=(
			"*You push yourself further.*\n\n"
			"Your speed increases by 10 feet while you aren't wearing "
			"Heavy armor."
			),
		)

Feral_Instinct = _core(
		name="Feral Instinct",
		min_level=7,
		description=(
			"*Your awareness prepares you for combat at any moment.*\n\n"
			"Your instincts are so honed that you have Advantage on "
			"Initiative rolls."
			),
		)

Instinctive_Pounce = _core(
		name="Instinctive Pounce",
		min_level=7,
		description=(
			"*Your instinct activates with a burst of energy.*\n\n"
			"As part of the Bonus Action you take to enter your Rage, "
			"you can move up to half your Speed."
			),
		)

Brutal_Strike = _core(
		name="Brutal Strike",
		min_level=9,
		description=_brutal_strike_entry,
		chips=(
				("Brutal Strike", lambda c: "2d10" if _rank(c) >= 17 else "1d10"),
				),
		)

Relentless_Rage = _core(
		name="Relentless Rage",
		min_level=11,
		description=(
			"*Your will is unstoppable. You rage against death itself.*\n\n"
			"Your Rage can keep you fighting despite grievous wounds. "
			"If you drop to 0 Hit Points while your Rage is active and "
			"don't die outright, you can make a DC 10 Constitution "
			"saving throw. If you succeed, your Hit Points instead change "
			"to a number equal to twice your Barbarian level."
			"<br>Each time you use this feature after the first, the DC "
			"increases by 5. When you finish a Short or Long Rest, the "
			"DC resets to 10."
			),
		)

# L13 options fold into Brutal Strike's callable Entry once earned.
Persistent_Rage = _core(
		name="Persistent Rage",
		min_level=15,
		description=(
			"*You understand your path. Your rage grows stronger, and you "
			"lose yourself in it more.*\n\n"
			"When you roll Initiative, you can regain all expended uses "
			"of Rage. After you regain uses of Rage in this way, you "
			"can't do so again until you finish a Long Rest."
			"<br>In addition, your Rage now lasts for 10 minutes without "
			"you needing to extend it from round to round. Your Rage ends "
			"early if you have the Unconscious condition (not just "
			"Incapacitated) or don Heavy armor."
			),
		)

# 2024 also names level 17 "Improved Brutal Strike"; distinct title avoids
Indomitable_Might = _core(
		name="Indomitable Might",
		min_level=18,
		description=(
			"*Your mighty body can react on its own. Unguided.*\n\n"
			"If your total for a Strength check or Strength saving throw "
			"is less than your Strength score, you can use that score in "
			"place of the total."
			),
		)

Primal_Champion = _core(
		name="Primal Champion",
		min_level=20,
		description=(
			"*You have mastered your path. Now you walk new horizons.*\n\n"
			"Your Strength and Constitution "
			"scores increase by 4, to a maximum of 25."
			),
		apply=_apply_primal_champion,
		)


# ---------------------------------------------------------------------------
# Path of the Berserker
# ---------------------------------------------------------------------------


Frenzy = _berserker(
		name="Frenzy",
		min_level=3,
		description=_frenzy_entry,
		chips=(
				("Frenzy Dice", lambda c: f"{_rage_damage(c)}d6"),
				),
		)

Mindless_Rage = _berserker(
		name="Mindless Rage",
		min_level=6,
		description=(
			"*Your mind is pure flow: nothing to grasp, nothing to tame.*\n\n"
			"You have Immunity to the Charmed and Frightened conditions "
			"while your Rage is active. If you're Charmed or Frightened "
			"when you enter your Rage, the condition ends on you."
			),
		)

Retaliation = _berserker(
		name="Retaliation",
		min_level=10,
		description=(
			"*Your body moves on its own. Action, reaction. Enter the storm, "
			"get struck.*\n\n"
			"When you take damage from a creature that is within 5 feet "
			"of you, you can take a Reaction to make one melee attack "
			"against that creature, using a weapon or an Unarmed Strike."
			),
		)

Intimidating_Presence = _berserker(
		name="Intimidating Presence",
		min_level=14,
		description=lambda char: (
			"*Your will is not only untamable, but uncontainable. Others "
			"cannot help but cower.*\n\n"
			"As a Bonus Action, you can strike terror into others with "
			"your menacing presence and primal power. Each creature of "
			"your choice in a 30-foot Emanation originating from you must "
			f"make a Wisdom saving throw (DC {_strength_save_dc( char )}). "
			"On a failed save, a creature has the "
			"Frightened condition for 1 minute. At the end of each of the "
			"Frightened creature's turns, the creature repeats the save, "
			"ending the effect on itself on a success."
			"<br>Once you use this feature, you can't use it again until "
			"you finish a Long Rest unless you expend a use of your Rage "
			"(no action required) to restore your use of it."
			),
		)


# ---------------------------------------------------------------------------
# Path of the Wild Heart
# ---------------------------------------------------------------------------


Animal_Speaker = _path(
		WILD_HEART,
		name="Animal Speaker",
		min_level=3,
		description=(
			"*Your spirit is present and listens to the wilds.*\n\n"
			"You can cast the <i>Beast Sense</i> and "
			"<i>Speak with Animals</i> spells but only as Rituals. "
			"Wisdom is your spellcasting ability for them."
			),
		)

Rage_of_the_Wilds = _path(
		WILD_HEART,
		name="Rage of the Wilds",
		min_level=3,
		description=(
			"*Your heart beats wilder, and you sense the presence of the "
			"beast in you.*\n\n"
			"Whenever you activate your Rage, choose one option:"
			"<br><b>Bear.</b> While raging, you have Resistance to every "
			"damage type except Force, Necrotic, Psychic, and Radiant."
			"<br><b>Eagle.</b> When you activate Rage, you can take the "
			"Disengage and Dash actions as part of that Bonus Action. "
			"While raging, you can take a Bonus Action to take both of "
			"those actions."
			"<br><b>Wolf.</b> While raging, your allies have Advantage on "
			"attack rolls against any enemy of yours within 5 feet of you."
			),
		)

Aspect_of_the_Wilds = _path(
		WILD_HEART,
		name="Aspect of the Wilds",
		min_level=6,
		description=(
			"*Your movements become those of the wild, carried by your "
			"untamed spirit.*\n\n"
			"Choose one option whenever you finish a Long Rest:"
			"<br><b>Owl.</b> Darkvision 60 feet (or +60 feet if you "
			"already have Darkvision)."
			"<br><b>Panther.</b> Climb Speed equal to your Speed."
			"<br><b>Salmon.</b> Swim Speed equal to your Speed."
			),
		)

Nature_Speaker = _path(
		WILD_HEART,
		name="Nature Speaker",
		min_level=10,
		description=(
			"*Your heart opens to become one with nature.*\n\n"
			"You can cast <i>Commune with Nature</i> but only as a Ritual. "
			"Wisdom is your spellcasting ability for it."
			),
		)

Power_of_the_Wilds = _path(
		WILD_HEART,
		name="Power of the Wilds",
		min_level=14,
		description=(
			"*You are present. You are aware. You are the beast.*\n\n"
			"Whenever you activate your Rage, choose one option:"
			"<br><b>Falcon.</b> While raging, Fly Speed equal to your "
			"Speed if you aren't wearing armor."
			"<br><b>Lion.</b> While raging, enemies within 5 feet of you "
			"have Disadvantage on attack rolls against targets other than "
			"you or another Barbarian with this option active."
			"<br><b>Ram.</b> While raging, when you hit a Large or "
			"smaller creature with a melee attack, you can force it to "
			"have the Prone condition."
			),
		)


# ---------------------------------------------------------------------------
# Path of the World Tree
# ---------------------------------------------------------------------------


def _vitality_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	dice = _rage_damage(
			char
			)
	return (
		"Your Rage taps into the life force of the World Tree."
		f"<br><b>Vitality Surge.</b> When you activate your Rage, you "
		f"gain Temporary Hit Points equal to your Barbarian level "
		f"(<b>{level}</b>)."
		f"<br><b>Life-Giving Force.</b> At the start of each of your "
		f"turns while raging, you can choose another creature within "
		f"10 feet to gain Temporary Hit Points equal to "
		f"<b>{dice}d6</b>. Those Temporary Hit Points vanish when your "
		f"Rage ends."
		)


Vitality_of_the_Tree = _path(
		WORLD_TREE,
		name="Vitality of the Tree",
		min_level=3,
		description=_vitality_entry,
		chips=(
				("Life-Giving Force", lambda c: f"{_rage_damage(c)}d6"),
				),
		)

Branches_of_the_Tree = _path(
		WORLD_TREE,
		name="Branches of the Tree",
		min_level=6,
		description=lambda char: (
			"*Your connection with the flows of energy manipulates the "
			"space around you.*\n\n"
			"Whenever a creature you can see starts its turn within "
			"30 feet of you while your Rage is active, you can take a "
			"Reaction to summon spectral branches around it. The target "
			"must succeed on a Strength saving throw (DC "
			f"{_strength_save_dc( char )}) or be teleported "
			"to an unoccupied space you can see within 5 feet of you "
			"(or the nearest unoccupied space). After it teleports, you "
			"can reduce its Speed to 0 until the end of the current turn."
			),
		)

Battering_Roots = _path(
		WORLD_TREE,
		name="Battering Roots",
		min_level=10,
		description=lambda char: (
			"*Space and energy are just veils you see through, like waves "
			"in a pond.*\n\n"
			"During your turn, your reach is 10 feet greater with any "
			"Melee weapon that has the Heavy or Versatile property. When "
			"you hit with such a weapon on your turn, you can activate "
			"the Push or Topple mastery property in addition to a "
			"different mastery property you're using with that weapon."
			# Spelled out because this feature grants both regardless of
			# which weapons the Character actually drilled: a Barbarian who
			# never trained a Topple weapon still gets Topple here, and would
			# otherwise have no way to know what it does.
			"<br><b>Push.</b> "
			+ _mastery_text( "Push", char )
			+ "<br><b>Topple.</b> "
			+ _mastery_text( "Topple", char )
			),
		)

Travel_along_the_Tree = _path(
		WORLD_TREE,
		name="Travel along the Tree",
		min_level=14,
		description=(
			"*Space stops being a boundary that holds you. You can walk "
			"through its illusions.*\n\n"
			"When you activate your Rage and as a Bonus Action while "
			"raging, you can teleport up to 60 feet to an unoccupied "
			"space you can see."
			"<br>Once per Rage, you can increase that teleport to "
			"150 feet and bring up to six willing creatures within "
			"10 feet of you, each to an unoccupied space within 10 feet "
			"of your destination."
			),
		)


# ---------------------------------------------------------------------------
# Path of the Zealot
# ---------------------------------------------------------------------------


def _warrior_dice(
		char,
		) -> int:
	level = _rank(
			char
			)
	if level >= 17:
		return 7
	if level >= 12:
		return 6
	if level >= 6:
		return 5
	return 4


def _divine_fury_entry(
		char,
		) -> str:
	half = max(
			1,
			_rank(
					char
					) // 2,
			)
	return (
		"*You carry the wrath of the heavens and the punishment of the "
			"hells in your hands.*\n\n"
			"On each of your turns while your Rage is active, the first "
		"creature you hit with a weapon or an Unarmed Strike takes "
		f"extra damage equal to <b>1d6 + {half}</b>. Choose Necrotic "
		"or Radiant each time you deal the damage."
		)


Divine_Fury = _path(
		ZEALOT,
		name="Divine Fury",
		min_level=3,
		description=_divine_fury_entry,
		chips=(
				("Divine Fury", lambda c: f"1d6+{max(1, _rank(c)//2)}"),
				),
		)

Warrior_of_the_Gods = _path(
		ZEALOT,
		name="Warrior of the Gods",
		min_level=3,
		description=lambda char: (
			"*Eternal life flows through you, healing your wounds.*\n\n"
			f"You have a pool of {_warrior_dice( char )}d12 you can spend "
			"to heal yourself. As a Bonus Action, expend any number of "
			"those dice, roll them, and regain Hit Points equal to the "
			"total. You regain all expended dice when you finish a Long "
			"Rest."
			),
		chips=(
				("Warrior Dice", _warrior_dice),
				),
		)

Fanatical_Focus = _path(
		ZEALOT,
		name="Fanatical Focus",
		min_level=6,
		description=lambda char: (
			"*You fixate on your commandment and channel the will of the "
			"gods.*\n\n"
			"Once per Rage, if you fail a saving throw, you can reroll "
			f"it with a bonus of +{_rage_damage( char )}, and you must "
			"use the new roll."
			),
		)

Zealous_Presence = _path(
		ZEALOT,
		name="Zealous Presence",
		min_level=10,
		description=(
			"*You are a beacon of hope and a martyr who inspires others. "
			"Your words are a message from a God.*\n\n"
			"As a Bonus Action, unleash a divine battle cry. Up to ten "
			"other creatures of your choice within 60 feet gain Advantage "
			"on attack rolls and saving throws until the start of your "
			"next turn."
			"<br>Once you use this feature, you can't use it again until "
			"you finish a Long Rest unless you expend a use of your Rage "
			"(no action required) to restore your use of it."
			),
		)

Rage_of_the_Gods = _path(
		ZEALOT,
		name="Rage of the Gods",
		min_level=14,
		description=lambda char: (
			"*Your body is a vessel filled by your God. An avatar made to "
			"its shape. You rage, glorious.*\n\n"
			"When you activate your Rage, you can assume a divine warrior "
			"form for 1 minute or until you drop to 0 Hit Points. Once "
			"you use this feature, you can't do so again until you finish "
			"a Long Rest."
			"<br><b>Flight.</b> Fly Speed equal to your Speed; you can hover."
			"<br><b>Resistance.</b> Resistance to Necrotic, Psychic, and "
			"Radiant damage."
			"<br><b>Revivification.</b> When a creature within 30 feet "
			"would drop to 0 Hit Points, you can take a Reaction and "
			"expend a use of Rage to change that creature's Hit Points "
			f"to {_rank( char )} instead."
			),
		)
