'''
Masters: the words of mastery and royalty that an origin can carry.

A vocabulary of Map_of_Titles: a word list keyed by what the lusor's genus
answers. The story engine (Map_of_Stories) may import it directly, without
the title composer.
'''
from ._glue import Genus

def Master(
		lusor,
		*,
		dice=None,
		):
	genus = Genus(lusor)

	master = []

	master += [
		"Master",
		"Royal",

		"Regent",
		]

	if "She" in genus:
		master += [
			"Mistress",
			"Lady",
			"Queen",

			"Empress",
			"Princess",
			]
	if "He" in genus:
		master += [
			"Master",
			"Lord",
			"King",

			"Emperor",
			"Prince",
			]
	if "Human" in genus:
		master += [
			"Prince",
			"Princess",
			"Crown",

			"Emperor",
			"Empress",
			"Throne",
			]
	if "Elf" in genus:
		master += [
			"Khan",
			"Leader",

			"Chieftain",
			"Ruler",
			]
	if "Dwarf" in genus:
		master += [
			"Conqueror",
			"Conquistador",
			"Colonizer",

			"Prince",
			"Princess",
			]
	if "Goblin" in genus:
		master += [
			"Captain",
			"Voicer",
			"Grandfather",
			"Grandmother",

			"Greatfather",
			"Greatmother",
			"Senator",
			]
	if "Orc" in genus:
		master += [
			"Tribune",
			"Hordelord",
			]
	if "Dragon" in genus:
		master += [
			"Headmaster",
			]
	if "Elemental" in genus:
		master += [
			"Djinn",
			"Genie",
			]
	if "Undead" in genus:
		master += [
			"Lich",
			"Pharaoh",
			]
	if "Vampire" in genus:
		master += [
			"Count",
			"Countess",

			"Baron",
			"Baroness",
			]
	return lusor.Pick(
		master,
		dice=dice,
		)
