"""
Sorcerer Training Tags — 2024 PHB core + all four Sorcerous Origins.

Thought pattern
	1. Core lessons belong to the Sorcerer Guild (no Origin).
	2. Origin lessons point at their Origin's Shape (``path=`` the Tag, not
	   a name) and awaken only when the Character carries that Shape.
	3. Every number an entry quotes is read from SorcererKit's Reports at
	   sheet-read time, so an entry and the kit cannot disagree.
	4. Every pick was made before the page existed and the entry names it:
	   the Metamagic options, the Elemental Affinity, the Manifestation of
	   Order.  Only choices re-made at the table each time stay open.
	5. A lesson that says it grants something grants it: Resistance,
	   Hit Points, the unarmored Armor Class.
	6. ASI / Epic Boon stay on legacy Progression.

The lessons carry rules only for now.  Their lines, the italic sentence the
Bard and the Fighter print above each rule, wait for the Sorcerer's fantasy
to be settled with Julio.
"""

from __future__ import annotations

from AtlasLusoris.AtlasOfGuilds.SorcererKit import (
	AberrantSorcery,
	ClockworkSorcery,
	DraconicSorcery,
	WildMagicSorcery,
	Find_Always_Prepared,
	Find_Creatable_Slots,
	Find_Innate_Sorcery_Uses,
	Find_Sorcery_Points,
	Resolve_Elemental_Affinity,
	Resolve_Manifestation_Of_Order,
	)
from AtlasLusoris.FeaturesKit import Grant_Resistance
from AtlasLusoris.MetamagicKit import (
	Describe_Metamagic,
	Find_Metamagic,
	)
from AtlasLusoris.TrainingKit import Build_Training
from AtlasVenustas import Chip


GUILD = "Sorcerer"
CORE_SOURCE = "Training: Sorcerer"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _core(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return Build_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			source=CORE_SOURCE,
			)


def _origin(
		origin,
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return Build_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			path=origin,
			source=f"Training: {origin.NAME}",
			)


# ---------------------------------------------------------------------------
# What the sheet already knows
# ---------------------------------------------------------------------------


def _ability_modifier(
		char,
		ability: str,
		) -> int:
	from AtlasActorLudi.Map_of_Scores import Modifier
	scores = getattr(
			char,
			"AS",
			None,
			)
	return Modifier(
			getattr(
					scores,
					ability,
					10,
					)
			)


def _charisma_count(
		char,
		) -> int:
	"""The Charisma modifier as a count of uses: never below one."""
	return max(
			1,
			_ability_modifier(
					char,
					"CHA",
					),
			)


def _spell_save_dc(
		char,
		) -> int:
	"""8 + Proficiency Bonus + Charisma modifier."""
	proficiency = int(
			getattr(
					char,
					"proficiency_bonus",
					2,
					) or 2
			)
	return (
			8
			+ proficiency
			+ _ability_modifier(
					char,
					"CHA",
					)
			)


def _signed(
		value: int,
		) -> str:
	"""A modifier as the sheet prints one: +3, -1, +0."""
	return f"{value:+d}"


def _times(
		count: int,
		) -> str:
	if count == 1:
		return "once"
	if count == 2:
		return "twice"
	return f"{count} times"


def _Named(
		names,
		) -> str:
	"""Join names the way a sentence would: a, b and c."""
	names = list(
			names
			)
	if not names:
		return ""
	if len(
			names
			) == 1:
		return names[0]
	return (
		", ".join(
				names[:-1]
				)
		+ " and "
		+ names[-1]
		)


def _restored_by(
		points: int,
		) -> str:
	"""The closing sentence every once-per-rest Origin feature shares."""
	return (
		"<br>Once you use this feature, you can't use it again until you "
		"finish a Long Rest, unless you spend "
		f"<b>{points} Sorcery Points</b> (no action required) to restore it."
		)


# ---------------------------------------------------------------------------
# Callable entries
# ---------------------------------------------------------------------------


def _innate_sorcery_entry(
		char,
		) -> str:
	raised = _spell_save_dc(
			char
			) + 1
	uses = Find_Innate_Sorcery_Uses(
			char
			)
	return (
		"<b>Bonus Action:</b> unleash the magic within you for 1 minute. "
		"While it lasts:<ul>"
		"<li>The spell save DC of your Sorcerer spells rises by 1, to "
		f"<b>{raised}</b>.</li>"
		"<li>You have Advantage on the attack rolls of Sorcerer spells you "
		"cast.</li>"
		"</ul>"
		f"You can do this <b>{_times(uses)}</b>, and regain every use when "
		"you finish a Long Rest."
		)


def _font_of_magic_entry(
		char,
		) -> str:
	points = Find_Sorcery_Points(
			char
			)
	costs = "".join(
			f"<li>A level {row.slot_level} spell slot costs "
			f"<b>{row.cost} Sorcery Points</b>.</li>"
			for row in Find_Creatable_Slots(
					char
					)
			)
	return (
		f"You have <b>{points} Sorcery Points</b>, and regain them all when "
		"you finish a Long Rest."
		"<br><b>Converting Spell Slots.</b> You can expend a spell slot to "
		"gain Sorcery Points equal to its level (no action required)."
		"<br><b>Creating Spell Slots.</b> As a Bonus Action, you can turn "
		"Sorcery Points into one spell slot:"
		f"<ul>{costs}</ul>"
		"A slot you create vanishes when you finish a Long Rest."
		)


def _metamagic_entry(
		char,
		) -> str:
	known = Find_Metamagic(
			char
			)
	opening = (
		"When you cast a spell, you can spend Sorcery Points to reshape it "
		"with one of your Metamagic options. Unless an option says "
		"otherwise, a spell takes one option at a time."
		)
	if not known:
		# Only a Sorcerer built without an Origin's ``after`` rite lands
		# here; the Player generator always runs it.
		return opening
	options = "".join(
			"<li>"
			+ Describe_Metamagic(
					option,
					char,
					)
			+ "</li>"
			for option in known
			)
	return f"{opening}<ul>{options}</ul>"


def _sorcerous_restoration_entry(
		char,
		) -> str:
	half = _rank(
			char
			) // 2
	return (
		"When you finish a Short Rest, you can regain expended Sorcery "
		f"Points, up to <b>{half}</b> (half your Sorcerer level). Once you "
		"do, you can't again until you finish a Long Rest."
		)


def _always_prepared_entry(
		char,
		) -> str:
	"""Name every Origin spell this Sorcerer keeps prepared at their level."""
	spells = Find_Always_Prepared(
			char
			)
	names = _Named(
			f"<i>{spell.name}</i>"
			for spell in spells
			)
	return (
		f"You always have {names} prepared. They never count against the "
		"number of spells you prepare."
		)


def _clockwork_spells_entry(
		char,
		) -> str:
	manifestation = getattr(
			char,
			"manifestation_of_order",
			None,
			)
	shown = (
		"<br><b>Manifestation of Order.</b> While you cast your Sorcerer "
		f"spells, {manifestation}"
		if manifestation
		else ""
		)
	return _always_prepared_entry(
			char
			) + shown


def _telepathic_speech_entry(
		char,
		) -> str:
	miles = _charisma_count(
			char
			)
	minutes = _rank(
			char
			)
	distance = (
		"1 mile"
		if miles == 1
		else f"{miles} miles"
		)
	return (
		"<b>Bonus Action:</b> choose one creature you can see within 30 feet. "
		"You and that creature can speak telepathically with each other while "
		f"you are within <b>{distance}</b> of each other (your Charisma "
		"modifier). Each of you must use a language the other knows. The link "
		f"lasts <b>{minutes} minutes</b> (your Sorcerer level), and ends "
		"early if you open one with a different creature."
		)


def _revelation_in_flesh_entry(
		char,
		) -> str:
	speed = int(
			getattr(
					char,
					"speed",
					30,
					) or 30
			)
	return (
		"<b>Bonus Action:</b> spend 1 or more Sorcery Points to change your "
		"body for 10 minutes. For each point you spend, choose one of these:"
		"<ul>"
		"<li><b>Aquatic Adaptation.</b> You gain a Swim Speed of "
		f"<b>{speed * 2} feet</b> (twice your Speed), and you can breathe "
		"underwater.</li>"
		"<li><b>Glistening Flight.</b> You gain a Fly Speed of "
		f"<b>{speed} feet</b> (your Speed), and you can hover.</li>"
		"<li><b>See the Invisible.</b> You can see any Invisible creature "
		"within 60 feet of you that isn't behind Total Cover.</li>"
		"<li><b>Wormlike Movement.</b> Your body turns slick and pliable. You "
		"can move through a space as narrow as 1 inch, and you can spend 5 "
		"feet of movement to escape nonmagical restraints or the Grappled "
		"condition.</li>"
		"</ul>"
		)


def _warping_implosion_entry(
		char,
		) -> str:
	dc = _spell_save_dc(
			char
			)
	return (
		"<b>Magic action:</b> teleport to an unoccupied space you can see "
		"within 120 feet. Each creature within 30 feet of the space you left "
		f"makes a <b>DC {dc}</b> Strength saving throw. On a failure it takes "
		"3d10 Force damage and is pulled straight toward the space you left, "
		"ending as close to it as possible. On a success it takes half as "
		"much damage and is not pulled."
		+ _restored_by(
				5
				)
		)


def _restore_balance_entry(
		char,
		) -> str:
	uses = _charisma_count(
			char
			)
	return (
		"<b>Reaction:</b> when a creature you can see within 60 feet is about "
		"to roll a d20 with Advantage or Disadvantage, you cancel both, and "
		"the d20 is rolled plain. You can do this "
		f"<b>{_times(uses)}</b> (your Charisma modifier), and regain every "
		"use when you finish a Long Rest."
		)


def _draconic_armour_class(
		char,
		) -> int:
	return (
			10
			+ _ability_modifier(
					char,
					"DEX",
					)
			+ _ability_modifier(
					char,
					"CHA",
					)
			)


def _draconic_resilience_entry(
		char,
		) -> str:
	hit_points = _rank(
			char
			)
	armour_class = _draconic_armour_class(
			char
			)
	return (
		"Your Hit Point maximum increases by "
		f"<b>{hit_points}</b> (one for each Sorcerer level). While you aren't "
		f"wearing armor, your base Armor Class is <b>{armour_class}</b> "
		"(10 + your Dexterity and Charisma modifiers)."
		)


def _elemental_affinity_entry(
		char,
		) -> str:
	affinity = getattr(
			char,
			"elemental_affinity",
			None,
			)
	bonus = _signed(
			_ability_modifier(
					char,
					"CHA",
					)
			)
	if not affinity:
		# The lesson's ``apply`` draws the element before any sheet reads
		# this; the rule alone is the honest answer if it somehow has not.
		return (
			"Your magic answers to one damage type the dragons breathe: "
			"Acid, Cold, Fire, Lightning or Poison. You have Resistance to "
			"it, and add your Charisma modifier "
			f"(<b>{bonus}</b>) to one damage roll of a spell that deals it."
			)
	return (
		f"Your magic answers to <b>{affinity}</b>. You have Resistance to "
		f"{affinity} damage, and when you cast a spell that deals {affinity} "
		"damage, you add your Charisma modifier "
		f"(<b>{bonus}</b>) to one damage roll of that spell."
		)


# ---------------------------------------------------------------------------
# What the lessons grant
# ---------------------------------------------------------------------------


def _apply_draconic_resilience(
		char,
		) -> None:
	"""
	Grant the Hit Points and the unarmored Armor Class the entry promises.

	Hit Points join ``bonus_health_sources`` by name, the way Dwarven
	Toughness does, so neither can overwrite the other.  One per level is
	exact for a single-class Sorcerer, the only kind the generator builds.

	Armor Class is derived after every lesson, from what is worn, by
	``unarmoured_formula``.  Setting ``char.AC`` here would be overwritten,
	so the lesson grants the training that formula reads instead.
	"""
	sources = dict(
			getattr(
					char,
					"bonus_health_sources",
					{},
					) or {}
			)
	sources[
			"Draconic Resilience"
			] = 1
	char.bonus_health_sources = sources
	char.bonus_health_per_level = sum(
			sources.values()
			)

	skills = getattr(
			char,
			"skills",
			None,
			)
	scales = getattr(
			skills,
			"Unarmed_Draconic",
			None,
			)
	if scales is not None:
		scales.set_proficiency()


def _apply_elemental_affinity(
		char,
		) -> None:
	"""Draw the element, then make its Resistance true on the sheet."""
	affinity = Resolve_Elemental_Affinity(
			char
			)
	Grant_Resistance(
			char,
			affinity,
			)


def _apply_psychic_defenses(
		char,
		) -> None:
	Grant_Resistance(
			char,
			"Psychic",
			)


def _apply_clockwork_spells(
		char,
		) -> None:
	Resolve_Manifestation_Of_Order(
			char
			)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


# The Spells section owns this prose; the Tag still awakens for identity.
Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description="",
		)

Innate_Sorcery = _core(
		name="Innate Sorcery",
		min_level=1,
		description=_innate_sorcery_entry,
		chips=(
				Chip(
						"",
						"Innate Sorcery",
						Find_Innate_Sorcery_Uses,
						),
				),
		)

Font_of_Magic = _core(
		name="Font of Magic",
		min_level=2,
		description=_font_of_magic_entry,
		chips=(
				Chip(
						"",
						"Sorcery Points",
						Find_Sorcery_Points,
						),
				),
		)

Metamagic = _core(
		name="Metamagic",
		min_level=2,
		description=_metamagic_entry,
		)

Sorcerous_Restoration = _core(
		name="Sorcerous Restoration",
		min_level=5,
		description=_sorcerous_restoration_entry,
		)

Sorcery_Incarnate = _core(
		name="Sorcery Incarnate",
		min_level=7,
		description=(
			"If you have no uses of Innate Sorcery left, you can still "
			"unleash it by spending <b>2 Sorcery Points</b> as you take the "
			"Bonus Action. While Innate Sorcery is active, you can use up to "
			"<b>two</b> Metamagic options on each spell you cast."
			),
		)

Arcane_Apotheosis = _core(
		name="Arcane Apotheosis",
		min_level=20,
		description=(
			"While Innate Sorcery is active, you can use one Metamagic option "
			"on each of your turns without spending Sorcery Points on it."
			),
		)


# ---------------------------------------------------------------------------
# Aberrant Sorcery
# ---------------------------------------------------------------------------


Psionic_Spells = _origin(
		AberrantSorcery,
		name="Psionic Spells",
		min_level=3,
		description=_always_prepared_entry,
		)

Telepathic_Speech = _origin(
		AberrantSorcery,
		name="Telepathic Speech",
		min_level=3,
		description=_telepathic_speech_entry,
		)

Psionic_Sorcery = _origin(
		AberrantSorcery,
		name="Psionic Sorcery",
		min_level=6,
		description=(
			"When you cast a level 1+ spell from your Psionic Spells, you can "
			"pay for it with Sorcery Points equal to its level instead of a "
			"spell slot. Cast that way, it needs no Verbal or Somatic "
			"components, and no Material components unless the spell "
			"consumes them or they have a listed cost."
			),
		)

Psychic_Defenses = _origin(
		AberrantSorcery,
		name="Psychic Defenses",
		min_level=6,
		description=(
			"You have Resistance to Psychic damage, and Advantage on saving "
			"throws to avoid or end the Charmed or Frightened condition."
			),
		apply=_apply_psychic_defenses,
		)

Revelation_in_Flesh = _origin(
		AberrantSorcery,
		name="Revelation in Flesh",
		min_level=14,
		description=_revelation_in_flesh_entry,
		)

Warping_Implosion = _origin(
		AberrantSorcery,
		name="Warping Implosion",
		min_level=18,
		description=_warping_implosion_entry,
		)


# ---------------------------------------------------------------------------
# Clockwork Sorcery
# ---------------------------------------------------------------------------


Clockwork_Spells = _origin(
		ClockworkSorcery,
		name="Clockwork Spells",
		min_level=3,
		description=_clockwork_spells_entry,
		apply=_apply_clockwork_spells,
		)

Restore_Balance = _origin(
		ClockworkSorcery,
		name="Restore Balance",
		min_level=3,
		description=_restore_balance_entry,
		chips=(
				Chip(
						"",
						"Restore Balance",
						_charisma_count,
						),
				),
		)

Bastion_of_Law = _origin(
		ClockworkSorcery,
		name="Bastion of Law",
		min_level=6,
		description=(
			"<b>Magic action:</b> spend 1 to 5 Sorcery Points to ward yourself "
			"or a creature you can see within 30 feet. The ward is a pool of "
			"d8s, one for each point spent. When the warded creature takes "
			"damage, it can expend any number of those dice, roll them, and "
			"reduce the damage by the total. The ward lasts until you finish "
			"a Long Rest or use this feature again."
			),
		)

Trance_of_Order = _origin(
		ClockworkSorcery,
		name="Trance of Order",
		min_level=14,
		description=(
			"<b>Bonus Action:</b> enter a state of perfect order for 1 minute. "
			"While it lasts, attack rolls against you can't benefit from "
			"Advantage, and whenever you make a D20 Test you can treat a roll "
			"of 9 or lower on the d20 as a 10."
			+ _restored_by(
					5
					)
			),
		)

Clockwork_Cavalcade = _origin(
		ClockworkSorcery,
		name="Clockwork Cavalcade",
		min_level=18,
		description=(
			"<b>Magic action:</b> spirits of order sweep a 30-foot Cube "
			"originating from you, and bring all of these at once:<ul>"
			"<li><b>Heal.</b> They restore up to 100 Hit Points, divided as "
			"you choose among any creatures of your choice in the Cube.</li>"
			"<li><b>Repair.</b> Every damaged object entirely inside the Cube "
			"is repaired.</li>"
			"<li><b>Dispel.</b> Every spell of level 6 or lower ends on "
			"creatures and objects of your choice in the Cube.</li>"
			"</ul>"
			+ _restored_by(
					7
					)
			),
		)


# ---------------------------------------------------------------------------
# Draconic Sorcery
# ---------------------------------------------------------------------------


Draconic_Resilience = _origin(
		DraconicSorcery,
		name="Draconic Resilience",
		min_level=3,
		description=_draconic_resilience_entry,
		chips=(
				Chip(
						"",
						"Unarmored AC",
						_draconic_armour_class,
						),
				),
		apply=_apply_draconic_resilience,
		)

Draconic_Spells = _origin(
		DraconicSorcery,
		name="Draconic Spells",
		min_level=3,
		description=_always_prepared_entry,
		)

Elemental_Affinity = _origin(
		DraconicSorcery,
		name="Elemental Affinity",
		min_level=6,
		description=_elemental_affinity_entry,
		apply=_apply_elemental_affinity,
		)

Dragon_Wings = _origin(
		DraconicSorcery,
		name="Dragon Wings",
		min_level=14,
		description=(
			"<b>Bonus Action:</b> dragon wings sprout from your back and give "
			"you a Fly Speed of 60 feet. They last 1 hour, or until you "
			"dismiss them (no action required)."
			+ _restored_by(
					3
					)
			),
		)

Dragon_Companion = _origin(
		DraconicSorcery,
		name="Dragon Companion",
		min_level=18,
		description=(
			"You can cast <i>Summon Dragon</i> without a Material component, "
			"and once per Long Rest without a spell slot. Whenever you cast "
			"it, you can free it from Concentration; if you do, it lasts "
			"1 minute."
			),
		)


# ---------------------------------------------------------------------------
# Wild Magic Sorcery
# ---------------------------------------------------------------------------


Wild_Magic_Surge = _origin(
		WildMagicSorcery,
		name="Wild Magic Surge",
		min_level=3,
		description=(
			"Once per turn, immediately after you cast a Sorcerer spell with "
			"a spell slot, you can roll a d20. On a 20, roll on the Wild Magic "
			"Surge table to create a magical effect. If that effect is a "
			"spell, it is too wild for your Metamagic to touch."
			),
		)

Tides_of_Chaos = _origin(
		WildMagicSorcery,
		name="Tides of Chaos",
		min_level=3,
		description=(
			"Before you roll a D20 Test, you can give yourself Advantage on "
			"it. Once you do, you can't again until you cast a Sorcerer spell "
			"with a spell slot or finish a Long Rest. Casting that spell "
			"before the Long Rest also makes you roll on the Wild Magic Surge "
			"table."
			),
		)

Bend_Luck = _origin(
		WildMagicSorcery,
		name="Bend Luck",
		min_level=6,
		description=(
			"<b>Reaction:</b> immediately after another creature you can see "
			"rolls the d20 for a D20 Test, you can spend <b>1 Sorcery "
			"Point</b> to roll 1d4 and add it to, or subtract it from, that "
			"d20 roll."
			),
		)

Controlled_Chaos = _origin(
		WildMagicSorcery,
		name="Controlled Chaos",
		min_level=14,
		description=(
			"Whenever you roll on the Wild Magic Surge table, you roll twice "
			"and use either number."
			),
		)

Tamed_Surge = _origin(
		WildMagicSorcery,
		name="Tamed Surge",
		min_level=18,
		description=(
			"Immediately after you cast a Sorcerer spell with a spell slot, "
			"you can pick an effect from the Wild Magic Surge table instead "
			"of rolling for one. Any effect but the table's last row can be "
			"picked, and any roll it calls for is still made. Once you do, "
			"you can't again until you finish a Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Self-test: the lessons cover what SorcererKit declares
# ---------------------------------------------------------------------------


def _self_test() -> None:
	from AtlasLusoris.AtlasOfGuilds.SorcererKit import (
			SPECIALIZATIONS,
			Sorcerer,
			)
	from AtlasLusoris.TrainingKit import trainings_for

	lessons = trainings_for(
			GUILD
			)
	for origin in (
			None,
			*SPECIALIZATIONS,
			):
		owner = (
			Sorcerer
			if origin is None
			else origin
			)
		for grant in owner.FEATURES:
			matches = [
				lesson
				for lesson in lessons
				if lesson.NAME == grant.name
				and lesson.MIN_LEVEL == grant.level
				and lesson.PATH is origin
				]
			assert len(
					matches
					) == 1, (
				f"{owner.NAME} declares {grant.name} at level "
				f"{grant.level}; {len(matches)} lessons teach it."
				)
	declared = sum(
			len(
					owner.FEATURES
					)
			for owner in (
					Sorcerer,
					*SPECIALIZATIONS,
					)
			)
	assert len(
			lessons
			) == declared, (
		f"{len(lessons)} Sorcerer lessons for {declared} declared features."
		)
	print(
			"OK — Sorcerer Training self-test:",
			declared,
			"lessons cover the kit",
			)


if __name__ == "__main__":
	from AtlasLusoris.AtlasOfTraining.Map_of_Sorcerer_Training import (
			_self_test as _package_self_test,
			)
	_package_self_test()
