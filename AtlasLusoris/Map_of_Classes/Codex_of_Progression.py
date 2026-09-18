'''Atlas Lusoris : Map of Classes:  Codex of Progression '''

''' Cartography '''
from typing import List
from AtlasActorLudi.Map_of_Scores import Modifier
from AtlasLusoris.Grimoire_of_Features import Feature




class Progression:
	def __init__(self, character):
		self.char = character

	def features(self) -> List[Feature]:
		raise NotImplementedError


def get_class_progression(character):
	"""
	Return a Progression instance bound to this character.
	"""
	class_name = character.character_class
	from .  import (  # local import avoids circulars during top-level load
			Barbarian, Bard, Cleric, Druid, Fighter, Monk,
			Paladin, Ranger, Rogue, Sorcerer,
			#Warlock,
			#Wizard
			)
	from AtlasLusoris.Map_of_Classes.Training.Warlock import Warlock
	from AtlasLusoris.Map_of_Classes.Training.Wizard import Wizard
	from AtlasLusoris.Map_of_Classes.Training.Artificer import Artificer
	mapping = {
		"Fighter": 	Fighter,
		"Wizard":  	Wizard,
		"Barbarian": Barbarian,
		"Rogue": 	Rogue,
		"Paladin": 	Paladin,
		"Bard": 	Bard,
		"Druid": 	Druid,
		'Warlock': 	Warlock,
		'Monk': 	Monk,
		'Ranger': 	Ranger,
		'Sorcerer': 	Sorcerer,
		'Cleric': 	Cleric,
		'Artificer': 	Artificer,
		}
	prog_cls = mapping.get(class_name)
	return prog_cls(character)

def GetFeatures(character) -> List[Feature]:
	progression = get_class_progression(character)
	if progression:
		return progression.features()  # ✅ only one argument
	return []

def get_features(character):
	return GetFeatures(character)

