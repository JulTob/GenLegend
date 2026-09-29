"""
Senses library
It includes all the racial senses abailable for creatures
It also calculates the radius of visibility of the creature in diferent sights
"""
try:
	from AtlasLudus.Map_of_Useful_Functions import select1
	from AtlasScriptum.Map_of_Formats import Entry_Text
	from AtlasLudus.Map_of_Dice import Dice, Dizero
	from AtlasActorLudi.Map_of_Scores import Modifier, PB
except ImportError:
	raise

import app.random as random

def Senses(Character):
	try: # Set Up
		race = Character.race
		subrace = Character.subrace
		background = Character.archetype
		title = Character.title
		pb = Character.pb
		dc = Character.dc
	except:
		race = "Human"
		subrace = "Local"
		background = "Soldier"
		title = "The Character"
		pb = 2
		dc = 10

	# Senses
	sense = ""
	normal = 60
	darkvision = 0
	blindsight = 0
	tremorsense = 0
	telepathy = 0
	truesight = 0
	extras = []

	# Enhanced Senses
	OtherwordlyPerception = Entry_Text(
		f"Otherworldly Perception",
		f"{title} can sense the presence of any creature within 30 feet of {title} that is invisible or on the Ethereal Plane.")
	Enhanced_Smell = Entry_Text(
		f"Enhanced Smell",
		f"{title} has advantage on Wisdom (Perception) checks that rely on smell within {Dice(3) * Dice(2)*Dice(2) * 10} feet.")
	enhanced_hearing =  Entry_Text(
		f"Enhanced Hearing",
			f"{title} has advantage on Wisdom (Perception) checks that rely on sounds from up to {Dice(3) * Dice(2)*Dice(2) * 10} feet away.")
	enhanced_taste = Entry_Text(
		f"Enhanced Taste",
			f"{title} has advantage on Wisdom (Perception) checks that rely on taste, and has advantage on saving throws against ingested poisons.")
	keen_smell = Entry_Text(
		f"Keen Smell",
			f"{title} has advantage on Wisdom (Perception) checks that rely on smell.")
	keen_hearing =  Entry_Text(
		f"Keen Hearing",
			f"{title} has advantage on Wisdom (Perception) checks that rely on hearing.")
	KeenSight = Entry_Text(
		f"Keen Sight",
		f"Advantage on Wisdom (Perception) checks that rely on sight.")
	KeenSenses = Entry_Text(
		f"Keen Senses",
		f"Advantage on Wisdom (Perception) checks that rely on one of their senses.")

	# Specialized Senses
	echolocation = Entry_Text(
		f"Echolocation",
			f"{title} can perceive its surroundings within 60 feet as if it had blindsight, but only if it isn't deafened.")

	# Sensory Communication
	color_change = Entry_Text(
		f"Color Change",
			f"{title} can change the color of its skin to communicate or as a response to its environment.")

	# Sensory Deprivation & Resistance
	blind_fighting = Entry_Text(
		f"Blind Fighting",
			f"{title} doesn’t need to see a creature to target it with an attack, provided the creature isn't hidden from the {race}.")

	# Hide and Mimic
	mimicry = Entry_Text(
		f"Mimicry",
		select1(
			(	f"{title} can mimic simple sounds it has heard, such as a person whispering, a baby crying, or an animal chittering. " +
				f"A creature that hears the sounds can tell they are imitations with a successful DC {dc} Wisdom (Insight) check.",
			f"{title} can mimic any sounds it has heard, including voices. A creature that hears the sounds can tell they are imitations with a successful DC {dc} Wisdom (Insight) check.",
			)))
	Mimicry = mimicry
	chameleon_skin = Entry_Text(
		f"Chameleonic Skin",
			f"{title} has advantage on Dexterity (Stealth) checks made to hide.")

	# Enviromental adaptations
	water_breathing= Entry_Text(
		f"Water Breathing",
		f"{title} can breathe underwater")
	underwater_camouflage = Entry_Text(f"Underwater Camouflage",
		f"{title} has advantage on Dexterity (Stealth) checks made while underwater.")
	hold_breath =   Entry_Text(
		f"Hold Breath",
		f"{title} can hold its breath for {5*Dice(3)*Dice(2)*Dice(2)} minutes.")

	# Sensibilities
	sunlight_sensitivity = Entry_Text(
		f"Sunlight Sensitivity",
		f"While in sunlight, {title} has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight.")

	# Illumination
	illumination = Entry_Text(
		f"Illumination",
		f"{title} sheds bright light in a {Dice(3)*10}-foot radius and dim light for an additional {Dice(3)*10} ft.")
	sense_magic = Entry_Text(
		f"Sense Magic",
		f"{title} senses magic within {Dice(2) * Dice(2) * Dice(3) * 10} feet of it at will. This trait otherwise works like the Detect Magic spell but isn't itself magical.")
	SpeakAnimal = Entry_Text(
			"Speak with Animal",
			f"{title} can communicate simple concepts to his affinity animal when it speaks in Beast language.")
	RadiantSight = Entry_Text(
		f"Radiant Sight",
		f"Can see divine auras and celestial beings within a {Dice(2) * Dice(2) * Dice(3) * 10} range.")
	DarkSight = Entry_Text(
		f"{race} Sight",
		f"Can see through magical darkness and illusions up to {Dice(2)*Dice(2) * Dice(3) * 10} feet."
		)
	Cogniscent = Entry_Text(
		f"Cogniscent",
		f"At the start of its turn, {title} automatically knows its target's location. If the target was hidden, it is no longer hidden from {title}."
		)
	TreasureSense = Entry_Text("Treasure Sense.",
		f"{title} can sense, like guided by scent, the location of precious metals and stones, such as coins and gems, within {Dice(pb)*10} feet of it."
		)

	if race == "Aberration":
		normal      -= Dice(2) * Dice(2) * Dice(3) * Dice(3) * 10
		blindsight  += Dice(0) * Dice(2) * Dice(2) * Dice(3) * 10
		telepathy   += Dice(0) * Dice(2) * Dice(2) * Dice(3) * 10
		tremorsense += Dice(0) * Dice(0) * Dice(3) * 10
		truesight   += Dice(0) * Dice(0) * Dice(3) * 10
		extras      += [
			sense_magic,
			enhanced_hearing,
			enhanced_taste,
			echolocation,
			color_change,
			blind_fighting,
			keen_smell,
			water_breathing,
			underwater_camouflage,
			hold_breath,
			keen_hearing,
			chameleon_skin,
			sunlight_sensitivity,
			Cogniscent,
			Mimicry,
			OtherwordlyPerception,
			]
	if race == "Aven":
		normal      += Dice(3) * Dice(3) * Dice(2) * Dice(2) * Dice(2) * 10
		darkvision  += Dice(0) * Dice(3) * Dice(2) * Dice(3) * 10
		blindsight  += Dice(0) * Dice(0) * Dice(2) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			KeenSight,
			enhanced_hearing,
			blind_fighting,
			mimicry,
			hold_breath,
			Mimicry,
			OtherwordlyPerception,
			]
		if "Kenku" in subrace:
			extras += [
				TreasureSense,
			]
	if race == "Beast":
		normal      += Dice(2) * Dice(2) * Dice(2) * Dice(2) * Dice(3) * 10
		darkvision  += Dice(0) * Dice(3) * Dice(2) * Dice(2) * Dice(2) * 10
		blindsight  += Dice(0) * Dice(3) * Dice(2) * Dice(2) * 10
		tremorsense += Dice(0) * Dice(2) * Dice(3) * 10
		telepathy   += Dice(0) * Dice(3) * 10
		truesight   += Dice(0) * Dice(0) * Dice(2) * Dice(3) * 10

		extras += [
			KeenSenses,
			enhanced_hearing,
			enhanced_taste,
			echolocation,
			color_change,
			blind_fighting,
			keen_smell,
			mimicry,
			water_breathing,
			underwater_camouflage,
			hold_breath,
			keen_hearing,
			chameleon_skin,
			sunlight_sensitivity,
			illumination,
			Cogniscent,
			]
		if "Monkey King" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Beastfolk":
		normal      += Dice(2) * Dice(2) * Dice(3) * Dice(2) * Dice(2) * 10
		darkvision  += Dice(0) * Dice(3) * Dice(5) * 10
		blindsight  += Dice(0) * Dice(3) * Dice(2)*Dice(2) * 10
		tremorsense += Dice(0) * Dice(2)*Dice(3) * 5
		telepathy   += Dice(0) * Dice(2)*Dice(3) * 10
		truesight   += Dice(0) * Dice(3) * 10

		extras += [
			KeenSenses,
			SpeakAnimal,
			enhanced_hearing,
			enhanced_taste,
			echolocation,
			color_change,
			blind_fighting,
			water_breathing,
			underwater_camouflage,
			hold_breath,
			chameleon_skin,
			sunlight_sensitivity,
			illumination,
			OtherwordlyPerception,
			]
		if "Kitsune" in subrace:
				extras += [
					TreasureSense,
					]
	if race == "Celestial":
		normal      += Dice(2) * Dice(2) * Dice(2) * Dice(5) * 10
		darkvision  += Dice(2) * Dice(2) * Dice(3) * Dice(3) * 10
		blindsight  += Dice(0) * Dice(2) * Dice(3) * 10
		tremorsense += 0
		telepathy   += Dice(0) * Dice(2) * Dice(2) * Dice(5) * 10
		truesight   += Dice(2) * Dice(3) * Dice(3) * 10

		extras += [
			RadiantSight,
			blind_fighting,
			keen_hearing,
			illumination,
			DarkSight,
			Cogniscent,
			OtherwordlyPerception,
			]
		if "Couatl" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Construct":
		normal      += Dice(2)*Dice(3) * Dice(2)*Dice(3) * 20 - Dice(2)*Dice(2)*Dice(3)*10
		darkvision  += Dice(0) * Dice(2)*Dice(3) * Dice(2)*Dice(3) * 10
		blindsight  += Dizero(2) * Dizero(3) * 10
		tremorsense += Dice(0) * Dice(3) * 5
		telepathy   += Dice(0) * Dizero(2)  * 10
		truesight   += Dice(0) * Dizero(2) * Dizero(2) * Dizero(2)  * Dizero(2) * 10

		extras += [
			enhanced_hearing,
			color_change,
			blind_fighting,
			mimicry,
			illumination,
			Cogniscent,
			]
		if "Golem" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Dragon":
		normal      += Dice(2) * Dice(2)*Dice(2)*Dice(3) * 20
		darkvision  += Dice(0) * Dice(2) * Dice(2) * Dice(3) * 20
		blindsight  += Dice(0) * Dice(2) * Dice(2) * Dice(3)  * 10
		tremorsense += Dice(0) * Dice(3) * 5
		telepathy   += Dice(0) * Dice(2) * Dice(3) * Dice(2)*Dice(2) * 10
		truesight   += Dice(0) * Dice(2) * Dice(3)  * 10

		extras += [
			enhanced_hearing,
			enhanced_taste,
			color_change,
			blind_fighting,
			keen_smell,
			water_breathing,
			underwater_camouflage,
			hold_breath,
			keen_hearing,
			chameleon_skin,
			DarkSight,
			TreasureSense,
			]
	if race == "Dwarf":
		normal      += Dice(2) * Dice(2) * Dice(2) * Dice(2) * 10
		darkvision  += Dice(2) * Dice(2) * Dice(3) * 20
		blindsight  += Dice(0) * Dice(2) * 10
		tremorsense += Dice(0) * Dice(2) * Dice(2) * 5
		telepathy   += Dice(0) * Dice(3) * 10
		truesight   += Dice(0) * Dice(0) * Dice(0) * 10

		extras += [
			sunlight_sensitivity,
			TreasureSense,
			]
	if race == "Elf":
		normal      += Dice(2) * Dice(2) * Dice(2) * Dice(3) * 20
		darkvision  += Dice(0) * Dice(2) * Dice(3) * 20
		blindsight  += Dice(0) * Dice(0) * 10
		tremorsense += 0
		telepathy   += Dice(0) * Dice(3) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			KeenSenses,
			enhanced_hearing,
			blind_fighting,
			sunlight_sensitivity,
			]
		if race == "Dark Elf":
			darkvision  += Dice(2) * Dice(2) * Dice(3) * 10
		if race == "Night Elf":
			darkvision  += Dice(2) * Dice(2) * Dice(3) * 10
		if race == "Shadow Elf":
			darkvision  += Dice(2) * Dice(2) * Dice(3) * 10
		if race == "Moon Elf":
			darkvision  += Dice(2) * Dice(2) * Dice(3) * 10
	if race == "Elemental":
		normal      += Dice(2) * Dice(2)*Dice(3) * 20
		darkvision  += Dice(0) * Dice(2)*Dice(3) * Dice(3) * 10
		blindsight  += Dice(0) * Dice(3) * 10
		tremorsense += Dice(0) * Dice(2)*Dice(2) * Dice(2)*Dice(2) * 5
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(2) * 10

		extras += [
			water_breathing,
			underwater_camouflage,
			chameleon_skin,
			illumination,
			]
		if "Genie" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Fey":
		normal      += Dice(2)   * Dice(2)   * Dice(2) * Dice(3) * 10
		darkvision  += Dice(2)   * Dice(2)   * Dice(2) * Dice(3) * Dice(2) * 10
		blindsight  += Dice(0)   * Dizero(3) * 10
		telepathy   += Dizero(2) * Dizero(2) * Dizero(3) * 10
		truesight   += Dice(0)   * Dizero(2) * Dizero(3) * 10

		extras +=[
			DarkSight,
			blind_fighting,
			mimicry,
			chameleon_skin,
			OtherwordlyPerception,
			]
		if "Leprechaun" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Fiend":
		normal      += Dice(2)*Dice(2) * Dice(2)*Dice(3) * 20
		darkvision  += Dice(2) * Dice(2)*Dice(3) * 20
		blindsight  += Dice(0) * Dice(2)*Dice(5) * 10
		tremorsense += Dice(0) * Dice(2) * 5
		telepathy   += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		truesight   += Dice(2) * Dice(2)*Dice(3) * 10

		extras += [
			DarkSight,
			enhanced_taste,
			blind_fighting,
			keen_smell,
			mimicry,
			hold_breath,
			sunlight_sensitivity,
			Cogniscent,
			OtherwordlyPerception,
			]
	if race == "Giant":
		normal      += Dice(3) * Dice(2)*Dice(3) * 20
		darkvision  += Dice(0) * Dice(0) * 20
		blindsight  += Dice(0) * Dice(0) * 10
		tremorsense += Dice(0) * Dice(0) * 5
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			keen_smell,
			sunlight_sensitivity,
			]
		if "Fire Giant" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Gnome":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(2) * Dice(2)*Dice(3) * 20
		blindsight  += Dice(0) * Dice(5) * 10
		tremorsense += Dice(0) * Dice(0) * 5
		telepathy   += Dice(0) * Dice(3) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			mimicry,
			]
		if "Leprechaun" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Goblin":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(2) * Dice(2)*Dice(3) * 20
		blindsight  += Dice(0) * Dice(0) * 10
		tremorsense += Dice(0) * Dice(0) * 5
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			enhanced_hearing,
			keen_smell,
			]
	if race == "Halfling":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(0) * Dice(0) * 20
		blindsight  += Dice(0) * Dice(0) * 10
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			TreasureSense,
			]
	if race == "Kobold":
		normal      += Dice(0) * Dice(0) * 20
		darkvision  += Dice(2)*Dice(2) * Dice(3) * 20
		blindsight  += Dice(0) * Dice(0) * 10
		tremorsense += Dice(0) * Dice(0) * Dice(0) * 5
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			enhanced_taste,
			keen_smell,
			hold_breath,
			sunlight_sensitivity,
			TreasureSense,
			]
	if race == "Lizardfolk":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(2)*Dice(2) * Dice(3) * 10
		blindsight  += Dice(0) * Dice(0) * 10
		tremorsense += Dice(0) * Dice(0) * 5
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			enhanced_taste,
			color_change,
			blind_fighting,
			keen_smell,
			underwater_camouflage,
			hold_breath,
			chameleon_skin,
			sunlight_sensitivity,
			]
		if "Silurian" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Monstrosity":
		normal      += Dice(-1)  * Dice(100) * 20
		darkvision  += Dizero(2) * Dice(2)   * Dice(3) * 10
		blindsight  += Dizero(2) * Dice(2)   * Dice(3) *  5
		tremorsense += Dizero(2) * Dizero(2) * Dizero(3) *  5
		telepathy   += Dizero(2) * Dice(2)   * Dice(3) *  10
		truesight   += Dizero(3) * Dice(2)   * 10

		extras += [
			enhanced_hearing,
			enhanced_taste,
			echolocation,
			color_change,
			blind_fighting,
			keen_smell,
			mimicry,
			water_breathing,
			underwater_camouflage,
			hold_breath,
			chameleon_skin,
			sunlight_sensitivity,
			illumination,
			DarkSight,
			OtherwordlyPerception,
			]
		if "Sphynx" in subrace:
			extras += [
				TreasureSense,
				]
	if race == "Ooze":
		normal      += Dice(-1) * Dice(0) * 60
		darkvision  += Dice(-1) * Dice(0) * 20
		blindsight  += Dice(0) * Dice(3) * 10
		tremorsense += Dice(0) * Dice(2)*Dice(3) * 5
		telepathy   += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		truesight   += Dice(-1) * Dice(0) * 10

		extras += [
			color_change,
			blind_fighting,
			water_breathing,
			underwater_camouflage,
			]
	if race == "Orc":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(2) * Dice(2)*Dice(3) * 20
		blindsight  += Dice(0) * Dice(0) * 10
		tremorsense += Dice(0) * Dice(0) * 5
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += []
	if race == "Plant":
		normal      -= Dice(0) * Dice(2) * Dice(2) * Dice(3) * Dice(3) * 10
		darkvision  -= Dice(0) * Dice(2) * Dice(2) * Dice(5) * 10
		blindsight  += Dice(2) * Dice(2) * Dice(3) * 10
		tremorsense += Dice(0) * Dice(2) * Dice(3) * 5
		telepathy   += Dice(0) * Dice(2) * Dice(3) * 10
		truesight   += Dice(0) * Dice(2) * Dice(3) * 5

		extras += [
			color_change,
			blind_fighting,
			water_breathing,
			underwater_camouflage,
			chameleon_skin,
			sunlight_sensitivity,
			illumination,
			]
	if race == "Snakefolk":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(2) * Dice(2)*Dice(3) * 20
		blindsight  += Dice(2) * Dice(2)*Dice(2) * 10
		tremorsense += Dice(0) * Dice(3) * 5
		telepathy   += Dice(0) * Dice(2) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			enhanced_taste,
			color_change,
			blind_fighting,
			keen_smell,
			underwater_camouflage,
			hold_breath,
			chameleon_skin,
			OtherwordlyPerception,
			]
	if race == "Undead":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 20
		blindsight  += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		tremorsense += Dice(0) * Dice(5) * 5
		telepathy   += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		truesight   += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		extras += [
			enhanced_taste,
			blind_fighting,
			sunlight_sensitivity,
			illumination,
			Cogniscent,
			OtherwordlyPerception,
			]
		if "Tomb's Hoarder" in subrace:
			extras += [
				TreasureSense,
			]

	if race == "Vampire":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 20
		darkvision  += Dice(2) * Dice(2)*Dice(2)*Dice(3) * 20
		blindsight  += Dice(2) * Dice(2)*Dice(2)*Dice(3) * 10
		tremorsense += Dice(0) * Dice(5) * 0
		telepathy   += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		truesight   += Dice(0) * Dice(2)*Dice(2)*Dice(3) * 10
		extras += [
			enhanced_taste,
			blind_fighting,
			sunlight_sensitivity,
			Cogniscent,
			OtherwordlyPerception,
			]
	if race == "Catfolk":
		normal      += Dice(2) * Dice(2) * Dice(2) * Dice(3) * Dice(5) * Dice(5) * 10
		darkvision  += Dice(2) * Dice(2) * Dice(2) * Dice(2) * Dice(3) * Dice(3) * 10
		blindsight  += Dice(0) * Dice(2) * 10
		telepathy   += Dice(0) * Dice(0) * 10
		truesight   += Dice(0) * Dice(0) * 10

		extras += [
			Enhanced_Smell,
			keen_smell,
			enhanced_hearing,
			enhanced_taste,
			SpeakAnimal,
			DarkSight,
			]
		if "Felinian" in subrace:
			extras += [
				TreasureSense,
				]

	if background == "Artist":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 0
		extras += [
			Mimicry,
			OtherwordlyPerception,
			TreasureSense,
			]
	if background == "Bandit":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 0
		extras += [
			Mimicry,
			TreasureSense,
			]
	if background == "Bard":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 0
		extras += [
			Mimicry,
			OtherwordlyPerception,
			]
	if background == "Charlatan":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 0
		extras += [
			Mimicry,
			TreasureSense,
			]
	if background == "Crafter":
		extras += [
			TreasureSense,
			]
	if background == "Cleric":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Cultist":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Druid":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Expert":
		extras += [
			TreasureSense,
			]
	if background == "Explorer":
		extras += [
		OtherwordlyPerception,
		TreasureSense,
			]
	if background == "Guard":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Monk":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Merchant":
		extras += [
		TreasureSense,
			]
	if background == "Ninja":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Paladin":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Priest":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Pirate":
		extras += [
		TreasureSense,
			]
	if background == "Ranger":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Scholar":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Shaman":
		extras += [
		OtherwordlyPerception,
			]
	if background == "Spy":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 0
		darkvision  += Dice(0) * Dice(2) * 10
		extras += [
			Mimicry,
			OtherwordlyPerception,
			]
	if background == "Trickster":
		extras += [
			Mimicry,
			]
	if background == "Warlock":
		extras += [
			OtherwordlyPerception,
			]
	if background == "Witch":
		normal      += Dice(2)*Dice(5) * Dice(2)*Dice(5) * 0
		extras += [
			Mimicry,
			OtherwordlyPerception,
			]

	# Additional sense-related abilities
	if telepathy>0:
		if Dice() == 1:
			extras += [
				Entry_Text(
					f"Probing Telepathy",
					f"If a creature communicates telepathically with {title}, {title} learns the creature's greatest desires if {title} can see the creature."
					),
				Entry_Text(
					f"Telepathic Shroud.",
					f"The {race} is immune to any effect that would sense its emotions or read its thoughts, as well as all divination spells."),
				Entry_Text(
					f"Advanced Telepathy",
					f"The {race} can perceive the content of any telepathic communication used within {telepathy//2} feet of it, and it can't be surprised by creatures with any form of telepathy."),
				Entry_Text(
					f"Limited Telepathy.",
					f"The {race} can magically transmit simple messages and images to any creature within {telepathy} feet of it that can understand a language. This form of telepathy doesn't allow the receiving creature to telepathically respond."),
				Entry_Text( f"Detect Sentience",
					f"The {race} can sense the presence and location of any creature within {telepathy} feet of it that has an Intelligence of 3 or higher, regardless of interposing barriers, unless the creature is protected by a mind blank spell."),
				Entry_Text(f"Limited Telepathy",
					f"The {race} can magically communicate simple ideas, emotions, and images telepathically with any creature within {telepathy} feet of it that can understand a language. It can also communicate with any {race}"),

				]


	if normal<=0:
		sense += f"<b>Blind beyond these radius</b>\n"
	else:
		if darkvision>0: sense += f"<b>Darkvision:</b> <i> {darkvision}ft. </i>\n"
	if blindsight>0: sense += f"<b>Blindsight:</b> <i>{blindsight}ft.</i> \n"
	if tremorsense>0: sense += f"<b>Tremorsense:</b> <i>{tremorsense}ft. </i>\n"
	if truesight>0: sense += f"<b>Truesight:</b> <i>{truesight}ft.</i> \n"

	if extras:
		extras = list(set(extras))
		number = min(PB(pb),len(extras))
		sense += '<p style="font-size: 0.85em;">'
		sense += "\n"+'\n\n'.join(random.sample(extras,number))  # extras
		sense += '</p>'

	sense += "\n"
	return sense
