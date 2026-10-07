import random

try:
	from AtlasLudus.Map_of_Dice import Dice
except ImportError:
	raise
	#-- The old non-player tree (AtlasAlusoris.Map_of_NPC) was imported here
	#-- and never used: the Player path does not load it (QST-0144.8, .10).

def add_language(languages, language, chance=100, INT=0):
	"""Try to add a language based on a dice roll and chance."""
	if chance <= 1 and language not in languages:		languages.append(language)
	elif Dice(chance-INT) <= 1 and language not in languages:
		languages.append(language)

def Language(npc):
	"""
	The language : chance to know the language, as 1 out of "number"
	Represents the population's average chance of one element knowing
		the language.
	Substracting the inteligence modifier of the npc represents a
		higher (or lower) chance of knowing more languages than the average.
	"""
	race = npc.race
	archetype = npc.archetype
	INT = npc.ability_scores.int_mod
	if race == "":
		race = "base"
	if archetype == "":
		archetype = "base"

	languages = []


	if race == "base":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 	20,
			"Giant": 	20,
			"Gnomish": 	20,
			"Goblin": 	20,
			"Halfling": 20,
			"Orc": 		20,
			"Abyssal": 	20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 	20,
			"Undercommon": 20,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

	if race == "Human":
		langs = {
			"Common": 1,
			"Dwarvish": 7,
			"Elvish": 7,
			"Giant": 7,
			"Gnomish": 7,
			"Goblin":7,
			"Halfling": 7,
			"Orc": 7,
			"Abyssal": 25,
			"Celestial": 25,
			"Draconic": 25,
			"Deep Speech": 25,
			"Infernal": 25,
			"Primordial": 25,
			"Sylvan": 20,
			"Undercommon": 25,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

	if race == "Aberration":
		langs = {
			"Common": 6,
			"Dwarvish": 19,
			"Elvish": 21,
			"Giant": 15,
			"Gnomish": 26,
			"Goblin": 13,
			"Halfling": 26,
			"Orc": 11,
			"Abyssal": 10,
			"Celestial": 10,
			"Draconic": 21,
			"Deep Speech": 1,
			"Infernal": 10,
			"Primordial": 26,
			"Sylvan": 50,
			"Undercommon": 3,
			"Telepathy (60 ft.) ": 11,
			}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Aven":
		langs = {
			"Common": 4,
			"Dwarvish": 26,
			"Elvish": 10,
			"Giant": 21,
			"Gnomish": 26,
			"Goblin": 26,
			"Halfling": 16,
			"Orc": 26,
			"Abyssal": 26,
			"Celestial": 7,
			"Draconic": 7,
			"Deep Speech": 100,
			"Infernal": 100,
			"Primordial": 4,
			"Sylvan": 1,
			"Undercommon": 100,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Beast":
		langs = {
			"Common": 4,
			"Beastly Speech":1,
			"Dwarvish": 20,
			"Elvish": 10,
			"Giant": 20,
			"Gnomish": 10,
			"Goblin": 10,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 10,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 10,
			"Sylvan": 2,
			"Undercommon": 20,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Beastfolk":
		langs = {
			"Common": 3,
			"Beastly Speech":3,
			"Dwarvish": 25,
			"Elvish": 8,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 15,
			"Celestial": 15,
			"Draconic": 10,
			"Deep Speech": 200,
			"Infernal": 15,
			"Primordial": 10,
			"Sylvan": 1,
			"Undercommon": 15,
			f"Beast Telepathy: The {npc.race} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":3,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Catfolk":
		langs = {
			"Common": 5,
			"Dwarvish": 20,
			"Elvish": 	15,
			"Giant": 	20,
			"Gnomish": 	20,
			"Goblin": 	20,
			"Halfling": 25,
			"Orc": 		20,
			"Abyssal": 	15,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 15,
			"Primordial": 15,
			"Sylvan": 	1,
			"Undercommon": 5,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Celestial":
		langs = {
			"Common": 1,
			"Dwarvish": 11,
			"Elvish": 9,
			"Giant": 11,
			"Gnomish": 11,
			"Goblin": 11,
			"Halfling": 11,
			"Orc": 11,
			"Abyssal": 9,
			"Celestial": 1,
			"Draconic": 11,
			"Deep Speech": 22,
			"Infernal": 10,
			"Primordial": 25,
			"Sylvan": 7,
			"Undercommon": 22,
			"Understands All languages":10,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

		if Dice(2)>1: add_language(languages, "Telepathy (60 feet)", 8)
		elif Dice(2)>1: add_language(languages, "Telepathy (120 feet)", 10)
	if race == "Construct":
		add_language(languages, "Understands the languages of its creator.", 1)
		add_language(languages, "Understands All languages.", 5)
	if race == "Dragon":
		langs = {
			"Common": 1,
			"Dwarvish": 8,
			"Elvish": 9,
			"Giant": 8,
			"Gnomish": 20,
			"Goblin": 15,
			"Halfling": 20,
			"Orc": 8,
			"Abyssal": 10,
			"Celestial": 15,
			"Draconic": 1,
			"Deep Speech": 12,
			"Infernal": 8,
			"Primordial": 10,
			"Sylvan": 5,
			"Undercommon": 10,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Dwarf":
		langs = {
			"Common": 1,
			"Dwarvish": 1,
			"Elvish": 10,
			"Giant": 8,
			"Gnomish": 17,
			"Goblin": 19,
			"Halfling": 10,
			"Orc": 22,
			"Abyssal": 21,
			"Celestial": 19,
			"Draconic": 14,
			"Deep Speech": 12,
			"Infernal": 14,
			"Primordial": 12,
			"Sylvan": 25,
			"Undercommon": 5,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Elf":
		langs = {
			"Common": 1,
			"Dwarvish": 6,
			"Elvish": 1,
			"Giant": 12,
			"Gnomish": 6,
			"Goblin": 18,
			"Halfling": 12,
			"Orc": 20,
			"Abyssal": 8,
			"Celestial": 8,
			"Draconic": 8,
			"Deep Speech": 16,
			"Infernal": 8,
			"Primordial": 6,
			"Sylvan": 4,
			"Undercommon": 6,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Elemental":
		values = [1, 20, 20, 20]
		random.shuffle(values)
		aq, ter, ign, aur = values
		langs = {
			"Common": 5,
			"Dwarvish": 8,
			"Elvish": 8,
			"Giant": 8,
			"Gnomish": 8,
			"Goblin": 18,
			"Halfling": 18,
			"Orc": 12,
			"Abyssal": 12,
			"Celestial": 12,
			"Draconic": 12,
			"Deep Speech": 20,
			"Infernal": 12,
			"Primordial": 1,
			"Sylvan": 4,
			"Undercommon": 10,
			"Ignan": ign,
			"Terran":ter,
			"Aquan": aq,
			"Auran": aur,
		}
		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Fey":
		langs = {
			"Common": 3,
			"Dwarvish": 14,
			"Elvish": 3,
			"Giant": 10,
			"Gnomish": 8,
			"Goblin": 4,
			"Halfling": 16,
			"Orc": 16,
			"Abyssal": 16,
			"Celestial": 16,
			"Draconic": 8,
			"Deep Speech": 20,
			"Infernal": 16,
			"Primordial": 8,
			"Sylvan": 1,
			"Undercommon": 20,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Fiend":
		langs = {
			"Common": 1,
			"Dwarvish": 4,
			"Elvish": 4,
			"Giant": 8,
			"Gnomish": 4,
			"Goblin": 2,
			"Halfling": 12,
			"Orc": 4,
			"Abyssal": 2,
			"Celestial": 25,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 2,
			"Primordial": 22,
			"Sylvan": 20,
			"Undercommon": 8,
			"Telepathy (60 ft.)": 10,
			}
		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Giant":
		langs = {
			"Common": 5,
			"Dwarvish": 4,
			"Elvish": 20,
			"Giant": 1,
			"Gnomish": 8,
			"Goblin": 8,
			"Halfling": 20,
			"Orc": 8,
			"Abyssal": 12,
			"Celestial": 12,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 12,
			"Primordial": 16,
			"Sylvan": 8,
			}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Gnome":
		langs = {
			"Common": 1,
			"Dwarvish": 3,
			"Elvish": 3,
			"Giant": 3,
			"Gnomish": 1,
			"Goblin": 6,
			"Halfling": 6,
			"Orc": 10,
			"Abyssal": 12,
			"Celestial": 12,
			"Draconic": 12,
			"Deep Speech": 12,
			"Infernal": 12,
			"Primordial": 12,
			"Sylvan": 4,
			"Undercommon": 12,
			}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Goblin":
		langs = {
			"Common": 	4 ,
			"Dwarvish": 20 ,
			"Elvish": 	16 ,
			"Giant": 	18 ,
			"Gnomish": 	18 ,
			"Goblin": 	1,
			"Halfling": 18 ,
			"Orc": 		6  ,
			"Abyssal": 	14 ,
			"Celestial":  20 ,
			"Draconic":   14 ,
			"Deep Speech": 14 ,
			"Infernal":   14 ,
			"Primordial": 20 ,
			"Sylvan": 4 ,
			"Undercommon": 4 ,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Halfling":
		langs = {
			"Common": 1,
			"Dwarvish": 4,
			"Elvish": 4,
			"Giant": 20,
			"Gnomish": 4,
			"Goblin": 20,
			"Halfling": 1,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 4,
			"Draconic": 6,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 18,
			"Sylvan": 18,
			"Undercommon": 20
			}
		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Kobold":
		langs = {
			"Common": 4,
			"Dwarvish": 8,
			"Elvish": 20,
			"Giant": 25,
			"Gnomish": 40,
			"Goblin": 10,
			"Halfling": 20,
			"Orc": 18,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 1,
			"Deep Speech": 20,
			"Infernal": 10,
			"Primordial": 22,
			"Sylvan": 14,
			"Undercommon": 3,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Lizardfolk":
		langs = {
			"Common": 4,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 10,
			"Gnomish": 20,
			"Goblin": 10,
			"Halfling": 20,
			"Orc": 4,
			"Abyssal": 4,
			"Celestial": 20,
			"Draconic": 1,
			"Deep Speech": 4,
			"Infernal": 4,
			"Primordial": 4,
			"Sylvan": 4,
			"Undercommon": 20,
			f"Beast Telepathy (Only Reptiles): The {npc.race} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":3,

		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Monstrosity":
		langs = {
			"Common": 6,
			"Dwarvish": 10,
			"Elvish": 22,
			"Giant": 9,
			"Gnomish": 25,
			"Goblin": 11,
			"Halfling": 22,
			"Orc": 7,
			"Abyssal": 4,
			"Celestial": 22,
			"Draconic": 6,
			"Deep Speech": 1,
			"Infernal": 5,
			"Primordial": 12,
			"Sylvan": 9,
			"Undercommon": 1
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Ooze":
		add_language(languages, "Telepathy (60 ft.)", 1)
	if race == "Orc":
		langs = {
			"Common": 1,
			"Dwarvish": 12,
			"Elvish": 12,
			"Giant": 4,
			"Gnomish": 22,
			"Goblin": 2,
			"Halfling": 22,
			"Orc": 1,
			"Abyssal": 8,
			"Celestial": 8,
			"Draconic": 8,
			"Deep Speech": 22,
			"Infernal": 8,
			"Primordial": 8,
			"Sylvan": 8,
			"Undercommon": 8,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Plant":
		langs = {
			"Common": 		2 ,
			"Dwarvish": 	22,
			"Elvish": 		6 ,
			"Giant": 		22,
			"Gnomish": 		18,
			"Goblin": 		18,
			"Halfling": 	25,
			"Orc": 			22,
			"Abyssal": 		24,
			"Celestial": 	8 ,
			"Draconic": 	22,
			"Deep Speech": 	22,
			"Infernal": 	22,
			"Primordial": 	1 ,
			"Sylvan": 		1,
			"Undercommon": 	8 ,
			"Telepathy": 	5 ,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Snakefolk":
		langs = {
			"Common": 	5,
			"Dwarvish": 21,
			"Elvish": 	20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 21,
			"Halfling": 21,
			"Orc": 20,
			"Abyssal": 6,
			"Celestial": 20,
			"Draconic": 1,
			"Deep Speech": 6,
			"Infernal": 12,
			"Primordial": 6,
			"Sylvan": 9,
			"Undercommon": 20,
			f"Beast Telepathy (Only Snakes): The {npc.race} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":3,

		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Undead":
		langs = {
			"Common": 	3,
			"Dwarvish": 18,
			"Elvish": 18,
			"Giant": 20,
			"Gnomish": 18,
			"Goblin": 16,
			"Halfling": 18,
			"Orc": 18,
			"Abyssal": 12,
			"Celestial": 12,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 12,
			"Primordial": 100,
			"Sylvan": 100,
			"Undercommon": 15,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if race == "Vampire":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 	15,
			"Giant": 	20,
			"Gnomish": 	20,
			"Goblin": 	20,
			"Halfling": 20,
			"Orc": 		20,
			"Abyssal": 	5,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 10,
			"Infernal": 5,
			"Primordial": 20,
			"Sylvan": 	5,
			"Undercommon": 5,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

	# BACKGROUNDS
	if archetype == "base":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20,
			}
		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

	if archetype == "Druid":
		langs = {
			"Common": 1,
			"Druidic":1,
			"Dwarvish": 20,
			"Elvish": 5,
			"Giant": 20,
			"Gnomish": 10,
			"Goblin": 10,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 16,
			"Draconic": 4,
			"Deep Speech": 21,
			"Infernal": 20,
			"Primordial": 4,
			"Sylvan": 3,
			"Undercommon": 20,
			f"Beast Telepathy: {npc.title} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":3,
			}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Bandit":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Bard":
		langs = {
			"Common": 1,
			"Dwarvish": 6,
			"Elvish": 6,
			"Giant": 20,
			"Gnomish": 6,
			"Goblin": 6,
			"Halfling": 6,
			"Orc": 6,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 6,
			"Undercommon": 20
		}
		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Berserker":
		langs = {
			"Common": 	5,
			"Dwarvish": 6,
			"Elvish": 	20,
			"Giant": 	6,
			"Gnomish": 	20,
			"Goblin": 	20,
			"Halfling": 20,
			"Orc": 		6,
			"Abyssal": 	12,
			"Celestial": 	20,
			"Draconic": 	16,
			"Deep Speech": 	16,
			"Infernal": 	12,
			"Primordial": 	16,
			"Sylvan": 		20,
			"Undercommon": 	6,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Charlatan":
		langs = {
			"Common": 1,
			"Dwarvish": 6,
			"Elvish": 6,
			"Giant": 20,
			"Gnomish": 6,
			"Goblin": 6,
			"Halfling": 6,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Cultist":
		langs = {
			"Common": 3,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 8,
			"Celestial": 8,
			"Draconic": 8,
			"Deep Speech": 8,
			"Infernal": 8,
			"Primordial": 8,
			"Sylvan": 20,
			"Undercommon": 8,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Criminal":
		langs = {
			"Common": 5,
			"Thieve's Cant":1,
			"Dwarvish": 12,
			"Elvish": 12,
			"Giant": 20,
			"Gnomish": 12,
			"Goblin": 12,
			"Halfling": 12,
			"Orc": 12,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 4,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Expert":
		langs = {
			"Common": 1,
			"Dwarvish": 5,
			"Elvish": 5,
			"Giant": 5,
			"Gnomish": 5,
			"Goblin": 19,
			"Halfling": 19,
			"Orc": 19,
			"Abyssal": 19,
			"Celestial": 6,
			"Draconic": 19,
			"Deep Speech": 19,
			"Infernal": 19,
			"Primordial": 19,
			"Sylvan": 19,
			"Undercommon": 19,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Explorer":
		langs = {
			"Common": 1,
			"Dwarvish": 4,
			"Elvish": 4,
			"Giant": 4,
			"Gnomish": 4,
			"Goblin": 4,
			"Halfling": 4,
			"Orc": 4,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 4,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Fighter":
		langs = {
			"Common": 20,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 15,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 15,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 15,
			"Undercommon": 15,
			}
		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

	if archetype == "Healer":
		langs = {
			"Common": 5,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 10,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 4,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 4,
			"Sylvan": 4,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Hero":
		langs = {
			"Common": 2,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 6,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Hunter":
		langs = {
			"Common": 10,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 6,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 6,
			"Sylvan": 1,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Knight":
		langs = {
			"Common": 2,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 6,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Mage":
		langs = {
			"Common": 3,
			"Dwarvish": 6,
			"Elvish": 6,
			"Giant": 6,
			"Gnomish": 6,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 6,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 6,
			"Infernal": 6,
			"Primordial": 6,
			"Sylvan": 6,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Monk":
		langs = {
			"Common": 5,
			"Dwarvish": 10,
			"Elvish": 10,
			"Giant": 10,
			"Gnomish": 10,
			"Goblin": 10,
			"Halfling": 10,
			"Orc": 10,
			"Abyssal": 10,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 10,
			"Infernal": 10,
			"Primordial": 6,
			"Sylvan": 10,
			"Undercommon": 10,
			f"Beast Telepathy: The {npc.race} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":10,

		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Noble":
		langs = {
			"Common": 1,
			"Dwarvish": 6,
			"Elvish": 6,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 12,
			"Draconic": 12,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Priest":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 6,
			"Celestial": 6,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 6,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Pirate":
		langs = {
			"Common": 1,
			"Thieve's Cant": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 12,
			"Infernal": 20,
			"Primordial": 12,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Ranger":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 4,
			"Giant": 4,
			"Gnomish": 20,
			"Goblin": 4,
			"Halfling": 20,
			"Orc": 4,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 6,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 6,
			"Sylvan": 6,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Scholar":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 6,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 6,
			"Infernal": 6,
			"Primordial": 6,
			"Sylvan": 6,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Shaman":
		langs = {
			"Common": 5,
			"Druidic":1,
			"Dwarvish": 20,
			"Elvish": 6,
			"Giant": 6,
			"Gnomish": 20,
			"Goblin": 6,
			"Halfling": 20,
			"Orc": 6,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 8,
			"Sylvan": 1,
			"Undercommon": 20,
			f"Beast Telepathy: The {npc.race} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":10,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Spy":
		langs = {
			"Common": 1,
			"Thieve's Cant":1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Traveler":
		langs = {
			"Common": 1,
			"Dwarvish": 5,
			"Elvish": 5,
			"Giant": 5,
			"Gnomish": 5,
			"Goblin": 5,
			"Halfling": 5,
			"Orc": 5,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 12,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Prankster":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Warrior":
		langs = {
			"Common": 2,
			"Dwarvish": 6,
			"Elvish": 6,
			"Giant": 6,
			"Gnomish": 6,
			"Goblin": 6,
			"Halfling": 6,
			"Orc": 6,
			"Abyssal": 20,
			"Celestial": 20,
			"Draconic": 20,
			"Deep Speech": 20,
			"Infernal": 20,
			"Primordial": 20,
			"Sylvan": 20,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Warlock":
		langs = {
			"Common": 4,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 20,
			"Gnomish": 20,
			"Goblin": 20,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 6,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 6,
			"Infernal": 6,
			"Primordial": 6,
			"Sylvan": 6,
			"Undercommon": 20
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)
	if archetype == "Witch":
		langs = {
			"Common": 1,
			"Dwarvish": 20,
			"Elvish": 20,
			"Giant": 12,
			"Gnomish": 20,
			"Goblin": 6,
			"Halfling": 20,
			"Orc": 20,
			"Abyssal": 6,
			"Celestial": 6,
			"Draconic": 6,
			"Deep Speech": 6,
			"Infernal": 6,
			"Primordial": 6,
			"Sylvan": 12,
			"Undercommon": 20,
			f"Beast Telepathy: The {npc.race} can magically command any animal it shares an affinity to within 120 feet of it, using a limited telepathy.":10,
		}

		for lang, chance in langs.items():
			add_language(languages, lang, chance,INT)

	languages = [lang.strip() for lang in languages if lang.strip()]
		# Remove any empty strings and strip whitespace
	if not languages: return "<i>Common</i>"
	return f"<i> {'<br> '.join(languages)} </i>"


COMMON = "Common"
	#-- Every Character knows Common (2024 PHB, Choose Languages).

STANDARD_FACES = {
		"Common Sign Language": 1,
		"Draconic": 1,
		"Dwarvish": 2,
		"Elvish": 2,
		"Giant": 1,
		"Gnomish": 1,
		"Goblin": 1,
		"Halfling": 2,
		"Orc": 1,
		}
	#-- The printed d12 of the 2024 Standard Languages table, as faces per
	#-- language (QST-0144.10).  Draconic is Standard since 2024.

SPECIES_TONGUE_FACES = 6
	#-- The faces a Character's own Species tongue adds to each creation
	#-- pick when that tongue is Standard: half a die, a nudge and not a
	#-- filter (Julio's ruling 1, QST-0144.10; Decree 0005).

standard_languages = frozenset(
		STANDARD_FACES
		)
rare_languages = frozenset(
		(
			"Abyssal",
			"Celestial",
			"Deep Speech",
			"Druidic",
			"Infernal",
			"Primordial",
			"Sylvan",
			"Thieves' Cant",
			"Undercommon",
			)
		)
all_languages = standard_languages | rare_languages
exotic_languages = rare_languages
	#-- The 2014 name of the Rare table, kept for the callers that read it.


class Linguistics:
	def __init__(lingua):
		lingua.langs = set()

	def Add(lingua, language):
		if language is None:
		    return
		    # Guard
		if isinstance(language, str):
			name = language.strip()
			if name:
				lingua.langs.add(name)
			return
		try:
			from collections.abc import Mapping, Iterable

			if isinstance(language, Mapping):
				iterable = language.keys()
			elif isinstance(language, Iterable):
				iterable = language
			else:
				iterable = (language,)

			for item in iterable:
				lingua.Add(item)

		except Exception:
			# Last resort: coerce to string
			lingua.langs.add(str(language))

	def AddAnyLanguage(
			lingua,
			langs=None,
			n=1,
			*,
			dice,
			):
		"""
		Learn n languages drawn from langs that lingua does not know yet.

		``dice`` is the Dice Bag the offering Tag opened for this grant
		(ruling 8, QST-0144.6): there is no draw without one.  The pool is
		sorted, so the answer depends on the bag alone and never on set
		order.  Returns the names learned, in the order drawn.
		"""
		if langs is None:
			langs = all_languages
		unknown = sorted(
				set( langs ) - lingua.langs
				)
		if not unknown or n <= 0:
			return ()
		k = min(
				n,
				len( unknown ),
				)
		chosen = tuple(
				dice.sample(
						unknown,
						k,
						)
				)
		lingua.langs |= set( chosen )
		return chosen

	def names(lingua):
		"""The known languages, sorted: what the sheet and the lore read."""
		return sorted( lingua.langs )

	def AsListHTML(linguistics):
		final = linguistics.langs
		if not final:
			return "<i>Common</i>"
		langs_html = "<br>".join(
				sorted(
						final
						)
				)
		return f"<i>{langs_html}</i>"

	def AsHTML(linguistics):
		return f"""
		<div class="npc-textbox">
		<h2>Languages</h2>
		{linguistics.AsListHTML()}
		</div>
		"""

	def __str__(linguistics):
		return linguistics.AsHTML()


def Linguistics_Of( char ):
	"""
	The Linguistics the Character holds, or None.

	Before Character_Languages ran, ``char.languages`` is nothing or the
	plain list an Origin Feat wrote; a lesson that grants a language asks
	here first and does nothing when there is no Linguistics yet.
	"""
	languages = getattr(
			char,
			"languages",
			None,
			)
	if isinstance(
			languages,
			Linguistics,
			):
		return languages
	return None


def Record_Language_Grant(
		char,
		feature,
		names,
		):
	"""
	Write which languages ``feature`` granted, so its Entry can name them.

	``char.language_feature_grants`` maps a feature's name to the list of
	languages it granted (Thieves' Cant, Deft Explorer).
	"""
	grants = getattr(
			char,
			"language_feature_grants",
			None,
			)
	if grants is None:
		grants = {}
		char.language_feature_grants = grants
	grants[ feature ] = list( names )
	return grants


def Species_Tongue( char ):
	"""
	The tongue the Character's Species declares as ``TONGUE``, or None.

	Each Species carries its tongue as plain class data in its own file
	(Elf Elvish, Dwarf Dwarvish, ...; Human none).  The Species Tag is the
	one the Character carries, read the way SpeciesKit reads it.
	"""
	from AtlasActorLudi.SpeciesKit.catalog import Current_Species
	species = Current_Species( char )
	return getattr(
			species,
			"TONGUE",
			None,
			)


def Creation_Faces( tongue ):
	"""
	The faces of the creation die: the printed d12, the Species tongue added.

	A Rare tongue (Infernal, Celestial) is not on the die and adds nothing.
	"""
	faces = dict( STANDARD_FACES )
	if tongue in faces:
		faces[ tongue ] += SPECIES_TONGUE_FACES
	return faces


def Creation_Languages(
		char,
		dice,
		):
	"""
	The two Standard languages a Character learns at creation.

	Each is one roll of the die of Creation_Faces, the Character's own
	Species tongue weighing SPECIES_TONGUE_FACES more when it is Standard;
	a roll that repeats the first language is rolled again, so the two are
	distinct.  Every roll comes from ``dice``, the bag the caller opened
	(``identity.languages``).  Returns the pair in the order rolled.
	"""
	faces = Creation_Faces(
			Species_Tongue( char )
			)
	names = sorted( faces )
	weights = [
			faces[ name ]
			for name in names
			]
	chosen = []
	while len( chosen ) < 2:
		[ name ] = dice.choices(
				names,
				weights=weights,
				k=1,
				)
		if name not in chosen:
			chosen.append( name )
	return tuple( chosen )


def Character_Languages( char ):
	"""
	Build the Linguistics of a Player and return it.

	1. Common, always.
	2. The two creation languages of Creation_Languages, rolled from the
	   Character's ``identity.languages`` Dice Bag.
	3. Fold in whatever language the Character already held: the ``langs``
	   of a Linguistics, or the plain list an Origin Feat wrote during the
	   background step (Agitator, Dragon Cult Initiate, the Dark Gifts), so
	   that nothing granted before this rite is wiped (QST-0144.10).

	Class languages (Thieves' Cant, Druidic, Deft Explorer) are not granted
	here: each lesson Tag grants its own, after this rite, and draws from
	its own bag.
	"""
	ling = Linguistics()
	ling.Add( COMMON )
	ling.Add(
			Creation_Languages(
					char,
					char.Dice_Bag( "identity.languages" ),
					)
			)
	prior = getattr(
			char,
			"languages",
			None,
			)
	ling.Add(
			getattr(
					prior,
					"langs",
					prior,
					)
			)
	return ling


if __name__ == "__main__":
	from random import Random
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit import Apply_Species

	#-- The tables are the 2024 ones: Draconic Standard, the two secret
	#-- tongues Rare and listed.
	assert sum( STANDARD_FACES.values() ) == 12, STANDARD_FACES
	assert "Draconic" in standard_languages
	assert {"Druidic", "Thieves' Cant"} <= rare_languages
	assert not standard_languages & rare_languages
	assert all_languages == standard_languages | rare_languages
	assert exotic_languages == rare_languages
	assert len( all_languages ) == 18, len( all_languages )

	#-- The Species tongue adds half a die, and only when it is Standard.
	assert Creation_Faces( "Elvish" )[ "Elvish" ] == 2 + SPECIES_TONGUE_FACES
	assert Creation_Faces( "Infernal" ) == STANDARD_FACES
	assert Creation_Faces( None ) == STANDARD_FACES

	opened = []
	original = Character.Dice_Bag

	def Recording_Dice_Bag(
			char,
			purpose,
			**key,
			):
		opened.append(
				(
					purpose,
					key,
					)
				)
		return original(
				char,
				purpose,
				**key,
				)

	def Skeleton(
			seed,
			species,
			):
		char = Character(
				seed=seed,
				)
		Apply_Species(
				char,
				species,
				)
		opened.clear()
			#-- The Species opened its own bags (heritage, lineage); only the
			#-- language rite's bag is under test.
		return char

	def Replay(
			char,
			tongue,
			):
		"""The two creation picks, rolled again by hand from a fresh bag."""
		faces = Creation_Faces( tongue )
		names = sorted( faces )
		weights = [
				faces[ name ]
				for name in names
				]
		bag = original(
				char,
				"identity.languages",
				)
		rolled = []
		while len( rolled ) < 2:
			[ name ] = bag.choices(
					names,
					weights=weights,
					k=1,
					)
			if name not in rolled:
				rolled.append( name )
		return rolled

	Character.Dice_Bag = Recording_Dice_Bag
	try:
		#-- An Elf reads Elvish from its Species; the two picks come from
		#-- identity.languages alone, with the default key, and replay.
		elf = Skeleton(
				seed=1,
				species="Elf",
				)
		assert Species_Tongue( elf ) == "Elvish"
		known = Character_Languages( elf )
		assert opened == [
				(
					"identity.languages",
					{},
					),
				], opened
		assert isinstance( known, Linguistics )
		assert COMMON in known.langs
		extra = known.langs - {COMMON}
		assert len( extra ) == 2 and extra <= standard_languages, extra
		assert extra == set(
				Replay(
						elf,
						"Elvish",
						)
				), extra

		#-- The same Character rolls the same languages again.
		opened.clear()
		assert Character_Languages( elf ).langs == known.langs

		#-- A Rare tongue (Tiefling: Infernal) and no tongue (Human) roll the
		#-- plain d12.
		tiefling = Skeleton(
				seed=1,
				species="Tiefling",
				)
		assert Species_Tongue( tiefling ) == "Infernal"
		assert Character_Languages( tiefling ).langs - {COMMON} == set(
				Replay(
						tiefling,
						None,
						)
				)
		human = Skeleton(
				seed=1,
				species="Human",
				)
		assert Species_Tongue( human ) is None
		assert Character_Languages( human ).langs - {COMMON} == set(
				Replay(
						human,
						None,
						)
				)

		#-- The nudge: over the same seeds, Elves know Elvish more often than
		#-- Humans do, and every Standard language stays possible for both.
		seeds = range( 1, 121 )
		elvish_elves = sum(
				"Elvish" in Character_Languages(
						Skeleton(
								seed=seed,
								species="Elf",
								)
						).langs
				for seed in seeds
				)
		elvish_humans = sum(
				"Elvish" in Character_Languages(
						Skeleton(
								seed=seed,
								species="Human",
								)
						).langs
				for seed in seeds
				)
		assert elvish_elves > elvish_humans, (elvish_elves, elvish_humans)
		assert elvish_elves < len( seeds ), "a nudge, not a filter"

		#-- A language written before the rite (an Origin Feat during the
		#-- background step) is folded in, from a plain list or a Linguistics.
		agitator = Skeleton(
				seed=1,
				species="Human",
				)
		agitator.languages = [ "Thieves' Cant" ]
		folded = Character_Languages( agitator )
		assert "Thieves' Cant" in folded.langs, folded.langs
		assert folded.langs - {"Thieves' Cant"} == Character_Languages( human ).langs
		agitator.languages = folded
		assert Character_Languages( agitator ).langs == folded.langs
	finally:
		Character.Dice_Bag = original

	#-- AddAnyLanguage draws from the sorted unknown pool, never repeats a
	#-- known language, stops at the pool, and has no draw without a bag.
	ling = Linguistics()
	ling.Add( COMMON )
	assert ling.AddAnyLanguage(
			{COMMON, "Elvish"},
			5,
			dice=Random( 1 ),
			) == ( "Elvish", )
	assert ling.langs == {COMMON, "Elvish"}, ling.langs
	learned = ling.AddAnyLanguage(
			all_languages,
			2,
			dice=Random( 7 ),
			)
	assert learned == tuple(
			Random( 7 ).sample(
					sorted( all_languages - {"Elvish"} ),
					2,
					)
			), learned
	assert ling.names() == sorted( ling.langs )
	try:
		ling.AddAnyLanguage( all_languages )
	except TypeError:
		pass
	else:
		raise AssertionError( "AddAnyLanguage drew without a bag" )

	#-- The helpers the lessons use.
	class Holder:
		pass

	holder = Holder()
	assert Linguistics_Of( holder ) is None
	holder.languages = [ "Draconic" ]
	assert Linguistics_Of( holder ) is None
	holder.languages = ling
	assert Linguistics_Of( holder ) is ling
	Record_Language_Grant(
			holder,
			"Deft Explorer",
			learned,
			)
	assert holder.language_feature_grants == {"Deft Explorer": list( learned )}

	print( "OK - Map_of_Languages: Common and two d12 Standard languages from identity.languages, the Species tongue weighing in; prior grants folded." )
