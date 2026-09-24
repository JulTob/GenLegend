"""
Artificer Training Tags — 2024 core Guild lessons + all Specialties.

Thought pattern
        1. Core lessons belong to the Artificer Guild (no Specialty).
        2. Specialty lessons set path=… and awaken only for that Specialty.
        3. Infusion counts live as Chips.
        4. Artificer has no legacy Progression — all lessons live here.
"""

from __future__ import annotations

from AtlasLusoris.TrainingKit import Make_Training
from AtlasVenustas import Chip


GUILD = "Artificer"
CORE_SOURCE = "Training: Artificer"
ALCHEMIST = "Alchemist"
ARMORER = "Armorer"
ARTILLERIST = "Artillerist"
BATTLE_SMITH = "Battle Smith"


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
			char,
			GUILD,
			)


def _infusions_known(
		char,
		) -> int:
	level = _rank(
			char
			)
	if level >= 20:
		return 12
	if level >= 18:
		return 11
	if level >= 14:
		return 10
	if level >= 12:
		return 9
	if level >= 10:
		return 8
	if level >= 8:
		return 7
	if level >= 6:
		return 6
	if level >= 4:
		return 4
	return 2


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


def _specialty(
		specialty_name: str,
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
			path=specialty_name,
			source=f"Training: {specialty_name} Specialty",
			)


# ---------------------------------------------------------------------------
# Core Guild lessons
# ---------------------------------------------------------------------------


Spellcasting = _core(
		name="Spellcasting",
		min_level=1,
		description=(
			"You have studied the workings of magic and learned to channel "
			"it through tools. Intelligence is your spellcasting ability "
			"for Artificer spells. You can use Thieves' Tools, Tinker's "
			"Tools, or another Artisan's Tool you are proficient with as a "
			"Spellcasting Focus."
			),
		)

Tinkers_Magic = _core(
		name="Tinker's Magic",
		min_level=1,
		description=(
			"With Tinker's Tools or other Artisan's Tools in hand, you can "
			"imbue a Tiny nonmagical object with one magical property of "
			"your choice: a gentle light, a recorded message, a faint odor "
			"or nonverbal sound, or a static visual effect. You can maintain "
			"a number of such objects equal to your Intelligence modifier "
			"(minimum 1)."
			),
		)

Replicate_Magic_Item = _core(
		name="Replicate Magic Item",
		min_level=2,
		description=(
			"You have learned plans for crafting certain magic items. "
			"Whenever you finish a Long Rest, you can create one or more "
			"magic items from your known plans. The number of items you "
			"can maintain and the plans available scale with your Artificer "
			"level. Creating an item requires the tools named in the plan."
			),
		chips=(
				Chip(
					"✦",
					"Infusions Known",
					_infusions_known,
					),
				),
		)

Magic_Item_Tinker = _core(
		name="Magic Item Tinker",
		min_level=6,
		description=(
			"Your understanding of magic items deepens. You can be attuned "
			"to a maximum of <b>four</b> magic items simultaneously "
			"(instead of the normal three)."
			),
		)

Flash_of_Genius = _core(
		name="Flash of Genius",
		min_level=7,
		description=(
			"As a Reaction when you or another creature you can see within "
			"30 feet makes an ability check or saving throw, you can "
			"add your Intelligence modifier to the roll. Uses equal your "
			"Intelligence modifier (minimum 1); regained on a Long Rest."
			),
		)

Magic_Item_Adept = _core(
		name="Magic Item Adept",
		min_level=10,
		description=(
			"You can be attuned to up to <b>five</b> magic items at once. "
			"If you craft a magic item requiring an Uncommon or Rare formula, "
			"it takes a quarter of the normal time and costs half as much "
			"gold."
			),
		)

Spell_Storing_Item = _core(
		name="Spell-Storing Item",
		min_level=11,
		description=(
			"When you finish a Long Rest, touch a Simple or Martial weapon "
			"or a Spellcasting Focus and store a level 1 or 2 Artificer "
			"spell in it (casting time: 1 Action). While holding the item, "
			"a creature can take a Magic action to expend a stored charge "
			"and cast the spell. The item holds up to your Intelligence "
			"modifier (minimum 1) charges."
			),
		)

Advanced_Artifice = _core(
		name="Advanced Artifice",
		min_level=14,
		description=(
			"You can be attuned to up to <b>six</b> magic items at once. "
			"You can now replicate Rare magic items with Replicate Magic Item. "
			"Once per Long Rest per spell, you can cast any Artificer "
			"spell you know using Tinker's Tools without expending a "
			"spell slot."
			),
		)

Magic_Item_Master = _core(
		name="Magic Item Master",
		min_level=18,
		description=(
			"Magic items are extensions of your will. You can be attuned "
			"to up to <b>seven</b> magic items simultaneously."
			),
		)

Soul_of_Artifice = _core(
		name="Soul of Artifice",
		min_level=20,
		description=(
			"For each magic item you are currently attuned to, you gain a "
			"+1 bonus to all saving throws (maximum +6). In addition, if "
			"you're reduced to 0 Hit Points, you can use your Reaction to "
			"end one of your Artificer infusions, dropping to 1 HP instead."
			),
		)


# ---------------------------------------------------------------------------
# Alchemist Specialty
# ---------------------------------------------------------------------------


def _alchemist(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _specialty(
			ALCHEMIST,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Tools_of_the_Trade_Alchemist = _alchemist(
		name="Tools of the Trade",
		min_level=3,
		description=(
			"You gain proficiency with Alchemist's Supplies. If you already "
			"have this proficiency, gain proficiency with one other Artisan's "
			"Tools of your choice. You can use Alchemist's Supplies as a "
			"Spellcasting Focus for Artificer spells."
			),
		)

Alchemist_Spells = _alchemist(
		name="Alchemist Spells",
		min_level=3,
		description=(
			"Your alchemical study unlocks extra spells always prepared: "
			"<i>Healing Word, Ray of Sickness, Flaming Sphere, Melf's "
			"Acid Arrow, Mass Healing Word, Stinking Cloud.</i> "
			"These don't count against your prepared spells."
			),
		)

Experimental_Elixir = _alchemist(
		name="Experimental Elixir",
		min_level=3,
		description=(
			"When you finish a Long Rest, produce a number of experimental "
			"elixirs equal to your Intelligence modifier (minimum 1). "
			"Roll for each on the Experimental Elixir table or choose: "
			"<i>Healing</i> (2d4+Int HP), <i>Swiftness</i> (+10 ft Speed "
			"1 hour), <i>Resilience</i> (1d8+Int Temp HP), <i>Boldness</i> "
			"(Advantage on attacks and saves vs. fear 1 min), <i>Flight</i> "
			"(10 ft Fly Speed 10 min), <i>Transformation</i> (Alter Self "
			"10 min). Elixirs expire on your next Long Rest."
			),
		)

Alchemical_Savant = _alchemist(
		name="Alchemical Savant",
		min_level=5,
		description=(
			"When you cast a spell using Alchemist's Supplies as your "
			"Spellcasting Focus, add your Intelligence modifier to one "
			"roll that restores Hit Points or deals Acid, Fire, Necrotic, "
			"or Poison damage."
			),
		)

Restorative_Reagents = _alchemist(
		name="Restorative Reagents",
		min_level=9,
		description=(
			"Whenever a creature drinks one of your Experimental Elixirs, "
			"it gains Temporary Hit Points equal to 2d6 plus your "
			"Intelligence modifier. You always have <i>Lesser Restoration</i> "
			"prepared; you can cast it without a spell slot a number "
			"of times equal to your Intelligence modifier (minimum 1), "
			"regained on a Long Rest."
			),
		)

Chemical_Mastery = _alchemist(
		name="Chemical Mastery",
		min_level=15,
		description=(
			"You gain Immunity to the Poisoned condition and Resistance to "
			"Acid and Poison damage. You can cast <i>Greater Restoration</i> "
			"and <i>Heal</i> each once per Long Rest without expending a "
			"spell slot, using Alchemist's Supplies as the focus."
			),
		)


# ---------------------------------------------------------------------------
# Armorer Specialty
# ---------------------------------------------------------------------------


def _armorer(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _specialty(
			ARMORER,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Tools_of_the_Trade_Armorer = _armorer(
		name="Tools of the Trade",
		min_level=3,
		description=(
			"You gain proficiency with Heavy armor and Smith's Tools. "
			"If you already have Smith's Tools proficiency, gain proficiency "
			"with one other Artisan's Tools of your choice."
			),
		)

Armorer_Spells = _armorer(
		name="Armorer Spells",
		min_level=3,
		description=(
			"Your research into armored combat unlocks extra spells "
			"always prepared: <i>Magic Missile, Thunderwave, Mirror "
			"Image, Shatter, Hypnotic Pattern, Lightning Bolt.</i> "
			"These don't count against your prepared spells."
			),
		)

Arcane_Armor = _armorer(
		name="Arcane Armor",
		min_level=3,
		description=(
			"As a Magic action with Smith's Tools in hand, turn a suit of "
			"armor you wear into Arcane Armor. Benefits while wearing it: "
			"ignore the Strength property; use it as a Spellcasting Focus; "
			"attach or detach it as a Bonus Action; it can't be removed "
			"against your will."
			),
		)

Armor_Model = _armorer(
		name="Armor Model",
		min_level=3,
		description=(
			"Choose a model for your Arcane Armor — <b>Guardian</b> "
			"or <b>Infiltrator</b>. You can change the model when "
			"you finish a Short or Long Rest.<br><b>Guardian.</b> "
			"Thunder Gauntlets (1d8 Thunder, Str-based; hit targets "
			"have Disadvantage on attacks against others until "
			"your next turn) and Defensive Field (Bonus Action: "
			"Temp HP = Artificer level; uses = Prof Bonus / Long Rest)."
			"<br><b>Infiltrator.</b> Lightning Launcher (ranged 1d6 "
			"Lightning, Dex-based; once per turn +1d6 Lightning on hit), "
			"Powered Steps (+5 ft Speed), Dampening Field (Advantage on "
			"Stealth checks)."
			),
		)

Extra_Attack_Armorer = _armorer(
		name="Extra Attack",
		min_level=5,
		description=(
			"You can attack twice, instead of once, whenever you take the "
			"Attack action on your turn."
			),
		)

Improved_Armorer = _armorer(
		name="Improved Armorer",
		min_level=9,
		description=(
			"Your Arcane Armor grows in power. Guardian: Defensive Field "
			"gives Temp HP equal to twice your Artificer level. Infiltrator: "
			"Lightning Launcher's bonus damage increases to 2d6. You can "
			"use your armor's special attacks with the Attack action, "
			"replacing one of your attacks."
			),
		)

Perfected_Armor = _armorer(
		name="Perfected Armor",
		min_level=15,
		description=(
			"<b>Guardian.</b> When you use Defensive Field, one "
			"creature within 60 feet receives the same Temp HP. "
			"You can also use a Reaction when hit to add your "
			"Intelligence modifier to your AC against that hit.<br>"
			"<b>Infiltrator.</b> Activate a Stealth device as a Bonus "
			"Action — you become Invisible until the start of your next "
			"turn. Uses: Proficiency Bonus per Long Rest."
			),
		)


# ---------------------------------------------------------------------------
# Artillerist Specialty
# ---------------------------------------------------------------------------


def _artillerist(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _specialty(
			ARTILLERIST,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Tools_of_the_Trade_Artillerist = _artillerist(
		name="Tools of the Trade",
		min_level=3,
		description=(
			"You gain proficiency with Woodworker's Tools. If you already "
			"have this proficiency, gain proficiency with one other "
			"Artisan's Tools of your choice."
			),
		)

Artillerist_Spells = _artillerist(
		name="Artillerist Spells",
		min_level=3,
		description=(
			"Your knowledge of battlefield magic unlocks extra "
			"spells always prepared: <i>Shield, Thunderwave, "
			"Scorching Ray, Shatter, Fireball, Wind Wall.</i> "
			"These don't count against your prepared spells."
			),
		)

Eldritch_Cannon = _artillerist(
		name="Eldritch Cannon",
		min_level=3,
		description=(
			"Using Woodworker's or Smith's Tools, take a Magic action to "
			"create a Small or Tiny Eldritch Cannon in an unoccupied space "
			"within 5 feet. It lasts 1 hour, until 0 HP, or until dismissed. "
			"Activate a cannon within 60 feet as a Bonus Action each turn."
			"<br><b>Flamethrower.</b> 15-ft Cone, 2d8 Fire, Dex save half."
			"<br><b>Force Ballista.</b> 120 ft, 2d8 Force, push target 5 ft."
			"<br><b>Protector.</b> You and allies within 10 ft gain 1d8 + "
			"Int Temp HP."
			),
		)

Arcane_Firearm = _artillerist(
		name="Arcane Firearm",
		min_level=5,
		description=(
			"Carve sigils into a wand, staff, rod, or ranged weapon with "
			"your Woodworker's Tools to make it your Arcane Firearm. "
			"It serves as a Spellcasting Focus, and when you cast a spell "
			"through it, roll 1d8 and add the result to one of the spell's "
			"damage rolls."
			),
		)

Explosive_Cannon = _artillerist(
		name="Explosive Cannon",
		min_level=9,
		description=(
			"Every Eldritch Cannon you create deals 1d8 more damage. "
			"As a Magic action within 60 feet of it, you can command it to "
			"detonate: each creature within 20 feet makes a Dex saving throw "
			"— fail: 3d8 Force damage; success: half."
			),
		)

Fortified_Position = _artillerist(
		name="Fortified Position",
		min_level=15,
		description=(
			"You and your allies have Half Cover while within 10 feet of "
			"an Eldritch Cannon you create. You can also create two cannons "
			"simultaneously with the same Magic action (each must be a "
			"different type)."
			),
		)


# ---------------------------------------------------------------------------
# Battle Smith Specialty
# ---------------------------------------------------------------------------


def _battle_smith(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		):
	return _specialty(
			BATTLE_SMITH,
			name=name,
			min_level=min_level,
			description=description,
			chips=chips,
			)


Tools_of_the_Trade_Battle_Smith = _battle_smith(
		name="Tools of the Trade",
		min_level=3,
		description=(
			"You gain proficiency with Martial weapons and Smith's Tools. "
			"If you already have Smith's Tools proficiency, gain proficiency "
			"with one other Artisan's Tools of your choice."
			),
		)

Battle_Smith_Spells = _battle_smith(
		name="Battle Smith Spells",
		min_level=3,
		description=(
			"Your martial artifice unlocks extra spells always "
			"prepared: <i>Heroism, Shield, Branding Smite, "
			"Warding Bond, Aura of Vitality, Conjure Barrage.</i> "
			"These don't count against your prepared spells."
			),
		)

Battle_Ready = _battle_smith(
		name="Battle Ready",
		min_level=3,
		description=(
			"Your combat training and arcane knowledge fuse into a cohesive "
			"whole. When you attack with a magic weapon, you can use your "
			"Intelligence modifier instead of Strength or Dexterity for the "
			"attack and damage rolls."
			),
		)

Steel_Defender = _battle_smith(
		name="Steel Defender",
		min_level=3,
		description=(
			"Your tinkering produces a loyal mechanical companion — the "
			"Steel Defender. It is friendly to you and your allies, obeys "
			"your commands, and acts on your initiative. If it dies, "
			"you can rebuild it using Smith's Tools over a Long Rest. "
			"Its statistics use your Proficiency Bonus and scale with your "
			"Artificer level."
			),
		)

Extra_Attack_Battle_Smith = _battle_smith(
		name="Extra Attack",
		min_level=5,
		description=(
			"You can attack twice, instead of once, whenever you take the "
			"Attack action on your turn."
			),
		)

Arcane_Jolt = _battle_smith(
		name="Arcane Jolt",
		min_level=9,
		description=(
			"When you or your Steel Defender hit a target "
			"with a magic weapon attack, you can channel "
			"magical energy through the strike for one effect:"
			"<br><b>Healing.</b> One creature or object within "
			"30 feet of the target restores 2d6 Hit Points."
			"<br><b>Lightning Strike.</b> The target takes "
			"an extra 2d6 Lightning damage and can't take "
			"Reactions until the start of its next turn."
			"<br>Uses: Intelligence modifier per Long Rest (minimum 1)."
			),
		)

Improved_Defender = _battle_smith(
		name="Improved Defender",
		min_level=15,
		description=(
			"Arcane Jolt damage and healing both increase to <b>4d6</b>. "
			"Your Steel Defender gains a +2 bonus to AC. Whenever your "
			"Steel Defender uses its Deflect Attack, the attacker takes "
			"1d4 + your Intelligence modifier Force damage."
			),
		)
