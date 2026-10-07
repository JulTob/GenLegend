from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
	Feature,
	add_new_fighting_style,
	ApplyRandomFeats,
	ApplyEpicBoon
	)


class Ranger(Progression):
	def __init__(self, character):
		self.char = character

	def features(self, character=None):
		if character is None:
			character = self.char
		else:
			self.char = character

		level = character.Level
		from AtlasLusoris.GuildKit import Specialization_Choices

		subclass = (
			character.Subclass
			or character.Pick(
				Specialization_Choices("Ranger"),
				dice=character.Dice_Bag(
					"training.ranger.archetype",
					version="2024",
					namespace="GenLegendRanger",
					),
				)
			)
		#character.Subclass = subclass
		features = []
		favored_enemy = 2
		if level >= 5: favored_enemy += 1
		if level >= 9: favored_enemy += 1
		if level >= 13: favored_enemy += 1
		if level >= 17: favored_enemy += 1
		# --- Core Ranger Features ---
		if level >= 1:
			roll_health(character)

			features.append(Feature("Favored Enemy",
				f"""You always have the <i>Hunter’s Mark</i> spell prepared. You can cast it {favored_enemy} times without a spell slot, regaining all uses on a Long Rest."""))

			features.append(Feature("Weapon Mastery",
				"""You can use the mastery properties of 2 weapons of your choice. You may change them after a Long Rest."""))

		if level >= 2:
			#-- Deft Explorer is the Deft_Explorer lesson's (AtlasOfTraining/
			#-- Map_of_Ranger_Training): its Expertise and its two languages,
			#-- from Deft_Explorer.languages (QST-0144.10).
			fs = add_new_fighting_style(self.char, level=2)
			features.append(fs or Feature("Fighting Style",
				"""Choose a Fighting Style or the Druidic Warrior option for 2 cantrips.""" ))

		if level >= 3:
			features.append(Feature(f"{subclass} Archetype",
				f"You adopt the {subclass} specialization."))

			if subclass == "Beast Master":
				features.append(Feature("Primal Companion",
				"""Summon a magical beast that obeys your commands. You can change it after each Long Rest.""" ))

			if subclass == "Fey Wanderer":
				features.append(Feature("Dreadful Strikes",
					"""Once per turn, deal +1d4 Psychic damage on a hit. Increases to 1d6 at level 11.""" ))
				features.append(Feature("Fey Spells",
					"""You always have these spells prepared: <i>Charm Person (3rd), Misty Step (5th), Summon Fey (9th), Dimension Door (13th), Mislead (17th)</i>.""" ))
				features.append(Feature("Otherworldly Glamour",
					"""Gain a bonus to Charisma checks equal to your Wisdom modifier. Gain proficiency in Deception, Performance, or Persuasion.""" ))

			if subclass == "Gloom Stalker":
				features.append(Feature("Dread Ambusher",
					"""+10 ft speed on first turn. +2d6 Psychic on first hit each turn. Add WIS to initiative.""" ))
				features.append(Feature("Umbral Sight",
					"""Gain 60 ft Darkvision, or extend your existing. You're Invisible in darkness to creatures with Darkvision.""" ))
				features.append(Feature("Gloom Spells",
					"""Always have prepared: <i>Disguise Self (3rd), Rope Trick (5th), Fear (9th), Greater Invisibility (13th), Seeming (17th)</i>.""" ))

			if subclass == "Hunter":
				features.append(Feature("Hunter's Prey",
					"""Choose Colossus Slayer (+1d8 vs wounded) or Horde Breaker (bonus hit vs adjacent). You can change it after a rest.""" ))
				features.append(Feature("Hunter’s Lore",
					"""While a creature is marked by Hunter’s Mark, you learn any Immunities, Resistances, or Vulnerabilities it has.""" ))

		if level >= 4:
			features.extend(ApplyRandomFeats(character, n=1, level=4))

		if level >= 5:
			features.append(Feature("Extra Attack",
				"""You can attack twice when taking the Attack action.""" ))

		if level >= 6:
			features.append(Feature("Roving",
				"""+10 ft speed while not in heavy armor. Gain Swim and Climb speeds equal to your base speed.""" ))

		if level >= 7:
			if subclass == "Beast Master":
				features.append(Feature("Exceptional Training",
					"""Your beast can Dash, Disengage, Dodge, or Help as part of your Bonus Action. It can also deal Force damage.""" ))

			if subclass == "Fey Wanderer":
				features.append(Feature("Beguiling Twist",
					"""When a creature within 120 ft resists Charmed/Frightened, you can use your Reaction to force another save on a different creature.""" ))

			if subclass == "Gloom Stalker":
				features.append(Feature("Iron Mind",
					"""Gain proficiency in WIS saves. If already proficient, gain INT or CHA saves instead.""" ))

			if subclass == "Hunter":
				features.append(Feature("Defensive Tactics",
					"""Choose one: <b>Escape the Horde</b> (disadv. on OA vs you) or <b>Multiattack Defense</b> (disadv. after hit). Can switch after a rest.""" ))

		if level >= 8:
			features.extend(ApplyRandomFeats(character, n=1, level=8))

		if level >= 9:
			features.append(Feature("Expertise",
				"""Choose 2 skills you know and gain Expertise in them.""" ))

		if level >= 10:
			features.append(Feature("Tireless",
				"""Use a Magic Action to gain 1d8 + WIS Temp HP (min 1), usable WIS mod times/day. Also reduce 1 Exhaustion on Short Rest.""" ))

		if level >= 11:
			if subclass == "Beast Master":
				features.append(Feature("Bestial Fury",
					"""Your beast can use its Strike twice, and deals bonus damage to targets marked by Hunter's Mark.""" ))

			if subclass == "Fey Wanderer":
				features.append(Feature("Fey Reinforcements",
					"""You can cast Summon Fey without material component. Once/day cast it without slot. Optionally make it non-concentration (1 min).""" ))

			if subclass == "Gloom Stalker":
				features.append(Feature("Stalker's Flurry",
					"""Your Dreadful Strike deals 2d8. On use, choose: <b>Sudden Strike</b> (bonus attack) or <b>Mass Fear</b> (AoE frighten).""" ))

			if subclass == "Hunter":
				features.append(Feature("Superior Hunter’s Prey",
					"""When you damage a creature marked by Hunter's Mark, you may apply the extra damage to a different creature within 30 ft.""" ))

		if level >= 12:
			features.extend(ApplyRandomFeats(character, n=1, level=12))

		if level >= 13:
			features.append(Feature("Relentless Hunter",
				"""Taking damage doesn't break your concentration on Hunter's Mark.""" ))

		if level >= 14:
			features.append(Feature("Nature’s Veil",
				"""Bonus Action: become Invisible until end of next turn. Usable WIS mod times/day.""" ))

		if level >= 15:
			if subclass == "Beast Master":
				features.append(Feature("Share Spells",
					"""When casting a spell on yourself, your beast is also affected if within 30 ft.""" ))

			if subclass == "Fey Wanderer":
				features.append(Feature("Misty Wanderer",
					"""Misty Step WIS mod/day. When you cast it, bring a willing adjacent creature along.""" ))

			if subclass == "Gloom Stalker":
				features.append(Feature("Shadowy Dodge",
					"""When attacked, use Reaction to impose Disadvantage. Then teleport up to 30 ft.""" ))

			if subclass == "Hunter":
				features.append(Feature("Superior Hunter’s Defense",
					"""When taking damage, you may use a Reaction to gain Resistance to it and to all damage of same type until end of turn.""" ))

		if level >= 16:
			features.extend(ApplyRandomFeats(character, n=1, level=16))

		if level >= 17:
			features.append(Feature("Precise Hunter",
				"""Gain Advantage on attacks vs the creature marked by your Hunter’s Mark.""" ))

		if level >= 18:
			features.append(Feature("Feral Senses",
				"""You gain 30 ft Blindsight.""" ))

		if level >= 19:
			features.extend(ApplyEpicBoon(character))

		if level >= 20:
			features.append(Feature("Foe Slayer", 
				"""Your Hunter's Mark deals 1d10 damage instead of 1d6.""" ))

		return features


if __name__ == "__main__":
	#-- Self-test (QST-0144.10).  The legacy block prints no Deft Explorer
	#-- of its own: the lesson grants its two languages, so a level-5
	#-- Ranger knows Common, the two creation languages and the pair, five
	#-- in all, and the lesson recorded the pair.
	import contextlib
	import io
	from AtlasActorLudi.Map_of_Character_Generation import summon_player

	with contextlib.redirect_stdout(
			io.StringIO()
			), contextlib.redirect_stderr(
			io.StringIO()
			):
		ranger = summon_player(
				guild="Ranger",
				level=5,
				seed=7,
				)
	known = ranger.languages.langs
	assert "Common" in known, known
	assert len( known ) == 5, known
	first, second = ranger.language_feature_grants[ "Deft Explorer" ]
	assert {first, second} <= known and first != second, (first, second)
	print(
			"OK: the legacy Ranger block grants no language; the Deft_Explorer "
			f"lesson knows {first} and {second}."
			)
