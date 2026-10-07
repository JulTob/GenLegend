# AtlasLusoris.Map_of_Species

from Minion import guardian

from AtlasActorLudi.AtlasAlusoris.Map_of_Races import race_weights as races
# from AtlasActorLudi.AtlasAlusoris.Map_of_Races import *
from AtlasActorLudi.AtlasAlusoris.Map_of_Races import (
	Humans
	)
from AtlasActorLudi.SpeciesKit import SPECIES_WEIGHTS
from AtlasActorLudi.SpeciesKit.Dragonborn.Map_of_Ancestors import draconic_ancestor

from AtlasLusoris.Grimoire_of_Features import  *

species = dict(
	SPECIES_WEIGHTS
	)

# Retired catalogue notes:
#	"Githyanki":    	40,
#	"Githerai":        	40,
#	"Goblin":        	30,
#	"Kobold":        	30,
#	"Lizardfolk":    	30,
#	"Satyr":        	30,
#	"Minotaur":        	30,
#	"Shifter":        	30,
#	"Aarakocra":    	25,
#	"Changeling":    	25,
#	"Deep Gnome":    	25,
#	"Duergar":        	25,
#	"Eladrin":        	25,
#	"Fairy":        	25,
#	"Firbolg":        	25,
#	"Air Genasi":    	25,
#	"Earth Genasi":    	25,
#	"Fire Genasi":    	25,
#	"Water Genasi":    	25,
#	"Yuan Ti":        	25,
#	"Warforged":    	25,
#	"Centaur":        	20,
#	"Harengon":        	15,
#	"Kenku":        	15,
#	"Locathah":        	15,
#	"Owlin":        	15,
#	"Sea Elf":        	15,
#	"Shadar Kai":    	15,
#	"Tabaxi":        	15,
#	"Tortle":        	15,
#	"Triton":       	15,
#	"Verdan":        	15,
#	"Bugbear":        	15,
#	"Grung":        	15,
#	"Hobgoblin":    	15,
#	"Kender":        	15,
#	"Kalashtar":    	15,
#	"Dhampire":        	15,
#	"Hexblood":        	15,
#	"Reborn":        	15,
#	"Aetherborn":    	10,
#	"Aven":            	10,
#	"Khenra":        	10,
#	"Kor":            	10,
#	"Merfolk":        	10,
#	"Naga":            	10,
#	"Siren":        	10,
#	"Vampire":        	10,
#	"Loxodon":        	10,
#	"Simic Hybrid":    	10,
#	"Vedalken":        	10,
#	"Astral Elf":    	10,
#	"Autognome":    	10,
#	"Giff":            	10,
#	"Hadozee":        	10,
#	"Plasmoid":        	10,
#	"Thri Kreen":    	10,
#	"Leonin":        	10,

@guardian
def species_to_race_and_subrace(
	species_name,
	character=None,
	):
	mapping = {
		"Human": ("Human", None),
		"Dwarf": ("Dwarf", None),
		"Elf": ("Elf", None),
		"Dragonborn": ("Dragon", "Dragonborn"),
		"Gnome": ("Gnome", None),
		"Orc": ("Orc", None),
		"Halfling": ("Halfling", None),
		"Tiefling": ("Fiend", "Tiefling"),
		"Goliath": ("Giant", "Goliath"),
		"Aasimar": ("Celestial", "Aasimar"),
		# Add others if needed.
		}
	if species_name not in mapping:
		return ("Unknown", None)

	race, subrace = mapping[
		species_name
		]

	if character is not None:
		from AtlasActorLudi.SpeciesKit import Current_Heritage

		heritage = Current_Heritage( character )

		if heritage is not None:
			subrace = heritage.__name__.replace(
				"_",
				" ",
				)

	if (
		species_name == "Human"
		and character is not None
		):
		#-- One choice, one bag: the Human culture is drawn from the bag
		#-- opened here and handed to Map_of_Races.Humans, which draws from it.
		culture_dice = character.Dice_Bag( "Human.culture" )
		subrace = Humans(
			character,
			dice=culture_dice,
			)

	return (
		race,
		subrace,
		)


def species_features(
	species_name,
	character=None,
	):

	species = {
		# Human species Traits are applied via SpeciesKit (see
		# Grimoire_of_Characters.apply_species_features).  Kept here only
		# as a catalogue note for callers that inspect species_features().
		"Aasimar": [],
		"Goliath": [],
		"Halfling": [],
		"Human": [],
		"Gnome": [],
		"Orc": [],
		"Tiefling": [],


		# Dwarf Traits are applied via SpeciesKit.Dwarves, which carries the
		# 2024 rules the entries below predate: Darkvision 120 rather than 60,
		# the Poisoned *condition* on the save, and Stonecunning.
		"Dwarf": [],
			}
	if species_name == "Elf":
		return ElvenFeats()
	if species_name == "Dragonborn":
		return DragonbornFeats( character )

	return species.get(species_name, [])


def apply_species_features(char, species_name):
	for feature in species_features(
		species_name,
		char,
		):
		feature(char)  # Will only run if `apply` exists
		char.features.append(feature)

def DragonbornFeats(
	character,
	):
	damage = {
		"Black":	"Acid",
		"Blue":		"Lightning",
		"Brass":	"Fire",
		"Bronze":	"Lightning",
		"Copper":	"Acid",
		"Gold":		"Fire",
		"Green":	"Poison",
		"Red":		"Fire",
		"Silver":	"Cold",
		"White":	"Cold"}
	#-- One choice, one bag: the colour is the one Draconic_Ancestry drew, or
	#-- draws now from its own bag; never a second draw for the same ancestor.
	color, _damage_type = draconic_ancestor( character )
	dragonborn = Feature(name="Dragonborn",
		description="""Legends and myth shrouds the origins of the Dragonborn, but one thing is certain: They are the children of dragons.
		Their colors and features are reminiscent of their draconic ancestors, nontheless, their origins do not determine their destiny.
		The Dragonborn are a proud and noble people, inclined to follow their own paths, with honor and respect for their heritage..

		<br>
		Dragonborn look like wingless, bipedal dragons: Scaly, bright eyed, and thick boned with horns on their heads, and their coloration and other features are reminiscent of their draconic ancestors.""",
		source="Species Feature")
	DraconicAncestry = Feature(name="Draconic Ancestry",
		description=f"""
		Your lineage stems from a {color} Dragon progenitor. <br>
		You have Resistance to {damage[color]} damage.
		""",
		source="Species Feature")
	BreathWeapon  = Feature(name="Breath Weapon",
			description=f"""
When you take the Attack action on your turn, you can replace one of your attacks with an exhalation of magical energy in either a 15-foot Cone or a 30-foot Line that is 5 feet wide (choose the shape each time).
Each creature in that area must make a Dexterity saving throw (DC 8 plus your Constitution modifier and Proficiency Bonus).
On a failed save, a creature takes 1d10 {damage[color]} damage.
On a successful save, a creature takes half as much damage.
This damage increases by 1d10 when you reach character levels 5 (2d10), 11 (3d10), and 17 (4d10).

You can use this Breath Weapon a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest.
			""",
			source="Species Feature")
	DraconicFlight = Feature(name="Draconic Flight.",
			description=f"""
When you reach character level 5, you can channel draconic magic to give yourself temporary flight. As a Bonus Action, you sprout spectral wings on your back that last for 10 minutes or until you retract the wings (no action required) or have the Incapacitated condition. During that time, you have a Fly Speed equal to your Speed. Your wings appear to be made of the same energy as your Breath Weapon. Once you use this trait, you can't use it again until you finish a Long Rest.
			""",
			source="Species Feature")
	return [Humanoid(),	dragonborn, DraconicAncestry, BreathWeapon, Darkvision(), DraconicFlight]

def ElvenFeats():
	features =  [
		Humanoid(),
		Darkvision(),
		Feature(name="Keen Senses", description="You have proficiency in the Perception skill.", source="Species Feature"),
		Feature(name="Fey Ancestry", description="You have advantage on saving throws against being charmed.", source="Species Feature")
		]
	return features


def Humanoid():
	return Feature(name="Creature Type", description="Humanoid", source="Species Feature")


def creature_type_label(features=None, default="Humanoid"):
	"""Return the Creature Type string from species features, if present."""
	for feature in features or []:
		if getattr(feature, "name", "") == "Creature Type":
			return getattr(feature, "description", default) or default
	return default


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the Human culture on the sheet comes from one
	#-- Dice Bag opened here as "Human.culture" with the default key and
	#-- handed to Map_of_Races.Humans, which draws from it and nothing else.
	from AtlasActorLudi.CharactersKit import Character

	opened = []
	purpose_of_bag = {}
	drawn = []
	original_dice_bag = Character.Dice_Bag
	original_pick = Character.Pick

	def recording_dice_bag(
		char,
		purpose,
		**key,
		):
		bag = original_dice_bag(
			char,
			purpose,
			**key,
			)
		opened.append(
			(
				purpose,
				key,
				)
			)
		purpose_of_bag[
			id(
				bag
				)
			] = purpose
		return bag

	def recording_pick(
		char,
		ledger,
		weights=None,
		**options,
		):
		drawn.append(
			(
				purpose_of_bag.get(
					id(
						options.get(
							"dice"
							)
						)
					),
				tuple(
					ledger
					),
				None
				if weights is None
				else tuple(
					weights
					),
				)
			)
		return original_pick(
			char,
			ledger,
			weights,
			**options,
			)

	Character.Dice_Bag = recording_dice_bag
	Character.Pick = recording_pick
	try:
		character = Character(
			seed=7,
			)
		race, subrace = species_to_race_and_subrace(
			"Human",
			character,
			)
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	cultures = (
		"Local",
		"Foreigner",
		"Highlander",
		"Nomad",
		"Islander",
		"Forester",
		"Plainsfolk",
		"Urbanite",
		"Northerner",
		"Southerner",
		"Easterner",
		"Westerner",
		)
	assert race == "Human"
	assert subrace in cultures
	assert opened == [
		(
			"Human.culture",
			{},
			),
		], opened
	assert drawn == [
		(
			"Human.culture",
			cultures,
			( 30, 25, 20, 20, 16, 16, 15, 14, 20, 20, 20, 20 ),
			),
		], drawn


def _test_dragonborn_feats_read_the_standing_ancestor() -> None:
	#-- The legacy Dragonborn Entries read the ancestor Draconic_Ancestry
	#-- drew; they open no second bag for the same choice.
	from AtlasActorLudi.CharactersKit import Character

	opened = []
	original_dice_bag = Character.Dice_Bag

	def recording_dice_bag(
		char,
		purpose,
		**key,
		):
		opened.append( purpose )
		return original_dice_bag(
			char,
			purpose,
			**key,
			)

	Character.Dice_Bag = recording_dice_bag
	try:
		character = Character(
			seed=7,
			)
		character.draconic_ancestor = "Gold"
		features = species_features(
			"Dragonborn",
			character,
			)
	finally:
		Character.Dice_Bag = original_dice_bag

	ancestry = next(
		feature
		for feature in features
		if feature.name == "Draconic Ancestry"
		)
	assert opened == [], opened
	assert "Gold Dragon" in ancestry.description
	assert "Fire damage" in ancestry.description


if __name__ == "__main__":
	_test_dice_purpose()
	_test_dragonborn_feats_read_the_standing_ancestor()
	print( "OK: Map_of_Species self-test" )
