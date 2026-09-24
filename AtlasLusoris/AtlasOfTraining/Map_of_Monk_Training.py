"""
Monk Training Tags — 2024 PHB core + all Monk Traditions.

Thought pattern
        1. Core lessons belong to the Monk Guild (no path).
        2. Tradition lessons set ``path=…`` and awaken only for that Tradition.
        3. Numbers (Martial Arts die, Focus Points, Unarmored Movement speed)
           live as Chips and in callable Entries.
        4. ASI / Epic Boon stay on legacy Progression.
        5. Speed bonuses stay in legacy (character mutation).
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
		Unarmored_Armour_Class,
		)


GUILD = "Monk"
CORE_SOURCE = "Training: Monk"
MERCY = "Mercy"
OPEN_HAND = "Open Hand"
SHADOW = "Shadow"
ELEMENTS = "Elements"


_MARTIAL_ARTS_DIE = (
		"",
		"1d6", "1d6", "1d6", "1d6",
		"1d8", "1d8", "1d8", "1d8", "1d8", "1d8",
		"1d10", "1d10", "1d10", "1d10", "1d10", "1d10",
		"1d12", "1d12", "1d12", "1d12",
		)


def _focus_points(
		char,
		) -> int:
	return max(
			1,
			_rank(char),
			)


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _martial_die(
		char,
		) -> str:
	level = max(
			1,
			min(
					20,
					_rank(char),
					),
			)
	return _MARTIAL_ARTS_DIE[level]


def _unarmored_speed_bonus(
		char,
		) -> int:
	level = _rank(char)
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
			source=f"Training: Monk ({path_name})",
			)


def _mercy(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			MERCY,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _open_hand(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			OPEN_HAND,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _shadow(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			SHADOW,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _elements(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			ELEMENTS,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


# ---------------------------------------------------------------------------
# Callable entries (level-sensitive text)
# ---------------------------------------------------------------------------


def _martial_arts_entry(
		char,
		) -> str:
	die = _martial_die(char)
	return (
		"Your practice of martial arts gives you mastery of combat "
		"styles that use your Unarmed Strike and Monk weapons. "
		"You gain the following benefits while unarmed or wielding "
		"only Monk weapons and not wearing armor or wielding a "
		"Shield:<ul><li><b>Bonus Unarmed Strike.</b> You can make "
		"an Unarmed Strike as a Bonus Action.</li>"
		"<li><b>Martial Arts Die.</b> Roll <b>"
		f"{die}</b> in place of the normal damage of your Unarmed "
		"Strike or Monk weapons.</li>"
		"<li><b>Dexterous Attacks.</b> You can use your Dexterity "
		"modifier instead of Strength for attack and damage rolls "
		"of Unarmed Strikes and Monk weapons. Also applies to "
		"Grapple or Shove save DCs.</li>"
		"</ul>"
		)


def _monks_focus_entry(
		char,
		) -> str:
	fp = _focus_points(char)
	return (
		"Your training and discipline have given you a well of focus. You have <b>"
		f"{fp} Focus Points</b> that fuel your special actions. "
		"You regain all spent points when you finish a Short or Long Rest."
		"<br>You can spend Focus Points on:"
		"<ul>"
		"<li><b>Flurry of Blows (1 point).</b> After the Attack "
		"action, make two Unarmed Strikes as a Bonus Action.</li>"
		"<li><b>Patient Defense (1 point).</b> Take the Dodge "
		"action as a Bonus Action.</li>"
		"<li><b>Step of the Wind (1 point).</b> Take the Disengage "
		"or Dash action as a Bonus Action; jump distance doubles "
		"for the turn.</li>"
		"</ul>"
		)


def _unarmored_movement_entry(
		char,
		) -> str:
	bonus = _unarmored_speed_bonus(char)
	return (
		"Your speed increases by <b>+"
		f"{bonus} feet</b> while you aren't wearing armor or "
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
		min_level=1,
		description=_martial_arts_entry,
		chips=(
				("Martial Arts Die", _martial_die, "🥋"),
				),
		)

def _unarmored_defense_entry(
		char,
		) -> str:
	# Same reader as the chip below, so the prose prints the live number.
	armour_class = Unarmored_Armour_Class( char )

	return (
		"While not wearing armor or wielding a Shield, your AC "
		f"equals <b>{armour_class}</b> (10 + Dexterity modifier + "
		"Wisdom modifier)."
		)


Unarmored_Defense = _core(
		name="Unarmored Defense",
		min_level=1,
		description=_unarmored_defense_entry,
		chips=(
				("Unarmored AC", Unarmored_Armour_Class, "🥋"),
				),
		)

Monks_Focus = _core(
		name="Monk's Focus",
		min_level=2,
		description=_monks_focus_entry,
		chips=(
				("Focus Points", _focus_points, "☯"),
				),
		)

Unarmored_Movement = _core(
		name="Unarmored Movement",
		min_level=2,
		description=_unarmored_movement_entry,
		chips=(
				("Speed Bonus", _unarmored_speed_bonus, "👞"),
				),
		)

Uncanny_Metabolism = _core(
		name="Uncanny Metabolism",
		min_level=2,
		description=(
			"When you roll Initiative, you can regain all expended "
			"Focus Points. When you do so, roll your Martial Arts die "
			"and regain a number of Hit Points equal to your Monk "
			"level plus the number rolled.<br>Once you use this "
			"feature, you can't use it again until you finish a "
			"<i>Long Rest</i>."
			),
		)

Deflect_Attacks = _core(
		name="Deflect Attacks",
		min_level=3,
		description=(
			"When an attack roll hits you and its damage includes "
			"Bludgeoning, Piercing, or Slashing damage, you can take a "
			"<i>Reaction</i> to reduce the attack's total damage. The "
			"reduction equals <b>1d10 + Dexterity modifier + Monk level</b>."
			"<br>If you reduce the damage to 0, you can expend 1 Focus "
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
			"You can take a <i>Reaction</i> when you fall to reduce any "
			"falling damage you take by an amount equal to <b>five times "
			"your Monk level</b>."
			),
		)

Extra_Attack = _core(
		name="Extra Attack",
		min_level=5,
		description=(
			"You can attack <b>twice</b> instead of once whenever you "
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
			"Constitution saving throw.<br>On a <b>failed save</b>: "
			"the target has the Stunned condition until the start of "
			"your next turn."
			"<br>On a <b>successful save</b>: the target's Speed is "
			"halved until the start of your next turn, and the next "
			"attack roll made against the target before then has "
			"Advantage."
			),
		)

Empowered_Strikes = _core(
		name="Empowered Strikes",
		min_level=6,
		description=(
			"Your Unarmed Strikes now count as <b>Magical</b> for the "
			"purpose of overcoming Resistance and Immunity to "
			"non-magical attacks and damage.<br>Your Flurry of Blows, "
			"Patient Defense, and Step of the Wind gain the following "
			"benefits:"
			"<br><b>Flurry of Blows.</b> Expend 1 Focus Point to make "
			"<b>three</b> Unarmed Strikes instead of two."
			"<br><b>Patient Defense.</b> When you expend a Focus Point "
			"for Patient Defense, gain Temporary Hit Points equal to two "
			"rolls of your Martial Arts die."
			"<br><b>Step of the Wind.</b> When you expend a Focus Point "
			"for Step of the Wind, you can move a willing creature within "
			"5 feet (Large or smaller) with you until the end of your "
			"turn. Its movement doesn't provoke Opportunity Attacks."
			),
		)

Evasion = _core(
		name="Evasion",
		min_level=7,
		description=(
			"When you're subjected to an effect that allows you to make "
			"a Dexterity saving throw to take only half damage, you "
			"instead take <b>no damage</b> if you succeed and only half "
			"if you fail. You can't use this feature while Incapacitated."
			),
		)

Acrobatic_Movement = _core(
		name="Acrobatic Movement",
		min_level=9,
		description=(
			"While you aren't wearing armor or wielding a Shield, you "
			"gain the ability to <b>move along vertical surfaces and "
			"across liquids</b> on your turn without falling during "
			"the movement."
			),
		)

Heightened_Focus = _core(
		name="Heightened Focus",
		min_level=10,
		description=(
			"Your Flurry of Blows, Patient Defense, and Step of the Wind "
			"gain the following upgrades (in addition to their Empowered "
			"Strikes benefits):"
			"<br><b>Flurry of Blows.</b> Once per turn, a creature you hit "
			"with one of the attacks must succeed on a Constitution save "
			"(DC 8 + proficiency bonus + Wisdom modifier) or be Stunned "
			"until the start of your next turn."
			"<br><b>Patient Defense.</b> When you expend a Focus Point, "
			"you gain both the Dodge benefit and Temporary Hit Points."
			"<br><b>Step of the Wind.</b> When you expend a Focus Point, "
			"your Speed doubles until the end of the current turn."
			),
		)

Self_Restoration = _core(
		name="Self-Restoration",
		min_level=10,
		description=(
			"Through sheer force of will, you can remove one of the "
			"following conditions from yourself at the end of each of "
			"your turns: <b>Charmed, Frightened, or Poisoned</b>."
			"<br>In addition, forgoing food and drink doesn't give you "
			"levels of Exhaustion."
			),
		)

Deflect_Energy = _core(
		name="Deflect Energy",
		min_level=13,
		description=(
			"You can now use your Deflect Attacks feature against "
			"attacks that deal <b>any damage type</b>, not just "
			"Bludgeoning, Piercing, or Slashing."
			),
		)

Disciplined_Survivor = _core(
		name="Disciplined Survivor",
		min_level=14,
		description=(
			"Your physical and mental discipline grant you "
			"<b>proficiency in all saving throws</b>."
			"<br>Additionally, whenever you make a saving throw and "
			"fail, you can expend 1 Focus Point to reroll it, and you "
			"must use the new roll."
			),
		)

Perfect_Focus = _core(
		name="Perfect Focus",
		min_level=15,
		description=(
			"When you roll Initiative and don't use Uncanny Metabolism, "
			"you regain expended Focus Points until you have <b>4</b> "
			"if you have 3 or fewer."
			),
		)

Superior_Defense = _core(
		name="Superior Defense",
		min_level=18,
		description=(
			"At the start of your turn, you can expend <b>3 Focus "
			"Points</b> to bolster yourself against harm for 1 minute "
			"or until you have the Incapacitated condition. During that "
			"time, you have <b>Resistance to all damage except Force</b>."
			),
		)

Body_and_Mind = _core(
		name="Body and Mind",
		min_level=20,
		description=(
			"You have perfected your body and mind. Your Dexterity and "
			"Wisdom scores increase by <b>4</b> each, to a maximum of 25."
			),
		apply=_apply_body_and_mind,
		)


# ---------------------------------------------------------------------------
# Warrior of Mercy
# ---------------------------------------------------------------------------


def _hand_of_harm_entry(
		char,
		) -> str:
	level = _rank(char)
	poison_note = (
		"<br>You can also give that creature the Poisoned "
		"condition until the end of your next turn."
		if level >= 6
		else ""
		)
	return (
		"Once per turn when you hit a creature with an Unarmed "
		"Strike and deal damage, you can expend 1 Focus Point to "
		"deal extra <b>Necrotic damage</b> equal to one roll of "
		"your Martial Arts die plus your Wisdom modifier."
		f"{poison_note}"
		)


def _hand_of_healing_entry(
		char,
		) -> str:
	level = _rank(char)
	cure_note = (
		"<br>When you use your Flurry of Blows, you can also end "
		"one of the following conditions on the creature you heal "
		"(Charmed, Frightened, Paralyzed, Poisoned, or Stunned)."
		if level >= 6
		else ""
		)
	return (
		"As a <i>Magic action</i>, expend 1 Focus Point to touch a "
		"creature and restore Hit Points equal to one roll of your "
		"Martial Arts die plus your Wisdom modifier.<br>When you "
		"use your Flurry of Blows, you can replace one Unarmed "
		"Strike with a use of this feature without expending a "
		"Focus Point for the healing."
		f"{cure_note}"
		)


Implements_of_Mercy = _mercy(
		name="Implements of Mercy",
		min_level=3,
		description=(
			"You gain proficiency in Insight, Medicine, and Herbalism "
			"Kit. You also gain a special mask. It is a symbol of your "
			"tradition's philosophy."
			),
		)

Hand_of_Harm = _mercy(
		name="Hand of Harm",
		min_level=3,
		description=_hand_of_harm_entry,
		)

Hand_of_Healing = _mercy(
		name="Hand of Healing",
		min_level=3,
		description=_hand_of_healing_entry,
		)

Physicians_Touch = _mercy(
		name="Physician's Touch",
		min_level=6,
		description=(
			"Your Hand of Harm and Hand of Healing gain additional "
			"effects (see those entries). At level 6 and above, Hand of "
			"Harm can apply Poisoned, and Hand of Healing can cure a "
			"condition from the list."
			),
		)

Flurry_of_Healing_and_Harm = _mercy(
		name="Flurry of Healing and Harm",
		min_level=11,
		description=(
			"When you use Flurry of Blows, you can replace each of the "
			"Unarmed Strikes with a use of Hand of Healing <b>without "
			"expending Focus Points</b> for the healing."
			"<br>In addition, when you make an Unarmed Strike with "
			"Flurry of Blows and deal damage, you can use Hand of Harm "
			"with that strike "
			"<b>without expending a Focus Point</b>. You can still use "
			"Hand of Harm only once per turn.<br>You can use these "
			"benefits a total number of times equal to your Wisdom "
			"modifier (minimum once). All uses restore on a Long Rest."
			),
		)

Hand_of_Ultimate_Mercy = _mercy(
		name="Hand of Ultimate Mercy",
		min_level=17,
		description=(
			"Your mastery of life energy opens the door to the "
			"ultimate mercy. As a <i>Magic action</i>, touch the "
			"corpse of a creature that died within the past 24 hours "
			"and expend 5 Focus Points. The creature returns to life "
			"with Hit Points equal to <b>4d10 plus your Wisdom "
			"modifier</b>. Conditions removed on revival: Blinded, Deafened, "
			"Paralyzed, Poisoned, and Stunned.<br>Once you use this "
			"feature, you can't use it again until you finish a Long "
			"Rest."
			),
		)


# ---------------------------------------------------------------------------
# Warrior of the Open Hand
# ---------------------------------------------------------------------------


Open_Hand_Technique = _open_hand(
		name="Open Hand Technique",
		min_level=3,
		description=(
			"Whenever you hit a creature with an attack granted by your "
			"Flurry of Blows, you can impose one of the following "
			"effects on that target:"
			"<ul>"
			"<li><b>Addle.</b> The target can't make Opportunity "
			"Attacks until the start of its next turn.</li>"
			"<li><b>Push.</b> Strength save or be pushed up to 15 feet "
			"away from you.</li>"
			"<li><b>Topple.</b> Dexterity save or have the Prone "
			"condition.</li>"
			"</ul>"
			),
		)

Wholeness_of_Body = _open_hand(
		name="Wholeness of Body",
		min_level=6,
		description=(
			"As a <i>Bonus Action</i>, roll your Martial Arts die and "
			"regain Hit Points equal to the roll plus your Wisdom "
			"modifier (minimum 1).<br>You can use this feature a "
			"number of times equal to your Wisdom modifier (minimum "
			"once). "
			"All uses restore on a Long Rest."
			),
		)

Fleet_Step = _open_hand(
		name="Fleet Step",
		min_level=11,
		description=(
			"When you take a Bonus Action other than Step of the Wind, "
			"you can also use <b>Step of the Wind</b> immediately after "
			"that Bonus Action."
			),
		)

Quivering_Palm = _open_hand(
		name="Quivering Palm",
		min_level=17,
		description=(
			"When you hit a creature with an Unarmed Strike, you can "
			"expend <b>4 Focus Points</b> to start imperceptible "
			"vibrations in the target's body, lasting a number of days "
			"equal to your Monk level.<br>The vibrations are harmless "
			"until you end them. When you take the Attack action, you "
			"can forgo one attack to end the vibrations. To end them, "
			"you and the target must be on the same plane. When you end "
			"them, the target makes a Constitution save, taking "
			"<b>10d12 Force damage</b> on a failed save or half on "
			"success.<br>You can have only one creature under this "
			"effect at a time. You can end vibrations harmlessly with "
			"no action."
			),
		)


# ---------------------------------------------------------------------------
# Warrior of Shadow
# ---------------------------------------------------------------------------


Shadow_Arts = _shadow(
		name="Shadow Arts",
		min_level=3,
		description=(
			"You can use your discipline to create illusions and "
			"harness shadows.<br><b>Darkness.</b> Expend 1 Focus Point "
			"to cast <i>Darkness</i> without components. You can see "
			"within the spell's area. While active, you can move the "
			"Darkness to a space within 60 feet at the start of each of "
			"your turns.<br><b>Darkvision.</b> You gain Darkvision 60 "
			"feet (or +60 feet if you already have it)."
			"<br><b>Shadowy Figments.</b> You know the <i>Minor "
			"Illusion</i> cantrip. Wisdom is your spellcasting ability "
			"for it."
			),
		)

Shadow_Step = _shadow(
		name="Shadow Step",
		min_level=6,
		description=(
			"While entirely within Dim Light or Darkness, you can use a "
			"<i>Bonus Action</i> to <b>teleport up to 60 feet</b> to an "
			"unoccupied space you can see that is also in Dim Light or "
			"Darkness. You then have Advantage on the next melee attack "
			"you make before the end of the current turn."
			),
		)

Improved_Shadow_Step = _shadow(
		name="Improved Shadow Step",
		min_level=11,
		description=(
			"When you use your Shadow Step, you can expend 1 Focus "
			"Point to remove the requirement that you must start and "
			"end in Dim Light or Darkness for that use. As part of this "
			"Bonus Action, you can make an Unarmed Strike immediately "
			"after you teleport."
			),
		)

Cloak_of_Shadows = _shadow(
		name="Cloak of Shadows",
		min_level=17,
		description=(
			"As a <i>Magic action</i> while entirely within Dim Light "
			"or Darkness, expend <b>3 Focus Points</b> to shroud "
			"yourself with shadows for 1 minute (or until "
			"Incapacitated, or until you end your turn in Bright "
			"Light). While shrouded:"
			"<ul><li><b>Invisibility.</b> You have the Invisible "
			"condition.</li>"
			"<li><b>Partially Incorporeal.</b> You can move through "
			"occupied spaces as Difficult Terrain. If you end your turn "
			"in such a space, you are shunted to the last unoccupied "
			"space you were in.</li>"
			"<li><b>Shadow Flurry.</b> You can use Flurry of Blows "
			"without expending Focus Points.</li></ul>"
			),
		)


# ---------------------------------------------------------------------------
# Warrior of the Elements
# ---------------------------------------------------------------------------


Elemental_Attunement = _elements(
		name="Elemental Attunement",
		min_level=3,
		description=(
			"At the start of your turn, you can expend 1 Focus Point to "
			"imbue yourself with elemental energy for 10 minutes or "
			"until Incapacitated. While active:"
			"<ul><li><b>Reach.</b> Your Unarmed Strike reach is 10 feet "
			"greater than normal, as elemental energy extends from "
			"you.</li>"
			"<li><b>Elemental Strikes.</b> When you hit with an Unarmed "
			"Strike, you can deal Acid, Cold, Fire, Lightning, or "
			"Thunder damage instead. You can also force a Strength "
			"save; on a failed save, move the target up to 10 feet "
			"toward or away from you.</li>"
			"</ul>"
			),
		)

Manipulate_Elements = _elements(
		name="Manipulate Elements",
		min_level=3,
		description=(
			"You know the <i>Elementalism</i> cantrip. Wisdom is your "
			"spellcasting ability for it."
			),
		)

Elemental_Burst = _elements(
		name="Elemental Burst",
		min_level=6,
		description=(
			"As a <i>Magic action</i>, expend <b>2 Focus Points</b> to "
			"cause elemental energy to burst in a <b>20-foot-radius "
			"Sphere</b> centered on a point within 120 feet. Choose "
			"Acid, Cold, Fire, Lightning, or Thunder damage.<br>Each "
			"creature in the Sphere makes a Dexterity save. On a failed "
			"save, a creature takes damage equal to <b>three rolls of "
			"your Martial Arts die</b>. On a success, half damage."
			),
		)

Stride_of_the_Elements = _elements(
		name="Stride of the Elements",
		min_level=11,
		description=(
			"While your Elemental Attunement is active, you have a "
			"<b>Fly Speed and Swim Speed</b> equal to your Speed."
			),
		)

Elemental_Epitome = _elements(
		name="Elemental Epitome",
		min_level=17,
		description=(
			"While your Elemental Attunement is active, you gain the "
			"following additional benefits:<br><b>Damage Resistance.</b> "
			"Resistance to one of the following damage types of your "
			"choice: Acid, Cold, Fire, Lightning, or Thunder. You can "
			"change this choice at the start of each of your turns."
			"<br><b>Destructive Stride.</b> When you use Step of the "
			"Wind, your Speed increases by 20 feet until the end of the "
			"turn. Any creature of your choice takes damage equal to "
			"one roll of your Martial Arts die when you enter a space "
			"within 5 feet of it (once per turn). Damage type is your "
			"choice of Acid, Cold, Fire, Lightning, or Thunder."
			"<br><b>Empowered Strikes.</b> Once on each of your turns, "
			"you can deal extra damage equal to one Martial Arts die "
			"roll when you hit with an Unarmed Strike. Same damage type "
			"as the strike."
			),
		)
