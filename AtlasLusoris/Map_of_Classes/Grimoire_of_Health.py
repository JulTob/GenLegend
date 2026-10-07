from AtlasLudus.Map_of_Dice import Dice

HIT_DIE_TABLE = {
	"Barbarian": 12,
	"Fighter": 10, "Paladin": 10, "Ranger": 10,
	"Artificer": 8, "Bard": 8, "Cleric": 8, "Druid": 8, "Monk": 8,
	"Rogue": 8, "Warlock": 8,
	"Sorcerer": 6, "Wizard": 6,
	}

def roll_health(character):
	"""Roll the hit points of every level after the first.

	The rolls come from one Dice Bag of the Character, named by the Guild
	(``<Guild>.hit_points``, ruling 8 of Dialog 0027, QST-0144.6), so no
	draw made before them can move them.
	"""
	guild = character.char_class
	dice_value = health_dice(guild)
	dice = character.Dice_Bag( f"{guild}.hit_points" )
	level = character.Level
	for lvl in range(1,level):
		character.base_health += Dice(D=dice_value, dice=dice)


def hit_dice(character):
	if "Barbarian" in character: 	return 12

	elif "Fighter" in character: 	return 10
	elif "Paladin" in character: 	return 10
	elif "Ranger" in character: 	return 10

	elif "Bard" in character: 		return 8
	elif "Cleric" in character: 	return 8
	elif "Druid" in character: 		return 8
	elif "Monk" in character: 		return 8
	elif "Rogue" in character: 		return 8
	elif "Warlock" in character: 	return 8

	elif "Sorcerer" in character: 	return 6
	elif "Wizard" in character: 	return 6
	from AtlasLudus.Map_of_Dice import Dice
	return 5 + Dice(6)





def health_dice(class_name: str) -> int:
	"""
	Return the size of this class's hit die (e.g. 10 for a d10).
	Every Guild has a row in HIT_DIE_TABLE: the size is a lookup, never a
	roll, so a name outside the table is an error.
	"""
	die = HIT_DIE_TABLE.get(class_name.title())
	if die is None:
		raise ValueError(
				f"health_dice: {class_name!r} has no hit die in HIT_DIE_TABLE "
				f"(the Guilds it knows: {', '.join( sorted( HIT_DIE_TABLE ) )})."
				)
	return die


if __name__ == "__main__":
	from random import Random

	class Probe:
		"""A Character stand-in with the fields roll_health reads."""
		def __init__(probe, guild, level):
			probe.char_class = guild
			probe.Level = level
			probe.base_health = 0
			probe.opened = []

		def Dice_Bag(probe, purpose):
			probe.opened.append(purpose)
			return Random(purpose)

	#-- the die size is a lookup for every Guild, Artificer included
	assert health_dice("Artificer") == 8
	assert health_dice("Barbarian") == 12
	assert health_dice("wizard") == 6
	try:
		health_dice("Alchemist")
	except ValueError as refusal:
		assert "Alchemist" in str(refusal)
	else:
		raise AssertionError("an unknown Guild must be refused, not rolled")

	#-- the hit points come from one bag, <Guild>.hit_points, one roll per
	#-- level after the first, and replay from the same bag
	probe = Probe("Fighter", 5)
	roll_health(probe)
	assert probe.opened == ["Fighter.hit_points"], probe.opened
	bag = Random("Fighter.hit_points")
	assert probe.base_health == sum(bag.randint(1, 10) for _ in range(4))
	assert 4 <= probe.base_health <= 40

	#-- a level 1 Character rolls nothing
	fresh = Probe("Rogue", 1)
	roll_health(fresh)
	assert fresh.base_health == 0 and fresh.opened == ["Rogue.hit_points"]

	print("OK - Grimoire_of_Health: hit points roll from <Guild>.hit_points.")
