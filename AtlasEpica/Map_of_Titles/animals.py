'''
Animals: the beasts an origin can be of.

A vocabulary of Map_of_Titles: a plain word list, the one vocabulary that
does not read the genus. The story engine (Map_of_Stories) may import it
directly, without the title composer.
'''

def Animal(
		lusor,
		*,
		dice=None,
		):
	animal = [
		"Baboon",
		"Butterfly",
		"Beetle",
		"Cat",
		"Cheetah",
		"Cougar",
		"Coyote",
		"Crocodile",

		"Dolphin",
		"Dinosaur",
		"Elephant",
		"Bison",
		"Boar",
		"Badger",
		"Deer",
		]
	return lusor.Pick(
		animal,
		dice=dice,
		)
