"""
Bard Training Tags — 2024 PHB core + all Colleges.

Thought pattern
	1. Core lessons belong to the Bard Guild (no College).
	2. College lessons set ``path=…`` and awaken only for that College.
	3. Bardic Inspiration die is a Chip + callable Entry — not separate.
	4. ASI / Epic Boon picks stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasVenustas import Chip
from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
		Unarmored_Armour_Class,
		)


GUILD = "Bard"
CORE_SOURCE = "Training: Bard"
DANCE = "Dance"
GLAMOUR = "Glamour"
LORE = "Lore"
VALOR = "Valor"

def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)

def _bardic_die(
		char,
		) -> str:
	level = _rank(
			char,
			)
	if level >= 15:
		return "d12"
	if level >= 10:
		return "d10"
	if level >= 5:
		return "d8"
	return "d6"


def _bardic_uses(
		char,
		) -> int:
	from AtlasActorLudi.Map_of_Scores import Modifier
	cha = getattr(
			getattr(
					char,
					"abilities",
					None,
					),
			"CHA",
			10,
			)
	return max(
			1,
			Modifier(
					cha,
					),
			)

def _core(
		*,
		name: str,
		min_level: int,
		description,
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
			on_sheet=on_sheet,
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
			source=f"Training: College of {path_name}",
			)

def _dance(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			DANCE,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)

def _glamour(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			GLAMOUR,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)

def _lore(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			LORE,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)

def _valor(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _path(
			VALOR,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)

def _Untrained_Skill_Names(
		skills,
		) -> list[str]:
	"""
	Name every skill this Character is not yet proficient in.

	``get_all_skills`` answers with Skill objects; ``activate_proficiencies``
	compares each entry against a name. Handing it the objects matches
	nothing and grants nothing, which is how the College of Lore lost all
	three of its skills in silence.
	"""
	return [
		skill.name
		for skill in skills.get_all_skills()
		if skill.proficiency_level < 1
		]


# ---------------------------------------------------------------------------
# What the Dice Bag chose
#
# This is a generator, not a builder: every pick was rolled before the page
# existed, so no entry may read as though a decision is still pending
# (Documenta/Canon/Feature-Text.md). Each lesson below rolls its own pick and
# writes the result into a ledger on the Character, and its Entry reads that
# ledger back when the sheet is rendered.
# ---------------------------------------------------------------------------

_LEDGER = "bard_choices"


def _Ledger(
		char,
		) -> dict:
	"""The record of what each Bard lesson chose for this Character."""
	chosen = getattr(
			char,
			_LEDGER,
			None,
			)
	if chosen is None:
		chosen = {}
		setattr(
				char,
				_LEDGER,
				chosen,
				)
	return chosen


def _Recall(
		char,
		lesson: str,
		) -> tuple[str, ...]:
	"""What one lesson chose, or nothing if it has not run."""
	return _Ledger(
			char,
			).get(
			lesson,
			(),
			)


def _Named(
		entries,
		) -> str:
	"""Join names the way a sentence would: a, b and c."""
	names = list(
			entries
			)
	if not names:
		return ""
	if len(names) == 1:
		return names[0]
	return " and ".join(
			(
				", ".join(
						names[:-1]
						),
				names[-1],
				)
			)


def _Doubled_Skill_Names(
		char,
		) -> list[str]:
	"""Every skill whose Proficiency Bonus is already doubled."""
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return []
	return [
		skill.name
		for skill in skills.get_all_skills()
		if skill.proficiency_level >= 2
		]


def _Trained_Skill_Names(
		char,
		) -> list[str]:
	"""Every skill this Character is trained in, doubled or not."""
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return []
	return [
		skill.name
		for skill in skills.get_all_skills()
		if skill.proficiency_level >= 1
		]


def _Double_Two_Skills(
		char,
		lesson: str,
		) -> None:
	"""
	Double the Proficiency Bonus on two more trained skills, and record them.

	This used to run inside ``set_Skills``, which seats the Guild's three
	skills and reaches for Expertise straight away. The Background's two
	skills are seated afterwards, so the pool held three names when it
	should have held five, and the level 9 lesson regularly found nothing
	left to double. A Training awakens after the Background has taught, so
	the pool here is the whole sheet.
	"""
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return
	before = set(
			_Doubled_Skill_Names(
					char,
					)
			)
	skills.activate_expertise(
			2,
			skills.get_proficient_skills(),
			)
	_Ledger(
			char,
			)[lesson] = tuple(
			name
			for name in _Doubled_Skill_Names(
					char,
					)
			if name not in before
			)


def _apply_expertise(
		char,
		) -> None:
	"""The level 2 lesson doubles two skills."""
	_Double_Two_Skills(
			char,
			"Expertise",
			)


def _apply_expertise_II(
		char,
		) -> None:
	"""The level 9 lesson doubles two more."""
	_Double_Two_Skills(
			char,
			"Expertise (II)",
			)


def _apply_bonus_proficiencies(
		char,
		) -> None:
	"""College of Lore: three more skills go in the bag, and are named."""
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return
	before = set(
			_Trained_Skill_Names(
					char,
					)
			)
	skills.activate_proficiencies(
			3,
			_Untrained_Skill_Names(
					skills,
					),
			)
	_Ledger(
			char,
			)["Bonus Proficiencies"] = tuple(
			name
			for name in _Trained_Skill_Names(
					char,
					)
			if name not in before
			)


def _Highest_Spell_Rank(
		char,
		) -> int:
	"""
	The highest spell rank this Bard holds a slot for.

	The Bard is a full caster, so the rank climbs by one every second
	Guild level and stops at nine: rank 1 at Bard 1 and 2, rank 2 at 3
	and 4, and so on.
	"""
	level = _rank(
			char,
			)
	return min(
			9,
			(level + 1) // 2,
			)


def _Borrowable_Spells(
		char,
		):
	"""
	Cleric, Druid and Wizard spells this Bard could actually cast.

	A cantrip, or a spell of a rank they hold a slot for, exactly as the
	lesson's own wording requires.
	"""
	from AtlasLusoris.Grimoire_of_Spellcasters import SPELL_LISTS

	ceiling = _Highest_Spell_Rank(
			char,
			)
	borrowable = {}
	for guild in (
			"Cleric",
			"Druid",
			"Wizard",
			):
		for rank, bank in SPELL_LISTS.get(
				guild,
				{},
				).items():
			if rank > ceiling:
				continue
			for spell in bank:
				borrowable.setdefault(
						spell.name,
						spell,
						)
	return list(
			borrowable.values()
			)


def _apply_magical_discoveries(
		char,
		) -> None:
	"""College of Lore: two spells lifted from the other traditions."""
	from AtlasLusoris.Grimoire_of_Spellcasters import _pick_distinct

	held = {
		spell.name
		for spell in getattr(
				char,
				"known_spells",
				(),
				) or ()
		}
	pool = [
		spell
		for spell in _Borrowable_Spells(
				char,
				)
		if spell.name not in held
		]
	taken = _pick_distinct(
			char,
			pool,
			2,
			)
	for spell in taken:
		char.known_spells.append(
				spell
				)
	_Ledger(
			char,
			)["Magical Discoveries"] = tuple(
			spell.name
			for spell in taken
			)


def _apply_martial_training(
		char,
		) -> None:
	"""College of Valor: Martial weapons, Medium armor, Shields."""
	skills = getattr(
			char,
			"skills",
			None,
			)
	if skills is None:
		return
	for proficiency in (
			"Martial_Weapons",
			"Medium",
			"Shields",
			):
		trained = getattr(
				skills,
				proficiency,
				None,
				)
		if trained is not None:
			trained.set_proficiency()


def _bardic_entry(
		char,
		) -> str:
	die = _bardic_die(
			char,
			)
	uses = _bardic_uses(
			char,
			)
	level = _rank(
			char,
			)
	rest = "Short or Long" if level >= 5 else "Long"
	return _Sung(
			"Believe in them. You will see.",
			f"Your Bardic Inspiration die is a <b>{die}</b>. "
			"<br><b>Bonus Action:</b> inspire a creature within 60 feet "
			"that can see or hear you. That creature gains one Bardic "
			"Inspiration die. A creature can have only one Bardic Inspiration "
			"die at a time. "
			"<br>Once within the next hour, when the creature fails a D20 Test, "
			"it can roll the die and add the number to the d20, potentially "
			"turning failure into success. The die is expended when rolled. "
			f"<br>You can confer a total of <b>{uses} Bardic Inspiration dice</b>. "
			f"You regain all expended uses when you finish a <b>{rest} Rest</b>."
			)


def _Sung(
		line: str,
		rules: str,
		) -> str:
	"""
	One Entry: the line that inspires it, then the rule that pays it off.

	The inspiration line comes first and the mechanics follow, which is the
	house order for a Feature Entry, and the same shape the Fighter and the
	Barbarian already print. The lines are Julio's, from the wiki.
	"""
	return f"*{line}*\n\n{rules}"


def _expertise_entry(
		char,
		) -> str:
	"""
	Name every skill Expertise has doubled, both helpings in one entry.

	The level 9 lesson does not print a second time. It grows this one.
	The rules hand out Expertise twice, but a reader holding the sheet
	wants one answer to "which of my skills are doubled", not two entries
	to add up, and the second would repeat this one's line word for word.
	So the level 9 Training awakens with ``on_sheet=False``: it still
	rolls and grants its two, and what it chose is named here.
	"""
	chosen = _Recall(
			char,
			"Expertise",
			) + _Recall(
			char,
			"Expertise (II)",
			)
	if not chosen:
		return _Sung(
			"Learn your lines. Then we'll start.",
			"Your Proficiency Bonus is doubled for any ability check that "
			"uses a skill this lesson has doubled.",
			)
	return _Sung(
		"Learn your lines. Then we'll start.",
		f"Your Proficiency Bonus is <b>doubled</b> on "
		f"<b>{_Named(chosen)}</b>.",
		)


def _bonus_proficiencies_entry(
		char,
		) -> str:
	"""Name the three skills the College added."""
	chosen = _Recall(
			char,
			"Bonus Proficiencies",
			)
	if not chosen:
		return _Sung(
			"Knowledge dies unpractised.",
			"The College trains you in three more skills.",
			)
	return _Sung(
		"Knowledge dies unpractised.",
		f"The College trained you in <b>{_Named(chosen)}</b>.",
		)


def _magical_discoveries_entry(
		char,
		) -> str:
	"""Name the two spells lifted from the other traditions."""
	chosen = _Recall(
			char,
			"Magical Discoveries",
			)
	if not chosen:
		return _Sung(
			"Everyone keeps secrets. I keep copies.",
			"Two spells from the Cleric, Druid or Wizard traditions are "
			"always prepared for you, and never count against the number "
			"you prepare.",
			)
	return _Sung(
		"Everyone keeps secrets. I keep copies.",
		f"<b>{_Named(chosen)}</b> are always prepared for you, and never "
		"count against the number of spells you prepare.",
		)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------

Bardic_Inspiration = _core(
	name="Bardic Inspiration",
	min_level=1,
	description=_bardic_entry,
	chips=(
		Chip(
			"",
			"Bardic Die",
			_bardic_die,
			),
		Chip(
			"",
			"Bardic Uses",
			_bardic_uses,
			),
		),
	)

Spellcasting = _core(
	name="Spellcasting",
	min_level=1,
	description=_Sung(
		"Anyone can say the words. Few can play the role.",
		"You cast Bard spells through performance and wit. <b>Charisma</b> is "
		"your spellcasting ability. You know a selection of Bard spells from the "
		"Bard spell list, and you can replace one known spell when you gain a "
		"Bard level."
		),
	)

Expertise = _core(
	name="Expertise",
	min_level=2,
	description=_expertise_entry,
	apply=_apply_expertise,
	)

Jack_of_All_Trades = _core(
	name="Jack of All Trades",
	min_level=2,
	description=_Sung(
		"Theory says theory always works.",
		"You can add half your proficiency bonus (rounded down) to any ability "
		"check you make that doesn't already use your proficiency bonus."
		),
	)

Font_of_Inspiration = _core(
	name="Font of Inspiration",
	min_level=5,
	description=_Sung(
		"Passion, nap, repeat.",
		"You regain all your expended Bardic Inspiration uses when you finish a "
		"Short or Long Rest. <br>"
		"You can also expend a spell slot (no action required) to regain one "
		"expended use."
		),
	)

Countercharm = _core(
	name="Countercharm",
	min_level=7,
	description=_Sung(
		"Smoke and mirrors, sure, but transparent when you know the tricks.",
		"<b>Reaction:</b> when you, or a creature within 30 feet of you, fails a "
		"saving throw against an effect that applies the <b>Charmed</b> or "
		"<b>Frightened</b> condition, that saving throw is rerolled with "
		"Advantage. The new roll stands. <br>"
		"This spends no Bardic Inspiration, and there is no limit on how often "
		"you can do it."
		),
	)

Expertise_II = _core(
	name="Expertise (II)",
	min_level=9,
	description="",
	apply=_apply_expertise_II,
	on_sheet=False,
	)

Magical_Secrets = _core(
	name="Magical Secrets",
	min_level=10,
	description=_Sung(
		"You heard a song once and learnt it? That's cute.",
		"You have plundered magical knowledge from a wide spectrum of "
		"disciplines. Whenever your number of prepared spells increases, and "
		"whenever you replace one of them, you can take the spell from the "
		"<b>Cleric</b>, <b>Druid</b> or <b>Wizard</b> list as readily as your "
		"own. <br>"
		"A spell taken this way counts as a Bard spell for you."
		),
	)

Superior_Inspiration = _core(
	name="Superior Inspiration",
	min_level=18,
	description=_Sung(
		"Breathe in. Breathe out. Easy.",
		"When you roll Initiative, you regain expended uses of Bardic "
		"Inspiration until you have <b>two</b>."
		),
	)

Words_of_Creation = _core(
	name="Words of Creation",
	min_level=20,
	description=_Sung(
		"You are no longer an instrument. You are the conductor.",
		"You have mastered two of the Words of Creation: <em>Power Word Heal</em> "
		"and <em>Power Word Kill</em>. These spells are always prepared for you "
		"and don't count against your number of prepared spells. <br>"
		"When you cast either spell, you can target a second creature with the "
		"spell if that creature is within 10 feet of the first target."
		),
	)


# ---------------------------------------------------------------------------
# College of Dance
# ---------------------------------------------------------------------------

Dazzling_Footwork = _dance(
	name="Dazzling Footwork",
	min_level=3,
	description=_Sung(
		"Don't you dare look back. Just keep your eyes on me.",
		"While you aren't wearing armor or wielding a Shield, you gain:<ul>"
		"<li><b>Unarmored Defense.</b> Your base AC equals 10 + your Dexterity "
		"modifier + your Charisma modifier.</li>"
		"<li><b>Agile Strikes.</b> When you expend a use of your Bardic "
		"Inspiration as part of an action, Bonus Action, or Reaction, you can "
		"make one Unarmed Strike as part of that same action, Bonus Action, or "
		"Reaction.</li>"
		"<li><b>Bardic Damage.</b> You can use Dexterity instead of Strength for "
		"Unarmed Strike attack rolls. When you deal damage with an Unarmed "
		"Strike, you can deal Bludgeoning damage equal to a roll of your Bardic "
		"Inspiration die plus your Dexterity modifier (this roll doesn't expend "
		"the die).</li>"
		"</ul>"
		),
	chips=(
		Chip(
			"🩰",
			"Unarmored AC",
			Unarmored_Armour_Class,
			),
		),
	)

Inspiring_Movement = _dance(
	name="Inspiring Movement",
	min_level=6,
	description=_Sung(
		"Don't get so close",
		"When an enemy you can see ends its turn within 5 feet of you, you can "
		"take a Reaction and expend one use of your Bardic Inspiration to move up "
		"to half your Speed. One ally of your choice within 30 feet can then also "
		"move up to half their Speed using their Reaction. None of this movement "
		"provokes Opportunity Attacks."
		),
	)

Tandem_Footwork = _dance(
	name="Tandem Footwork",
	min_level=6,
	description=_Sung(
		"On your marks.",
		"When you roll Initiative (and don't have the Incapacitated condition), "
		"you can expend one use of your Bardic Inspiration. When you do, roll "
		"your Bardic Inspiration die; you and each ally within 30 feet that can "
		"see or hear you gain a bonus to Initiative equal to the number rolled."
		),
	)

Leading_Evasion = _dance(
	name="Leading Evasion",
	min_level=14,
	description=_Sung(
		"Watch out!",
		"When you are subjected to an effect that allows you to make a Dexterity "
		"saving throw to take only half damage, you instead take no damage on a "
		"success and only half damage on a failure. <br>"
		"If any creatures within 5 feet of you are making the same Dexterity "
		"saving throw, you can share this benefit with them for that save. You "
		"can't use this feature if you have the Incapacitated condition."
		),
	)


# ---------------------------------------------------------------------------
# College of Glamour
# ---------------------------------------------------------------------------

Beguiling_Magic = _glamour(
	name="Beguiling Magic",
	min_level=3,
	description=_Sung(
		"Adore me or dread me. Either way, you are mine.",
		"You always have the <em>Charm Person</em> and <em>Mirror Image</em> "
		"spells prepared. <br>"
		"Immediately after you cast an Enchantment or Illusion spell using a "
		"spell slot, you can cause a creature you can see within 60 feet to make "
		"a Wisdom saving throw (DC equals your spell save DC). On a failed save, "
		"the target has the Charmed or Frightened condition (your choice) for 1 "
		"minute. The target repeats the save at the end of each of its turns. <br>"
		"Once you use this benefit, you can't use it again until you finish a "
		"Long Rest. You can also restore it by expending one use of your Bardic "
		"Inspiration (no action required)."
		),
	)

Mantle_of_Inspiration = _glamour(
	name="Mantle of Inspiration",
	min_level=3,
	description=_Sung(
		"On your feet, darling. The night is young.",
		"<b>Bonus Action:</b> expend a use of Bardic Inspiration and roll the "
		"die. Choose a number of other creatures within 60 feet, up to your "
		"Charisma modifier (minimum one). Each chosen creature gains Temporary "
		"Hit Points equal to <b>2 × the number rolled</b> and can use its "
		"Reaction to move up to its Speed without provoking Opportunity Attacks."
		),
	)

Mantle_of_Majesty = _glamour(
	name="Mantle of Majesty",
	min_level=6,
	description=_Sung(
		"Say no, then. I'll wait.",
		"You always have the <em>Command</em> spell prepared. <br>"
		"<b>Bonus Action:</b> cast <em>Command</em> without expending a spell "
		"slot and assume an unearthly appearance for 1 minute or until your "
		"Concentration ends. While this lasts, you can cast Command as a Bonus "
		"Action on each turn (no slot required). <br>"
		"Any creature Charmed by you automatically fails its saving throw against "
		"the Command you cast with this feature. <br>"
		"Once used, you can't use it again until you finish a Long Rest, or until "
		"you expend a level-3+ spell slot (no action required)."
		),
	)

Unbreakable_Majesty = _glamour(
	name="Unbreakable Majesty",
	min_level=14,
	description=_Sung(
		"Go on, bite. Pure gold.",
		"<b>Bonus Action:</b> assume a magically majestic presence for 1 minute "
		"or until you have the Incapacitated condition. <br>"
		"For the duration, the first time each turn any creature hits you with an "
		"attack roll, the attacker must succeed on a Charisma saving throw "
		"against your spell save DC or the attack misses instead, as the creature "
		"recoils from your majesty. <br>"
		"Once used, you can't use it again until you finish a Short or Long Rest."
		),
	)


# ---------------------------------------------------------------------------
# College of Lore
# ---------------------------------------------------------------------------

Bonus_Proficiencies = _lore(
	name="Bonus Proficiencies",
	min_level=3,
	description=_bonus_proficiencies_entry,
	apply=_apply_bonus_proficiencies,
	)

Cutting_Words = _lore(
	name="Cutting Words",
	min_level=3,
	description=_Sung(
		"I only cut them short. Truth is the best distraction.",
		"<b>Reaction:</b> when a creature you can see within 60 feet makes a "
		"damage roll or succeeds on an ability check or attack roll, you can "
		"expend one use of Bardic Inspiration and roll the die. Subtract the "
		"number rolled from the creature's roll, potentially turning success into "
		"failure or reducing damage."
		),
	)

Magical_Discoveries = _lore(
	name="Magical Discoveries",
	min_level=6,
	description=_magical_discoveries_entry,
	apply=_apply_magical_discoveries,
	)

Peerless_Skill = _lore(
	name="Peerless Skill",
	min_level=14,
	description=_Sung(
		"Don't panic. Keep thinking. Fail better",
		"When you make an ability check or attack roll and fail, you can expend "
		"one use of Bardic Inspiration. Roll the Bardic Inspiration die and add "
		"the number rolled to your d20, potentially turning a failure into a "
		"success. On a failure, the Bardic Inspiration use is not expended."
		),
	)


# ---------------------------------------------------------------------------
# College of Valor
# ---------------------------------------------------------------------------

Combat_Inspiration = _valor(
	name="Combat Inspiration",
	min_level=3,
	description=_Sung(
		"Hold the line. I'll hold your back.",
		"A creature that has a Bardic Inspiration die from you can use it for one "
		"of the following effects:<ul>"
		"<li><b>Defense.</b> When the creature is hit by an attack roll, it can "
		"use its Reaction to roll the die and add the number to its AC against "
		"that attack, potentially causing the attack to miss.</li>"
		"<li><b>Offense.</b> Immediately after the creature hits a target with an "
		"attack roll, it can roll the die and add the number to the attack's "
		"damage against the target.</li>"
		"</ul>"
		),
	)

Martial_Training = _valor(
	name="Martial Training",
	min_level=3,
	description=_Sung(
		"Blade and board. Some weights are worth holding onto.",
		"You gain proficiency with Martial weapons and training with Medium Armor "
		"and Shields. <br>"
		"In addition, you can use a Simple or Martial weapon as a Spellcasting "
		"Focus to cast spells from your Bard spell list."
		),
	apply=_apply_martial_training,
	)

Valor_Extra_Attack = _valor(
	name="Extra Attack",
	min_level=6,
	description=_Sung(
		"Hold fast. Every strike is a refusal to be moved.",
		"You can attack twice instead of once whenever you take the Attack action "
		"on your turn. <br>"
		"In addition, you can cast one of your cantrips that has a casting time "
		"of an action in place of one of those attacks."
		),
	)

Battle_Magic = _valor(
	name="Battle Magic",
	min_level=14,
	description=_Sung(
		"Never hold back.",
		"After you cast a spell that has a casting time of an action, you can "
		"make one attack with a weapon or Unarmed Strike as a Bonus Action."
		),
	)
