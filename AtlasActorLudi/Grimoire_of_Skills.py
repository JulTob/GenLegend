""" AtlasActorLudi.Grimoire of Skills """
"""
This Grimoire endows the bearer with a wide range of abilities,
capturing the essence of strength, agility, knowledge, perception,
and charisma.
Each skill can be enhanced through proficiency,
allowing for expertise and mastery in particular fields.
"""
try:
	from AtlasActorLudi.Map_of_Scores import Modifier
	from AtlasLudus.Map_of_Dice import Dice
except ImportError:
	raise

import app.random as random

class Skills:
	def __init__(Skillset, AS, ProficiencyBonus, proficient_skills=None, jack_of_all_trades=False):
		"""
		Initialize Skills with Ability Scores (AS), Proficiency Bonus (ProficiencyBonus),
		and an optional list of proficient skills.
		"""
		Skillset.proficient_skills = proficient_skills if proficient_skills else []

		Skillset.ProficiencyBonus = ProficiencyBonus
		# Jack of all trades
		Skillset.jack = jack_of_all_trades

		# Core skills by ability score categories
		Skillset.initialize_skills(AS)

	def initialize_skills(Skillset, AS):
		"""Define skill values with ability modifiers and proficiency status."""
		# STR
		Skillset.Athletics = Modifier(AS.STR) + Skillset.proficient()
		# DEX
		Skillset.Acrobatics =       Modifier(AS.DEX) + Skillset.proficient()
		Skillset.Sleight_of_Hand =  Modifier(AS.DEX) + Skillset.proficient()
		Skillset.Stealth =          Modifier(AS.DEX) + Skillset.proficient()
		# CON
		# INT
		Skillset.Arcana =           Modifier(AS.INT) + Skillset.proficient()
		Skillset.History =          Modifier(AS.INT) + Skillset.proficient()
		Skillset.Investigation =    Modifier(AS.INT) + Skillset.proficient()
		Skillset.Nature =           Modifier(AS.INT) + Skillset.proficient()
		Skillset.Religion =         Modifier(AS.INT) + Skillset.proficient()
		# WIS
		Skillset.Animal_Handling =  Modifier(AS.WIS) + Skillset.proficient()
		Skillset.Insight =          Modifier(AS.WIS) + Skillset.proficient()
		Skillset.Medicine =         Modifier(AS.WIS) + Skillset.proficient()
		Skillset.Perception =       Modifier(AS.WIS) + Skillset.proficient()
		Skillset.Survival =         Modifier(AS.WIS) + Skillset.proficient()
		# CHA
		Skillset.Deception =    Modifier(AS.CHA) + Skillset.proficient()
		Skillset.Intimidation = Modifier(AS.CHA) + Skillset.proficient()
		Skillset.Performance =  Modifier(AS.CHA) + Skillset.proficient()
		Skillset.Persuasion =   Modifier(AS.CHA) + Skillset.proficient()

	def proficient(Skillset):
		"""
		Apply proficiency bonus to a skill if proficient.
		This function simulates varying proficiency effects,
		allowing for random enhanced skill bonuses.
		"""
		if    Dice()==1:    return Dice(Skillset.ProficiencyBonus)
		elif  Dice(10)==1:  return Dice(Skillset.ProficiencyBonus,2)
		else:               return 0

	def string(Skillset, AS):
		'''
		Dictionary to hold skill names associated with their
		respective abilities
		'''
		skills_str = ""
		skills = {
			'Athletics': 	Skillset.Athletics,
			'Acrobatics': 	Skillset.Acrobatics,
			'Sleight of Hand': Skillset.Sleight_of_Hand,
			'Stealth': 	Skillset.Stealth,
			'Arcana': 	Skillset.Arcana,
			'History': 	Skillset.History,
			'Investigation': 	Skillset.Investigation,
			'Nature': 	Skillset.Nature,
			'Religion': Skillset.Religion,
			'Animal Handling': 	Skillset.Animal_Handling,
			'Insight': 	Skillset.Insight,
			'Medicine': Skillset.Medicine,
			'Perception': 	Skillset.Perception,
			'Survival': 	Skillset.Survival,
			'Deception': 	Skillset.Deception,
			'Intimidation': Skillset.Intimidation,
			'Performance': 	Skillset.Performance,
			'Persuasion': 	Skillset.Persuasion
		}

		# Only display skills with modified proficiency values
		for skill_name, skill_mod in skills.items():
			base_modifier = (getattr(AS, skill_name.replace(" ", "_").upper(), 0))
			#Inform(f"🩷base modifier:{base_modifier}, {type(base_modifier)}")
			base_modifier = Modifier(int(base_modifier))
			#Inform(f"❤️base modifier:{base_modifier}, {type(base_modifier)}")
			if skill_mod != base_modifier:
				skills_str += f"{skill_name}:\t{skill_mod:+}\n"
		return skills_str
		# Legacy. Check first thet the top works
		'''
		if not(Skillset.Athletics == Modifier(AS.STR)):
			skills_str += f"Athletics:\t{Skillset.Athletics:+}\n"

		if not(Skillset.Acrobatics == Modifier(AS.DEX)):
			skills_str += f"Acrobatics:\t{Skillset.Acrobatics:+}\n"
		if not(Skillset.Sleight_of_Hand == Modifier(AS.DEX)):
			skills_str += f"Sleight of Hand:\t{Skillset.Sleight_of_Hand:+}\n"
		if not(Skillset.Stealth == Modifier(AS.DEX)):
			skills_str += f"Stealth:\t{Skillset.Stealth:+}\n"

		if not(Skillset.Arcana == Modifier(AS.INT)):
			skills_str += f"Arcana:\t{Skillset.Arcana:+}\n"
		if not(Skillset.History == Modifier(AS.INT)):
			skills_str += f"History:\t{Skillset.History:+}\n"
		if not(Skillset.Investigation == Modifier(AS.INT)):
			skills_str += f"Investigation:\t{Skillset.Investigation:+}\n"
		if not(Skillset.Nature == Modifier(AS.INT)):
			skills_str += f"Nature:\t{Skillset.Nature:+}\n"
		if not(Skillset.Religion == Modifier(AS.INT)):
			skills_str += f"Religion:\t{Skillset.Religion:+}\n"

		if not(Skillset.Animal_Handling == Modifier(AS.WIS)):
			skills_str += f"Animal Handling:\t{Skillset.Animal_Handling:+}\n"
		if not(Skillset.Insight == Modifier(AS.WIS)):
			skills_str += f"Insight:\t{Skillset.Insight:+}\n"
		if not(Skillset.Medicine == Modifier(AS.WIS)):
			skills_str += f"Medicine:\t{Skillset.Medicine:+}\n"
		if not(Skillset.Perception == Modifier(AS.WIS)):
			skills_str += f"Perception:\t{Skillset.Perception:+}\n"
		if not(Skillset.Survival == Modifier(AS.WIS)):
			skills_str += f"Survival:\t{Skillset.Survival:+}\n"

		if not(Skillset.Deception == Modifier(AS.CHA)):
			skills_str += f"Deception:\t{Skillset.Deception:+}\n"
		if not(Skillset.Intimidation == Modifier(AS.CHA)):
			skills_str += f"Intimidation:\t{Skillset.Intimidation:+}\n"
		if not(Skillset.Performance == Modifier(AS.CHA)):
			skills_str += f"Performance:\t{Skillset.Performance:+}\n"
		if not(Skillset.Persuasion == Modifier(AS.CHA)):
			skills_str += f"Persuasion:\t{Skillset.Persuasion:+}\n"
		return skills_str
		'''

	def Passive(Skillset,skill):
		return 10+skill


class Skill:
	def __init__(self,
		name,
		ability_score,
		ProficiencyBonus=2,
		proficiency_level=0,
		jack_of_all_trades=False):

		"""
		Initialize a Skill.

		Parameters:
		- name: Name of the skill (string).
		- ability_score: The ability score associated with the skill (integer).
		- proficiency_level: 0 = not proficient, 1 = proficient, 2 = expertise.
		"""

		self.name = name
		self.ability_score = ability_score
		self.proficiency_level = proficiency_level
		self.ProficiencyBonus = ProficiencyBonus
		self.jack = jack_of_all_trades
		self.flat_bonus = 0

	def set_proficiency(self):
		"""Set the skill as proficient."""
		if self.proficiency_level < 1:
			self.proficiency_level = 1

	def set_expertise(self):
		"""Set the skill as having expertise."""
		self.proficiency_level = 2

	def remove_proficiency(self):
		"""Remove proficiency or expertise from the skill."""
		self.proficiency_level = 0

	def calculate_modifier(self):
		"""
		Calculate the total skill modifier.

		Parameters:
		- proficiency_bonus: The character's proficiency bonus (integer).

		Returns:
		- Total skill modifier (integer).
		"""
		base = Modifier(self.ability_score)
		if self.proficiency_level >= 1:
			base += self.ProficiencyBonus
		if self.proficiency_level >= 2:
			base += self.ProficiencyBonus
		if self.proficiency_level == 0 and self.jack:
			# Jack of All Trades adds half PB only to a check that adds no PB
			# (2024).  The flag is set before Backgrounds and Feats train their
			# skills, so a trained skill may still carry it (QST-0125).
			base = base + (self.ProficiencyBonus//2)
		flat = int(
			getattr(
				self,
				"flat_bonus",
				0,
				) or 0
			)
		if flat:
			base = base + flat
		return base

	def update_ability_score(self, new_score: int):
		"""Keep the ability score in sync with the character sheet."""
		self.ability_score = int(new_score)

	def calculate_ability_modifier(self):
		"""Calculate the ability modifier from the ability score."""
		return (self.ability_score - 10) // 2

	def modifier(self):
		return self.calculate_modifier()

	def is_proficient(self):
		if self.proficiency_level > 0:
			return True
		else:
			return False

	def __repr__(self):
		"""String representation of the Skill."""
		return (f"{self.name}: Ability Score = {self.ability_score}, "
				f"Proficiency Level = {self.proficiency_level}")

class Tool(Skill):
	def __init__(self, name, proficiency_level=0):
		"""
		Initialize a Tool.

		Parameters:
		- name: Name of the tool (string).
		- ability_score: The ability score associated with the tool (integer).
		- proficiency_level:
			0 = not proficient,
			1 = proficient,
			2 = expertise.
		"""
		super().__init__(name, ability_score=0, proficiency_level=proficiency_level)

	def modifier(self,ProficiencyBonus):
		if self.proficiency_level == 1:
			return 1
		elif self.proficiency_level == 2:
			return 2
		else:
			return 0
		return

	def calculate_modifier(self, proficiency_bonus):
		return modifier(proficiency_bonus)


class Weapon(Tool):
	def __init__(self, name, proficiency_level=0):
		"""
		Initialize a Weapon proficiency, inheriting from Tool.
		"""
		super().__init__(name, proficiency_level)

class Armor(Tool):
	def __init__(self, name, proficiency_level=0):
		"""
		Initialize an Armor proficiency, inheriting from Tool.
		"""
		super().__init__(name, proficiency_level)



class Char_Skills:
	def __init__(self, character=None, AS=None, ProficiencyBonus=None, proficient_skills=None):
		"""
		Initialize Char_Skills with Ability Scores (AS), Proficiency Bonus (ProficiencyBonus),
		and optional lists of proficient and expertise skills.

		Parameters:
		- AS: An AbilityScores instance with attributes STR, DEX, CON, INT, WIS, CHA.
		- PB: Proficiency Bonus (integer).
		- proficient_skills: List of skill names the character is proficient in.
		- expertise_skills: List of skill names the character has expertise in.
		"""
		# QST-0016.2 threading, completed to the suite's contract: the
		# character leads the signature; keyword callers are unaffected.
		self.character = character
		self.ProficiencyBonus = ProficiencyBonus

		# STR
		self.Athletics = Skill('Athletics', AS.STR, ProficiencyBonus)

		# DEX
		self.Acrobatics = Skill('Acrobatics', AS.DEX, ProficiencyBonus)
		self.Sleight_of_Hand = Skill('Sleight of Hand', AS.DEX, ProficiencyBonus)
		self.Stealth = Skill('Stealth', AS.DEX, ProficiencyBonus)
		# CON
		# INT
		self.Arcana = Skill('Arcana', AS.INT, ProficiencyBonus)
		self.History = Skill('History', AS.INT, ProficiencyBonus)
		self.Investigation = Skill('Investigation', AS.INT, ProficiencyBonus)
		self.Nature = Skill('Nature', AS.INT, ProficiencyBonus)
		self.Religion = Skill('Religion', AS.INT, ProficiencyBonus)

		# WIS
		self.Animal_Handling = Skill('Animal Handling', AS.WIS, ProficiencyBonus)
		self.Insight = Skill('Insight', AS.WIS, ProficiencyBonus)
		self.Medicine = Skill('Medicine', AS.WIS, ProficiencyBonus)
		self.Perception = Skill('Perception', AS.WIS, ProficiencyBonus)
		self.Survival = Skill('Survival', AS.WIS, ProficiencyBonus)
		# CHA
		self.Deception = Skill('Deception', AS.CHA, ProficiencyBonus)
		self.Intimidation = Skill('Intimidation', AS.CHA, ProficiencyBonus)
		self.Performance = Skill('Performance', AS.CHA, ProficiencyBonus)
		self.Persuasion = Skill('Persuasion', AS.CHA, ProficiencyBonus)

		# Tools: one attribute per tool in ToolsKit's catalog, a kind (Musical
		# Instrument, Gaming Set) standing for all its variants, and every old
		# name the same object as the tool it became (QST-0116).  The sheet
		# keeps no list of its own.
		from AtlasInventarium.ToolsKit import (
			Sheet_Tool_Aliases,
			Sheet_Tool_Attributes,
			)

		for attribute, name in Sheet_Tool_Attributes():
			setattr(self, attribute, Tool(name))

		for alias, attribute in Sheet_Tool_Aliases():
			setattr(self, alias, getattr(self, attribute))

		# Weapons
		self.Simple_Weapons = Weapon('Simple Weapons')
		self.Martial_Weapons = Weapon('Martial Weapons')
		self.Hand_Crossbow = Weapon('Hand Crossbow')
		self.Rapier = Weapon('Rapier')
		self.Shortsword = Weapon('Shortsword')
		self.Finesse = Weapon('Finesse Weapons')
		self.Light_Weapons = Weapon('Light Weapons')

		# Armor
		self.Shields = Armor('Shields')
		self.Light = Armor('Light Armor')
		self.Medium = Armor('Medium Armor')
		self.Heavy = Armor('Heavy Armor')
		self.Unarmed_Monk = Armor('Unarmed Defense')
		self.Unarmed_Barb = Armor('Unarmed Defense')
		self.Unarmed_Dance = Armor('Unarmed Defense')

	@property
	def list(self):
		return [
			(self.Athletics,         "Athletics (STR)"),
			(self.Acrobatics,        "Acrobatics (DEX)"),
			(self.Sleight_of_Hand,   "Sleight of Hand (DEX)"),
			(self.Stealth,           "Stealth (DEX)"),
			(self.Arcana,            "Arcana (INT)"),
			(self.History,           "History (INT)"),
			(self.Investigation,     "Investigation (INT)"),
			(self.Nature,            "Nature (INT)"),
			(self.Religion,          "Religion (INT)"),
			(self.Animal_Handling,   "Animal Handling (WIS)"),
			(self.Insight,           "Insight (WIS)"),
			(self.Medicine,          "Medicine (WIS)"),
			(self.Perception,        "Perception (WIS)"),
			(self.Survival,          "Survival (WIS)"),
			(self.Deception,         "Deception (CHA)"),
			(self.Intimidation,      "Intimidation (CHA)"),
			(self.Performance,       "Performance (CHA)"),
			(self.Persuasion,        "Persuasion (CHA)"),
			]

	def sync_with_abilities(self, AS):
		"""Refresh every skill so later stat boosts update the modifier."""
		mapping = {
			"Athletics": "STR",
			"Acrobatics": "DEX",
			"Sleight_of_Hand": "DEX",
			"Stealth": "DEX",
			"Arcana": "INT",
			"History": "INT",
			"Investigation": "INT",
			"Nature": "INT",
			"Religion": "INT",
			"Animal_Handling": "WIS",
			"Insight": "WIS",
			"Medicine": "WIS",
			"Perception": "WIS",
			"Survival": "WIS",
			"Deception": "CHA",
			"Intimidation": "CHA",
			"Performance": "CHA",
			"Persuasion": "CHA",
		}
		for attr, ability_key in mapping.items():
			skill = getattr(self, attr, None)
			if skill is not None:
				skill.update_ability_score(getattr(AS, ability_key))

	def get_all_weapons(self):
		return [
			self.Simple_Weapons,
			self.Martial_Weapons,
			self.Hand_Crossbow,
			self.Rapier,
			self.Shortsword,
			self.Finesse,
			self.Light_Weapons,
			# Add other weapons here...
			]

	def get_proficient_weapons(self):
		"""
		Returns a list of proficient weapons only.
		"""
		all_weapons = self.get_all_weapons()

		return [weapon for weapon in all_weapons if weapon.proficiency_level > 0]

	def get_all_armors(self):
		return [
			self.Shields,
			self.Light,
			self.Medium,
			self.Heavy,
			self.Unarmed_Monk,
			self.Unarmed_Barb,
			self.Unarmed_Dance,
			]

	def get_proficient_armors(self):
		"""
		Returns a list of proficient armors only.
		"""
		all_armors = self.get_all_armors()

		return [armor for armor in all_armors if armor.proficiency_level > 0]

	def set_proficient(self, skill_name):
		"""Set a skill as proficient."""
		skill = self._get_skill(skill_name)
		skill.set_proficiency()

	def set_expertise(self, skill_name):
		"""Set a skill as having expertise."""
		skill = self._get_skill(skill_name)
		skill.set_expertise()

	def remove_proficiency(self, skill_name):
		"""Remove proficiency or expertise from a skill."""
		skill = self._get_skill(skill_name)
		skill.remove_proficiency()

	def get_skill_modifier(self, skill_name):
		skill = self._get_skill(skill_name)
		return skill.calculate_modifier()

	def passive(self, skill_name):
		"""
		Calculate the passive score for a given skill.

		Parameters:
		- skill_name: Name of the skill (string).

		Returns:
		- Passive score (integer).
		"""
		return 10 + self.get_skill_modifier(skill_name)

	def _get_skill(self, skill_name):
		"""Retrieve a Skill instance by name."""
		if not hasattr(self, skill_name):
			raise ValueError(f"Skill '{skill_name}' does not exist.")
		return getattr(self, skill_name)

	def __repr__(self):
		"""String representation of all skills and their states."""
		skills = [
			self.Athletics, self.Acrobatics, self.Sleight_of_Hand, self.Stealth,
			self.Arcana, self.History, self.Investigation, self.Nature, self.Religion,
			self.Animal_Handling, self.Insight, self.Medicine, self.Perception,
			self.Survival, self.Deception, self.Intimidation, self.Performance, self.Persuasion
		]
		return '\n'.join([str(skill) for skill in skills])

	def Passive(self,skill,ProficiencyBonus):
		return 10+skill.modifier(ProficiencyBonus)

	def activate_proficiencies(self, n, skill_names):
			"""
			Activates proficiency in `n` skills from the provided skill_list.
			"""
			# ----- nothing to do? bail out early -----
			if n <= 0 or not skill_names:
				return
			# Randomly pick a skill from the list
			s = random.choice(skill_names)

			if s == "Athletics":
				if self.Athletics.proficiency_level < 1:
					self.Athletics.proficiency_level = 1  # Or call self.Athletics.set_proficient()
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)


			elif s == "Acrobatics":
				if self.Acrobatics.proficiency_level < 1:
					self.Acrobatics.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Sleight of Hand":
				if self.Sleight_of_Hand.proficiency_level < 1:
					self.Sleight_of_Hand.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Stealth":
				if self.Stealth.proficiency_level < 1:
					self.Stealth.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Arcana":
				if self.Arcana.proficiency_level < 1:
					self.Arcana.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "History":
				if self.History.proficiency_level < 1:
					self.History.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Investigation":
				if self.Investigation.proficiency_level < 1:
					self.Investigation.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Nature":
				if self.Nature.proficiency_level < 1:
					self.Nature.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Religion":
				if self.Religion.proficiency_level < 1:
					self.Religion.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Animal Handling":
				if self.Animal_Handling.proficiency_level < 1:
					self.Animal_Handling.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Insight":
				if self.Insight.proficiency_level < 1:
					self.Insight.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Medicine":
				if self.Medicine.proficiency_level < 1:
					self.Medicine.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Survival":
				if self.Survival.proficiency_level < 1:
					self.Survival.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Perception":
				if self.Perception.proficiency_level < 1:
					self.Perception.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Deception":
				if self.Deception.proficiency_level < 1:
					self.Deception.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Intimidation":
				if self.Intimidation.proficiency_level < 1:
					self.Intimidation.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Persuasion":
				if self.Persuasion.proficiency_level < 1:
					self.Persuasion.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Performance":
				if self.Performance.proficiency_level < 1:
					self.Performance.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)


			elif s == "Thieves' Tools":
				if self.Thieves_Tools.proficiency_level < 1:
					self.Thieves_Tools.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Disguise Kit":
				if self.Disguise_Kit.proficiency_level < 1:
					self.Disguise_Kit.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)

			elif s == "Alchemist's Supplies":
				if self.Alchemist_Supplies.proficiency_level < 1:
					self.Alchemist_Supplies.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Brewer's Supplies":
				if self.Brewer_Supplies.proficiency_level < 1:
					self.Brewer_Supplies.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)
			elif s == "Calligrapher's Supplies":
				if self.Calligrapher_Supplies.proficiency_level < 1:
					self.Calligrapher_Supplies.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)

			elif s in ("Cartographer's Tools", "Navigator's Tools"):
				if self.Cartographer_Tools.proficiency_level < 1:
					self.Cartographer_Tools.proficiency_level = 1
					skill_names.remove(s)
					return self.activate_proficiencies(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_proficiencies(n,skill_names)


			skill_names.remove(s)
			n -= 1
			self.activate_proficiencies(n, skill_names)

	def activate_expertise(self, n, skill_names):
		# ----- nothing to do? bail out early (mirrors activate_proficiencies;
		# the recursion ends on an empty list, which must not reach choice) -----
		if n <= 0 or not skill_names:
			return
		# Randomly pick a skill from the list
		s = random.choice(skill_names)

		if n>0 and skill_names:
			if s == "Athletics":
				if self.Athletics.proficiency_level < 2:
					self.Athletics.proficiency_level = 2  # Or call self.Athletics.set_proficient()
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)


			elif s == "Acrobatics":
				if self.Acrobatics.proficiency_level < 2:
					self.Acrobatics.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Sleight of Hand":
				if self.Sleight_of_Hand.proficiency_level < 2:
					self.Sleight_of_Hand.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Stealth":
				if self.Stealth.proficiency_level < 2:
					self.Stealth.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Arcana":
				if self.Arcana.proficiency_level < 2:
					self.Arcana.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "History":
				if self.History.proficiency_level < 2:
					self.History.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Investigation":
				if self.Investigation.proficiency_level < 2:
					self.Investigation.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Nature":
				if self.Nature.proficiency_level < 2:
					self.Nature.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Religion":
				if self.Religion.proficiency_level < 2:
					self.Religion.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Animal Handling":
				if self.Animal_Handling.proficiency_level < 2:
					self.Animal_Handling.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Insight":
				if self.Insight.proficiency_level < 2:
					self.Insight.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Medicine":
				if self.Medicine.proficiency_level < 2:
					self.Medicine.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Survival":
				if self.Survival.proficiency_level < 2:
					self.Survival.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Perception":
				if self.Perception.proficiency_level < 2:
					self.Perception.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Deception":
				if self.Deception.proficiency_level < 2:
					self.Deception.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Intimidation":
				if self.Intimidation.proficiency_level < 2:
					self.Intimidation.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)
			elif s == "Persuasion":
				if self.Persuasion.proficiency_level < 2:
					self.Persuasion.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)
			elif s == "Performance":
				if self.Performance.proficiency_level < 2:
					self.Performance.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)


			elif s == "Thieves' Tools":
				if self.Thieves_Tools.proficiency_level < 2:
					self.Thieves_Tools.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)
			elif s == "Disguise Kit":
				if self.Disguise_Kit.proficiency_level < 2:
					self.Disguise_Kit.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s == "Alchemist's Supplies":
				if self.Alchemist_Supplies.proficiency_level < 2:
					self.Alchemist_Supplies.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)
			elif s == "Brewer's Supplies":
				if self.Brewer_Supplies.proficiency_level < 2:
					self.Brewer_Supplies.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)
			elif s == "Calligrapher's Supplies":
				if self.Calligrapher_Supplies.proficiency_level < 2:
					self.Calligrapher_Supplies.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)

			elif s in ("Cartographer's Tools", "Navigator's Tools"):
				if self.Cartographer_Tools.proficiency_level < 2:
					self.Cartographer_Tools.proficiency_level = 2
					skill_names.remove(s)
					return self.activate_expertise(n-1,skill_names)
				else:
					skill_names.remove(s)
					return self.activate_expertise(n,skill_names)


			skill_names.remove(s)
			n -= 1
			self.activate_expertise(n, skill_names)

	def get_proficient_skills(self):
		"""
		Return a list of skill names (the actual name attribute) where proficiency_level is 1 or greater.
		"""
		proficient_skills = []

		# Loop through all attributes of Char_Skills
		for skill_obj in vars(self).values():
			# Check if it's a Skill object and has proficiency level >= 1
			if isinstance(skill_obj, Skill) and skill_obj.proficiency_level == 1:
				if not isinstance(skill_obj, Tool):
					proficient_skills.append(skill_obj.name)  # Use the skill's actual name attribute

		return proficient_skills

	def activate_jack_of_all_trades(self):
		"""
		Activate Jack of All Trades for all skills by setting the `jack` attribute to True
		in skills that are not proficient.
		"""
		for skill in self.get_all_skills():
			if skill.proficiency_level == 0:
				# Only apply to non-proficient skills
				skill.jack = True

	def get_all_skills(self):
		"""
		Return a list of all skill objects.
		"""
		return [
			self.Athletics,
			self.Acrobatics ,
			self.Sleight_of_Hand ,
			self.Stealth,
			self.Arcana ,
			self.History ,
			self.Investigation ,
			self.Nature,
			self.Religion,
			self.Animal_Handling,
			self.Insight,
			self.Medicine,
			self.Perception,
			self.Survival,
			self.Deception,
			self.Intimidation ,
			self.Performance,
			self.Persuasion ,
		]

def get_other_proficiencies(skills, character=None):
	from AtlasInventarium.ToolsKit import Tool_Proficiency_Names

	# 1. tools, each instrument and game by name: the Character's training
	# ledger knows which (ToolsKit reads it); the sheet alone knows only kinds.
	result = list(
		Tool_Proficiency_Names(
			character
			if character is not None
			else getattr(skills, "character", None),
			skills,
			)
		)
	# 2. add weapon proficiencies (avoid duplicates)
	for wpn in skills.get_proficient_weapons():
		if wpn.name not in result:
			result.append(wpn.name)
	# 3. add armour proficiencies
	for arm in skills.get_proficient_armors():
		if arm.name not in result:
			result.append(arm.name)

	return result
