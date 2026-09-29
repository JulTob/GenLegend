"""
Core_Kit — every Monk's lessons, and the readers the Warriors share.

Thought pattern
	1. Core lessons belong to the Monk Guild and carry no Warrior (no path).
	2. Numbers (Martial Arts die, Focus Points, Unarmored Movement speed)
	   live as Chips and in callable Entries: readers of the Character.
	3. The readers are public (Monk_Level, Martial_Arts_Die, Focus_Points,
	   Unarmored_Speed_Bonus) because the Warrior Kits beside this file use
	   them too.
	4. ASI / Epic Boon stay on legacy Progression; speed bonuses stay in
	   legacy (character mutation), until QST-0142 station 8.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
		Unarmored_Armour_Class,
		)
from AtlasVenustas import Chip


GUILD = "Monk"
CORE_SOURCE = "Training: Monk"


_MARTIAL_ARTS_DIE = (
		"",
		"1d6", "1d6", "1d6", "1d6",
		"1d8", "1d8", "1d8", "1d8", "1d8", "1d8",
		"1d10", "1d10", "1d10", "1d10", "1d10", "1d10",
		"1d12", "1d12", "1d12", "1d12",
		)


def Focus_Points(
		char,
		) -> int:
	return max(
			1,
			Monk_Level(char),
			)


def Monk_Level(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def Martial_Arts_Die(
		char,
		) -> str:
	level = max(
			1,
			min(
					20,
					Monk_Level(char),
					),
			)
	return _MARTIAL_ARTS_DIE[level]


def Unarmored_Speed_Bonus(
		char,
		) -> int:
	level = Monk_Level(char)
	if level >= 18:
		return 35
	if level >= 14:
		return 30
	if level >= 10:
		return 25
	if level >= 6:
		return 20
	if level >= 2:
		return 15
	return 10


def _core(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		flag: bool = False,
		):
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			source=CORE_SOURCE,
			flag=flag,
			)



# ---------------------------------------------------------------------------
# Callable entries (level-sensitive text)
# ---------------------------------------------------------------------------


def _martial_arts_entry(
		char,
		) -> str:
	die = Martial_Arts_Die(char)
	return (
		"Your practice of martial arts gives you mastery of combat "
		"styles that use your Unarmed Strike and Monk weapons. "
		"You gain the following benefits while unarmed or wielding "
		"only Monk weapons and not wearing armor or wielding a "
		"Shield:\n\n\n- **Bonus Unarmed Strike.** You can make "
		"an Unarmed Strike as a Bonus Action."
		"\n- **Martial Arts Die.** Roll **"
		f"{die}** in place of the normal damage of your Unarmed "
		"Strike or Monk weapons."
		"\n- **Dexterous Attacks.** You can use your Dexterity "
		"modifier instead of Strength for attack and damage rolls "
		"of Unarmed Strikes and Monk weapons. Also applies to "
		"Grapple or Shove save DCs."
		"\n\n"
		)


def _monks_focus_entry(
		char,
		) -> str:
	fp = Focus_Points(char)
	return (
		"Your training and discipline have given you a well of focus. You have **"
		f"{fp} Focus Points** that fuel your special actions. "
		"You regain all spent points when you finish a Short or Long Rest."
		"\n\nYou can spend Focus Points on:"
		"\n\n"
		"\n- **Flurry of Blows (1 point).** After the Attack "
		"action, make two Unarmed Strikes as a Bonus Action."
		"\n- **Patient Defense (1 point).** Take the Dodge "
		"action as a Bonus Action."
		"\n- **Step of the Wind (1 point).** Take the Disengage "
		"or Dash action as a Bonus Action; jump distance doubles "
		"for the turn."
		"\n\n"
		)


def _unarmored_movement_entry(
		char,
		) -> str:
	bonus = Unarmored_Speed_Bonus(char)
	return (
		"Your speed increases by **+"
		f"{bonus} feet** while you aren't wearing armor or "
		"wielding a Shield."
		)


def _apply_body_and_mind(
		char,
		) -> None:
	abilities = getattr(char, "abilities", None)
	if abilities is None:
		return
	from AtlasLusoris.Grimoire_of_Features import raise_stat
	raise_stat(char, "DEX", 4, cap=25)
	raise_stat(char, "WIS", 4, cap=25)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Martial_Arts = _core(
		name="Martial Arts",
		flag=True,
		min_level=1,
		description=_martial_arts_entry,
		chips=(
				Chip(
					"🥋",
					"Martial Arts Die",
					Martial_Arts_Die,
					),
				),
		)

def _unarmored_defense_entry(
		char,
		) -> str:
	# Same reader as the chip below, so the prose prints the live number.
	armour_class = Unarmored_Armour_Class( char )

	return (
		"While not wearing armor or wielding a Shield, your AC "
		f"equals **{armour_class}** (10 + Dexterity modifier + "
		"Wisdom modifier)."
		)


Unarmored_Defense = _core(
		name="Unarmored Defense",
		flag=True,
		min_level=1,
		description=_unarmored_defense_entry,
		chips=(
				Chip(
					"🥋",
					"Unarmored AC",
					Unarmored_Armour_Class,
					),
				),
		)

Monks_Focus = _core(
		name="Monk's Focus",
		min_level=2,
		description=_monks_focus_entry,
		chips=(
				Chip(
					"☯",
					"Focus Points",
					Focus_Points,
					),
				),
		)

Unarmored_Movement = _core(
		name="Unarmored Movement",
		flag=True,
		min_level=2,
		description=_unarmored_movement_entry,
		chips=(
				Chip(
					"👞",
					"Speed Bonus",
					Unarmored_Speed_Bonus,
					),
				),
		)

Uncanny_Metabolism = _core(
		name="Uncanny Metabolism",
		min_level=2,
		description=(
			"When you roll Initiative, you can regain all expended "
			"Focus Points. When you do so, roll your Martial Arts die "
			"and regain a number of Hit Points equal to your Monk "
			"level plus the number rolled.\n\nOnce you use this "
			"feature, you can't use it again until you finish a "
			"*Long Rest*."
			),
		)

Deflect_Attacks = _core(
		name="Deflect Attacks",
		min_level=3,
		description=(
			"When an attack roll hits you and its damage includes "
			"Bludgeoning, Piercing, or Slashing damage, you can take a "
			"*Reaction* to reduce the attack's total damage. The "
			"reduction equals **1d10 + Dexterity modifier + Monk level**."
			"\n\nIf you reduce the damage to 0, you can expend 1 Focus "
			"Point to redirect the force. Choose a creature within 5 feet "
			"(melee) or 60 feet without Total Cover (ranged). That creature "
			"makes a Dexterity save or takes damage equal to two Martial "
			"Arts die rolls + Dexterity modifier of the same type."
			),
		)

Slow_Fall = _core(
		name="Slow Fall",
		min_level=4,
		description=(
			"You can take a *Reaction* when you fall to reduce any "
			"falling damage you take by an amount equal to **five times "
			"your Monk level**."
			),
		)

Extra_Attack = _core(
		name="Extra Attack",
		flag=True,
		min_level=5,
		description=(
			"You can attack **twice** instead of once whenever you "
			"take the Attack action on your turn."
			),
		)

Stunning_Strike = _core(
		name="Stunning Strike",
		min_level=5,
		description=(
			"Once per turn when you hit a creature with a Monk weapon "
			"or an Unarmed Strike, you can expend 1 Focus Point to "
			"attempt a stunning strike. The target must make a "
			"Constitution saving throw.\n\nOn a **failed save**: "
			"the target has the Stunned condition until the start of "
			"your next turn."
			"\n\nOn a **successful save**: the target's Speed is "
			"halved until the start of your next turn, and the next "
			"attack roll made against the target before then has "
			"Advantage."
			),
		)

Empowered_Strikes = _core(
		name="Empowered Strikes",
		flag=True,
		min_level=6,
		description=(
			"Your Unarmed Strikes now count as **Magical** for the "
			"purpose of overcoming Resistance and Immunity to "
			"non-magical attacks and damage.\n\nYour Flurry of Blows, "
			"Patient Defense, and Step of the Wind gain the following "
			"benefits:"
			"\n\n**Flurry of Blows.** Expend 1 Focus Point to make "
			"**three** Unarmed Strikes instead of two."
			"\n\n**Patient Defense.** When you expend a Focus Point "
			"for Patient Defense, gain Temporary Hit Points equal to two "
			"rolls of your Martial Arts die."
			"\n\n**Step of the Wind.** When you expend a Focus Point "
			"for Step of the Wind, you can move a willing creature within "
			"5 feet (Large or smaller) with you until the end of your "
			"turn. Its movement doesn't provoke Opportunity Attacks."
			),
		)

Evasion = _core(
		name="Evasion",
		flag=True,
		min_level=7,
		description=(
			"When you're subjected to an effect that allows you to make "
			"a Dexterity saving throw to take only half damage, you "
			"instead take **no damage** if you succeed and only half "
			"if you fail. You can't use this feature while Incapacitated."
			),
		)

Acrobatic_Movement = _core(
		name="Acrobatic Movement",
		flag=True,
		min_level=9,
		description=(
			"While you aren't wearing armor or wielding a Shield, you "
			"gain the ability to **move along vertical surfaces and "
			"across liquids** on your turn without falling during "
			"the movement."
			),
		)

Heightened_Focus = _core(
		name="Heightened Focus",
		min_level=10,
		description=(
			"Your Flurry of Blows, Patient Defense, and Step of the Wind "
			"gain the following benefits."
			"\n\n**Flurry of Blows.** When you expend 1 Focus Point to "
			"use Flurry of Blows, you make **three** Unarmed Strikes "
			"with it instead of two."
			"\n\n**Patient Defense.** When you expend a Focus Point to "
			"use Patient Defense, you also gain Temporary Hit Points "
			"equal to **two rolls of your Martial Arts die**."
			"\n\n**Step of the Wind.** When you expend a Focus Point to "
			"use Step of the Wind, you can choose a willing creature "
			"within 5 feet of you that is Large or smaller. It moves "
			"with you until the end of your turn, and its movement "
			"doesn't provoke Opportunity Attacks."
			),
		)

Self_Restoration = _core(
		name="Self-Restoration",
		flag=True,
		min_level=10,
		description=(
			"Through sheer force of will, you can remove one of the "
			"following conditions from yourself at the end of each of "
			"your turns: **Charmed, Frightened, or Poisoned**."
			"\n\nIn addition, forgoing food and drink doesn't give you "
			"levels of Exhaustion."
			),
		)

Deflect_Energy = _core(
		name="Deflect Energy",
		min_level=13,
		description=(
			"You can now use your Deflect Attacks feature against "
			"attacks that deal **any damage type**, not just "
			"Bludgeoning, Piercing, or Slashing."
			),
		)

Disciplined_Survivor = _core(
		name="Disciplined Survivor",
		flag=True,
		min_level=14,
		description=(
			"Your physical and mental discipline grant you "
			"**proficiency in all saving throws**."
			"\n\nAdditionally, whenever you make a saving throw and "
			"fail, you can expend 1 Focus Point to reroll it, and you "
			"must use the new roll."
			),
		)

Perfect_Focus = _core(
		name="Perfect Focus",
		min_level=15,
		description=(
			"When you roll Initiative and don't use Uncanny Metabolism, "
			"you regain expended Focus Points until you have **4** "
			"if you have 3 or fewer."
			),
		)

Superior_Defense = _core(
		name="Superior Defense",
		min_level=18,
		description=(
			"At the start of your turn, you can expend **3 Focus "
			"Points** to bolster yourself against harm for 1 minute "
			"or until you have the Incapacitated condition. During that "
			"time, you have **Resistance to all damage except Force**."
			),
		)

Body_and_Mind = _core(
		name="Body and Mind",
		flag=True,
		min_level=20,
		description=(
			"You have perfected your body and mind. Your Dexterity and "
			"Wisdom scores increase by **4** each, to a maximum of 25."
			),
		apply=_apply_body_and_mind,
		)
