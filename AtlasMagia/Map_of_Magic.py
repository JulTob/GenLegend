import random
try:
	from AtlasMagia.Lodge_of_Spells import *
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasActorLudi.Map_of_Scores import PB, Modifier
	from AtlasScriptum.Map_of_Formats import Entry, Entry_Text
except ImportError:
	raise

def is_ritualcaster(ludus):
	# return True
	if "Berserker" in ludus:   return True
	if "Priest" in ludus:      return True
	if "Cleric" in ludus:      return True
	if "Cultist"  in ludus:     return True
	if "Druid"  in ludus:       return True
	if "Mage" in ludus:        return True
	if "Shaman" in ludus:      return True
	if "Warlock"  in ludus:     return True
	if "Witch"  in ludus:       return True
	return False

def is_spellcaster(ludus):
	# return True
	if "Priest"  in ludus:  return True
	if "Cleric"  in ludus:  return True
	if "Cultist" in ludus: return True
	if "Druid"  in ludus:   return True
	if "Mage"  in ludus:    return True
	if "Shaman"  in ludus:  return True
	if "Warlock"  in ludus: return True
	if "Witch"  in ludus:   return True
	return False



class Spell:
	def __init__(self,
				 name="",
				 level=0,
				 school="",
				 casting_time="",
				 ranges = "",
				 duration = "",
				 components = "",
				 concentration = ""):
		self.name =  name
		self.level = level
		self.school = school
		self.casting_time = casting_time
		self.ranges = ranges
		self.duration = duration
		self.components = components
		self.concentration = concentration

	def describe(self):
		desc = self.string
		return desc

	@property
	def string(self):

		name  = f"{self.name}"
		desc  = f"{self.school}"
		if self.casting_time:   desc += f"({self.casting_time})"
		if self.concentration:  desc += f"⟨{self.concentration}"
		if self.duration:       desc += f"⟨{self.duration}⟩"
		if self.ranges:         desc += f"- {self.ranges}-"
		#-- Only the name ever printed: with no definition, the header line
		#-- (school, time, range) was never shown.
		entry = Entry(title=name)
		return f"{entry:html}"



class Spellcaster:
	def __init__(self, ludus):
		#print("Spellcaster Initiated")
		self.ludus = ludus
		self.spell_slots = self.SlotCalculator()

	@property
	def maximum_spell_level(self):
		#print("Maximum Spell Level Called")
		delay = self.difficulty - 1
		rate = 2 * self.difficulty
		f = (self.ludus.level - delay) // rate
		f = min(f,12)
		f = max(0,f)
		return f

	def SlotCalculator(self):
		#print("Slot Calculator initiated")
		max_spell_level = self.maximum_spell_level
		difficulty = self.difficulty
		# Initialize slots list with a placeholder for index 0
		slots = [0] * (max_spell_level + 1)
		slots[0] = None  # Placeholder for 0th index

		# Calculate slots for lower spell levels
		for spell_level in range(max_spell_level , 0, -1):
			# Determine how many levels down from the max we are
			levels_down = max_spell_level - spell_level

			# Calculate the additional slots based on the difficulty
			additional_slots = (levels_down + difficulty) // (difficulty + 1)

			if additional_slots > 3:
				if spell_level == 1:
					additional_slots = 4
				else:
					additional_slots = 3

			# Assign slots to the current spell level
			slots[spell_level] = 1 + additional_slots

		return slots

	def slots(self,n):
		#print(f"Slot of level {n} called")
		try:
			s = self.spell_slots[n]
		except IndexError:
			s = 0
		return s

	@property
	def difficulty(self):
		#print("Difficulty called")
		background = self.ludus.background
		race = self.ludus.race

		difficulty = 6
		if  "Artist"    in background:  difficulty = Dice(2)
		if  "Bandit"    in background:  difficulty = Dice(6)
		if  "Bard"      in background:  difficulty = 1
		if  "Berserker" in background:  difficulty = Dice(3)+ Dice(3)
		if  "Barbarian" in background:  difficulty = Dice(Dice(3)+ Dice(3))
		if  "Crafter"   in background:  difficulty = Dice(3)
		if  "Criminal"  in background:  difficulty = Dice(6)
		if  "Cultist"   in background:  difficulty = Dice(3)
		if  "Charlatan" in background:  difficulty = Dice(Dice(6))
		if  "Commoner" 	in background:  difficulty = 1+Dice(6)
		if  "Cleric"	in background:  difficulty = 1
		if  "Crafter" 	in background:  difficulty = 1+Dice(Dice(6))
		if  "Druid"     in background:  difficulty = 1
		if  "Expert"    in background:  difficulty = 1 + Dice(3)
		if  "Explorer"  in background:  difficulty = Dice(3)
		if  "Fighter"   in background:  difficulty = 1 + Dice(6)
		if  "Guard"     in background:  difficulty = Dice(6)
		if  "Healer"    in background:  difficulty = Dice(2)
		if  "Hero"      in background:  difficulty = Dice( Dice(3) + Dice(3) )
		if  "Hero"      in background:  difficulty = 1 + Dice( Dice(3) + Dice(3) )
		if  "Knight"    in background:  difficulty = 1 + Dice( Dice(3))
		if  "Mage"      in background:  difficulty = 1
		if  "Merchant"  in background:  difficulty = Dice(Dice(6))
		if  "Monk"  	in background:  difficulty = Dice(3)
		if  "Ninja"  	in background:  difficulty = 1 + Dice(3)
		if  "Noble"     in background:  difficulty = ( Dice(6) + Dice(6) )//2
		if  "Pirate"    in background:  difficulty = 1 + Dice(3)
		if  "Priest"    in background:  difficulty = 1 + Dice(3)
		if  "Paladin"   in background:  difficulty = Dice(3)
		if  "Ranger"    in background:  difficulty = Dice(3)
		if  "Rogue"     in background:  difficulty = 1 + Dice(4)
		if  "Scholar"  	in background:  difficulty = Dice(4)
		if  "Shaman"  	in background:  difficulty = 1
		if  "Sorcerer"  in background:  difficulty = 1
		if  "Soldier"   in background:  difficulty = Dice(6)
		if  "Spy"   	in background:  difficulty = Dice(4)
		if  "Traveler"  in background:  difficulty = Dice(6)
		if  "Prankster" in background:  difficulty = Dice(6)
		if  "Warlock"   in background:  difficulty = 1
		if  "Warrior"   in background:  difficulty = Dice(6)
		if  "Witch"   	in background:  difficulty = 1
		if  "Wizard"    in background:  difficulty = 0


		if "Gnome"        	in race: difficulty -= 1
		if "Celestial"    	in race: difficulty -= 1
		if "Dragon"        	in race: difficulty -= 1
		if "Aberration"    	in race: difficulty += 1
		if "Giant"        	in race: difficulty += 1
		if "Fey"        	in race: difficulty -= 2


		if difficulty < 1: difficulty = 1

		#print(f'Difficulty: {difficulty}')

		return difficulty




def Magic(ludus):
	#print(f"Magic Function called")

	caster = Spellcaster(ludus)


	dif = caster.difficulty

	s1 = caster.slots(1)
	s2 = caster.slots(2)
	s3 = caster.slots(3)
	s4 = caster.slots(4)
	s5 = caster.slots(5)
	s6 = caster.slots(6)
	s7 = caster.slots(7)
	s8 = caster.slots(8)
	s9 = caster.slots(9)

	#print("Slots set")
	print(caster.spell_slots)


	Cantrip = ""
	count = 0
	c = ""
	while count < (6-dif) and count < 4:
		c = cantrip(ludus).string
		if not c in Cantrip:
			Cantrip += f"{c}\n"
			count += 1

	#print("Cantrips set")

	First = ""
	count = 0
	s = "dummy"
	while count < (6-dif) and count <= s1:
		s = first(ludus).string
		if not s in First:
			First += f"{s}\n"
		count += 1

	#print("First set")

	Second = ""
	count = 0
	s = "dummy"
	while count < (6-dif) and count <= s2:
		s = second(ludus).string
		if not s in Second:
			Second += f"{s}\n"
		count += 1

	#print("Second set")

	Third = ""
	count = 0
	s = "dummy"
	while count < (5-dif) and count < s3:
		s = third(ludus).string
		if not s in Third:
			Third += f"{s}\n"
		count += 1

	#print("Third set")

	Fourth = ""
	count = 0
	s = "dummy"
	while count < (5-dif) and count < s4:
		s = fourth(ludus).string
		if not s in Fourth:
			Fourth += f"{s}\n"
		count += 1

	#print("Fourth set")

	Fifth = ""
	count = 0
	s = "dummy"
	while count < (4-dif) and count < s5:
		s = fifth(ludus).string
		if not s in Fifth:
			Fifth += f"{s}\n"
		count += 1

	#print("Fifth set")


	Sixth = ""
	count = 0
	s = "dummy"
	while count < (4-dif) and count < s6:
		s = sixth(ludus).string
		if not s in Sixth:
			Sixth += f"{s}\n"
		count += 1

	#print("Sixth set")

	Seventh = ""
	count = 0
	s = "dummy"
	while count < (3-dif) and count < s7:
		s = seventh(ludus).string
		if not s in Seventh:
			Seventh += f"{s}\n"
		count += 1

	#print("Seventh set")

	Eigth = ""
	count = 0
	s = "dummy"
	while count < (3-dif) and count < s8:
		s = eighth(ludus).string
		if not s in Eigth:
			Eigth += f"{s}\n"
		count += 1

	#print("Eigth set")

	Ninth = ""
	count = 0
	s = "dummy"
	while count < (2-dif) and count < s9:
		s = ninth(ludus).string
		if not s in Ninth:
			Ninth += f"{s}\n"
		count += 1

	#print("Ninth set")

	Natural = natural(caster,ludus)


	Recharge = rechargable(ludus)

	result = ""

	if Cantrip: result += f"<h5>Cantrips:</h5>{Cantrip} \n"

	if is_ritualcaster(ludus): result += f"{ludus.title} can use spells as rituals.\n"


	if is_spellcaster(ludus):
		if First     and s1: result += f"<h5>[{s1}] 1st Level Spells:</h5>{First} \n"
		if Second    and s2: result += f"<h5>[{s2}] 2nd Level Spells:</h5>{Second} \n"
		if Third     and s3: result += f"<h5>[{s3}] 3rd Level Spells:</h5>{Third} \n"
		if Fourth    and s4: result += f"<h5>[{s4}] 4th Level Spells:</h5>{Fourth} \n"
		if Fifth     and s5: result += f"<h5>[{s5}] 5th Level Spells:</h5>{Fifth} \n"
		if Sixth     and s6: result += f"<h5>[{s6}] 6th Level Spells:</h5>{Sixth} \n"
		if Seventh   and s7: result += f"<h5>[{s7}] 7th Level Spells:</h5>{Seventh} \n"
		if Eigth     and s8: result += f"<h5>[{s8}] 8th Level Spells:</h5>{Eigth} \n"
		if Ninth     and s9: result += f"<h5>[{s9}] 9th Level Spells:</h5>{Ninth} \n"

	elif Natural:
		result += f"<h5>Natural Spells:</5> \n{Natural} \n"

	if Recharge: result += f"<h5>Rechargable Spells:</h5> {Recharge} \n"

	print("Magic finished")

	return result

def spell_of_level(ludus,n):
	if n == 1: return first(ludus).string
	if n == 2: return second(ludus).string
	if n == 3: return third(ludus).string
	if n == 4: return fourth(ludus).string
	if n == 5: return fifth(ludus).string
	if n == 6: return sixth(ludus).string
	if n == 7: return seventh(ludus).string
	if n == 8: return eighth(ludus).string
	if n == 9: return ninth(ludus).string
	return first(ludus).string


def natural(caster,ludus):
	"""
	Generate a list of daily spells for a caster based on their maximum spell level and difficulty.

	Args:
	caster (Caster): An object with attributes `maximum_spell_level` and `difficulty`.

	Returns:
	str: A formatted string listing the spells the caster can use per day.
	"""
	maximum = caster.maximum_spell_level
	dif = caster.difficulty


	daily1 = set()
	daily2 = set()
	daily3 = set()

	# Populate daily1 with spells of the highest level
	while len(daily1) < 3:
		spell = spell_of_level(ludus,maximum)
		daily1.add(spell)

	# If maximum spell level is 2 or higher, populate daily2 with spells up to a random level from 1 to (maximum - 1)
	if maximum >= 2:
		while len(daily2) < 3:
			spell = spell_of_level(ludus,Dice(maximum - 1))
			daily2.add(spell)

	# If maximum spell level is 3 or higher, populate daily3 with spells up to half the maximum level (rounded down)
	if maximum >= 3:
		while len(daily3) < 3:
			spell = spell_of_level(ludus,Dice(maximum - 2))
			daily3.add(spell)


	# Format the result string
	result = "1 use per day each:\n" + "\n".join(daily1) + "\n"
	if daily2:
		result += "2 uses per day each:\n" + "\n".join(daily2) + "\n"
	if daily3:
		result += "3 uses per day each:\n" + "\n".join(daily3)

	return result





def slots(ludus, level = 1, difficulty=1 ):
	character_level = ludus.level
	if difficulty < 1: difficulty = 1
	if difficulty > 6: difficulty = 6
	max_level = (1+character_level - difficulty) // (difficulty)

	# Contract limits
	if max_level < 0:   max_level = 0
	if max_level > 12:  max_level = 12

	if max_level == 0:      return 0
	if level > max_level:   return 0
	if level == max_level:  return 1
	slots = (1+max_level - level)//2
	slots = min(slots, 5)
	return int(slots)


def cantrip(ludus,dif=6):


	race = ludus.race
	background = ludus.background
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells_background = {
		"Artist": [		Guidance,		Guidance, Friends, WordofRadiance, ViciousMockery, Thaumaturgy, ShapeWater, ProduceFlame, Prestidigitation, MoldEarth, MinorIllusion, Message, Mending, MageHand, Light, EncodeThoughts, DancingLights, AcidSplash],
		"Barbarian": [	Guidance,		BoomingBlade, BladeWard, DancingLights, ViciousMockery, MageHand, MinorIllusion, Prestidigitation, Light, Message, Mending, Friends],
		"Bard": [		ViciousMockery, Prestidigitation, MinorIllusion,	Guidance,		EncodeThoughts, BoomingBlade, DancingLights, ViciousMockery, MageHand, MinorIllusion, Prestidigitation, Light, Message, Mending, Friends],
		"Bandit": [		SwordBurst, 	BladeWard, Thaumaturgy, MageHand, MinorIllusion, Prestidigitation, Message],
		"Berserker": [	BladeWard, 		Thaumaturgy, TrueStrike],
		"Charlatan": [	Guidance, 		Friends, MageHand, Prestidigitation, MinorIllusion, Message],
		"Cleric": [		Guidance,		SacredFlame, ChillTouch, Thaumaturgy, Guidance, Light, Resistance],
		"Crafter": [	Guidance,		Prestidigitation, Guidance, Light, MoldEarth, Mending, MageHand, Druidcraft, CreateBonfire, ControlFlames, ShapeWater, AcidSplash],
		"Criminal": [	ViciousMockery, Resistance, Mending, LightningLure, GreenFlameBlade, Prestidigitation, MinorIllusion, MageHand, ChillTouch, BladeWard, AcidSplash],
		"Cultist": [ 	Guidance,		ViciousMockery, TolltheDead, Thaumaturgy, SacredFlame, Light, Infestation, Guidance, EldritchBlast, ChillTouch, BoomingBlade, AcidSplash],
		"Druid": [		Guidance, 		ProduceFlame, Shillelagh,	Guidance,		Gust, Druidcraft, MoldEarth, AcidSplash, PrimalSavagery, ProduceFlame],
		"Expert": [		Guidance,		ControlFlames, AcidSplash, Guidance, Mending],
		"Explorer": [	Guidance,		MagicStone, Gust, BoomingBlade, Druidcraft, CreateBonfire],
		"Guard": [		Guidance,		SparetheDying, BoomingBlade, BladeWard, TrueStrike],
		"Healer": [		Guidance,		],
		"Hero": [		Guidance,		WordofRadiance, BoomingBlade, BladeWard, TrueStrike, Guidance],
		"Hunter": [		PrimalSavagery, Druidcraft, ProduceFlame, ShapeWater],
		"Knight": [		Guidance,		BoomingBlade, BladeWard],
		"Merchant": [	Guidance,		AcidSplash, MageHand, Message],
		"Monk": [		Guidance,		],
		"Mage": [		Firebolt, 		AcidSplash, Light, Prestidigitation, RayofFrost],
		"Noble": [		BoomingBlade, 	BladeWard, Prestidigitation, MageHand, Friends, Message],
		"Paladin": [	Guidance,		],
		"Priest": [		Guidance,		SacredFlame, WordofRadiance, Light, Thaumaturgy, Guidance],
		"Pirate": [		BoomingBlade, 	BladeWard, CreateBonfire, ControlFlames],
		"Prankster": [	ChillTouch, 	BladeWard, Message, Prestidigitation],
		"Ranger": [		Guidance,		],
		"Rogue": [		BoomingBlade, 	BladeWard, ViciousMockery, MinorIllusion],
		"Scholar": [	Guidance,		AcidSplash, Light, Prestidigitation, MageHand, MinorIllusion],
		"Shaman": [		Guidance,		ChillTouch, AcidSplash, PrimalSavagery, SappingSting, Druidcraft],
		"Soldier": [	BladeWard, 		BoomingBlade, GreenFlameBlade, SwordBurst, TrueStrike, Resistance, Guidance],
		"Sorcerer": [	DancingLights, 	ControlFlames, ShockingGrasp, RayofFrost, ProduceFlame, Prestidigitation, Mending, MagicStone, Light, Firebolt, BoomingBlade, ChillTouch, AcidSplash],
		"Spy": [		AcidSplash, 	MinorIllusion, Message],
		"Traveler": [	Guidance,		BoomingBlade, ControlFlames, MagicStone],
		"Warrior": [	BoomingBlade, 	BladeWard, 	GreenFlameBlade, TrueStrike, SwordBurst],
		"Witch": [		Guidance,		ChillTouch, AcidSplash, Druidcraft, Infestation],
		"Wizard": [		Firebolt, 		MageHand, 	Prestidigitation,	BoomingBlade, 	AcidSplash, Firebolt, Light, Prestidigitation],
		"Warlock": [	EldritchBlast, 	ChillTouch, BoomingBlade, AcidSplash],
		}


	spells_race = {
		"Aberration": [	EldritchBlast, 	MageHand, MinorIllusion, ChillTouch, AcidSplash],
		"Aven": [		PrimalSavagery,	Gust, 			Thaumaturgy, Guidance,	Gust, BoomingBlade],
		"Beast": [		PrimalSavagery,	Druidcraft, PrimalSavagery, ThornWhip,	Guidance,	TolltheDead, Thaumaturgy, SappingSting, MinorIllusion, Message, Light, Infestation, Gust, Druidcraft],
		"Beastfolk": [	PrimalSavagery,	Shillelagh, MagicStone, Druidcraft,	TrueStrike, Thaumaturgy, Shillelagh, ShapeWater, MoldEarth, MagicStone, Infestation, Guidance, Friends, Druidcraft],
		"Catfolk":	[	MinorIllusion, PrimalSavagery, Thaumaturgy],
		"Celestial": [	Light, SacredFlame, Guidance,	Guidance,	BoomingBlade, BladeWard, Light, SacredFlame],
		"Construct": [	Mending, ShockingGrasp, Prestidigitation,	Guidance,	ChillTouch, BoomingBlade, BladeWard, AcidSplash],
		"Dragon": [		PrimalSavagery,	Firebolt, AcidSplash, RayofFrost,	Firebolt, AcidSplash, ProduceFlame, ControlFlames],
		"Dwarf": [		Resistance, Light, Mending,	Guidance,	BladeWard, AcidSplash, Mending],
		"Elf": [		MinorIllusion, Prestidigitation, RayofFrost,	BoomingBlade, Light, RayofFrost, MinorIllusion],
		"Elemental": [	ControlFlames, ShapeWater, Gust],
		"Fey": [		Druidcraft, EldritchBlast, Thaumaturgy,	BoomingBlade, Druidcraft, Light, Prestidigitation],
		"Fiend": [		Thaumaturgy, EldritchBlast, ChillTouch,	ChillTouch, BoomingBlade, BladeWard, AcidSplash],
		"Giant": [		ThornWhip, Mending, Guidance,	Guidance,	BoomingBlade, BladeWard, Light],
		"Gnome": [		Prestidigitation, MageHand, MinorIllusion,	BoomingBlade, MinorIllusion, Prestidigitation, Mending],
		"Goblin": [		MinorIllusion, Thaumaturgy, ShockingGrasp,	MindSliver, AcidSplash, MinorIllusion, Prestidigitation, MageHand, ViciousMockery, Message, PoisonSpray],
		"Halfling": [	MageHand, Guidance, DancingLights,	AcidSplash, Mending, Light],
		"Human": [		Prestidigitation, Light, MageHand, Guidance,	],
		"Kobold": [		Firebolt, AcidSplash, ShockingGrasp],
		"Lizardfolk": [	PrimalSavagery,	ThornWhip, Druidcraft, PrimalSavagery,	AcidSplash, PrimalSavagery, Druidcraft],
		"Monstrosity": [Thaumaturgy, EldritchBlast, ShockingGrasp,	Thaumaturgy, PoisonSpray, Infestation, ChillTouch, AcidSplash],
		"Ooze": [		AcidSplash, Mending, Thaumaturgy,	AcidSplash, PoisonSpray, Mending],
		"Orc": [		PrimalSavagery,	Thaumaturgy, EldritchBlast, ChillTouch,	ChillTouch, BoomingBlade, BladeWard, AcidSplash],
		"Plant": [		Druidcraft, ThornWhip, Shillelagh,	Guidance,	AcidSplash, Druidcraft, PrimalSavagery, MoldEarth],
		"Snakefolk": [	PrimalSavagery,	PoisonSpray, Thaumaturgy, Druidcraft,	MindSliver, SappingSting, GreenFlameBlade, CreateBonfire, BoomingBlade, TrueStrike, Shillelagh, PrimalSavagery, MagicStone, Druidcraft, ChillTouch, AcidSplash],
		"Undead": [		ChillTouch, Thaumaturgy, EldritchBlast,	Infestation, EldritchBlast, ChillTouch, SparetheDying, LightningLure, DancingLights, BoomingBlade, AcidSplash],
	}


	spells_subrace = {
		"Arachnidfolk": [ChillTouch, AcidSplash],
		"Armored Bear": [BladeWard, BoomingBlade],
		"Atlantian": [AcidSplash, ShapeWater],
		"Cactoid Nomad": [BladeWard, PrimalSavagery],
		"Celestial Serpent": [AcidSplash, SacredFlame],
		"Celestial Stag": [BoomingBlade, Light],
		"Centaur": [BladeWard, Shillelagh],
		"Chronian": [ChillTouch],
		"Couatl": [AcidSplash, Light],
		"Cronusian": [ChillTouch],
		"Dark Elf": [ChillTouch, DancingLights],
		"Death Knight": [BladeWard, ChillTouch],
		"Deer Spirit": [ChillTouch, Druidcraft],
		"Deva": [ChillTouch, SacredFlame],
		"Eldritch Horror": [BoomingBlade, EldritchBlast],
		"Etherian": [ChillTouch],
		"Fata": [ChillTouch],
		"Feral": [BladeWard, PrimalSavagery],
		"Forgotten God": [ChillTouch, DivineWord],
		"Hag": [ChillTouch, AcidSplash],
		"Harpy": [ChillTouch, ViciousMockery],
		"Highlander": [BladeWard, TrueStrike],
		"Hobgoblin": [BladeWard, Firebolt],
		"Hydrakin": [BladeWard, CreateBonfire],
		"Illithid": [MindSliver, ChillTouch],
		"Insectfolk": [AcidSplash, PoisonSpray],
		"Islander": [Message, ShapeWater],
		"Kenku": [ChillTouch],
		"Kerberus Dog": [ChillTouch, Firebolt],
		"Kitsune Fox": [ChillTouch, BoomingBlade],
		"Kitsune": [	Guidance,	ChillTouch, BoomingBlade],
		"Lich": [AcidSplash, ChillTouch],
		"Living Spell": [BoomingBlade, EldritchBlast],
		"Magmaforged": [BladeWard, Firebolt],
		"Merfolk": [AcidSplash, ShapeWater],
		"Mischief Poltergeist": [AcidSplash, MageHand],
		"Monkey King": [BoomingBlade, BladeWard],
		"Old One": [MindSliver, ChillTouch],
		"Pixie": [AcidSplash, Druidcraft],
		"Primordial": [AcidSplash, ControlFlames],
		"Scorpionfolk": [BladeWard, AcidSplash],
		"Sharkfolk": [BladeWard, ShapeWater],
		"Skinwalker": [ChillTouch, PrimalSavagery],
		"Spider Queen": [AcidSplash, ChillTouch],
		"Stout": [BladeWard, BoomingBlade],
		"Sun Elf": [BladeWard, SacredFlame],
		"Sun Scarab": [AcidSplash, SacredFlame],
		"Swamp Crocfolk": [BladeWard, AcidSplash],
		"Swamp": [AcidSplash, MoldEarth],
		"Tartarian": [ChillTouch, AcidSplash],
		"Titan Rex": [BladeWard, TrueStrike],
		"Trickster": [AcidSplash, MinorIllusion],
		"Tundran": [ChillTouch, Frostbite],
		"Uranians": [ChillTouch, MindSliver],
		"Urbanite": [AcidSplash, Message],
		"Uruk": [BladeWard, ChillTouch],
		"Vampire": [ChillTouch, CharmPerson],
		"Vegetation Abomination": [BladeWard, AcidSplash],
		"Vulture Spirit": [ChillTouch, Infestation],
		"Wendigo": [BladeWard, Frostbite],
		"Werebear": [BladeWard, PrimalSavagery],
		"World Serpent's Spawn": [AcidSplash, PoisonSpray],
		"Wraith": [BladeWard, ChillTouch],
		}



	spells = [ Light]

	# Fetch from the possible spells for the selected race and background
	spells += list(set( spells_race.get(ludus.race, []) +
						spells_subrace.get(ludus.subrace, []) +
						spells_background.get(ludus.background, [])))

	if  "Dragon" in ludus.race    and     "Black" in ludus.subrace:
		spells += [AcidSplash]
	if  "Dragon" in ludus.race    and     "Green" in ludus.subrace:
		spells += [AcidSplash]
	if  "Dragon" in ludus.race    and     "Copper" in ludus.subrace:
		spells += [AcidSplash]
	if  "Dragon" in ludus.race    and     "Prismatic" in ludus.subrace:
		spells += [AcidSplash]
	if  "Dragon" in ludus.race    and     "Dragonborn" in ludus.subrace:
		spells += [BladeWard]
	if  "Shadow" in ludus.subrace:
		spells += [ChillTouch]

	spell = random.choice(spells)

	return spell


	'''
	number_of_spells = min(len(spells),
						   max(1,
							   6 - dif
							   )
						   )


	# Randomly select cantrips if there are any to choose from
	selected_spells = random.sample(spells, number_of_spells) if spells else []

	# Formatting the output
	return '<i>' + '\n'.join(spell.describe() for spell in selected_spells) + '</i>' if selected_spells else ""
	'''

def first(ludus,dif=6):

	#print('First Level Spelled called')

	# = Spell("")

	race = ludus.race
	background = ludus.background
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []



	# Dictionary initialization for spells by background
	spells_background = {
		"Artist": [		DisguiseSelf,	ColorSpray, SilveryBarbs, Identify, DistortValue, IllusoryScript, SilentImage, DisguiseSelf, AbsorbElements],
		"Bandit": [		DisguiseSelf,	Command, FogCloud, CharmPerson, DisguiseSelf, ExpeditiousRetreat, Sleep],
		"Bard": [		CureWounds, 	CharmPerson, DisguiseSelf,	DisguiseSelf,	ChromaticOrb, AbsorbElements, DisguiseSelf, HealingWord, Identify, FaerieFire, CharmPerson, SilentImage, Sleep, HideousLaughter, UnseenServant, SpeakwithAnimals],
		"Berserker": [	AbsorbElements, Bane, CompelledDuel, WrathfulSmite, SearingSmite],
		"Criminal": [	Bane, 			Sleep, SilentImage, CharmPerson, ExpeditiousRetreat, Entangle, DisguiseSelf, Alarm],
		"Charlatan": [	DisguiseSelf,	CharmPerson, AbsorbElements, DistortValue],
		"Commoner": [	DisguiseSelf,	CharmPerson, AbsorbElements, Goodberry],
		"Cultist": [	Bless, ArmsOfHadar, ChaosBolt],
		"Crafter": [DistortValue, Identify, UnseenServant],
		"Cleric": [Bless, CureWounds, ShieldofFaith],
		"Druid": [		CureWounds, Entangle, FaerieFire,	BeastBond, AbsorbElements, Entangle],
		"Expert": [ComprehendLanguages, Catapult, Identify],
		"Explorer": [	DisguiseSelf,	AnimalFriendship, DetectMagic, AbsorbElements],
		"Guard": [CauseFear, Shield, Heroism],
		"Healer": [Bless, CureWounds, HealingWord],
		"Hero": [Bless, CureWounds, AbsorbElements],
		"Hunter": [EnsnaringStrike, AbsorbElements, HailofThorns],
		"Knight": [Ceremony, AbsorbElements, ShieldofFaith],
		"Mage": [		DisguiseSelf,	BurningHands, AbsorbElements, MageArmor],
		"Merchant": [	DisguiseSelf,	DistortValue, ComprehendLanguages, DetectMagic],
		"Monk": [Bless, CureWounds, AbsorbElements],
		"Ninja": [		DisguiseSelf,	Bane, CauseFear, SilentImage],
		"Noble": [CompelledDuel, CharmPerson, DisguiseSelf, Identify, FeatherFall, Alarm],
		"Pirate": [ArmsOfHadar, ChaosBolt, FogCloud],
		"Priest": [Bless, DetectEvilandGood, Ceremony],
		"Paladin": [Bless, ShieldofFaith, Heroism],
		"Prankster": [	DisguiseSelf,	AnimalFriendship, Grease, FalseLife],
		"Ranger": [CreateorDestroyWater, AbsorbElements, Goodberry],
		"Rogue": [Grease, SilentImage, Sleep],
		"Scholar": [AbsorbElements, Identify, ComprehendLanguages],
		"Shaman": [Bless, ArmsOfHadar, DetectMagic, AbsorbElements],
		"Soldier": [Alarm, Command, Shield, Heroism, CureWounds, ExpeditiousRetreat, ProtectionfromEvilandGood],
		"Sorcerer": [DetectMagic, ChromaticOrb, ColorSpray, AbsorbElements, MagicMissile],
		"Spy": [		DisguiseSelf,	DetectEvilandGood, CharmPerson, DisguiseSelf],
		"Traveler": [	DisguiseSelf,	DisguiseSelf, Sanctuary, MageArmor, Jump, Identify, Heroism, FogCloud, FindFamiliar, FeatherFall, DistortValue, DetectPoisonandDisease, DetectMagic, Catapult, BeastBond, AnimalFriendship],
		"Warlock": [	DisguiseSelf,	ArmsOfHadar, ArmorofAgathys, Hex],
		"Warrior": [	InflictWounds, 	CompelledDuel, WrathfulSmite],
		"Witch": [		DisguiseSelf,	Bless, ArmsOfHadar, AbsorbElements, WitchBolt],
		"Wizard": [		MagicMissile, 	MageArmor, Shield,	DisguiseSelf,	Catapult, FaerieFire, MagicMissile],
	}

	# Dictionary initialization for spells by race
	spells_race = {
		"Aberration": [	MagicMissile, Shield, DetectMagic,	ArmsOfHadar, Bane, DetectMagic],
		"Aven": [		FeatherFall, GuidingBolt, HealingWord,	Bless, Ceremony, BeastBond],
		"Beast": [		CureWounds, Entangle, FaerieFire,	Bless, CureWounds, SpeakwithAnimals, Sanctuary, PurifyFoodandDrink, ProtectionfromEvilandGood, HuntersMark, Goodberry, FogCloud, FindFamiliar, FeatherFall, ExpeditiousRetreat],
		"Beastfolk": [	CureWounds, AnimalFriendship, SpeakwithAnimals,	CreateorDestroyWater, Sanctuary, HuntersMark, Goodberry, FogCloud, BeastBond, AbsorbElements],
		"Catfolk": [	CharmPerson, FeatherFall, SilentImage,	DisguiseSelf,	],
		"Celestial": [	CureWounds, GuidingBolt, ShieldofFaith,	DisguiseSelf,	Bless, CureWounds, AbsorbElements],
		"Construct": [	Shield, Identify, MagicMissile,	BurningHands, AbsorbElements, MageArmor],
		"Dragon": [		BurningHands, Thunderwave, ChromaticOrb,	Command, AbsorbElements, BurningHands],
		"Dwarf": [		ShieldofFaith, GuidingBolt, InflictWounds,	Catapult, AbsorbElements, ShieldofFaith],
		"Elemental": [	BurningHands, Thunderwave, IceKnife,	EarthTremor, AbsorbElements, BurningHands],
		"Elf": [		MagicMissile, Shield, DetectMagic,	Identify, FaerieFire, Longstrider],
		"Fey": [		FaerieFire, CureWounds, CharmPerson,	DisguiseSelf,	CauseFear, CharmPerson, FaerieFire],
		"Fiend": [		HellishRebuke, CharmPerson, WitchBolt,	DisguiseSelf,	ArmsOfHadar, DissonantWhispers, AbsorbElements, HellishRebuke],
		"Giant": [		EnlargeReduce, Thunderwave, EarthTremor,	CompelledDuel, Catapult, AbsorbElements, EarthTremor],
		"Gnome": [		MagicMissile, Shield, DetectMagic,	ColorSpray, AbsorbElements, MageArmor],
		"Goblin": [		MagicMissile, Shield, Thunderwave,	ArmsOfHadar, DetectPoisonandDisease, CharmPerson, Sleep, DissonantWhispers, HideousLaughter, FaerieFire, Snare, Entangle],
		"Halfling": [	Bless, CureWounds, FaerieFire,	ComprehendLanguages, ExpeditiousRetreat, SilentImage],
		"Human": [		MagicMissile, Shield, DetectMagic,	DistortValue, Bless, Shield],
		"Kobold": [		BurningHands, Thunderwave, MagicMissile,	Grease, SilentImage, ColorSpray],
		"Lizardfolk": [	CureWounds, Entangle, AnimalFriendship,	FalseLife, DetectPoisonandDisease, RayofSickness],
		"Monstrosity": [MagicMissile, Shield, DetectMagic,	ChromaticOrb, AbsorbElements, CauseFear],
		"Ooze": [		Grease, MagicMissile, Shield,	DisguiseSelf,	ArmsOfHadar, DisguiseSelf, AbsorbElements, Grease],
		"Orc": [		InflictWounds, ShieldofFaith, GuidingBolt,	CompelledDuel, AbsorbElements, CauseFear],
		"Plant": [		Entangle, CureWounds, Goodberry,	CharmPerson, Entangle, Goodberry],
		"Snakefolk": [	CharmPerson, DetectPoisonandDisease, Entangle,	DisguiseSelf,	ArmsOfHadar, Command, DetectPoisonandDisease],
		"Undead": [		InflictWounds, FalseLife, RayofSickness,	ArmsOfHadar, Bane, ArmorofAgathys, Hex, FalseLife],
	}

	# Dictionary initialization for spells by subrace
	spells_subrace = {
		"Beholder": [AbsorbElements, CharmPerson, DisguiseSelf],
		"Chaos Warper": [AbsorbElements, ChaosBolt, EarthTremor],
		"Eldritch Horror": [AbsorbElements, ArmsOfHadar, CauseFear],
		"Living Spell": [AbsorbElements, MageArmor, MagicMissile],
		"Vampire": [	DisguiseSelf,	FalseLife, CharmPerson, Sleep],
	}

	# Fetch from the possible spells for the selected race and background
	spells = list(set( spells_race.get(ludus.race, []) +
						spells_subrace.get(ludus.subrace, []) +
						spells_background.get(ludus.background, [])))

	if len(spells) < 3:
		spells = list(set(spells_race.get(ludus.race, []) +
						  spells_subrace.get(ludus.subrace, []) +
						  spells_background.get(ludus.background, []) +
						  [Bless, CureWounds, AbsorbElements]))


	spell = random.choice(spells)

	print(f'First level spell: {spell.name}')

	return spell

def second(ludus, dif=6):
	print(f"Second Level Spell:")


	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	spells_background = {
		"Artist": [MistyStep, PhantasmalForce, MirrorImage, Darkness, EnhanceAbility],
		"Bandit": [AganazzarScorcher, Darkness, PassWithoutTrace, Silence, Invisibility, AlterSelf],
		"Barbarian": [AganazzarScorcher, BrandingSmite, MagicWeapon, FindSteed],
		"Bard": [		EnhanceAbility, Suggestion, Silence,	Invisibility, Knock, DetectThoughts, EnhanceAbility, LesserRestoration, ZoneOfTruth, CalmEmotions, HeatMetal, Suggestion, PhantasmalForce],
		"Berserker": [AganazzarScorcher, BrandingSmite, MagicWeapon, FindSteed],
		"Criminal": [AganazzarScorcher, SpiderClimb, Silence, ProtectionFromPoison, PassWithoutTrace, MagicAura, LocateObject, GlowingCoin, Invisibility],
		"Charlatan": [PassWithoutTrace, AlterSelf, EnhanceAbility],
		"Commoner": [AganazzarScorcher, Blur, Darkvision],
		"Cultist": [ContinualFlame, CalmEmotions, SeeInvisibility, EnhanceAbility, BrandingSmite, MagicWeapon, Darkness, PhantasmalForce],
		"Druid": [	Barkskin, Moonbeam, SpikeGrowth,	ContinualFlame, Earthbind, CalmEmotions, HeatMetal, SeeInvisibility, AnimalMessenger, PassWithoutTrace],
		"Explorer": [LesserRestoration, PassWithoutTrace, DetectMagic],
		"Guard": [MagicWeapon, FlameBlade, Aid],
		"Hero": [EnhanceAbility, PassWithoutTrace, BrandingSmite, Aid],
		"Mage": [AganazzarScorcher, MirrorImage, MistyStep, ScorchingRay],
		"Noble": [DetectThoughts, Suggestion, LocateObject, SeeInvisibility, MagicAura, PassWithoutTrace],
		"Ninja": [SeeInvisibility, Invisibility, AlterSelf, MagicWeapon, Silence, PassWithoutTrace],
		"Pirate": [AganazzarScorcher, MistyStep, Knock, DustDevil],
		"Priest": [ZoneOfTruth, WitherBloom, Suggestion, SpiritualWeapon, PrayerOfHealing, MagicAura, LesserRestoration, HealingSpirit, GentleRepose, Aid],
		"Paladin": [BrandingSmite, Aid, MagicWeapon, LesserRestoration],
		"Soldier": [MagicWeapon, Aid, EnhanceAbility, Blur, ProtectionFromPoison, FindSteed],
		"Shaman": [ScorchingRay, Pyrotechnics, GustOfWind, FortunesFavor, MirrorImage],
		"Sorcerer": [Pyrotechnics, GustOfWind, FortunesFavor, ScorchingRay, MirrorImage, Suggestion],
		"Spy": [DetectThoughts, Darkness, MistyStep],
		"Traveler": [BorrowedKnowledge, Augury, FindTraps, LocateAnimalsPlants],
		"Prankster": [Darkness, Invisibility, MistyStep],
		"Warlock": [ArmsOfHadar, ArmorofAgathys, ScorchingRay, Darkness, HoldPerson],
		"Warrior": [InflictWounds, CompelledDuel, BrandingSmite, MagicWeapon],
		"Witch": [	Bless, CharmPerson, ScorchingRay, Darkness, DetectThoughts, MirrorImage],
		"Wizard": [	MistyStep, MirrorImage, ScorchingRay,	Catapult, FaerieFire, MistyStep, Invisibility, DetectMagic],
	}

	spells_race = {
		"Aberration": [	Invisibility, MirrorImage, MistyStep,	BlindnessDeafness, DetectThoughts, Darkness],
		"Aven": [	GustofWind, Moonbeam, LesserRestoration,	Blur, MistyStep, EnhanceAbility],
		"Beast": [	Barkskin, Moonbeam, SpikeGrowth,	SummonBeast, Invisibility, HealingSpirit, FlockofFamiliars, Earthbind, CrownofMadness, CalmEmotions, BorrowedKnowledge, BeastSense, Barkskin, Augury, AnimalMessenger],
		"Beastfolk": [	Barkskin, SpikeGrowth, EnhanceAbility,	CreateorDestroyWater, Sanctuary, Jump, HuntersMark, Goodberry, FogCloud, BeastBond, AbsorbElements],
		"Catfolk": [MirrorImage, Invisibility, Suggestion],
		"Celestial": [LesserRestoration, SpiritualWeapon, Aid,	DetectThoughts, Augury, Aid, FlameBlade, LesserRestoration],
		"Construct": [HeatMetal, Shatter, EnhanceAbility,	BurningHands, ScorchingRay],
		"Dragon": [ScorchingRay, Shatter, AcidArrow,	Command, ScorchingRay,BorrowedKnowledge, Darkvision, DragonsBreath, FlamingSphere, GustOfWind, HoldPerson, GlowingCoin, Knock, Levitate, Pyrotechnics, ScorchingRay,  SpiderClimb, Darkness, AlterSelf, AnimalMessenger, EnhanceAbility, SeeInvisibility, CalmEmotions, ContinualFlame, ZoneOfTruth ],
		"Dwarf": [SpiritualWeapon, LesserRestoration, HoldPerson,	Catapult, MagicWeapon],
		"Elemental": [FlamingSphere, GustofWind, MistyStep,	EarthTremor, ScorchingRay],
		"Elf": [Invisibility, MirrorImage, MistyStep,	Identify, MistyStep, EnhanceAbility],
		"Fey": [MirrorImage, MistyStep, Suggestion,	CauseFear, Suggestion, PhantasmalForce],
		"Fiend": [	Darkness, Suggestion, AganazzarsScorcher,	ArmsOfHadar, DissonantWhispers, ScorchingRay, HoldPerson],
		"Giant": [	MaximiliansEarthenGrasp, EnlargeReduce, Shatter,	CompelledDuel, Catapult, Earthbind, HeatMetal],
		"Gnome": [	Invisibility, MirrorImage, MistyStep,	ColorSpray, MirrorImage, Knock],
		"Goblin": [	Invisibility, MirrorImage, Shatter,	Invisibility, Silence, Suggestion, MirrorImage, PhantasmalForce, PassWithoutTrace, Web],
		"Halfling": [	EnhanceAbility, PassWithoutTrace, Silence,	ComprehendLanguages, ExpeditiousRetreat, PassWithoutTrace, Mischief],
		"Human": [		Invisibility, MirrorImage, MistyStep,	DistortValue, Suggestion, LocateObject],
		"Kobold": [		ScorchingRay, Shatter, MagicWeapon,	Grease, ScorchingRay, MistyStep],
		"Lizardfolk": [	Barkskin, Moonbeam, SpikeGrowth,	SpikeGrowth, PassWithoutTrace, MagicWeapon, Invisibility, FlockofFamiliars, Barkskin, LesserRestoration],
		"Monstrosity": [Invisibility, MirrorImage, MistyStep,	ChromaticOrb, MirrorImage, HoldPerson],
		"Ooze": [		AcidArrow, MistyStep, SpiderClimb,	ArmsOfHadar, DisguiseSelf, EnlargeReduce, AlterSelf, Invisibility],
		"Orc": [		HoldPerson, SpiritualWeapon, LesserRestoration,	CompelledDuel, ScorchingRay, BrandingSmite],
		"Plant": [		Barkskin, SpikeGrowth, EnhanceAbility,	CharmPerson, Barkskin, AnimalMessenger, Silence, AlterSelf, MagicWeapon, ZoneOfTruth],
		"Snakefolk": [	HoldPerson, MistyStep, LesserRestoration,	AnimalMessenger, AlterSelf, SpikeGrowth, PassWithoutTrace, MagicWeapon, Invisibility, FlockofFamiliars, Barkskin],
		"Undead": [		BlindnessDeafness, HoldPerson, RayofEnfeeblement,	ArmsOfHadar, Bane, ArmorofAgathys, Hex, ScorchingRay, Darkness],
	}

	spells_subrace = {
		"Guardian Kong": [MagicWeapon, LocateAnimalsPlants, CrownofMadness, EnlargeReduce],
		"Vampire": [Suggestion, Darkness, HoldPerson],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	if not spells:
		spells = [MagicMouth, SpiderClimb, AlterSelf]

	spell = random.choice(spells)

	print(f"{spell.name}")

	return spell

def third(ludus, dif=6):

	print("Third Level Spell:")

	race = ludus.race
	background = ludus.background
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	spells_background = {
		"Artist": [		SpiritGuardians,	ElementalWeapon,	CharmMonster,		Sending,			Nondetection,		Counterspell, Antagonize, Nondetection, MajorImage, MotivationalSpeech, FastFriends, SpeakPlants],
		"Bandit": [		ElementalWeapon,	Nondetection,		CreateFoodWater,	HypnoticPattern, TinyHut, Nondetection, DispelMagic, Blink, BlindingSmite, Slow],
		"Barbarian": [	SpiritGuardians,	ElementalWeapon,	CharmMonster,		Counterspell, CallLightning, EruptingEarth, GlyphWarding, ThunderStep],
		"Bard": [		HypnoticPattern, 	MajorImage, 		TinyHut,			SpiritGuardians,	SpeakwithDead,		CharmMonster,		Sending,			Counterspell, Antagonize, DispelMagic, TinyHut, HypnoticPattern, MajorImage, Sending, Tongues, Fear, CharmMonster, StinkingCloud, SpeakwithDead, Blink, Catnap, FastFriends],
		"Berserker": [	SpiritGuardians,	ElementalWeapon,	Counterspell, 		CrusadersMantle, ElementalWeapon, Fear, SpiritGuardians, Fireball, ThunderStep, CallLightning],
		"Charlatan": [	SpiritGuardians,	SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		Counterspell, Antagonize, FastFriends, MotivationalSpeech, GaseousForm, Blink, InciteGreed],
		"Criminal": [	CharmMonster,		Sending,			Nondetection,		Counterspell, Antagonize, Tongues, Nondetection, InciteGreed, FastFriends, DispelMagic, Blink, BlindingSmite, EnemiesAbound, PlantGrowth, EruptingEarth],
		"Cultist": [	SpiritGuardians,	ElementalWeapon,	SpeakwithDead,		CharmMonster,		Nondetection,		WaterWalk, Counterspell, Clairvoyance, AnimateDead, HypnoticPattern, BestowCurse, HungerHadar, SpiritShroud, SpeakwithDead],
		"Cleric": [		SpiritGuardians,	SpeakwithDead,		AnimateDead, 		BeaconHope, RemoveCurse, SpiritShroud, MassHealingWord, GlyphWarding],
		"Commoner": [	SpiritGuardians,	CharmMonster,		Sending,			Nondetection,		CreateFoodWater,	],
		"Crafter": [	ElementalWeapon,	CharmMonster,		Sending,			CreateFoodWater,	],
		"Druid": [		CallLightning, 		PlantGrowth, 		WindWall,			SpiritGuardians,	CharmMonster,		CreateFoodWater,	WaterBreathing, WaterWalk, WindWall, CreateFoodWater, Daylight, ConjureAnimals, Catnap, BestowCurse, CallLightning, SpeakPlants, PlantGrowth],
		"Explorer": [	SpiritGuardians,	ElementalWeapon,	CharmMonster,		Sending,			Nondetection,		CreateFoodWater,	CreateFoodWater, PhantomSteed, WaterBreathing, Nondetection, Clairvoyance, Daylight, TinyHut],
		"Expert": [		ElementalWeapon,	Sending,			Nondetection,		],
		"Fighter": [	ElementalWeapon,	Antagonize, 		EruptingEarth, 		FastFriends, SpiritGuardians, Fear, LightningBolt, Fly],
		"Guard": [		SpiritGuardians,	ElementalWeapon,	SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		Antagonize, GlyphWarding, SpiritGuardians, Fear, EruptingEarth, BlindingSmite, ElementalWeapon],
		"Hunter": [		CharmMonster,		Nondetection,		CreateFoodWater,	Antagonize, FlameArrows, ConjureBarrage, EruptingEarth, MeldIntoStone, CallLightning, Haste, ProtectionfromEnergy],
		"Healer": [		CreateFoodWater,	AnimateDead, 		LifeTransference, 	MassHealingWord, SpiritGuardians, BeaconHope, Revivify, RemoveCurse],
		"Hero": [		ElementalWeapon,	CharmMonster,		CreateFoodWater,	],
		"Knight": [		SpiritGuardians,	ElementalWeapon,	SpeakwithDead,		CharmMonster,		Antagonize, CrusadersMantle, ElementalWeapon, MagicCircle, Fly, ProtectionfromEnergy, Haste],
		"Mage": [		CharmMonster,		AnimateDead, 		Counterspell, 		Fireball, MajorImage, Haste, Fly, DispelMagic, Tongues],
		"Merchant": [	ElementalWeapon,	CharmMonster,		Sending,			CreateFoodWater,	],
		"Monk": [		SpiritGuardians,	ElementalWeapon,	SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		CreateFoodWater,	],
		"Noble": [		SpiritGuardians,	SpeakwithDead,		CreateFoodWater,	Antagonize, Tongues, Sending, TinyHut, Clairvoyance, Counterspell, Fear, MotivationalSpeech, GaseousForm, DispelMagic],
		"Ninja": [		SpiritGuardians,	SpeakwithDead,		Nondetection,		],
		"Pirate": [		Sending,			Nondetection,		CreateFoodWater,	Antagonize, GaseousForm, InciteGreed, TidalWave, HypnoticPattern, CallLightning, ThunderStep],
		"Priest": [		SpiritGuardians,	SpeakwithDead,		CreateFoodWater,	AnimateDead, SpiritGuardians, SpeakwithDead, Revivify, RemoveCurse, MassHealingWord, LifeTransference, HypnoticPattern, GlyphWarding, DispelMagic, Daylight, Counterspell, Clairvoyance, BeaconHope, TinyServant],
		"Paladin": [	ElementalWeapon,	CharmMonster,		Antagonize, CrusadersMantle, AuraVitality, BlindingSmite, Haste, ElementalWeapon, MagicCircle],
		"Prankster": [	CharmMonster,		Nondetection,		CreateFoodWater,	Antagonize, Tongues, TinyHut, WaterBreathing, Nondetection, SpeakwithDead, PlantGrowth],
		"Ranger": [		CharmMonster,		Nondetection,		CreateFoodWater,	],
		"Rogue": [		SpeakwithDead,		Sending,			Nondetection,		Antagonize, Blink, Fear, Nondetection, EnemiesAbound, FastFriends, Slow, GaseousForm],
		"Sorcerer": [	WindWall, 			WallSand, 			PulseWave, MagicCircle, Fly, Fireball, Counterspell, CallLightning, Haste, SleetStorm, LightningBolt, ThunderStep],
		"Shaman": [		SpeakwithDead,		CharmMonster,		CreateFoodWater,	AnimateDead, BestowCurse, LifeTransference, RemoveCurse, GlyphWarding, SpiritShroud, SpeakwithDead, CreateFoodWater],
		"Soldier": [	ElementalWeapon,	CreateFoodWater,	Antagonize, ProtectionfromEnergy, Haste, DispelMagic, Revivify, CrusadersMantle, Slow, EruptingEarth, ElementalWeapon, LightningArrow],
		"Spy": [		SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		Nondetection,		Antagonize, Nondetection, Tongues, InciteGreed, Clairvoyance, Blink, GaseousForm],
		"Scholar": [	SpeakwithDead,		CharmMonster,		],
		"Traveler": [	ElementalWeapon,	SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		CreateFoodWater,	Antagonize, Blink, Tongues, Sending, TinyHut, Clairvoyance, Counterspell, Fly, Fear, PhantomSteed, WaterWalk, HypnoticPattern],
		"Warlock": [	ElementalWeapon,	SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		Antagonize, AnimateDead, HungerHadar, Fear, VampiricTouch, EnemiesAbound, GaseousForm],
		"Warrior": [	ElementalWeapon,	CreateFoodWater,	],
		"Witch": [		SpeakwithDead,		CharmMonster,		Sending,			Nondetection,		AnimateDead, BestowCurse, PlantGrowth, VampiricTouch, LifeTransference, SpeakwithDead, HypnoticPattern, GaseousForm],
		"Wizard": [		Counterspell, 		Fireball, 			Fly,				CharmMonster,		Sending,			AnimateDead, Counterspell, Fireball, HypnoticPattern, MajorImage, Slow, Blink, Fly, LightningBolt, DispelMagic],
	}

	spells_race = {
		"Aberration": [Fireball, Counterspell, Fly],
		"Aven": [		Fly, WindWall, LightningBolt, 	Clairvoyance, Fly, WindWall, Slow, SleetStorm, Fear],
		"Beast": [		CallLightning, PlantGrowth, WindWall,	Haste, Fear, SpiritGuardians, Revivify, RemoveCurse, Nondetection, Daylight, ConjureAnimals, Blink, AuraVitality, EruptingEarth, CallLightning, Tongues, ProtectionfromEnergy],
		"Beastfolk": [	CallLightning, ConjureAnimals, Daylight,	CreateFoodWater,	Haste, Fear, SpiritGuardians, Revivify, ConjureAnimals, EruptingEarth, Daylight],
		"Catfolk": [	Catnap, Haste, HypnoticPattern,	CreateFoodWater,	],
		"Celestial": [	Revival, BeaconofHope, Daylight,	CreateFoodWater,	BeaconHope, AnimateDead, SpiritGuardians, Daylight, CrusadersMantle, Tongues, LifeTransference],
		"Construct": [Counterspell, DispelMagic, Fly],
		"Dragon": [		LightningBolt, Fireball, EruptingEarth,Fear, Fireball, LightningBolt, ProtectionfromEnergy, Fly, Haste, WallSand],
		"Dwarf": [		SpiritGuardians, Revivify, BestowCurse,	CreateFoodWater,	],
		"Elf": [		DispelMagic, MajorImage, PlantGrowth,	Fireball, Counterspell, Fly,	CreateFoodWater,	],
		"Elemental": [Fireball, WaterBreathing, WindWall],
		"Fey": [		CreateFoodWater,	ConjureAnimals, HypnoticPattern, MajorImage, PlantGrowth, Nondetection, SpeakPlants, FastFriends],
		"Fiend": [		Fear, Fireball, VampiricTouch],
		"Giant": [		EruptingEarth, Fly, WaterBreathing,	CreateFoodWater,	],
		"Gnome": [Fireball, Counterspell, Fly],
		"Goblin": [		Fireball, Counterspell, Fly,	Fear, MajorImage, BestowCurse, EnemiesAbound, Blink, GaseousForm, StinkingCloud, HypnoticPattern, FastFriends, InciteGreed, HungerHadar],
		"Halfling": [	DispelMagic, CallLightning, WaterBreathing,	CreateFoodWater,	Nondetection, TinyHut, Haste, MajorImage, Blink, Slow, WaterWalk],
		"Human": [		Fireball, Counterspell, Fly,	CreateFoodWater,	],
		"Kobold": [LightningBolt, Fireball, EruptingEarth],
		"Lizardfolk": [	CallLightning, PlantGrowth, WaterBreathing,	Tongues, HungerHadar, Fear, ElementalWeapon, EruptingEarth, MeldIntoStone, StinkingCloud, ProtectionfromEnergy, Fly],
		"Monstrosity": [Fireball, Counterspell, Fly],
		"Ooze": [Fireball, Fly, GaseousForm],
		"Orc": [		SpiritGuardians, Revivify, BestowCurse,	CreateFoodWater,	],
		"Plant": [		CallLightning, PlantGrowth, WindWall,	CreateFoodWater,	AnimateDead, PlantGrowth, Daylight, SpeakPlants, ConjureAnimals, WaterBreathing, GlyphWarding],
		"Snakefolk": [BestowCurse, Fly, WaterBreathing],
		"Undead": [	AnimateDead, BestowCurse, Fear,	AnimateDead, VampiricTouch, LifeTransference, SpeakwithDead, StinkingCloud, HungerHadar],

			}

	spells_subrace = {
		"Guardian Kong": [StinkingCloud, SpiritShroud, SpiritGuardians, Slow, TinyHut, EnemiesAbound, CreateFoodWater],
		"Vampire": [VampiricTouch, AnimateDead, GaseousForm, Fear, HungerHadar, LifeTransference],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [Fireball, Fly, Counterspell]

	spell = random.choice(spells)

	print(f"{spell.name}")

	return spell

def fourth(ludus, dif=6):
	#print('Fourth Level Spell:')


	race = ludus.race
	background = ludus.background
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	spells_background = {
		"Artist": [PhantasmalKiller, HallucinatoryTerrain, GreaterInvisibility, DimensionDoor, Fabricate, ControlWater],
		"Bandit": [DimensionDoor, GreaterInvisibility, ArcaneEye, Confusion, Blight, SickeningRadiance],
		"Bard": [		DimensionDoor, GreaterInvisibility, Polymorph,	ArcaneEye, DimensionDoor, Polymorph, GreaterInvisibility, FreedomOfMovement, HallucinatoryTerrain, LocateCreature, Compulsion, Confusion, Geas, StoneShape, Fabricate, SickeningRadiance, RaulothimPsychicLance],
		"Berserker": [Stoneskin, FreedomOfMovement, Compulsion, GraspingVine, FireShield, WallofFire],
		"Charlatan": [ArcaneEye, Fabricate, GreaterInvisibility, DimensionDoor, SecretChest],
		"Criminal": [FaithfulHound, FreedomOfMovement, Divination, DimensionDoor, Confusion, PhantasmalKiller, SickeningRadiance],
		"Cultist": [StormSphere, AuraLife, ArcaneEye, PhantasmalKiller, Blight, ShadowofMoil, EvardsBlackTentacles],
		"Cleric": [AnimateDead, BeaconHope, RemoveCurse, SpiritShroud, MassHealingWord, GlyphWarding, PhantasmalKiller, Banishment, GuardianFaith],
		"Druid": [	ConjureWoodlandBeings, DominateBeast, GraspingVine,	GuardianNature, StormSphere, WaterySphere, LocateCreature, AuraLife, AuraofPurity, GiantInsect, ControlWater, StoneShape],
		"Fighter": [Antagonize, EruptingEarth, FastFriends, SpiritGuardians, Fear, LightningBolt, Fly, Stoneskin, DimensionDoor, GreaterInvisibility],
		"Guard": [Antagonize, GlyphWarding, SpiritGuardians, Fear, EruptingEarth, BlindingSmite, ElementalBane, GuardianFaith],
		"Explorer": [ArcaneEye, LocateCreature, SecretChest, FindGreaterSteed, FreedomOfMovement],
		"Hunter": [FaithfulHound, ElementalBane, ConjureWoodlandBeings, ConjureMinorElementals],
		"Healer": [AnimateDead, LifeTransference, MassHealingWord, SpiritGuardians, BeaconHope, Revivify, RemoveCurse, DeathWard, AuraofPurity],
		"Knight": [Antagonize, CrusadersMantle, ElementalWeapon, MagicCircle, Fly, ProtectionfromEnergy, Haste, Stoneskin, StaggeringSmite],
		"Mage": [AnimateDead, Counterspell, Fireball, MajorImage, Haste, Fly, DispelMagic, Tongues, ArcaneEye, PhantasmalKiller, Fabricate, GravitySinkhole],
		"Noble": [Antagonize, Tongues, Sending, TinyHut, Clairvoyance, Counterspell, Fear, MotivationalSpeech, GaseousForm, DispelMagic, SecretChest, PrivateSanctum],
		"Pirate": [Antagonize, GaseousForm, InciteGreed, TidalWave, HypnoticPattern, CallLightning, ThunderStep, ControlWater, WaterySphere],
		"Priest": [AnimateDead, SpiritGuardians, SpeakwithDead, Revivify, RemoveCurse, MassHealingWord, LifeTransference, HypnoticPattern, GlyphWarding, DispelMagic, Daylight, Counterspell, Clairvoyance, BeaconHope, TinyServant, GuardianFaith, AuraofPurity],
		"Paladin": [Antagonize, CrusadersMantle, AuraVitality, BlindingSmite, Haste, ElementalWeapon, MagicCircle, DeathWard, GuardianFaith],
		"Rogue": [Antagonize, Blink, Fear, Nondetection, EnemiesAbound, FastFriends, Slow, GaseousForm, GreaterInvisibility, ShadowofMoil, Confusion],
		"Sorcerer": [WindWall, WallSand, PulseWave, MagicCircle, Fly, Fireball, Counterspell, CallLightning, Haste, SleetStorm, LightningBolt, ThunderStep, StormSphere, ElementalBane, IceStorm],
		"Shaman": [AnimateDead, BestowCurse, LifeTransference, RemoveCurse, GlyphWarding, SpiritShroud, SpeakwithDead, CreateFoodWater, ControlWater, WaterySphere],
		"Soldier": [Antagonize, ProtectionfromEnergy, Haste, DispelMagic, Revivify, CrusadersMantle, Slow, EruptingEarth, ElementalWeapon, LightningArrow, DeathWard, FreedomOfMovement, Stoneskin, AuraLife, AuraofPurity, GuardianFaith],
		"Spy": [Antagonize, Nondetection, Tongues, InciteGreed, Clairvoyance, Blink, GaseousForm, GreaterInvisibility, ShadowofMoil, SickeningRadiance],
		"Traveler": [Antagonize, Blink, Tongues, Sending, TinyHut, Clairvoyance, Counterspell, Fly, Fear, PhantomSteed, WaterWalk, HypnoticPattern, ArcaneEye, LocateCreature, SecretChest, FreedomOfMovement],
		"Prankster": [Antagonize, Tongues, TinyHut, WaterBreathing, Nondetection, SpeakwithDead, PlantGrowth, FreedomOfMovement, Stoneskin, GuardianNature, ConjureMinorElementals],
		"Warlock": [Antagonize, AnimateDead, HungerHadar, Fear, VampiricTouch, EnemiesAbound, GaseousForm, ShadowofMoil, PhantasmalKiller, SickeningRadiance, WallofFire, SummonGreaterDemon],
		"Witch": [	AnimateDead, BestowCurse, PlantGrowth, VampiricTouch, LifeTransference, SpeakwithDead, HypnoticPattern, GaseousForm, ControlWater, SickeningRadiance],
		"Wizard": [	Banishment, Polymorph, WallofFire,	AnimateDead, Counterspell, Fireball, HypnoticPattern, MajorImage, Slow, Blink, Fly, LightningBolt, DispelMagic, ArcaneEye, Polymorph, GreaterInvisibility, PhantasmalKiller, Fabricate, ControlWater, IceStorm, GravitySinkhole, SickeningRadiance],
	}

	spells_race = {
		"Aberration": [GreaterInvisibility, DimensionDoor, IceStorm],
		"Aven": [FreedomofMovement, Stoneskin, WallofFire,	AuraLife, Banishment, ArcaneEye, DimensionDoor, Fabricate, LocateCreature],
		"Beast": [ConjureWoodlandBeings, DominateBeast, GraspingVine,	Stoneskin, FreedomOfMovement, DominateBeast, ConjureWoodlandBeings, AuraofPurity, ControlWater, GiantInsect, Polymorph, ConjureMinorElementals],
		"Beastfolk": [ConjureWoodlandBeings, DominateBeast, GraspingVine],
		"Catfolk": [GreaterInvisibility, Polymorph, Stoneskin],
		"Celestial": [DeathWard, GuardianofFaith, Banishment],
		"Dragon": [Fear, Fireball, LightningBolt, ProtectionfromEnergy, Fly, Haste, WallSand, DimensionDoor, ElementalBane, WallofFire, GravitySinkhole],
		"Undead": [AnimateDead, VampiricTouch, LifeTransference, SpeakwithDead, StinkingCloud, HungerHadar, ShadowofMoil, SickeningRadiance],
		"Beastfolk": [Stoneskin, FreedomOfMovement, DominateBeast, ConjureWoodlandBeings, AuraofPurity, ControlWater, GiantInsect, Polymorph, ConjureMinorElementals],
		"Celestial": [BeaconHope, AnimateDead, SpiritGuardians, Daylight, CrusadersMantle, Tongues, LifeTransference, Banishment, GuardianFaith, AuraofPurity, AuraLife],
		"Construct": [Fabricate, Stoneskin, GreaterInvisibility],
		"Dragon": [WallofFire, Polymorph, Stoneskin],
		"Dwarf": [GuardianofFaith, DeathWard, Banishment],
		"Elf": [GreaterInvisibility, DimensionDoor, IceStorm],
		"Elemental": [ConjureMinorElementals, Stoneskin, IceStorm],
		"Fey": [ConjureWoodlandBeings, DominateBeast, GraspingVine,	ConjureAnimals, HypnoticPattern, MajorImage, PlantGrowth, Nondetection, SpeakPlants, FastFriends, Polymorph, DominateBeast, ControlWater, ConjureWoodlandBeings],
		"Fiend": [Blight, PhantasmalKiller, WallofFire],
		"Giant": [Stoneskin, GiantInsect, Polymorph],
		"Goblin": [Blight, PhantasmalKiller, WallofFire,	Fear, MajorImage, BestowCurse, EnemiesAbound, Blink, GaseousForm, StinkingCloud, HypnoticPattern, FastFriends, InciteGreed, HungerHadar, Polymorph, ShadowofMoil, SickeningRadiance],
		"Gnome": [GreaterInvisibility, DimensionDoor, Stoneskin],
		"Halfling": [	FreedomofMovement, ConjureWoodlandBeings, Divination,	FaithfulHound, GreaterInvisibility, FreedomOfMovement, Confusion, SecretChest, LocateCreature, DimensionDoor, HallucinatoryTerrain, AuraLife, AuraofPurity, Fabricate],
		"Human": [GreaterInvisibility, DimensionDoor, Stoneskin],
		"Kobold": [WallofFire, Polymorph, Stoneskin],
		"Lizardfolk": [ConjureWoodlandBeings, DominateBeast, GraspingVine,	Tongues, HungerHadar, Fear, ElementalWeapon, EruptingEarth, MeldIntoStone, StinkingCloud, ProtectionfromEnergy, Fly, GreaterInvisibility, LocateCreature, Polymorph, GiantInsect],
		"Monstrosity": [GreaterInvisibility, DimensionDoor, IceStorm],
		"Ooze": [Blight, Stoneskin, PhantasmalKiller],
		"Orc": [GuardianofFaith, DeathWard, Banishment],
		"Plant": [ConjureWoodlandBeings, DominateBeast, GraspingVine,	AnimateDead, PlantGrowth, Daylight, SpeakPlants, ConjureAnimals, WaterBreathing, GlyphWarding, ConjureWoodlandBeings, DominateBeast, Stoneskin, ControlWater],
		"Snakefolk": [GreaterInvisibility, Polymorph, Stoneskin],
		"Undead": [Blight, PhantasmalKiller, DimensionDoor]

	}

	spells_subrace = {
		"Guardian Kong": [GuardianNature, GraspingVine, Divination, AuraLife, WaterySphere, GravitySinkhole],
		"Vampire": [VampiricTouch, AnimateDead, GaseousForm, Fear, HungerHadar, LifeTransference, ShadowofMoil, SickeningRadiance],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [Polymorph, GreaterInvisibility, FireShield]

	spell = random.choice(spells)

	print(f"Spell Selected: {spell.name}")

	return spell

def fifth(ludus, dif=6):
	#print("Fifth Level Spell:")

	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	# Define background-specific spells
	spells_background = {
		"Explorer": [GreaterRestoration, Commune, Passwall, ContactOtherPlane],
		"Artist": [Seeming, Mislead, Creation, ModifyMemory],
		"Hunter": [SwiftQuiver, CommuneNature, ConjureVolley, TreeStride],
		"Criminal": [Passwall, Mislead, DominatePerson, Seeming, TeleportationCircle, ContactOtherPlane],
		"Cultist": [DispelEvilandGood, InsectPlague, WrathNature, GreaterRestoration, DanseMacabre, InfernalCalling],
		"Bandit": [Mislead, ModifyMemory, Passwall, Seeming, TeleportationCircle, ContactOtherPlane, Dream],
		"Bard": [		MassCureWounds, AnimateObjects, SynapticStatic,	MassCureWounds, RaiseDead, GreaterRestoration, TeleportationCircle, Mislead, ModifyMemory, AnimateObjects, Awaken, Scrying, DominatePerson, Geas, LegendLore, Scrying],
		"Berserker": [DestructiveWave, FlameStrike, Geas, CommuneNature, CircleofPower, Dawn],
		"Druid": [	CommuneWithNature, TreeStride, WallofStone,	DispelEvilandGood, ControlWinds, InsectPlague, TransmuteRock, MassCureWounds, TreeStride, WallStone, WrathNature, GreaterRestoration, CommuneNature, ConjureElemental],
		"Guard": [BanishingSmite, CircleofPower, Dawn, HoldMonster],
		"Soldier": [GreaterRestoration, RaiseDead, DestructiveWave, FlameStrike, PlanarBinding, CircleofPower, Dawn],
		"Noble": [Geas, LegendLore, ModifyMemory, Scrying, TeleportationCircle, Mislead, ContactOtherPlane],
		"Priest": [DispelEvilandGood, SummonCelestial, Scrying, Reincarnate, MassCureWounds, Immolation, HolyWeapon, DispelEvilandGood, LegendLore, Commune, Dawn],
		"Sorcerer": [WallStone, WallLight, WallForce, TransmuteRock, SummonDraconicSpirit, SteelWindStrike, ControlWinds, ConjureElemental, ConeCold, FarStep],
		"Warlock": [AntilifeShell, ContactOtherPlane, Dream, Enervation, FarStep, HoldMonster, Immolation, InfernalCalling, Mislead, NegativeEnergyFlood],
		"Wizard": [	ConeofCold, WallofForce, TeleportationCircle,	AnimateObjects, Awaken, BigbysHand, Commune, ConeCold, ConjureElemental, ContactOtherPlane, Creation, DanseMacabre, Dawn, DominatePerson, Dream, Enervation, FarStep, HoldMonster, LegendLore, Mislead, ModifyMemory, NegativeEnergyFlood, PlanarBinding, Scrying, Seeming, SynapticStatic, Telekinesis, TemporalShunt, WallForce, WallLight],
	}

	# Define race-specific spells
	spells_race = {
		'Aberration': [ConeofCold, TeleportationCircle, WallofForce],
		"Aven": [ControlWinds, DestructiveWave, Cloudkill, CommuneNature, SwiftQuiver, ControlWinds, SteelWindStrike, Creation, Dawn],
		"Beast": [CommuneWithNature, TreeStride, WallofStone, WrathNature, TreeStride, Reincarnate, InsectPlague, DispelEvilandGood, CommuneNature, ConjureElemental, DanseMacabre, DominatePerson, FlameStrike],
		"Beastfolk": [CommuneWithNature, TreeStride, WallofStone, WrathNature, TreeStride, Reincarnate, InsectPlague, DispelEvilandGood, CommuneNature, ConjureElemental, DanseMacabre, DominatePerson, FlameStrike],
		"Catfolk": [DominatePerson, HoldMonster, SynapticStatic],
		"Celestial": [MassCureWounds, RaiseDead, FlameStrike,	BanishingSmite, SummonCelestial, HolyWeapon, Dawn, CommuneNature, GreaterRestoration, CircleofPower, FlameStrike],
		"Construct": [AnimateObjects, WallofForce, TeleportationCircle],
		"Dragon": [		Cloudkill, Immolation, ConeofCold,	ConeCold, Immolation, SummonDraconicSpirit, WallStone, SteelWindStrike, TemporalShunt, Maelstrom],
		"Dwarf": [		FlameStrike, MassCureWounds, RaiseDead],
		"Elemental": [ConjureElemental, Immolation, WallofStone],
		"Elf": [ConeofCold, TeleportationCircle, WallofForce],
		"Fey": [	DominatePerson, Awaken, Reincarnate,	WrathNature, SwiftQuiver, TreeStride, CommuneNature, ConjureVolley, Mislead, Seeming, Dream, Polymorph],
		"Fiend": [DominatePerson, HoldMonster, SynapticStatic],
		"Giant": [ControlWinds, Cloudkill, DestructiveWave],
		"Gnome": [ConeofCold, TeleportationCircle, WallofForce],
		"Goblin": [		DominatePerson, HoldMonster, SynapticStatic,	Mislead, AnimateObjects, DominatePerson, Geas, Seeming, Cloudkill, HoldMonster, NegativeEnergyFlood],
		"Halfling": [	CommuneWithNature, GreaterRestoration, TreeStride,	TreeStride, Awaken, CommuneNature, GreaterRestoration, WallStone, SwiftQuiver],
		"Human": [ConeofCold, TeleportationCircle, WallofForce],
		"Kobold": [Cloudkill, Immolation, ConeofCold],
		"Lizardfolk": [	CommuneWithNature, TreeStride, WallofStone,	WrathNature, TreeStride, SwiftQuiver, SummonDraconicSpirit, HoldMonster, Commune, ControlWinds, InsectPlague, PlanarBinding],
		"Monstrosity": [ConeofCold, TeleportationCircle, WallofForce],
		"Ooze": [Cloudkill, Contagion, DestructiveWave],
		"Orc": [FlameStrike, MassCureWounds, RaiseDead],
		"Plant": [CommuneWithNature, TreeStride, WallofStone,	AnimateObjects, CommuneNature, ConjureElemental, ControlWinds, InsectPlague, PlantGrowth, TreeStride, WrathNature],
		"Snakefolk": [DominatePerson, HoldMonster, SynapticStatic],
		"Undead": [Cloudkill, DanseMacabre, NegativeEnergyFlood,	DanseMacabre, NegativeEnergyFlood, Enervation, HoldMonster, Dream, FarStep, WallLight, Mislead, LegendLore, Scrying],
	}

	# Define subrace-specific spells
	spells_subrace = {
		"Guardian Kong": [WallStone, HoldMonster, CommuneNature, TreeStride, FarStep, AnimateObjects],
		"Vampire": [VampiricTouch, AnimateDead, GaseousForm, Fear, HungerHadar, LifeTransference, ShadowofMoil, SickeningRadiance, NegativeEnergyFlood],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [Scrying, DominatePerson, Cloudkill]

	spell = random.choice(spells)

	print(f"%th level spell {spell.name}")
	return spell

def sixth(ludus, dif=6):
	#print("Sixth Level Spell:")


	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells_background = {
		"Artist": [TrueSeeing, ProgrammedIllusion, MassSuggestion, IrresistibleDance, MentalPrison],
		"Bandit": [TrueSeeing, Contingency, MassSuggestion, Eyebite, Disintegrate],
		"Bard": [		MassSuggestion, HeroesFeast, TrueSeeing,	TrueSeeing, IrresistibleDance, ProgrammedIllusion, MassSuggestion, HeroesFeast, FindthePath, Eyebite, Countercharm, GuardsandWards],
		"Berserker": [HeroesFeast, FindthePath, WindWalk, Harm, BladeBarrier],
		"Criminal": [Scatter, Contingency, ArcaneGate, MentalPrison, CreateUndead, MagicJar],
		"Druid": [	Heal, HeroesFeast, TransportviaPlants,	Sunbeam, TransportviaPlants, InvestitureWind, DruidGrove, WallThorns, WindWalk, ChainLightning, BonesEarth, FindthePath, MoveEarth],
		"Soldier": [Heal, HeroesFeast, FindthePath, Contingency, CreateUndead, Forbiddance, CircleofDeath],
		"Noble": [MassSuggestion, TrueSeeing, GuardsandWards, Contingency, FindthePath, ProgrammedIllusion, IrresistibleDance],
		"Priest": [TrueSeeing, MassSuggestion, Heal, PlanarAlly, HeroesFeast, WordRecall],
		"Sorcerer": [Disintegrate, WallIce, WallThorns, Scatter, GlobeInvulnerability, ArcaneGate, MentalPrison],
		"Explorer": [FindthePath, Scatter, ArcaneGate],
		"Hunter": [ConjureFey, FindthePath, GuardsandWards],
		"Spy": [MassSuggestion, TrueSeeing, Disintegrate],
		"Warlock": [Eyebite, CircleofDeath, Disintegrate, MagicJar, CreateUndead],
		"Wizard": [	ChainLightning, Disintegrate, GlobeofInvulnerability,	GlobeInvulnerability, TrueSeeing, MassSuggestion, Scatter, Disintegrate, MagicJar],
	}

	spells_race = {
		"Aberration": [ChainLightning, Sunbeam, TrueSeeing],
		"Aven": [	WindWalk, Sunbeam, FindthePath,	ChainLightning, Scatter, TrueSeeing],
		"Beast": [	Heal, HeroesFeast, TransportviaPlants,	FindthePath, TrueSeeing, MassSuggestion, InvestitureFlame, Sunbeam],
		"Beastfolk": [	Heal, HeroesFeast, TransportviaPlants,	BonesEarth, TrueSeeing, Disintegrate, WindWalk],
		"Catfolk": [Eyebite, MassSuggestion, IrresistibleDance],
		"Celestial": [	Heal, Harm, WordofRecall,	ArcaneGate, PlanarAlly, Heal],
		"Construct": [ChainLightning, Disintegrate, GlobeofInvulnerability],
		"Dragon": [	Disintegrate, ChainLightning, InvestitureofFlame,	ChainLightning, Disintegrate, GlobeInvulnerability],
		"Dwarf": [Heal, Harm, WordofRecall],
		"Elemental": [InvestitureofFlame, WindWalk, MoveEarth],
		"Elf": [ChainLightning, Sunbeam, TrueSeeing],
		"Fey": [FindthePath, HeroesFeast, TransportviaPlants,	ConjureFey, FindthePath, MassSuggestion, WindWalk, TransportviaPlants],
		"Fiend": [CircleofDeath, MassSuggestion, MentalPrison],
		"Gnome": [ChainLightning, Sunbeam, TrueSeeing],
		"Goblin": [	CircleofDeath, MassSuggestion, MentalPrison,	MassSuggestion, ProgrammedIllusion, TrueSeeing, Eyebite, CircleofDeath, MagicJar, BonesEarth],
		"Giant": [	BonesofEarth, ChainLightning, FleshtoStone,	ChainLightning, InvestitureFlame, GlobeInvulnerability],
		"Halfling": [Heal, HeroesFeast, TransportviaPlants, Scatter, FindthePath, HeroesFeast, GlobeInvulnerability],
		"Human": [ChainLightning, Sunbeam, TrueSeeing],
		"Kobold": [Disintegrate, ChainLightning, InvestitureofFlame],
		"Lizardfolk": [Heal, HeroesFeast, TransportviaPlants,	BonesEarth, WallIce, WallThorns, InvestitureIce, MassSuggestion, Harm, TrueSeeing],
		"Monstrosity": [ChainLightning, Sunbeam, TrueSeeing],
		"Ooze": [Disintegrate, FleshtoStone, IrresistibleDance],
		"Orc": [Heal, Harm, WordofRecall],
		"Plant": [Heal, HeroesFeast, TransportviaPlants],
		"Snakefolk": [CircleofDeath, MassSuggestion, MentalPrison],
		"Undead": [CreateUndead, CircleofDeath, Eyebite, 	CircleofDeath, CreateUndead, MagicJar, TrueSeeing, Eyebite],
	}

	spells_subrace = {
		"Vampire": [CreateUndead, MagicJar, TrueSeeing, Eyebite],
		"Guardian Kong": [TransportviaPlants, GlobeInvulnerability, DruidGrove, WallThorns, BonesEarth],
	}

	spells = []

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [Heal, Disintegrate, TrueSeeing]

	spell = random.choice(spells)

	print(f"6th level spell {spell.name}")

	return spell

def seventh(ludus, dif=6):
	#print("Seventh Level Spell")

	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	spells_background = {
		"Artist": [Simulacrum, ProjectImage, MirageArcane, Symbol, Sequester],
		"Bandit": [Teleport, MirageArcane, ProjectImage, FireStorm, Forcecage],
		"Bard": [		ProjectImage, Teleport, MirageArcane,	Teleport, Resurrection, Regenerate, MirageArcane, Etherealness, Symphony, Forcecage, DreamOfTheBlueVeil, Simulacrum, MordenkainenSword],
		"Berserker": [Regenerate, FireStorm, Resurrection, CrownofStars, FingerDeath],
		"Criminal": [Forcecage, PowerWordPain, Etherealness, Symbol, ReverseGravity],
		"Druid": [	FireStorm, MirageArcane, PlaneShift,	FireStorm, Regenerate, Whirlwind, ConjureCelestial, PlaneShift, MirageArcane],
		"Explorer": [DraconicTransformation, Simulacrum, PlaneShift, TempleOfTheGods],
		"Soldier": [Resurrection, Regenerate, Symbol, Teleport, ConjureCelestial, CrownofStars, DelayedBlastFireball],
		"Noble": [Teleport, MagnificentMansion, Symbol, MirageArcane, Regenerate, Resurrection, Sequester, Simulacrum],
		"Priest": [Resurrection, Etherealness, ConjureCelestial, DivineWord, HeroesFeast, PlaneShift, Symbol],
		"Sorcerer": [Whirlwind, Teleport, ReverseGravity, PrismaticSpray, Forcecage, FireStorm, DelayedBlastFireball, Simulacrum, FingerDeath],
		"Warlock": [PowerWordPain, FingerDeath, Symbol, DelayedBlastFireball, Forcecage],
		"Wizard": [	FingerofDeath, Teleport, PlaneShift,	Simulacrum, TrueSeeing, MassSuggestion, Scatter, Disintegrate, MagicJar, FireStorm, DelayedBlastFireball, MirageArcane, ProjectImage],
	}

	spells_race = {
		"Aberration": [Teleport, FireStorm, PrismaticSpray],
		"Aven": [	Etherealness, PlaneShift, Whirlwind,	ConjureCelestial, PlaneShift, CrownofStars, DivineWord],
		"Beast": [	FireStorm, MirageArcane, PlaneShift,	CrownofStars, Whirlwind, FireStorm, DraconicTransformation, ConjureCelestial],
		"Beastfolk": [	FireStorm, MirageArcane, PlaneShift,	Whirlwind, FireStorm, Simulacrum, PlaneShift],
		"Celestial": [	Resurrection, DivineWord, Regenerate,	ConjureCelestial, DivineWord, Resurrection, HeroesFeast, Etherealness],
		"Construct": [Forcecage, Teleport, ProjectImage],
		"Catfolk": [Etherealness, Regenerate, Resurrection],
		"Dragon": [DelayedBlastFireball, PrismaticSpray, FireStorm,	Teleport, DraconicTransformation, Forcecage, FireStorm, DelayedBlastFireball],
		"Dwarf": [DivineWord, FireStorm, Regenerate],
		"Elemental": [Whirlwind, PlaneShift, ConjureCelestial],
		"Elf": [Teleport, FireStorm, PrismaticSpray],
		"Fey": [	Regenerate, Resurrection, MirageArcane,	ConjureFey, PlaneShift, MassSuggestion, WindWalk, TransportviaPlants],
		"Giant": [	Etherealness, PlaneShift, Whirlwind,	CrownofStars, Whirlwind, Simulacrum, PlaneShift, Forcecage],
		"Goblin": [	FingerofDeath, ReverseGravity, CrownofStars,	MirageArcane, ProjectImage, PrismaticSpray, Simulacrum, Etherealness, Teleport, Symbol],
		"Halfling": [	PlaneShift, MirageArcane, Regenerate,	MagnificentMansion, MirageArcane, FireStorm, Etherealness],
		"Human": [Teleport, FireStorm, PrismaticSpray],
		"Kobold": [DelayedBlastFireball, PrismaticSpray, FireStorm],
		"Lizardfolk": [FireStorm, MirageArcane, PlaneShift,	Forcecage, ReverseGravity, FireStorm, CrownofStars],
		"Monstrosity": [Teleport, FireStorm, PrismaticSpray],
		"Ooze": [PrismaticSpray, ReverseGravity, Etherealness],
		"Orc": [DivineWord, FireStorm, Regenerate],
		"Plant": [FireStorm, MirageArcane, PlaneShift],
		"Snakefolk": [	Etherealness, Regenerate, Resurrection,	PowerWordPain, FingerDeath, DelayedBlastFireball, Forcecage],
		"Undead": [	FingerofDeath, Etherealness, PlaneShift,	CreateUndead, MagicJar, TrueSeeing, FingerDeath, Resurrection],
	}

	spells_subrace = {
		"Vampire": [CreateUndead, MagicJar, TrueSeeing, FingerDeath],
		"Guardian Kong": [CrownofStars, Simulacrum, MirageArcane, ReverseGravity],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [Teleport, FireStorm, Resurrection]

	spell = random.choice(spells)

	print(f"Seventh level Spell: {spell.name}")

	return spell

def eighth(ludus, dif=6):
	#print("Eighth Level Spell")


	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	spells_background = {
		"Artist": [		PowerWordStun, Glibness, RealityBreak],
		"Bandit": [		AntimagicField, MindBlank, Demiplane, Feeblemind, Maze],
		"Bard": [		Glibness, PowerWordStun, MindBlank,	PowerWordStun, MindBlank, Maze, Glibness, DominateMonster, AntimagicField, Foresight, Feeblemind, Demiplane, RealityBreak],
		"Berserker": [	Earthquake, ControlWeather, AnimalShapes, MaddeningDarkness, HolyAura],
		"Criminal": [	PowerWordStun, MightyFortress, Feeblemind, AntipathySympathy, AntimagicField, Clone, Telepathy],
		"Druid": [		AnimalShapes, ControlWeather, Earthquake,	Sunburst, ControlWeather, Tsunami, AnimalShapes, Earthquake, RealityBreak],
		"Explorer": [	Demiplane, Foresight, Telepathy, AntipathySympathy],
		"Soldier": [	HolyAura, AntimagicField, Glibness, Earthquake, DominateMonster, Feeblemind, RealityBreak],
		"Noble": [		MindBlank, AntipathySympathy, Demiplane, Maze, DominateMonster, Telepathy, HolyAura],
		"Priest": [		HolyAura, AntimagicField, Glibness, MindBlank, DominateMonster, RealityBreak],
		"Sorcerer": [	Tsunami, IncendiaryCloud, IllusoryDragon, Earthquake, ControlWeather, MaddeningDarkness, Sunburst, DarkStar, RealityBreak],
		"Wizard": [		MindBlank, PowerWordStun, Sunburst,	],
	}

	spells_race = {
		"Aberration": [MindBlank, IncendiaryCloud, Sunburst],
		"Aven": [Earthquake, Sunburst, ControlWeather,	ControlWeather, DarkStar, RealityBreak, Telepathy],
		"Beast": [	AnimalShapes, Earthquake, Sunburst,	AnimalShapes, Earthquake, Feeblemind, ControlWeather, Foresight],
		"Beastfolk": [	AnimalShapes, Earthquake, Sunburst,	AnimalShapes, MaddeningDarkness, HolyAura, RealityBreak],
		"Catfolk": [MindBlank, DominateMonster, Feeblemind],
		"Celestial": [	HolyAura, Sunburst, Earthquake,	AntimagicField, HolyAura, MindBlank, Glibness],
		"Construct": [Clone, AntimagicField, PowerWordStun],
		"Dragon": [	IncendiaryCloud, Earthquake, PowerWordStun,	IncendiaryCloud, MaddeningDarkness, RealityBreak],
		"Dwarf": [Earthquake, Sunburst, HolyAura],
		"Elemental": [Tsunami, Earthquake, ControlWeather],
		"Elf": [MindBlank, IncendiaryCloud, Sunburst],
		"Fey": [	ControlWeather, Earthquake, Sunburst,	AntipathySympathy, Demiplane, ControlWeather, Telepathy, RealityBreak],
		"Fiend": [DominateMonster, MaddeningDarkness, Feeblemind],
		"Giant": [Earthquake, Sunburst, MightyFortress],
		"Gnome": [MindBlank, IncendiaryCloud, Sunburst],
		"Goblin": [	DominateMonster, MaddeningDarkness, Feeblemind,	Maze, DominateMonster, PowerWordStun, AntipathySympathy, Demiplane, Feeblemind, IncendiaryCloud, RealityBreak],
		"Halfling": [AnimalShapes, Earthquake, Sunburst,	AntipathySympathy, Telepathy, Demiplane, Clone, RealityBreak],
		"Human": [MindBlank, IncendiaryCloud, Sunburst],
		"Kobold": [IncendiaryCloud, Earthquake, PowerWordStun],
		"Lizardfolk": [	AnimalShapes, Earthquake, Sunburst,	AnimalShapes, MaddeningDarkness, Earthquake, Tsunami, RealityBreak],
		"Monstrosity": [MindBlank, IncendiaryCloud, Sunburst],
		"Ooze": [AntimagicField, Feeblemind, Earthquake],
		"Orc": [Earthquake, Sunburst, HolyAura],
		"Plant": [AnimalShapes, Earthquake, Sunburst],
		"Snakefolk": [MindBlank, DominateMonster, Feeblemind],
		"Undead": [Clone, AntimagicField, ControlWeather,	Clone, PowerWordStun, Feeblemind, Demiplane, RealityBreak],
	}

	spells_subrace = {
		"Vampire": [Clone, PowerWordStun, Feeblemind, MaddeningDarkness, RealityBreak],
		"Guardian Kong": [DominateMonster, Earthquake, RealityBreak],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [DominateMonster, Feeblemind, Demiplane]

	spell = random.choice(spells)

	print(f"8th level spell {spell.name}")

	return spell

def ninth(ludus, dif=6):
	#print("Ninth Level Spell:")

	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	spells_background = {
		"Druid": [Shapechange, StormofVengeance, TrueResurrection,	TrueResurrection, MassPolymorph, Shapechange, Invulnerability, StormofVengeance],
		"Explorer": [TruePolymorph, TimeStop, RavenousVoid, Gate],
		"Hunter": [PowerWordKill, Shapechange, Invulnerability],
		"Criminal": [TimeStop, PowerWordKill, Invulnerability, PsychicScream, Wish],
		"Bandit": [TimeStop, Foresight, Imprisonment, Weird, Gate],
		"Bard": [		TruePolymorph, Foresight, Wish,	PowerWordKill, TruePolymorph, TimeStop, PsychicScream, PrismaticWall, MassPolymorph, Foresight, MeteorSwarm, Wish, Shapechange],
		"Berserker": [StormofVengeance, TrueResurrection, Shapechange, Invulnerability, MassHeal],
		"Soldier": [MassHeal, TrueResurrection, PowerWordKill, AstralProjection, Gate, PrismaticWall],
		"Noble": [Foresight, Imprisonment, PowerWordKill, TruePolymorph, Wish, PsychicScream],
		"Priest": [TrueResurrection, PowerWordHeal, HolyAura, MassHeal],
		"Sorcerer": [Wish, TimeStop, StormofVengeance, PrismaticWall, MeteorSwarm, Invulnerability, PsychicScream, RavenousVoid],
		"Wizard": [MeteorSwarm, PowerWordKill, TimeStop, Wish]
		}

	spells_race = {
	"Aberration": [TimeStop, Foresight, MeteorSwarm],
	"Aven": [StormofVengeance, Foresight, PowerWordKill,	StormofVengeance, Gate, Foresight, RavenousVoid],
	"Beast": [Invulnerability, MassPolymorph, Shapechange,	Shapechange, StormofVengeance, TrueResurrection],
	"Beastfolk": [TrueResurrection, Shapechange, StormofVengeance,	Shapechange, StormofVengeance, TrueResurrection],
	"Catfolk": [Shapechange, MassHeal, PsychicScream],
	"Celestial": [TrueResurrection, HolyAura, Invulnerability,	MassHeal, TrueResurrection, StormofVengeance],
	"Construct": [PowerWordKill, PrismaticWall, Wish],
	"Dragon": [Weird, TruePolymorph, MeteorSwarm,	MeteorSwarm, PowerWordKill, Shapechange],
	"Dwarf": [MassHeal, TrueResurrection, StormofVengeance],
	"Elemental": [Tsunami, Foresight, StormofVengeance],
	"Elf": [TimeStop, Foresight, MeteorSwarm],
	"Fey": [Wish, TimeStop, RavenousVoid,	TruePolymorph, Foresight, StormofVengeance],
	"Fiend": [PowerWordKill, PsychicScream, Wish],
	"Giant": [MeteorSwarm, PowerWordKill, Shapechange],
	"Gnome": [TimeStop, Foresight, MeteorSwarm],
	"Goblin": [PowerWordKill, Weird, TruePolymorph, TimeStop, Foresight, MeteorSwarm, PsychicScream, Wish,	PowerWordKill, PsychicScream, Wish],
	"Halfling": [Wish, TimeStop, Gate, PsychicScream,	Shapechange, TrueResurrection, StormofVengeance],
	"Human": [TimeStop, Foresight, MeteorSwarm],
	"Kobold": [MeteorSwarm, PowerWordKill, Shapechange],
	"Lizardfolk": [PowerWordKill, PowerWordHeal, Invulnerability, TruePolymorph,	Shapechange, StormofVengeance, TrueResurrection],
	"Monstrosity": [TimeStop, Foresight, MeteorSwarm],
	"Ooze": [Imprisonment, Shapechange, PowerWordKill],
	"Orc": [MassHeal, TrueResurrection, StormofVengeance],
	"Plant": [Shapechange, StormofVengeance, TrueResurrection],
	"Snakefolk": [PowerWordKill, Shapechange, Invulnerability,	Shapechange, MassHeal, PsychicScream],
	"Undead": [PowerWordKill, PsychicScream, Imprisonment, RavenousVoid,	AstralProjection, Foresight, MassPolymorph],
	}

	spells_subrace = {
		"Vampire": [AstralProjection, Invulnerability, TruePolymorph],
		"Guardian Kong": [AstralProjection, Invulnerability, TimeStop, Foresight],
	}

	# Fetch from the possible spells for the selected race and background
	spells += list(set(spells_race.get(ludus.race, []) +
					   spells_subrace.get(ludus.subrace, []) +
					   spells_background.get(ludus.background, [])))

	# Ensure there are spells to choose from
	if not spells:
		spells = [PowerWordKill, TruePolymorph, Wish]

	spell = random.choice(spells)

	print(f"9th level spell {spell.name}")

	return spell













###     Notes     ###
# Calculate the probability of learning the spell
# Two Points Slope
# (SpellLvl,Chance)
# (0,p0) & (max+1,0)
# ch = y1 + (x-x1) * (y2-y1):(x2-x1)
# ch = p0 + (Lvl) * (-p0):(max+1) = p0 + (1 - Lvl):(max+1)
#p0 = 1 - (0.95/max_spell_level)
#probability = p0 * ( 1 - spell_level / (1 + max_spell_level))
# Randomly select if the spell is not already in the list
#if random.random() < probability:




def add_spell(spell_list, spell_name, spell_definition=""):
	if  spell_name not in spell_list:
		spell_list += f"\n- {spell_name}"
		if spell_definition:
			spell_list += f": {spell_definition}"
	return spell_list

class Spellbook:
	def __init__(self,ludus):

		self.character_level = ludus.level
		self.cantrip = ""
		self.spells = {level: "" for level in range(1, 10)}

		self.cantrip_set = set()

		self.difficulty = 10

		self.slots = {level: 0 for level in range(1, 10)}

		# Natural Spellcasting. Doesn't need spell slots.
		self.one     = ""
		self.two     = ""
		self.three   = ""
		self.one_day_each_list = []
		self.two_day_each_list = []
		self.three_day_each_list = []
		self.num1d = 3
		self.num2d = 3
		self.num3d = 3

		self.recharge = []
		self.recharge_list = []

		self.accessible = {level: [] for level in range(1, 10)}
		self.selected = {level: [] for level in range(1, 10)}

	def slots_at(self, spell_level):
		character_level = self.character_level
		difficulty = self.difficulty
		pb = PB(character_level)
		# Calculate the maximum spell level
		max_level = get_max_spell_level(character_level, difficulty)
		# If max_level is 0, then no slots should be available
		if max_level == 0:
			return None
		# For levels beyond the maximum level, there should be no slots
		if spell_level > max_level:
			return None
		# For the maximum level, there should be exactly 1 slot
		if spell_level == max_level:
			return 1
		# Calculate slots for levels below the maximum
		# Start with a higher number of slots at level 1, gradually decreasing to 1 slot at max_level
		# The function should start at pb / difficulty at level 0 and approach 1 at max_level
		max_slots_at_level_one = pb / difficulty
		slope = (1 - max_slots_at_level_one) / (max_level - 1)
		slots = max_slots_at_level_one + slope * (spell_level - 1)
		# Adjust the number of slots
		slots = max(1, round(slots))  # Ensure at least 1 slot
		return slots if slots >= 1 else None  # Return None if slots fall below 1


	def select_spells(self,spellcaster = False):
		selected_spells_set = set()  # Keep track of all selected spells
		self.UpdateSlots()
		power_level = self.max_spell_level
		if spellcaster:
			for level in range(1, 10):
				num_slots = self.slots[level] if self.slots[level] is not None else 0
				num_spells =  Dice( num_slots) + max(self.number_spell(level), 0)  # Ensure non-negative
				# Update accessible spells for each level
				accessible_spells = set(self.accessible[level]) - selected_spells_set  # Remove already selected spells
				accessible_spells = list(accessible_spells)
				if accessible_spells and num_spells > 0:  # Check for non-empty list and positive num_spells
					num_to_select = min(num_spells, len(accessible_spells))
					selected_spells = random.sample(accessible_spells, num_to_select)
					self.selected[level] = selected_spells
					selected_spells_set.update(selected_spells)  # Add new selections to the set of selected spells
				else:
					self.selected[level] = []  # Handle empty or non-applicable cases
		else:
			# Update for one, two, three times per day lists
			for spell_list, num in [(self.one_day_each_list, self.num1d),
									(self.two_day_each_list, self.num2d),
									(self.three_day_each_list, self.num3d)]:
				available_spells = list(set(spell_list) - selected_spells_set)
				# Remove already selected spells
				num = min(num, len(available_spells))
				# Ensure we don't exceed the number of available spells
				if num > 0:
					selected_spells = random.sample(available_spells, num)
					spell_list[:] = selected_spells
					# Update the list in place
					selected_spells_set.update(selected_spells)
					# Add to the set of selected spells
				else:
					spell_list[:] = []  # Clear the list if no spells are to be selected

	def number_spell(self,spell_level):
		if spell_level == 0:
			return min(5, max(0, self.max_spell_level))
		d = self.difficulty
		l = spell_level
		pb = PB(self.character_level)
		num = (2*pb-d-l)//d
		return num

	def number_daily_spells(self, times_day):
		num   = 6-times_day
		return num

	def add_random_spells(self):
		for level, spells in self.accessible.items():
			num_spells = self.number_spell(level)
			if spells:
				selected_spells = random.sample(spells, min(num_spells, len(spells)))
				for spell in selected_spells:
					self.add_spell(level, spell)
	@property
	def first(self):
		return self.spells[1]

	@property
	def second(self):
		return self.spells[2]

	@property
	def third(self):
		return self.spells[3]

	@property
	def fourth(self):
		return self.spells[4]

	@property
	def fifth(self):
		return self.spells[5]

	@property
	def sixth(self):
		return self.spells[6]

	@property
	def seventh(self):
		return self.spells[7]

	@property
	def eighth(self):
		return self.spells[8]

	@property
	def ninth(self):
		return self.spells[9]

	@property
	def max_spell_level(self):
		difficulty = self.difficulty
		character_level = self.character_level
		if difficulty < 1: difficulty = 1
		if difficulty > 10: difficulty = 10
		self.difficulty = difficulty
		level = (character_level - difficulty) // (2 * difficulty)
		if level < 0: return 0
		if level > 9: return 9
		return level

	def UpdateDifficulty(self,D):
		if D < 1: D = 1
		if D > 10: D = 10
		self.difficulty = D
		self.UpdateSlots()

	def slots_calculator(self, spell_level):
		import math
		max_spell_level = self.max_spell_level
		k = -math.log(1 / max_spell_level) / max_spell_level
		slots = max_spell_level * math.exp(-k * spell_level)
		slots = math.ceil(slots)
		return max(1, int(slots))

	def UpdateSlots(self):
		'''
		max_spell_level = self.max_spell_level
		for level in range(1, 10):
			# Example slot allocation: Decrease slots as the level approaches max_spell_level
			self.slots[level] = self.slots_at(level) if level <= max_spell_level else 1
		'''
		# Base spell slot progression factor
		l = self.character_level
		d = self.difficulty
		m = self.max_spell_level
		# Update the number of slots for each spell level
		for level in range(1, 10):
			if level <= 3:
				slots = min(5,m -(level - d) // d)
			else:
				slots = min(4,m -(level - d) // d)
			self.slots[level] = slots
		# Set slots to 0 for levels beyond the maximum spell level
		for level in range(1, 10):
			if self.slots[level] <= 0:
				self.slots[level] = None


	def add_spell(self, spell_level, spell_name, spell_definition=""):
		# Using a set to track added spells
		if spell_level == 0:
			if spell_name not in self.cantrip_set:
				self.cantrip += f"\n\t<b>{spell_name}</b>"
				if spell_definition:
					self.cantrip += f": <i>{spell_definition}</i>"
				self.cantrip_set.add(spell_name)
		elif 1 <= spell_level <= 9:
			spell_list = self.spells.get(spell_level, "")
			if spell_name not in spell_list:
				spell_list += f"\n\t<b>{spell_name}</b>"
				if spell_definition:
					spell_list += f": <i class=" + '"bc4"' + f">{spell_definition}</i>"
				self.spells[spell_level] = spell_list

	def add_natural(self, spell, definition="", times_day = 1):
		result = f"\n\t <b>{spell}:</b> <i class=" + '"bc4"' + f">{times_day} per day. </i> <i>{definition}</i>"
		if times_day == 1:
			self.one += result
		elif times_day == 2:
			self.two += result
		elif times_day == 3:
			self.three += result

	def add_rechargeable(self, spell, definition="", recharge_at=6):
		if spell:  # Ensure the spell name is not empty
			#roll = f"{recharge_at}-6" if recharge_at < 6 else "6"
			recharge_entry = f"\n\t{spell}\n" # + \t- Recharges at {roll} in a d6. {definition}"
			self.recharge.append(recharge_entry)

	def SpellbookString(self,ludus):
		result = "\n"
		if is_ritualcaster(ludus):
			result += f"{ludus.title} is a ritual spellcaster. \n"
		if self.cantrip:
			result += f"<h4>Cantrips (at will):</h4> {self.cantrip}"
		if is_spellcaster(ludus):
			for level in range(1, 10):
				slots = self.slots[level]
				if slots is not None:  # Check if slots is not None
					if self.spells[level]:
						ordinal = "th" if 4 <= level <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(level % 10, "th")
						result += f"<h4>[{slots}] {level}{ordinal} Level Spells:</h4>" + self.spells[level]
						result += "\n"
		else:
			# Include natural spells
			if self.one.strip():
				result += f"<h4>Natural Spells (1/day): </h4> {self.one}"
			if self.two.strip():
				result += f"<h4>Natural Spells (2/day): </h4> {self.two}"
			if self.three.strip():
				result += f"<h4>Natural Spells (3/day): </h4> {self.three}"
			# Include rechargeable spells
			if self.recharge:
				result += "\n<h4>Rechargeable Spells:</h4>"
				for spell_entry in self.recharge:
					if spell_entry.strip():  # Ensure the entry is not empty
						result += spell_entry
		return result.strip()












#Spell(name, level, school, casting_time, ranges, duration, components):

	# Criminal







# = Spell("")













def rechargable(ludus,dif=6):
	race = ludus.race
	background = ludus.background
	lvl = ludus.level
	creature_type = ludus.race + ' ' + ludus.subrace + ' ' + ludus.background

	spells = []

	Leadership = Entry_Text(
		"Leadership",
		f"{ludus.title} can utter a special command or warning whenever another creature that it can see within 30 feet of it makes an attack roll or a saving throw. The creature can add a d4 to its roll provided it can hear and understand {ludus.title}. A creature can benefit from only one Leadership die at a time. This effect ends if {ludus.title} is incapacitated.",
		"Reaction.\n (Recharges after a Short or Long Rest) \n- V.")

	ColdBreath = Entry_Text(
		"Cold Breath",
		f"{ludus.title}  exhales a blast of freezing wind in a 15-foot cone. Each creature in that area must make a DC{ludus.dc} Dexterity saving throw, taking {4*ludus.pb//2} ({ludus.pb//2}d8) cold damage on a failed save, or half as much damage on a successful one.",
		f"Recharge 5–6")


	Web = Entry_Text(
	   "Web",
	   """You conjure a mass of thick, sticky webbing at a point of your choice within range. The webs fill a 20-foot cube from that point for the duration. The webs are difficult terrain and lightly obscure their area.
If the webs aren’t anchored between two solid masses (such as walls or trees) or layered across a floor, wall, or ceiling, the conjured web collapses on itself, and the spell ends at the start of your next turn. Webs layered over a flat surface have a depth of 5 feet.
Each creature that starts its turn in the webs or that enters them during its turn must make a Dexterity saving throw. On a failed save, the creature is restrained as long as it remains in the webs or until it breaks free.
A creature restrained by the webs can use its action to make a Strength check against your spell save DC. If it succeeds, it is no longer restrained.
The webs are flammable. Any 5-foot cube of webs exposed to fire burns away in 1 round, dealing 2d4 fire damage to any creature that starts its turn in the fire.""",
	   "(Recharge 6)")

	spells_background = {
		"Hunter":   [Web],
		"Criminal": [Web],
		"Bandit":   [Leadership],
		"Charlatan":[Leadership],
		"Cultist":  [Leadership],
		"Guard":    [Leadership],
		"Hero":     [Leadership],
		"Noble":    [Leadership],
		"Soldier":  [Leadership],

	}
	spells_race = {
		"Celestial":    [Leadership],
		"Dragon":       [ColdBreath],
		"Undead":       [],
		"Beast":        [ColdBreath],
		"Beastfolk":    [],
		"Celestial" :   [],
		"Elemental":    [ColdBreath],
		"Fey":          [],
		"Dwarf":        [Leadership],
		"Goblin":       [Leadership],
		"Orc":          [Leadership],

	}

	spells_subrace = {
		"Beholder":         [Leadership],
		"Mindlinker":       [Leadership],
		"Depth Dominators":  [Leadership],
		"Golden Lion":      [Leadership],
		"Celestial Stag":   [Leadership],
		"Spider Queen":     [Web,           Leadership],
		"Leonid":           [Leadership],
		"Werebear":         [Leadership],
		"Throne":           [Leadership],
		"Valkyrie":         [Leadership],
		"Archangel":        [Leadership],
		"Genie":            [Leadership],
		"Titan":            [Leadership],
		"Devil":            [Leadership],
		"Fallen Angel":     [Leadership],
		"Infernal Warlord": [Leadership],
		"Archfey":          [Leadership],
		"Hobgoblin":        [Leadership],
		"Vampire":          [],
		"Pride Mummy":      [Leadership],
		"High Elf":         [Leadership],
		"Conquistador":     [Leadership],

	}
	# Fetch from the possible spells for the selected race and background
	spells += list(set( spells_race.get(ludus.race, []) +
						spells_subrace.get(ludus.subrace, []) +
						spells_background.get(ludus.background, [])))

	number_of_spells = min(len(spells),
						   max(1,
							   6-Dice(dif)
							   )
						   )

	# Randomly select spells if there are any to choose from
	selected_spells = random.sample(spells, number_of_spells) if spells else []

	# Formatting the output
	return '<i>' + '\n'.join(spell for spell in selected_spells) + '</i>' if selected_spells else ""


def legacynatural(ludus,dif=6):
	ludus_type = f"{ludus.race} {ludus.subrace} {ludus.background}"
	Affinity = 10 - dif




	# Fetch from the possible spells for the selected race and background
	spells = list(set( spells_race.get(ludus.race, []) +
						spells_subrace.get(ludus.subrace, []) +
						spells_background.get(ludus.background, [])))

	number_of_spells = min(len(spells),
						   max(1,
							   6-Dice(dif)
							   )
						   )

	one = random.sample(spells, number_of_spells) if spells else []

	spells = [spell for spell in spells if spell not in one]
	number_of_spells = min(len(spells),
						   max(1,
							   5-Dice(dif)
							   )
						   )
	two = random.sample(spells, number_of_spells) if spells else []

	spells = [spell for spell in spells if spell not in one]
	number_of_spells = min(len(spells),
						   max(1,
							   5-Dice(dif)
							   )
						   )

	three = random.sample(spells, number_of_spells) if spells else []

	one =   '\n'.join(spell for spell in one)   if one   else ""
	two =   '\n'.join(spell for spell in two)   if two   else ""
	three = '\n'.join(spell for spell in three) if three else ""

	spells_string = f""
	if one:     spells_string += f"One use a day: {one} \n"
	if two:     spells_string += f"Two uses a day: {two} \n"
	if three:   spells_string += f"Three uses a day: {three} \n"

	return spells_string
