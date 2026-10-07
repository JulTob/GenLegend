# Compass of Biomas

# Biome: Mapping and Coloring
import app.random as random
from time import time_ns
from random import choices
from AtlasOfMapmaking.Kit_of_HandDrawing import add_edge_shading, add_parchment_background, add_hand_drawn_filter, add_icon_filter, handdrawn_emoji
from AtlasNomina.Map_of_Names import NamesList, Phonotactic, SurnamesList, SurPhonotactic, NewWord
from AtlasEpica.Map_of_Titles import Descriptor, Rank, Title
from AtlasAlusoris.Map_of_Races  		import Race
from AtlasAlusoris.Map_of_Archetypes	import Archetype
from AtlasActorLudi.Map_of_Gender  		import NewGender

def Namer(lusor):
	#print("Name Builder Initiated")

	names = NamesList(lusor)
	o, n, c = Phonotactic(lusor)
	try:
		result = map_rng.choice(names)
	except:
		result = NewWord(
				names = names,
				onset = o,
				nuclei = n,
				codas = c,
				)
	while len(result) < 3:
		result = NewWord(
				names = names,
				onset = o,
				nuclei = n,
				codas = c,
				)
	return result.capitalize()

def Surnamer(lusor):
	#print("Name Builder Initiated")
	names = SurnamesList(lusor)
	o, n, c = SurPhonotactic(lusor)
	try:
		result = map_rng.choice(names)
	except:
		try:
			result = NewWord(
				names = names,
				onset = o,
				nuclei = n,
				codas = c,
				)
		except:
			result = Namer(lusor)
	while len(result)< 3:
			result = NewWord(
				names = names,
				onset = o,
				nuclei = n,
				codas = c,
				)
	return result.capitalize()

map_rng = random.Random()  # Independent RNG for map features
map_rng.seed(time_ns())

class NPC():
	def __init__(npc, race = None, archetype = None):
		npc.seed = map_rng.randint(0,2**32-1)
		if race is None: npc.race = Race()
		else: npc.race = race
		npc.subrace = ""
		npc.alignment = ""
		npc.gender =   NewGender()
		if archetype is None: npc.archetype = Archetype()
		else: npc.archetype = 	archetype

	@property
	def genus(npc):
		attributes = [
			npc.race,
			npc.archetype]
		return attributes


# Biomes and their colors

class Biomes:
	"""Mapping of heights to biomes and their colors."""
	BIOMES = {
		"Hell": (float("-inf"), -20),
		"Underdark": (-20, -15),
		"Sea": (-15, -6),
		"Water": (-6, 1),
		"Sand": (1, 10),
		"Plains": (10, 20),
		"Forest": (20, 30),
		"Mountain": (30, 40),
		"Snow": (40, float("inf")),
		}

	@staticmethod
	def list_all():
		"""Return a list of all biome names."""
		return list(Biomes.BIOMES.keys())

	@staticmethod
	def color(biome):
		return Color(biome)  # Default to black

	@staticmethod
	def height_to_biome(height):
		"""Map a height value to a biome."""
		for biome, (min_h, max_h) in Biomes.BIOMES.items():
			if min_h <= height < max_h:
				return biome
		return "Water"

	@staticmethod
	def select_icon(biome):
		"""Select a random icon for the given biome."""
		return Icons(biome)

def extract(items,weights):
	return map_rng.choices(items, weights=weights, k=1)[0]

def Color(biome):
		SEA_COLOR = 		"#4073B3"
		SEA_COLOR2 = 		"#379CD6"
		SEA_COLOR3 = 		"#1034A6"
		WATER_COLOR = 		"#1E97F2"
		WATER_COLOR2 = 		"#379CD6"
		SAND_COLOR = 		"#FF9966"
		SAND_COLOR2 = 		"#EDC9AF"
		SAND_COLOR3 = 		"#D99376"
		SAND_COLOR4 = 		"#F0DB7D"
		PLAINS_COLOR = 		"#7FB238"
		PLAINS_COLOR2 = 	"#78CC48"
		PLAINS_COLOR3 = 	"#C7D454"
		PLAINS_COLOR4 = 	"#3F9B0B"
		FOREST_COLOR = 		"#007C00"
		FOREST_COLOR2 = 	"#2A7E19"
		FOREST_COLOR3 = 	"#66B58F"
		MOUNTAIN_COLOR = 	"#976D4D"
		MOUNTAIN_COLOR2 = 	"#86483C"
		MOUNTAIN_COLOR3 = 	"#959396"
		SNOW_COLOR = 		"#D6FFFA"
		UNDERDARK_COLOR = 	"silver"
		UNDERDARK_COLOR2 = 	"violet"
		HELL_COLOR = 		"#993333"
		HELL_COLOR2 = 		"#C5C52C"

		if biome == "Sea":
			return extract(
				[SEA_COLOR , SEA_COLOR2],
				[8,				1])
		if biome == "Water":
			return 	extract(
				[WATER_COLOR , WATER_COLOR2],
				[8,				1])
		if biome == "Sand":
			return  extract(
				[SAND_COLOR , SAND_COLOR2, SAND_COLOR3, SAND_COLOR4],
				[8,				1, 		1,			1])
		if biome == "Plains":
			return  extract(
				[PLAINS_COLOR , PLAINS_COLOR2, PLAINS_COLOR3, PLAINS_COLOR4],
				[8,				1, 		1,			1])
		if biome == "Forest":
			return 	extract(
				[FOREST_COLOR , FOREST_COLOR2,	FOREST_COLOR3],
				[8,				5,	1])

		if biome == "Mountain":
			return 	extract(
				[MOUNTAIN_COLOR , MOUNTAIN_COLOR2,	MOUNTAIN_COLOR3],
				[8,				5,	1])

		if biome == "Snow":
			return SNOW_COLOR
		if biome == "Underdark":
			return extract(
				[UNDERDARK_COLOR , UNDERDARK_COLOR2],
				[8,				1])
		if biome == "Hell":
			return extract(
				[HELL_COLOR, 	HELL_COLOR2],
				[8,				1])
		return WATER_COLOR

def Icons(biome):
	"""Handles icons and generates corresponding names for each biome."""
	if biome == "Plains":
		icons = [
			('𓄶', 1, lambda:  f"The Tower {Rank(NPC())}"),
			('𓄷', 1, lambda:  f"The {Rank(NPC())} Tower"),
			('𖬷', 1, lambda:  f"{Rank(NPC())} Way"),
			('༼𝄡༽', 1, lambda:  f"Library of {Title(NPC(archetype = 'Scholar'))}"),
			('༼🜌༽', 1, lambda:  f"{Descriptor(NPC(archetype = 'Scholar'))} Library"),
			('༼⏣༽', 1, lambda:  f"{Descriptor(NPC(archetype = 'Scholar'))} Library"),
			('༼⚚༽', 1, lambda:  f"{Descriptor(NPC(archetype = 'Scholar'))} Library"),
			('༼𖫑༽', 1, lambda:  f"{Rank(NPC(archetype = 'Scholar'))} Library"),
			("𖤘", 2, lambda:  f"Town of {Namer(NPC())}"),
			("𖤘𞀏", 2, lambda:  f"{Namer(NPC())} Town"),
			("𖠿", 2, lambda:  f"{Descriptor(NPC())}town"),
			("𖡪", 2, lambda:  f"{Descriptor(NPC())}ville"),
			("⌂", 2, lambda:  f"Town of {Surnamer(NPC())}"),
			("⌂", 2, lambda:  f"{Surnamer(NPC())} Town"),
			("⛫", 1, lambda:  f"The {Descriptor(NPC())} City"),
			("⛫", 1, lambda:  f"{Surnamer(NPC())} City"),
			("⚜", 3, lambda:  f"The {Descriptor(NPC())} Castle"),
			("⚔", 1, lambda:  f"Fortress of {Title(NPC())}"),
			("⛩", 2, lambda:  f"Shrine of {Title(NPC())}"),
			("𖠿", 2, lambda:  f"{Surnamer(NPC())} Town"),
			("⌂", 2, lambda:  f"{Surnamer(NPC())} Town"),
			("⌂", 2, lambda:  f"{Namer(NPC())} Town"),
			("⌂", 2, lambda:  f"{Descriptor(NPC())} Town"),
			("⌂", 2, lambda:  f"{Descriptor(NPC())}town"),
			("⛫", 1, lambda:  f"The {Descriptor(NPC())} City"),
			("⛫", 1, lambda:  f"{Surnamer(NPC())} City"),
			("⛫", 1, lambda:  f"{Namer(NPC())} City"),
			("⚜", 3, lambda:  f"The {Descriptor(NPC())} Castle"),
			("⚜", 3, lambda:  f"The Castle of the {Rank(NPC())}"),
			("⚜", 3, lambda:  f"The Castle of {Title(NPC())}"),
			("⚔", 1, lambda:  f"Fortress of the {Rank(NPC())}"),
			("⚔", 1, lambda:  f"Fortress of {Title(NPC())}"),
			("𐘜", 1, lambda:  f"Swords of {Title(NPC())}"),
			("⛩", 2, lambda:  f"Shrine of {Title(NPC())}"),
			("⚚", 2, lambda:  f"Sanctum of {Title(NPC())}"),
			("⚖", 1, lambda:  f"Market of {Title(NPC())}"),
			("⛨", 2, lambda:  f"{Descriptor(NPC())} Watchtower"),
			("⚔", 1, lambda:  f"Fortress of {Rank(NPC())}"),
			("۞", 1, lambda:  f"Fortress of \n{Title(NPC())}"),
			("✵", 2, lambda:  f"Camp of {Surnamer(NPC())}"),
			("🜲", 1, lambda:  f"Ruins of \n{Title(NPC())}"),
			("⚅", 1, lambda:  f"Dungeon of {Namer(NPC())}"),
			("⚄", 1, lambda:  f"Dungeon of \n{Title(NPC())}"),
			("𓉱", 2, lambda:  f"Sanctuary of \n{Title(NPC())}"),
			("☭", 1, lambda:  f"Mill town of {Surnamer(NPC())}"),
			("♞", 1, lambda:  f"Rest of {Namer(NPC())}"),
			("⚐", 2, lambda:  f"Banner of {Rank(NPC())}"),
			("𓄇", 2, lambda:  f"Beasts of \n{Title(NPC())}"),
			("𝜗", 2, lambda:  f"{Descriptor(NPC())} Crossing"),
			("♔", 2, lambda:  f"Castle of {Title(NPC())}"),
			("♝", 1, lambda:  f"{Descriptor(NPC())} Magetower"),
			("♝̂", 1, lambda:  f"{Descriptor(NPC())}tower"),
			("♗", 1, lambda:  f"{Descriptor(NPC())} Warlocktower"),
			("♗̂", 1, lambda:  f"{Descriptor(NPC())} Wizardtower"),
			("♖", 1, lambda:  f"{Rank(NPC())} Keep"),
			("♖̅", 1, lambda:  f"{Rank(NPC())}keep"),
			("♖̂", 1, lambda:  f"{Rank(NPC())} Fortress"),
			("𝛿", 2, lambda:  f"{Descriptor(NPC())} Guardians"),
			("⚜", 2, lambda:  f"Throne of {Title(NPC())}"),
			("⚜", 2, lambda:  f"{Descriptor(NPC())} Thrones"),
			("⚜", 2, lambda:  f"{Descriptor(NPC())} Throne"),
			("⚜", 2, lambda:  f"{Rank(NPC())} Thrones"),
			("⚜", 2, lambda:  f"{Rank(NPC())} Throne"),
			("𓅃", 1, lambda:  f"Lands of {Title(NPC(archetype='Ranger'))}"),
			("𓏢", 1, lambda:  f"Fields of {Title(NPC())}"),
			("♝", 1, lambda:  f"Chapel of {Namer(NPC())}"),
			("𐂐", 1, lambda:  f"{Descriptor(NPC())} Ruins"),
			("⚚", 1, lambda:  f"Crossroads of {Title(NPC())}"),
			("𓃬", 1, lambda:  f"Beast of \n{Title(NPC(race = 'Beast'))}"),
			("𓃬", 1, lambda:  f"{Descriptor(NPC(race = 'Beast'))} Beast"),
			("𓇬", 1, lambda:  f"{Descriptor(NPC())}lands"),
			("🜲", 1, lambda:  f"{Descriptor(NPC())} Kingdom"),
			("𑣿", 1, lambda:  f"{Descriptor(NPC())}fields"),
			("𐘢", 1, lambda:  f"{Descriptor(NPC())} Keep"),
			("⛿", 1, lambda:  f"{Descriptor(NPC())} Outpost"),
			("𐁊", 1, lambda:  f"{Descriptor(NPC())} Outpost"),
		]
	elif biome == "Underdark":
		icons = [
			("⚒", 3, lambda:  f"Mines of {Title(NPC(race='Dwarf'))}"),
			("⛏", 3, lambda:  f"{Descriptor(NPC(race='Dwarf'))} Mines"),
			("۞", 1, lambda:  f"Mines of {Namer(NPC())}"),
			("🜃", 1, lambda:  f"Mines of {Surnamer(NPC())}"),
			("⛮", 3, lambda:  f"Forge of {Title(NPC(race='Dwarf'))}"),
			("𐁗", 3, lambda:  f"{Descriptor(NPC())}forge"),
			("᯼", 2, lambda:  f"Labyrinth of {Title(NPC())}"),
			("◈", 2, lambda:  f"Vault of {Surnamer(NPC())}"),
			("▤", 2, lambda:  f"Cave of {Title(NPC(race='Beast'))}"),
			("⟡", 1, lambda:  f"Chamber of {Title(NPC())}"),
			("▣", 2, lambda:  f"Abyss of {Title(NPC())}"),
			("⧈", 1, lambda:  f"Burrows of {Namer(NPC())}"),
			("ℿ", 2, lambda:  f"Crypt of {Descriptor(NPC())}"),
			("❒", 2, lambda:  f"Undergrounds of {Title(NPC())}"),
			("▓", 1, lambda:  f"Prison of {Title(NPC())}"),
			("⏣", 1, lambda:  f"Hall of {Title(NPC())}"),
			("⌓", 2, lambda:  f"Cavern of {Surnamer(NPC())}"),
			("⋇", 2, lambda:  f"Temple of {Descriptor(NPC())}"),
			("𐚄", 1, lambda:  f"Altar of {Title(NPC())}"),
			("𐜧", 1, lambda:  f"Pit of the {Rank(NPC())}"),
			("𐜯", 2, lambda:  f"Throne of {Title(NPC())}"),
			("𐛗", 1, lambda:  f"Chasm of {Descriptor(NPC())}"),
			("𐘜", 2, lambda:  f"{Rank(NPC())} Outpost"),
			("𐘥", 2, lambda:  f"{Descriptor(NPC())} Crystals"),
			("𐚲", 1, lambda:  f"Lair of {Title(NPC())}"),
			("𖦺", 1, lambda:  f"{Descriptor(NPC(race='Fiend'))} Shrine of the {Rank(NPC(race='Fiend'))}"),
			("⦻", 2, lambda:  f"Catacomb of {Title(NPC())}"),
			("𐙛", 1, lambda:  f"Ruins of {Surnamer(NPC())}"),
			("⧈", 2, lambda:  f"Stronghold of the {Rank(NPC())}"),
			("𐘿", 1, lambda:  f"Echoes of {Title(NPC())}"),
			("⧊", 1, lambda:  f"{Descriptor(NPC())} Darkness"),
			("𐁝", 2, lambda:  f"Vault of {Title(NPC())}"),
			("⧞", 1, lambda:  f"Grave of the {Rank(NPC())}"),
		("⧬", 2, lambda:  f"Domain of {Title(NPC(race='Demon'))}"),
			("𐂋", 1, lambda:  f"Nest of {Descriptor(NPC(race='Verminhive'))}"),
			("🝖", 2, lambda:  f"Tunnels of {Rank(NPC())}"),
			("𓍴", 1, lambda:  f"Sepulcher of {Title(NPC())}"),
			("𖡦", 1, lambda:  f"Ruined City of {Surnamer(NPC())}"),
			("𖡵", 2, lambda:  f"Underground Citadel of {Rank(NPC())}"),
			("𖡈", 1, lambda:  f"{Descriptor(NPC())} Reliquary"),
			("𖠌", 2, lambda:  f"Abyssal Gate of {Title(NPC(race='Demon'))}"),
			("𖠷", 1, lambda:  f"Spire of {Surnamer(NPC())}"),
			("𖡪", 1, lambda:  f"Observatory of {Descriptor(NPC())}"),
		("𞠡", 2, lambda:  f"Shrine of {Title(NPC())}"),
		("𞢍", 1, lambda:  f"Pit of the {Rank(NPC())}"),
		("⏚", 2, lambda:  f"Dungeon of {Title(NPC())}"),
		("⛉", 1, lambda:  f"Outpost of the {Rank(NPC())}"),
		("⛊", 1, lambda:  f"Fort of {Title(NPC())}"),
		("⛓", 2, lambda:  f"Prison of {Title(NPC(race='Fiend'))}"),
		("⛭", 1, lambda:  f"Workshop of the {Rank(NPC(race='Dwarf'))}"),
		("⛯", 1, lambda:  f"Forge of {Title(NPC(race='Fiend'))}"),
		("𖡨", 2, lambda:  f"{Rank(NPC(race='Fiend'))} Forge"),
		("⍉", 2, lambda:  f"{Descriptor(NPC())} Chamber"),
		("⛋", 1, lambda:  f"Vault of the {Rank(NPC())}")

		]
	elif biome == "Sea":
		icons = [
			("𐋋", 2, lambda: f"The {Descriptor(NPC())} Shark"),
			("ᯤ", 2, lambda: f"{Descriptor(NPC())}water"),
			("𖭜", 2, lambda: f"{Descriptor(NPC())} Seas"),
			("♒︎", 2, lambda: f"{Descriptor(NPC())} Sea"),
			("﹌", 2, lambda: f"Sea of the {Rank(NPC())}"),
			("𓆨", 3, lambda:  f"{Descriptor(NPC(race='Beast'))} Monster"),
			("♒︎", 2, lambda:  f"Sea of the {Descriptor(NPC())}"),
			("﹌", 2, lambda:  f"Sea of the {Rank(NPC())}"),
			("𓆨", 3, lambda:  f"Monster of {Surnamer(NPC(race='Beast'))}"),
			("𓆉", 2, lambda:  f"Turtle Island of {Surnamer(NPC())}"),  # Turtle
			("♆", 2, lambda:  f"Domain of {Title(NPC(race='Merfolk'))}"),  # Poseidon/Neptune trident
			("⛵︎", 2, lambda:  f"Shipwreck of {Namer(NPC())}"),  # Sailing ship
			("𖠳", 2, lambda:  f"Ships of {Namer(NPC())}"),  # Sailing ship
			("꩜", 1, lambda:  f"Whirlpool of {Descriptor(NPC())}"),
			("𓆡", 3, lambda:  f"Roaming Island of {Surnamer(NPC())}"),  # Fish
			("﹋", 2, lambda:  f"Reefs of {Title(NPC())}"),
			("﹏", 2, lambda:  f"Seaway of {Namer(NPC())}"),  # Wave
			("⚔", 1, lambda:  f"{Title(NPC())} Fleet"),
			("⚔", 1, lambda:  f"{Rank(NPC())} Floating Fortress"),
			("꥟", 1, lambda:  f"{Descriptor(NPC())} Mist"),  # Mystical sea
			("⎈", 2, lambda:  f"Trade Route of {Namer(NPC())}"),  # Helm
			("〰", 2, lambda:  f"Tides of {Surnamer(NPC())}"),
			("𓆢", 1, lambda:  f"Kraken"),
			("𖤓", 2, lambda:  f"Isle of {Title(NPC())}"),
			("∽", 1, lambda:  f"{Descriptor(NPC())} Sirens"),
			("～", 1, lambda:  f"Gulf of {Surnamer(NPC())}"),
			("∿", 1, lambda:  f"Tides of {Rank(NPC())}"),
			("𓆜", 2, lambda:  f"Shallows of {Descriptor(NPC())}")
		  ]
	elif biome == "Water":
		icons = [
			("☠", 3, lambda:  f"{Descriptor(NPC(archetype='Pirate'))} Port"),
			("⚓︎", 2, lambda:  f"Dock of {Namer(NPC())}"),
			("𓊝", 2, lambda:  f"Ships of \n{Title(NPC())}"),
			("𓊝", 2, lambda:  f"Ship of \n{Namer(NPC())}"),
			("☠", 3, lambda:  f"Port of {Title(NPC(archetype='Pirate'))}"),
			("⚓︎", 2, lambda:  f"Docks of {Namer(NPC())}"),
			("𓊝", 2, lambda:  f"Float of {Title(NPC())}"),
			("⛵︎", 2, lambda:  f"Ships of {Surnamer(NPC())}"),
			("Ѱ", 2, lambda:  f"{Descriptor(NPC())} Trench"),  # Psi-like wave
			("ѱ", 2, lambda:  f"Deeps of the {Rank(NPC())}"),  # Deep sea area
			("𐀩", 2, lambda:  f"Warships of {Surnamer(NPC())}"),
			("𓃗", 2, lambda:  f"Raiders of the {Rank(NPC())}"),
			("𓆌", 1, lambda:  f"Predators of {Namer(NPC())}"),  # Fishhook
			("~", 2, lambda:  f"{Descriptor(NPC())} Tides"),
			("⁓", 1,  lambda:  f"Channel of {Title(NPC())}"),
			("𓍄", 2,  lambda:  f"Rutes of {Title(NPC(archetype = 'Merchant'))}"),
			("𓆌", 2,  lambda:  f"Beast of {Title(NPC(race = 'Aberration'))}"),
			("〰", 2, lambda:  f"Waves of {Namer(NPC())}"),
			("〜", 1, lambda:  f"{Descriptor(NPC())} Tides"),
			("⚓︎", 1, lambda:  f"Anchor of the {Rank(NPC())} Fleet"),
			("𖤝", 1, lambda:  f"The {Descriptor(NPC())} Shores"),
		]
	elif biome == "Sand":
		icons = [
			("𖡪", 3, lambda:  f"{Descriptor(NPC())} Goblins"),
			("⚕︎", 3, lambda:  f"{Descriptor(NPC())} Temple"),
			("𓅽", 3, lambda:  f"{Descriptor(NPC())} Sphynx"),
			("𓉱", 3, lambda:  f"Temple of the {Descriptor(NPC())}"),
			("𓉸", 3, lambda:  f"Tomb of {Title(NPC())}"),
			("☉", 2, lambda:  f"City of {Namer(NPC())}"),
			("⚰", 2, lambda:  f"Grave of {Surnamer(NPC())}"),
			("𓅂", 1, lambda:  f"Hunters of the {Rank(NPC())}"),
			("𓉱", 3, lambda:  f"Temple of {Title(NPC())}"),
			("𓉸", 3, lambda:  f"Tomb of {Title(NPC())}"),
			("☉", 2, lambda:  f"City of {Namer(NPC())}"),
			("⚰", 2, lambda:  f"Grave of {Surnamer(NPC())}"),
			("𓊅", 2, lambda:  f"Ruins of {Namer(NPC())}"),  # Ancient obelisk
			("𓉐", 2, lambda:  f"Ruins of {Title(NPC())}"),  # Pyramid-like symbol
			("𓉴", 2, lambda:  f"Ruins of the {Descriptor(NPC())}"),  # Oasis symbol
			("𓉶", 2, lambda:  f"Obelisk of the {Rank(NPC())}"),  # Sand dunes
			("𓁹", 1, lambda:  f"Eye of {Surnamer(NPC())}"),  # Eye of Ra/Horus
			("𐀼", 2, lambda:  f"{Descriptor(NPC())} Sanctuary"),  # Trade/merchant symbol
			("𖣲", 1, lambda:  f"Market of {Title(NPC())}"),  # Protection/hidden place
			("ⵥ", 2, lambda:  f"Prison of {Surnamer(NPC())}"),  # North African Berber symbol
			("𓆓", 2, lambda:  f"{Descriptor(NPC())} Pit"),  # Cobra/serpent pit
			("𓆗", 1, lambda:  f"Lair of {Namer(NPC())}"),
			("⚚", 2, lambda:  f"Hermit of the {Rank(NPC())}"),  # Rod of Hermes
			("⛯", 1, lambda:  f"Sands of {Descriptor(NPC())}"),  # Desert fire or forge
			("☥", 2, lambda:  f"Shrine of {Title(NPC())}"),  # Ankh symbol of life
			("𓁀", 1, lambda:  f"Ruined Tomb of {Rank(NPC())}"),  # Journeying pilgrim
			("༄", 1, lambda:  f"{Descriptor(NPC())} Sandstorms"),  # Sandstorm
			("𓋹", 2, lambda:  f"Throne of {Title(NPC())}"),  # Royal power or seat
			("𓆙", 1, lambda:  f"Lair of {Title(NPC(race='Beast'))}"),
			("⚖", 1, lambda:  f"Hall of {Rank(NPC())}"),
			("𐦐", 1, lambda:  f"Temple of {Namer(NPC())}"),
			("𑵿𑶑", 1, lambda:  f"{Rank(NPC())} of the Sands"),
	]
	elif biome == "Forest":
		icons = [

			("𖥍", 1, lambda:  f""),
			("𖭩", 1, lambda:  f"{Descriptor(NPC())}trees"),
			("𖦉", 1, lambda:  f"{Descriptor(NPC())} Forest"),
			("⏾", 3, lambda:  f"Clear of {Title(NPC(archetype='Explorer'))}"),
			("𝍔", 2, lambda:  f"Falls of {Namer(NPC())}"),
			("☘", 2, lambda:  f"Sanctuary of {Title(NPC())}"),
			("⏾⃣", 3, lambda:  f"Clear of the {Rank(NPC())}"),
			("ਲਿੀ", 2, lambda:  f"Grove of {Namer(NPC())}"),
			("☘", 2, lambda:  f"Sanctuary of the {Descriptor(NPC())}"),
			("⚭⃝", 2, lambda:  f"Circle of {Title(NPC(archetype='Druid'))}"),  # Druidic circle
			("⚮", 2, lambda:  f"Grounds of the {Descriptor(NPC())}"),  # Binding ring
			("⚯", 1, lambda:  f"Hunt of {Title(NPC())}"),  # Nature binding
			("𓌖", 1, lambda:  f"Watchtower of {Surnamer(NPC())}"),  # Dense tree cover
			("𓅓", 1, lambda:  f"Parliament of {Title(NPC(race='Aven'))}"),  # Bird/tree-related
			("☾", 1, lambda:  f"Glade of {Descriptor(NPC())}"),  # Night glade
			("☽", 1, lambda:  f"Grove of the {Rank(NPC())} Moon"),  # Celestial ties
			("∏", 2, lambda:  f"Shrine of {Namer(NPC())}"),  # Forest hollow
			("𐘃", 1, lambda:  f"Tree of {Title(NPC())}"),  # Ancient forest guardians
			("𓃵", 1, lambda:  f"Forest of the {Descriptor(NPC())}"),  # Animal dens
			("𐦉", 1, lambda:  f"Parliament of {Title(NPC())}"),
			("♧", 2, lambda:  f"Feywilds of the {Rank(NPC())}"),
			("⚧", 2, lambda:  f"Portal of \n{Title(NPC())}"),
			("⚬", 2, lambda:  f"Spring of {Surnamer(NPC())}"),  # Water spring or sacred source
			("⚝", 1, lambda:  f"Fairy Ring of {Namer(NPC())}"),  # Mystical and hidden area
			("△", 1, lambda:  f"Trail of {Title(NPC())}"),  # Path through woods
			("⛩", 1, lambda:  f"Arch of {Descriptor(NPC())}"),  # Spirit gateway
			("𓃲", 1, lambda:  f"Forest of {Title(NPC(race='Beast'))}"),
			("⛻", 1, lambda:  f"Forest of {Title(NPC())}"),  # Gate to mystical glades
			("𐘃", 1, lambda:  f"Woods of the {Rank(NPC())}"),
			("𓊆𓊇", 1, lambda:  f"Circle of the {Descriptor(NPC(archetype = 'Druid'))}"),
			("♧", 1, lambda:  f"{Rank(NPC())}wood"),
			("𑜍", 1, lambda:  f"{Rank(NPC())}camp"),
			("𖠘", 1, lambda:  f"{Descriptor(NPC())} Camp"),
			("𖧨", 1, lambda:  f"{Descriptor(NPC())} Settlement"),
			("𐙷", 1, lambda:  f"Wardens of {Title(NPC())}"),

			]
	elif biome == "Mountain":
		icons = [
				('༼۞༽', 2, lambda:  f"Library of {Title(NPC(archetype = 'Scholar'))}"),
				('༼𝛀༽', 2, lambda:  f"Library of {Title(NPC(archetype = 'Scholar'))}"),
				('༼࿄༽', 2, lambda:  f"{Descriptor(NPC(archetype = 'Scholar'))} Library"),
				('༼𖤍༽', 2, lambda:  f"{Descriptor(NPC(archetype = 'Scholar'))} Library"),
				('༼𝚿༽', 2, lambda:  f"{Descriptor(NPC(archetype = 'Scholar'))} Library"),
				("㊥", 3, lambda:  f"Temple of \n{Title(NPC(race='Dragon'))}"),
				("⚒", 2, lambda:  f"Mine of {Surnamer(NPC())}"),
				("⛰️", 2, lambda:  f"Peak of {Title(NPC())}"),
				("⛏", 2, lambda:  f"Cliff of {Namer(NPC())}"),
				 ("༼۩༽", 2, lambda:  f"Monastery of {Title(NPC(archetype='Monk'))}"),  # Sacred mountain temple
				("✠", 2, lambda:  f"Crag of {Rank(NPC())}"),  # Knightly stronghold
				("⛫⃣", 10, lambda:  f"Citadel of the {Descriptor(NPC())}"),  # Citadel atop peaks
				("⚒", 2, lambda:  f"Mine of {Surnamer(NPC())}"),  # Dwarf-like mine
				("ᨏ", 2, lambda:  f"Peaks of {Title(NPC())}"),  # Summit or high point
				("⛏", 2, lambda:  f"Mine of {Namer(NPC())}"),  # Sheer cliffs or dangerous zones
				("☸", 1, lambda:  f"Shrine of the {Rank(NPC())}"),  # Symbolic monk shrine
				("☯", 1, lambda:  f"Temple of {Title(NPC())}"),  # Yin-yang balance temple
				("ᛝ", 2, lambda:  f"Sanctuary of {Title(NPC(race='Giant'))}"),  # Giant sanctuaries
				("ᛤ", 1, lambda:  f"Forge of {Title(NPC(race='Dwarf'))}"),  # Sacred dwarven forges
				("⧍", 2, lambda:  f"Caves of {Surnamer(NPC())}"),  # Triple mountain peaks
				("⧊", 2, lambda:  f"Cave of {Namer(NPC())}"),  # Hidden cave
				("◬", 1, lambda:  f"Pillar of {Descriptor(NPC())}"),  # Sharp rising formations
				("⌃", 1, lambda:  f"Summit of {Rank(NPC())}"),  # Summit sanctuaries
				("𓊎", 2, lambda:  f"Hermitage of {Title(NPC())}"),  # Remote hermit locations
				("𐃈", 1, lambda:  f"Highlands of {Namer(NPC())}"),  # Large mountainous region
				("⚏", 1, lambda:  f"Cliffs of {Descriptor(NPC())}"),  # Dangerous cliff edges
				("⚒", 2, lambda:  f"Stones of {Surnamer(NPC())}"),  # Large rock extractions
				("⛰", 1, lambda:  f"Mountain of {Title(NPC())}"),  # Default mountain
				("࿊", 1, lambda:  f"Monastery of {Descriptor(NPC())}"),  # High-altitude temples
				("⚗", 1, lambda:  f"Wizardtower of {Surnamer(NPC())}"),  # Alchemy/mysticism at mountain tops
				("𑁍", 2, lambda:  f"Hermits of the {Rank(NPC())}"),  # Hard-to-find routes
				("☯︎", 1, lambda:  f"Celestial Peak of {Descriptor(NPC())}"),  # Monk and celestial related peaks
				("⎔", 1, lambda:  f"Lights of {Title(NPC())}"),  # Sacred stone rings at summits
				("⋀", 2, lambda:  f"Twin Peaks of {Surnamer(NPC())}"),  # Twin peaks or linked formations
				("∧", 2, lambda:  f"Spire of {Title(NPC())}"),  # Tall single mountain spires
				("⌬", 1, lambda:  f"{Descriptor(NPC())} Tower"),  # Alchemical/mystic circle
				("ᚼ", 1, lambda:  f"Ridge of {Title(NPC())}"),  # High ridges
				("⚐", 1, lambda:  f"Fortress of {Namer(NPC())}"),  # Old mountain meeting places
				("⚖", 1, lambda:  f"Market of the {Rank(NPC())}"),  # Sites of judgment
				("⚝", 1, lambda:  f"Crater of {Surnamer(NPC())}"),  # Meteorite/magical peaks
				("⛰̃", 2, lambda:  f"Volcano of the {Descriptor(NPC())}"),  # Volcanic mountains
				("⛊", 1, lambda:  f"Fortress of the {Rank(NPC())}"),
				("ᜈ", 1, lambda:  f"{Rank(NPC())} Caves"),
				("ᨃᨚ", 1, lambda:  f"{Descriptor(NPC())} Horn"),
				("𐀋", 1, lambda:  f"{Descriptor(NPC())}stone"),
				("∆", 1, lambda:  f"{Descriptor(NPC())}rock"),
				("♔", 1, lambda:  f"{Descriptor(NPC())} Kings"),
				("♚", 1, lambda:  f"{Rank(NPC())} Kings"),
				("♛", 1, lambda:  f"{Descriptor(NPC())} Queens"),
				("♕", 1, lambda:  f"{Rank(NPC())} Queens"),
				("♔", 1, lambda:  f"{Descriptor(NPC())} King"),
				("♚", 1, lambda:  f"{Rank(NPC())} King"),
				("♛", 1, lambda:  f"{Descriptor(NPC())} Queen"),
				("♕", 1, lambda:  f"{Rank(NPC())} Queen"),
				("ꥃ", 1, lambda:  f"{Descriptor(NPC())}rock"),
				("ꤼ", 1, lambda:  f"{Descriptor(NPC())}hill"),
				("🀄︎", 1, lambda:  f"Layer of \n{Title(NPC(race = 'Dragon'))}"),
				]
	elif biome == "Snow":
		icons = [
			("𐁗", 3, lambda:  f"{Descriptor(NPC())}forge"),
			("ᛗ", 3, lambda:  f"Fortress of {Title(NPC(race='Dwarf'))}"),
			("ᛉ", 3, lambda:  f"Fortress of {Title(NPC(race='Giant'))}"),
			("❆", 2, lambda:  f"Snowfield of {Title(NPC())}"),
			("❅", 2, lambda:  f"Ices of {Title(NPC(race='Dwarf'))}"),
			("❆", 3, lambda:  f"Snows of {Descriptor(NPC())}"),
			("𓆍", 2, lambda:  f"Lair of \n{Title(NPC(race='Dragon'))}"),
			("⛫⃣", 1, lambda:  f"{Rank(NPC())} Citadel"),
			("⛊", 2, lambda:  f"{Descriptor(NPC())} Fortress"),
			("⛉", 2, lambda:  f"{Rank(NPC())} Outpost"),  # Cold frontier outpost
			("⛈", 2, lambda:  f"Storms of {Title(NPC())}"),
			("⚒", 3, lambda:  f"Mines of {Surnamer(NPC(race='Dwarf'))}"),
			("♨", 1, lambda:  f"Hot Springs of {Surnamer(NPC())}"),
			("△", 2, lambda:  f"{Descriptor(NPC())} Glacial"),  # Frozen mountain ridges
			("ʘ", 1, lambda:  f"{Rank(NPC())} Blizzards"),  # Eye-shaped symbol
			("☁", 1, lambda:  f"Clouds of {Namer(NPC())}"),
			("🜁", 2, lambda:  f"Lake of {Title(NPC())}"),  # Symbolic frozen body of water
			("🜍", 1, lambda:  f"Ruins of the {Rank(NPC())}"),  # Cold-burning region
			("⟐", 2, lambda:  f"{Descriptor(NPC())} Monastery"),  # Mystic icy temple
			("♕", 2, lambda:  f"Capital of {Title(NPC())}"),  # Snow-king ruler
			("🜎", 1, lambda:  f"Prison of {Title(NPC())}"),  # Trapped entities in ice
			("🝟", 1, lambda:  f"Silence of {Surnamer(NPC())}"),  # Unending snowy plains
			("🜾", 2, lambda:  f"Springs of {Namer(NPC())}"),  # Frozen waterfall area
			("⛰", 1, lambda:  f"{Descriptor(NPC())} Peak"),
			("ᛗ", 2, lambda:  f"Bastion of {Title(NPC(race='Dwarf'))}"),  # Dwarven fortress in the snow
			("ᛉ", 2, lambda:  f"Fortress of {Title(NPC(race='Giant'))}"),
			("☾", 1, lambda:  f"{Descriptor(NPC())} Glacier"),  # Magical and icy at night
			("☽", 1, lambda:  f"Tundra of the {Rank(NPC())}"),
			("⚔", 1, lambda:  f"Forges of {Rank(NPC())}"),
			("🜏", 1, lambda:  f"Alchemytower of \n{Title(NPC())}"),
			("⚗", 1, lambda:  f"Alchemist {Surnamer(NPC())}"),
			("⊰⊰", 1, lambda:  f"Blizzards of \n{Title(NPC())}"),
			("༄༅", 1, lambda:  f"Lands of \n{Title(NPC())}"),
			("࿓࿔࿔", 1, lambda:  f"{Descriptor(NPC())} Winter"),
			("𑣥", 1, lambda:  f"The Frozen {Rank(NPC())} Winter"),
		]
	elif biome == "Hell":
		icons = [
			("🃟", 4, lambda:  f"{Descriptor(NPC())} Circus"),
			("🃏", 4, lambda:  f"{Descriptor(NPC())} Arena"),
			("⛤", 3, lambda:  f"{Descriptor(NPC(race='Fiend'))} Bastion"),
			("⛧", 3, lambda:  f"Pit of {Descriptor(NPC(race='Fiend'))}"),
			("⚝", 3, lambda:  f"Depths of {Descriptor(NPC(race='Fiend'))}"),
			("🜍", 3, lambda:  f"Inferno of {Descriptor(NPC(race='Fiend'))}"),
			("⚸", 3, lambda:  f"Abyss of {Title(NPC(race='Fiend'))}"),
			("⋇", 3, lambda:  f"Abyss of {Title(NPC(race='Fiend'))}"),
 ("⛥", 2, lambda:  f"Citadel of {Title(NPC(race='Fiend'))}"),
("⛯", 3, lambda:  f"Forge of {Surnamer(NPC(race='Demon'))}"),
("⛢", 2, lambda:  f"{Descriptor(NPC())} Hellgate"),
("⚶", 3, lambda:  f"Purgatory of {Title(NPC())}"),
("⚚", 2, lambda:  f"Cradle of {Rank(NPC(race='Demon'))}"),
("♆", 2, lambda:  f"{Descriptor(NPC(race='Fiend'))} Trident"),
("☠", 3, lambda:  f"Skulls of {Surnamer(NPC(race='Fiend'))}"),
("☢", 2, lambda:  f"Wastes of {Descriptor(NPC())}"),
("☣", 2, lambda:  f"Plague of {Title(NPC())}"),
("⛧", 3, lambda:  f"Keep of {Title(NPC(race='Fiend'))}"),
("⚸", 2, lambda:  f"{Descriptor(NPC())} Chasm"),
("⚵", 3, lambda:  f"Darkstar of {Title(NPC())}"),
("⚴", 2, lambda:  f"Void of {Surnamer(NPC())}"),
("⚳", 3, lambda:  f"Chains of {Descriptor(NPC(race='Demon'))}"),
("⚜", 2, lambda:  f"Throne of {Title(NPC(race='Fiend'))}"),
("♨", 2, lambda:  f"{Descriptor(NPC())} Magma"),
("⚔", 2, lambda:  f"{Rank(NPC())} Citadel"),
("⚔", 2, lambda:  f"Citadel of {Title(NPC())} "),
("⌬", 2, lambda:  f"Rift of {Surnamer(NPC())}"),
("🜎", 2, lambda:  f"Prison of {Title(NPC(race='Fiend'))}"),
("🝁", 3, lambda:  f"Fires of {Rank(NPC())}"),
("♛", 2, lambda:  f"Crown of {Title(NPC())}"),
("☿", 1, lambda:  f"Pit of {Namer(NPC())}"),
("☽", 1, lambda:  f"Dark Moon of {Namer(NPC())}"),
("⚗", 2, lambda:  f"Forge of {Title(NPC())}"),
("℧", 1, lambda:  f"Shrine of the {Descriptor(NPC(race='Demon'))}"),
("⚗", 1, lambda:  f"Furnace of {Surnamer(NPC())}"),
("⚗", 1, lambda:  f"Vault of {Rank(NPC())}"),
("⛤", 3, lambda:  f"Depths of {Title(NPC())}"),
("⍟", 2, lambda:  f"Scars of the {Rank(NPC())}"),
("§", 2, lambda:  f"Accords of {Descriptor(NPC())}")

		]
	else:
		icons = [
			("✗", 1, "Treasure")
		]

	symbols, weights, names = zip(*icons)
	chosen = map_rng.choices(symbols, weights)[0]
	index = symbols.index(chosen)
	# Generate the name **only** for the selected icon
	name = names[index]()


	return chosen, name.title()


def HandDrawnEmoji(biome):
	if biome == "Sea":
		emoji = "🌊"
	elif biome == "Water":
		emoji = "🏝️"
	elif biome == "Sand":
		emoji = "🐫"
	elif biome == "Plains":
		emoji = "🌾"
	elif biome == "Forest":
		emoji = "🌲"
	elif biome == "Mountain":
		emoji = "⛰️"
	elif biome == "Snow":
		emoji = "🌨️"
	else:
		emoji = "🐉"

	return emoji


def density(biome):
	biome = 25
	if biome == "Sea":
		return 25
	if biome == "Water":
		return 30
	if biome == "Sand":
		return 25
	if biome == "Plains":
		return 35
	if biome == "Forest":
		return 40
	if biome == "Mountain":
		return 28
	if biome == "Snow":
		return 15
	if biome == "Hell":
		return 6
	if biome == "Underdark":
		return 4
	return 10
