"""
Druid Training Tags — 2024 PHB core + all Circles.

Thought pattern
	1. Core lessons belong to the Druid Guild (no Circle).
	2. Circle lessons set path=… and awaken only for that Circle.
	3. Numbers live as Chips and callables — not as separate Tag members.
	4. ASI / Epic Boon stay on legacy Progression.
"""

from __future__ import annotations

from AtlasLusoris.FeaturesKit import Grant_Resistance
from AtlasLusoris.TrainingKit import Make_Training


GUILD = "Druid"
CORE_SOURCE = "Training: Druid"
LAND = "Land"
MOON = "Moon"
SEA = "Sea"
STARS = "Stars"


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
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			source=CORE_SOURCE,
			)


def _circle(
		circle_name: str,
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
			path=circle_name,
			source=f"Training: Circle of the {circle_name}",
			)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


def _apply_primal_order(
		char,
		) -> None:
	"""
	Settle the Primal Order once, and record it.

	This used to live inside the Entry callable, which drew from the shared
	stream and re-assigned on every call.  Entries are *projections*: they are
	resolved whenever the sheet is read, so anything that decides something has
	to happen in ``apply`` instead, guarded and drawn from a named Dice Bag.
	Deciding inside an Entry meant a Druid could change Order between reads.
	"""
	if getattr(
			char,
			"primal_order",
			None,
			) in (
			"Magician",
			"Warden",
			):
		return

	char.primal_order = char.Pick(
			(
					"Magician",
					"Warden",
					),
			dice=char.Dice_Bag(
					"Primal_Order.choice",
					),
			)


def _primal_order_entry(
		char,
		) -> str:
	order = getattr(
			char,
			"primal_order",
			"Magician",
			)
	if order == "Magician":
		return (
			"\n\n**Primal Order: Magician.** You know one extra cantrip "
			"from the Druid spell list and lean into primal spellcraft."
			)
	return (
		"\n\n**Primal Order: Warden.** You gain proficiency with Martial "
		"weapons and training in Medium armor."
		)


def _wild_shape_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	if level < 4:
		cr = "1/4"
	elif level < 8:
		cr = "1/2"
	else:
		cr = str(
				level // 3
				)
	fly = level >= 8
	fly_line = (
			" You can adopt a form with a Fly Speed."
			if fly
			else ""
			)
	return (
		"The power of nature allows you to assume the form of an animal. "
		"As a *Bonus Action*, you shape-shift into a Beast form you "
		"have learned. You stay in that form for a number of hours equal "
		"to half your Druid level or until you use Wild Shape again, have "
		"the Incapacitated condition, or die. You can leave the form early "
		"as a Bonus Action."
		f"\n\nMaximum Beast CR: **{cr}**.{fly_line}"
		"\n\nWhen you assume a Wild Shape form you gain **Temporary Hit "
		"Points** equal to your Druid level."
		)


def _elemental_fury_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	die = "2d6" if level >= 15 else "1d6"
	return (
		"The might of the elemental world infuses your Wild Shape and "
		"spells. Once per turn, choose one option:"
		"\n\n**Potent Spellcasting.** When you cast a Druid cantrip "
		"that deals damage, add your Wisdom modifier to one damage roll."
		"\n\n**Primal Strike.** Once per turn when you hit a creature "
		"while in Wild Shape, deal an extra "
		f"**{die}** Force or Necrotic damage."
		)


Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description=(
			"Drawing on the power of the natural world, you can cast spells. "
			"Wisdom is your spellcasting ability for Druid spells. You can "
			"use a Druidic Focus as your Spellcasting Focus. You prepare a "
			"list of Druid spells each Long Rest."
			),
		)

def _apply_druidic(
		char,
		) -> None:
	"""
	Know Druidic (2024 PHB; QST-0144.10).

	A fixed grant, no draw.  Before the Character holds a Linguistics there
	is nothing to grant to.
	"""
	from AtlasLudus.Map_of_Languages import Linguistics_Of
	languages = Linguistics_Of(
			char
			)
	if languages is None:
		return
	languages.Add(
			"Druidic"
			)


Druidic = _core(
		name="Druidic",
		min_level=1,
		description=(
			"You know **Druidic**, the secret language of Druids. While "
			"learning this ancient tongue, you also unlocked the magic of "
			"communicating with animals; you always have the *Speak with "
			"Animals* spell prepared."
			),
		apply=_apply_druidic,
		)

Primal_Order = _core(
		name="Primal Order",
		min_level=1,
		description=_primal_order_entry,
		apply=_apply_primal_order,
		)

Wild_Shape = _core(
		name="Wild Shape",
		min_level=2,
		description=_wild_shape_entry,
		)

def _apply_wild_companion(
		char,
		) -> None:
	"""Add Find Familiar to learned spells — sheet card lives in Spells."""
	from AtlasMagia.Lodge_of_Spells import FindFamiliar

	if getattr(
			char,
			"known_spells",
			None,
			) is None:
		char.known_spells = []
	names = {
			getattr(
					spell,
					"name",
					None,
					)
			for spell in char.known_spells
			}
	if FindFamiliar.name not in names:
		char.known_spells.append(
				FindFamiliar
				)


Wild_Companion = _core(
		name="Wild Companion",
		min_level=2,
		description=(
			"You learn *Find Familiar* and can cast it without preparing "
			"it. As a *Magic action*, expend a spell slot or a use of "
			"Wild Shape to cast it without Material components. The familiar "
			"is Fey and disappears when you finish a Long Rest."
			),
		apply=_apply_wild_companion,
		)

Wild_Resurgence = _core(
		name="Wild Resurgence",
		min_level=5,
		description=(
			"Once on each of your turns, if you have no uses of Wild Shape "
			"left, you can give yourself one use by expending a spell slot "
			"(no action required). In addition, you can expend one use of "
			"Wild Shape (no action required) to give yourself a level 1 "
			"spell slot, but you can't do so again until you finish a "
			"Long Rest."
			),
		)

Elemental_Fury = _core(
		name="Elemental Fury",
		min_level=7,
		description=_elemental_fury_entry,
		)

Improved_Elemental_Fury = _core(
		name="Improved Elemental Fury",
		min_level=15,
		description=(
			"Your Elemental Fury grows more powerful."
			"\n\n**Potent Spellcasting** now adds double your Wisdom "
			"modifier to cantrip damage."
			"\n\n**Primal Strike** now deals an extra **2d6** Force "
			"or Necrotic damage."
			),
		)

Beast_Spells = _core(
		name="Beast Spells",
		min_level=18,
		description=(
			"You can perform the Somatic and Verbal components of a Druid "
			"spell while in a Beast form, but you can't provide Material "
			"components."
			),
		)

Archdruid = _core(
		name="Archdruid",
		min_level=20,
		description=(
			"The title of Archdruid is yours. You can use Wild Shape an "
			"unlimited number of times; whenever you roll Initiative with "
			"no uses remaining, you regain one use. Moreover, for every "
			"10 years that pass, your body ages only 1 year."
			),
		)


# ---------------------------------------------------------------------------
# Circle of the Land
# ---------------------------------------------------------------------------


def _land(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _circle(
			LAND,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Circle_Spells_Land = _land(
		name="Circle Spells",
		min_level=3,
		description=(
			"Your mystical connection to the land infuses you with the "
			"ability to cast certain spells. You always have prepared a set "
			"of spells determined by your chosen land type (Arctic, Coast, "
			"Desert, Forest, Grassland, Mountain, Swamp, or Underdark). "
			"These don't count against the number of spells you can prepare."
			),
		)

Lands_Aid = _land(
		name="Land's Aid",
		min_level=3,
		description=(
			"As a *Magic action*, expend a use of Wild Shape to bolster "
			"allies or drain a foe. Choose a point within 60 feet — each "
			"creature of your choice within 30 feet regains Hit Points equal "
			"to 1d6 plus your Wisdom modifier, and one creature in that area "
			"must make a Constitution saving throw or become Poisoned until "
			"the end of your next turn."
			),
		)

Natural_Recovery = _land(
		name="Natural Recovery",
		min_level=6,
		description=(
			"When you finish a Short Rest, you can expend uses of Wild Shape "
			"to recover spell slots. Each use of Wild Shape you expend "
			"recovers one spell slot level; recovered slots can't exceed "
			"level 5."
			),
		)

Natures_Ward = _land(
		name="Nature's Ward",
		min_level=10,
		description=(
			"You have Immunity to the Frightened and Poisoned conditions "
			"and to disease. Difficult terrain caused by natural plants "
			"doesn't impede your movement."
			),
		)

Natures_Sanctuary = _land(
		name="Nature's Sanctuary",
		min_level=14,
		description=(
			"When a Beast or Plant creature attacks you, it must make a "
			"Wisdom saving throw against your spell save DC. On a failed "
			"save, the creature must choose a different target, or the "
			"attack misses. On a success, the creature is immune to this "
			"effect for 24 hours."
			),
		)


# ---------------------------------------------------------------------------
# Circle of the Moon
# ---------------------------------------------------------------------------


def _moon(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _circle(
			MOON,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Circle_Forms = _moon(
		name="Circle Forms",
		min_level=3,
		description=(
			"Your Wild Shape forms grow more powerful. You can transform "
			"into any Beast with a CR equal to your Druid level divided by 3 "
			"(round down, minimum 1). Starting at level 10, you can also "
			"Wild Shape into an Elemental (Air, Earth, Fire, or Water) "
			"once per Long Rest."
			),
		)

Moon_Spells = _moon(
		name="Moon Spells",
		min_level=3,
		description=(
			"Your connection to the moon grants extra spells always prepared: "
			"*Faerie Fire, Moonbeam, Vampiric Touch, Greater Invisibility.* "
			"These don't count against the number of spells you can prepare."
			),
		)

Improved_Circle_Forms = _moon(
		name="Improved Circle Forms",
		min_level=6,
		description=(
			"While in a Wild Shape form, you can expend spell slots to deal "
			"extra Radiant damage. As a Bonus Action, expend a spell slot; "
			"the next time you hit a creature this turn, add 2d6 Radiant "
			"damage per slot level to the hit."
			),
		)

Moonlight_Step = _moon(
		name="Moonlight Step",
		min_level=10,
		description=(
			"As a Bonus Action, you teleport up to 30 feet to an unoccupied "
			"space you can see. Uses equal your Wisdom modifier (minimum 1); "
			"all uses regained on a Long Rest."
			),
		)

Lunar_Form = _moon(
		name="Lunar Form",
		min_level=14,
		description=(
			"While in Wild Shape, you have Resistance to all damage except "
			"Psychic and Radiant, your natural weapon attacks count as "
			"magical, and you regain Hit Points equal to your Wisdom "
			"modifier at the start of each of your turns."
			),
		)


# ---------------------------------------------------------------------------
# Circle of the Sea
# ---------------------------------------------------------------------------


def _sea(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		apply=None,
		):
	return _circle(
			SEA,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			apply=apply,
			)


Sea_Spells = _sea(
		name="Sea Spells",
		min_level=3,
		description=(
			"Your bond to the ocean grants extra spells always prepared: "
			"*Fog Cloud, Thunderwave, Shatter, Misty Step.* "
			"These don't count against the number of spells you can prepare."
			),
		)

Wrath_of_the_Sea = _sea(
		name="Wrath of the Sea",
		min_level=3,
		description=(
			"As a Bonus Action, expend a use of Wild Shape to create a "
			"watery aura for 10 minutes. Whenever a creature starts its turn "
			"within 10 feet of you, it must make a Strength saving throw "
			"against your spell save DC — on a fail it takes 2d8 Cold or "
			"Thunder damage (your choice) and is pushed 15 feet away."
			),
		)

Aquatic_Affinity = _sea(
		name="Aquatic Affinity",
		min_level=6,
		description=(
			"You gain a Swim Speed equal to your Speed, can breathe "
			"underwater, and have Advantage on Strength (Athletics) checks "
			"while swimming. Wild Shape forms also gain your Swim Speed."
			),
		)

def _grant_storm_resistances(
		char,
		) -> None:
	Grant_Resistance(
			char,
			"Cold",
			"Lightning",
			"Thunder",
			)


Stormborn = _sea(
		name="Stormborn",
		min_level=10,
		description=(
			"You have Resistance to Cold, Lightning, and Thunder damage. "
			"Once per turn when you deal Cold, Lightning, or Thunder damage "
			"with a spell, you can push the target up to 10 feet away."
			),
		apply=_grant_storm_resistances,
		)

Oceanic_Gift = _sea(
		name="Oceanic Gift",
		min_level=14,
		description=(
			"As an action, unleash a surge of ocean energy. Each creature "
			"of your choice within 60 feet must succeed on a Strength saving "
			"throw or take 10d8 Cold damage and be knocked Prone; on a "
			"success it takes half damage and isn't Prone. Friendly creatures "
			"in the area instead regain Hit Points equal to the damage "
			"calculated for them."
			"\n\nOnce you use this feature, you can't do so again until you "
			"finish a Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Circle of Stars
# ---------------------------------------------------------------------------


def _stars(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _circle(
			STARS,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


def _starry_form_entry(
		char,
		) -> str:
	level = _rank(
			char
			)
	die = "2d8" if level >= 10 else "1d8"
	return (
		"When you use Wild Shape, you can expend a use to adopt a luminous "
		"Starry Form instead of a Beast form. You retain your statistics, "
		"but gain one active constellation:"
		f"\n\n**Archer.** Bonus Action ranged spell attack — **{die}** "
		"Radiant on a hit."
		f"\n\n**Chalice.** When you cast a healing spell, you or a "
		f"creature within 30 feet regains an extra **{die}** HP."
		"\n\n**Dragon.** When you make an Intelligence or Wisdom check, "
		"treat any roll of 9 or lower as a 10."
		)


Star_Map = _stars(
		name="Star Map",
		min_level=3,
		description=(
			"You have charted the heavens and created a Star Map — a record "
			"of the night sky that serves as a Spellcasting Focus. You always "
			"have *Guidance* and *Guiding Bolt* prepared; you can "
			"cast *Guiding Bolt* without expending a spell slot a "
			"number of times equal to your Wisdom modifier per Long Rest."
			),
		)

Starry_Form = _stars(
		name="Starry Form",
		min_level=3,
		description=_starry_form_entry,
		)

Cosmic_Omen = _stars(
		name="Cosmic Omen",
		min_level=6,
		description=(
			"When you finish a Long Rest, roll a die. Until your next Long "
			"Rest, you can use a Reaction when a creature you can see within "
			"30 feet makes a roll:"
			"\n\n**Weal (even).** Add 1d6 to the roll."
			"\n\n**Woe (odd).** Subtract 1d6 from the roll."
			"Uses equal your Wisdom modifier (minimum 1); regained on "
			"a Long Rest."
			),
		)

Twinkling_Constellations = _stars(
		name="Twinkling Constellations",
		min_level=10,
		description=(
			"Your Starry Form constellations improve. Archer and Chalice "
			"each deal or restore 2d8 instead of 1d8. While in Dragon form, "
			"you have a Fly Speed of 20 feet and can hover."
			),
		)

Full_of_Stars = _stars(
		name="Full of Stars",
		min_level=14,
		description=(
			"While in your Starry Form, you become partially incorporeal, "
			"gaining Resistance to Bludgeoning, Piercing, and Slashing damage."
			),
		)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> None:
	"""Primal Order draws from a bag named by its lesson (ruling 8)."""
	from types import SimpleNamespace

	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills

	opened = []
	original = Character.Dice_Bag

	def Recording_Dice_Bag(
			char,
			purpose,
			**key,
			):
		bag = original(
				char,
				purpose,
				**key,
				)
		opened.append(
				(
					purpose,
					key,
					bag,
					)
				)
		return bag

	def Purposes() -> list:
		"""What was opened, as (purpose, key): a key of {} is the default."""
		return [
				(
					purpose,
					key,
					)
				for purpose, key, _ in opened
				]

	def Skeleton(
			seed: int,
			level: int,
			):
		"""A Character with a skill sheet and nothing else."""
		char = Character(
				seed=seed,
				level=level,
				)
		char.skills = Char_Skills(
				char,
				SimpleNamespace(
						STR=10,
						DEX=10,
						CON=10,
						INT=10,
						WIS=10,
						CHA=10,
						),
				2,
				)
		return char

	Character.Dice_Bag = Recording_Dice_Bag
	try:
		char = Skeleton(
				seed=7,
				level=1,
				)

		_apply_primal_order(
				char,
				)
		assert Purposes() == [
				(
					"Primal_Order.choice",
					{},
					),
				], opened
		assert char.primal_order == char.Pick(
				(
					"Magician",
					"Warden",
					),
				dice=original(
						char,
						"Primal_Order.choice",
						),
				)
			#-- The pool is the pair, in this order, and the answer is that
			#-- bag's first draw over it: nothing else draws from this bag.
		opened.clear()
		_apply_primal_order(
				char,
				)
		assert opened == [], "a settled Order is not drawn again"

		#-- Druidic is a fixed grant onto the Linguistics the Character holds,
		#-- with no draw; before there is one, nothing happens.
		from AtlasLudus.Map_of_Languages import Linguistics
		_apply_druidic(
				char,
				)
		assert getattr(
				char,
				"languages",
				None,
				) is None
		char.languages = Linguistics()
		char.languages.Add(
				"Common"
				)
		opened.clear()
		_apply_druidic(
				char,
				)
		assert opened == [], opened
		assert char.languages.langs == {"Common", "Druidic"}, char.languages.langs
	finally:
		Character.Dice_Bag = original
	print(
			"Map_of_Druid_Training: self-test OK"
			)


if __name__ == "__main__":
	_self_test()
