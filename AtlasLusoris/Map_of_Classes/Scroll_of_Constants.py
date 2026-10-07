# AtlasLusoris/Classes/data.py

def classes():
	return [
	'Fighter',	'Wizard',	'Rogue',	'Cleric',
	'Ranger',	'Paladin',	'Bard',		'Monk',
	'Druid',	'Warlock',	'Sorcerer',	'Barbarian',
	]

CLASSES = classes()

def subclasses():
	return {
	'Fighter': [
		"Champion", "Battle Master", "Eldritch Knight", "Samurai"],
	'Wizard': [
		"Evoker", "Illusion", "Necromancy", "Divination",
		"Abjuration",
		],
	'Rogue': [
		"Assassin",	 "Arcane Trickster", "Thief", "Swashbuckler",	],
	'Cleric': [
		"Knowledge", "War", "Tempest", "Life",
		"Light", "Trickery", "Nature", "Forge",
		"Grave", ],
	'Ranger': [
		"Hunter", "Beast Master", "Gloom Stalker",	"Horizon Walker" ],
	'Paladin': [
		"Devotion", "Oathbreaker", "Ancients",	 "Vengeance", ],
	'Bard': [
		"Dance",	"Glamour",		"Lore",	 "Valor",  ],
	'Monk': [
		"Elements", "Open Hand", "Shadow", "Mercy", ],
	'Druid': [
		"Moon", "Land", "Sea",	"Stars", ],
	'Warlock': [
		"Great Old One", "Fiend", "Archfey", "Celestial", ],
	'Sorcerer': [
		"Draconic",	"Wild Magic", "Divine Soul", "Shadow Magic", ],
	'Barbarian': [
		"Berserker", "Wild Heart", "Storm Herald", ],
	}

SUBCLASSES = subclasses()

def Archetype(char):
	if char == "Fighter":		return f"{char.subclass} League"
	if char == "Wizard":		return f"{char.subclass} School"
	if char == "Rogue":			return f"{char.subclass} Guild"
	if char == "Cleric":		return f"{char.subclass} Domain"
	if char == "Ranger":		return f"{char.subclass} Order"
	if char == "Paladin":		return f"Oath of {char.subclass}"
	if char == "Bard":			return f"College of {char.subclass}"
	if char == "Barbarian":		return f"Path of the {char.subclass}"
	if char == "Sorcerer":		return f"{char.subclass} Heritage"
	if char == "Warlock":		return f"Contract with the {char.subclass}"
	if char == "Druid":			return f"Circle of the {char.subclass}"
	if char == "Monk":			return f"Warrior of the {char.subclass}"
	return ""
