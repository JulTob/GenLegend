"""
Warlock Training Tags — 2024 PHB core + all Patrons.

Thought pattern
        1. Core lessons belong to the Warlock Guild (no Patron).
        2. Patron lessons set path=… and awaken only for that Patron.
        3. Invocation counts and Pact Magic slots live as Chips and callables.
        4. ASI / Epic Boon stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.FeaturesKit import Grant_Resistance
from AtlasLusoris.TrainingKit import Make_Training


GUILD = "Warlock"
CORE_SOURCE = "Training: Warlock"
ARCHFEY = "Archfey"
CELESTIAL = "Celestial"
FIEND = "Fiend"
GREAT_OLD_ONE = "Great Old One"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _invocations_known(
		char,
		) -> int:
	level = _rank(
			char
			)
	table = (
			1, 3, 3, 3, 5, 5, 6, 6, 7, 7,
			7, 8, 8, 8, 9, 9, 9, 10, 10, 10,
			)
	return table[min(
			level,
			20,
			) - 1]


def _pact_row(
		char,
		) -> dict:
	"""
This Warlock's row of the Pact Magic table.

Read, never recomputed.  The table in ``Grimoire_of_Spellcasters`` is what
the sheet actually casts from, and a second copy of the progression here
was quietly disagreeing with it: it granted one slot below level 11 and two
above, where the rules give one, then two, then three, then four.
"""
	from AtlasLusoris.Grimoire_of_Spellcasters import WARLOCK_SPELLCASTING_TABLE

	# Clamped into the table's own range: a level 0 build reads row 1,
	# an over-levelled one reads row 20.
	return WARLOCK_SPELLCASTING_TABLE.get(
			min(
					max(
							_rank(char),
							1,
							),
					20,
					),
			WARLOCK_SPELLCASTING_TABLE[20],
			)


def _pact_slot_level(
		char,
		) -> int:
	return _pact_row(char)["slot_level"]


def _pact_slots(
		char,
		) -> int:
	return _pact_row(char)["slots"][0]


def _pact_magic_entry(
		char,
		) -> str:
	row = _pact_row(char)
	slots = row["slots"][0]
	plural = "" if slots == 1 else "s"
	return (
		"Through occult ceremony you have formed a pact with a "
		"mysterious entity. You have <b>"
		f"{slots} Pact Magic slot{plural}</b> of spell level <b>"
		f"{row['slot_level']}</b>. All of your slots are of that level, "
		"and you regain all expended Pact Magic slots when you finish "
		"a Short or Long Rest."
		)


def _mystic_arcanum_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	arcana = []
	if level >= 11:
		arcana.append("6th")
	if level >= 13:
		arcana.append("7th")
	if level >= 15:
		arcana.append("8th")
	if level >= 17:
		arcana.append("9th")
	if not arcana:
		return "Mystic Arcanum not yet unlocked at this level."
	known = ", ".join(
			arcana
			)
	return (
		"Your patron grants you a magical secret called an arcanum. You "
		"choose one Warlock spell at each of these levels as an arcanum: <b>"
		f"{known}</b>. You can cast each of them once without a spell "
		"slot, and you regain all uses when you finish a Long Rest."
		)


def _magical_cunning_entry(
		char,
		) -> str:
	"""
Recovery moved from a rite to the moment of danger.

The published feature is a one-minute rite, once per Long Rest, for half
your slots.  A minute of quiet is a Short Rest with extra steps, and the
Warlock refills on a Short Rest anyway, so the feature only mattered in a
window that barely exists.

Hung on Initiative it costs almost nothing in power -- a party that rests
after every fight already had this -- and it buys the class its fantasy.
Attrition still bites, because **Hit Points do not come back**.  You get
what you signed for, which is power and not rescue: more dangerous every
round, and no closer to surviving.
"""
	slots = _pact_slots(char)
	plural = "" if slots == 1 else "s"

	return (
		"You keep a line open, and it answers when you are about to "
		"need it. <b>When you roll Initiative, you regain all expended "
		f"Pact Magic spell slots</b>: {slots} slot{plural} at spell level "
		f"{_pact_slot_level(char)}, with no limit on how often. What "
		"comes back is power, not rescue. Your wounds stay exactly "
		"where they are."
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


def _patron(
		patron_name: str,
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
			path=patron_name,
			source=f"Training: The {patron_name} Patron",
			)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Eldritch_Invocations = _core(
		name="Eldritch Invocations",
		min_level=1,
		description=(
			"You have unearthed Eldritch Invocations: pieces of forbidden "
			"knowledge that imbue you with an abiding magical ability or "
			"other lessons. If an invocation has a prerequisite, you must "
			"meet it to learn that invocation. You can't pick the same "
			"invocation more than once unless its description says otherwise."
			),
		chips=(
				("Invocations Known", _invocations_known, "🧿"),
				),
		)

Pact_Magic = _core(
		name="Pact Magic",
		min_level=1,
		description=_pact_magic_entry,
		chips=(
				("Pact Slots", _pact_slots, "🕯️"),
				("Pact Slot Level", _pact_slot_level, "💠"),
				),
		)

Magical_Cunning = _core(
		name="Magical Cunning",
		min_level=2,
		description=_magical_cunning_entry,
		)

Contact_Patron = _core(
		name="Contact Patron",
		min_level=9,
		description=(
			"In the past you contacted your patron through intermediaries. "
			"Now you can communicate directly: you always have <i>Contact "
			"Other Plane</i> prepared. With this feature you can cast the "
			"spell without expending a spell slot to contact your patron, "
			"and you automatically succeed on the spell's saving throw. "
			"Once you cast it this way, you can't do so again until you "
			"finish a Long Rest."
			),
		)

Mystic_Arcanum = _core(
		name="Mystic Arcanum",
		min_level=11,
		description=_mystic_arcanum_entry,
		)

Eldritch_Master = _core(
		name="Eldritch Master",
		min_level=20,
		description=(
			"When you roll Initiative, you can regain one expended use of "
			"your Mystic Arcanum."
			),
		)


# ---------------------------------------------------------------------------
# The Archfey Patron
# ---------------------------------------------------------------------------


def _archfey(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _patron(
			ARCHFEY,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


Archfey_Spells = _archfey(
		name="Archfey Spells",
		min_level=3,
		description=(
			"The magic of your patron ensures you always have certain spells prepared. <b>Level 3.</b> <i>Calm Emotions, Faerie Fire, Misty Step, Phantasmal Force, Sleep.</i>"
			"<br><b>Level 5.</b> <i>Blink, Plant Growth.</i><br><b>Level 7.</b> <i>Dominate Beast, Greater Invisibility.</i>"
			"<br><b>Level 9.</b> <i>Dominate Person, Seeming.</i> These don't count against the number of spells you prepare."
			),
		)

Steps_of_the_Fey = _archfey(
		name="Steps of the Fey",
		min_level=3,
		description=(
			"Your patron bestowed on you the ability to move between the "
			"boundaries of the planes. You can cast <i>Misty Step</i> "
			"without expending a spell slot a number of times equal to "
			"your Charisma modifier (minimum of once), and you regain all "
			"expended uses when you finish a Long Rest. Whenever you cast "
			"that spell, you can choose one of the following additional "
			"effects. <br><b>Refreshing Step.</b> Immediately after you "
			"teleport, you or one creature you can see within 10 feet of "
			"yourself gains 1d10 Temporary Hit Points. <br><b>Taunting "
			"Step.</b> Creatures within 5 feet of the space you left must "
			"succeed on a Wisdom saving throw against your spell save DC "
			"or have Disadvantage on attack rolls against creatures other "
			"than you until the start of your next turn."
			),
		)

Misty_Escape = _archfey(
		name="Misty Escape",
		min_level=6,
		description=(
			"You can cast <i>Misty Step</i> as a Reaction in response to "
			"taking damage. In addition, the following effects are now "
			"among your Steps of the Fey options. <br><b>Disappearing "
			"Step.</b> You have the Invisible condition until the start "
			"of your next turn or until immediately after you make an "
			"attack roll, deal damage, or cast a spell. <br><b>Dreadful "
			"Step.</b> Creatures within 5 feet of the space you left or "
			"the space you appear in (your choice) must succeed on a "
			"Wisdom saving throw against your spell save DC or take 2d10 "
			"Psychic damage."
			),
		)

Beguiling_Defenses = _archfey(
		name="Beguiling Defenses",
		min_level=10,
		description=(
			"Your patron taught you how to guard your mind and body. You "
			"are immune to the Charmed condition. In addition, immediately "
			"after a creature you can see hits you with an attack roll, "
			"you can take a Reaction to reduce the damage you take by "
			"half (round down), and you can force the attacker to make a "
			"Wisdom saving throw against your spell save DC. On a failed "
			"save the attacker takes Psychic damage equal to the damage "
			"you take. Once you use this Reaction, you can't use it again "
			"until you finish a Long Rest, unless you expend a Pact Magic "
			"spell slot (no action required) to restore your use of it."
			),
		)

Bewitching_Magic = _archfey(
		name="Bewitching Magic",
		min_level=14,
		description=(
			"Your patron granted you the ability to weave your magic with "
			"teleportation. Immediately after you cast an Enchantment or "
			"Illusion spell using an action and a spell slot, you can cast "
			"<i>Misty Step</i> as part of the same action and without expending a spell slot."
			),
		)


# ---------------------------------------------------------------------------
# The Celestial Patron
# ---------------------------------------------------------------------------


def _celestial(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _patron(
			CELESTIAL,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _healing_light_dice(
		char,
		) -> int:
	"""One plus your Warlock level.  Was level + 5, which is the 2014 pool."""
	return _rank(
			char
			) + 1


def _charisma_modifier(
		char,
		) -> int:
	scores = getattr(
			char,
			"AS",
			None,
			)

	if scores is None:
		return 1

	return max(
			1,
			(
					int(
							getattr(
									scores,
									"CHA",
									10,
									)
							) - 10
					) // 2,
			)


Celestial_Spells = _celestial(
		name="Celestial Spells",
		min_level=3,
		description=(
			"The magic of your patron ensures you always have certain spells prepared. <b>Level 3.</b> <i>Aid, Cure Wounds, Guiding Bolt, Lesser Restoration, Light, Sacred Flame.</i>"
			"<br><b>Level 5.</b> <i>Daylight, Revivify.</i><br><b>Level 7.</b> <i>Guardian of Faith, Wall of Fire.</i>"
			"<br><b>Level 9.</b> <i>Greater Restoration, Summon Celestial.</i> These don't count against the number of spells you prepare."
			),
		)

def _healing_light_entry(
		char,
		) -> str:
	pool = _healing_light_dice(char)
	spend = _charisma_modifier(char)

	return (
		"You channel celestial energy to heal wounds, drawing on a pool of <b>"
		f"{pool}d6</b>. As a Bonus Action you can heal yourself or one "
		"creature you can see within 60 feet, expending dice from the "
		"pool and restoring Hit Points equal to the total rolled. "
		f"You can spend at most <b>{spend}</b> dice at once. Your pool "
		"regains all expended dice when you finish a Long Rest."
		)


Healing_Light = _celestial(
		name="Healing Light",
		min_level=3,
		description=_healing_light_entry,
		chips=(
				("Healing Light Dice", _healing_light_dice, "🪶"),
				("Healing Light Spend", _charisma_modifier, "💛"),
				),
		)

def _grant_radiant_resistance(
		char,
		) -> None:
	Grant_Resistance(
			char,
			"Radiant",
			)


Radiant_Soul = _celestial(
		name="Radiant Soul",
		min_level=6,
		description=(
			"You have Resistance to Radiant damage. Once per turn, when a "
			"spell you cast deals Radiant or Fire damage, you can add your "
			"Charisma modifier to that spell's damage against one of the "
			"spell's targets."
			),
		apply=_grant_radiant_resistance,
		)

Celestial_Resilience = _celestial(
		name="Celestial Resilience",
		min_level=10,
		description=(
			"When you use Magical Cunning or finish a Short or Long Rest, "
			"you gain Temporary Hit Points equal to your Warlock level "
			"plus your Charisma modifier. Choose up to five creatures you "
			"can see — each gains Temporary Hit Points equal to half "
			"that amount."
			),
		)

Searing_Vengeance = _celestial(
		name="Searing Vengeance",
		min_level=14,
		description=(
			"When you or an ally within 60 feet of you is about to make a "
			"Death Saving Throw, you can unleash radiant energy to save "
			"the creature. The creature regains Hit Points equal to half "
			"its Hit Point maximum and can end the Prone condition on "
			"itself. Each creature of your choice that is within 30 feet "
			"of the creature takes Radiant damage equal to 2d8 plus your "
			"Charisma modifier, and each has the Blinded condition until "
			"the end of the current turn. Once you use this feature, you "
			"can't use it again until you finish a Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# The Fiend Patron
# ---------------------------------------------------------------------------


def _fiend(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _patron(
			FIEND,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _dark_ones_blessing_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	gained = max(
			1,
			level + _charisma_modifier(char),
			)

	return (
		"When you reduce an enemy to 0 Hit Points, you gain <b>"
		f"{gained} Temporary Hit Points</b>. You also gain this benefit "
		"if someone else reduces an enemy within 10 feet of you to 0 "
		"Hit Points."
		)


Dark_Ones_Blessing = _fiend(
		name="Dark One's Blessing",
		min_level=3,
		description=_dark_ones_blessing_entry,
		)

Fiend_Spells = _fiend(
		name="Fiend Spells",
		min_level=3,
		description=(
			"The magic of your patron ensures you always have certain spells prepared. <b>Level 3.</b> <i>Burning Hands, Command, Scorching Ray, Suggestion.</i>"
			"<br><b>Level 5.</b> <i>Fireball, Stinking Cloud.</i><br><b>Level 7.</b> <i>Fire Shield, Wall of Fire.</i>"
			"<br><b>Level 9.</b> <i>Geas, Insect Plague.</i> These don't count against the number of spells you prepare."
			),
		)

def _dark_ones_own_luck_entry(
		char,
		) -> str:
	uses = max(
			1,
			_charisma_modifier(char),
			)

	return (
		"You can call on your fiendish patron to alter fate in your "
		"favour. When you make an ability check or a saving throw, you "
		"can use this feature to add 1d10 to your roll. You can do so "
		"after seeing the roll but before any of its effects occur. "
		f"You have <b>{uses}</b> use{'' if uses == 1 else 's'}, no more "
		"than one per roll, and you regain all expended uses when you "
		"finish a Long Rest."
		)


Dark_Ones_Own_Luck = _fiend(
		name="Dark One's Own Luck",
		min_level=6,
		description=_dark_ones_own_luck_entry,
		)

Fiendish_Resilience = _fiend(
		name="Fiendish Resilience",
		min_level=10,
		description=(
			"Choose one damage type, other than Force, whenever you "
			"finish a Short or Long Rest. You have Resistance to that "
			"damage type until you choose a different one with this feature."
			),
		)

Hurl_Through_Hell = _fiend(
		name="Hurl Through Hell",
		min_level=14,
		description=(
			"Once per turn when you hit a creature with an attack roll, "
			"you can try to transport the target instantly through the "
			"Lower Planes. The target must succeed on a Charisma saving "
			"throw against your spell save DC, or it disappears and "
			"hurtles through a nightmare landscape. The target takes 8d10 "
			"Psychic damage if it isn't a Fiend, and it has the "
			"Incapacitated condition until the end of your next turn, "
			"when it returns to the space it previously occupied or the "
			"nearest unoccupied space. Once you use this feature, you "
			"can't use it again until you finish a Long Rest, unless you "
			"expend a Pact Magic spell slot (no action required) to "
			"restore your use of it."
			),
		)


# ---------------------------------------------------------------------------
# The Great Old One Patron
# ---------------------------------------------------------------------------


def _goo(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _patron(
			GREAT_OLD_ONE,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


def _awakened_mind_entry(
		char,
		) -> str:
	miles = max(
			1,
			_charisma_modifier(char),
			)
	minutes = max(
			1,
			_rank(char),
			)

	return (
		"Your patron left a door open in your mind. As a Bonus Action "
		"you can choose one creature you can see within 30 feet, and "
		"the two of you can speak telepathically while you are within <b>"
		f"{miles} mile{'' if miles == 1 else 's'}</b> of each other. To "
		"understand each other you must each mentally use a language the "
		f"other knows. The connection lasts <b>{minutes} minutes</b>, "
		"and ends early if you use this feature on someone else."
		)


Awakened_Mind = _goo(
		name="Awakened Mind",
		min_level=3,
		description=_awakened_mind_entry,
		)

Great_Old_One_Spells = _goo(
		name="Great Old One Spells",
		min_level=3,
		description=(
			"The magic of your patron ensures you always have certain spells prepared. <b>Level 3.</b> <i>Detect Thoughts, Dissonant Whispers, Phantasmal Force, Tasha's Hideous Laughter.</i>"
			"<br><b>Level 5.</b> <i>Clairvoyance, Hunger of Hadar.</i><br><b>Level 7.</b> <i>Confusion, Summon Aberration.</i>"
			"<br><b>Level 9.</b> <i>Modify Memory, Telekinesis.</i> These don't count against the number of spells you prepare."
			),
		)

Psychic_Spells = _goo(
		name="Psychic Spells",
		min_level=3,
		description=(
			"When you cast a Warlock spell that deals damage, you can "
			"change its damage type to Psychic. When you cast a Warlock "
			"spell that is an Enchantment or an Illusion, you can cast it "
			"without Verbal or Somatic components."
			),
		)

Clairvoyant_Combatant = _goo(
		name="Clairvoyant Combatant",
		min_level=6,
		description=(
			"When you form a telepathic bond with a creature using your "
			"Awakened Mind, you can force that creature to make a Wisdom "
			"saving throw against your spell save DC. On a failed save "
			"the creature has Disadvantage on attack rolls against you, "
			"and you have Advantage on attack rolls against it, for the "
			"duration of the bond. Once you use this feature, you can't "
			"use it again until you finish a Short or Long Rest, unless "
			"you expend a Pact Magic spell slot (no action required) to "
			"restore your use of it."
			),
		)

Eldritch_Hex = _goo(
		name="Eldritch Hex",
		min_level=10,
		description=(
			"Your alien patron granted you a powerful curse. You always "
			"have the <i>Hex</i> spell prepared. When you cast <i>Hex</i> "
			"and choose an ability, the target also has Disadvantage on "
			"saving throws of the chosen ability for the spell's duration."
			),
		)

def _grant_psychic_resistance(
		char,
		) -> None:
	Grant_Resistance(
			char,
			"Psychic",
			)


Thought_Shield = _goo(
		name="Thought Shield",
		min_level=10,
		description=(
			"Your thoughts can't be read by telepathy or other means unless "
			"you allow it. You have Resistance to Psychic damage. Whenever "
			"a creature deals Psychic damage to you, that creature takes "
			"the same amount of Psychic damage."
			),
		apply=_grant_psychic_resistance,
		)

def _create_thrall_entry(
		char,
		) -> str:
	temporary = max(
			1,
			_rank(char) + _charisma_modifier(char),
			)

	return (
		"When you cast <i>Summon Aberration</i>, you can modify it so "
		"that it does not require Concentration. If you do, the spell's "
		"duration becomes 1 minute for that casting, and the Aberration "
		f"arrives with <b>{temporary} Temporary Hit Points</b>. In "
		"addition, the first time each turn the Aberration hits a "
		"creature under the effect of your <i>Hex</i>, it deals extra "
		"Psychic damage to that target equal to the bonus damage of "
		"that spell."
		)


Create_Thrall = _goo(
		name="Create Thrall",
		min_level=14,
		description=_create_thrall_entry,
		)
