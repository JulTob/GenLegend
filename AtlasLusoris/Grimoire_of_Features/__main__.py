"""Run the Grimoire_of_Features self-test beside the package.

    python -m AtlasLusoris.Grimoire_of_Features

Ruling 8 (Dialog 0027, QST-0144.6): every choice a legacy Feat makes draws
from the Character's Dice Bag, opened with the purpose named by the Tag that
offers it.  This proves the purposes opened are exactly the declared ones and
that the pools are what they were.
"""

from random import Random

from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
from AtlasActorLudi.Grimoire_of_Skills import Char_Skills
from AtlasActorLudi.Map_of_Scores import PB
from AtlasLusoris.Grimoire_of_Features import (
		ApplyEpicBoon,
		ApplyRandomFeats,
		Blessed_Warrior_Cantrips,
		BoonEnergyResistance,
		BoonSkill,
		BoonSpellRecall,
		BuildAvailableBoon,
		BuildAvailableFeats,
		Druidic_Warrior_Cantrips,
		Fighting_Styles,
		_ability_to_increase,
		add_new_fighting_style,
		character_fighting_styles,
		)


DECLARED_PURPOSES = frozenset(
		{
				"General_Feat.choice",
				"Epic_Boon.choice",
				"Fighting_Style.choice",
				"Blessed_Warrior.cantrips",
				"Druidic_Warrior.cantrips",
				"Boon_of_Skill.expertise",
				"Boon_of_Spell_Recall.ability",
				"Boon_of_Energy_Resistance.damage_types",
				"Boon_of_Combat_Prowess.ability",
				"Boon_of_Dimensional_Travel.ability",
				"Boon_of_Energy_Resistance.ability",
				"Boon_of_Fate.ability",
				"Boon_of_Fortitude.ability",
				"Boon_of_Recovery.ability",
				"Boon_of_Skill.ability",
				"Boon_of_Speed.ability",
				"Boon_of_the_Night_Spirit.ability",
				"Boon_of_Truesight.ability",
				}
		)

DAMAGE_TYPES = {
		"Acid", "Cold", "Fire", "Lightning", "Necrotic",
		"Poison", "Psychic", "Radiant", "Thunder",
		}

GUILDS = (
		"Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
		"Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
		)


class Probe:
	"""A Character stand-in with the fields the legacy feats read."""

	def __init__(
			probe,
			*tags,
			level=19,
			scores=(15, 14, 13, 12, 10, 8),
			seed=7,
			):
		probe.tags = set(
				tags
				)
		probe.level = level
		probe.seed = seed
		probe.abilities = AbilityScores(
				*scores
				)
		probe.skills = Char_Skills(
				AS=probe.abilities,
				ProficiencyBonus=PB(
						level
						),
				)
		probe.features = []
		probe.speed = 30
		probe.base_health = 100
		probe.opened = []

	def __contains__(
			probe,
			name,
			):
		return name in probe.tags

	def Dice_Bag(
			probe,
			purpose,
			):
		probe.opened.append(
				purpose
				)
		return Random(
				f"{probe.seed}|{purpose}"
				)


def scores_of(
		probe,
		):
	return {
			key: getattr(
					probe.abilities,
					key,
					)
			for key in ("STR", "DEX", "CON", "INT", "WIS", "CHA")
			}


def test_ability_to_increase() -> None:
	#-- the highest odd score below the cap wins; ties break from the bag
	probe = Probe(
			"Fighter",
			)
	assert _ability_to_increase(
			probe,
			dice=Random(
					1
					),
			) == "STR"
	tied = Probe(
			"Fighter",
			scores=(15, 15, 12, 12, 10, 8),
			)
	assert _ability_to_increase(
			tied,
			dice=Random(
					3
					),
			) == Random(
			3
			).choice(
			["STR", "DEX"]
			)
	even = Probe(
			"Fighter",
			scores=(16, 14, 12, 12, 10, 8),
			)
	assert _ability_to_increase(
			even,
			dice=Random(
					1
					),
			) == "STR"
	assert even.opened == [], "a bag handed in is not reopened"


def test_general_feats() -> None:
	#-- one bag, General_Feat.choice, over the pool BuildAvailableFeats gives
	probe = Probe(
			"Fighter",
			level=4,
			)
	pool = [
			feat.name
			for feat in BuildAvailableFeats(
					probe
					)
			]
	chosen = ApplyRandomFeats(
			probe,
			n=1,
			)
	assert probe.opened == ["General_Feat.choice"], probe.opened
	assert len(
			chosen
			) == 1 and chosen[0].name in pool, (chosen, pool)
	assert scores_of(
			probe
			) != scores_of(
			Probe(
					"Fighter",
					level=4,
					)
			), "the feat raised a score"
	again = Probe(
			"Fighter",
			level=4,
			)
	assert ApplyRandomFeats(
			again,
			n=1,
			)[0].name == chosen[0].name, "the same Character takes the same feat"
	assert Random(
			"7|General_Feat.choice"
			).sample(
			pool,
			1,
			) == [chosen[0].name]


def test_epic_boons() -> None:
	#-- Epic_Boon.choice over the pool BuildAvailableBoon gives; every boon
	#-- of every Guild applies from its own declared bags
	for guild in GUILDS:
		probe = Probe(
				guild,
				)
		pool = [
				boon.name
				for boon in BuildAvailableBoon(
						probe
						)
				]
		chosen = ApplyEpicBoon(
				probe,
				n=1,
				)
		assert "Epic_Boon.choice" in probe.opened, probe.opened
		assert set(
				probe.opened
				) <= DECLARED_PURPOSES, set(
				probe.opened
				) - DECLARED_PURPOSES
		assert chosen[0].name in pool and chosen[0] in probe.features
		for boon in BuildAvailableBoon(
				Probe(
						guild,
						)
				):
			fresh = Probe(
					guild,
					)
			before = sum(
					scores_of(
							fresh
							).values()
					)
			boon(
					fresh
					)
			assert set(
					fresh.opened
					) <= DECLARED_PURPOSES, (boon.name, fresh.opened)
			assert sum(
					scores_of(
							fresh
							).values()
					) == before + 1, boon.name


def test_boon_bags() -> None:
	#-- Boon of Skill: all skills, one Expertise from Boon_of_Skill.expertise
	probe = Probe(
			"Rogue",
			)
	BoonSkill()(
			probe
			)
	assert probe.opened == ["Boon_of_Skill.expertise", "Boon_of_Skill.ability"], probe.opened
	doubled = [
			skill.name
			for skill in probe.skills.get_all_skills()
			if skill.proficiency_level == 2
			]
	assert len(
			doubled
			) == 1, doubled
	assert all(
			skill.proficiency_level >= 1
			for skill in probe.skills.get_all_skills()
			)

	#-- Boon of Spell Recall: INT, WIS or CHA from Boon_of_Spell_Recall.ability
	probe = Probe(
			"Wizard",
			)
	before = scores_of(
			probe
			)
	BoonSpellRecall()(
			probe
			)
	assert probe.opened == ["Boon_of_Spell_Recall.ability"], probe.opened
	raised = [
			key
			for key, value in scores_of(
					probe
					).items()
			if value != before[key]
			]
	assert raised == [
			Random(
					"7|Boon_of_Spell_Recall.ability"
					).choice(
					["INT", "WIS", "CHA"]
					)
			], raised

	#-- Boon of Energy Resistance: two damage types drawn when the boon is
	#-- built, from Boon_of_Energy_Resistance.damage_types, the same each time
	probe = Probe(
			"Monk",
			)
	boon = BoonEnergyResistance(
			probe
			)
	assert probe.opened == ["Boon_of_Energy_Resistance.damage_types"], probe.opened
	named = [
			damage
			for damage in DAMAGE_TYPES
			if f"{damage} and " in boon.description or f"and {damage} damage" in boon.description
			]
	assert len(
			named
			) == 2, boon.description
	assert BoonEnergyResistance(
			Probe(
					"Monk",
					)
			).description == boon.description


def test_fighting_styles() -> None:
	#-- the Paladin's Blessed Warrior text names the cantrips of one bag,
	#-- Blessed_Warrior.cantrips, the same on every reading
	paladin = Probe(
			"Paladin",
			level=2,
			)
	styles = Fighting_Styles(
			paladin
			)
	cantrips = Blessed_Warrior_Cantrips(
			paladin
			)
	assert set(
			paladin.opened
			) == {"Blessed_Warrior.cantrips"}, paladin.opened
	assert "Blessed Warrior" in styles and "Druidic Warrior" not in styles
	assert all(
			str(
					cantrip
					) in styles["Blessed Warrior"]
			for cantrip in cantrips
			), (cantrips, styles["Blessed Warrior"])
	assert Blessed_Warrior_Cantrips(
			paladin
			) == cantrips

	#-- the Ranger's Druidic Warrior likewise, from Druidic_Warrior.cantrips
	ranger = Probe(
			"Ranger",
			level=2,
			)
	styles = Fighting_Styles(
			ranger
			)
	assert set(
			ranger.opened
			) == {"Druidic_Warrior.cantrips"}, ranger.opened
	assert "Druidic Warrior" in styles and "Blessed Warrior" not in styles
	assert all(
			str(
					cantrip
					) in styles["Druidic Warrior"]
			for cantrip in Druidic_Warrior_Cantrips(
					ranger
					)
			)

	#-- the style learned comes from Fighting_Style.choice over the styles
	#-- not yet owned; a second call cannot return the first style again
	fighter = Probe(
			"Fighter",
			level=1,
			)
	first = add_new_fighting_style(
			fighter
			)
	assert fighter.opened == ["Fighting_Style.choice"], fighter.opened
	assert first.name in Fighting_Styles(
			fighter
			)
	assert first.name == Random(
			"7|Fighting_Style.choice"
			).choice(
			list(
					Fighting_Styles(
							fighter
							)
					)
			)
	fighter.features.append(
			first
			)
	assert character_fighting_styles(
			fighter
			) == {first.name}
	second = add_new_fighting_style(
			fighter
			)
	assert second.name != first.name

	#-- a Paladin who draws Blessed Warrior is granted the cantrips the text
	#-- names: the same bag, no second draw
	for seed in range(
			64
			):
		paladin = Probe(
				"Paladin",
				level=2,
				seed=seed,
				)
		feat = add_new_fighting_style(
				paladin
				)
		if feat.name != "Blessed Warrior":
			continue
		paladin.known_spells = []
		feat(
				paladin
				)
		assert paladin.known_spells == Blessed_Warrior_Cantrips(
				paladin
				), paladin.known_spells
		assert set(
				paladin.opened
				) == {"Blessed_Warrior.cantrips", "Fighting_Style.choice"}
		break
	else:
		raise AssertionError(
				"no seed below 64 drew Blessed Warrior"
				)


def main() -> None:
	test_ability_to_increase()
	test_general_feats()
	test_epic_boons()
	test_boon_bags()
	test_fighting_styles()
	print(
			"OK - Grimoire_of_Features: every legacy feat draws from the Dice Bag its Tag names."
			)


if __name__ == "__main__":
	main()
