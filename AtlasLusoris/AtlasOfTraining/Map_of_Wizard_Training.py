"""
Wizard Training Tags — 2024 PHB core + all Arcane Traditions.

Thought pattern
        1. Core lessons belong to the Wizard Guild (no Tradition).
        2. Tradition lessons set path=… and awaken only for that Tradition.
        3. Recovery levels and Portent dice live as Chips.
        4. ASI / Epic Boon stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasVenustas import Chip


GUILD = "Wizard"
CORE_SOURCE = "Training: Wizard"
ABJURER = "Abjurer"
DIVINER = "Diviner"
EVOKER = "Evoker"
ILLUSIONIST = "Illusionist"

BLADESINGER = "Bladesinger"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _intelligence_modifier(
		char,
		) -> int:
	scores = getattr(
			char,
			"AS",
			None,
			)
	return int(
			getattr(
					scores,
					"int_mod",
					0,
					) or 0,
			)


def _bladesong_uses(
		char,
		) -> int:
	"""Intelligence modifier, minimum once."""
	return max(
			1,
			_intelligence_modifier(
					char
					),
			)


def _bladesong_ac(
		char,
		) -> int:
	"""The Agility bonus: Intelligence modifier, minimum +1."""
	return max(
			1,
			_intelligence_modifier(
					char
					),
			)


def _recovery_slots(
		char,
		) -> int:
	return max(
			1,
			(_rank(char) + 1) // 2,
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


def _tradition(
		tradition_name: str,
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
			path=tradition_name,
			source=f"Training: {tradition_name} Tradition",
			)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


def _arcane_recovery_entry(
		char,
		) -> str:
	recovery = _recovery_slots(
			char
			)
	return (
		"When you finish a Short Rest, you can choose expended spell "
		"slots to recover. The slots can have a combined level equal "
		f"to no more than <b>{recovery}</b> (half your Wizard level, "
		"rounded up), and none can be level 6 or higher.<br>"
		"Once you use this feature, you can't do so again until you "
		"finish a Long Rest."
		)


Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description=(
			"Your scholarly study of arcane magic grants you the ability to "
			"cast Wizard spells. Intelligence is your spellcasting ability. "
			"You can use an Arcane Focus or your Spellbook as your "
			"Spellcasting Focus. You prepare a list of Wizard spells from your Spellbook each Long Rest."
			),
		)


def _spell_levels_on_the_sheet(
		char,
		) -> int:
	"""
The summed level of every levelled spell this Character is carrying.

Rebuilding a lost book costs an hour and 10 GP per spell level, so this is
the number both figures are struck from. Cantrips cost nothing to set down
again and are not counted.
"""
	try:
		known = char.get_spellcaster().spells_known
	except Exception:
		return 0
	total = 0
	for spell in known:
		if "Cantrip" in type(
				spell
				).__name__:
			continue
		total += int(
				getattr(
						spell,
						"level",
						0,
						) or 0,
				)
	return total


def _apply_spellbook(
		char,
		) -> None:
	"""Settle what this Wizard's book physically is, once and for life."""
	from AtlasLusoris.AtlasOfTraining.Map_of_Spellbooks import Draw_Spellbook
	Draw_Spellbook(
			char,
			)


def _spellbook_entry(
		char,
		) -> str:
	"""
The rules, opening on whatever this Character's book turned out to be.

Matter-of-fact on purpose: the form is one clause, the rules follow
unchanged, and nothing announces that a choice was made.
"""
	form = getattr(
			char,
			"spellbook_form",
			None,
			) or "a Tiny object"

	# Both rebuild figures below are struck from the same count, so the
	# prose can never disagree with itself.
	levels = _spell_levels_on_the_sheet(
			char
			)
	return (
		f"Your Spellbook is {form}. It holds the spells you know. "
		"It is a Tiny object weighing 3 pounds, it has room for 100 pages, "
		"and it can be read only by you or by someone casting "
		"<i>Identify</i>.<br><b>Copying a Spell.</b> A Wizard spell you "
		"find, on a Spell Scroll or in another book, can be copied into "
		"yours if it is of a level you can prepare. It takes 2 hours and "
		"50 GP per spell level.<br><b>Copying the Book.</b> Copying a "
		"spell you already know into a second book is faster: 1 hour and "
		"10 GP per spell level. Many Wizards keep a spare for exactly "
		"that reason.<br><b>Replacing the Book.</b> If you lose it you must spend <b>"
		f"{levels * 10} GP</b> and <b>{levels} hours</b> to rebuild it "
		"with the spells on this sheet. Any other spell you had learnt "
		"is lost with the original."
		)


Spellbook = _core(
		name="Spellbook",
		min_level=1,
		description=_spellbook_entry,
		apply=_apply_spellbook,
		)

Ritual_Adept = _core(
		name="Ritual Adept",
		min_level=1,
		description=(
			"You can cast any spell as a Ritual if that spell has the Ritual "
			"tag and the spell is in your Spellbook. You needn't have the "
			"spell prepared, but you must read from the book."
			),
		)

Arcane_Recovery = _core(
		name="Arcane Recovery",
		min_level=1,
		description=_arcane_recovery_entry,
		chips=(
				Chip(
					"✦",
					"Recovery Levels",
					_recovery_slots,
					),
				),
		)

Scholar = _core(
		name="Scholar",
		min_level=2,
		description=(
			"While studying magic, you also specialized in another field. "
			"Choose one skill in which you have proficiency: Arcana, History, "
			"Investigation, Medicine, Nature, or Religion. You have Expertise "
			"in that skill."
			),
		)

Memorize_Spell = _core(
		name="Memorize Spell",
		min_level=5,
		description=(
			"Whenever you finish a Short Rest, you can study your Spellbook "
			"and replace one of the level 1+ Wizard spells you have prepared "
			"with another level 1+ spell from the book."
			),
		)

Spell_Mastery = _core(
		name="Spell Mastery",
		min_level=18,
		description=(
			"Choose a level 1 and a level 2 spell from your Spellbook "
			"with a casting time of an Action. You always have those "
			"spells prepared and can cast them at their lowest level "
			"without expending a spell slot. To cast either spell at "
			"a higher level, you must expend a spell slot.<br>"
			"Whenever you finish a Long Rest, you can study your "
			"Spellbook and replace one of those spells with an "
			"eligible spell of the same level from the book."
			),
		)

Signature_Spells = _core(
		name="Signature Spells",
		min_level=20,
		description=(
			"Choose two level 3 spells from your Spellbook as your Signature "
			"Spells. You always have them prepared and can cast each once at "
			"level 3 without expending a slot. When you do, you can't cast "
			"them in this way again until a Short or Long Rest. To cast "
			"either at a higher level, expend a spell slot."
			),
		)


# ---------------------------------------------------------------------------
# Abjurer Tradition
# ---------------------------------------------------------------------------


def _abjurer(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _tradition(
			ABJURER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Abjuration_Savant = _abjurer(
		name="Abjuration Savant",
		min_level=3,
		description=(
			"You can add two Abjuration spells from the Wizard list to your "
			"Spellbook at no cost when you gain this feature and one each "
			"subsequent Wizard level-up. Spells must be of a level for which "
			"you have slots."
			),
		)

Arcane_Ward = _abjurer(
		name="Arcane Ward",
		min_level=3,
		description=(
			"When you cast an Abjuration spell of level 1 or higher, you "
			"can simultaneously create a magical ward on yourself. The "
			"ward has HP equal to twice your Wizard level plus your "
			"Intelligence modifier. Whenever you take damage, the ward "
			"takes the damage instead. If this reduces the ward to 0, you "
			"take any remaining damage. Casting an Abjuration spell of "
			"level 1+ restores HP to the ward equal to twice the spell's level."
			),
		)

Projected_Ward = _abjurer(
		name="Projected Ward",
		min_level=6,
		description=(
			"When a creature you can see within 30 feet takes damage, you "
			"can use your Reaction to cause your Arcane Ward to absorb that "
			"damage instead. If this reduces the ward to 0, the warded "
			"creature takes any remaining damage."
			),
		)

Spell_Breaker = _abjurer(
		name="Spell Breaker",
		min_level=10,
		description=(
			"When you restore Hit Points to an ally with a healing spell of "
			"level 1 or higher, you can simultaneously end one spell on the "
			"ally of a level less than or equal to the healing spell's level."
			),
		)

Spell_Resistance = _abjurer(
		name="Spell Resistance",
		min_level=14,
		description=(
			"You have Advantage on saving throws against spells. Furthermore, "
			"you have Resistance to the damage of spells."
			),
		)


# ---------------------------------------------------------------------------
# Diviner Tradition
# ---------------------------------------------------------------------------


def _diviner(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _tradition(
			DIVINER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _portent_dice(
		char,
		) -> int:
	return 3 if _rank(char) >= 14 else 2


Divination_Savant = _diviner(
		name="Divination Savant",
		min_level=3,
		description=(
			"You can add two Divination spells from the Wizard list to your "
			"Spellbook at no cost when you gain this feature and one each "
			"subsequent Wizard level-up. Spells must be of a level for which "
			"you have slots."
			),
		)

Portent = _diviner(
		name="Portent",
		min_level=3,
		description=(
			"Glimpses of the future haunt your dreams. When you finish a "
			"Long Rest, roll d20s and record the results. Once before your "
			"next Long Rest, you can replace any attack roll, saving throw, "
			"or ability check made by you or a creature you can see with "
			"one foretold result — you must choose before the roll."
			),
		chips=(
				Chip(
					"✦",
					"Portent Dice",
					_portent_dice,
					),
				),
		)

Expert_Divination = _diviner(
		name="Expert Divination",
		min_level=6,
		description=(
			"When you cast a Divination spell of level 2 or higher using a "
			"spell slot, you regain one expended spell slot. The regained "
			"slot is of a level lower than the spell cast and can't be "
			"level 6 or higher."
			),
		)

The_Third_Eye = _diviner(
		name="The Third Eye",
		min_level=10,
		description=(
			"When you take the Study action or finish a Short Rest, choose "
			"one benefit (lasts until Incapacitated or until another rest):"
			"<br><b>Darkvision.</b> 60-foot Darkvision (or extend by 60 ft)."
			"<br><b>Ethereal Sight.</b> See into the Ethereal Plane within "
			"60 feet."
			"<br><b>Greater Comprehension.</b> Read any language."
			"<br><b>See Invisibility.</b> As per the <i>See Invisibility</i> "
			"spell."
			),
		)

Greater_Portent = _diviner(
		name="Greater Portent",
		min_level=14,
		description=(
			"The visions in your dreams grow more vivid. You now roll "
			"<b>three</b> d20s for your Portent feature, rather than two."
			),
		)


# ---------------------------------------------------------------------------
# Evoker Tradition
# ---------------------------------------------------------------------------


def _evoker(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _tradition(
			EVOKER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Evocation_Savant = _evoker(
		name="Evocation Savant",
		min_level=3,
		description=(
			"You can add two Evocation spells from the Wizard list to your "
			"Spellbook at no cost when you gain this feature and one each "
			"subsequent Wizard level-up. Spells must be of a level for which "
			"you have slots."
			),
		)

Potent_Cantrip = _evoker(
		name="Potent Cantrip",
		min_level=3,
		description=(
			"When a creature succeeds on a saving throw against one of your "
			"damaging cantrips, the creature takes half the cantrip's damage "
			"(but no other effect)."
			),
		)

Sculpt_Spells = _evoker(
		name="Sculpt Spells",
		min_level=6,
		description=(
			"When you cast an Evocation spell affecting other creatures you "
			"can see, you can choose a number of them equal to 1 plus the "
			"spell's level. The chosen creatures automatically succeed on "
			"their saving throws and take no damage if they would normally "
			"take half damage on a successful save."
			),
		)

Empowered_Evocation = _evoker(
		name="Empowered Evocation",
		min_level=10,
		description=(
			"You can add your Intelligence modifier to one damage roll of "
			"any Wizard Evocation spell you cast."
			),
		)

Overchannel = _evoker(
		name="Overchannel",
		min_level=14,
		description=(
			"When you cast a Wizard spell of level 1–5 that deals damage, "
			"you can deal maximum damage with that spell.<br>"
			"The first time you do this, no ill effects. The second time "
			"and each time before your next Long Rest, you take 2d12 "
			"Necrotic damage per spell level immediately after casting. "
			"This damage can't be reduced."
			),
		)


# ---------------------------------------------------------------------------
# Illusionist Tradition
# ---------------------------------------------------------------------------


def _illusionist(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _tradition(
			ILLUSIONIST,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Illusion_Savant = _illusionist(
		name="Illusion Savant",
		min_level=3,
		description=(
			"You can add two Illusion spells from the Wizard list to your "
			"Spellbook at no cost when you gain this feature and one each "
			"subsequent Wizard level-up. Spells must be of a level for which "
			"you have slots."
			),
		)

Improved_Illusions = _illusionist(
		name="Improved Illusions",
		min_level=3,
		description=(
			"You can cast Illusion spells without Verbal components. When "
			"you cast an Illusion spell with a Duration of 1 minute or "
			"longer, you can make it permanent by expending a level 3+ "
			"spell slot in addition to the spell's own slot. A permanent "
			"illusion requires no Concentration."
			),
		)

Phantasmal_Creatures = _illusionist(
		name="Phantasmal Creatures",
		min_level=6,
		description=(
			"When you cast an Illusion spell of level 1 or higher using a "
			"spell slot, you can choose one illusion to become a phantasmal "
			"creature of a type of your choice. The duplicate can take "
			"actions and interact with creatures using your spell save DC "
			"and spell attack bonus, but deals no damage and has 1 HP."
			),
		)

Illusory_Self = _illusionist(
		name="Illusory Self",
		min_level=10,
		description=(
			"When a creature makes an attack roll against you, you can use "
			"your Reaction to interpose an illusory duplicate. The attack "
			"automatically misses, then the illusion dissipates. Once used, "
			"<br>Once you use this feature, you can't do so again until you "
			"finish a Short or Long Rest."
			),
		)

Illusory_Reality = _illusionist(
		name="Illusory Reality",
		min_level=14,
		description=(
			"When you cast an Illusion spell of level 1 or higher, you can "
			"choose one inanimate, nonmagical object that is part of the "
			"illusion and make that object real for 1 minute. The object "
			"can't deal damage or directly harm anyone."
			),
		)


# ---------------------------------------------------------------------------
# Bladesinger Tradition
#
# Not a 2024 PHB Tradition: carried forward from Tasha's Cauldron of
# Everything and renumbered to the 2024 subclass levels (3 / 6 / 10 / 14),
# so the Atlas can print an intact Bladesinger sheet.
# ---------------------------------------------------------------------------


def _bladesinger(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _tradition(
			BLADESINGER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _bladesong_entry(
		char,
		) -> str:
	return (
		"As a <i>Bonus Action</i> you invoke the Bladesong, provided you are "
		"not wearing armor or using a Shield. It lasts 1 minute, and ends "
		"early if you have the Incapacitated condition, if you don armor or "
		"a Shield, or if you use two hands to attack with a weapon. You can "
		"dismiss it at any time (no action required).<br>You can invoke it <b>"
		f"{_bladesong_uses(char)}</b> times, regaining all uses on a Long "
		"Rest and one use whenever you use Arcane Recovery.<br>"
		"<b>Agility.</b> You gain <b>+"
		f"{_bladesong_ac(char)}</b> to AC, your Speed increases by <b>10 "
		"feet</b>, and you have Advantage on Dexterity (Acrobatics) "
		"checks.<br><b>Bladework.</b> When you attack with a weapon you "
		"are proficient with, you can use <b>Intelligence</b> for the "
		"attack and damage rolls instead of Strength or Dexterity.<br>"
		"<b>Focus.</b> When you make a Constitution saving throw to "
		"maintain Concentration, you can add <b>+"
		f"{_intelligence_modifier(char)}</b> "
		"to the total."
		)


Bladesong = _bladesinger(
		name="Bladesong",
		min_level=3,
		description=_bladesong_entry,
		chips=(
				Chip(
					"✦",
					"Bladesong Uses",
					_bladesong_uses,
					),
				Chip(
					"✦",
					"Bladesong AC",
					_bladesong_ac,
					),
				),
		)

Training_in_War_and_Song = _bladesinger(
		name="Training in War and Song",
		min_level=3,
		description=(
			"You gain proficiency with all Melee Martial weapons that do "
			"not have the Two-Handed or Heavy property. You can use a "
			"Melee weapon you are proficient with as a <b>Spellcasting "
			"Focus</b> for your Wizard spells.<br>"
			"You also gain proficiency in one of Acrobatics, Athletics, "
			"Performance, or Persuasion."
			),
		)

Bladesinger_Extra_Attack = _bladesinger(
		name="Extra Attack",
		min_level=6,
		description=(
			"You can attack <b>twice</b> instead of once whenever you take "
			"the Attack action on your turn. You can also cast one of your "
			"Wizard cantrips that has a casting time of an action in place "
			"of one of those attacks."
			),
		)

Song_of_Defense = _bladesinger(
		name="Song of Defense",
		min_level=10,
		description=(
			"When you take damage while your Bladesong is active, you can "
			"take a <i>Reaction</i> to expend one spell slot and reduce the "
			"damage taken by <b>five times the slot's level</b>."
			),
		)

Song_of_Victory = _bladesinger(
		name="Song of Victory",
		min_level=14,
		description=(
			"After you cast a spell that has a casting time of an action, "
			"you can make one attack with a weapon as a <i>Bonus Action</i>."
			),
		)
