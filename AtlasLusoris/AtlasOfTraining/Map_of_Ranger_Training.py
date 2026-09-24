"""
Ranger Training Tags — 2024 PHB core + all Ranger Orders.

Thought pattern
	1. Core lessons belong to the Ranger Guild (no Order).
	2. Order lessons set ``path=…`` and awaken only for that Order.
	3. Numbers (Favored Enemy uses) and senses (Blindsight) are Chips —
	   rendered in the sheet's left rail, not inside the Entry.
	4. Generator prose names the pick (weapons, Hunter options, Expertise).
	5. Spellcasting / Fighting Style Tags awaken for identity but stay
	   off the Features list — Spells section / Fighting Style feats own them.
	6. ASI / Epic Boon / Fighting Style picks stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasVenustas import Chip


GUILD = "Ranger"
CORE_SOURCE = "Training: Ranger"
BEAST_MASTER = "Beast Master"
FEY_WANDERER = "Fey Wanderer"
GLOOM_STALKER = "Gloom Stalker"
HUNTER = "Hunter"

_HUNTERS_PREY = {
		"Colossus Slayer": (
			"Your tenacity can wear down the most potent foes. When you hit "
			"a creature with a weapon, the creature takes an extra <b>1d8</b> "
			"damage if it is below its Hit Point maximum. You can deal this "
			"extra damage only once per turn."
			),
		"Horde Breaker": (
			"Once on each of your turns when you make a weapon attack, you "
			"can make another attack with the same weapon against a different "
			"creature that is within 5 feet of the original target and within "
			"range of your weapon."
			),
		}

_DEFENSIVE_TACTICS = {
		"Escape the Horde": (
			"Opportunity Attacks against you have Disadvantage."
			),
		"Multiattack Defense": (
			"When a creature hits you with an attack roll, you gain +4 to "
			"your AC against all subsequent attacks from that creature for "
			"the rest of the current turn."
			),
		"Steel Will": (
			"You have Advantage on saving throws against the Frightened "
			"condition."
			),
		}

_SUPERIOR_PREY = {
		"Whirlwind Attack": (
			"When you take the Attack action, you can forgo one of your "
			"attacks and instead make melee attacks against any number of "
			"creatures within 5 feet of you, with a separate attack roll "
			"for each target."
			),
		"Volley": (
			"When you take the Attack action and use a ranged weapon, you "
			"can forgo one of your attacks to fire a volley, making a ranged "
			"attack against any number of creatures in a 10-foot-radius "
			"sphere centered on a point you can see within normal range of "
			"your weapon, with a separate roll for each target."
			),
		}

_SUPERIOR_DEFENSE = {
		"Evasion": (
			"When you are subjected to an effect that allows you to make a "
			"Dexterity saving throw to take only half damage, you take no "
			"damage on a success and half damage on a failure. You can't use "
			"this feature if you have the Incapacitated condition."
			),
		"Stand Against the Tide": (
			"When a hostile creature misses you with a melee attack, you can "
			"use your Reaction to force that creature to repeat the same "
			"attack against another creature (other than itself) of your choice."
			),
		"Uncanny Dodge": (
			"When an attacker that you can see hits you with an attack, you "
			"can use your Reaction to halve the attack's damage against you."
			),
		}


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _wis_mod(
		char,
		) -> int:
	abilities = getattr(
			char,
			"abilities",
			None,
			)
	wis = int(
			getattr(
					abilities,
					"WIS",
					10,
					) or 10
			) if abilities is not None else 10
	return (
			wis - 10
			) // 2


def _favored_uses(
		char,
		) -> int:
	level = _rank(
			char
			)
	uses = 2
	if level >= 5:
		uses += 1
	if level >= 9:
		uses += 1
	if level >= 13:
		uses += 1
	if level >= 17:
		uses += 1
	return uses


def _picks(
		char,
		) -> dict:
	bag = getattr(
			char,
			"_ranger_picks",
			None,
			)
	if bag is None:
		bag = {}
		char._ranger_picks = bag
	return bag


def _choose_named(
		char,
		key: str,
		options: dict[str, str],
		) -> tuple[str, str]:
	bag = _picks(
			char
			)
	if key in bag:
		name = bag[key]
		return name, options[name]
	name = char.Pick(
			list(
					options
					)
			)
	bag[key] = name
	return name, options[name]


def _core(
		*,
		name: str,
		min_level: int,
		description="",
		chips=(),
		apply=None,
		on_sheet: bool = True,
		):
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			source=CORE_SOURCE,
			on_sheet=on_sheet,
			)


def _path(
		path_name: str,
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
			path=path_name,
			source=f"Training: {path_name} Order",
			)


def _beast_master(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			BEAST_MASTER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _fey_wanderer(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			FEY_WANDERER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _gloom_stalker(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			GLOOM_STALKER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _hunter(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			HUNTER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


# ---------------------------------------------------------------------------
# Callable entries (generator prose)
# ---------------------------------------------------------------------------


def _favored_entry(
		char,
		) -> str:
	uses = _favored_uses(
			char
			)
	return (
		"You always have the <em>Hunter's Mark</em> spell prepared. "
		f"You can cast it a number of times equal to your Favored Enemy uses "
		f"(currently <b>{uses}</b>) without expending a spell slot. "
		"You regain all expended uses when you finish a Long Rest."
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


def _apply_deft_explorer(
		char,
		) -> None:
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return
	pool = list(
			skills.get_proficient_skills()
			)
	if not pool:
		return
	chosen = char.Pick(
			pool
			)
	skills.activate_expertise(
			1,
			[chosen],
			)
	_picks(
			char
			)["Deft Explorer"] = chosen


def _deft_explorer_entry(
		char,
		) -> str:
	skill = _picks(
			char
			).get(
			"Deft Explorer"
			)
	langs = (
			getattr(
					char,
					"language_feature_grants",
					None,
					) or {}
			).get(
			"Deft Explorer"
			) or []
	if len(
			langs
			) >= 2:
		lang_text = f"<b>{langs[0]}</b> and <b>{langs[1]}</b>"
	elif len(
			langs
			) == 1:
		lang_text = f"<b>{langs[0]}</b>"
	else:
		lang_text = "two languages"
	if skill:
		return (
			f"You have Expertise in <b>{skill}</b>, and you know "
			f"{lang_text}."
			)
	return (
		"You have Expertise in one skill you are proficient in, "
		f"and you know {lang_text}."
		)


def _apply_expertise(
		char,
		) -> None:
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return
	pool = list(
			skills.get_proficient_skills()
			)
	if not pool:
		return
	count = min(
			2,
			len(
					pool
					),
			)
	chosen = []
	while pool and len(
			chosen
			) < count:
		skill = char.Pick(
			pool
			)
		pool.remove(
			skill
			)
		chosen.append(
			skill
			)
	skills.activate_expertise(
			count,
			list(
					chosen
					),
			)
	_picks(
			char
			)["Expertise"] = chosen


def _expertise_entry(
		char,
		) -> str:
	chosen = _picks(
			char
			).get(
			"Expertise"
			) or []
	if len(
			chosen
			) >= 2:
		return (
			f"You have Expertise in <b>{chosen[0]}</b> and "
			f"<b>{chosen[1]}</b>."
			)
	if len(
			chosen
			) == 1:
		return f"You have Expertise in <b>{chosen[0]}</b>."
	return "You have Expertise in two skills you are proficient in."


def _signed_bonus(
		mod: int,
		) -> str:
	return f"+{mod}" if mod >= 0 else str(
			mod
			)


def _tireless_entry(
		char,
		) -> str:
	mod = _wis_mod(
			char
			)
	uses = max(
			1,
			mod,
			)
	times = "1 time" if uses == 1 else f"{uses} times"
	return (
		f"<em>Magic action:</em><br>"
		f"You gain <em>Temporary Hit Points</em> equal to "
		f"<b>1d8 {_signed_bonus(mod)}</b>. "
		f"You can use this action <b>{times}</b>. "
		f"You regain all expended uses when you finish a <b>Long Rest</b>."
		f"<br>Additionally, whenever you finish a <b>Short Rest</b>, "
		f"your Exhaustion level, if any, decreases by 1."
		)


def _tireless_uses(
		char,
		) -> int:
	return max(
			1,
			_wis_mod(
					char
					),
			)


def _natures_veil_entry(
		char,
		) -> str:
	uses = max(
			1,
			_wis_mod(
					char
					),
			)
	times = "1 time" if uses == 1 else f"{uses} times"
	return (
		"<em>Bonus Action:</em><br>"
		"You draw on nature's power to become <em>Invisible</em> "
		"until the end of your next turn. "
		f"You can use this feature <b>{times}</b>. "
		"You regain all expended uses when you finish a <b>Long Rest</b>."
		)


def _natures_veil_uses(
		char,
		) -> int:
	return max(
			1,
			_wis_mod(
					char
					),
			)


def _hunters_prey_entry(
		char,
		) -> str:
	name, text = _choose_named(
			char,
			"Hunter's Prey",
			_HUNTERS_PREY,
			)
	return (
		f"You trained in <b>{name}</b>. Whenever you finish a Short or Long "
		f"Rest, you can replace it with the other Hunter's Prey option."
		f"<br>{text}"
		)


def _defensive_tactics_entry(
		char,
		) -> str:
	name, text = _choose_named(
			char,
			"Defensive Tactics",
			_DEFENSIVE_TACTICS,
			)
	return (
		f"You trained in <b>{name}</b>. Whenever you finish a Short or Long "
		f"Rest, you can replace it with another Defensive Tactics option."
		f"<br>{text}"
		)


def _superior_prey_entry(
		char,
		) -> str:
	name, text = _choose_named(
			char,
			"Superior Hunter's Prey",
			_SUPERIOR_PREY,
			)
	return (
		f"Once per turn, you can apply <b>{name}</b>."
		f"<br>{text}"
		)


def _superior_defense_entry(
		char,
		) -> str:
	name, text = _choose_named(
			char,
			"Superior Hunter's Defense",
			_SUPERIOR_DEFENSE,
			)
	return (
		f"You trained in <b>{name}</b>."
		f"<br>{text}"
		)


def _dreadful_strikes_die(
		char,
		) -> str:
	return "1d6" if _rank(char) >= 11 else "1d4"


def _dreadful_strikes_entry(
		char,
		) -> str:
	die = _dreadful_strikes_die(
			char
			)
	return (
		f"Once per turn, when you damage a creature with a weapon attack, "
		f"you deal an extra <b>{die}</b> Psychic damage to the target, "
		"which can't regain Hit Points until the start of your next turn. "
		"The psychic damage increases to 1d6 at Ranger level 11."
		)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		on_sheet=False,
		)

Favored_Enemy = _core(
		name="Favored Enemy",
		min_level=1,
		description=_favored_entry,
		chips=(
				Chip(
					"🎯",
					"Favored Enemy Uses",
					_favored_uses,
					),
				),
		)

Weapon_Mastery = _core(
		name="Weapon Mastery",
		min_level=1,
		description=_weapon_mastery_entry,
		chips=(
				Chip(
					"⚔️",
					"Weapon Masteries",
					_weapon_mastery_chip,
					),
				),
		)

Deft_Explorer = _core(
		name="Deft Explorer",
		min_level=2,
		description=_deft_explorer_entry,
		apply=_apply_deft_explorer,
		)

Fighting_Style = _core(
		name="Fighting Style",
		min_level=2,
		on_sheet=False,
		)

Extra_Attack = _core(
		name="Extra Attack",
		min_level=5,
		description=(
			"You can attack twice instead of once whenever you take the "
			"Attack action on your turn."
			),
		)

Roving = _core(
		name="Roving",
		min_level=6,
		description=(
			"Your Speed increases by 10 feet while you aren't wearing Heavy Armor. "
			"You also gain a Climb Speed and a Swim Speed equal to your Speed."
			),
		)

Expertise = _core(
		name="Expertise",
		min_level=9,
		description=_expertise_entry,
		apply=_apply_expertise,
		)

Tireless = _core(
		name="Tireless",
		min_level=10,
		description=_tireless_entry,
		chips=(
				Chip(
					"💤",
					"Tireless Uses",
					_tireless_uses,
					),
				),
		)

Relentless_Hunter = _core(
		name="Relentless Hunter",
		min_level=13,
		description=(
			"Taking damage can't break your Concentration on "
			"<em>Hunter's Mark</em>."
			),
		)

Natures_Veil = _core(
		name="Nature's Veil",
		min_level=14,
		description=_natures_veil_entry,
		chips=(
				Chip(
					"🌿",
					"Nature's Veil Uses",
					_natures_veil_uses,
					),
				),
		)

Precise_Hunter = _core(
		name="Precise Hunter",
		min_level=17,
		description=(
			"You have Advantage on attack rolls against the creature currently "
			"marked by your <em>Hunter's Mark</em>."
			),
		)

Feral_Senses = _core(
		name="Feral Senses",
		min_level=18,
		description=(
			"Your connection to the natural world gives you preternatural senses."
			),
		chips=(
				Chip(
					"👁️",
					"Blindsight",
					"30 feet",
					),
				),
		)

Foe_Slayer = _core(
		name="Foe Slayer",
		min_level=20,
		description=(
			"You become an unparalleled hunter. "
			"Your <em>Hunter's Mark</em> deals <b>1d10</b> extra damage instead "
			"of 1d6."
			),
		)


# ---------------------------------------------------------------------------
# Beast Master Order
# ---------------------------------------------------------------------------


Primal_Companion = _beast_master(
		name="Primal Companion",
		min_level=3,
		description=(
			"You magically summon a primal beast that draws power from your bond. "
			"Choose a Beast of the Land, Beast of the Sea, or Beast of the Sky; "
			"it obeys your commands, uses your Proficiency Bonus for its modifiers, "
			"and acts on its own initiative count. "
			"<br>If the beast is killed, you can return it to life with an 8-hour "
			"ritual. You can also expend a spell slot during a Short Rest to restore "
			"it to its Hit Point maximum."
			),
		)

Exceptional_Training = _beast_master(
		name="Exceptional Training",
		min_level=7,
		description=(
			"On any of your turns when your Primal Companion beast doesn't attack, "
			"you can use your Bonus Action to command it to take the Dash, "
			"Disengage, Dodge, or Help action. "
			"<br>In addition, the beast's attacks now count as Magical for the "
			"purpose of overcoming Resistance and Immunity."
			),
		)

Bestial_Fury = _beast_master(
		name="Bestial Fury",
		min_level=11,
		description=(
			"When you command your Primal Companion beast to take the Attack action, "
			"the beast can make two attacks. "
			"<br>In addition, the first time the beast hits on a turn, the target "
			"takes extra damage equal to your Hunter's Mark damage die if the "
			"creature is marked."
			),
		)

Share_Spells = _beast_master(
		name="Share Spells",
		min_level=15,
		description=(
			"When you cast a spell targeting only yourself, you can also affect "
			"your Primal Companion beast with the spell if it is within 30 feet of you."
			),
		)


# ---------------------------------------------------------------------------
# Fey Wanderer Order
# ---------------------------------------------------------------------------


Dreadful_Strikes = _fey_wanderer(
		name="Dreadful Strikes",
		min_level=3,
		description=_dreadful_strikes_entry,
		chips=(
				Chip(
					"👻",
					"Dreadful Strikes",
					_dreadful_strikes_die,
					),
				),
		)

Fey_Spells = _fey_wanderer(
		name="Fey Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared:"
			"<ul>"
			"<li><b>3rd:</b> <em>Charm Person</em></li>"
			"<li><b>5th:</b> <em>Misty Step</em></li>"
			"<li><b>9th:</b> <em>Summon Fey</em></li>"
			"<li><b>13th:</b> <em>Dimension Door</em></li>"
			"<li><b>17th:</b> <em>Mislead</em></li>"
			"</ul>"
			),
		)

Otherworldly_Glamour = _fey_wanderer(
		name="Otherworldly Glamour",
		min_level=3,
		description=(
			"Whenever you make a Charisma check, you gain a bonus equal to your "
			"Wisdom modifier (minimum +1). "
			"<br>In addition, you gain proficiency in one of the following skills "
			"of your choice: Deception, Performance, or Persuasion."
			),
		)

Beguiling_Twist = _fey_wanderer(
		name="Beguiling Twist",
		min_level=7,
		description=(
			"The magic of the Feywild guards your mind. You have Advantage on "
			"saving throws against the Charmed and Frightened conditions. "
			"<br>In addition, whenever you or a creature you can see within 120 feet "
			"of you succeeds on a saving throw against a Charmed or Frightened effect, "
			"you can use your Reaction to force a different creature you can see within "
			"120 feet to make a Wisdom saving throw against your spell save DC. "
			"On a failed save, the target is Charmed or Frightened (your choice) "
			"by you for 1 minute."
			),
		)

Fey_Reinforcements = _fey_wanderer(
		name="Fey Reinforcements",
		min_level=11,
		description=(
			"You can cast <em>Summon Fey</em> without a material component. "
			"<br>You can also cast it once without expending a spell slot, and "
			"you regain this use when you finish a Long Rest. "
			"<br>Whenever you start casting the spell, you can modify it so that "
			"it doesn't require Concentration; if you do, the spell's duration "
			"becomes 1 minute for that casting."
			),
		)

Misty_Wanderer = _fey_wanderer(
		name="Misty Wanderer",
		min_level=15,
		description=(
			"You can cast <em>Misty Step</em> without expending a spell slot a "
			"number of times equal to your Wisdom modifier (minimum once). "
			"You regain all expended uses when you finish a Long Rest. "
			"<br>In addition, whenever you cast <em>Misty Step</em>, you can bring "
			"one willing creature you can see within 5 feet of you to an unoccupied "
			"space within 5 feet of your destination."
			),
		)


# ---------------------------------------------------------------------------
# Gloom Stalker Order
# ---------------------------------------------------------------------------


Dread_Ambusher = _gloom_stalker(
		name="Dread Ambusher",
		min_level=3,
		description=(
			"You master the art of the ambush. "
			"<br><b>Initiative.</b> You add your Wisdom modifier to Initiative rolls. "
			"<br><b>Dread Ambusher Attack.</b> On the first round of combat, your Speed "
			"increases by 10 feet, and if you take the Attack action, you can make "
			"one additional attack as part of it. If that attack hits, the target "
			"takes an extra <b>2d6</b> Psychic damage."
			),
		)

Gloom_Spells = _gloom_stalker(
		name="Gloom Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared:"
			"<ul>"
			"<li><b>3rd:</b> <em>Disguise Self</em></li>"
			"<li><b>5th:</b> <em>Rope Trick</em></li>"
			"<li><b>9th:</b> <em>Fear</em></li>"
			"<li><b>13th:</b> <em>Greater Invisibility</em></li>"
			"<li><b>17th:</b> <em>Seeming</em></li>"
			"</ul>"
			),
		)

Umbral_Sight = _gloom_stalker(
		name="Umbral Sight",
		min_level=3,
		description=(
			"You gain Darkvision out to a range of 60 feet. "
			"If you already have Darkvision, its range increases by 60 feet. "
			"<br>You are also adept at evading creatures that rely on Darkvision. "
			"While entirely in Darkness, you are Invisible to any creature that "
			"relies on Darkvision to see you in that darkness."
			),
		)

Iron_Mind = _gloom_stalker(
		name="Iron Mind",
		min_level=7,
		description=(
			"You have honed your ability to resist the mind-altering powers "
			"of your prey. "
			"You gain proficiency in Wisdom saving throws. "
			"If you already have proficiency in Wisdom saving throws, you instead "
			"gain proficiency in Intelligence or Charisma saving throws (your choice)."
			),
		)

Stalkers_Flurry = _gloom_stalker(
		name="Stalker's Flurry",
		min_level=11,
		description=(
			"You learn to attack with such unexpected speed that you can turn "
			"a miss into another strike. "
			"Once on each of your turns when you miss with an attack roll, "
			"you can make another attack roll against the same target."
			),
		)

Shadowy_Dodge = _gloom_stalker(
		name="Shadowy Dodge",
		min_level=15,
		description=(
			"You can dodge in unforeseen ways, with wisps of supernatural shadow "
			"around you. "
			"When a creature makes an attack roll against you and doesn't have "
			"Advantage on the roll, you can use your Reaction to impose Disadvantage "
			"on it. You must use this feature before you know whether the attack hits "
			"or misses."
			),
		)


# ---------------------------------------------------------------------------
# Hunter Order
# ---------------------------------------------------------------------------


Hunters_Lore = _hunter(
		name="Hunter's Lore",
		min_level=3,
		description=(
			"You can call on the knowledge of your most formidable foes. "
			"While a creature is marked by your <em>Hunter's Mark</em>, you know "
			"whether it has any Immunities, Resistances, or Vulnerabilities, "
			"and what they are."
			),
		)

Hunters_Prey = _hunter(
		name="Hunter's Prey",
		min_level=3,
		description=_hunters_prey_entry,
		)

Defensive_Tactics = _hunter(
		name="Defensive Tactics",
		min_level=7,
		description=_defensive_tactics_entry,
		)

Superior_Hunters_Prey = _hunter(
		name="Superior Hunter's Prey",
		min_level=11,
		description=_superior_prey_entry,
		)

Superior_Hunters_Defense = _hunter(
		name="Superior Hunter's Defense",
		min_level=15,
		description=_superior_defense_entry,
		)
