'''
Elements: the essences that modify places and origins, the X of "The X Fortress".

A vocabulary of Map_of_Titles: a word list keyed by what the lusor's genus
answers. The story engine (Map_of_Stories) may import it directly, without
the title composer.
'''
from ._glue import Genus

def Element(
		lusor,
		*,
		dice=None,
		):
	'''
Selects an elemental modifier for places and origins.
For "The Fortress of X", or "The X Fortress",this function would select the "X".
Element refers to any "essence" that is characteristic and provides archetypical meanings, or makes it sound cooler. 
'''
	genus = Genus(lusor)

	element = []
	element += [
		"Air",
		"Gem",
		"Fire",
		"Stone",
		"Earth",
		"Ice",
		"Light",
		"Darkness",
		"Lightning",
		"Storms",
		"Storm",
		"Thunder",
		"Flames",
		"Oceans",
		"Strength",
		"Life",
		"Sand",
		"Starlight",
		"Sunlight",
		"Moonlight",
		"Shadows",
		"Secrets",
		"Rain",
		"Water",
		]

	if "Dragon" in genus:
		element += [
			"Might",
			"Will",
			"Willpower",
			"Treasure",
			"Power",
			]

	if "Undead" in genus:
		element += [
			"Tomb",
			"Bone",
			"Skull",
			"Blood",
			"Spirits",
			]

	source = (
		dice
		if dice is not None
		else lusor.dices
		)

	source.shuffle(
		element,
		)

	while True:
		yield element[0]
		source.shuffle(
			element,
			)
