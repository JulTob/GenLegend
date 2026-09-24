"""
Sorcerer Training Tags — 2024 PHB core + all Origins.

Thought pattern
        1. Core lessons belong to the Sorcerer Guild (no Origin).
        2. Origin lessons set path=… and awaken only for that Origin.
        3. Sorcery Point counts live as Chips and callables.
        4. ASI / Epic Boon stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training


GUILD = "Sorcerer"
CORE_SOURCE = "Training: Sorcerer"
ABERRANT = "Aberrant Sorcery"
CLOCKWORK = "Clockwork Sorcery"
DRACONIC = "Draconic Sorcery"
WILD_MAGIC = "Wild Magic Sorcery"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _sorcery_points(
		char,
		) -> int:
	return _rank(
			char
			)


def _metamagic_count(
		char,
		) -> int:
	level = _rank(
			char
			)
	count = 2
	if level >= 10:
		count += 2
	if level >= 17:
		count += 2
	return count


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


def _origin(
		origin_name: str,
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
			path=origin_name,
			source=f"Training: {origin_name}",
			)


# ---------------------------------------------------------------------------
# Callable entries (level-sensitive text)
# ---------------------------------------------------------------------------


def _font_of_magic_entry(
		char,
		) -> str:
	pts = _sorcery_points(
			char
			)
	return (
		f"You have <b>{pts} Sorcery Points</b> (regained on Long "
		"Rest).<br><b>Creating Spell Slots.</b> As a Bonus Action, "
		"spend points to create a slot: 1st 2 pts, 2nd 3 pts, "
		"3rd 5 pts, 4th 6 pts, 5th 7 pts (max 5th level)."
		"<br><b>Converting Spell Slots.</b> As a Bonus Action, "
		"expend a slot to gain Sorcery Points equal to its level."
		)


def _metamagic_entry(
		char,
		) -> str:
	count = _metamagic_count(
			char
			)
	return (
		f"Choose <b>{count}</b> Metamagic options. Spend Sorcery "
		"Points to modify your spells — only one option per spell "
		"unless a feature says otherwise."
		"<br><i>Options (cost in Sorcery Points):</i> "
		"Careful Spell (1), Distant Spell (1), Empowered Spell (1), "
		"Extended Spell (1), Heightened Spell (2), Quickened "
		"Spell (2), Seeking Spell (1), Subtle Spell (1), "
		"Transmuted Spell (1), Twinned Spell (1)."
		)


Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description=(
			"An event in your past left an indelible mark, flooding "
			"you with raw magic. You cast Sorcerer spells using "
			"Charisma as your spellcasting ability. You can use an "
			"Arcane Focus as your Spellcasting Focus."
			),
		)

Innate_Sorcery = _core(
		name="Innate Sorcery",
		min_level=1,
		description=(
			"As a <i>Bonus Action</i>, unleash the sorcerous power "
			"within for 1 minute. While active:"
			"<br>• Your Sorcerer spell save DC increases by 1."
			"<br>• You have <b>Advantage</b> on attack rolls of "
			"Sorcerer spells you cast."
			"<br>Uses: 2 per Long Rest."
			),
		)

Font_of_Magic = _core(
		name="Font of Magic",
		min_level=2,
		description=_font_of_magic_entry,
		chips=(
				("Sorcery Points", _sorcery_points),
				),
		)

Metamagic = _core(
		name="Metamagic",
		min_level=2,
		description=_metamagic_entry,
		chips=(
				("Metamagic Options", _metamagic_count),
				),
		)

Sorcerous_Restoration = _core(
		name="Sorcerous Restoration",
		min_level=5,
		description=(
			"When you finish a Short Rest, regain Sorcery Points equal "
			"to half your Sorcerer level (round down). Uses: 1 per Long Rest."
			),
		)

Sorcery_Incarnate = _core(
		name="Sorcery Incarnate",
		min_level=7,
		description=(
			"If you have no uses of Innate Sorcery remaining, you can "
			"activate it by spending <b>2 Sorcery Points</b>. While "
			"Innate Sorcery is active, you can apply <b>two</b> "
			"Metamagic options to each spell you cast."
			),
		)

Arcane_Apotheosis = _core(
		name="Arcane Apotheosis",
		min_level=20,
		description=(
			"While Innate Sorcery is active, you can apply one Metamagic "
			"option per turn <b>without spending Sorcery Points</b>."
			),
		)


# ---------------------------------------------------------------------------
# Aberrant Sorcery
# ---------------------------------------------------------------------------


def _aberrant(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _origin(
			ABERRANT,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Psionic_Spells = _aberrant(
		name="Psionic Spells",
		min_level=3,
		description=(
			"Your aberrant nature grants extra spells always prepared: "
			"<i>Arms of Hadar, Dissonant Whispers, Calm Emotions, "
			"Detect Thoughts, Hunger of Hadar, Sending, Evard's Black "
			"Tentacles, Summon Aberration.</i> These don't count "
			"against your prepared spells."
			),
		)

Telepathic_Speech = _aberrant(
		name="Telepathic Speech",
		min_level=3,
		description=(
			"You can form a telepathic connection to one creature you "
			"can see within 30 feet. For a number of minutes equal to "
			"your Sorcerer level, you and the creature can speak "
			"telepathically while within 1 mile of each other. Both must "
			"know at least one language, though speech need not be vocalized."
			),
		)

Psionic_Sorcery = _aberrant(
		name="Psionic Sorcery",
		min_level=6,
		description=(
			"When you cast a spell from your Psionic Spells list, you "
			"can cast it by expending a spell slot as normal <b>or</b> "
			"by spending Sorcery Points equal to the spell's level. "
			"If cast using Sorcery Points, it requires no Verbal or "
			"Somatic components."
			),
		)

Psychic_Defenses = _aberrant(
		name="Psychic Defenses",
		min_level=6,
		description=(
			"You gain Resistance to Psychic damage, and you have Advantage "
			"on saving throws against the Charmed and Frightened conditions."
			),
		)

Revelation_in_Flesh = _aberrant(
		name="Revelation in Flesh",
		min_level=14,
		description=(
			"As a Bonus Action, spend 1–4 Sorcery Points to alter your "
			"body for 10 minutes. For each point spent, choose one effect:"
			"<br>• See any invisible creature within 60 feet."
			"<br>• Swim Speed equal to your Speed; breathe underwater."
			"<br>• Fly Speed equal to your Speed; you can hover."
			"<br>• Move through spaces at least 1 inch wide without "
			"squeezing."
			),
		)

Warping_Implosion = _aberrant(
		name="Warping Implosion",
		min_level=18,
		description=(
			"As an action, teleport up to 120 feet to an unoccupied "
			"space you can see. Each creature within 30 feet of the "
			"space you left makes a Strength saving throw — on a fail "
			"it takes 3d10 Force damage and is pulled to the nearest "
			"unoccupied space near your destination; on a success it "
			"takes half damage and isn't pulled. <br>Once you use this "
			"feature, you can't do so again until you finish a Long "
			"Rest, unless you spend 5 Sorcery Points to use it again."
			),
		)


# ---------------------------------------------------------------------------
# Clockwork Sorcery
# ---------------------------------------------------------------------------


def _clockwork(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _origin(
			CLOCKWORK,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Clockwork_Spells = _clockwork(
		name="Clockwork Spells",
		min_level=3,
		description=(
			"The magic of cosmic order grants extra spells always "
			"prepared: <i>Alarm, Protection from Evil and Good, Aid, "
			"Lesser Restoration, Dispel Magic, Protection from Energy, "
			"Freedom of Movement, Summon Construct.</i> These don't "
			"count against your prepared spells."
			),
		)

Restore_Balance = _clockwork(
		name="Restore Balance",
		min_level=3,
		description=(
			"As a Reaction when a creature you can see within 60 feet "
			"is about to roll with Advantage or Disadvantage, you can "
			"cancel the Advantage or Disadvantage. Uses equal your "
			"Charisma modifier (minimum 1); regained on a Long Rest."
			),
		)

Bastion_of_Law = _clockwork(
		name="Bastion of Law",
		min_level=6,
		description=(
			"As a Magic action, spend 1–5 Sorcery Points to create a "
			"ward on a creature you can see within 30 feet. The ward "
			"has Hit Points equal to <b>5 × Sorcery Points spent</b>. "
			"The next time the warded creature takes damage, reduce "
			"that damage by the ward's HP pool. The ward lasts until "
			"depleted or until you finish a Long Rest."
			),
		)

Trance_of_Order = _clockwork(
		name="Trance of Order",
		min_level=14,
		description=(
			"As a Bonus Action, enter a state of perfect order for 1 "
			"minute. While active, attack rolls against you can't "
			"benefit from Advantage, and whenever you make an attack "
			"roll, ability check, or saving throw, you can treat a "
			"roll of 9 or lower as a 10. <br>Once you use this "
			"feature, you can't do so again until you finish a Long "
			"Rest, unless you spend 5 Sorcery Points to use it again."
			),
		)

Clockwork_Cavalcade = _clockwork(
		name="Clockwork Cavalcade",
		min_level=18,
		description=(
			"As an action, spirits of order sweep a 30-foot Cube from "
			"you: each damaged creature regains 3d10 HP; conditions "
			"grappling, restraining, or paralyzing chosen creatures "
			"end; and damaged objects are repaired."
			"<br>Once you use this feature, you can't do so again "
			"until you finish a Long Rest, unless you spend 7 Sorcery "
			"Points."
			),
		)


# ---------------------------------------------------------------------------
# Draconic Sorcery
# ---------------------------------------------------------------------------


def _draconic(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _origin(
			DRACONIC,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _draconic_resilience_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	return (
		"<b>Draconic Resilience.</b> Your hit point maximum increases by <b>"
		f"{level}</b> (1 per Sorcerer level). When you aren't wearing "
		"armor, your AC equals 13 + your Dexterity modifier."
		)


Draconic_Resilience = _draconic(
		name="Draconic Resilience",
		min_level=3,
		description=_draconic_resilience_entry,
		chips=(
				("HP Bonus", _rank),
				),
		)

Draconic_Spells = _draconic(
		name="Draconic Spells",
		min_level=3,
		description=(
			"Your draconic lineage grants extra spells always prepared: "
			"<i>Chromatic Orb, Dragon's Breath, Fly, Fear, Dominate "
			"Beast, Summon Draconic Spirit.</i> These don't count "
			"against your prepared spells."
			),
		)

Elemental_Affinity = _draconic(
		name="Elemental Affinity",
		min_level=6,
		description=(
			"When you cast a spell that deals the damage type of your "
			"draconic ancestry, add your Charisma modifier to one "
			"damage roll. You can also spend 1 Sorcery Point to gain "
			"Resistance to that damage type for 1 hour."
			),
		)

Dragon_Wings = _draconic(
		name="Dragon Wings",
		min_level=14,
		description=(
			"As a Bonus Action, sprout draconic wings. You gain a Fly "
			"Speed equal to your Speed. The wings last until you "
			"dismiss them (no action required). You can't manifest them "
			"while wearing armor unless it's designed to accommodate them."
			),
		)

Dragon_Companion = _draconic(
		name="Dragon Companion",
		min_level=18,
		description=(
			"As an action, summon a Young Dragon of your draconic "
			"lineage in an unoccupied space within 30 feet. It acts on "
			"your initiative, follows your commands, and stays until "
			"it drops to 0 HP, you dismiss it, or you finish a Long "
			"Rest. Once used, <br>Once you use this feature, you can't "
			"do so again until you finish a Long Rest, unless you "
			"spend 7 Sorcery Points to use it again."
			),
		)


# ---------------------------------------------------------------------------
# Wild Magic Sorcery
# ---------------------------------------------------------------------------


def _wild_magic(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _origin(
			WILD_MAGIC,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Wild_Magic_Surge = _wild_magic(
		name="Wild Magic Surge",
		min_level=3,
		description=(
			"Your spellcasting can unleash surges of wild magic. "
			"Immediately after you cast a Sorcerer spell of level 1 or "
			"higher, the DM can have you roll a d20. On a 1, a Wild "
			"Magic Surge occurs — roll on the Wild Magic Surge table."
			),
		)

Tides_of_Chaos = _wild_magic(
		name="Tides of Chaos",
		min_level=3,
		description=(
			"Before you make an attack roll, ability check, or saving "
			"throw, you can gain Advantage on that roll. Once you do so, "
			"a Wild Magic Surge immediately occurs before you regain the "
			"use of this feature. Uses: 1 per Long Rest (or regain after a Surge)."
			),
		)

Bend_Luck = _wild_magic(
		name="Bend Luck",
		min_level=6,
		description=(
			"As a Reaction when another creature you can see makes an "
			"attack roll, ability check, or saving throw, you can spend "
			"2 Sorcery Points and roll 1d4. Add or subtract the result "
			"from the creature's roll (your choice)."
			),
		)

Controlled_Chaos = _wild_magic(
		name="Controlled Chaos",
		min_level=14,
		description=(
			"Whenever you roll on the Wild Magic Surge table, you can "
			"roll twice and use either result."
			),
		)

Tamed_Surge = _wild_magic(
		name="Tamed Surge",
		min_level=18,
		description=(
			"When you cast a Sorcerer spell of level 1 or higher, you "
			"can choose to cause a Wild Magic Surge. Once per turn when "
			"a Surge occurs, you can choose the result on the table "
			"rather than roll randomly."
			),
		)
