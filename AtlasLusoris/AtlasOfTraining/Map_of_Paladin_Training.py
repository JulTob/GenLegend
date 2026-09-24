"""
Paladin Training Tags — 2024 PHB core + all Oaths.

Thought pattern
	1. Core lessons belong to the Paladin Guild (no Oath).
	2. Oath lessons set ``path=…`` and awaken only for that Oath.
	3. Lay on Hands pool and Channel Divinity uses live as Chips and
	   in callable Entries — not as separate Tag members.
	4. ASI / Epic Boon / Fighting Style picks stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training


GUILD = "Paladin"
CORE_SOURCE = "Training: Paladin"
ANCIENTS = "Ancients"
DEVOTION = "Devotion"
GLORY = "Glory"
VENGEANCE = "Vengeance"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _lay_pool(
		char,
		) -> int:
	return 5 * max(
			1,
			_rank(
					char
					),
			)


def _channel_uses(
		char,
		) -> int:
	return 3 if _rank(char) >= 11 else 2


def _aura_range(
		char,
		) -> int:
	return 30 if _rank(char) >= 18 else 10


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
			source=f"Training: Oath of {path_name}",
			)


def _ancients(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			ANCIENTS,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _devotion(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			DEVOTION,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _glory(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			GLORY,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _vengeance(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _path(
			VENGEANCE,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


# ---------------------------------------------------------------------------
# Callable entries (level-sensitive text)
# ---------------------------------------------------------------------------


def _lay_entry(
		char,
		) -> str:
	pool = _lay_pool(
			char
			)
	return (
		"You have a pool of healing power that replenishes when you finish "
		"a Long Rest. With that pool, you can restore a total of "
		f"<b>{pool}</b> Hit Points. "
		"<br><b>Bonus Action:</b> touch a creature (which could be yourself) "
		"and draw power from the pool to restore Hit Points, up to the maximum "
		"remaining. "
		"<br>You can also expend 5 Hit Points from the pool to remove the "
		"<em>Poisoned</em> condition from the creature; those points don't also "
		"restore Hit Points."
		)


def _channel_entry(
		char,
		) -> str:
	uses = _channel_uses(
			char
			)
	return (
		"You can channel divine energy to fuel magical effects. "
		f"You can use Channel Divinity <b>{uses} times</b>. "
		"You regain one expended use when you finish a Short Rest, and you "
		"regain all expended uses when you finish a Long Rest. "
		"<br>If a Channel Divinity effect requires a saving throw, the DC equals "
		"your Paladin spell save DC."
		)


def _aura_protection_entry(
		char,
		) -> str:
	r = _aura_range(
			char
			)
	return (
		f"You and friendly creatures within <b>{r} feet</b> of you gain a bonus "
		"to all saving throws equal to your Charisma modifier (minimum +1). "
		"This aura is inactive while you have the Incapacitated condition. "
		"<br>If multiple Paladin auras overlap, a creature chooses which "
		"Aura of Protection to benefit from."
		)


def _aura_courage_entry(
		char,
		) -> str:
	r = _aura_range(
			char
			)
	return (
		f"You and friendly creatures within <b>{r} feet</b> of you can't be "
		"<em>Frightened</em> while you are conscious."
		)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Lay_on_Hands = _core(
		name="Lay on Hands",
		min_level=1,
		description=_lay_entry,
		chips=(
				("Lay on Hands HP", _lay_pool),
				),
		)

Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description=(
			"You cast Paladin spells through prayer and devotion. "
			"<b>Charisma</b> is your spellcasting ability. "
			"You prepare a list of Paladin spells chosen from the Paladin spell list. "
			"You can change your list of prepared spells when you finish a Long Rest."
			),
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
				("Weapon Masteries", _weapon_mastery_chip),
				),
		)

Fighting_Style = _core(
		name="Fighting Style",
		min_level=2,
		description=(
			"You adopt a particular style of fighting. Choose a Fighting Style "
			"option from the Paladin list (such as Defense, Dueling, "
			"Great Weapon Fighting, or Protection)."
			),
		)

Paladins_Smite = _core(
		name="Paladin's Smite",
		min_level=2,
		description=(
			"You always have the <em>Divine Smite</em> spell prepared. "
			"When you hit a target with a melee weapon or Unarmed Strike, "
			"you can expend a Paladin spell slot to cast <em>Divine Smite</em> "
			"as part of that attack (no action required)."
			),
		)

Channel_Divinity = _core(
		name="Channel Divinity",
		min_level=3,
		description=_channel_entry,
		chips=(
				("Channel Divinity Uses", _channel_uses),
				),
		)

Extra_Attack = _core(
		name="Extra Attack",
		min_level=5,
		description=(
			"You can attack twice instead of once whenever you take the "
			"Attack action on your turn."
			),
		)

Faithful_Steed = _core(
		name="Faithful Steed",
		min_level=5,
		description=(
			"You always have the <em>Find Steed</em> spell prepared. "
			"You can cast it once without expending a spell slot, and you regain "
			"the ability to do so when you finish a Long Rest. "
			"<br>The steed is Celestial, Fey, or Fiendish (your choice), obeys your "
			"commands, understands one language you speak, and vanishes at 0 Hit Points. "
			"While it is within 1 mile you can communicate telepathically, and any spell "
			"you cast that targets only you can also target the steed."
			),
		)

Aura_of_Protection = _core(
		name="Aura of Protection",
		min_level=6,
		description=_aura_protection_entry,
		chips=(
				("Aura Range (ft)", _aura_range),
				),
		)

Abjure_Foes = _core(
		name="Abjure Foes",
		min_level=9,
		description=(
			"<b>Channel Divinity — Magic action.</b> "
			"Choose creatures you can see within 60 feet. "
			"Each target must succeed on a Wisdom saving throw against your Paladin "
			"spell save DC or have the <em>Frightened</em> condition for 1 minute. "
			"<br>While frightened this way, a creature can do only one of the following "
			"on its turn: move, take an action, or take a Bonus Action. "
			"<br>Frightened creatures repeat the save at the end of each of their turns, "
			"ending the effect on a success."
			),
		)

Aura_of_Courage = _core(
		name="Aura of Courage",
		min_level=10,
		description=_aura_courage_entry,
		# No Aura Range chip: Aura of Protection already owns that number and
		# its callable covers every tier. Two declarations put the same label
		# on the rail twice.
		)

Radiant_Strikes = _core(
		name="Radiant Strikes",
		min_level=11,
		description=(
			"Whenever you hit a creature with a melee weapon or an Unarmed Strike, "
			"the target takes an extra <b>1d8</b> Radiant damage."
			),
		)

Restoring_Touch = _core(
		name="Restoring Touch",
		min_level=14,
		description=(
			"When you use Lay on Hands on a creature, you can expend 5 Hit Points "
			"from the pool (without restoring HP) to end one of these conditions on it: "
			"<em>Blinded, Charmed, Deafened, Frightened, Paralyzed,</em> or "
			"<em>Stunned</em>. Spend 5 Hit Points for each additional condition removed."
			),
		)

Aura_Expansion = _core(
		name="Aura Expansion",
		min_level=18,
		description=(
			"Your Aura of Protection and Aura of Courage now extend "
			"to <b>30 feet</b>."
			),
		)


# ---------------------------------------------------------------------------
# Oath of the Ancients
# ---------------------------------------------------------------------------


Ancients_Oath_Spells = _ancients(
		name="Oath Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared:"
			"<ul>"
			"<li><b>3rd:</b> <em>Ensnaring Strike, Speak with Animals</em></li>"
			"<li><b>5th:</b> <em>Misty Step, Moonbeam</em></li>"
			"<li><b>9th:</b> <em>Plant Growth, Protection from Energy</em></li>"
			"<li><b>13th:</b> <em>Ice Storm, Stoneskin</em></li>"
			"<li><b>17th:</b> <em>Commune with Nature, Tree Stride</em></li>"
			"</ul>"
			),
		)

Natures_Wrath = _ancients(
		name="Nature's Wrath",
		min_level=3,
		description=(
			"<b>Channel Divinity — Action.</b> "
			"You call on the powers of nature to restrain a creature you can see "
			"within 10 feet. The target must succeed on a Strength or Dexterity "
			"saving throw (its choice) against your spell save DC or have the "
			"<em>Restrained</em> condition until you use this feature again or until "
			"the target succeeds on the save repeated at the end of each of its turns."
			),
		)

Aura_of_Warding = _ancients(
		name="Aura of Warding",
		min_level=7,
		description=(
			"Ancient magic lies so heavily upon you that it forms an aura. "
			"You and friendly creatures within the range of your Aura of Protection "
			"have Resistance to damage from spells."
			),
		)

Undying_Sentinel = _ancients(
		name="Undying Sentinel",
		min_level=15,
		description=(
			"When you are reduced to 0 Hit Points and not killed outright, you can "
			"choose to drop to 1 Hit Point instead. Once you use this feature, you "
			"can't do so again until you finish a Long Rest. "
			"<br>Additionally, you suffer none of the drawbacks of old age, and you "
			"can't be aged magically."
			),
		)

Elder_Champion = _ancients(
		name="Elder Champion",
		min_level=20,
		description=(
			"As a Bonus Action, you can assume the form of an ancient force of nature "
			"for 1 minute or until you end it (no action required). "
			"<br>While transformed:"
			"<ul>"
			"<li><b>Regeneration.</b> At the start of each of your turns, you regain "
			"10 Hit Points.</li>"
			"<li><b>Extended Auras.</b> Beasts and Plants have Disadvantage on attack "
			"rolls against you.</li>"
			"<li><b>Bonus Spell.</b> When you cast a Paladin spell with a casting time "
			"of an action, you can cast it using a Bonus Action instead.</li>"
			"</ul>"
			"Once you use this feature, you can't use it again until you finish a "
			"Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Oath of Devotion
# ---------------------------------------------------------------------------


Devotion_Oath_Spells = _devotion(
		name="Oath Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared:"
			"<ul>"
			"<li><b>3rd:</b> <em>Protection from Evil and Good, Shield of Faith</em></li>"
			"<li><b>5th:</b> <em>Aid, Zone of Truth</em></li>"
			"<li><b>9th:</b> <em>Beacon of Hope, Dispel Magic</em></li>"
			"<li><b>13th:</b> <em>Freedom of Movement, Guardian of Faith</em></li>"
			"<li><b>17th:</b> <em>Commune, Flame Strike</em></li>"
			"</ul>"
			),
		)

Sacred_Weapon = _devotion(
		name="Sacred Weapon",
		min_level=3,
		description=(
			"<b>Channel Divinity — Bonus Action.</b> "
			"You imbue a weapon you are holding with positive energy. "
			"For 1 minute, you add your Charisma modifier to attack rolls made "
			"with that weapon (minimum bonus of +1), and the weapon emits bright light "
			"in a 20-foot radius and dim light 20 feet beyond that. "
			"<br>If the weapon isn't already magical, it becomes magical for the duration. "
			"The effect ends early if you aren't holding or carrying the weapon."
			),
		)

Aura_of_Devotion = _devotion(
		name="Aura of Devotion",
		min_level=7,
		description=(
			"You and friendly creatures within the range of your Aura of Protection "
			"can't be <em>Charmed</em> while you are conscious."
			),
		)

Smite_of_Protection = _devotion(
		name="Smite of Protection",
		min_level=15,
		description=(
			"Your magical smites now shield their targets with holy power. "
			"Whenever you cast Divine Smite, the creature you hit gains a +2 bonus "
			"to AC until the start of your next turn."
			),
		)

Holy_Nimbus = _devotion(
		name="Holy Nimbus",
		min_level=20,
		description=(
			"As a Bonus Action, you can emanate an aura of sunlight for 1 minute. "
			"For the duration, bright light fills a 30-foot Emanation originating from you. "
			"<br>Whenever an enemy starts its turn in the bright light, it takes "
			"<b>10 Radiant</b> damage. "
			"<br>In addition, for the duration, you have Advantage on saving throws "
			"against spells cast by Fiends or Undead. "
			"<br>Once you use this feature, you can't use it again until you finish "
			"a Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Oath of Glory
# ---------------------------------------------------------------------------


Glory_Oath_Spells = _glory(
		name="Oath Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared:"
			"<ul>"
			"<li><b>3rd:</b> <em>Guiding Bolt, Heroism</em></li>"
			"<li><b>5th:</b> <em>Enhance Ability, Magic Weapon</em></li>"
			"<li><b>9th:</b> <em>Aura of Vitality, Protection from Energy</em></li>"
			"<li><b>13th:</b> <em>Compulsion, Freedom of Movement</em></li>"
			"<li><b>17th:</b> <em>Legend Lore, Yolande's Regal Presence</em></li>"
			"</ul>"
			),
		)

Inspiring_Smite = _glory(
		name="Inspiring Smite",
		min_level=3,
		description=(
			"Immediately after you cast Divine Smite, you can use a Channel Divinity "
			"(no action required) and distribute Temporary Hit Points equal to "
			"<b>2d8 + your Paladin level</b> among yourself and any creatures of your "
			"choice within 30 feet of you."
			),
		)

Peerless_Athlete = _glory(
		name="Peerless Athlete",
		min_level=3,
		description=(
			"<b>Channel Divinity — Bonus Action.</b> "
			"For 10 minutes, whenever you make a Strength (Athletics) or Dexterity "
			"(Acrobatics) check, you treat a roll of 9 or lower on the d20 as a 10. "
			"Also, you can carry, push, drag, or lift twice the normal amount, and "
			"your jump distances are tripled."
			),
		)

Aura_of_Alacrity = _glory(
		name="Aura of Alacrity",
		min_level=7,
		description=(
			"Your Speed increases by 10 feet. "
			"In addition, whenever an ally starts their turn within your Aura of "
			"Protection, their Speed increases by 10 feet until the end of that turn."
			),
		)

Glorious_Defense = _glory(
		name="Glorious Defense",
		min_level=15,
		description=(
			"You can turn another's failure into your own glory. "
			"When you or another creature you can see within 10 feet of you is hit by "
			"an attack roll, you can use your Reaction to add your Charisma modifier "
			"(minimum of +1) to the target's AC against that attack. "
			"If the attack misses, you can make one weapon attack against the attacker "
			"as part of this Reaction, provided the attacker is within your reach. "
			"<br>You can use this feature a number of times equal to your Charisma "
			"modifier (minimum once). You regain all expended uses when you finish "
			"a Long Rest."
			),
		)

Living_Legend = _glory(
		name="Living Legend",
		min_level=20,
		description=(
			"You can empower yourself with the legends — whether true or exaggerated "
			"— of your past deeds. As a Bonus Action, you gain the following benefits "
			"for 1 minute:"
			"<ul>"
			"<li><b>Charismatic.</b> You are blessed with an otherworldly presence, "
			"gaining Advantage on Charisma checks.</li>"
			"<li><b>Saving Throw Reroll.</b> If you fail a saving throw, you can use "
			"your Reaction to reroll it. You must use this new roll.</li>"
			"<li><b>Unerring Strike.</b> Once on each of your turns when you miss with "
			"an attack roll, you can cause that attack to hit instead.</li>"
			"</ul>"
			"Once you use this feature, you can't use it again until you finish a "
			"Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Oath of Vengeance
# ---------------------------------------------------------------------------


Vengeance_Oath_Spells = _vengeance(
		name="Oath Spells",
		min_level=3,
		description=(
			"You always have the following spells prepared:"
			"<ul>"
			"<li><b>3rd:</b> <em>Bane, Hunter's Mark</em></li>"
			"<li><b>5th:</b> <em>Hold Person, Misty Step</em></li>"
			"<li><b>9th:</b> <em>Haste, Protection from Energy</em></li>"
			"<li><b>13th:</b> <em>Banishment, Dimension Door</em></li>"
			"<li><b>17th:</b> <em>Hold Monster, Scrying</em></li>"
			"</ul>"
			),
		)

Vow_of_Enmity = _vengeance(
		name="Vow of Enmity",
		min_level=3,
		description=(
			"<b>Channel Divinity — Bonus Action.</b> "
			"You utter a vow of enmity against a creature you can see within 30 feet. "
			"You gain Advantage on attack rolls against the creature for 1 minute or "
			"until it drops to 0 Hit Points or falls Unconscious. "
			"<br>If the creature drops to 0 Hit Points before the minute ends, you "
			"can transfer the vow to a different creature (no action required)."
			),
		)

Relentless_Avenger = _vengeance(
		name="Relentless Avenger",
		min_level=7,
		description=(
			"Your supernatural focus helps you close off a foe's retreat. "
			"When you hit a creature with an Opportunity Attack, you can reduce the "
			"creature's Speed to 0 until the end of the current turn, and you can "
			"then move up to half your Speed as part of the same Reaction. "
			"This movement doesn't provoke Opportunity Attacks."
			),
		)

Soul_of_Vengeance = _vengeance(
		name="Soul of Vengeance",
		min_level=15,
		description=(
			"The authority with which you speak your Vow of Enmity gives you "
			"enhanced power. When a creature under the effect of your Vow of Enmity "
			"makes an attack, you can use your Reaction to make a melee weapon attack "
			"against that creature if it is within reach."
			),
		)

Avenging_Angel = _vengeance(
		name="Avenging Angel",
		min_level=20,
		description=(
			"You can assume the form of an angelic avenger. As a Bonus Action, "
			"you sprout wings and gain the following benefits for 1 hour:"
			"<ul>"
			"<li><b>Flight.</b> Fly Speed equal to your Speed.</li>"
			"<li><b>Frightening Aura.</b> Whenever an enemy starts its turn in a "
			"30-foot Emanation originating from you, it must make a Wisdom saving "
			"throw against your spell save DC. On a failed save, the target has the "
			"<em>Frightened</em> condition for 1 minute. On a successful save, the "
			"target is immune to this aura for 24 hours.</li>"
			"</ul>"
			"Once you use this feature, you can't use it again until you finish "
			"a Long Rest."
			),
		)
