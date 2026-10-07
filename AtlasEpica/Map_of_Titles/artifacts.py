'''
Artifacts: the objects a title can be of, the X of "The Keeper of the X".

A vocabulary of Map_of_Titles: a word list keyed by what the lusor's genus
answers. The story engine (Map_of_Stories) may import it directly, without
the title composer.
'''
from ._glue import Genus

def Artifact(
		lusor,
		*,
		dice=None,
		):
	genus = Genus(lusor)

	artifact = []
	artifact += [
		"Amulet",
		"Book",
		"Goblet",

		"Ring",
		"Talisman",
		"Scales",
		]
	artifact += [
		"Sceptre",
		"Staff",

		"Scroll",
		"Sword",
		]
	if "Human" in genus:
		artifact += [
			"Crown",
			]
	if "Wizard" in genus:
		artifact += [
			"Spellbook",
			"Quill",
			"Book",

			"Wand",
			"Book of Wizards",
			]
	if "Cleric" in genus:
		artifact += [
			"Holy Book",
			"Scriptures",

			"Ankh",
			"Amulet",
			]
	return lusor.Pick(
		artifact,
		dice=dice,
		)
