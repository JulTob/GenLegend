"""
Rogue Training Tags — 2024 PHB core + all Rogue Archetypes.

Thought pattern
	1. Core lessons belong to the Rogue Guild (no path).
	2. Archetype lessons set ``path=…`` and awaken only for that Archetype.
	3. Numbers (Sneak Attack dice) live as Chips and in callable Entries.
	4. ASI / Epic Boon stay on legacy Progression.
	5. Language grants (Thieves' Cant) stay in legacy.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasVenustas import Chip


GUILD = "Rogue"
CORE_SOURCE = "Training: Rogue"
ARCANE_TRICKSTER = "Arcane Trickster"
ASSASSIN = "Assassin"
SOULKNIFE = "Soulknife"
THIEF = "Thief"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _sneak_dice(
		char,
		) -> str:
	level = _rank(char)
	n = (level + 1) // 2
	return f"{n}d6"


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
			source=f"Training: Rogue ({path_name})",
			)


def _arcane_trickster(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			ARCANE_TRICKSTER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _assassin(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			ASSASSIN,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _soulknife(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			SOULKNIFE,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _thief(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			THIEF,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


# ---------------------------------------------------------------------------
# Callable entry helpers
# ---------------------------------------------------------------------------


def _sneak_attack_entry(
		char,
		) -> str:
	dice = _sneak_dice(char)
	return (
		"Once per turn, you can deal an extra <b>"
		f"{dice}</b> damage to one creature you hit "
		"with an attack if you have Advantage on the attack roll, or "
		"if any ally of yours is within 5 feet of the enemy."
		"<br>You must be using a Finesse or Ranged weapon. The extra "
		"damage type matches the weapon's type."
		"<br>An enemy with the <b>Incapacitated</b> condition "
		"automatically triggers a Sneak Attack. Disadvantage on the "
		"attack roll cancels it regardless of activating factors."
		)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Expertise = _core(
		name="Expertise",
		min_level=1,
		description=(
			"Choose two of your skill proficiencies. Your proficiency "
			"bonus is doubled for any ability check you make that uses "
			"either of the chosen proficiencies."
			),
		)

Sneak_Attack = _core(
		name="Sneak Attack",
		min_level=1,
		description=_sneak_attack_entry,
		chips=(
				Chip(
					"🕷️",
					"Sneak Attack",
					_sneak_dice,
					),
				),
		)

def _thieves_cant_entry(
		char,
		) -> str:
	langs = (
			getattr(
					char,
					"language_feature_grants",
					None,
					) or {}
			).get(
			"Thieves' Cant"
			) or []
	extra = [
			name
			for name in langs
			if name != "Thieves' Cant"
			]
	extra_text = (
			f" You also learned <b>{extra[0]}</b>."
			if extra
			else " You also learned one additional language."
			)
	return (
		"You have learned <b>Thieves' Cant</b>, a secret mix of dialect, "
		"jargon, and code that allows you to hide messages in "
		"seemingly normal conversation. Only another creature who "
		"knows Thieves' Cant understands such messages. It takes "
		"four times longer to convey a message in Thieves' Cant "
		"than in normal speech."
		f"{extra_text}"
		)


Thieves_Cant = _core(
		name="Thieves' Cant",
		min_level=1,
		description=_thieves_cant_entry,
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

Cunning_Action = _core(
		name="Cunning Action",
		min_level=2,
		description=(
			"Your quick thinking and agility allow you to move and act "
			"quickly. On your turn, you can take one of the following "
			"actions as a <i>Bonus Action</i>:"
			"<ul>"
			"<li><b>Dash.</b> You gain extra movement equal to your Speed "
			"for the current turn.</li>"
			"<li><b>Disengage.</b> Your movement doesn't provoke "
			"Opportunity Attacks for the rest of the current turn.</li>"
			"<li><b>Hide.</b> Make a Dexterity (Stealth) check to conceal "
			"yourself. On a success, you have the Invisible condition "
			"until an enemy finds you, you make an attack roll, or you "
			"cast a spell with a Verbal component.</li>"
			"</ul>"
			),
		)

Steady_Aim = _core(
		name="Steady Aim",
		min_level=3,
		description=(
			"As a <i>Bonus Action</i>, you give yourself Advantage on "
			"your next attack roll on the current turn. You can use this "
			"feature only if you haven't moved during this turn, and "
			"after you use it, your Speed is 0 until the end of the "
			"current turn."
			),
		)

Cunning_Strike = _core(
		name="Cunning Strike",
		min_level=5,
		description=(
			"When you deal Sneak Attack damage, you can add one of the "
			"following Cunning Strike effects. Each effect costs a number "
			"of Sneak Attack dice that you forgo before rolling."
			"<br>Saving throw DC = 8 + Dexterity modifier + proficiency bonus."
			"<br><b>Poison (Cost: 1d6).</b> Force a Constitution save or "
			"the target has the Poisoned condition for 1 minute (repeating "
			"save at end of each of its turns). Requires a Poisoner's Kit."
			"<br><b>Trip (Cost: 1d6).</b> If Large or smaller, Dexterity "
			"save or Prone."
			"<br><b>Withdraw (Cost: 1d6).</b> Move up to half your Speed "
			"without provoking Opportunity Attacks immediately after "
			"the attack."
			),
		)

Uncanny_Dodge = _core(
		name="Uncanny Dodge",
		min_level=5,
		description=(
			"When an attacker that you can see hits you with an attack "
			"roll, you can take a <i>Reaction</i> to halve the attack's "
			"damage against you (round down)."
			),
		)

Expertise_II = _core(
		name="Expertise (II)",
		min_level=6,
		description=(
			"Choose two more of your skill proficiencies. Your proficiency "
			"bonus is doubled for any ability check you make that uses "
			"either of the chosen proficiencies."
			),
		)

Evasion = _core(
		name="Evasion",
		min_level=7,
		description=(
			"You can nimbly dodge out of the way of certain dangers. "
			"When you're subjected to an effect that allows you to make "
			"a Dexterity saving throw to take only half damage, you "
			"instead take <b>no damage</b> if you succeed on the saving "
			"throw and only half damage if you fail. You can't use this "
			"feature if you have the Incapacitated condition."
			),
		)

Reliable_Talent = _core(
		name="Reliable Talent",
		min_level=7,
		description=(
			"Whenever you make an ability check that uses one of your "
			"skill or tool proficiencies, you can treat a d20 roll of "
			"<b>9 or lower as a 10</b>."
			),
		)

Improved_Cunning_Strike = _core(
		name="Improved Cunning Strike",
		min_level=11,
		description=(
			"You can use <b>up to two</b> Cunning Strike effects when "
			"you deal Sneak Attack damage, paying the die cost for each."
			),
		)

Devious_Strikes = _core(
		name="Devious Strikes",
		min_level=14,
		description=(
			"You've practiced new ways to use your Sneak Attack deviously. "
			"The following effects are added to your Cunning Strike options:"
			"<ul>"
			"<li><b>Daze (Cost: 2d6).</b> Constitution save or the target "
			"can do only one of the following on its next turn: move, take "
			"an action, or take a Bonus Action.</li>"
			"<li><b>Knock Out (Cost: 6d6).</b> Constitution save or the "
			"target has the Unconscious condition for 1 minute or until it "
			"takes damage. Repeating save at end of each of its turns.</li>"
			"<li><b>Obscure (Cost: 3d6).</b> Dexterity save or the target "
			"has the Blinded condition until the end of its next turn.</li>"
			"</ul>"
			),
		)

Slippery_Mind = _core(
		name="Slippery Mind",
		min_level=15,
		description=(
			"Your cunning mind is exceptionally difficult to control. "
			"You gain proficiency in <b>Wisdom and Charisma saving "
			"throws</b>."
			),
		)

Elusive = _core(
		name="Elusive",
		min_level=18,
		description=(
			"You're so evasive that attackers rarely gain the upper hand "
			"against you. <b>No attack roll can have Advantage against "
			"you</b> unless you have the Incapacitated condition."
			),
		)

Stroke_of_Luck = _core(
		name="Stroke of Luck",
		min_level=20,
		description=(
			"You have a marvelous knack for succeeding when you need to. "
			"If you fail a D20 Test, you can turn the roll into a 20."
			"<br>Once you use this feature, you can't use it again until "
			"you finish a <i>Short or Long Rest</i>."
			),
		)


# ---------------------------------------------------------------------------
# Arcane Trickster (3 / 9 / 13 / 17)
# ---------------------------------------------------------------------------


Spellcasting_AT = _arcane_trickster(
		name="Spellcasting",
		min_level=3,
		description=(
			"You augment your roguish abilities with Enchantment and "
			"Illusion spells. You learn two Wizard cantrips of your "
			"choice and three level 1 Wizard spells, two of which must "
			"be from the Enchantment or Illusion school. Intelligence "
			"is your spellcasting ability."
			),
		)

Mage_Hand_Legerdemain = _arcane_trickster(
		name="Mage Hand Legerdemain",
		min_level=3,
		description=(
			"You know the <i>Mage Hand</i> cantrip. When you cast it, "
			"you can cast it as a <i>Bonus Action</i>, and you can make "
			"the spectral hand <b>Invisible</b>. You can control the "
			"hand as a Bonus Action, and through it you can make "
			"Dexterity (Sleight of Hand) checks."
			),
		)

Magical_Ambush = _arcane_trickster(
		name="Magical Ambush",
		min_level=9,
		description=(
			"If you have the Invisible condition when you cast a spell "
			"on a creature, it has <b>Disadvantage on any saving throw</b> "
			"it makes against the spell on the same turn."
			),
		)

Versatile_Trickster = _arcane_trickster(
		name="Versatile Trickster",
		min_level=13,
		description=(
			"You gain the ability to distract targets with your Mage Hand. "
			"When you use the Trip option of your Cunning Strike on a "
			"creature, you can also use that option on another creature "
			"within 5 feet of the spectral hand."
			),
		)

Spell_Thief = _arcane_trickster(
		name="Spell Thief",
		min_level=17,
		description=(
			"Immediately after a creature casts a spell that targets you "
			"or includes you in its area of effect, you can take a "
			"<i>Reaction</i> to force the creature to make an Intelligence "
			"saving throw (DC equals your spell save DC). On a failed save, "
			"you negate the spell's effect against you and steal the "
			"knowledge of the spell if it is at least level 1 and of a "
			"level you can cast. For the next 8 hours, you have the spell "
			"prepared; the creature can't cast it until then."
			"<br>Once you steal a spell, you can't use this feature again "
			"until you finish a Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Assassin (3 / 9 / 13 / 17)
# ---------------------------------------------------------------------------


Assassinate = _assassin(
		name="Assassinate",
		min_level=3,
		description=(
			"You're adept at ambushing a target."
			"<br><b>Initiative.</b> You have Advantage on Initiative rolls."
			"<br><b>Surprising Strikes.</b> During the first round of each "
			"combat, you have Advantage on attack rolls against any creature "
			"that hasn't taken a turn. If your Sneak Attack hits any target "
			"during that round, the target takes extra damage of the weapon's "
			"type equal to your Rogue level."
			),
		)


def _grant_assassins_tools(
		char,
		) -> None:
	"""
	Assassin's Tools: proficiency with the Disguise Kit and the Poisoner's
	Kit, and one of each in the Loadout. The kits are issued through GearKit
	so they are real Items in the bag, not sheet text.
	"""
	from AtlasInventarium.GearKit import issue
	from AtlasInventarium.Ledger_of_Tools import TOOLS_BY_NAME

	char.skills.Disguise_Kit.set_proficiency()
	char.skills.Poisoners_Kit.set_proficiency()
	for tool_name in (
			"Disguise Kit",
			"Poisoner's Kit",
			):
		issue(
				char,
				TOOLS_BY_NAME[tool_name],
				)

Assassins_Tools = _assassin(
		name="Assassin's Tools",
		min_level=3,
		description=(
			"You gain a <b>Disguise Kit</b> and a <b>Poisoner's Kit</b>, "
			"and you have proficiency with both."
			),
		apply=_grant_assassins_tools,
		)

Infiltration_Expertise = _assassin(
		name="Infiltration Expertise",
		min_level=9,
		description=(
			"You are expert at techniques that aid your infiltrations."
			"<br><b>Masterful Mimicry.</b> You can unerringly mimic "
			"another person's speech, handwriting, or both if you have "
			"spent at least 1 hour studying them."
			"<br><b>Roving Aim.</b> Your Speed isn't reduced to 0 by "
			"using Steady Aim."
			),
		)

Envenom_Weapons = _assassin(
		name="Envenom Weapons",
		min_level=13,
		description=(
			"When you use the Poison option of your Cunning Strike, "
			"the target also takes <b>2d6 Poison damage</b> whenever "
			"it fails the saving throw. This damage ignores Resistance "
			"to Poison damage."
			),
		)

Death_Strike = _assassin(
		name="Death Strike",
		min_level=17,
		description=(
			"When you hit with your Sneak Attack on the first round of "
			"a combat, the target must succeed on a Constitution saving "
			"throw (DC 8 + Dexterity modifier + proficiency bonus), or "
			"the <b>attack's damage is doubled</b> against the target."
			),
		)


# ---------------------------------------------------------------------------
# Soulknife (3 / 9 / 13 / 17)
# ---------------------------------------------------------------------------


def _psionic_power_rogue_entry(
		char,
		) -> str:
	level = _rank(char)
	import math
	pb = math.ceil(1 + level / 4)
	total = pb * 2
	die = "d6" if level < 5 else ("d8" if level < 11 else ("d10" if level < 17 else "d12"))
	return (
		"You harbor a wellspring of psionic energy within yourself. "
		f"You have <b>{total} Psionic Energy Dice</b> ({die}s). "
		"Spent dice are restored on a Long Rest; you can restore one "
		"by spending a Bonus Action (once per Short Rest)."
		"<br><b>Psi-Bolstered Knack.</b> If you fail an ability check "
		"using a skill or tool with which you have proficiency, expend "
		"one die and add the roll to the check. If it still fails, the "
		"die is not expended."
		"<br><b>Psychic Whispers.</b> As a Magic action, expend one "
		"Psionic Energy Die and choose creatures within 1 mile (up to "
		"your proficiency bonus). For a number of hours equal to the die "
		"roll, you and those creatures can communicate telepathically."
		)


Psionic_Power_SK = _soulknife(
		name="Psionic Power",
		min_level=3,
		description=_psionic_power_rogue_entry,
		)

Psychic_Blades = _soulknife(
		name="Psychic Blades",
		min_level=3,
		description=(
			"You can manifest blades of psychic energy. Whenever you take "
			"the Attack action, you can replace one of your attacks with "
			"manifesting a <b>Psychic Blade</b> from a free hand. The "
			"blade is a Finesse, thrown weapon (range 60 feet) that deals "
			"<b>1d6 Psychic damage</b> on a hit. It vanishes after "
			"the attack."
			"<br>After you attack with the blade, you can manifest a "
			"second one as a Bonus Action (no attack bonus added to "
			"that damage roll)."
			),
		)

Soul_Blades = _soulknife(
		name="Soul Blades",
		min_level=9,
		description=(
			"Your Psychic Blades are now an expression of your psi, "
			"sharpened to deadly potential."
			"<br><b>Homing Strikes.</b> If you miss with your Psychic "
			"Blade, expend one Psionic Energy Die (no action required); "
			"add the roll to the attack roll. If it still misses, the "
			"die is not expended."
			"<br><b>Psychic Teleportation.</b> As a Bonus Action, expend "
			"one Psionic Energy Die and roll it. Teleport up to 10 times "
			"the number rolled feet to an unoccupied space you can see."
			),
		)

Psychic_Veil = _soulknife(
		name="Psychic Veil",
		min_level=13,
		description=(
			"You can weave a veil of psychic static to mask yourself. "
			"As a Magic action, you gain the <b>Invisible condition</b> "
			"for 1 hour or until you dismiss the effect (no action "
			"required). This invisibility ends early if you deal damage "
			"or force a creature to make a saving throw."
			"<br>Once you use this feature, you can't do so again until "
			"you finish a Long Rest unless you expend a Psionic Energy "
			"Die to use it again."
			),
		)

Rend_Mind = _soulknife(
		name="Rend Mind",
		min_level=17,
		description=(
			"You can sweep your Psychic Blades through a creature's mind. "
			"When you use your Psychic Blades to deal Sneak Attack damage "
			"to a creature, you can force that target to make a Wisdom "
			"saving throw (DC 8 + Dexterity modifier + proficiency bonus). "
			"On a failed save, the target has the <b>Stunned condition</b> "
			"for 1 minute. The Stunned target repeats the saving throw "
			"at the end of each of its turns, ending the effect on a success."
			"<br>Once you use this feature, you can't do so again until "
			"you finish a Long Rest unless you expend 3 Psionic Energy "
			"Dice to use it again."
			),
		)


# ---------------------------------------------------------------------------
# Thief (3 / 9 / 13 / 17)
# ---------------------------------------------------------------------------


Fast_Hands = _thief(
		name="Fast Hands",
		min_level=3,
		description=(
			"As a <i>Bonus Action</i>, you can do one of the following:"
			"<ul>"
			"<li><b>Sleight of Hand.</b> Make a Dexterity (Sleight of "
			"Hand) check to pick a lock or disarm a trap with Thieves' "
			"Tools, or to pick a pocket.</li>"
			"<li><b>Use an Object.</b> Take the Utilize action, or take "
			"the Magic action to use a magic item that requires that "
			"action.</li>"
			"</ul>"
			),
		)

Second_Story_Work = _thief(
		name="Second-Story Work",
		min_level=3,
		description=(
			"You've trained to get into especially hard-to-reach places."
			"<br><b>Climber.</b> You gain a <b>Climb Speed</b> equal to "
			"your Speed."
			"<br><b>Jumper.</b> You can determine your jump distance using "
			"your <b>Dexterity</b> rather than your Strength."
			),
		)

Supreme_Sneak = _thief(
		name="Supreme Sneak",
		min_level=9,
		description=(
			"You gain the following Cunning Strike option:"
			"<br><b>Stealth Attack (Cost: 1d6).</b> If you have the "
			"Invisible condition granted by the Hide action, this attack "
			"doesn't end that condition on you if you end the turn behind "
			"Three-Quarters Cover or Total Cover."
			),
		)

Use_Magic_Device = _thief(
		name="Use Magic Device",
		min_level=13,
		description=(
			"You've learned how to maximize use of magic items."
			"<ul>"
			"<li><b>Attunement.</b> You can attune to up to <b>four</b> "
			"magic items at once.</li>"
			"<li><b>Charges.</b> Whenever you use a magic item property "
			"that expends charges, roll 1d6. On a 6, you use the property "
			"without expending the charges.</li>"
			"<li><b>Scrolls.</b> You can use any Spell Scroll, using "
			"Intelligence as your spellcasting ability. Level 1 or lower "
			"spells cast reliably. Higher-level scrolls require a DC "
			"(10 + spell level) Intelligence (Arcana) check; on a failed "
			"check, the scroll disintegrates.</li>"
			"</ul>"
			),
		)

Thiefs_Reflexes = _thief(
		name="Thief's Reflexes",
		min_level=17,
		description=(
			"You are adept at laying ambushes and quickly escaping danger. "
			"You can take <b>two turns during the first round of any "
			"combat</b>. You take your first turn at your normal Initiative "
			"and your second turn at your Initiative minus 10."
			),
		)
