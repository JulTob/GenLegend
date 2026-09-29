import app.random as random

try:
	from AtlasScriptum.Map_of_Formats import Entry
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasActorLudi.Map_of_Scores import PB
	from AtlasAlusoris.Grimoire_of_NPC import NPC
except ImportError:
	raise


class Weapon:
	def __init__(wpn,name,damage_intensity=1,damage_dice='d4',attack_modifier= 0,damage_type= "Bludgeoning",range_distance="",properties=""):
		wpn.name = name
		wpn.damage_intensity = damage_intensity
		wpn.damage_dice = 		damage_dice
		wpn.attack_modifier = 	attack_modifier
		wpn.damage_type = 		damage_type
		wpn.range_distance = 	range_distance
		wpn.properties = 		properties

	@property
	def weapon_type(wpn):
		return str(wpn)


	def __str__(wpn):
		result = f"{wpn.damage_intensity}{wpn.damage_dice}"
		if wpn.attack_modifier:
			result += f"{wpn.attack_modifier:+}"
		result += f" {wpn.damage_type}"
		if wpn.range_distance:
				result += f", {wpn.range_distance}"
		if wpn.properties:
				result += f", {wpn.properties}."
		else:
				result += "."
		entry = Entry(wpn.name, result)
		return f"{entry:html}"
