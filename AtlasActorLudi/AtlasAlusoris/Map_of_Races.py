'''NonPlayer generator Race catalogue and legacy subrace data.'''


def Player_Species(character):
	result = character.Pick(
		list(
			player,
			),
		weights=player.values(),
			purpose="NonPlayer.Player_Species",
		)
	return result

race_weights = {
"Aberration":   150, #
"Aven":         150, #
"Beast":        110,
"Beastfolk":    170,
"Catfolk":      130,
"Celestial":    151,
"Construct":    150,
"Dragon":       150,
"Dwarf":        170, # Based on the Spanish Golden Age (Conquistadores), Italians, Portuguese and Latino and Criollo Culture.
"Elemental":    150,
"Elf":          170, # Based on Nordic Fae, Vikings, Iceland, Romani, Celtic Ireland, Persian
"Fey":          150,
"Fiend":        150,
"Giant":        150,
"Gnome":        160,
"Goblin":       160,
"Halfling":     190, # Based on English and French Medieval Peasants
"Human":        200,
"Kobold":       160,
"Lizardfolk":   150,
"Monstrosity":  150,
"Ooze":         80,
"Orc":          180, # Cowboy / Native american inspired. A mix of Wild West fantasy
"Plant":        150,
"Snakefolk":    150,
"Undead":       180,
"Vampire": 		110,
		}




def Race(character):
	result = character.Pick(
		list(
			race_weights,
			),
		weights=race_weights.values(),
			purpose="NonPlayer.Race",
		)
	return result

def Aberrations(character):
	Names = {
		"Aboleth": 5,			# Immortal creatures of the Depths of the Sea and the Astral Sea
		"Beholder": 12,          # Known for their paranoia and individualism.
		"Shapeshifters": 3,     # Unique appearance as Mimics and shapeshifters with horrible true forms.
		"Illithid": 9,          # A highly intelligent race known for their psionic powers.
		"Old One": 	7,          # Ancient beings with vast knowledge and a desire to dominate other species.
		"Mindhive": 4,          # They seek knowledge and union by asimilation.
		"Depth Dominators": 5,  # Slave traders with a unique hierarchy.
		"Living Spell": 9,      # Former wizards transformed into monstrous forms.
		"Chaos Warper": 5,      # Cosmic horror element. Representing pure chaos, they're unpredictable.
		"Alien Spawn": 5,       # Cosmic horror element.
		"Parasyte": 4,          # Parasitic entities that can control other beings.
		"Symbioid": 4,          # Simbioit entities that can enhance and commune with other beings.
		"Destiny Devouers": 4,  # Time-traveling and body-swapping aliens.
		"Githyanki": 7,         # Raiders and conquerors.
		"Githzerai": 7,         # More enlightened.
		"Eldritch Horror": 7,	# Cuthulhu inspired civilization
		}

	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Aberrations",
		)

def Avens(character):
	Names = {
		"Birdfolk": 7,    # Generic birdfolk, versatile in nature.
		"Kenku": 11,      # Unique mimicry ability and urban setting.
		"Aarakocra": 8,   # High-flying and more spiritual.
		"Tengu": 6,       # Martial arts and japanese folklore connections.
		"Raptoran": 5,    # Mountain dwellers with a unique fast flight.
		"Owlin": 5,       # Owl-like Nocturnal and wise.
		"Harpy": 17,      # Half-bird, half-woman, often seen as omens.
	}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Avens",
		)

# Canonical Creature Type for each Alusoris Race label.
CREATURE_TYPE_BY_RACE = {
	"Aberration": "Aberration",
	"Aven": "Humanoid",
	"Beast": "Beast",
	"Beastfolk": "Humanoid",
	"Catfolk": "Humanoid",
	"Celestial": "Celestial",
	"Construct": "Construct",
	"Dragon": "Dragon",
	"Dwarf": "Humanoid",
	"Elemental": "Elemental",
	"Elf": "Humanoid",
	"Fey": "Fey",
	"Fiend": "Fiend",
	"Giant": "Giant",
	"Gnome": "Humanoid",
	"Goblin": "Humanoid",
	"Halfling": "Humanoid",
	"Human": "Humanoid",
	"Kobold": "Humanoid",
	"Lizardfolk": "Humanoid",
	"Monstrosity": "Monstrosity",
	"Ooze": "Ooze",
	"Orc": "Humanoid",
	"Plant": "Plant",
	"Snakefolk": "Humanoid",
	"Undead": "Undead",
	"Vampire": "Undead",
	}

def Creature_Type_For_Race(race):
	"""Map an Alusoris Race label to its canonical Creature Type key."""
	try:
		return CREATURE_TYPE_BY_RACE[
			race
			]
	except KeyError as error:
		raise ValueError(
			f"Unknown Alusoris Race: {race!r}."
			) from error

def Beasts(character):
	'''
	Are nonhumanoid creatures that are a natural
	part of the fantasy ecology. Some of them have magical
	powers, but most are unintelligent and lack any society
	or language. Beasts include all varieties of ordinary
	animals, dinosaurs, and giant versions of animals.
	'''
	Names = {
		"Armored Bear": 8,          # From Philip Pullman's His Dark Materials series.
		"Monkey King": 9,
		"Kong": 7,
		"Kaiju": 7,
		"Giant Eagle": 8,
		"Golden Lion": 7,
		"White Tiger": 6,
		"Vulture Spirit": 5,
		"Kitsune Fox": 10,
		"Deer Spirit": 6,           # Associated with gentleness and intuition in various cultures.
		"Giant Owl": 8,
		"Primal Stag": 7,        # Stags are often seen as messengers or connected to the otherworld in various mythologies.
		"Fenrir Wolf": 7,
		"Forest God": 5,            # A guardian of the forests, revered for its bravery.
		"Star Whale": 6,
		"Kaiju Dinosaur": 6,
		"Kerberus Dog": 7,
		"Sun Scarab": 9,
		"Moon Jackal": 6,
		"Spider Queen": 7,
		"Elder Elephant": 8 ,
		"Pandamonium": 7 ,
		"Phoenix": 2,
		"Pegasus": 2,
		"Unicorn": 1,             # Pure and gentle creatures, often associated with forests and healing.
		"landshark":4,
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Beasts",
		)

def Beastfolks(character):
	Names = {
		"Arachnidfolk": 16,     # Spiders are often associated with trickery and weaving fate.
		"Centaur": 19,          # Classic mythological creature, representing the wild side of humanity.
		"Elephantian": 13,		# Elephant and mammoth folks.
		"Gnoll": 16,            # Often seen as savage and chaotic, inspired by hyenas.
		"Insectfolk": 15,       # Unique and diverse, representing both hive minds and individuality.
		"Jackalmen": 16,        # Often seen in Egyptian mythologies, associated with the afterlife.
		"Kitsune": 18,          # Japanese fox spirits, both mischievous and wise.
		"Lycan": 17,            # General term for were-creatures, known for their cursed transformations.
		"Merfolk": 19,          # Classic creatures of the sea, representing both beauty and danger.
		"Minotaur": 18,         # The embodiment of the labyrinth's mystery and challenge.
		"Ratfolk": 17,          # Clever, opportunistic, and often seen in urban settings.
		"Scorpionfolk": 15,     # Dangerous and venomous, often used as guardians in myths.
		"Sharkfolk": 17,        # Predators of the sea, representing both fear and respect.
		"Skinwalker": 15,
		"Werebear": 16,         # A more noble version of lycanthropes, often associated with strength and protection.
		"Werewolf": 20,         # One of the most recognized lycanthropes, representing the untamed side of humanity.
		"Satyr": 18,            # Revelers and musicians, representing the carefree side of nature.
		"": 0
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Beastfolks",
		)

def Catfolks(character):
	Names = {
		"Leonid": 		15,
		"Pantherian": 	12,
		"Felinian": 	11,
		"Lynxen": 		13,
		"Leopardian": 	12,
		"Tigrisian": 	12,
		'Jaguarfolk':	10,
		'Puman': 8,
		"": 0
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Catfolks",
		)

def Celestials(character):
	'''
	Celestials are creatures native to the Upper Planes.
	Many of them are the servants of deities, employed
	as messengers or agents in the mortal realm and
	throughout the planes. Celestials tend to be good by nature,
	so the exceptional celestial who strays from a good
	alignment is a horrifying rarity. Celestials include
	angels, couatls, and pegasi.
	'''
	Names = {
		"Angelic Bloodline": 32,   # Mortals with celestial ancentry
		"Half-Angel": 22,          # Mortals with a celestial parent
		"Angel": 19,               # Classic representatives of good, messengers of deities.
		"Ascended": 18,            # Mortals who have risen to a divine or semi-divine status.
		"Saint": 18,               # Mortals with trascendent connections with the divine.
		"Couatl": 17,              # Feathered serpents, often seen as guardians or protectors.
		"Forgotten God": 16,       # Once powerful, now forgotten. Represents the ebb and flow of faith.
		"Lesser God": 18,          # Deities of minor aspects or domains.
		"Tutelar": 18,         	   # Local deities with limited influence.
		#"Pegasus": 17,            # The majestic winged horse, symbol of purity and grace.
		"Planetar": 19,            # High-ranking angels, often seen as warriors of good.
		"Seraph": 19,              # Burning ones, highest order of angels.
		"Throne": 18,              # Angels associated with celestial justice and maintaining the cosmic order.
		"Unicorn": 17,             # Pure and gentle creatures, often associated with forests and healing.
		"Celestial Serpent": 18,   # Serpentine creatures that reside in the heavens, symbols of power and majesty.
		"Valkyrie": 28,            # Choosers of the slain, guiding heroes to the afterlife.
		"Solar": 19,               # Extremely powerful celestial beings, champions of deities.
		"Ki-rin": 17,              # Eastern counterpart to unicorns, symbols of wisdom.
		"Deva": 18,                # Divine beings in Hindu mythology, often in conflict with Asuras.
		"Asura": 18,               # Divine beings in Zoroastrian mythology, often in conflict with Devas.
		"Archon": 18,              # Beings of pure law and good, often in opposition to demons and devils.
		"Archangel": 15,
		"Avatar": 15,              # Mortal form of a God
		"Zodiac": 19,			   # Star-made beings that wave fate
		}

	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Celestials",
		)

def Constructs(character):
	'''
	Constructs are made, not born. Some are
	programmed by their creators to follow a simple set of
	instructions, while others are imbued with sentience
	and capable of independent thought. Golems are the
	iconic constructs. Many creatures native to the outer
	plane of Mechanus, such as modrons, are constructs
	shaped from the raw material of the plane by the will of
	more powerful creatures.
	'''
	Names = {
		"Animated Armor": 8, 		# Empty suits of armor brought to life, often as guardians.
		"Drone": 7, 				# Modern or futuristic unmanned devices, often for reconnaissance.
		"Golem": 9, 				# Beings made from inanimate material, like clay or stone. Classic magic constructs.
		"Homunculus": 7, 			# Full Metal Alchemist's style created humanoids.
		"Robot": 7,					# Mechanical Slave
		"Android": 6,				# Homanoid Constructs
		"Scarecrow": 7,				# Animated scarecrows, often created to protect crops but can be sinister.
		"Clockwork": 8,				# Intricate mechanical beings, often steampunk-inspired.
		"Warforged": 9, 			# Sentient constructs made for war, often searching for purpose after conflict.
		"Modron": 8, 				# Geometrically inspired beings from a plane of utter order.
		"Shield Centinel": 8, 		# Created to protect its creator, often bound by an amulet.
		"Origami Spell": 7, 		# Animated books or beings made of paper, protecting knowledge.
		"Effigy": 8, 				# Ritualistic statues or figures, animated for various purposes.
		"Animus": 8,  				# Soul holded by animatrons.
		"Soulhost": 8,  			# Soul jar in an independent robot The soul controls the host.
		"Soulmech": 8  				# Soul jar in an independent robot The soul controls the host.
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Constructs",
		)


DragonColors = {
		"Black": 18,               # Chromatic, acid breath.
		"Blue": 18,                # Chromatic, electric breath.
		"Green": 18,               # Chromatic, poison breath.
		"Red": 18,                 # Chromatic, fire breath.
		"White": 18,               # Chromatic, cold breath.
		"Bronze": 17,              # Metallic, good-aligned, lightning breath.
		"Silver": 17,              # Metallic, cold/paralyzing breath.
		"Gold": 17,                # Metallic, fire/weakening breath.
		"Brass": 17,               # Metallic, fire/sleep breath.
		"Copper": 17,              # Metallic, acid/slowing breath.
		"Shadow": 16,              # Tainted by Shadowfell, necrotic breath.
		"Gem": 16,                 # Rare, associated with gemstones and psionics.
		"Ethereal": 15,            # From the Ethereal Plane.
		"Planar": 15,              # Associated with specific planes.
		"Prismatic": 13 ,           # Rare and extremely powerful, known for multi-colored, rainbow-like powers.
		}

def Dragons(character):
	'''
	Dragons are large reptilian creatures of ancient origin
	and tremendous power. True dragons, including the
	good metallic dragons and the evil chromatic dragons,
	are highly intelligent and have innate magic. Also in this
	category are creatures distantly related to true dragons,
	but less powerful, less intelligent, and less magical, such
	as wyverns and pseudodragons.
	'''
	DragonTypes = {
		"Dragonborn": 33,         # Dragon-like humanoids.
		"Wyrm": 20,
		"Drake": 17,
		"Draco": 16,
		"Dragon": 18,
		"Sky Serpent": 15,
		"Half Dragon": 14,
		"Dragon Turtle": 14,
		"Centenary": 11,        # Old Dragons
		"Millenary": 11,        # Ancient Dragons
		"Wyvern": 15,           # 2 leged Dragons
		"Long": 13,             # Dragons of asian mythology
		"Drakon": 13,           # Dragons of greek mythology
		}


	# Pick one from each category
	chosen_type = character.Pick(
		list(
			DragonTypes,
			),
		weights=DragonTypes.values(),
			purpose="NonPlayer.Dragons",
		)
	chosen_color = character.Pick(
		list(
			DragonColors,
			),
		weights=DragonColors.values(),
			purpose="NonPlayer.Dragons.2",
		)

	return f"{chosen_color} {chosen_type}"

def Elementals(character):
	'''
	Elementals are creatures native to the elemental
	planes. Some creatures of this type are little more than
	animate masses of their respective elements, including
	the creatures simply called elementals. Others have
	biological forms infused with elemental energy. The
	races of genies, including djinn and efreet, form the
	most important civilizations on the elemental planes.
	Other elemental creatures include azers, invisible
	stalkers, and water weirds.
	'''
	Names = {
		"Atlantian": 10,     # Connection to water and ancient crystal technology.
		"Chronian": 7,       # Time elementals
		"Cronusian": 6,      # Representing time and age.
		"Eosian": 	9,       # Tied to the rising sun.
		"Etherian": 9,       # Ether and the electric.
		"Gaian": 	10,      # Essence of the earth.
		"Galaxian": 9,       # Elemental related to constellations and stars.
		"Genasi": 	21,      # Representing air, earth, fire, and water.
		"Genie": 	11,      # Powerful primordial entities.
		"Hyperian": 8,       # Radiant, solar-powered.
		"Magmaforged": 10,   # Fusion of earth and fire.
		"Oceanians": 10,     # Depths, tides, storms.
		"Primordial": 8,     # Fundamental forces of reality.
		"Promethean": 9,     # Fire, electricity, and energy, with spirit of innovation.
		"Salamandrian": 4,   # Associated with fire.
		"Nymphian":		4,	 # Water elementals
		"Sylphians": 	4,   # Air elementals
		"Pigmians":		4,	 # Earth Elementals
		"Tartarian": 9,      # Dark ocean depths.
		"Titan": 9,          # Raw elemental power.
		"Tundran": 9,        # Harsh icy landscapes.
		"Uranians": 9,       # Sky, stars, celestial magic.
		"Zephyrian": 10,     # Gentle airs.
		"Djinn": 4,			 # Beings with fire in their eyes, they live in the dessert and ride cyclons.
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Elementals",
		)

def Fiends(character):
	'''
	Fiends are creatures that are native
	to the Lower Planes. A few are the servants of deities,
	but many more labor under the leadership of archdevils
	and demon princes. Evil priests and mages sometimes
	summon fiends to the material world to do their bidding.
	Fiends include demons, devils, rakshasas...
	Devils are are related to Guilt, Sin, Desire, Punishment, and Retrivution.
	Demons are related to Chaos, Vanity, Ego, Lust, Change, Sickness, and War.
	Devils are the
	'''
	Names = {
		"Tiefling": 30,
		"Devil": 17,
		"Demon": 17,
		"Imp": 		13,
		"Cubus": 8,
		"Incubus": 8,
		"Succubus": 8,
		"Concubus": 7,
		"Dwarvendevil": 5,
		"Elvendevil": 5,
		"Gnolldevil": 5,
		"Orkishdevil": 5,
		"Goblindevil": 5,
		"Dwarvendemon": 4,
		"Elvendemon": 4,
		"Demongnoll": 4,
		"Orkishdemon": 4,
		"Goblindemon": 4,
		"Nightmare": 8,
		"Rakshasa": 10,
		"Fallen Angel": 11,
		"Hellbound Hunter": 9,
		"Leviathan": 7,
		"Behemoth": 7,
		"Shinigami":10,
		"Hell's Rider": 10,
		"Soul Collector": 8,
		"Infinder": 7,
		"Sinvestigator": 6,
		"Chaoslord": 7,
		"Justiciar": 8,
		"Vengeance Spirit": 7,
		"Retributioner": 7,
		"Pact Enforcer": 8,
		"Soulclaimer": 8,
		"Infernal Enforcer": 8,
		"Inforcer": 8,
		"Dark Gods": 1
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Fiends",
		)

def Feys(character):
	'''
	Fey are magical creatures closely tied to the realm of Dreams.
	They dwell in twilight groves and misty forests, merging From
	both the personal and the collective uncunscious. Some may
	produce nightmares, such as hags, while other bliss and joy,
	as Pixies do. From daydreaming to life-long dreams, they take
	a part on all of mortal's fantasies.
	They are closely tied to folklore, legends, and mythology.
	In some worlds, they are closely tied to the Feywild, also
	called The Dream.
	Fey include dryads, pixies, and satyrs.
	'''
	Names = {
		"Hag": 10,		# Witches often associated with dark magic
		"Nymph": 12,	# Spirits of nature: water, forest, etc.
		"Pixie": 10,	# Tiny, mischievous spirits
		"Satyr": 12,	# Half-man, half-goat
		"Sprite": 9,	# Airy spirits similar to pixies but usually less mischievous
		"High Fae": 7,  # Powerful fey lords and ladies
		"Redcap": 6,    # Malicious goblin-like creatures
		"Banshee": 6,   # Spirits heralding death
		"Leprechaun": 8,	# Mischievous little fey associated with pots of gold
		"Changeling": 6,	# Fey child left in place of a stolen human child
		"Nexus Fey": 7,		# Fey connected to a connection point
		"Duende": 6,		# Fey of the arts, beauty, and nature. Tricksters.
		"Home Lares": 5,	# Guardians of homes and families
		"Fata": 2,          # Fae that intervine in someone's fate, providing luck
		"Moira": 2,         # Fae guide someone's fate, spinning the fabric of life
		"Parca": 2,         # Fae omen of death, they come to cut the thread of life.
		"Archfey": 1,       # Fae of Enormous significance, akin to gods in the feywild
	}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Feys",
		)

def Giants(character):
	Names = {
		"Goliath": 20,				# Half Giants
		"Firbolg": 12,				# Tree hugging semigiants
		"Cyclops":  9,              # Greek one-eyed giants
		"Ogre":     11,             # Brutish man-eaters
		"Troll":    10,             # Norse mountain dwellers
		"Colossus":	10,				# City Protectors, guardians of civillizations and cultures
		"Jotunn (Frost Giant)": 8,  # Norse primal giants
		"Fire Giant": 8,            # Inhabitants of Muspelheim
		"Gigantes": 7,              # Giants from Greek mythology
		"Nephilim": 6,              # Biblical giants
		"Oni":      10,             # Japanese ogre-like giants
		"Ettin (Two headed)": 7,        # English two-headed giants
		"Fomorians (Sea Giants)": 6,    # Irish sea giants
		"Cloud Giant": 8,           # Noble sky dwellers
		"Stone Giant": 8,           # Earthy, rocky giants
		"Storm Giant": 7,               # Majestic tempest giants
	}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Giants",
		)

def Gnomes(character):
	Names = {
		"Mountain": 9,
		"Forest": 9,
		"Garden": 2,
		"Tinker": 5,
		"Crossroad": 4,
		"Wandering": 4,
		"Leprechaun": 2,
	}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Gnomes",
		)

def Goblins(character):
	Names = {
		"Goblin": 17,                       # Mischievous green-skinned creatures
		"Hobgoblin": 10,                     # Disciplined, militant goblinoids
		"Bugbear": 9,                       # Stealthy brutes of the goblinoid family
		"Gremlin (Tecnogoblin)": 8,         # Saboteurs of machinery
		"Redcap": 7,                        # Bloodthirsty goblin-like fey
		"Nyk (Watergoblin)": 8,             # Slavic water-dwelling goblins
		"Trow (Dark goblin)": 7,            # Orcadian mischief-makers
		"Knocker (Underdark goblin)": 8,    # Cornish mine-dwelling creatures
		"Domovoi (House Goblin)": 7,         # Slavic house spirits
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Goblins",
		)

def Humans(character, *, dice=None):
	if dice is None:
		dice = character.Dice_Bag(
			"Human.culture",
			)
		#-- the one bag of the Human's culture, the same one Map_of_Species
		#-- opens and passes; a caller that opened none gets it here
	Types = {
		"Local":        30,
		"Foreigner": 	25,
		"Highlander": 	20,
		"Nomad": 		20,
		"Islander": 	16,
		"Forester": 	16,
		"Plainsfolk": 	15,
		"Urbanite":		14,
		"Northerner":	20,
		"Southerner": 	20,
		"Easterner":	20,
		"Westerner":	20,
		}
	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
		dice=dice,
		)
	return f"{chosen_type}"

def Monstrosities(character):
	Names = {
		"Chimera": 		18,
		"Doppelganger": 18,
		"Shapeshifter": 10,
		"Gorgon": 		17,
		"Horror": 		16,
		"Sphynx": 		32,
		"Wendigo": 		13,
		"Kraken": 		15,
		"Nightmare": 	10
		}
	chosen_type = character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Monstrosities",
		)
	return chosen_type

def Oozes(character):
	Types = {
		"Plasmoid": 		18,	# Ooze people from space
		"Abominational": 	18, # From the Abomi-Nation. Owl House's Darius Deamonne and alike.
		"Magman": 			4,	# Lava people
		"Crystalclan": 		4,	# Crystalized shapes turn alive by the power of vibes
		"Cubecub": 			7,	# Cute cubes that can be friendly or terrorific
		"Frosten": 			5,	# Olaf kind of frozen maleable creature of snow.
		"Eldritch": 		3,	# The Thing? Probably something Kronengberg
		"High Mimic": 		6,
		"Slime": 			18,
		#"Adiposal": 3,
		}
	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Oozes",
		)
	return f"{chosen_type}"

def Orcs(character):
	# Cowboy / Native american inspired. Naturally nomadic, or with huge territories for each settlement. Willing to live among monsters, orcs are rough but fair. THeir societies value honor and personal responsibbility, along with comunnity care. "Wild America" as inspiration.
	Names = {
		"Mountain": 5,
		"Desert": 5,
		"Swamp": 6,
		"Snow": 4,
		"Uruk": 6,
		"Half-Orc": 7,
		"Orog (Underdark)": 5,
		"Cave": 6,
		"Forest": 6,
		"Nomadic": 7,
		"Island": 6,
		"Urbanite": 9,
		"Feral": 7
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Orcs",
		)

def Plants(character):
	Names = {
		"Willow Guardian": 10,
		"Treant": 12,
		"Awakened Tree": 12,
		"Forefather Oak": 10,
		"Myconid Sovereign": 10,
		"Ent": 12,
		"Treefolk": 10,
		"Floral Walkers": 10,
		"Living Totem": 10,
		"Walker Vine": 12,
		"Singing Lotus": 10,
		"Lichen Gravetaker": 10,
		"Cactoid Nomad": 9,
		"Vegetation Abomination":9,
		"Dryad":18,
		"Fungical Intellectual": 8,
		"Myceliuman": 8,
		}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Plants",
		)

def Undeads(character):
	Names = {
			"Cursed Eternal": 12,        # Mindless undead, driven by a hunger for the living.
			"Death Knight": 10,          # Elite undead warriors, remnants of former knights or warlords.
			"Despair Specter": 14,       # Souls that suffered tremendous despair, wishing the same for the living.
			"Fear Shadow": 12,           # Undead born from intense fear, lurking in darkness.
			"Honor Phantom": 12,         # Ethereal spirits bound by duty or a promise made in life.
			"Lich": 20,                  # Undying mages who sought eternal life through dark rituals.
			"Mischief Poltergeist": 12,  # Playful spirits, causing disturbances to attract attention.
			"Penance Wraith": 10,        # Souls seeking atonement for sins committed in life.
			"Pride Mummy": 12,           # Preserved dead, animated to guard ancient tombs and relics.
			"Protector Spirit": 14,      # Benevolent spirits still guarding a place, object, or person.
			"Ungone Ghost": 13,       	 # Souls trapped due to unfinished business or profound regrets.
			"Skeleton Protector": 14,    # Animated skeletal guardians, defending locations or treasures.
			"Thinker Skull": 12,         # Knowledgeable remnants, often used by dark mages for counsel.
			"Tomb's Hoarder": 10,        # Guardians of burial sites, obsessed with their treasures.
			"Vengeful Revenant": 10,     # Resurrected by sheer force of will to enact revenge.
			"Weeping Howler": 10,        # Spirits that mourn and wail, often announcing death.
			"Wrathful Wraith": 12,       # Souls consumed by anger, seeking to draw others into death.
			}
	return character.Pick(
		list(
			Names,
			),
		weights=Names.values(),
			purpose="NonPlayer.Undeads",
		)

def Elves(character):
	Types = {
		"High Elf": 18,
		"Sylvan Elf": 18,
		"Wood Elf": 18,
		"Dark Elf": 18,
		"Night Elf": 11,
		"Feywild Elf": 8,
		"Shadow Elf": 8,
		"Sea Elf": 13,
		"Nomad Elf": 13,
		"Snow Elf":8,
		"Sun Elf": 6,
		"Eclipse Elf":4,
		"Moon Elf": 6,
		"Wild Elf": 6,
		"Urban Elf": 13,
		"Sands Elf": 10,
		"Eladrin": 3,
		}
	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Elves",
		)
	return f"{chosen_type}"

def Halflings(character):
	Types = {
		"Hill": 12,         # Traditional, grounded, and tied to farm life.
		"Stout": 12,        # Hardy and resourceful, living near mountains or dwarves.
		"Countrian": 8,     # Traditionalist. Proud and insular, wary of strangers but fiercely independent.
		"Wanderlust": 6,    # Always traveling, rarely settle, pastoral.
		"Treetender": 6,    # Druidic Theocracy. Live in harmony with forests, druidic and arboreal climbers.
		"Sybarite": 10,     # Adapted to city life, merchants, free-city capitalist. Urban-dwelling merchants, capitalist free-thinkers.
		"Desert": 6,        # Adapted to arid climates, resilient and resourceful in scarcity.
		"Frostclan": 4,     # Hardy survivors of icy tundras and mountains.
		"Islander": 4,      # Coastal or archipelago dwellers, adept sailors and swimmers.
		"Solarpunks": 4,    # Anarchists, Live in harmony with flora, great herbalists and tinkerers
		"Comaradian": 4, 	# “Together, we thrive.”. Strength by unions. Democratic.
		"Eldertribe": 4,  	# Wisdom of the elders ensures balance.
		"Cloudwalker":3,	# Dreamers and inventors, creating airships and flying wonders.
		"Unlander": 1,      # Lone hobbit. Apatria
		}
	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Halflings",
		)
	return f"{chosen_type}"

def Dwarfs(character):
	Types = {
		"Mountain": 		20,
		"Conquistador":		10,
		"Seawolf": 			10,
		"Tinkerer": 		10,
		"Roadbarter": 		10,
		"Urbanite": 		12,
		"Stonemason": 		7,
		"Darkin":			5,
		"Crystal Cavern":	3,
		"Canyon Dweller":	5,
		"Bank Templar":		5,
		"Forgeclan": 		5
		}
	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Dwarfs",
		)
	return f"{chosen_type}"

def Lizardfolks(character):
	Types = {
		"Swamp Crocfolk": 8,
		"Jungle Guanafolk": 7,
		"Desertic Horned": 5,
		"Dune Dino":4,
		"Kappa": 2,
		"White Albino": 1,
		"Feathered Dinofolk":5,
		"Colored Chamalfolk":3,
		"Titan Rex": 3,
		"Tundra Saurius": 3,
		"Turtlefolk":6,
		"Frogfolk": 4,
		"Silurian": 	5,
		}

	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Lizardfolks",
		)

	return f"{chosen_type}"

def Kobolds(character):

	Kobold = {
		"Kobold":  10,
		"Winged Kobold":  1,
		}

	# Pick one from each category
	chosen_type = character.Pick(
		list(
			Kobold,
			),
		weights=Kobold.values(),
			purpose="NonPlayer.Kobolds",
		)
	chosen_color = character.Pick(
		list(
			DragonColors,
			),
		weights=DragonColors.values(),
			purpose="NonPlayer.Kobolds.2",
		)

	return f"{chosen_color} {chosen_type}"

def Snakefolks(character):
	Types = {
		"Arboreasps": 4,        # In lush forests, possibly skilled in herbalism and natural resources.
		"Iciconda": 2,          # Powerful, adapted to cold climates, resilient against extreme cold.
		"Titanboa": 3,          # Native to island ecosystems, they have a build of extraordinary size.
		"Nightscale": 3,        # Adapted to night and subterranean life, blending in the dark.
		"Aspisian": 4,          # Traveling across terrains, known for adaptability and diverse cultural knowledge.
		"Gorgonian": 2,         # Descended from mythical Gorgons, characterized by strong presence and traits.
		"Hydrakin": 1,          # Rare, revered, connected to multi-headed serpent deities.
		"Mounty Python": 3,     # A jovial and humorous society, known for their wit and good-natured humor. They tend to kill parrots.
		"Coatlfolk": 5,         # Mythical resonance, possibly linked to spiritual practices.
		"Cobraclan": 6,         # Resilient in desert environments.
		"Vipertongue": 5,       # Known for their naturally venomous abilities.
		"Ophidian": 4,          # Adapted to jungle environments, skilled in stealth and survival.
		"Naga": 4,              # Respected for their swimming abilities and connection to aquatic environments.
		"Lamia": 4,				# Greek mythical snake-ladies with  taste for human flesh
		"Ouroboros' Spawn": 2,
		}

	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Snakefolks",
		)

	return f"{chosen_type}"

def Vampires(character):
	Types = {
		"Dhampire":	10,
		"Neophyte": 10,
		"Venator": 8,
		"Nosferatian": 8,
		"Draculian": 5,
		"Bloodline": 7,
		"Bloodbound": 7,
		"Feral": 8,
		"Sanguine": 8,
		"Strigoi": 5,
		"Sekhmet": 3,
		"Malkavian": 3,
		"Nixtari": 3,
		"Vespiri": 3,
		"Moroi": 5,
		"Libitan": 2,
		"Lustari": 2,
		"Dreamhunter": 2,
		"Insomne": 2,
		"Anergetic": 2,
		"Animus": 2,
		"Daywalker": 1,
		"Elder": 1,

		}

	chosen_type = character.Pick(
		list(
			Types,
			),
		weights=Types.values(),
			purpose="NonPlayer.Vampires",
		)

	return f"{chosen_type}"


def Monster(character, Type):
	return Subrace(
		character,
		Type,
		)

def Creature(character, Type):
	return Subrace(
		character,
		Type,
		)

def Subrace(character, Type):
	type_function_map = {
		"Aberration": Aberrations,
		"Aven": Avens,
		"Beast": Beasts,
		"Beastfolk": Beastfolks,
		"Catfolk":  Catfolks,
		"Celestial": Celestials,
		"Construct": Constructs,
		"Dragon": Dragons,
		"Dwarf": Dwarfs,
		"Elemental": Elementals,
		"Elf": Elves,
		"Fey": Feys,
		"Fiend": Fiends,
		"Giant": Giants,
		"Goblin": Goblins,
		"Gnome": Gnomes,
		"Human": Humans,
		"Halfling": Halflings,
		"Kobold": Kobolds,
		"Lizardfolk":Lizardfolks,
		"Monstrosity": Monstrosities,
		"Orc": 	Orcs,
		"Ooze": Oozes,
		"Plant": Plants,
		"Snakefolk":Snakefolks,
		"Undead": Undeads,
		"Vampire": Vampires,
	}

	if Type in type_function_map:
		subrace = type_function_map[Type](
			character,
			)
	else:
		subrace = f"{Type} of an enigmatic lineage."

	return subrace



def AC_race_modifier(
	race = "",
	subrace = "",
	):
	AC_modifiers = {
		"Human": 2,
		"Beast": 3,
		"Beastfolk": 3,
		"Construct": 6,
		"Dragon": 5,
		"Dwarf":  3,
		"Elf": 2,
		"Giant": 3,
		"Goblin": 1,
		"Kobold": 3,
		"Lizardfolk": 5,
		"Orc": 3,
		"Undead": -3,
		"Ooze": -3,
		"Turtlefolk": 6,
		"Death Knight": 4,
		"Skeleton Protector": 2,
		"Vampire": 3,
		"Cactoid Nomad": 4,
		"Ogre": -2,
		"Troll": -1,
		"Scarecrow": -4,
		}
	AC = 0
	AC += AC_modifiers.get(race, 0)
	AC += AC_modifiers.get(subrace, 0)
	return AC


def AS_racial_modifier(npc):
	Dice = npc.Roll
	creature_type = npc.race + ' ' + npc.subrace

	### Ability Scores Generation
	STR = npc.AS.STR
	DEX = npc.AS.DEX
	CON = npc.AS.CON
	INT = npc.AS.INT
	WIS = npc.AS.WIS
	CHA = npc.AS.CHA

	AS_background_modifier(npc)

	### Race-based Ability Score Adjustments
	if "Human" in creature_type:
		# All humans have a baseline adaptability, hence the small boost to every ability score.
		STR += 1
		DEX += 1
		CON += 1
		INT += 1
		WIS += 1
		CHA += 1

		if "Local" in creature_type:
			CHA += Dice(4)
		if "Foreigner" in creature_type:
			WIS += Dice(4)
		if "Highlander" in creature_type:
			STR += Dice(4)
		if "Nomad" in creature_type:
			CON += Dice(4)
		if "Islander" in creature_type:
			DEX += Dice(4)
		if "Forester" in creature_type:
			WIS += Dice(4)
		if "Plainsfolk" in creature_type:
			CON += Dice(3)
			STR += Dice(3)
		if "Urbanite" in creature_type:
			CHA += Dice(4)
		if "Northerner" in creature_type:
			STR += Dice(4)
		if "Southerner" in creature_type:
			CHA += Dice(4)
		if "Easterner" in creature_type:
			INT += Dice(4)
		if "Westerner" in creature_type:
			DEX += Dice(4)

	if "Aberration" in creature_type:
		CON += Dice(4)
			# Aberrations often have hardy constitutions due to their alien nature.

		if npc.subrace == "Aboleth":
			# Bonus to charisma due to their terrifying presence and wisdom for their ancient knowledge.
			CHA += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Beholder":
			# Bonus to Intelligence for their ancestral memory. And constitution for their resillience
			INT += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Shapeshifters":
			CHA += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Illithid":
			# Bonus to intelligence for their psychic capabilities and charisma for their mental influence.
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Old One":
			INT += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Mindhive":
			CHA += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Depth Dominators":
			CHA += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Living Spell":
			CHA += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Chaos Warper":
			CHA += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Alien Spawn":
			STR += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Parasyte":
			DEX += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Symbioid":
			STR += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Destiny Devouers":
			STR += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Githyanki":
			STR += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Githzerai":
			DEX += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Eldritch Horror":
			CON += Dice(4)
			CHA += Dice(4)

	if "Aven" in creature_type:
		DEX += Dice(4)  # Avens, being bird-like, generally have good agility and coordination.

		if npc.subrace == "Birdfolk":
			CON += Dice(4)
		elif npc.subrace == "Kenku":
			CHA += Dice(4)
		elif npc.subrace == "Aarakocra":
			WIS += Dice(4)
		elif npc.subrace == "Tengu":
			DEX += Dice(4)
		elif npc.subrace == "Raptoran":
			STR += Dice(4)
		elif npc.subrace == "Harpy":
			CHA += Dice(4)

	if "Beast" == npc.race:
		CON += Dice(4)

		if npc.subrace == "Armored Bear":
			STR += Dice(4)
		elif npc.subrace == "Monkey King":
			WIS += Dice(4)
		elif npc.subrace == "Kong":
			STR += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Kaiju":
			STR += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Giant Eagle":
			DEX += Dice(4)  # For their flying capabilities
			WIS += Dice(4)  # Keen senses, especially sight
		elif npc.subrace == "Golden Lion":
			STR += Dice(4)
			CHA += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "White Tiger":
			STR += Dice(4)
			WIS += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Vulture Spirit":
			WIS += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Kitsune Fox":
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Deer Spirit":
			WIS += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Giant Owl":
			INT += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Primal Stag":
			WIS += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Fenrir Wolf":
			CHA += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Forest God":
			WIS += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Star Whale":
			STR += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Kaiju Dinosaur":
			STR += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Kerberus Dog":
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Sun Scarab":
			CON += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Moon Jackal":
			CHA += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Spider Queen":
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Ouroboros' Spawn":
			CON += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Elder Elephant":
			WIS += Dice(4)
			INT += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Pandamonium":
			DEX += Dice(4)
			STR += Dice(4)
			CON += Dice(4)

	if "Beastfolk" in creature_type:
		if npc.subrace == "Arachnidfolk":
			DEX += Dice(4)  # Representing their speed and agility
			INT += Dice(4)  # Scheeming
			CHA += Dice(4)  # Gregarian nature
		elif npc.subrace == "Centaur":
			STR += Dice(4)
			WIS += Dice(4)
			CON += Dice(4)  # Sturdy constitution
		elif npc.subrace == "Elephantian":
			WIS += Dice(4)
			CON += Dice(4)  # Sturdy constitution
			INT += Dice(4)
		elif npc.subrace == "Gnoll":
			DEX += Dice(4)
			CON += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Insectfolk":
			DEX += Dice(4)
			CHA += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Jackalmen":
			WIS += Dice(4)
			DEX += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Kitsune":
			CHA += Dice(4)
			DEX += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Lycan":
			STR += Dice(4)
			WIS += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Merfolk":
			CHA += Dice(4)
			DEX += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Minotaur":
			STR += Dice(4)
			CON += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Ratfolk":
			DEX += Dice(4)
			CON += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Scorpionfolk":
			STR += Dice(4)
			CON += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Sharkfolk":
			STR += Dice(4)
			CON += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Skinwalker":
			CHA += Dice(4)
			CON += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Werebear":
			STR += Dice(4,2)
			CON += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Werewolf":
			STR += Dice(4)
			CON += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Satyr":
			WIS += Dice(4)
			INT += Dice(4)
			CHA += Dice(4)

	if "Catfolk" in creature_type:
		DEX += Dice(4)
		if npc.subrace == "Leonid":
			STR += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Pantherian":
			DEX += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Felinian":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Lynxen":
			DEX += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Leopardian":
			DEX += Dice(4,2)
		if npc.subrace == "Tigrisian":
			DEX += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Jaguarfolk":
			STR += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Puman":
			STR += Dice(4)
			INT += Dice(4)

	if "Celetial" in creature_type:
		CHA += Dice(4)

		if "Angelic Bloodline" in npc.subrace:
			CHA += Dice(4)  # Radiant presence
		elif "Half-Angel" in npc.subrace :
			STR += Dice(4)
		elif "Angel" 	in npc.subrace :
			WIS += Dice(4)
		elif "Ascended" in npc.subrace :
			CHA += Dice(4)
		elif "Saint" 	in npc.subrace :
			WIS += Dice(4)
		elif "Couatl" 	in npc.subrace :
			DEX += Dice(4)
		elif "Couatl" 	in npc.subrace :
			DEX += Dice(4)
		elif "Forgotten God" in npc.subrace :
			STR += Dice(4)
			CON += Dice(4)
		elif "Lesser God" in npc.subrace :
			STR += Dice(4)
			WIS += Dice(4)
		elif "Tutelar" 	in npc.subrace :
			CHA += Dice(4)
			WIS += Dice(4)
		elif "Planetar" in npc.subrace :
			STR += Dice(4)
			WIS += Dice(4)
		elif "Seraph" 	in npc.subrace :
			STR += Dice(4)
			WIS += Dice(4)
			CHA += Dice(4)
		elif "Throne" 	in npc.subrace :
			INT += Dice(4)
			WIS += Dice(4)
			CHA += Dice(4)
		elif "Unicorn" 	in npc.subrace :
			CHA += Dice(4)
			WIS += Dice(4)
			DEX += Dice(4)
		elif "Celestial Serpent" in npc.subrace :
			CON += Dice(4)
			WIS += Dice(4)
			DEX += Dice(4)
		elif "Valkyrie" in npc.subrace :
			CON += Dice(4)
			STR += Dice(4)
			DEX += Dice(4)
		elif "Solar" 	in npc.subrace :
			WIS += Dice(4)
			STR += Dice(4)
			DEX += Dice(4)
		elif "Ki-rin" 	in npc.subrace :
			WIS += Dice(4)
			CHA += Dice(4)
			DEX += Dice(4)
		elif "Deva" 	in npc.subrace :
			WIS += Dice(4)
			CHA += Dice(4)
			STR += Dice(4)
		elif "Asura" 	in npc.subrace :
			INT += Dice(4)
			CHA += Dice(4)
			STR += Dice(4)
		elif "Archon" 	in npc.subrace :
			INT += Dice(4)
			CHA += Dice(4)
			WIS += Dice(4)
		elif "Archangel" in npc.subrace :
			INT += Dice(4)
			CHA += Dice(4)
			WIS += Dice(4)
			STR += Dice(4)
		elif "Avatar" 	in npc.subrace :
			INT += Dice(4)
			CHA += Dice(4)
			WIS += Dice(4)
			STR += Dice(4)
			CON += Dice(4)
			DEX += Dice(4)

	if "Construct" in creature_type:
		CON += Dice(4)
		npc.subrace = npc.Pick(["Stone Golem", "Iron Golem", "Wooden Puppet", "Clockwork Automaton", "Magical Sentinel", "Homunculus"], purpose="NonPlayer.AS_racial_modifier")

		if npc.subrace == "Animated Armor":
			STR += Dice(4)
		elif npc.subrace == "Drone":
			DEX += Dice(4)
		elif npc.subrace == "Golem":
			CON += Dice(4)
		elif npc.subrace == "Homunculus":
			CHA += Dice(4)
		elif npc.subrace == "Robot":
			INT += Dice(4)
		elif npc.subrace == "Android":
			WIS += Dice(4)
		elif npc.subrace == "Scarecrow":
			CHA += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Clockwork":
			INT += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Warforged":
			STR += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Modron":
			INT += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Shield Centinel":
			STR += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Origami Spell":
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Effigy":
			CHA += Dice(4)
			STR += Dice(4)

	if npc.race == "Dragon" or npc.race == "Kobold":
		if npc.race == "Dragon":
			STR += Dice(4)
			if "Dragonborn" 	in npc.subrace:
				CHA += Dice(4)
			if "Wyrm" 			in npc.subrace:
				DEX += Dice(4)
			if "Drake" 			in npc.subrace:
				CON += Dice(4)
			if "Draco" 			in npc.subrace:
				STR += Dice(4)
			if "Dragon" 		in npc.subrace:
				STR += Dice(4)
				CON += Dice(4)
				CHA += Dice(4)
			if "Sky Serpent" 	in npc.subrace:
				DEX += Dice(4)
				CON += Dice(4)
				CHA += Dice(4)
			if "Half Dragon" 	in npc.subrace:
				CON += Dice(4)
				CHA += Dice(4)
			if "Dragon Turtle" 	in npc.subrace:
				CON += Dice(4)
				STR += Dice(4)
			if "Centenary" 		in npc.subrace:
				CON += Dice(4)
				INT += Dice(4)
			if "Millenary" 		in npc.subrace:
				WIS += Dice(4)
				INT += Dice(4)
			if "Wyvern" 		in npc.subrace:
				DEX += Dice(4)
				STR += Dice(4)
			if "Long" 			in npc.subrace:
				INT += Dice(4)
				CHA += Dice(4)
			if "Drakon" 		in npc.subrace:
				WIS += Dice(4)
				CHA += Dice(4)
		if npc.race == "Kobold":
			DEX += Dice(4)


		if "Black" 		in npc.subrace:
			CHA += Dice(4)
		if "Blue" 		in npc.subrace:
			INT += Dice(4)
		if "Green" 		in npc.subrace:
			WIS += Dice(4)
		if "Red" 		in npc.subrace:
			STR += Dice(4)
		if "White" 		in npc.subrace:
			DEX += Dice(4)
		if "Bronze" 	in npc.subrace:
			CON += Dice(4)
		if "Silver" 	in npc.subrace:
			INT += Dice(4)
		if "Gold" 		in npc.subrace:
			CHA += Dice(4)
		if "Brass" 		in npc.subrace:
			CHA += Dice(4)
		if "Copper" 	in npc.subrace:
			STR += Dice(4)
		if "Shadow" 	in npc.subrace:
			CHA += Dice(4)
		if "Gem" 		in npc.subrace:
			INT += Dice(4)
		if "Ethereal" 	in npc.subrace:
			INT += Dice(4)
			CHA += Dice(4)
		if "Planar" 	in npc.subrace:
			INT += Dice(4)
			WIS += Dice(4)
		if "Prismatic" 	in npc.subrace:
			INT += Dice(4)
			WIS += Dice(4)
			CHA += Dice(4)

	if npc.race == "Elemental":
		CON += Dice(4)  # Base hardiness for all elementals.
		WIS += Dice(4)  # Base elemental wisdom.

		if npc.subrace == "Atlantian":
			STR += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Chronian":
			DEX += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Cronusian":
			CHA += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Eosian":
			DEX += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Etherian":
			DEX += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Gaian":
			STR += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Galaxian":
			STR += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Genasi":
			DEX += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Genie":
			DEX += Dice(4)
			CON += Dice(4)
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Hyperian":
			DEX += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Magmaforged":
			CHA += Dice(4)
			STR += Dice(4)
		elif npc.subrace == "Oceanians":
			CHA += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Primordial":
			CON += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Promethean":
			CHA += Dice(4)
			INT += Dice(4)
		elif npc.subrace == "Salamandrian":
			CHA += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Nymphian":
			INT += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Sylphians":
			WIS += Dice(4)
			DEX += Dice(4)
		elif npc.subrace == "Pigmians":
			WIS += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Tartarian":
			WIS += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Titan":
			WIS += Dice(4)
			STR += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Tundran":
			WIS += Dice(4)
			CON += Dice(4)
		elif npc.subrace == "Uranians":
			INT += Dice(4)
			CHA += Dice(4)
		elif npc.subrace == "Zephyrian":
			INT += Dice(4)
			WIS += Dice(4)
		elif npc.subrace == "Djinn":
			INT += Dice(4)
			CHA += Dice(4)
			WIS += Dice(4)

	if npc.race == "Fiend":
		CHA += Dice(4)

		if npc.subrace == "Tiefling":
			CHA += Dice(4)
		if npc.subrace == "Devil":
			CHA += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Demon":
			INT += Dice(4)     # Boost to their arcane knowledge.
			WIS += Dice(4)     # For a deeper understanding of magic.
		if npc.subrace == "Imp":
			DEX += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Cubus":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Incubus":
			CHA += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Succubus":
			CHA += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Concubus":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Dwarvendevil":
			CHA += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Elvendevil":
			CHA += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Gnolldevil":
			CHA += Dice(4)
			DEX += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Orkishdevil":
			CON += Dice(4)
			STR += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Goblindevil":
			DEX += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Dwarvendemon":
			CON += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Elvendemon":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Demongnoll":
			DEX += Dice(4)
			STR += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Orkishdemon":
			CON += Dice(4)
			STR += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Goblindemon":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Nightmare":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Rakshasa":
			CON += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Fallen Angel":
			CHA += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Hellbound Hunter":
			WIS += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Leviathan":
			CON += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Behemoth":
			DEX += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Shinigami":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Hell's Rider":
			DEX += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Soul Collector":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Infinder":
			WIS += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Sinvestigator":
			WIS += Dice(4)
			CHA += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Chaoslord":
			STR += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Justiciar":
			STR += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Vengeance Spirit":
			STR += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Retributioner":
			WIS += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Pact Enforcer":
			STR += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Soulclaimer":
			WIS += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Infernal Enforcer":
			WIS += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Inforcer":
			WIS += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Dark Gods":
			WIS += Dice(4)
			CHA += Dice(4)
			INT += Dice(4)
			STR += Dice(4)

	if npc.race == "Fey":
		CHA += Dice(4)

		if npc.subrace == "Hag":
			INT += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Nymph":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Pixie":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Satyr":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Sprite":
			DEX += Dice(4)
			CON += Dice(4)
		if npc.subrace == "High Fae":
			WIS += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Redcap":
			STR += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Leprechaun":
			CHA += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Changeling":
			INT += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Nexus Fey":
			INT += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Duende":
			WIS += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Home Lares":
			WIS += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Fata":
			WIS += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Moira":
			WIS += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Parca":
			WIS += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Archfey":
			WIS += Dice(4)
			INT += Dice(4)
			CON += Dice(4)

	if npc.race == "Giant":
		STR += Dice(4)  # All giants possess enormous strength.
		CON += Dice(4)  # And have a tough constitution.

		if npc.subrace == "Goliath":
			STR += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Firbolg":
			WIS += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Cyclops":
			INT += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Ogre":
			CON += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Troll":
			CON += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Jotunn (Frost Giant)":
			CHA += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Fire Giant":
			CHA += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Gigantes":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Nephilim":
			STR += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Oni":
			CHA += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Ettin (Two headed)":
			CHA += Dice(4)
			INT += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Fomorians (Sea Giants)":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Cloud Giant":
			DEX += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Stone Giant":
			STR += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Storm Giant":
			DEX += Dice(4)
			CON += Dice(4)

	if npc.race == "Gnome":
		DEX += Dice(4)
		INT += Dice(4)
		CHA += Dice(4)


		if npc.subrace == "Mountain":
			STR += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Forest":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Garden":
			CHA += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Tinker":
			INT += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Crossroad":
			INT += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Trickster":
			DEX += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Wandering":
			CON += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Leprechaun":
			INT += Dice(4)
			CHA += Dice(4)
			STR += Dice(4)

	if npc.race == "Goblin":
		DEX += Dice(4)	# For their nimbleness.
		INT += Dice(4) 	# For their cunning and potential for strategy or invention.
		CHA += Dice(4) 	# For their often charismatic nature.

		if npc.subrace == "Goblin":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Hobgoblin":
			STR += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Bugbear":
			STR += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Gremlin (Tecnogoblin)":
			INT += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Redcap":
			STR += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Nyk (Watergoblin)":
			WIS += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Trow (Dark goblin)":
			WIS += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Knocker (Underdark goblin)":
			INT += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Domovoi (House Goblin)":
			INT += Dice(4)
			CHA += Dice(4)

	if npc.race == "Monstrosity":
		STR += Dice(4)
		CON += Dice(4)

		if npc.subrace == "Chimera":
			STR += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Doppelganger":
			CHA += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Shapeshifter":
			CHA += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Gorgon":
			CHA += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Horror":
			CHA += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Sphynx":
			WIS += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Wendigo":
			WIS += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Kraken":
			STR += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Nightmare":
			CHA += Dice(4)
			WIS += Dice(4)

	if npc.race == "Ooze":
		CON += Dice(4)  # Base increase for being amorphous and hard to damage.


		if npc.subrace == "Plasmoid":
			INT += Dice(4)
		if npc.subrace == "Abominational":
			STR += Dice(4)
		if npc.subrace == "Globkin":
			DEX += Dice(4)
		if npc.subrace == "Blobfolk":
			CON += Dice(4)
		if npc.subrace == "Slimeling":
			DEX += Dice(4)
		if npc.subrace == "Gelatoid":
			STR += Dice(4)
		if npc.subrace == "Waxian":
			WIS += Dice(4)
		if npc.subrace == "Adhesians":
			INT += Dice(4)
		if npc.subrace == "Cuborg":
			CHA += Dice(4)

	if npc.race == "Orc":
		STR += Dice(4)  # Base increase due to the general physical prowess of orcs.
		CON += Dice(4)  # Due to their rugged and tough nature.

		if npc.subrace == "Mountain":
			STR += Dice(4)    # Extra physical training and combat experience.
		if npc.subrace == "Desert":
			DEX += Dice(4)
		if npc.subrace == "Swamp":
			WIS += Dice(4)
		if npc.subrace == "Snow":
			CON += Dice(4)
		if npc.subrace == "Uruk":
			STR += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Half-Orc":
			CHA += Dice(4)
		if npc.subrace == "Orog (Underdark)":
			WIS += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Cave":
			WIS += Dice(4)
			STR += Dice(4)
		if npc.subrace == "Forest":
			WIS += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Nomadic":
			CON += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Island":
			INT += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Urbanite":
			INT += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Feral":
			STR += Dice(4)
			WIS += Dice(4)

	if npc.race == "Plant":
		CON += Dice(4)  # Base increase due to the hardiness of plants.

		if npc.subrace == "Willow Guardian":
			STR += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Treant":
			DEX += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Awakened Tree":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Forefather Oak":
			WIS += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Myconid Sovereign":
			CHA += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Ent":
			STR += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Treefolk":
			DEX += Dice(4)
			WIS += Dice(4)
		if npc.subrace == "Floral Walkers":
			DEX += Dice(4)
			INT += Dice(4)
		if npc.subrace == "Living Totem":
			WIS += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Walker Vine":
			DEX += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Singing Lotus":
			CHA += Dice(4)
			DEX += Dice(4)
		if npc.subrace == "Lichen Gravetaker":
			WIS += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Cactoid Nomad":
			DEX += Dice(4)
			CON += Dice(4)
		if npc.subrace == "Vegetation Abomination":
			STR += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Dryad":
			DEX += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Fungical Intellectual":
			INT += Dice(4)
			CHA += Dice(4)
		if npc.subrace == "Myceliumanoid":
			WIS += Dice(4)
			CHA += Dice(4)

	if npc.race == "Undead":
		# Basic stats increase due to the unnatural nature of undead.
		CON += Dice(4)  # Undying nature.
		CHA += Dice(4)  # Eerie presence.

		if npc.subrace == "Cursed Eternal":
			WIS += Dice(4)
		if npc.subrace == "Death Knight":
			STR += Dice(4)
		if npc.subrace == "Despair Specter":
			CHA += Dice(4)
		if npc.subrace == "Fear Shadow":
			INT += Dice(4)
		if npc.subrace == "Honor Phantom":
			CHA += Dice(4)
		if npc.subrace == "Lich":
			INT += Dice(4)
		if npc.subrace == "Mischief Poltergeist":
			CHA += Dice(4)
		if npc.subrace == "Penance Wraith":
			WIS += Dice(4)
		if npc.subrace == "Pride Mummy":
			CHA += Dice(4)
		if npc.subrace == "Protector Spirit":
			STR += Dice(4)
		if npc.subrace == "Regreting Ghost":
			INT += Dice(4)
		if npc.subrace == "Skeleton Protector":
			CON += Dice(4)
		if npc.subrace == "Thinker Skull":
			INT += Dice(4)
		if npc.subrace == "Tomb's Hoarder":
			CHA += Dice(4)
		if npc.subrace == "Vengeful Revenant":
			DEX += Dice(4)
		if npc.subrace == "Weeping Howler":
			WIS += Dice(4)
		if npc.subrace == "Wraith":
			STR += Dice(4)
			DEX += Dice(4)
	if npc.race == "Vampire":
		INT += Dice(4)
		WIS += Dice(4)
		CHA += Dice(4)
		DEX += Dice(4)

	if npc.race == "Elf":
		DEX += Dice(4)  # Elves are commonly known for their agility and grace.
		if Dice(4) == 1: STR += Dice(4)  # Some elves could be stronger, especially if they're warrior-types.
		if Dice(4) == 1: DEX += Dice(4)  # Dextrous and agile.
		if Dice(4) == 1: CON += Dice(4)  # Rarely, an elf might have more physical hardiness.
		if Dice(4) == 1: INT += Dice(4)  # Their long lifespans allow them to accumulate knowledge.
		if Dice(4) == 1: WIS += Dice(4)  # Representing their inherent connection to the world and ancient wisdom.
		if Dice(4) == 1: CHA += Dice(4)  # Many elves possess a natural charisma and allure.

	if npc.race == "Halfling": # Hobbits
		CHA += Dice(4)  # Known for their natural charm.
		if Dice(4) == 1: STR += Dice(4)  # They can take on any rival.
		if Dice(4) == 1: DEX += Dice(4)  # They can be quick and nimble.
		if Dice(4) == 1: CON += Dice(4)  # No sleep 'till... Mordor!
		if Dice(4) == 1: INT += Dice(4)  # No riddle is too hard.
		if Dice(4) == 1: WIS += Dice(4)  # Attentive to their gardens.
		if Dice(4) == 1: CHA += Dice(4)  # Friendship can compel any Company.

	if npc.race == "Dwarf":
		CON += Dice(4)  # Known for their hardiness.
		if Dice(4) == 1: STR += Dice(4)  # For their natural strength.
		if Dice(4) == 1: DEX += Dice(4)  # Some dwarves might be surprisingly agile.
		if Dice(4) == 1: CON += Dice(4)  # No Mead is too hard.
		if Dice(4) == 1: INT += Dice(4)  # Some could be especially knowledgeable or clever.
		if Dice(4) == 1: WIS += Dice(4)  # For their accumulated knowledge and wisdom.
		if Dice(4) == 1: CHA += Dice(4)  # A few dwarves might have a notably commanding or charismatic presence.

	if npc.race == "Lizardfolk":
		STR += Dice(4)  # Lizardfolk are big and sturdy.
		if Dice(4) == 1: STR += Dice(4)  # Some Lizardfolk could be stronger, especially if they're warrior-types.
		if Dice(4) == 1: DEX += Dice(4)  # Dextrous and agile.
		if Dice(4) == 1: CON += Dice(4)  # Some are specially sturdy.
		if Dice(4) == 1: INT += Dice(4)  # They can be very logical, analytical, and calculating.
		if Dice(4) == 1: WIS += Dice(4)  # In tune with their environments.
		if Dice(4) == 1: CHA += Dice(4)  # Frightening presence.

	if npc.race == "Snakefolk":
		CHA += Dice(4)  # Snakefolk are scary and alluring both at the same time.
		if Dice(4) == 1: STR += Dice(4)  # Some snakes can be very strong.
		if Dice(4) == 1: DEX += Dice(4)  # Dextrous and agile.
		if Dice(4) == 1: CON += Dice(4)  # Some are quite sturdy.
		if Dice(4) == 1: INT += Dice(4)  # Capable of great schemes and plans.
		if Dice(4) == 1: WIS += Dice(4)  # In tune with their environments.
		if Dice(4) == 1: CHA += Dice(4)  # Frightening presence.

	npc.AS.STR = STR
	npc.AS.DEX = DEX
	npc.AS.CON = CON
	npc.AS.INT = INT
	npc.AS.WIS = WIS
	npc.AS.CHA = CHA


Marine_Subraces = ["Swamp Crocfolk",	"Sea Elf", "Kraken", "Nyk (Watergoblin)", "Fomorians (Sea Giants)", "Nymph", "Nymphian",	"Oceanians",	"Gaian",	"Atlantian",	"Merfolk","Sharkfolk", "Aboleth", "Old One", "Depth Dominators", "Star Whale", "Kaiju Dinosaur"]
