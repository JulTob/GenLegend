"""
Cleric Training Tags — 2024 Player's Handbook.

Core lessons belong to the Cleric Guild. Domain lessons set ``path=…`` and
awaken only for that Domain. ASI / Epic Boon picks stay on legacy Progression.
"""

from __future__ import annotations

import random

from AtlasLusoris.TrainingKit import Make_Training
from AtlasVenustas import Chip


GUILD = "Cleric"
CORE_SOURCE = "Training: Cleric"
LIFE = "Life"
LIGHT = "Light"
TRICKERY = "Trickery"
WAR = "War"


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
	score = int(
		getattr(
			getattr(
				char,
				"AS",
				None,
				),
			"WIS",
			10,
			) or 10
		)
	return (
		score - 10
		) // 2


def _channel_uses(
		char,
		) -> int:
	level = _rank(
			char
			)
	if level >= 18:
		return 4
	if level >= 6:
		return 3
	return 2


def _divine_spark_dice(
		char,
		) -> int:
	"""Number of d8s for Divine Spark (2024): 1, then 2/3/4 at 7/13/18."""
	level = _rank(
			char
			)
	if level >= 18:
		return 4
	if level >= 13:
		return 3
	if level >= 7:
		return 2
	return 1


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
			source=f"Training: {path_name} Domain",
			)


def _life(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			LIFE,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _light(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			LIGHT,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _trickery(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			TRICKERY,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _war(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			WAR,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


# ---------------------------------------------------------------------------
# Callable entries (level-sensitive text)
# ---------------------------------------------------------------------------


def _channel_entry(
		char,
		) -> str:
	uses = _channel_uses(
			char
			)
	spark_dice = _divine_spark_dice(
			char
			)
	dice_label = (
		f"{spark_dice}d8"
		if spark_dice > 1
		else "1d8"
		)
	return (
		"You can channel divine energy directly from the Outer Planes to fuel "
		"magical effects. "
		f"You can use this class's Channel Divinity <b>{uses} times</b>. "
		"You regain one expended use when you finish a Short Rest, and you "
		"regain all expended uses when you finish a Long Rest."
		"<br>Each time you use Channel Divinity, choose one effect you know. "
		"You start with Divine Spark and Turn Undead."
		"<ul>"
		f"<li><b>Divine Spark.</b> Magic action. Point your Holy Symbol at "
		"another creature you can see within 30 feet. "
		f"Roll <b>{dice_label}</b> and add your Wisdom modifier. "
		"You either restore Hit Points to the creature equal to that total, "
		"or force it to make a Constitution saving throw. On a failed save, "
		"it takes Necrotic or Radiant damage (your choice) equal to that total. "
		"On a successful save, it takes half as much damage (round down). "
		"You roll an additional d8 at Cleric levels 7 (2d8), 13 (3d8), and "
		"18 (4d8).</li>"
		"<li><b>Turn Undead.</b> Magic action. Present your Holy Symbol. "
		"Each Undead of your choice within 30 feet must make a Wisdom saving "
		"throw. On a failed save, it has the Frightened and Incapacitated "
		"conditions for 1 minute. For that duration, it tries to move as far "
		"from you as it can on its turns. The effect ends early on a creature "
		"if it takes any damage, if you have the Incapacitated condition, or "
		"if you die.</li>"
		"</ul>"
		"<br>If a Channel Divinity effect requires a saving throw, the DC "
		"equals your Cleric spell save DC."
		)


def _fork_rng(
		char,
		salt,
		):
	seed = getattr(
		char,
		"seed",
		None,
		)
	if seed is None:
		seed = getattr(
			char,
			"name",
			"",
			) or 0
	return random.Random(
		f"{seed}:{salt}"
		)


def _apply_divine_order(
		char,
		):
	order = getattr(
		char,
		"divine_order",
		None,
		)
	if order not in (
			"Protector",
			"Thaumaturge",
			):
		order = _fork_rng(
			char,
			"divine_order",
			).choice(
			(
				"Protector",
				"Thaumaturge",
				)
			)
		char.divine_order = order

	skills = getattr(
		char,
		"skills",
		None,
		)
	if skills is None:
		return

	if order == "Protector":
		if hasattr(
				skills,
				"Martial_Weapons",
				):
			skills.Martial_Weapons.set_proficiency()
		if hasattr(
				skills,
				"Heavy",
				):
			skills.Heavy.set_proficiency()
		return

	# Thaumaturge: Wis mod (min +1) to Intelligence (Arcana or Religion) checks.
	bonus = max(
		1,
		_wis_mod(
			char
			),
		)
	char.thaumaturge_check_bonus = bonus
	for skill_name in (
			"Arcana",
			"Religion",
			):
		skill = getattr(
			skills,
			skill_name,
			None,
			)
		if skill is None:
			continue
		prior = int(
			getattr(
				skill,
				"flat_bonus",
				0,
				) or 0
			)
		skill.flat_bonus = prior + bonus


def _divine_order_entry(
		char,
		) -> str:
	if getattr(
			char,
			"divine_order",
			None,
			) == "Protector":
		return (
			"<b>Protector.</b> Trained for battle, you gain proficiency with "
			"Martial weapons and training with Heavy armor."
			)
	bonus = getattr(
		char,
		"thaumaturge_check_bonus",
		None,
		)
	if bonus is None:
		bonus = max(
			1,
			_wis_mod(
				char
				),
			)
	return (
		"<b>Thaumaturge.</b> You know one extra cantrip from the Cleric spell "
		"list. In addition, your mystical connection to the divine gives you a "
		f"<b>+{bonus}</b> bonus to your Intelligence (Arcana or Religion) "
		"checks (equal to your Wisdom modifier, minimum +1)."
		)


def _apply_blessed_strikes(
		char,
		):
	if getattr(
			char,
			"blessed_strikes",
			None,
			) not in (
			"Divine Strike",
			"Potent Spellcasting",
			):
		char.blessed_strikes = _fork_rng(
			char,
			"blessed_strikes",
			).choice(
			(
				"Divine Strike",
				"Potent Spellcasting",
				)
			)


def _blessed_strikes_entry(
		char,
		) -> str:
	if getattr(
			char,
			"blessed_strikes",
			None,
			) == "Potent Spellcasting":
		return (
			"<b>Potent Spellcasting.</b> Add your Wisdom modifier to the "
			"damage you deal with any Cleric cantrip."
			)
	return (
		"<b>Divine Strike.</b> Once on each of your turns when you hit a "
		"creature with an attack roll using a weapon, you can cause the target "
		"to take an extra <b>1d8</b> Necrotic or Radiant damage (your choice)."
		)


def _improved_blessed_strikes_entry(
		char,
		) -> str:
	if getattr(
			char,
			"blessed_strikes",
			None,
			) == "Potent Spellcasting":
		return (
			"<b>Potent Spellcasting improves.</b> When you cast a Cleric "
			"cantrip and deal damage to a creature with it, you can give "
			"vitality to yourself or another creature within 60 feet of "
			"yourself, granting Temporary Hit Points equal to "
			"<b>twice your Wisdom modifier</b>."
			)
	return (
		"<b>Divine Strike improves.</b> The extra damage of your Divine Strike "
		"increases to <b>2d8</b>."
		)


# ---------------------------------------------------------------------------
# Core Guild lessons (2024)
# ---------------------------------------------------------------------------


Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description=(
			"You have learned to cast spells through prayer and meditation. "
			"<b>Wisdom</b> is your spellcasting ability for your Cleric spells. "
			"You can use a Holy Symbol as a Spellcasting Focus for them."
			"<br>You know cantrips and prepare level 1+ Cleric spells as shown "
			"in the Cleric Features table. Whenever you finish a Long Rest, "
			"you can change your list of prepared spells. Spells granted by "
			"other Cleric features that you always have prepared do not count "
			"against that number."
			),
		)

Divine_Order = _core(
		name="Divine Order",
		min_level=1,
		description=_divine_order_entry,
		apply=_apply_divine_order,
		)

Channel_Divinity = _core(
		name="Channel Divinity",
		min_level=2,
		description=_channel_entry,
		chips=(
				Chip(
					"🕊️",
					"Channel Divinity Uses",
					_channel_uses,
					),
				),
		)

Sear_Undead = _core(
		name="Sear Undead",
		min_level=5,
		description=(
			"Whenever you use Turn Undead, you can roll a number of d8s equal "
			"to your Wisdom modifier (minimum of 1d8) and add the rolls "
			"together. Each Undead that fails its saving throw against that "
			"use of Turn Undead takes Radiant damage equal to the total. "
			"This damage doesn't end the turn effect."
			),
		)

Blessed_Strikes = _core(
		name="Blessed Strikes",
		min_level=7,
		description=_blessed_strikes_entry,
		apply=_apply_blessed_strikes,
		)

Divine_Intervention = _core(
		name="Divine Intervention",
		min_level=10,
		description=(
			"You can call on your deity or pantheon to intervene on your "
			"behalf. As a Magic action, choose any Cleric spell of level 5 or "
			"lower that doesn't require a Reaction to cast. As part of the same "
			"action, you cast that spell without expending a spell slot or "
			"needing Material components. "
			"You can't use this feature again until you finish a Long Rest."
			),
		)

Improved_Blessed_Strikes = _core(
		name="Improved Blessed Strikes",
		min_level=14,
		description=_improved_blessed_strikes_entry,
		)

Greater_Divine_Intervention = _core(
		name="Greater Divine Intervention",
		min_level=20,
		description=(
			"You can call on even more powerful divine intervention. When you "
			"use your Divine Intervention feature, you can choose <em>Wish</em> "
			"when you select a spell. If you do so, you can't use Divine "
			"Intervention again until you finish <b>2d4 Long Rests</b>."
			),
		)


# ---------------------------------------------------------------------------
# Life Domain (2024)
# ---------------------------------------------------------------------------


Life_Domain_Spells = _life(
		name="Domain Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared. They don't count "
			"against the number of spells you can prepare with Spellcasting."
			"<ul>"
			"<li><b>3rd:</b> <em>Aid, Bless, Cure Wounds, Lesser Restoration</em></li>"
			"<li><b>5th:</b> <em>Prayer of Healing, Mass Healing Word</em></li>"
			"<li><b>9th:</b> <em>Revivify, Mass Cure Wounds</em></li>"
			"<li><b>13th:</b> <em>Aura of Life, Death Ward</em></li>"
			"<li><b>17th:</b> <em>Greater Restoration, Heal</em></li>"
			"</ul>"
			),
		)

Disciple_of_Life = _life(
		name="Disciple of Life",
		min_level=3,
		description=(
			"When a spell you cast with a spell slot restores Hit Points to a "
			"creature, that creature regains additional Hit Points equal to "
			"<b>2 + the spell's level</b> on the turn you cast the spell."
			),
		)

Preserve_Life = _life(
		name="Preserve Life",
		min_level=3,
		description=(
			"<b>Channel Divinity — Magic action.</b> "
			"You evoke healing energy that can restore a number of Hit Points "
			"equal to <b>five times your Cleric level</b>. Choose Bloodied "
			"creatures within 30 feet of yourself (which can include you), and "
			"distribute those Hit Points among them. This feature can restore a "
			"creature to no more than half of its Hit Point maximum."
			),
		)

Blessed_Healer = _life(
		name="Blessed Healer",
		min_level=6,
		description=(
			"The healing spells you cast on others heal you as well. "
			"When you cast a spell with a spell slot that restores Hit Points "
			"to a creature other than yourself, you regain Hit Points equal to "
			"<b>2 + the spell's level</b>."
			),
		)

Supreme_Healing = _life(
		name="Supreme Healing",
		min_level=17,
		description=(
			"When you would normally roll one or more dice to restore Hit "
			"Points with a spell or Channel Divinity, you instead use the "
			"highest number possible for each die."
			),
		)


# ---------------------------------------------------------------------------
# Light Domain (2024)
# ---------------------------------------------------------------------------


Light_Domain_Spells = _light(
		name="Domain Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared. They don't count "
			"against the number of spells you can prepare with Spellcasting."
			"<ul>"
			"<li><b>3rd:</b> <em>Burning Hands, Faerie Fire, Scorching Ray, See Invisibility</em></li>"
			"<li><b>5th:</b> <em>Daylight, Fireball</em></li>"
			"<li><b>9th:</b> <em>Arcane Eye, Wall of Fire</em></li>"
			"<li><b>13th:</b> <em>Flame Strike, Scrying</em></li>"
			"</ul>"
			),
		)

Radiance_of_the_Dawn = _light(
		name="Radiance of the Dawn",
		min_level=3,
		description=(
			"<b>Channel Divinity — Magic action.</b> "
			"You present your Holy Symbol, and any Magical Darkness within "
			"30 feet of you is dispelled. Additionally, each creature of your "
			"choice within 30 feet must make a Constitution saving throw. On a "
			"failed save, a creature takes Radiant damage equal to "
			"<b>2d10 + your Cleric level</b>, or half as much on a successful "
			"save."
			),
		)

Warding_Flare = _light(
		name="Warding Flare",
		min_level=3,
		description=(
			"<b>Reaction:</b> when a creature you can see within 30 feet of "
			"yourself makes an attack roll, you can impose Disadvantage on "
			"that attack roll. "
			"<br>You can use this feature a number of times equal to your "
			"Wisdom modifier (minimum once). You regain all expended uses when "
			"you finish a Long Rest."
			),
		)

Improved_Warding_Flare = _light(
		name="Improved Warding Flare",
		min_level=6,
		description=(
			"You regain all expended uses of Warding Flare when you finish a "
			"Short or Long Rest. "
			"<br>In addition, when you use Warding Flare, the target of the "
			"triggering attack gains Temporary Hit Points equal to "
			"<b>2d6 + your Wisdom modifier</b>."
			),
		)

Corona_of_Light = _light(
		name="Corona of Light",
		min_level=17,
		description=(
			"<b>Magic action:</b> you cause yourself to emanate an aura of "
			"sunlight that lasts for 1 minute or until you end it (no action "
			"required). You emit Bright Light in a 60-foot radius and Dim Light "
			"for an additional 30 feet. "
			"<br>Your enemies in the Bright Light have Disadvantage on saving "
			"throws against your Radiance of the Dawn and against any spell "
			"that deals Fire or Radiant damage. "
			"<br>You can use this feature a number of times equal to your "
			"Wisdom modifier (minimum once). You regain all expended uses when "
			"you finish a Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Trickery Domain (2024)
# ---------------------------------------------------------------------------


Trickery_Domain_Spells = _trickery(
		name="Domain Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared. They don't count "
			"against the number of spells you can prepare with Spellcasting."
			"<ul>"
			"<li><b>3rd:</b> <em>Charm Person, Disguise Self, Invisibility, Pass without Trace</em></li>"
			"<li><b>5th:</b> <em>Hypnotic Pattern, Nondetection</em></li>"
			"<li><b>9th:</b> <em>Confusion, Dimension Door</em></li>"
			"<li><b>13th:</b> <em>Dominate Person, Modify Memory</em></li>"
			"</ul>"
			),
		)

Blessing_of_the_Trickster = _trickery(
		name="Blessing of the Trickster",
		min_level=3,
		description=(
			"<b>Magic action:</b> you can give yourself or a willing creature "
			"within 30 feet of yourself Advantage on Dexterity (Stealth) "
			"checks. This blessing lasts until you finish a Long Rest or until "
			"you use this feature again."
			),
		)

Invoke_Duplicity = _trickery(
		name="Invoke Duplicity",
		min_level=3,
		description=(
			"<b>Channel Divinity — Bonus Action.</b> "
			"You create a perfect visual illusion of yourself in an unoccupied "
			"space you can see within 30 feet. The illusion lasts for 1 minute "
			"or until you dismiss it (no action required). It does not require "
			"Concentration."
			"<br>As a Bonus Action on your later turns, you can move the "
			"illusion up to 30 feet to a space you can see."
			"<br>You can cast spells as though you were in the illusion's "
			"space, using your own senses. You have Advantage on attack rolls "
			"against any creature within 5 feet of the illusion."
			),
		)

Tricksters_Transposition = _trickery(
		name="Trickster's Transposition",
		min_level=6,
		description=(
			"Whenever you create or move your Invoke Duplicity illusion with a "
			"Bonus Action, you can teleport, swapping places with the illusion."
			),
		)

Improved_Duplicity = _trickery(
		name="Improved Duplicity",
		min_level=17,
		description=(
			"The power of your Invoke Duplicity improves:"
			"<br><b>Shared Distraction.</b> You and your allies have Advantage "
			"on attack rolls against any creature within 5 feet of the illusion."
			"<br><b>Healing Illusion.</b> When the illusion ends, you or one "
			"creature of your choice within 5 feet of it regains Hit Points "
			"equal to your Cleric level."
			),
		)


# ---------------------------------------------------------------------------
# War Domain (2024)
# ---------------------------------------------------------------------------


War_Domain_Spells = _war(
		name="Domain Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared. They don't count "
			"against the number of spells you can prepare with Spellcasting."
			"<ul>"
			"<li><b>3rd:</b> <em>Guiding Bolt, Magic Weapon, Shield of Faith, Spiritual Weapon</em></li>"
			"<li><b>5th:</b> <em>Crusader's Mantle, Spirit Guardians</em></li>"
			"<li><b>9th:</b> <em>Fire Shield, Freedom of Movement</em></li>"
			"<li><b>13th:</b> <em>Hold Monster, Steel Wind Strike</em></li>"
			"</ul>"
			),
		)

Guided_Strike = _war(
		name="Guided Strike",
		min_level=3,
		description=(
			"<b>Channel Divinity — Reaction.</b> "
			"When you or a creature within 30 feet of you misses with an attack "
			"roll, you can grant a <b>+10 bonus</b> to the attack roll, "
			"potentially turning the miss into a hit. You can use this feature "
			"after seeing the roll but before any effects of the roll are applied."
			),
		)

War_Priest = _war(
		name="War Priest",
		min_level=3,
		description=(
			"When you take the Attack action, you can make one attack with a "
			"weapon or an Unarmed Strike as a Bonus Action."
			"<br>You can use this feature a number of times equal to your "
			"Wisdom modifier (minimum once). You regain all expended uses when "
			"you finish a Short or Long Rest."
			),
		)

War_Gods_Blessing = _war(
		name="War God's Blessing",
		min_level=6,
		description=(
			"<b>Channel Divinity.</b> "
			"You can expend a use of your Channel Divinity to cast "
			"<em>Shield of Faith</em> or <em>Spiritual Weapon</em> without "
			"expending a spell slot. When you cast the spell this way, it "
			"doesn't require Concentration, and it lasts for 1 minute."
			),
		)

Avatar_of_Battle = _war(
		name="Avatar of Battle",
		min_level=17,
		description=(
			"You gain Resistance to Bludgeoning, Piercing, and Slashing damage."
			),
		)
