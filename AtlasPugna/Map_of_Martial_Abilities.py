
try:
	from AtlasLudus.Map_of_Useful_Functions import select1
	from AtlasLudus.Map_of_Dice import Dice, Dizero, SelectDx
	from AtlasActorLudi.Map_of_Scores import PB
	from AtlasScriptum.Map_of_Formats import Entry_Text
except ModuleNotFoundError:
	raise

import random

def Skills(npc):
	"""
	Generate a string of skills for an NPC based on their race, subrace, background, and level.

	Parameters:
	npc (object): An object representing the NPC with attributes like race, subrace, background, and level.
		defined in npc_class.py

	Returns:
	str: A formatted string of selected skills.
	"""
	# Select one protection randomly
	selected = set()
	number = PB(Dice(npc.pb))
	for _ in range(number):
		skill = Skill(npc)
		selected.add(skill)
	# Convert set to string for printing
	skills_string = '\n'.join(selected)
	return skills_string

def Skill(npc):
	'''
	Returns a martial skill [string]
	'''
	race = npc.race
	gender = npc.gender
	subrace = npc.subrace
	background = npc.background
	gender = npc.gender
	lvl = npc.level
	pb = npc.pb
	title = npc.title
	dc = npc.spell_save_dc
	STR = npc.AS.str_mod
	DEX = npc.AS.dex_mod
	CON = npc.AS.con_mod
	INT = npc.AS.int_mod
	WIS = npc.AS.wis_mod
	CHA = npc.AS.cha_mod
	speed = npc.speed
	MIGHT = max(STR,DEX,CON)
	MAGIC = max(INT,WIS,CHA)
	MIGHT_DC = 8 + MIGHT + pb
	MAGIC_DC = 8 + MAGIC + pb


	skills = []

	# Definitions of extra martial skills
	Siege = Entry_Text("Siege",
		f"{title} deals double damage to objects and structures."
		)
	WoundedFury = Entry_Text(
		f"Wounded Fury",
		f"While {title} has {npc.HP//2} hit points or fewer, {title} has advantage on attack rolls. In addition, {title} deals an extra {int(PB(pb)*3.5)} ({PB(pb)}d6) damage to any target {title} hits with a melee attack.")
	PackTactics = Entry_Text(
		f"Pack Tactics",
		f"{title} has advantage on an attack roll against a creature if at least one of {title}'s allies is within 5 feet of the creature and the ally isn't incapacitated.")
	Pounce = Entry_Text(
		f"Pounce",
		f"If {title} moves at least {Dice(2)*Dice(2)*5} feet straight toward a creature and then hits the target with an attack on the same turn, that target must succeed on a DC {8 + pb + STR} Strength saving throw or be knocked prone. If the target is prone, {title} can make one attack against the target as a bonus action."
		)
	Charge =  Entry_Text( f"Charge",
			(	f"If {title} moves at least" + \
				f"{round(int(speed) // 10) * 5} feet straight toward a target and then hits the target with an attack on the same turn," + \
				f"the target takes an extra {PB(pb)}" + \
				SelectDx(pb=pb) + \
				f"+{STR}"  + \
				random.choice(['bludgeoning','slashing','piercing'])  + \
				f" damage. If the target is a creature, they must succeed on a " + \
				f"DC {MIGHT_DC} Strength saving throw or" + \
				select1([
					'be knocked prone',
					'be pushed up to 10 feet away',
					'be pushed up to 10 feet away and be knocked prone',
					f"be knocked prone. If the target is prone, {title} can make one simple attack against the target as a bonus action."
					], [pb, pb, pb//3, pb//4]
					)
				)
			)
	Grappler = Entry_Text( "Grappler",
			f"On a hit on a melee attack, {title} can choose to do no damage to grapple a creature up to its size. The target is then grappled, with DC {8 + npc.pb + npc.AS.str_mod} to scape the grapple.\n" + \
			random.choice([
				Entry_Text("Constrict",
					f"Until the grapple ends, the creature is restrained. {title} can't constrict another creature."),
				Entry_Text("Smother",
					f"Until this grapple ends, the target is restrained, blinded, and at risk of suffocating, and {title} can't smother another target. In addition, at the start of each of the target's turns, the target takes {PB(pb) * 3 + STR} ({PB(pb)}d6 + {STR}) bludgeoning damage."),
			]))
	blinding_spittle = Entry_Text(
		f"Blinding Spittle",
		f"(Recharge 5–6). {title} spits a chemical glob at a point {title} can see within 15 feet of it. The glob explodes in a blinding flash of light on impact. Each creature within 5 feet of the flash must succeed on a DC {dc} Dexterity saving throw or be blinded until the end of {title}'s next turn.")
	body_thief = Entry_Text(
		f"Body Thief" ,
		f"{title} initiates an Intelligence contest with an incapacitated humanoid within 5 feet, that isn't protected by <i class= 'bc4'>Protection from Evil and Good</i>." + \
		f"If {title} wins the contest, the {race}'s magically takes control of the target's body. " +\
		f"{title} retains its Intelligence, Wisdom, and Charisma scores, as well as understanding of any language, senses, and traits." +\
		f"{title} otherwise adopts the target's statistics. {title} knows everything the creature knew, including spells and languages." +\
		f"\n\t If the host body dies, the {race} must leave it. A protection from evil and good spell cast on the body drives {title} out. " +\
		f"{title} is also forced out if the target regains control by means of a wish. " +\
		f"By spending 5 feet of its movement, {title} can voluntarily leave the body within 5 feet of it.")
	devour_intellect = Entry_Text(
		f"Devour Intellect",
		f"{title} targets one creature {gender} can see within 10 feet that has a brain. "+
		f"The target must succeed on a DC {dc} Intelligence saving throw against this magic or take {5*pb//2} ({pb//2}{SelectDx(pb=pb)}) psychic damage. " +
		f"Also on a failure, roll 3d6: If the total equals or exceeds the target's Intelligence score, that score is reduced to {1}. " +
		"The target is stunned until it regains at least one point of Intelligence.")
	Rampage = Entry_Text(
		f"Rampage",
		f"When {title} reduces a creature to 0 hit points with a melee attack on its turn, {title} can take a bonus action to move up to half its speed and make a simple attack.")
	invisible_passage = Entry_Text(
		f"Invisible Passage",
		f"{title} magically turns invisible until they attack or cast a spell, or until their concentration ends (as if concentrating on a spell)." +\
		 "While invisible, they leave no physical evidence of their passage, so they can be tracked only by magic. Any equipment they wear or carry is invisible with them.")
	gibbering = Entry_Text("Gibbering",
				f"{title} babbles incoherently while it can see any creature and isn't incapacitated. " +\
				f"Each creature that starts its turn within 20 feet of {title} and can hear the gibbering must succeed on a DC {8+PB(lvl)+CON} Wisdom saving throw. " +\
				"On a failure, the creature can't take reactions until the start of its next turn and rolls a d8 to determine what it does during its turn. " +\
				"On a 1 to 4, the creature does nothing. " +\
				"On a 5 or 6, the creature takes no action or bonus action and uses all its movement to move in a randomly determined direction. " +\
				"On a 7 or 8, the creature makes a melee attack against a randomly determined creature within its reach or does nothing if it can't make such an attack.")
	tentacles= Entry_Text("Tentacles",
				f"Melee Weapon Attack. Reach 10 ft., one creature. Hit: {5 + STR} (1d10 + {STR}) piercing damage, and the target must succeed on a " +\
			   f"DC {8+PB(lvl)+STR} Constitution saving throw or be poisoned for 1 minute. The poisoned target is paralyzed, and it can repeat the saving throw at the" +\
			   f" start of each of its turns, ending the effect on a success. \n\t The target is also grappled (escape DC {8+PB(lvl)+STR}). If the target is Medium or " +\
			   f"smaller, it is also restrained until this grapple ends. While grappling the target, {title} has advantage on attack rolls against it and can 't "+\
			   f"use this attack against other targets. When {title} moves, any Medium or smaller target it is grappling moves with it.")
	# Multiattack
	multiattack = Entry_Text("Multiattack" , (
			f"{title} makes " + \
			select1(
					[
						"two simple attacks.",
						"two different simple attacks.",
						"two simple melee attacks.",
						"one special attack and a simple attacks. Alternatively, it can do two simple attacks.",
						"one special attacks and one spellcastings, or two special attacks.",
						"one special attack or spellcasting, and then two simple attacks.",
						"two special melee attacks or two simple attacks.",
						"three simple attacks.",
						"two special melee attacks or three simple attacks.",
						"three simple melee attacks or two ranged attacks.",
						"an extraordinary Rapid Shot, making three ranged attacks, each with a -2 penalty to the attack roll.",
						"one simple attack against each enemy within reach.",
						"three attacks.",
						"three simple attacks. Alternatively, it can do one simple attacks and a special attack.",
					],
					[ # weights
						pb,
						pb,
						pb,
						pb//2,
						pb//3,
						pb//4,
						pb//3,
						pb//4,
						pb//5,
						pb//4,
						pb//4,
						pb//2,
						pb//4,
						pb//3,
					])
			))
	skewer = Entry_Text(f"Skewer",
		f"Once per turn, when {title} makes a Melee attack and hits, the target takes an extra {pb//2*3} ({pb//2}d6) damage, and the {race} gains temporary hit points equal to the extra damage dealt.")
	stench = Entry_Text(
		f"Stench",
		f"Any creature other than any {race} that starts its turn within 5 feet of {title} must succeed on a DC {8+npc.proficiency_bonus + npc.ability_scores.con_mod} Constitution saving throw or be poisoned until the start of the creature's next turn. On a successful saving throw, the creature is immune to the stench of all {race}s for 1 hour.")
	blood_frenzy = Entry_Text(
		f"Blood Frenzy",
		f"{title} has advantage on melee attack rolls against any creature that doesn't have all its hit points.")
	reckless = Entry_Text(
		f"Reckless",
		f"At the start of its turn, {title} can gain advantage on all melee weapon attack rolls during that turn, but attack rolls against it have advantage until the start of its next turn.")
	martial_advantage = Entry_Text(
		f"Martial Advantage",
		f"Once per turn, the {race} can deal an extra {npc.proficiency_bonus*3} ({npc.proficiency_bonus}d6) damage to a creature it hits with a weapon attack if that creature is within 5 feet of an ally of the {race} that isn't incapacitated.")
	MagicWeapons = Entry_Text(
		f"Magic Weapons",
		f"{title}'s attacks are magical.")
	GrapplingAttack = Entry_Text("Grappling Attack",
		f"When {title} makes a simple attack, it can grapple the creature instead of dealing damage (escape DC {8+pb+STR}).")
	FrightfulPresence = Entry_Text("Frightful Presence",
		f"Each creature of {title}'s choice that is within 120 feet of {title} and aware of it must succeed on a DC {dc} Wisdom saving throw or become frightened for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to {title}'s Frightful Presence for the next 24 hours."
		)
	WingAttack = Entry_Text("Wing Attack",
		f"{title} beats its wings. Each creature within 10 ft. of {title} must succeed on a DC {8+pb+STR} Dexterity saving throw or take {pb*3//2 + STR} ({pb//2}d6 + {STR}) bludgeoning damage and be knocked prone. {title} can then fly up to half its flying speed."
		)
	HorrificAppearance = Entry_Text("Horrific Appearance",
		f"Any humanoid that starts its turn within 30 feet of {title} and can see the {race}'s true form must make a DC{dc} Wisdom saving throw. On a failed save, the creature is frightened for 1 minute. A creature can repeat the saving throw at the start of each of its turns, with disadvantage if the {race} is within line of sight, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the {race}'s Horrific Appearance for the next 24 hours. \n\t Unless the target is surprised or the revelation of the {race}'s true form is sudden, the target can avert its eyes and avoid making the initial saving throw. Until the start of its next turn, a creature that averts its eyes has disadvantage on attack rolls against {title}."
		)
	DeathGlare= Entry_Text("Death Glare.",
		f"{title} targets one frightened creature {gender} can see within 30 feet of themselves. If the target can see the {race}, it must succeed on a DC {dc} Wisdom saving throw against this magic or drop to 0 hit points."
		)
	FireTouch = Entry_Text("Fire Touch",
		f"Melee Weapon Attack \t Hit: {3*(PB(pb)-1)} ({(PB(pb)-1)}d6 + {MIGHT}) fire damage. If the target is a creature or a flammable object, it ignites. Until a creature takes an action to douse the fire, the target takes 5 (1d10) fire damage at the start of each of its turns."
		)
	Heated = Entry_Text("Heated",
		select1([
		f"A creature that touches {title} or hits it with a melee attack while within 5 feet of it takes 3 (1d6) fire damage",
		f"Any metal melee weapon {title} wields deals an extra 3 (1d6) fire damage on a hit (included in the attack).",
		f"A creature that touches {title} or hits it with a melee attack while within 5 feet of it takes 3 (1d6) fire damage.",
		]))

	# Dictionary to store possible extra skills for each background
	try:
		extra_skills_background = {
			"Artist":	[		],
			"Bandit": 	[multiattack,		PackTactics,		Pounce,	Grappler],
			"Barbarian":[Siege,		Charge,			multiattack,		GrapplingAttack,	Pounce,	Charge,	],
			"Berserker":[Charge,			FrightfulPresence,	multiattack,		MagicWeapons,		reckless,			WoundedFury,		PackTactics,		Rampage,	Pounce,	Charge,	Grappler,	multiattack, blood_frenzy, reckless],
			"Charlatan":[reckless,			],
			"Commoner": [reckless,			PackTactics,		reckless],
			"Criminal": [multiattack,		MagicWeapons,		reckless,			PackTactics,		multiattack, reckless],
			"Cultist": [FireTouch, 			DeathGlare,			MagicWeapons, 		reckless, WoundedFury],
			"Crafter":	[Siege,				FireTouch,			MagicWeapons,		],
			"Druid":	[FireTouch,			MagicWeapons,				],
			"Expert":	[Siege,				FireTouch,			MagicWeapons,		],
			"Explorer":	[multiattack,		MagicWeapons,		],
			"Fighter":	[Charge,			multiattack,		],
			"Guard":	[Charge,			multiattack,		GrapplingAttack,	MagicWeapons,		PackTactics,		Charge,	],
			"Hero":		[FireTouch,			multiattack,		MagicWeapons,		WoundedFury,		Charge,	],
			"Hunter":	[multiattack,		PackTactics,		Pounce,	Grappler],
			"Knight":	[Siege,				Charge,			FrightfulPresence,	multiattack,		MagicWeapons,		Charge,	],
			"Mage":		[FireTouch,			MagicWeapons,		],
			"Merchant":	[MagicWeapons,		],
			"Monk": 	[FireTouch,			multiattack,		GrapplingAttack,	MagicWeapons,		Rampage,	Pounce,	Grappler],
			"Ninja": 	[FrightfulPresence,	multiattack,		MagicWeapons,		Pounce,			Grappler],
			"Noble": 	[multiattack,		MagicWeapons,		multiattack],
			"Pirate": 	[FrightfulPresence,	multiattack,		MagicWeapons,		reckless,			Pounce	],
			"Priest":	[MagicWeapons,				],
			"Paladin":	[FireTouch,			Charge,			multiattack,		],
			"Rogue": 	[MagicWeapons,		Pounce,	],
			"Ranger":	[multiattack,		],
			"Shaman":	[FireTouch,			DeathGlare		],
			"Soldier":	[Siege,				Charge,			multiattack,		MagicWeapons,		PackTactics,	],
			"Spy": 		[MagicWeapons,		Pounce,	],
			"Sorcerer":	[FireTouch,			],
			"Traveler": [MagicWeapons,		Pounce,	],
			"Prankster":[multiattack,		PackTactics],
			"Warrior": 	[multiattack,		MagicWeapons,		reckless,			Rampage,	Pounce,	Charge,	Grappler],
			"Warlock":	[FireTouch,			DeathGlare,		HorrificAppearance,					FrightfulPresence,	MagicWeapons,		WoundedFury],
			"Witch":	[DeathGlare,		HorrificAppearance,					FrightfulPresence,		],
			"Wizard":	[MagicWeapons,				],
		}

		# Dictionary to store possible extra martial skills for each race
		extra_skills_race = {
			"Aberration": 	[Charge,			DeathGlare,		HorrificAppearance,FrightfulPresence,	reckless,				WoundedFury,		Rampage,	Grappler,	reckless, blinding_spittle, body_thief, gibbering, tentacles, multiattack, devour_intellect, stench],
			"Aven":			[WingAttack,			WoundedFury,		],
			"Beast":		[Charge,			reckless,			WoundedFury,		PackTactics,		Rampage,	Pounce,	Charge,	Charge,	Grappler,	reckless, blood_frenzy, multiattack,skewer, stench],
			"Beastfolk":	[Charge,			FrightfulPresence,	reckless,			WoundedFury,		PackTactics,		Rampage,	Charge,	Grappler,	reckless, blood_frenzy, multiattack],
			"Catfolk":		[Siege,				Charge,			FrightfulPresence,	GrapplingAttack,	WoundedFury,		Rampage,			Pounce,		Charge,	],
			"Celestial":	[FireTouch,			WingAttack,		Rampage,			Charge,		],
			"Construct":	[Siege,				Heated,			GrapplingAttack,	Grappler,			],
			"Dragon":		[Heated,			FireTouch,			WingAttack,		FrightfulPresence,	Grappler,			],
			"Dwarf":		[Siege,				multiattack,		reckless,			Rampage,			],
			"Elemental":	[Siege,				Heated,			FireTouch,			Grappler,			],
			"Elf":			[Pounce,			],
			"Fey": 			[invisible_passage, gibbering, multiattack],
			"Fiend":		[Heated,			FireTouch,			DeathGlare,		HorrificAppearance,			FrightfulPresence,	GrapplingAttack,	reckless,			WoundedFury,		Rampage,			Charge,	skewer, stench, multiattack, blood_frenzy, reckless],
			"Giant":		[Siege,				FrightfulPresence,	GrapplingAttack,	reckless,			WoundedFury,		Rampage,			Charge,	Grappler,	],
			"Gnome":		[invisible_passage,	],
			"Goblin":		[multiattack,		],
			"Human":		[Siege,				WoundedFury,		Charge,			],
			"Kobold":		[PackTactics,		],
			"Lizardfolk": 	[FrightfulPresence,	multiattack,		GrapplingAttack,	reckless,			WoundedFury,		Rampage,			Pounce,	Grappler,	skewer, stench, blood_frenzy, reckless],
			"Monstrosity":	[FrightfulPresence,	reckless,			WoundedFury,		Rampage,			Charge,	Grappler,	blood_frenzy, reckless],
			"Ooze":			[GrapplingAttack,	Grappler,			],
			"Orc":			[Siege,				FrightfulPresence,	reckless,			WoundedFury,		PackTactics,		Rampage,	Charge,	],
			"Plant": 		[GrapplingAttack,	Grappler,			body_thief, tentacles, multiattack, devour_intellect, skewer],
			"Snakefolk":	[FrightfulPresence,	GrapplingAttack,	Grappler,			],
			"Undead": 		[DeathGlare,		HorrificAppearance,					FrightfulPresence,	GrapplingAttack,	reckless,			WoundedFury,		Rampage,			Charge,	body_thief, invisible_passage, multiattack, devour_intellect,skewer, stench, blood_frenzy, reckless],
			"Vampire": 		[DeathGlare,		HorrificAppearance,					FrightfulPresence,	GrapplingAttack,	reckless,			WoundedFury,		Rampage,			Charge,	body_thief, invisible_passage, multiattack, devour_intellect,skewer, stench, blood_frenzy, reckless],
		}

		extra_skills_subrace = {

			"Aboleth":		[DeathGlare,	],
			"Alien Spawn":	[HorrificAppearance,	Charge,	],
			"Armored Bear": [Siege,	],
			"Archangel":	[Siege,	],
			"Bugbear": 		[Siege,		Grappler,	],
			"Conquistador":	[Charge,	],
			"Cactoid Nomad":[Charge,	],
			"Couatl":		[Grappler,	],
			"Celestial Serpent": 		[Grappler,	WingAttack,	],
			"Cubus": 		[Grappler,	],
			"Chaos Warper":	[Heated,			HorrificAppearance,	Charge,	],
			"Concubus": 	[Grappler,	],
			"Chimera": 		[WingAttack,	],
			"Cyclops":		[DeathGlare,	],
			"Coatlfolk":	[Heated,			FireTouch,	],
			"Desert":		[Heated,			FireTouch,	],
			"Devil": [	Siege,		],
			"Dune Dino":	[FireTouch,	],
			"Eldritch Horror":			[HorrificAppearance,	],
			"Ent": [	Siege,	],
			"Fire Giant":	[Heated,			FireTouch,			],
			"Forgeclan":	[Heated,			FireTouch,			],
			"Fear Shadow":	[Charge,	],
			"Frogfolk":		[Charge,	],
			"Githyanki":	[Siege,				],
			"Golem":		[Charge,	],
			"Giant Owl":	[WingAttack,	],
			"Giant Eagle":	[WingAttack,	],
			"Gorgon":		[DeathGlare,	],
			"Hag":			[DeathGlare,	HorrificAppearance,	],
			"Hobgoblin": 	[Grappler,	],
			"Highlander": 	[Grappler,	],
			"Harpy": 		[HorrificAppearance,	],
			"Home Lares": [	Siege,	],
			"Hydrakin":	[	Siege,	],
			"Incubus": 		[Grappler,	],
			"Islander": 	[Grappler,	],
			"Island": 		[Grappler,	],
			"Kraken":	[Siege,	],
			"Kaiju":	[Siege,	],
			"Kaiju Dinosaur":	[Siege,	],
			"Lone Lover": 	[Grappler,	],
			"Leprechaun": 	[Grappler,	],
			"Living Spell": [Heated,			FireTouch,			],
			"Leonid":		[Siege,	],
			"Mischief Poltergeist": 	[Grappler,	],
			"Mounty Python":[Charge,	],
			"Moira":		[DeathGlare,	],
			"Minotaur":		[Siege,	],
			"Parca":		[DeathGlare,	],
			"Naga":			[Charge,	],
			"Nymph": 		[Grappler,	],
			"Nightmare": 	[HorrificAppearance,	],
			"Old One": 		[HorrificAppearance,		],
			"Pride Mummy": 	[Grappler,	],
			"Plainsfolk": 	[Charge,	],
			"Raptoran": 	[Charge,	],
			"Redcap": 		[Charge,	],
			"Satyr":		[Charge,	],
			"Salamandrian": [Charge,	],
			"Sands Elf":	[FireTouch,			],
			"Soul Collector": 	[Grappler,	],
			"Soulclaimer": 	[Grappler,	],
			"Stout": 		[Charge,	],
			"Succubus": 	[Grappler,	],
			"Sun Elf": 		[Heated,			FireTouch,			],
			"Sun Scarab": 	[FireTouch,			],
			"Shapeshifters":[HorrificAppearance,	],
			"Sphynx":		[WingAttack,	],
			"Solarpunks":[	Siege,],
			"Stonemason": [ Siege,],
			"Tengu":[	Siege,	],
			"Titan Rex": 	[Siege,	Charge,	],
			"Tomb's Hoarder": 	[Grappler,	],
			"Urbanite":	[	Siege,	],
			"Urban Elf":	[	Siege,	],
			"Uruk":	[Siege,	],
			"Vampire": 		[Grappler,	],
			"Vulture Spirit":[WingAttack,	],
			"Wild Elf": 	[Charge,	],
			"Wrathful Wraith": 		[Charge,	Siege,	],
			"Waxian":		[Heated,			],
			"Zephyrian": 	[Charge,	],


		}

		if "Abominational" in subrace:
			skills += [ Siege,	]
		# Fetch the extra skills for the selected race and background
		skills += list(set(extra_skills_race.get(npc.race, []) +
								extra_skills_subrace.get(npc.subrace, []) +
								extra_skills_background.get(npc.background, [])))

		if not skills: skills = [Charge]
		# Select and format skills
		skill = f"\n{random.choice(skills)}"
	#except SyntaxError as e:

	except Exception as e:
		skill = Charge
		raise RuntimeError("Martial Abilities unreached") from e


	return skill
