try:
	from AtlasLudus.Map_of_Useful_Functions import select1
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasActorLudi.Map_of_Scores import PB
	from AtlasScriptum.Map_of_Formats import Entry_Text
	from AtlasActorLudi.Map_of_Size import Size as sizer
except ImportError:
	raise

import app.random as random


def Resistances(npc):

	race = npc.race
	subrace = npc.subrace
	background = npc.background
	pb = npc.pb

	damage_types = [
		"acid", "bludgeoning", "cold", "fire", "force",
		"lightning", "necrotic", "piercing", "poison",
		"psychic", "radiant", "slashing", "thunder",
		"bludgeoning, piercing, and slashing from nonmagical attacks"

	]
	race_damage_tendencies = {
		"Dragon": {
			"acid": {
				"Immune": pb//2, "Resistant": pb//2, "None": pb, "Vulnerable": pb//3},
			"bludgeoning": {
				"Immune": pb//6, "Resistant": pb//2, "None": pb, "Vulnerable": pb//6},
			"cold": {
				"Immune": pb//3, "Resistant": pb//2, "None": pb, "Vulnerable": pb//6},
			"fire": {
				"Immune": pb//3, "Resistant": pb//2, "None": pb, "Vulnerable": pb//6},
			"force": {
				"Immune": pb//12, "Resistant": pb//6, "None": pb*2, "Vulnerable": pb//2},
			"lightning": {
				"Immune": pb//3, "Resistant": pb//2, "None": pb, "Vulnerable": pb//6},
			"necrotic": {
				"Immune": pb//6, "Resistant": pb//2, "None": pb, "Vulnerable": pb//6},
			"piercing": {
				"Immune": pb//6, "Resistant": pb, "None": 2*pb, "Vulnerable": pb//6},
			"poison": {
				"Immune": pb//6, "Resistant": (pb+1)//2, "None": pb, "Vulnerable": pb//6},
			"psychic": {
				"Immune": pb//6, "Resistant": pb//3, "None": pb, "Vulnerable": pb//6},
			"radiant": {
				"Immune": pb//7, "Resistant": pb//4, "None": pb, "Vulnerable": pb//6},
			"slashing": {
				"Immune": pb//6, "Resistant": pb//3, "None": pb, "Vulnerable": pb//6},
			"thunder": {
				"Immune": pb//6, "Resistant": pb//2, "None": pb, "Vulnerable": pb//6},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//6, "Resistant": pb//3, "None": pb, "Vulnerable": 0},
			},

		"Human": {
				"acid":{
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"bludgeoning": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"cold": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"fire": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"force": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"lightning": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"necrotic": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"piercing": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"poison": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"psychic": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"radiant": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"slashing": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"thunder": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb//3},
				"bludgeoning, piercing, and slashing from nonmagical attacks": {
					"Immune": pb//8, "Resistant": pb//3, "None": pb*2, "Vulnerable": 0},
				},
		"Aberration": {
				"acid": {
					"Immune": pb//4, "Resistant": pb//2, "None": pb//3, "Vulnerable": pb//5},
				"bludgeoning": {
					"Immune": pb//5, "Resistant": pb//4, "None": pb//2, "Vulnerable": pb//3},
				"cold": {
					"Immune": pb//8, "Resistant": pb//4, "None": pb//3, "Vulnerable": pb//2},
				"fire": {
					"Immune": pb//8, "Resistant": pb//4, "None": pb//3, "Vulnerable": pb//2},
				"force": {
					"Immune": 0, "Resistant": pb//4, "None": pb//3, "Vulnerable": pb//2},
				"lightning": {
					"Immune": pb//8, "Resistant": pb//4, "None": pb//3, "Vulnerable": pb//2},
				"necrotic": {
					"Immune": pb//8, "Resistant": pb//4, "None": pb//2, "Vulnerable": 0},
				"piercing": {
					"Immune": pb//8, "Resistant": pb//8, "None": pb//2, "Vulnerable": pb//2},
				"poison": {
					"Immune": pb//2, "Resistant": pb//3, "None": pb//4, "Vulnerable": pb//5},
				"psychic": {
					"Immune": pb//2, "Resistant": pb//3, "None": pb//4, "Vulnerable": pb//5},
				"radiant": {
					"Immune": pb//5, "Resistant": pb//4, "None": pb//3, "Vulnerable": pb//2},
				"slashing": {
					"Immune": pb//8, "Resistant": pb//8, "None": pb//2, "Vulnerable": pb//2},
				"thunder": {
					"Immune": pb//5, "Resistant": pb//4, "None": pb//3, "Vulnerable": pb//2},
				"bludgeoning, piercing, and slashing from nonmagical attacks": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb//2, "Vulnerable": pb//16},
				},
		"Aven": {
				"acid": {
					"Immune": 0, "Resistant": 2, "None": 10, "Vulnerable": 1},
				"bludgeoning": {
					"Immune": 0, "Resistant": 4, "None": 10, "Vulnerable": 2},
				"cold": {
					"Immune": 1, "Resistant": 3, "None": 10, "Vulnerable": 3},
				"fire": {
					"Immune": 0, "Resistant": 2, "None": 10, "Vulnerable": 3},
				"force": {
					"Immune": 0, "Resistant": 0, "None": 10, "Vulnerable": 2},
				"lightning": {
					"Immune": 1, "Resistant": 4, "None": 10, "Vulnerable": 1},
				"necrotic": {
					"Immune": 0, "Resistant": 2, "None": 10, "Vulnerable": 2},
				"piercing": {
					"Immune": 0, "Resistant": 3, "None": 10, "Vulnerable": 3},
				"poison": {
					"Immune": 0, "Resistant": 2, "None": 10, "Vulnerable": 2},
				"psychic": {
					"Immune": 0, "Resistant": 2, "None": 10, "Vulnerable": 1},
				"radiant": {
					"Immune": 0, "Resistant": 2, "None": 10, "Vulnerable": 1},
				"slashing": {
					"Immune": 0, "Resistant": 3, "None": 10, "Vulnerable": 3},
				"thunder": {
					"Immune": 0, "Resistant": 3, "None": 10, "Vulnerable": 1},
				"bludgeoning, piercing, and slashing from nonmagical attacks": {
					"Immune": 0, "Resistant": pb//2, "None": pb, "Vulnerable": 0},
				},
		"Beast": {
				"acid": {"Immune": 1, "Resistant": 3, "None": 6, "Vulnerable": 2},
				"bludgeoning": {"Immune": 2, "Resistant": 4, "None": 3, "Vulnerable": 3},
				"cold": {"Immune": 2, "Resistant": 4, "None": 4, "Vulnerable": 2},
				"fire": {"Immune": 1, "Resistant": 3, "None": 5, "Vulnerable": 3},
				"force": {"Immune": 1, "Resistant": 1, "None": 8, "Vulnerable": 2},
				"lightning": {"Immune": 2, "Resistant": 3, "None": 5, "Vulnerable": 2},
				"necrotic": {"Immune": 1, "Resistant": 2, "None": 6, "Vulnerable": 3},
				"piercing": {"Immune": 2, "Resistant": 4, "None": 3, "Vulnerable": 3},
				"poison": {"Immune": 3, "Resistant": 4, "None": 2, "Vulnerable": 3},
				"psychic": {"Immune": 1, "Resistant": 2, "None": 7, "Vulnerable": 2},
				"radiant": {"Immune": 1, "Resistant": 2, "None": 6, "Vulnerable": 3},
				"slashing": {"Immune": 2, "Resistant": 4, "None": 3, "Vulnerable": 3},
				"thunder": {"Immune": 2, "Resistant": 3, "None": 5, "Vulnerable": 2},
				"bludgeoning, piercing, and slashing from nonmagical attacks": {
					"Immune": 4, "Resistant": 3, "None": 2, "Vulnerable": 3},
				},
		"Beastfolk": {
				"acid": {"Immune": pb//8, "Resistant": pb//5, "None": pb, "Vulnerable": pb//4},
				"bludgeoning": {"Immune": pb//8, "Resistant": pb//5, "None": pb, "Vulnerable": pb//4},
				"cold": {"Immune": pb//5, "Resistant": pb//2, "None": pb, "Vulnerable": pb//3},
				"fire": {"Immune": pb//7, "Resistant": pb//5, "None": pb, "Vulnerable": pb//2},
				"force": {"Immune": 0, "Resistant": pb//8, "None": pb, "Vulnerable": 0},
				"lightning": {"Immune": pb//9, "Resistant": pb//7, "None": pb, "Vulnerable": pb//6},
				"necrotic": {"Immune": pb//5, "Resistant": pb//3, "None": pb, "Vulnerable": pb//3},
				"piercing": {"Immune": 0, "Resistant": pb//7, "None": pb, "Vulnerable": pb//6},
				"poison": {"Immune": 1, "Resistant": 1+pb//2, "None": pb, "Vulnerable": pb//2},
				"psychic": {"Immune": 1, "Resistant": 1+pb//2, "None": pb, "Vulnerable": pb//3},
				"radiant": {"Immune": pb//5, "Resistant": pb//3, "None": pb, "Vulnerable": pb//2},
				"slashing": {"Immune": 0, "Resistant": pb//4, "None": pb, "Vulnerable":0},
				"thunder": {"Immune": pb//4, "Resistant": pb//3, "None": pb, "Vulnerable": pb//2},
				"bludgeoning, piercing, and slashing from nonmagical attacks that aren't silvered": {
					"Immune": 1, "Resistant": pb//2, "None": pb, "Vulnerable": 0},
				},
		"Catfolk": {
				"acid": {"Immune": pb//10, "Resistant": pb//7, "None": pb, "Vulnerable": pb//5},
				"bludgeoning": {"Immune": pb//5, "Resistant": pb//3, "None": pb, "Vulnerable": pb//8},
				"cold": {"Immune": pb//10, "Resistant": pb//6, "None": pb, "Vulnerable": pb//3},
				"fire": {"Immune": pb//10, "Resistant": pb//6, "None": pb, "Vulnerable": pb//3},
				"force": {"Immune": 0, "Resistant":pb//10, "None": pb, "Vulnerable": 0},
				"lightning": {"Immune": pb//7, "Resistant": pb//3, "None": pb, "Vulnerable": pb//3},
				"necrotic": {"Immune": pb//8, "Resistant": pb//4, "None": pb, "Vulnerable": pb//3},
				"piercing": {"Immune": pb//10, "Resistant": pb//8, "None": pb, "Vulnerable": 0},
				"poison": {"Immune": pb//10, "Resistant": pb//7, "None": pb, "Vulnerable": pb//6},
				"psychic": {"Immune": pb//5, "Resistant": pb//3, "None": pb, "Vulnerable": pb//3},
				"radiant": {"Immune": pb//3, "Resistant": pb//2, "None": pb, "Vulnerable": pb//4},
				"slashing": {"Immune": pb//8, "Resistant": pb//4, "None": pb, "Vulnerable": pb//3},
				"thunder": {"Immune": pb//10, "Resistant": pb//7, "None": pb, "Vulnerable": pb//3},
				"bludgeoning, piercing, and slashing from nonmagical attacks that aren't silvered": {
					"Immune": pb//4, "Resistant": pb//3, "None": pb, "Vulnerable": 0},
				},
		"Celestial": {
				"acid": {
					"Immune": pb//2, "Resistant": pb+2, 	"None": pb*2, "Vulnerable": pb//3},
				"bludgeoning": {
					"Immune": pb//2, "Resistant": pb+2, 	"None": pb*2, "Vulnerable": pb//3},
				"cold": {
					"Immune": pb, 	"Resistant": pb+1, 		"None": pb*2, "Vulnerable": pb//3},
				"fire": {
					"Immune": pb, 	"Resistant": pb+2, 		"None": pb*3, "Vulnerable": pb//4},
				"force": {
					"Immune": pb//5, "Resistant": pb//4, 	"None": pb//3, "Vulnerable": pb//2},
				"lightning": {
					"Immune": pb//2, "Resistant": pb, 		"None": pb*3, "Vulnerable": pb//4},
				"necrotic": {
					"Immune": pb, 	"Resistant": pb, 		"None": pb, "Vulnerable": pb},
				"piercing": {
					"Immune": pb//2, "Resistant": pb, 		"None": pb*2, "Vulnerable": pb//6},
				"poison": {
					"Immune": pb, 	"Resistant": pb*2, 		"None": pb*3, "Vulnerable": pb//4},
				"psychic": {
					"Immune": pb, 	"Resistant": pb, 		"None": pb*2, "Vulnerable": pb//5},
				"radiant": {
					"Immune": pb, 	"Resistant": pb//2, 	"None": pb//3, "Vulnerable": pb//6},
				"slashing": {
					"Immune": pb//3, "Resistant": pb, 		"None": pb*2, "Vulnerable": pb//4},
				"thunder": {
					"Immune": pb, 	"Resistant": pb+2, 		"None": pb, "Vulnerable": pb-1},
				"bludgeoning, piercing, and slashing from nonmagical attacks": {
					"Immune": pb, 	"Resistant": pb, "None": pb*2, "Vulnerable": 0},
				},
		"Construct": {
				"acid": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"bludgeoning": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"cold": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"fire": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"force": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"lightning": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"necrotic": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"piercing": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"poison": {
					"Immune": pb, "Resistant": pb//2, "None": 0, "Vulnerable": 0},
				"psychic": {
					"Immune": pb//2, "Resistant": pb//2, "None": pb, "Vulnerable": pb//3},
				"radiant": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"slashing": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"thunder": {
					"Immune": pb//5, "Resistant": pb//3, "None": pb+2, "Vulnerable": pb//2},
				"bludgeoning, piercing, and slashing from nonmagical attacks": {
					"Immune": pb//2, "Resistant": pb+1, "None": pb//2, "Vulnerable": 0},
				},
		"Dwarf": {
			"acid": {
				"Immune": pb//5, "Resistant": pb//3, "None": pb, "Vulnerable": pb//7},
			"bludgeoning": {
				"Immune": pb//7, "Resistant": pb//3, "None": pb, "Vulnerable": pb//7},
			"cold": {
				"Immune": pb//5, "Resistant": pb//2, "None": pb, "Vulnerable": pb//7},
			"fire": {
				"Immune": pb//11, "Resistant": pb//5, "None": pb, "Vulnerable": pb//7},
			"force": {
				"Immune": 0, "Resistant": 0, "None": pb, "Vulnerable": pb//3},
			"lightning": {
				"Immune": pb//7, "Resistant": pb//5, "None": pb, "Vulnerable": pb//3},
			"necrotic": {
				"Immune": pb//7, "Resistant": pb//3, "None": pb, "Vulnerable": pb//2},
			"piercing": {
				"Immune": pb//7, "Resistant": pb//3, "None": pb, "Vulnerable": pb//5},
			"poison": {
				"Immune": pb//3, "Resistant": pb, "None": pb//2, "Vulnerable": 0},
			"psychic": {
				"Immune": pb//3, "Resistant": pb//2, "None": pb, "Vulnerable": 0},
			"radiant": {
				"Immune": pb//11, "Resistant": pb//7, "None": pb, "Vulnerable": 0},
			"slashing": {
				"Immune": pb//7, "Resistant": pb//3, "None": pb, "Vulnerable": pb//5},
			"thunder": {
				"Immune": pb//5, "Resistant": pb//3, "None": pb, "Vulnerable": pb//2},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//7, "Resistant": pb//5, "None": pb, "Vulnerable": 0},
			},
		"Elf": {
			"acid": {"Immune": 1, "Resistant": 4, "None": 4, "Vulnerable": 1},
			"bludgeoning": {"Immune": 0, "Resistant": 3, "None": 6, "Vulnerable": 1},
			"cold": {"Immune": 1, "Resistant": 5, "None": 4, "Vulnerable": 0},
			"fire": {"Immune": 1, "Resistant": 5, "None": 4, "Vulnerable": 0},
			"force": {"Immune": 0, "Resistant": 4, "None": 6, "Vulnerable": 0},
			"lightning": {"Immune": 1, "Resistant": 4, "None": 4, "Vulnerable": 1},
			"necrotic": {"Immune": 1, "Resistant": 2, "None": 5, "Vulnerable": 2},
			"piercing": {"Immune": 0, "Resistant": 3, "None": 6, "Vulnerable": 1},
			"poison": {"Immune": 3, "Resistant": 5, "None": 2, "Vulnerable": 0},
			"psychic": {"Immune": 0, "Resistant": 3, "None": 7, "Vulnerable": 0},
			"radiant": {"Immune": 1, "Resistant": 3, "None": 5, "Vulnerable": 1},
			"slashing": {"Immune": 0, "Resistant": 3, "None": 6, "Vulnerable": 1},
			"thunder": {"Immune": 0, "Resistant": 3, "None": 6, "Vulnerable": 1},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 0, "Resistant": 2, "None": 8, "Vulnerable": 0},
			},
		"Elemental": {
			"acid": {
				"Immune": 5, "Resistant": 6, "None": 5, "Vulnerable": 5},
			"bludgeoning": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 6},
			"cold": {
				"Immune": 6, "Resistant": 6, "None": 8, "Vulnerable": 7},
			"fire":{
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 6},
			"force": {
				"Immune": 0, "Resistant": 5, "None": 5, "Vulnerable": 15},
			"lightning": {
				"Immune": 5, "Resistant": 5, "None": 5, "Vulnerable": 5},
			"necrotic": {
				"Immune": 5, "Resistant": 5, "None": 10, "Vulnerable": 5},
			"piercing": {
				"Immune": 5, "Resistant": 5, "None": 5, "Vulnerable": 5},
			"poison": {
				"Immune": 10, "Resistant": 5, "None": 0, "Vulnerable": 0},
			"psychic": {
				"Immune": 0, "Resistant": 5, "None": 10, "Vulnerable": 5},
			"radiant": {
				"Immune": 5, "Resistant": 5, "None": 5, "Vulnerable": 5},
			"slashing": {
				"Immune": 5, "Resistant": 5, "None": 5, "Vulnerable": 5},
			"thunder": {
				"Immune": 6, "Resistant": 6, "None": 7, "Vulnerable": 6},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 6, "Resistant": 7, "None": 10, "Vulnerable": 0},
			},
		"Fey": {
			"acid": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"bludgeoning": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"cold": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"fire": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"force": {
				"Immune": 0, "Resistant": 0, "None": pb*2, "Vulnerable": pb//2},
			"lightning": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"necrotic": {
				"Immune": pb//10, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb},
			"piercing": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"poison": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": pb//2},
			"psychic": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"radiant": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"slashing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"thunder": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": 0},
			},
		"Fiend": {
			"acid": {
				"Immune": pb//2, "Resistant": pb, "None": pb//2, "Vulnerable": pb//5},
			"bludgeoning": {
				"Immune": 0, "Resistant": 0, "None": pb, "Vulnerable": 0},
			"cold": {
				"Immune": pb//2, "Resistant": pb, "None": pb//3, "Vulnerable": pb//4},
			"fire": {
				"Immune": pb, "Resistant": pb//2, "None": pb//3, "Vulnerable": pb//4},
			"force": {
				"Immune": 0, "Resistant": pb//4, "None": pb, "Vulnerable": pb//4},
			"lightning": {
				"Immune": pb//2, "Resistant": pb, "None": pb//2, "Vulnerable": pb//3},
			"necrotic": {
				"Immune": pb, "Resistant": pb//2, "None": pb//3, "Vulnerable": pb//4},
			"piercing": {
				"Immune": 0, "Resistant": pb//2, "None": pb, "Vulnerable": 0},
			"poison": {
				"Immune": 2*pb, "Resistant": pb, "None": pb//2, "Vulnerable": pb//3},
			"psychic": {
				"Immune": pb//3, "Resistant": pb, "None": pb, "Vulnerable": pb//3},
			"radiant": {
				"Immune": pb//5, "Resistant": pb//4, "None": pb//2, "Vulnerable": pb*2},
			"slashing": {
				"Immune": 0, "Resistant": 0, "None": pb, "Vulnerable": 0},
			"thunder": {
				"Immune": pb//2, "Resistant": pb, "None": pb//2, "Vulnerable": pb//3},
			"bludgeoning, piercing, and slashing from nonmagical attacks that aren't silvered": {
				"Immune": pb*2, "Resistant": pb, "None": pb, "Vulnerable": 0},
			},
		"Giant": {
			"acid": {
				"Immune": 0, "Resistant": pb//3, "None": pb*2, "Vulnerable": pb+1},
			"bludgeoning": {
				"Immune": 0, "Resistant": pb, "None": pb//2, "Vulnerable": 0},
			"cold": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"fire": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"force": {
				"Immune": 0, "Resistant": 0, "None": pb*2, "Vulnerable": pb//4},
			"lightning": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"necrotic": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"piercing": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"poison": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"psychic": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//3},
			"radiant": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"slashing": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"thunder": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": pb//4},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//3, "Resistant": pb, "None": pb*2, "Vulnerable": 0},
			},
		"Gnome": {
			"acid": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"cold": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"fire": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"force": {
				"Immune": 0, "Resistant": 0, "None": pb*5, "Vulnerable": pb},
			"lightning": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"necrotic": {
				"Immune": pb//7, "Resistant": pb//2, "None": pb*2, "Vulnerable": pb},
			"piercing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"poison": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"psychic": {
				"Immune": pb//5, "Resistant": pb*2, "None": pb*3, "Vulnerable": pb//2},
			"radiant": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"slashing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"thunder": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//5, "Resistant": pb, "None": pb*2, "Vulnerable": 0},
			},
		"Goblin": {
			"acid": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"cold": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"fire": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"force": {
				"Immune": 0, "Resistant": 0, "None": pb*3, "Vulnerable": pb},
			"lightning": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"necrotic": {
				"Immune": pb//7, "Resistant": pb//2, "None": pb*3, "Vulnerable": pb*2},
			"piercing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"poison": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"psychic": {
				"Immune": pb//4, "Resistant": pb*2, "None": pb*2, "Vulnerable": pb},
			"radiant": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"slashing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"thunder": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//5, "Resistant": pb, "None": pb*4, "Vulnerable": 0},
			},
		"Halfling": {
			"acid": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"cold": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"fire": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"force": {
				"Immune": 0, "Resistant": pb//7, "None": pb*6, "Vulnerable": pb},
			"lightning": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"necrotic": {
				"Immune": pb//9, "Resistant": pb//2, "None": pb*3, "Vulnerable": pb*2},
			"piercing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"poison": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"psychic": {
				"Immune": pb//7, "Resistant": pb//2, "None": pb*2, "Vulnerable": pb},
			"radiant": {
				"Immune": pb//7, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"slashing": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"thunder": {
				"Immune": pb//6, "Resistant": pb, "None": pb*2, "Vulnerable": pb},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//6, "Resistant": pb, "None": pb*3, "Vulnerable": 0},
			},
		"Kobold": {
			"acid": {
				"Immune": 1, "Resistant": 2, "None": 12, "Vulnerable": 4},
			"bludgeoning": {
				"Immune": 0, "Resistant": 1, "None": 12, "Vulnerable": 8},
			"cold": {
				"Immune": 1, "Resistant": 2, "None": 12, "Vulnerable": 5},
			"fire": {
				"Immune": 2, "Resistant": 4, "None": 12, "Vulnerable": 3},
			"force": {
				"Immune": 0, "Resistant": 1, "None": 10, "Vulnerable": 4},
			"lightning": {
				"Immune": 1, "Resistant": 2, "None": 12, "Vulnerable": 4},
			"necrotic": {
				"Immune": 0, "Resistant": 2, "None": 12, "Vulnerable": 6},
			"piercing": {
				"Immune": 1, "Resistant": 2, "None": 13, "Vulnerable": 0},
			"poison": {
				"Immune": 2, "Resistant": 3, "None": 12, "Vulnerable": 3},
			"psychic": {
				"Immune": 0, "Resistant": 1, "None": 12, "Vulnerable": 5},
			"radiant": {
				"Immune": 0, "Resistant": 1, "None": 12, "Vulnerable": 5},
			"slashing": {
				"Immune": 0, "Resistant": 1, "None": 12, "Vulnerable": 7},
			"thunder": {
				"Immune": 1, "Resistant": 2, "None": 12, "Vulnerable": 5},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 0, "Resistant": 2, "None": 12, "Vulnerable": 0},
			},
		"Lizardfolk": {
			"acid": {
				"Immune": 3, "Resistant": 6, "None": 9, "Vulnerable": 1},
			"bludgeoning": {
				"Immune": 2, "Resistant": 7, "None": 9, "Vulnerable": 1},
			"cold": {
				"Immune": 3, "Resistant": 6, "None": 10, "Vulnerable": 1},
			"fire": {
				"Immune": 2, "Resistant": 5, "None": 10, "Vulnerable": 3},
			"force": {
				"Immune": 0, "Resistant": 4, "None": 11, "Vulnerable": 4},
			"lightning": {
				"Immune": 2, "Resistant": 6, "None": 8, "Vulnerable": 3},
			"necrotic": {
				"Immune": 1, "Resistant": 4, "None": 10, "Vulnerable": 5},
			"piercing": {
				"Immune": 2, "Resistant": 10, "None": 7, "Vulnerable": 2},
			"poison": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"psychic": {
				"Immune": 2, "Resistant": 3, "None": 10, "Vulnerable": 6},
			"radiant": {
				"Immune": 1, "Resistant": 3, "None": 10, "Vulnerable": 6},
			"slashing": {
				"Immune": 2, "Resistant": 8, "None": 8, "Vulnerable": 3},
			"thunder": {
				"Immune": 2, "Resistant": 5, "None": 10, "Vulnerable": 3},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 4, "Resistant": 7, "None": 10, "Vulnerable": 1},
			},
		"Monstrosity": {
			"acid": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"bludgeoning": {
				"Immune": 3, "Resistant": 6, "None": 6, "Vulnerable": 4},
			"cold": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"fire": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"force": {
				"Immune": 3, "Resistant": 3, "None": 6, "Vulnerable": 6},
			"lightning": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"necrotic": {
				"Immune": 4, "Resistant": 4, "None": 6, "Vulnerable": 5},
			"piercing": {
				"Immune": 3, "Resistant": 6, "None": 6, "Vulnerable": 4},
			"poison": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"psychic": {
				"Immune": 4, "Resistant": 4, "None": 6, "Vulnerable": 5},
			"radiant": {
				"Immune": 3, "Resistant": 4, "None": 6, "Vulnerable": 6},
			"slashing": {
				"Immune": 3, "Resistant": 6, "None": 6, "Vulnerable": 4},
			"thunder": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 6, "Resistant": 6, "None": 6, "Vulnerable": 1},
			},
		"Ooze": {
			"acid": {
				"Immune": pb, "Resistant": pb, "None": pb//2, "Vulnerable": pb//3},
			"bludgeoning": {
				"Immune": pb, "Resistant": pb, "None": pb//2, "Vulnerable": pb//3},
			"cold": {
				"Immune": pb//6, "Resistant": pb//3, "None": pb, "Vulnerable": pb//2},
			"fire": {
				"Immune": pb//2, "Resistant": pb, "None": pb, "Vulnerable": pb},
			"force": {
				"Immune": 0, "Resistant": pb//2, "None": pb, "Vulnerable": pb},
			"lightning": {
				"Immune": pb//2, "Resistant": pb, "None": pb, "Vulnerable": pb},
			"necrotic": {
				"Immune": pb-1, "Resistant": pb, "None": pb, "Vulnerable": pb//2},
			"piercing": {
				"Immune": pb, "Resistant": pb, "None": pb//6, "Vulnerable": pb//7},
			"poison": {
				"Immune": pb, "Resistant": pb, "None": pb, "Vulnerable": pb//3},
			"psychic": {
				"Immune": pb, "Resistant": pb, "None": pb, "Vulnerable": pb//3},
			"radiant": {
				"Immune": pb//4, "Resistant": pb, "None": pb, "Vulnerable": pb},
			"slashing": {
				"Immune": pb, "Resistant": pb, "None": pb//3, "Vulnerable": pb//6},
			"thunder": {
				"Immune": pb//2, "Resistant": pb, "None": pb, "Vulnerable": pb},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb*3, "Resistant": pb, "None": pb//2, "Vulnerable": pb//3},
			},
		"Orc": {
			"acid": {"Immune": 0, "Resistant": 3, "None": 7, "Vulnerable": 0},
			"bludgeoning": {"Immune": 0, "Resistant": 5, "None": 5, "Vulnerable": 0},
			"cold": {
				"Immune": 0, "Resistant": 3, "None": 7, "Vulnerable": 0},
			"fire": {"Immune": 0, "Resistant": 3, "None": 7, "Vulnerable": 0},
			"force": {"Immune": 0, "Resistant": 2, "None": 8, "Vulnerable": 0},
			"lightning": {"Immune": 0, "Resistant": 3, "None": 7, "Vulnerable": 0},
			"necrotic": {"Immune": 0, "Resistant": 2, "None": 8, "Vulnerable": 0},
			"piercing": {"Immune": 0, "Resistant": 5, "None": 5, "Vulnerable": 0},
			"poison": {"Immune": 1, "Resistant": 4, "None": 5, "Vulnerable": 0},
			"psychic": {"Immune": 0, "Resistant": 2, "None": 8, "Vulnerable": 0},
			"radiant": {"Immune": 0, "Resistant": 2, "None": 8, "Vulnerable": 0},
			"slashing": {"Immune": 0, "Resistant": 5, "None": 5, "Vulnerable": 0},
			"thunder": {"Immune": 0, "Resistant": 3, "None": 7, "Vulnerable": 0},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 0, "Resistant": 5, "None": 5, "Vulnerable": 0},
			},
		"Plant": {
			"acid": {
				"Immune": pb//2, "Resistant": pb-1, "None": 2*pb, "Vulnerable": pb},
			"bludgeoning": {
				"Immune": pb//2, "Resistant": pb-1, "None": 2*pb, "Vulnerable": pb},
			"cold": {
				"Immune": pb//2, "Resistant": pb-1, "None": 2*pb, "Vulnerable": pb},
			"fire": {
				"Immune": pb//8, "Resistant": pb//4, "None": pb, "Vulnerable": 2*pb},
			"force": {
				"Immune": 0, "Resistant": pb//2, "None": pb, "Vulnerable": pb+1},
			"lightning": {
				"Immune": (pb-1)//2, "Resistant": pb//2, "None": pb*2, "Vulnerable": pb},
			"necrotic": {
				"Immune": (pb-1)//4, "Resistant": pb//3, "None": pb, "Vulnerable": pb*2},
			"piercing": {
				"Immune": (pb-1)//3, "Resistant": pb//2, "None": pb+3, "Vulnerable": pb+1},
			"poison": {
				"Immune": pb*2, "Resistant": pb, "None": 0, "Vulnerable": 0},
			"psychic": {
				"Immune": pb, "Resistant": pb, "None": pb, "Vulnerable": 0},
			"radiant": {
				"Immune": pb//2, "Resistant": pb, "None": pb, "Vulnerable": pb//2},
			"slashing": {
				"Immune": 0, "Resistant": pb//3, "None": pb//2, "Vulnerable": pb},
			"thunder": {
				"Immune": 0, "Resistant": pb//2, "None": 2*pb, "Vulnerable": pb},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": pb//4, "Resistant": pb, "None": pb, "Vulnerable": 0},
			},
		"Snakefolk": {
			"acid": {"Immune": 2, "Resistant": 5, "None": 7, "Vulnerable": 1},
			"bludgeoning": {"Immune": 1, "Resistant": 3, "None": 8, "Vulnerable": 3},
			"cold": {"Immune": 1, "Resistant": 3, "None": 7, "Vulnerable": 4},
			"fire": {"Immune": 2, "Resistant": 5, "None": 6, "Vulnerable": 2},
			"force": {"Immune": 1, "Resistant": 2, "None": 10, "Vulnerable": 2},
			"lightning": {"Immune": 1, "Resistant": 4, "None": 8, "Vulnerable": 2},
			"necrotic": {"Immune": 1, "Resistant": 3, "None": 8, "Vulnerable": 3},
			"piercing": {"Immune": 1, "Resistant": 8, "None": 6, "Vulnerable": 0},
			"poison": {
				"Immune": 2*pb, "Resistant": pb, "None": pb//4, "Vulnerable": pb//8},
			"psychic": {"Immune": 1, "Resistant": 4, "None": 8, "Vulnerable": 2},
			"radiant": {"Immune": 0, "Resistant": 3, "None": 9, "Vulnerable": 3},
			"slashing": {"Immune": 1, "Resistant": 6, "None": 6, "Vulnerable": 2},
			"thunder": {"Immune": 1, "Resistant": 3, "None": 9, "Vulnerable": 2},
			"bludgeoning, piercing, and slashing from nonmagical attacks": {
				"Immune": 1, "Resistant": 7, "None": 5, "Vulnerable": 2},
			},
		"Undead": {
			"acid": {
				"Immune": pb//3, "Resistant": pb, "None": pb+2, "Vulnerable": pb//2},
			"bludgeoning": {
				"Immune": pb//3, "Resistant": pb, "None": pb+2, "Vulnerable": pb},
			"cold": {
				"Immune": pb-1, "Resistant": pb, "None": pb//3, "Vulnerable": pb//2},
			"fire": {
				"Immune": pb//3, "Resistant": pb-1, "None": pb+1, "Vulnerable": pb-1},
			"force": {
				"Immune": 0, "Resistant": pb//10, "None": 2*pb, "Vulnerable": pb//3},
			"lightning": {
				"Immune": pb//3, "Resistant": pb-1, "None": pb+1, "Vulnerable": pb//3},
			"necrotic": {
				"Immune": 2*pb, "Resistant": pb, "None": pb//6, "Vulnerable": pb//10},
			"piercing": {
				"Immune": pb//3, "Resistant": pb, "None": pb, "Vulnerable": pb//3},
			"poison": {
				"Immune": 2*pb, "Resistant": pb, "None": 0, "Vulnerable": 0},
			"psychic": {
				"Immune": pb//3, "Resistant": pb//2, "None": pb, "Vulnerable": pb-1},
			"radiant": {
				"Immune": pb//6, "Resistant": pb//3, "None": pb-2, "Vulnerable": 2*pb},
			"slashing": {
				"Immune": pb//3, "Resistant": pb, "None": pb, "Vulnerable": pb//3},
			"thunder": {
				"Immune": pb//3, "Resistant": pb-1, "None": pb+2, "Vulnerable": pb//2},
			"bludgeoning, piercing, and slashing from nonmagical attacks that aren't silvered": {
				"Immune": pb+3, "Resistant": pb, "None": pb, "Vulnerable": 0},
			},
		}

	# Fetch the damage tendencies for the selected race, or use an empty dictionary if the race is not defined
	damage_tendencies = race_damage_tendencies.get(race, {})

	# Randomly determine resistances, immunities, and vulnerabilities based on the damage tendencies
	resistances = []
	immunities = []
	vulnerabilities = []
	for damage_type, tendencies in damage_tendencies.items():
		category = random.choices(list(tendencies.keys()), list(tendencies.values()))[0]
		if category == "Resistant":
			resistances.append(damage_type)
		elif category == "Immune":
			immunities.append(damage_type)
		elif category == "Vulnerable":
			vulnerabilities.append(damage_type)


	# Convert lists to strings
	resistances_str = "\n ".join(resistances) if resistances else "None"
	immunities_str = "\n ".join(immunities) if immunities else "None"
	vulnerabilities_str = "\n ".join(vulnerabilities) if vulnerabilities else "None"

	# Compile the final string
	result = f" <h4>Immunities:</h4> <u>{immunities_str}</u> \n\n<h4>Resistances:</h4> <u>{resistances_str}</u> \n\n<h4>Vulnerabilities:</h4> <u>{vulnerabilities_str}</u>"
	return result

def ConditionImmunities(npc):
	race=npc.race
	background=npc.background
	pb = npc.pb

	# Condition Immunities
	condition_immunities = []

	conditions = [
		"Blinded", "Charmed", "Deafened", "Frightened", "Grappled",
		"Incapacitated", "Paralyzed", "Petrified", "Poisoned", "Prone",
		"Restrained", "Stunned", "Unconscious"
	]

	race_condition_immunities = {
"Human": {
	"Blinded": pb,
	"Charmed": pb,
	"Deafened": pb,
	"Frightened": pb,
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": pb,
	"Restrained": pb,
	"Stunned": pb,
	"Unconscious": pb,
	},
"Aberration": {
	"Blinded": pb*Dice(6),
	"Charmed": pb*Dice(6),
	"Deafened": pb*Dice(6),
	"Frightened": pb*Dice(6),
	"Grappled": pb*Dice(6),
	"Incapacitated": pb*Dice(6),
	"Paralyzed": pb*Dice(6),
	"Petrified": pb*Dice(6),
	"Poisoned": pb*Dice(6),
	"Prone": pb*Dice(6),
	"Restrained": pb*Dice(6),
	"Stunned": pb*Dice(6),
	"Unconscious": pb*Dice(6),
	},
"Aven": {
	"Blinded": pb*5,
	"Charmed": pb,
	"Deafened": pb,
	"Frightened": pb*Dice(2),
	"Grappled": pb*Dice(3),
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": pb*Dice(5),
	"Restrained": pb,
	"Stunned": pb,
	},
"Beast": {
	"Blinded": pb*Dice(4),
	"Charmed": pb,
	"Deafened": pb*Dice(4),
	"Frightened": pb,
	"Grappled": pb*Dice(4),
	"Incapacitated": pb*Dice(4),
	"Paralyzed": pb*Dice(4),
	"Petrified": 0,
	"Poisoned": pb,
	"Prone": pb*Dice(4),
	"Restrained": pb*Dice(4),
	"Stunned": pb*Dice(4),
	},
"Beastfolk": {
	"Blinded": pb*Dice(4),
	"Charmed": pb*Dice(5),
	"Deafened": pb*Dice(4),
	"Frightened": pb*Dice(5),
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(4),
	"Petrified": pb,
	"Poisoned": pb*Dice(3),
	"Prone": pb,
	"Restrained": pb*Dice(2),
	"Stunned": pb*Dice(3),
	},
"Celestial": {
	"Blinded": pb*Dice(10),
	"Charmed": pb*Dice(10),
	"Deafened": pb*Dice(10),
	"Frightened": pb*Dice(10),
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb*Dice(10),
	"Prone": pb,
	"Restrained": pb,
	"Stunned": pb,
	"Unconscious": pb*Dice(3),
	},
"Construct": {
	"Blinded": pb*Dice(6),
	"Charmed": 100,
	"Deafened": pb * Dice(6),
	"Frightened": pb * Dice(4),
	"Exhaustion": pb * Dice(2),
	"Grappled": pb*Dice(2),
	"Incapacitated": pb*Dice(3),
	"Paralyzed": pb*Dice(3),
	"Petrified": pb*Dice(10),
	"Poisoned": 100,
	"Prone": pb,
	"Restrained": pb*Dice(2),
	"Stunned": pb*Dice(3),
	"Unconscious": pb,
	},
"Dragon": {
	"Blinded": pb,
	"Charmed": pb*Dice(5),
	"Deafened": pb,
	"Frightened": pb*Dice(3),
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb*Dice(5),
	"Prone": pb,
	"Restrained": pb,
	"Stunned": pb,
	},
"Dwarf": {
	"Blinded": pb,
	"Charmed": pb,
	"Deafened": pb,
	"Frightened": pb*Dice(5),
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb*Dice(10),
	"Prone": pb,
	"Restrained": pb,
	"Stunned": pb,
	},
"Elf":{
	"Blinded": pb*Dice(2),
	"Charmed": pb*Dice(10),
	"Deafened": pb*Dice(2),
	"Frightened": pb,
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": pb*Dice(2),
	"Restrained": pb*Dice(5),
	"Stunned": pb,
	},
"Elemental": {
	"Blinded": pb,
	"Charmed": pb*Dice(2),
	"Deafened": pb*Dice(2),
	"Frightened": pb,
	"Grappled": pb*Dice(2),
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(2),
	"Petrified": pb*Dice(6),
	"Poisoned": pb*Dice(6),
	"Prone": pb*Dice(3),
	"Restrained": pb*Dice(3),
	"Stunned": pb,
	"Unconscious": pb,
	},
"Fey":{
	"Blinded": pb,
	"Charmed": pb*Dice(10),
	"Deafened": pb,
	"Frightened": pb*Dice(5),
	"Grappled": pb*Dice(2),
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(2),
	"Petrified": pb*Dice(2),
	"Poisoned": pb,
	"Prone": pb,
	"Restrained": pb*Dice(2),
	"Stunned": pb,
	"Unconscious": pb,
	},
"Fiend": {
	"Blinded": pb*Dice(2),
	"Charmed": pb*Dice(5),
	"Deafened": pb,
	"Frightened": pb*Dice(3),
	"Grappled": pb,
	"Incapacitated": pb*Dice(2),
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb*Dice(5),
	"Prone": pb,
	"Restrained": pb*Dice(2),
	"Stunned": pb,
	"Unconscious": pb,
	},
"Giant": {
	"Blinded": 0,
	"Charmed": pb,
	"Deafened": 0,
	"Frightened": pb*Dice(2),
	"Grappled": pb*Dice(6),
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(3),
	"Petrified": pb*Dice(10),
	"Poisoned": pb*Dice(2),
	"Prone": 0,
	"Restrained": pb,
	"Stunned": 0,
	},
"Gnome": {
	"Blinded": pb*Dice(2),
	"Charmed": pb*Dice(5),
	"Deafened": pb*Dice(2),
	"Frightened": pb*Dice(2),
	"Grappled": pb*Dice(2),
	"Incapacitated": pb*Dice(2),
	"Paralyzed": pb*Dice(2),
	"Petrified": pb*Dice(2),
	"Poisoned": pb*Dice(2),
	"Prone": pb*Dice(2),
	"Restrained": pb*Dice(2),
	"Stunned": pb*Dice(2),
	},
"Goblin": {
	"Blinded": pb,
	"Charmed": pb*Dice(5),
	"Deafened": pb,
	"Frightened": pb*Dice(3),
	"Grappled": pb*Dice(4),
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": 0,
	"Restrained": pb*Dice(5),
	"Stunned": pb,
	},
"Halfling": {
	"Blinded": pb,
	"Charmed": pb*Dice(3),
	"Deafened": pb,
	"Frightened": pb*Dice(3),
	"Grappled": pb*Dice(3),
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": pb,
	"Restrained": pb*Dice(3),
	"Stunned": pb,
	},
"Kobold": {
	"Blinded": pb,
	"Charmed": pb,
	"Deafened": pb,
	"Frightened": pb*Dice(10),
	"Grappled": pb*Dice(2),
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": pb,
	"Restrained": pb*Dice(2),
	"Stunned": pb,
	},
"Lizardfolk": {
	"Blinded": pb,
	"Charmed": pb,
	"Deafened": pb,
	"Frightened": pb*Dice(5),
	"Grappled": pb*Dice(2),
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb*Dice(10),
	"Prone": pb,
	"Restrained": pb*Dice(5),
	"Stunned": pb,
	},
"Monstrosity": {
	"Blinded": pb,
	"Charmed": pb*Dice(5),
	"Deafened": pb*Dice(5),
	"Frightened": pb*Dice(2),
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(2),
	"Petrified": pb*Dice(5),
	"Poisoned": pb,
	"Prone": pb,
	"Restrained": pb,
	"Stunned": pb,
	},
"Ooze": {
	"Blinded": pb,
	"Charmed": pb,
	"Deafened": pb*Dice(4),
	"Frightened": pb,
	"Grappled": pb*Dice(5),
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(3),
	"Petrified": pb*Dice(2),
	"Poisoned": pb*Dice(5),
	"Prone": pb*Dice(5),
	"Restrained": pb*Dice(5),
	"Stunned": pb,
	},
"Orc": {
	"Blinded": pb,
	"Charmed": pb,
	"Deafened": pb,
	"Frightened": pb*Dice(5),
	"Grappled": pb,
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb,
	"Poisoned": pb,
	"Prone": pb,
	"Restrained": pb,
	"Stunned": pb,
	},
"Plant": {
	"Blinded": pb*Dice(3),
	"Charmed": pb*Dice(2),
	"Deafened": pb*Dice(2),
	"Frightened": pb,
	"Grappled": pb*Dice(2),
	"Incapacitated": pb,
	"Paralyzed": pb*Dice(4),
	"Petrified": pb,
	"Poisoned": pb*Dice(10),
	"Prone": pb*Dice(2),
	"Restrained": pb*Dice(5),
	"Stunned": pb*Dice(5),
	"Unconscious": pb,
	},
"Snakefolk": {
	"Blinded": pb,
	"Charmed": pb*Dice(5),
	"Deafened": pb*Dice(2),
	"Frightened": pb*Dice(5),
	"Grappled": pb*Dice(2),
	"Incapacitated": pb,
	"Paralyzed": pb,
	"Petrified": pb*Dice(6),
	"Poisoned": 100,
	"Prone": pb*Dice(2),
	"Restrained": pb*Dice(2),
	"Stunned": pb,
	},
"Undead": {
	"Blinded": pb*Dice(6),
	"Charmed": pb*Dice(6),
	"Deafened": pb,
	"Exhaustion": 100,
	"Frightened": 100,
	"Grappled": pb*Dice(6),
	"Incapacitated": pb*Dice(3),
	"Paralyzed": pb*Dice(3),
	"Petrified": pb*Dice(6),
	"Poisoned": 100,
	"Prone": pb*Dice(6),
	"Restrained": pb*Dice(4),
	"Stunned": pb*Dice(3),
	"Unconscious": pb*Dice(6)
	},
"Vampire": {
	"Blinded": pb*Dice(6),
	"Charmed": pb*Dice(6),
	"Deafened": pb,
	"Exhaustion": 100,
	"Frightened": 100,
	"Grappled": pb*Dice(6),
	"Incapacitated": pb*Dice(3),
	"Paralyzed": pb*Dice(3),
	"Petrified": pb*Dice(6),
	"Poisoned": 100,
	"Prone": pb*Dice(6),
	"Restrained": pb*Dice(4),
	"Stunned": pb*Dice(3),
	"Unconscious": pb*Dice(6)
	},

	}



	# Fetch the condition immunities for the selected race, or use an empty dictionary if the race is not defined
	condition_immunity_weights = race_condition_immunities.get(race, {})

	# Randomly determine condition immunities based on the weights
	for condition, weight in condition_immunity_weights.items():
		if weight >= 100 or Dice(weight) > Dice(100):
			condition_immunities.append(condition)

	# Format the output
	if condition_immunities:
		return "\n <h4>Condition Immunities:</h4> <u>"  + "\n ".join(condition_immunities) + "</u>"
	else:
		return ""

def Protections(npc):
	# Select one protection randomly
	selected_protections = set()
	number = PB(Dice(npc.pb))
		## 	or any other logic to determine the number of protections
	for _ in range(number):
		protection = Protection(npc)
		selected_protections.add(protection)
	# Convert set to string for printing
	protections_string = '\n\n'.join(selected_protections)

	return protections_string

def Protection(npc):
	import AtlasPugna.Map_of_Attacks as attacks
	title = npc.title
	race =  npc.race
	background = npc.background
	subrace = npc.subrace
	CON = npc.AS.con_mod
	pb  = npc.pb
	lvl = npc.level
	Type = npc.Type
	gender = npc.gender
	dc = npc.dc

	beast = Beast(npc)

	# Definitions of extra defenses
	StoneCamouflage= Entry_Text("Stone Camouflage.",
			f"{title} has advantage on Dexterity (Stealth) checks made to hide in rocky terrain, stone constructions, and caves."
			)
	WaterCamouflage = Entry_Text("Water Camouflage",
		f"{title} is invisible while fully immersed in water.")
	TwoHeaded = Entry_Text("Two-Headed",
		f"{title} has advantage on Wisdom (Perception) checks and on saving throws against being blinded, charmed, deafened, frightened, stunned, or knocked unconscious.")
	Illumination = Entry_Text("Illumination",
			f"{title} sheds bright light in a 5 to {Dice(pb)*10}-foot radius and dim light for an additional number of ft. equal to the chosen radius. {title} can alter the radius, turn it off, or turn it on, as a bonus action."
			)
	Etherealness= Entry_Text("Etherealness",
		f"{title} enters the Ethereal Plane from the Material Plane, or vice versa. It is visible on the Material Plane while it is in the Border Ethereal, and vice versa, yet it can't affect or be affected by anything on the other plane.")
	DistressSpores = Entry_Text("Distress Spores",
		f"When {title} takes damage, any other {npc.race} within 240 feet of it can sense its pain.")
	Brave = Entry_Text("Brave",
		f"{title} has advantage on saving throws against being frightened.")
	Parry = Entry_Text("Parry",
		f"{title} adds 2 to its AC against one melee attack that would hit it. To do so, {title} must see the attacker and be wielding a melee weapon.")
	TelepathicBond = Entry_Text("Telepathic Bond",
		f"While {title} is on the same plane of existence as its master, it can magically convey what it senses to its master, and the two can communicate telepathically.")
	SpellImmunity = Entry_Text("Spell Immunity",
		random.choice([
			f"{title} is immune to three spells: Fireball, Heat Metal, and Lightning Bolt.",
			f"{title} is immune to three spells: Magic Missile, Silvery Barbs, and Counterspell.",
			f"{title} is immune to three spells: Cause Fear, Charm Person, and Sleep.",
			]))
	FalseApperance = Entry_Text("False Apperance",
		f"While {title} remains motionless in rest, it is indistinguishable from a mundane object or feature of the environment.")
	DamageTransfer= Entry_Text("Damage Transfer",
		f"While it is grappling a creature, {title} takes only half the damage dealt to it, and the creature grappled by {title} takes the other half."
		)
	SuperiorInvisibility = Entry_Text("Superior Invisibility",
		f"{title} magically turns invisible until its concentration ends (as if concentrating on a spell). Any equipment {title} wears or carries is invisible with it.")
	EntanglingPlants= Entry_Text(
		"Entangling Plants",
		f"Grasping roots and vines sprout in a 15-foot radius centered on {title}, withering away after 1 minute. For the duration, that area is difficult terrain.")
	Disintegration = Entry_Text(f"Disintegration",
		f"If {title} dies, its body disintegrates, leaving behind its weapons and anything else it was carrying.")
	AxiomaticMind= Entry_Text(f"Axiomatic Mind",
		f"{title} can't be compelled to act in a manner contrary to its nature or its instructions.")
	AntimagicSusceptibility = Entry_Text(
		f"Antimagic Susceptibility",
		f"{title} is incapacitated while in the area of an antimagic field. If targeted by dispel magic, {title} must succeed on a Constitution saving throw against the caster's spell save DC or fall unconscious for 1 minute.")
	MagicResistance = Entry_Text(
		f"Magic Resistance",
		f"{title} has advantage on saving throws against magical effects.")
	ChangeShape = select1([Entry_Text(
			f"Change Shape",
			f"{title} magically polymorphs into a humanoid or {beast} form, or back into its true form. It reverts to its true form if it dies. Any equipment it is wearing or carrying is absorbed or borne by the new {beast} form ({title}'s choice). \n\t In {beast} form, {title} retains its game statistics and ability to speak, but its AC, movement modes, Strength, Dexterity, and other actions are replaced by those of the new form, and it gains any statistics and capabilities (except class features, legendary actions, and lair actions) that the {beast} form has but that it lacks.")
		, Entry_Text(
			f"Change Shape",
			f"{title} magically polymorphs into a humanoid or beast that has a challenge rating no higher CR{pb}, or back into its true form. It reverts to its true form if it dies. Any equipment it is wearing or carrying is absorbed or borne by the new form ({title}'s choice). \n\t In a new form, {title} retains its alignment, hit points, Hit Dice, ability to speak, proficiencies, Legendary Resistance, lair actions, and Intelligence, Wisdom, and Charisma scores, as well as this action. Its statistics and capabilities are otherwise replaced by those of the new form, except any class features or legendary actions of that form.")
		])
	Shapechanger = Entry_Text(
		f"\n - Shapechanger",
		(f"{npc.title} can use its action to polymorph into their standard form, into a {beast} hybrid, or into a {beast}."+
		random.choice ([
			"Other than its size, its statistics are the same in each form.",
			f"{title} takes the Hit Points and stats of the {beast} form, but retains its Intelligence score.",
			f"{title} game statistics are replaced by the statistics of the beast, but {title} retains alignment, personality, and Intelligence, Wisdom, and Charisma scores."
			]) +
		random.choice ([
			"Any equipment it is wearing or carrying isn't transformed."
			]) +
		random.choice ([
			f"They reverts to its true form if it dies."
			])
		))
	acidic_blood = Entry_Text(
		f"Acidic Blood",
		f"Any creature that hits {title} with a melee attack while within 5 feet of it takes 2d6 acid damage.")
	alien_mind = Entry_Text(f"Alien Mind",
		f"{npc.title} has advantage on saving throws against being charmed or dominated.")
	aberrant_ground = Entry_Text(
		f"Aberrant Ground",
		f"The ground in a 10-foot radius around the {npc.race} is doughlike difficult terrain. Each creature that starts its turn in that area must succeed on a DC {8+int(npc.pb)+int(npc.spellcasting_ability_mod)} Strength saving throw or have its speed reduced to 0 until the start of its next turn.")
	arcane_awareness = Entry_Text(f"Arcane Awareness",
		f"{npc.title} has advantage on Intelligence (Arcana) checks to recognize or recall information about spells or magical effects.")
	berserker_resistance = Entry_Text(f"Berserker Resistance",
		f"{npc.title} has resistance to bludgeoning, piercing, and slashing damage.")
	diabolic_resilience = Entry_Text(f"Diabolic Resilience",
		f"{npc.title} has resistance to bludgeoning, piercing, and slashing damage from non-magical attacks not made with silvered weapons.")
	etherealness = Entry_Text(f"Etherealness",
		f"{npc.title} can shift partially into the Ethereal Plane, granting it resistance to non-magical attacks and the ability to move through solid objects until the end of their next turn.")
	fey_ancestry = Entry_Text(
		f"Fey Ancestry",
		f"{title} has advantage on saving throws against being charmed, and magic can't put {title} to sleep.")
	hellish_rebuke = Entry_Text(f"Hellish Rebuke",
		f"Once per turn, when {title} takes damage from a melee attack, it can cause flames to engulf its attacker, dealing fire 1d6 damage in return.")
	infernal_wisdom = Entry_Text(f"Infernal Wisdom",
		f"{title} has advantage on saving throws against being charmed or frightened."
		)
	lore_preservation = Entry_Text(f"Lore Preservation",
		f"Once per day, {title} can reroll a failed Intelligence check, taking the new roll.")
	magic_resistance = Entry_Text(f"Magic Resistance",
		f"{npc.title} has advantage on saving throws against spells and other magical effects.")
	mental_fortitude = Entry_Text(f"Mental Fortitude",
		f"The {npc.race} has advantage on saving throws against being charmed or frightened.")
	meticulous = Entry_Text(f"Meticulous",
		f"{title} has advantage on Investigation checks when analyzing texts or searching for information.")
	otherwordly_perception = Entry_Text(
		f"Otherworldly Perception",
		f"{npc.title} can sense the presence of invisible or hidden creatures within 60 feet of it.")
	parry = Entry_Text(
		f"Parry",
		f"As a reaction, {npc.title} can add {PB(pb)} to its AC against one melee attack that would hit it.")
	psychic_feedback = Entry_Text(f"Psychic Feedback",
		f"Any creature that attempts to read {npc.title}'s thoughts or communicate telepathically with it takes {Dice(pb//2)}d8 psychic damage.")
	regeneration = Entry_Text(
		f"Regeneration",
		f"{title} regains {abs(CON + pb)} hit points at the start of its turn" \
		+ random.choice(['.', ' if it has at least 1 hit point.']) \
		+ random.choice([
			f"If {title} takes acid or fire damage, this trait doesn't function at the start of its next turn.",
			f"If {title} takes {attacks.Damage()} damage, this trait doesn't function at the start of its next turn."
			]) \
		+ f"{title} dies only if it starts its turn with 0 hit points and doesn't regenerate."
		)
	relentless = Entry_Text(
		f"Relentless",
		f"(Recharges after a Short or Long Rest). \n\t If {npc.title} takes {npc.pb+CON} damage or less that would reduce it to 0 hit points, it is reduced to 1 hit point instead.")
	telepathic_shield = Entry_Text(
		f"Telepathic Shield",
		f"{npc.title} has advantage on intelligence, wisdom, and charisma saving throws against spells and other magical effects that target its mind.")
	spell_reflection = Entry_Text(
		f"Spell Reflection",
		f"If {npc.title} makes a successful saving throw against a spell, or a spell attack misses it, {npc.title} can choose another creature (including the spellcaster) it can see within 30 feet of it. The spell targets the chosen creature instead of {npc.title}. If the spell forced a saving throw, the chosen creature makes its own save. If the spell was an attack, the attack roll is rerolled against the chosen creature")
	snow_camouflage = Entry_Text(f"Snow Camouflage",
		f"{title} has advantage on Dexterity (Stealth) checks made to hide in snowy terrain.")
	sure_footed = Entry_Text(f"Sure-Footed",
		f"{title} has advantage on Strength and Dexterity saving throws made against effects that would knock it prone.")
	shielded_mind = Entry_Text(f"Shielded Mind",
		f"{title} is immune to any effect that would sense its emotions, read its thoughts, or detect its location.")
	nimble_scape = Entry_Text(
		f"Nimble Scape",
		f"{npc.title} can take the Disengage or Hide action as a bonus action on each of its turns.")
	freeze = Entry_Text(
		f"Freeze",
		f"If the {npc.race} takes cold damage, it partially freezes; All its speed is reduced by 20 feet until the end of its next turn.")
	slippery = Entry_Text(
		f"Slippery",
		f"{npc.title} has advantage on ability checks and saving throws made to escape a grapple.")
	SwampCamouflage =  Entry_Text(f"Swamp Camouflage",
		f"{npc.title} has advantage on Dexterity (Stealth) checks made to hide in swampy terrain.")
	LabyrinthineRecall = Entry_Text(f"Labyrinthine Recall",
		f"{title} can perfectly recall any path it has traveled.")
	Burden = Entry_Text(f"{race} of Burden",
		f"{title} is considered to be a {sizer(npc.height)} creature for the purpose of determining its carrying capacity.")
	UnusualNature = Entry_Text(
		"Unusual Nature",
		f"{npc.title} doesn't require air, food, drink, or sleep.")
	MucousCloud = Entry_Text(f"Mucous Cloud",
					f"While underwater or wet, the skin of {title} is surrounded by dense mucus. A creature that touches {title} or that hits it with a melee attack while within 5 ft. of it must make a DC {8+npc.pb+CON} Constitution saving throw. On a failure, the creature is diseased for {Dice(4)} hours. The diseased creature gains a level of exhaustion for the duration."
					)
	Inscrutable = Entry_Text(
		"Inscrutable",
		f"{npc.title} is immune to any effect that would sense its emotions or read its thoughts, as well as any divination spell that it refuses. Wisdom (Insight) checks made to ascertain {npc.title}'s intentions or sincerity have disadvantage.")
	AntimagicSusceptibility = Entry_Text(
		"Antimagic Susceptibility",
		f"{title} is incapacitated while in the area of an antimagic field. If targeted by dispel magic, {title}  must succeed on a Constitution saving throw against the caster's spell save DC or fall unconscious for 1 minute."
		)
	FalseAppearance = Entry_Text(
		"False Appearance",
		f"While {title} remains motionless, it is indistinguishable from a normal inanimate object, such as a statue, rock, or plant."
		)
	IllusoryAppearance = Entry_Text("Illusory Appearance",
		(f"{title} covers herself and anything they are wearing or carrying with a magical illusion that makes {gender} look like other creature of their general size and shape. The effect ends if {title} takes a bonus action to end it or if {gender} dies."
		f"The changes wrought by this effect fail to hold up to physical inspection. For example, a hag could appear to have no claws, but someone touching her hand might feel the claws. Otherwise, a creature must take an action to visually inspect the illusion and succeed on a DC {dc} Intelligence (Investigation) check to discern that {title} is disguised."
		))
	ImmutableForm = Entry_Text(f"Immutable Form",
		f"{title} is immune to any spell or effect that would alter its form.")
	LightningAbsorption = Entry_Text(f"Lightning Absorption",
		f"Whenever {title} is subjected to lightning damage, it takes no damage and instead regains a number of hit points equal to the lightning damage dealt.")
	Rejuvenation = Entry_Text(f"Rejuvenation",
		f"You might decide that {title} in your campaign is nearly impossible to destroy. Their life essence might be preserved somehow into a vessel. \n\t If the essence-preserving vessel of {title} is intact, {npc.gender} gains a new body in {Dice(pb)}d10 days, regaining all its hit points and becoming active again. The new body appears within 5 feet of the object.")


	possible_Protections = []
	# Dictionary to store possible extra defenses for each background
	Protections_background = {
		"Artist":		[IllusoryAppearance,					Rejuvenation,		Inscrutable,		Brave,				SpellImmunity,		SuperiorInvisibility,					ChangeShape,		MagicResistance,	],
		"Bandit":		[Parry,				SuperiorInvisibility,					],
		"Barbarian":	[ChangeShape,		DamageTransfer,	EntanglingPlants,	Shapechanger,		ChangeShape,		regeneration		],
		"Berserker": 	[MagicResistance,	relentless,berserker_resistance],
		"Bard":			[IllusoryAppearance,					ChangeShape,		Brave,				Parry,				SpellImmunity,		SuperiorInvisibility,					],
		"Charlatan":	[IllusoryAppearance,					Inscrutable,		Brave,				Parry,				SuperiorInvisibility,					ChangeShape,		MagicResistance,	],
		"Criminal":		[IllusoryAppearance,					SuperiorInvisibility,					ChangeShape,		],
		"Crafter":		[StoneCamouflage,	Illumination,		IllusoryAppearance,					SpellImmunity,		MagicResistance,	],
		"Commoner":		[Brave,				],
		"Cleric":		[Illumination,		Etherealness,		],
		"Cultist":		[Illumination,		Rejuvenation,		Etherealness,		TelepathicBond,	SpellImmunity,		SuperiorInvisibility,					EntanglingPlants,	Disintegration,	AxiomaticMind,		ChangeShape,		MagicResistance,	regeneration,		],
		"Druid":		[Illumination,		ChangeShape,		Etherealness,		EntanglingPlants,	ChangeShape,		Shapechanger,		regeneration],
		"Expert":		[SpellImmunity,		SuperiorInvisibility,					MagicResistance,	],
		"Explorer":		[Illumination,		ChangeShape,		Brave,				SuperiorInvisibility,					EntanglingPlants,	ChangeShape,		MagicResistance,	],
		"Guard":		[Illumination,		Brave,				Parry,				SpellImmunity,		],
		"Healer":		[regeneration,		],
		"Hero":			[Illumination,		Brave,				Parry,				SpellImmunity,		MagicResistance,	regeneration],
		"Hunter":		[StoneCamouflage,	WaterCamouflage,	Rejuvenation,		ChangeShape,		SuperiorInvisibility,					EntanglingPlants,	],
		"Knight":		[Illumination,		Brave,				Parry,				SpellImmunity,		MagicResistance,	],
		"Mage":			[Illumination,		IllusoryAppearance,					Rejuvenation,		SpellImmunity,		SuperiorInvisibility,					ChangeShape,		MagicResistance,	],
		"Monk":			[Inscrutable,		Etherealness,		Brave,		Parry,				SpellImmunity,		DamageTransfer,	SuperiorInvisibility,					AxiomaticMind,		MagicResistance,	regeneration],
		"Ninja":		[StoneCamouflage,	IllusoryAppearance,					Parry,				FalseApperance,	DamageTransfer,	SuperiorInvisibility,					EntanglingPlants,	Disintegration,	ChangeShape,		MagicResistance,	],
		"Noble": 		[Parry,				parry,				],
		"Pirate":		[Brave,				Parry,				SuperiorInvisibility,					],
		"Priest":		[Illumination,		Etherealness,		AxiomaticMind,		],
		"Ranger":		[StoneCamouflage,	WaterCamouflage,	ChangeShape,		FalseApperance,	SuperiorInvisibility,EntanglingPlants,	Shapechanger,		ChangeShape,		],
		"Rogue":		[ChangeShape,		SuperiorInvisibility,					],
		"Scholar":		[Illumination,		Etherealness,		SuperiorInvisibility,					LabyrinthineRecall,	spell_reflection, arcane_awareness, mental_fortitude, lore_preservation, meticulous, shielded_mind],
		"Shaman": 		[Illumination,		Rejuvenation,		LightningAbsorption,					ChangeShape,		Etherealness,		EntanglingPlants,	Shapechanger,		ChangeShape,		Shapechanger,		MagicResistance,	regeneration,],
		"Spy":			[IllusoryAppearance,					Inscrutable,		Brave,				FalseApperance,	SuperiorInvisibility,					AxiomaticMind,		ChangeShape,		],
		"Sorcerer":		[Illumination,		LightningAbsorption,					SpellImmunity,		MagicResistance,	],
		"Soldier":		[Brave,				Parry,				AxiomaticMind,		],
		"Traveler":		[StoneCamouflage,	Illumination,		Etherealness,		Brave,		SuperiorInvisibility,					EntanglingPlants,	ChangeShape,		],
		"Prankster":	[IllusoryAppearance,					Brave,				SuperiorInvisibility,					ChangeShape,		],
		"Warlock":		[IllusoryAppearance,					Rejuvenation,		Etherealness,		TelepathicBond,	SpellImmunity,		SuperiorInvisibility,					EntanglingPlants,	AxiomaticMind,		ChangeShape,		MagicResistance,	],
		"Warrior":		[Parry,				Brave,		],
		"Witch":		[IllusoryAppearance,					Rejuvenation,		ImmutableForm,		ChangeShape,		Etherealness,		SpellImmunity,		EntanglingPlants,	Disintegration,	Shapechanger,		ChangeShape,		MagicResistance,	regeneration],
		"Wizard":		[Illumination,		IllusoryAppearance,					Rejuvenation,		SpellImmunity,		SuperiorInvisibility,					MagicResistance,	],
		}

	# Dictionary to store possible extra defenses for each race
	Protections_race = {
		"Aberration": [
			StoneCamouflage,	IllusoryAppearance,	Rejuvenation,		LightningAbsorption,					ImmutableForm,		Inscrutable,		MucousCloud,		TwoHeaded,	DistressSpores,		SpellImmunity,		AxiomaticMind,			AntimagicSusceptibility,						MagicResistance,		regeneration,			slippery, shielded_mind, relentless,spell_reflection, aberrant_ground, magic_resistance, regeneration, telepathic_shield, otherwordly_perception, 			etherealness, 		acidic_blood, 		psychic_feedback, 	alien_mind],
		"Aven":[		Etherealness,		Brave,				SpellImmunity,		MagicResistance,		],
		"Beast":[		ChangeShape,		Etherealness,		MagicResistance,	SwampCamouflage,		regeneration,			Burden,			slippery,			sure_footed],
		"Beastfolk": [	ChangeShape,		fey_ancestry,		Brave,		SpellImmunity,		MagicResistance,		SwampCamouflage,		regeneration,			Burden,			slippery, fey_ancestry,sure_footed, LabyrinthineRecall],
		"Celestial": [	Illumination,		IllusoryAppearance,	Rejuvenation,		Inscrutable,		ChangeShape,		Illumination,		Etherealness,		Parry,				SpellImmunity,		Disintegration,			AxiomaticMind,			AntimagicSusceptibility,						regeneration,			shielded_mind],
		"Catfolk": [	fey_ancestry,		Brave,				Parry,				MagicResistance,		],
		"Construct": [	Illumination,		FalseApperance,		Rejuvenation,		LightningAbsorption,					FalseAppearance,	AntimagicSusceptibility,				TwoHeaded,			Illumination,		TelepathicBond,		SpellImmunity,		FalseApperance,			DamageTransfer,			Disintegration,			AxiomaticMind,			AntimagicSusceptibility,						MagicResistance,		regeneration,			magic_resistance],
		"Dragon":[		Rejuvenation,		LightningAbsorption,					ImmutableForm,		ChangeShape,		TwoHeaded,			DamageTransfer,			MagicResistance,		magic_resistance],
		"Dwarf": [		StoneCamouflage,	Brave,				],
		"Elf": [		Inscrutable,		fey_ancestry,		Brave,		Parry,				fey_ancestry,			],
		"Elemental":[	StoneCamouflage,	WaterCamouflage,	Illumination,		FalseApperance,		Rejuvenation,		LightningAbsorption,					ImmutableForm,		FalseAppearance,	SpellImmunity,		FalseApperance,			DamageTransfer,			Disintegration,			AntimagicSusceptibility,						freeze],
		"Fey": [		Illumination,		IllusoryAppearance,	Rejuvenation,		ImmutableForm,		Inscrutable,		ChangeShape,		fey_ancestry,		Illumination,		DistressSpores,		SpellImmunity,		Disintegration,			AntimagicSusceptibility,						MagicResistance,		fey_ancestry,			nimble_scape,		regeneration],
		"Fiend": [		Illumination,		IllusoryAppearance,	Rejuvenation,		ImmutableForm,		Inscrutable,		MucousCloud,		TwoHeaded,			Etherealness,		TelepathicBond,		SpellImmunity,		Disintegration,			AxiomaticMind,			LabyrinthineRecall,		slippery,				Burden,			relentless,			regeneration,			magic_resistance,			regeneration,			otherwordly_perception, etherealness, infernal_wisdom],
		"Gnome": [		fey_ancestry,		Brave,				SpellImmunity,		],
		"Giant":	[	StoneCamouflage,	MagicResistance,	regeneration,			],
		"Goblin": [		fey_ancestry,		Brave,				slippery, 				nimble_scape],
		"Human": [		Brave,				Parry,				],
		"Kobold": [		Brave,		],
		"Lizardfolk":[	Inscrutable,		MucousCloud,		Brave,		Parry,				MagicResistance,		SwampCamouflage, 		slippery, freeze,relentless,regeneration],
		"Monstrosity":[	Rejuvenation,		Inscrutable,		ChangeShape,		TwoHeaded,			MagicResistance,		regeneration,			],
		"Ooze":[		StoneCamouflage,	WaterCamouflage,	Illumination,		FalseApperance,		Rejuvenation,		LightningAbsorption,					ImmutableForm,		MucousCloud,		SpellImmunity,		FalseApperance,			Disintegration,			regeneration,			],
		"Orc": [		Brave,				Parry,				Burden,					relentless],
		"Plant":[		FalseApperance,		Rejuvenation,		ImmutableForm,		FalseAppearance,	AntimagicSusceptibility,				MucousCloud,		DistressSpores,		SpellImmunity,		FalseApperance,			DamageTransfer,			MagicResistance,		regeneration,			],
		"Snakefolk":[	IllusoryAppearance,	Inscrutable,		SpellImmunity,		DamageTransfer,			AxiomaticMind,			SwampCamouflage, 		slippery],
		"Undead": [		Illumination,		IllusoryAppearance,	Rejuvenation,		FalseAppearance,	ChangeShape,		TwoHeaded,			Illumination,		Etherealness,		TelepathicBond,		SpellImmunity,		Disintegration,			AxiomaticMind,			AntimagicSusceptibility,						MagicResistance,		UnusualNature,			],
		"Vampire": [		Illumination,		IllusoryAppearance,	Rejuvenation,		FalseAppearance,	ChangeShape,		TwoHeaded,			Illumination,		Etherealness,		TelepathicBond,		SpellImmunity,		Disintegration,			AxiomaticMind,			AntimagicSusceptibility,						MagicResistance,		UnusualNature,			],
	}

	# Dictionary to store possible extra defenses for each subrace
	Protections_subrace = {
		#"":[],
		"Armored Bear":[	Brave,		Parry,				],
		"Animated Armor":[	Parry,				],
		"Alien Spawn":[	TelepathicBond,		],
		"Archon":[		TelepathicBond,		],
		"Archangel":[	TelepathicBond,		],
		"Asura":[		TwoHeaded,	],
		"Celestial Stag":[	Illumination,		],
		"Colored Chamalfolk":[	StoneCamouflage,	IllusoryAppearance,			],
		"Death Knight":[	Parry,				],
		"Depth Dominators":[	TelepathicBond,	],
		"Deer Spirit":[	Illumination,		],
		"Deva":[		TwoHeaded,	],
		"Doppelganger":[IllusoryAppearance,	],
		"Dark Elf":[	IllusoryAppearance,	],
		"Etherian":[	Illumination,		],
		"Eladrin":[		Illumination,		],
		"Eldritch Horror": [Rejuvenation,		],
		"Fallen Angel":[	Illumination,		],
		"Firbolg": [	StoneCamouflage,	FalseApperance,	],
		"Forest God":[	FalseApperance,		DistressSpores,		],
		"Forest":	[	DistressSpores,		],
		"Forester":	[	DistressSpores,		],
		"Feywild Elf":[	IllusoryAppearance,			],
		"Frogfolk":[	WaterCamouflage,	],
		"Galaxian":[	Illumination,		],
		"Golden Lion":[	Illumination,		],
		"Genasi":[		Illumination,		],
		"Genie":[		Illumination,		],
		"Golden Lion":[	Illumination,		],
		"Golem":[		StoneCamouflage,	],
		"Hyperian":[	Illumination,		],
		"Hydrakin":[	WaterCamouflage,	],
		"Islander": [	WaterCamouflage,	],
		"Kitsune Fox":[	Illumination,		],
		"Kitsune":[		Illumination,		],
		"Kobold":[		StoneCamouflage,	],
		"Leonid":[			Illumination,		],
		"Living Spell":[	SpellImmunity,	Illumination,		],
		"Living Totem":[	SpellImmunity,	Illumination,		],
		"Magmaforged":[		Illumination,		],
		"Merfolk":[			Parry,				],
		"Monkey King":[		Parry,				],
		"Mindhive":[		TelepathicBond,		],
		"Moon Jackal":[		Illumination,		],
		"Moon Elf":[		Illumination,		],
		"Nephilim":[		Illumination,		],
		"Nightmare":[		IllusoryAppearance,	],
		"Nomad Elf":[		WaterCamouflage,	],
		"Ogre":[			StoneCamouflage,	],
		"Parasyte":[		TelepathicBond,		DamageTransfer,			],
		"Planetar":[		Parry,				],
		"Promethean":[		Illumination,		],
		"Riverfolk":[		WaterCamouflage,	],
		"Salamandrian":[	Illumination,		],
		"Seraph":[			Parry,				],
		"Symbioid":[		TelepathicBond,		DamageTransfer,			],
		"Sun Scarab":[		Illumination,		],
		"Stone Giant":[		StoneCamouflage,	],
		"Storm Giant":[		Illumination,		],
		"Sphynx":[			Inscrutable,		Inscrutable,		Inscrutable,		Inscrutable,		Inscrutable,		Illumination,		],
		"Swamp":[			WaterCamouflage,	],
		"Swamp Crocfolk":[	WaterCamouflage,	],
		"Singing Lotus":[	WaterCamouflage,	],
		"Treetop":[			DistressSpores,		],
		"Throne":[			TwoHeaded,	],
		"Titan":[			TwoHeaded,	],
		"Troll": [			StoneCamouflage,	FalseApperance,	],
		"Uranians":[		Illumination,		],
		"Monkey King":[		DamageTransfer,		],
		"Minotaur":[		LabyrinthineRecall,	],
		"Mountain":[		StoneCamouflage,	],
		"Lone Lover":[		regeneration,		],
		"Githyanki":[		Parry,				],
		"Githzerai":[		Parry,				],
		"Throne":[			TelepathicBond,		],
		"Sun Elf":[			Illumination,		],
		"Shapeshifters":[	FalseApperance,		],
		"Sphynx":[			StoneCamouflage,	],
		"Stout":[			StoneCamouflage,	],
		"Planetar":[		TelepathicBond,		],
		"Insectfolk":[		TelepathicBond,		],
		"Vulture Spirit":[	Illumination,		],
		"Ouroboros's Spawn":[	DamageTransfer,			],
		"Werewolf":[		TelepathicBond,		],
		"Wood Elf":[		DistressSpores,		],
		"Wild Elf":[		WaterCamouflage,	DistressSpores,		],
		}

	if "Ettin" in Type:
		possible_Protections += TwoHeaded

	# Fetch the extra defenses for the selected race and background
	possible_Protections += Protections_race.get(race, [])
	possible_Protections += Protections_subrace.get(subrace, [])
	possible_Protections += Protections_background.get(background, [])
	possible_Protections = list(set(possible_Protections))

	if not possible_Protections:
		return "<u>None</u>"

	# Select one protection randomly
	selected_protection = random.choice(possible_Protections)
	return selected_protection

def Beast(npc):
		'''
		Generate a beast [string] for an NPC based on their race, subrace, background.
		For transformations.

		Parameters:
		npc (object): An object representing the NPC with attributes like race, subrace, background, and level.
		defined in npc_class.py

		Returns:
		str: A formatted string of selected skills.
		'''

		race = npc.race
		subrace = npc.subrace
		background = npc.background
		title = npc.title

		beasts = ["wolf"]


		# Dictionary to store possible extra skills for each background
		beast_background = {
			"Bandit": 	["rat","crow"],
			"Barbarian":["bear","wolf",'tiger',"boar"],
			"Berserker":["wolf","bear","tiger","hyena"],
			"Commoner": ["dog","goat"],
			"Criminal": ["rat", "cat"],
			"Guard":	["mastiff"],
			"Hero":		["lion","griffon"],
			"Hunter":	["wolf","hawk"],
			"Knight":	["lion","griffon"],
			"Monk": 	["monkey"],
			"Ninja": 	["spider"],
			"Noble": 	["wolf","falcon"],
			"Pirate": 	["shark"	],
			"Rogue": 	["spider"	],
			"Spy": 		["spider", "rat"	],
			"Scholar":   ["owl"],
			"Traveler": ["falcon"	],
			"Warrior": 	["hound", "bull"],
		}

		# Dictionary to store possible extra beast for each race
		beast_race = {
			"Aberration": ["kraken", "Giant Octopus", "Giant Squid",],
			"Aven":       ["crow", "falcon", "owl", "eagle"],
			"Beast":      ["crow", "bear", "boar", "wolf"],
			"Beastfolk":  ["crow", "bear", "tiger", "boar"],
			"Catfolk":    ["cat", "lion", "panther", "tiger", "feline"],
			"Celestial":  ["eagle", "vulture", "pegasus", "unicorn"],
			"Construct":  ["horse", "camel", "golem"],
			"Dragon":     ["lizard", "wyvern", "drake"],
			"Dwarf":      ["mole", "bear", "badger", "goat"],
			"Elemental":  ["lizard", "salamander", "phoenix"],
			"Elf":        ["bird", "Giant Butterfly", "stag", "unicorn"],
			"Fiend":      ["wolf", "bat", "rat", "hellhound","wolf", "Dire Wolf", "hellhound"],
			"Fey":        ["bird", "lizard", "Giant Butterfly", "Giant Dragonfly", "stag"],
			"Goblin":     ["bat", "rat", "toad", "worg"],
			"Gnome":      ["badger", "beaver", "rabbit", "squirrel"],
			"Giant":      ["bear", "ape", "mammoth", "giant eagle"],
			"Halfling":   ["bear", "otter", "dog"],
			"Human":      ["wolf", "bear", "tiger"],
			"Kobold":     ["lizard", "drake", "dragon"],
			"Lizardfolk": ["lizard", "velociraptor", "crocodile"],
			"Monstrosity":["lion", "bear", "hydra", "manticore"],
			"Ooze":       ["bear", "slime",],
			"Orc":        ["bear", "wolf", "boar", "worg"],
			"Plant":      ["bear", "snake", "treant", "shambling mound"],
			"Snakefolk":  ["snake", "python", "cobra"],
			"Undead":     ["snake", "spider", "rat", "ghoul", "wraith"],
			"Vampire":    ["wolf", "bat", "cat", "crow"],
		}



		beast_subrace = {
			"Vampire":  ["Wolf", "Bat", "Dire Wolf"],
			"Werewolf": ["Wolf", "Dire Wolf"],

			}

		# Fetch the extra skills for the selected race and background
		beasts = list(set(
			beast_race.get(npc.race, []) +
			beast_subrace.get(npc.subrace, []) +
			beast_background.get(npc.background, [])))


		# Select and format skills
		beast = random.choice(beasts)
		if not beast:
			beast = "wolf"

		return beast



def Invocation(npc):
		'''
		Generate a beast [string] for an NPC based on their race, subrace, background.
		For Invocations.

		Parameters:
		npc (object): An object representing the NPC with attributes like race, subrace, background, and level.
		defined in npc_class.py

		Returns:
		str: A formatted string of selected skills.
		'''

		race = npc.race
		subrace = npc.subrace
		background = npc.background
		title = npc.title

		beasts = ["wolf"]


		# Dictionary to store possible extra skills for each background
		beast_background = {
			"Bandit": 	["rat","crow"],
			"Barbarian":["bear","wolf",'tiger',"boar"],
			"Berserker":["wolf","bear","tiger","hyena"],
			"Commoner": ["dog","goat"],
			"Criminal": ["rat", "cat"],
			"Guard":	["mastiff"],
			"Hero":		["lion","griffon"],
			"Hunter":	["wolf","hawk"],
			"Knight":	["lion","griffon"],
			"Monk": 	["monkey"],
			"Ninja": 	["spider"],
			"Noble": 	["wolf","falcon"],
			"Pirate": 	["shark"	],
			"Rogue": 	["spider"	],
			"Spy": 		["spider", "rat"	],
			"Scholar":   ["owl"],
			"Traveler": ["falcon"	],
			"Warrior": 	["hound", "bull"],
		}

		# Dictionary to store possible extra beast for each race
		beast_race = {
			"Aberration": ["kraken", "aboleth", "beholder", "mind flayer"],
			"Aven":       ["crow", "falcon", "owl", "eagle"],
			"Beast":      ["crow", "bear", "boar", "wolf"],
			"Beastfolk":  ["crow", "bear", "tiger", "boar"],
			"Catfolk":    ["cat", "lion", "panther", "tiger", "feline"],
			"Celestial":  ["eagle", "vulture", "pegasus", "unicorn"],
			"Construct":  ["horse", "camel", "golem"],
			"Dragon":     ["lizard", "wyvern", "drake"],
			"Dwarf":      ["mole", "bear", "badger", "goat"],
			"Elemental":  ["lizard", "salamander", "phoenix"],
			"Elf":        ["bird", "butterfly", "stag", "unicorn"],
			"Fiend":      ["wolf", "bat", "rat", "hellhound"],
			"Fey":        ["bird", "lizard", "butterfly", "dragonfly", "stag"],
			"Fiend":	  ["wolf" "Dire Wolf"],
			"Goblin":     ["bat", "rat", "toad", "worg"],
			"Gnome":      ["badger", "beaver", "rabbit", "squirrel"],
			"Giant":      ["bear", "ape", "mammoth", "giant eagle"],
			"Halfling":   ["bear", "otter", "dog"],
			"Human":      ["wolf", "bear", "tiger", "horse"],
			"Kobold":     ["lizard", "drake", "dragon"],
			"Lizardfolk": ["lizard", "velociraptor", "crocodile"],
			"Monstrosity":["lion", "bear", "hydra", "manticore"],
			"Ooze":       ["bear", "slime", "gelatinous cube"],
			"Orc":        ["bear", "wolf", "boar", "worg"],
			"Plant":      ["bear", "snake", "treant", "shambling mound"],
			"Snakefolk":  ["snake", "python", "cobra"],
			"Undead":     ["snake", "spider", "wolf", "rat", "ghoul", "wraith"],
		}



		beast_subrace = {
			"Vampire":  ["Wolf", "Bat", "Dire Wolf"],
			"Werewolf": ["Wolf", "Dire Wolf"],
			"Aboleth": ["Giant Octopus", "Giant Squid", "Kraken"],
			"Beholder": ["Gazer", "Spectator", "Death Tyrant"],
			"Shapeshifters": ["Doppelganger", "Mimic"],
			"Illithid": ["Intellect Devourer"],
			"Old One": ["Star Spawn", "Gibbering Mouther", "Nothic"],
			"Mindhive": ["Swarm of Cranium Rats"],
			"Depth Dominators": ["Chuul"],
			"Living Spell": ["Animated Armor", "Helmed Horror"],
			"Chaos Warper": ["Gibbering Mouther", "Slaad (Blue, Green, Red)"],
			"Alien Spawn": ["Star Spawn"],
			"Parasyte": ["Intellect Devourer"],
			"Symbioid": ["Intellect Devourer"],
			"Destiny Devouers": ["Ghost", "Wraith"],
			"Githyanki": ["Githyanki Warrior"],
			"Githzerai": ["Githzerai Monk"],
			"Eldritch Horror": ["Doppelganger", "Nightmare"]

			}

		# Fetch the extra skills for the selected race and background
		beasts = list(set(
			beast_race.get(npc.race, []) +
			beast_subrace.get(npc.subrace, []) +
			beast_background.get(npc.background, [])))


		# Select and format skills
		beast = random.choice(beasts)
		if not beast:
			beast = "wolf"

		return beast
