import dnd
import npc_class as NPC
import app.random as random


def Extra_Weaknesses(npc):
	race= npc.race
	subrace= npc.subrace
	background= npc.archetype
	lvl = npc.level
	gender = npc.gender

	# Definitions of extra weaknesses
	freeze = f"\n- Freeze: If the {race} takes cold damage, it partially freezes; All its speed is reduced by 20 feet until the end of its next turn."
	sunlight_sensitivity = Entry_Text(f"Sunlight Sensitivity.",
		f"While in sunlight, the {subrace} has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight."
		)
	aversion_to_fire = f"\n- Aversion of Fire:\n\t If the {race} takes fire damage, it has disadvantage on attack rolls and ability checks until the end of its next turn."
	berserk = f"\n- Berserk:\n\t Whenever {title} starts its turn with {npc.HP//2} hit points or fewer, it gains the Bloodied condition. Roll a d6: On a 6, {title} goes berserk. On each of its turns while berserk, {title} attacks the nearest creature it can see. If no creature is near enough to move to and attack, {title} attacks an object, with preference for an object smaller than itself. Once {title} goes berserk, it continues to do so until it dies or is no longer bloodied. \n\t An ally of {title}, if within 60 feet of the berserk {race}, can try to calm it by speaking firmly and persuasively. {title} must be able to hear its ally, who must take an action to make a DC 15 Charisma (Persuasion) check. If the check succeeds, {title} ceases being berserk. If it takes damage while still at 40 hit points or fewer, {title} might go berserk again."
	PowerItem = Entry_Text(f"{subrace} Items.",
		(f"{title} carries a very rare magic item. If the object is lost, {title} will go to great lengths to retrieve it. Take a moment to think what object suits the character best. It can be a powerful artifact, a very personal item, or a piece of treasure they are magically bound to."
		))
	if Type == "Elemental" and Dice(D=6, N=1) == 1:     r += "\n - Water Susceptibility \n\t For every 5 feet the elemental moves in water, or for every gallon of water splashed on it, it takes 1 cold damage."


	# Dictionary to store possible extra weaknesses for each race
	extra_weaknesses_race = {
		"Aberration": [
			sunlight_sensitivity,
			aversion_to_fire,
			berserk,
			PowerItem,
			],
		"Beast":[
			sunlight_sensitivity,
			aversion_to_fire,
			berserk,
			],
		"Beastfolk": [
			sunlight_sensitivity,
			berserk,
			PowerItem,
			],
		"Catfolk": [
			berserk,
			],
		"Celestial": [
			PowerItem,
			],
		"Construct": [
			aversion_to_fire,
			berserk,
			PowerItem,
			],
		"Dragon":[
			berserk,
			PowerItem,
			],
		"Dwarf": [
			PowerItem,
			],
		"Elf": [
			],
		"Elemental":[
			freeze,
			PowerItem,
			],
		"Fey": [
			PowerItem,
			],
		"Fiend": [
			freeze,
			PowerItem,
			berserk,
			sunlight_sensitivity],
		"Giant": [
			aversion_to_fire,
			berserk,
			],
		"Goblin": [
			aversion_to_fire,
			berserk,
			],
		"Kobold":[
			sunlight_sensitivity],
		"Lizardfolk":[
			freeze,
			aversion_to_fire,
			],
		"Monstrosity": [
			aversion_to_fire,
			berserk,
			],
		"Ooze": [
			aversion_to_fire,
			],
		"Orc": [
			berserk,
			],
		"Plant": [
			aversion_to_fire,
			],
		"Snakefolk":[
			freeze,
			],
		"Undead":[
			aversion_to_fire,
			PowerItem,
			],

		"Dark Elf": [
			sunlight_sensitivity,
			],
		"Orog (Underdark)": [
			sunlight_sensitivity,
			],
		"Myconid Sovereign": [
			sunlight_sensitivity,
			],
		"Myceliumanoid": [
			sunlight_sensitivity,
			],
	}




	# Dictionary to store possible extra weaknesses for each background
	extra_weaknesses_background = {
		"Artist": [
			PowerItem,
			],
		"Barbarian": [
			],
		"Berserker": [
			berserk,
			],
		"Charlatan": [
			PowerItem,
			],
		"Crafter": [
			PowerItem,
			],
		"Cultist": [
			PowerItem,
			],
		"Explorer": [
			PowerItem,
			],
		"Knight": [
			PowerItem,
			],
		"Merchant": [
			PowerItem,
			],
		"Noble": [],
		"Scholar": [
			PowerItem,
			],
		"Warlock": [
			PowerItem,
			],
		"Witch": [
			PowerItem,
			],
		"Wizard": [
			PowerItem,
			],

		}

	# Fetch the extra weaknesses for the selected race and background
	possible_extra_weaknesses_race = extra_weaknesses_race.get(race, [])
	possible_extra_weaknesses_race += extra_weaknesses_race.get(subrace, [])
	possible_extra_weaknesses_background = extra_weaknesses_background.get(background, [])

	# Combine race and background weaknesses
	possible_extra_weaknesses = possible_extra_weaknesses_race + possible_extra_weaknesses_background

	# Determine the number of weaknesses to select, this number can be changed as needed
	number_of_weaknesses_to_select = PB(lvl)  # for example

	# Randomly determine which extra weaknesses the character has
	if possible_extra_weaknesses and len(possible_extra_weaknesses) >= number_of_weaknesses_to_select:
		selected_weaknesses = random.sample(possible_extra_weaknesses, number_of_weaknesses_to_select)
		formatted_weaknesses = [weaknesses.format(race) for weaknesses in selected_weaknesses]
	else:
		formatted_weaknesses = [""]

	# Join the list of formatted weaknesses into a single string separated by newlines or any other separator
	formatted_weaknesses_string = '\n'.join(formatted_weaknesses)

	return formatted_weaknesses_string
