import random

try:
	from AtlasLudus.Compass_of_Damages import ElementalDamage
	from AtlasAlusoris.Grimoire_of_NPC import NPC
	from AtlasActorLudi.Map_of_Scores import Modifier, PB
	from AtlasLudus.Map_of_Dice import Dice, Dizero
	from AtlasLudus.Map_of_Useful_Functions import select1
	from AtlasScriptum.Map_of_Formats import Entry_Text
except Exception:
	raise




def Hoovers(npc):
	race = npc.race
	if npc.race == "Monstrosity":
		return True
	if npc.race == "Aberration":
		return True
	return False

def Movement(npc):

	title = npc.title
	race = npc.race
	background = npc.archetype

	# movement
	movement = ""
	normal = 0
	fly = 0
	swim = 0
	burrow = 0
	climb = 0

	extras = []


	if race in [ "Human", "Aberration", "Aven", "Beast", "Beastfolk", "Celestial", "Construct", "Dragon","Dwarf","Elf","Elemental","Fey","Fiend", "Giant","Gnome","Goblin","Halfling","Kobold","Lizardfolk","Monstrosity","Ooze","Orc","Plant","Snakefolk","Undead"]:
		normal = 30

	base_speeds = {
		"Human": {      "Walk": 30},
		"Dwarf": {      "Walk": 25,
						"Climb": Dizero(2) * 5},
		"Elf": {        "Walk": 30},
		"Catfolk": {    "Walk": 40,
						"Climb":  Dizero(3) * 10},
		"Halfling": {   "Walk": 25},
		"Aberration": { "Walk": Dizero(6) * 10,
						"Fly": Dizero(6) * 10,
						"Climb": Dizero(3) * 10},
		"Aven": {       "Walk": 30,
						"Fly": Dizero(6) * 10},
		"Beast": {      "Walk": Dice(2) * Dice(2) * Dice(2) * Dice(3) * 5,
						"Swim": Dizero(2) * Dizero(2) * 10,
						"Burrow": Dizero(2) * Dizero(2) * 5,
						"Climb": Dizero(3) * 10},
		"Beastfolk": {  "Walk": Dice(8)*10,
						"Fly": 0,
						"Swim": Dizero(3) * 10,
						"Burrow": Dizero(2) * 5,
						"Climb": Dizero(3) * 10},
		"Celestial": {  "Walk": Dice(6) * 10,
						"Fly": Dice(4) * Dice(2) * 10},

		"Construct": {  "Walk": Dice(2) * Dice(3) * 10,
						"Fly": Dizero(2) * Dizero(3) * 10,
						"Swim": Dizero(2) * Dizero(2) * 10,
						"Burrow": Dizero(2) * 5,
						"Climb": Dizero(3) * Dizero(2) * 5
						},

		"Dragon": {     "Walk":   Dice(3) * Dice(2) * Dice(2) * 10,
						"Fly":    Dice(2) * Dice(2) * Dice(3) * 10,
						"Swim":   Dice(3) * Dice(2) * Dice(2) * 10,
						"Burrow": Dizero(3) * Dizero(2) * 5,
						"Climb":  Dizero(3) * Dizero(2) * 5
						},
		"Dwarf": {      "Walk":   25
						},
		"Elf": {        "Walk":   30,
						"Swim":   Dizero(3) * Dizero(3) * 5
						},
		"Elemental": {  "Walk":   Dizero(6) * 10,
						"Fly":    Dizero(6) * 10,
						"Swim":   Dizero(6) * 10,
						"Burrow": Dizero(6) * 5
						},
		"Fey": {        "Walk":   Dice(6) * 10,
						"Fly":    Dizero(6) * 5
						},
		"Fiend": {      "Walk":   Dice(6) * 10,
						"Fly":    Dizero(8) * 10,
						"Climb":  Dizero(3) * 10
						},
		"Giant": {      "Walk":   Dice(2) *  Dice(2) *  Dice(3) * 10
						},
		"Gnome": {      "Walk":   25
						},
		"Goblin": {     "Walk":   30
						},
		"Halfling": {   "Walk":   25
						},
		"Kobold": {     "Walk":   30,
						"Fly":    Dizero(3) * Dizero(2) * 5
						},
		"Lizardfolk": { "Walk":   Dice(3) * Dice(3) * 10,
						"Swim":   Dice(2) *  Dice(3) *  10,
						"Climb":  Dizero(3) * 10
						},
		"Monstrosity": {"Walk":   Dice(2) * Dice(3) * 10,
						"Fly":    Dice(2) * Dice(3) * 5,
						"Swim":   Dice(2) * Dice(3) * 10,
						"Climb":  Dizero(3) * 10
						},
		"Ooze": {       "Walk":   Dice(2) * Dice(3) * 10,
						"Burrow": Dice(3) * 5,
						"Climb":  Dice(2) * Dice(3) * 10
						},
		"Orc": {        "Walk":   30
						},
		"Plant":  {     "Walk":   Dice(3) * 10,
						"Swim":   Dice(3) * 10,
						"Burrow": Dice(3) * 5,
						"Climb":  Dice(3) * 10
						},
		"Snakefolk": {  "Walk":   30,
						"Swim":   Dizero(2) * Dizero(3) * 10,
						"Climb":  Dizero(3) * 5
						},
		"Undead": {     "Walk":   Dizero(2) * Dice(2) * Dice(3) * 5,
						"Fly":    Dizero(2) * Dizero(3) * 5,
						"Swim":   Dice(0) * Dizero(3) * 5,
						"Burrow": Dice(0) * Dizero(2) * 5
						},
	}



	spider_climb = Entry_Text(f"Spider Climb",f"The {race} can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check.\n")
	flyby = Entry_Text(f"Flyby",f"The {race} is an agile flier, quick to fly out of enemies' reach. The {race} doesn't provoke an opportunity attack when it flies out of an enemy's reach.\n")
	earth_glide = Entry_Text(f"Earth Glide",f"The {race} can burrow through nonmagical, unworked earth and stone. While doing so, the {race} doesn't disturb the material it moves through.\n")
	amphibious = Entry_Text(f"Amphibious",f"The {race} can breathe air and water.")
	IceWalk = Entry_Text(f"Ice Walk",f"The {race} can move across and climb icy surfaces without needing to make an ability check. Additionally, difficult terrain composed of ice or snow doesn't cost it extra movement.")
	ElementalForm = Entry_Text(f"Elemental Form",
		select1(
			[f"{title} can enter a hostile creature's space and stop there. It can move through a space as narrow as 1 inch wide without squeezing.",
			f"{title} can move through a space as narrow as 1 inch wide without squeezing. A creature that touches the elemental or hits it with a melee attack while within 5 feet of it takes 3 (1d6) {ElementalDamage()} damage. In addition, the elemental can enter a hostile creature's space and stop there. The first time it enters a creature's space on a turn, that creature takes damage as if they touched the {race}",
			]))

	# Set default speeds to 0
	normal = base_speeds.get(race, {}).get("Walk", 0)
	fly = base_speeds.get(race, {}).get("Fly", 0)
	if swim > 0: swim = max(base_speeds.get(race, {}).get("Swim", 0),(1+normal//10)*5)
	if burrow > 0: burrow = max(base_speeds.get(race, {}).get("Burrow", 0),(1+normal//10)*5)
	if climb > 0: climb =  max(base_speeds.get(race, {}).get("Climb", 0),(1+normal//10)*5)

	try:
		npc.speed = normal
	except:
		pass

	if  "Bear"  in npc.subrace:
		fly = 0
		climb += 10

	if "Winged Kobold"	in npc.subrace:
		fly += 15

	if "Dragonborn"	in npc.subrace:
		fly = 0



	if normal>=0:   movement += f"<b>Walk:</b> <i>{normal}ft.</i>  \t\n"
	if fly>0:
		if Hoovers(npc):
			movement += f"<b>Hoover:</b> <i>{fly}ft.</i>  \t\n"
		else:
			movement += f"<b>Fly:</b> <i>{fly}ft.</i>  \t\n"
	if swim>0:      movement += f"<b>Swim:</b> <i>{swim}ft.</i>  \n"
	if burrow>0:    movement += f"<b>Burrow:</b> <i>{burrow}ft.</i>  \t\n"
	if climb>0:     movement += f"<b>Climb:</b> <i>{climb}ft.</i>  \t\n"

	# Additional Movement-related abilities
	if race in [ "Aberration", "Beast", "Beastfolk", "Construct", "Dragon","Fey","Fiend", "Lizardfolk","Monstrosity","Ooze","Plant","Snakefolk","Undead"]:
		if Dice()==1: extras += [spider_climb]

	if "White"	in npc.subrace:
		if Dice()==1: extras += [IceWalk]

	if race in [ "Beast", "Beastfolk", "Dragon","Fey"]:
		if fly>0 and Dice(7) == 1: extras += [flyby]

	if race in [ "Aberration", "Beast", "Beastfolk","Gnome","Lizardfolk","Monstrosity"]:
		if Dice() == 1: extras += [Entry_Text(f"Standing Leap",f"{title}'s long jump is up to half his speed in feet and its high jump is up to third his speed, with or without a running start.")]
	if race in [ "Aberration", "Beast", "Beastfolk","Monstrosity","Fiend", "Lizardfolk","Ooze","Snakefolk","Undead"]:
		if Dice()==1:
			extras += [Entry_Text(f"Spider Climb",
				f"The {race} can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check.\n")
				]
			if Dice() == 1:
				extras += [Entry_Text(f"Web Sense",
					f"While in contact with a web, {title} knows the exact location of any other creature in contact with the same web.\n")
					]
			if Dice() == 1:
				extras += [Entry_Text(f"Web Walker",f"{title} ignores movement restrictions caused by webbing.\n")
						]
	if race in [ "Beast", "Beastfolk", "Dragon","Fey"]:
		if Dice()==1: extras += [Entry_Text(f"Hold Breath",f"{title} can hold its breath for {Dice(3) * Dice(4) * 5} minutes.\n")
				]
	if race in [ "Aberration", "Beast", "Beastfolk", "Construct", "Dragon","Fiend", "Lizardfolk","Monstrosity","Plant","Snakefolk","Undead"]:
		if burrow > 0 and Dice()==1:
			extras += [Entry_Text(f"Tunneler",f"{title} can burrow through solid rock at half its burrowing speed and leaves a 5 foot-wide, 8-foot-high tunnel in its wake.\n")
				]
	if race in ["Elemental"]:
		if burrow > 0 and Dice()==1: extras += [earth_glide]
		if Dice()==1: extras += [ElementalForm]

	if race in [ "Undead", "Celestial", "Elemental", "Fey", "Fiend", "Ooze" ]:
		if Dice()==1:
			extras += [Entry_Text(f"Incorporeal Movement",f"{title} can move through other creatures and objects as if they were difficult terrain. {title} takes 5 force damage if it ends its turn inside an object.\n")
				]

	Marine = ["Swamp Crocfolk",	"Sea Elf", "Kraken", "Nyk (Watergoblin)", "Fomorians (Sea Giants)", "Nymph", "Nymphian",	"Oceanians",	"Gaian",	"Atlantian",	"Merfolk","Sharkfolk", "Aboleth", "Old One", "Depth Dominators", "Star Whale", "Kaiju Dinosaur"]
	if race in ["Ooze"]:
		if swim <= 0: swim = 10 * Dice(2) * Dice(2)
		extras += [amphibious]
	if npc.subrace in Marine:
		if swim <= 0: swim = 10 * Dice(2) * Dice(2)
		extras += [amphibious]

	if swim > 0:
		if race in ["Aberration", "Dragon", "Construct", "Plant"]:
			if Dice() == 1:
				extras += [amphibious]

	# Sample two unique extras if available
	if len(extras) >= 2:
		selected_extras = random.sample(extras, Dice(2))  # Select two unique extras
	elif len(extras) == 1:
		selected_extras = extras  # If only one extra exists, use it
	else:
		selected_extras = []  # No extras available

	# Append selected extras to movement
	for extra in selected_extras:
		movement += f"\n{extra}"


	return movement
