'''
Places: the locations a title can be of, the X of "The Lord of the X".

A vocabulary of Map_of_Titles: a word list keyed by what the lusor's genus
answers. The story engine (Map_of_Stories) may import it directly, without
the title composer.
'''
from ._glue import Genus

def Place(
		lusor,
		*,
		dice=None,
		):
	genus = Genus(lusor)

	place = []
	place += [
		"Dungeon",
		"Woods",
		"Forest",
		"Lands",
		"Caves",
		"Halls",
		"Temple",
		"Temples",
		"Ruins",
		"Wilds",
		"Abyss",
		"Desert",
		"Lake",
		"Sea",
		"Ocean",
		"Labyrinth",
		"Labyrinths",
		"Road",
		"Paths",
		"Circle",
		"Skies",
		"Court",
		"Throne",
		"Watch",
		"Fortress",
		"Marshes",
		"Camp",
		"Garden",
		"Gardens",
		"Peaks",
		"Groves",
		"Groove",
		"WastesMonolith",
		"Fortress",
		]
	if "Human" in genus:
		place += [
			"Realm",
			"Kingdom",
			"Empire",

			"Nation",
			"State",
			]
	if "Cleric" in genus:
		place += [
			"Sanctuary",
			"Temple",
			"Temples",

			"Shrine",
			"Shrines",
			]
	if "Undead" in genus:
		place += [
			"Tomb",
			"Graveyard",
			"Graveyards",
			"Cemetary",

			"Cemetaries",
			"Necropolis",
			"Necropolises",
			]
	if "Fiend" in genus:
		place += [
			"Hell",
			"Hells",

			"Inferno",
			"Infernos",
			]

	return lusor.Pick(
		place,
		dice=dice,
		)
