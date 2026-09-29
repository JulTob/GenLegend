'''
Grimoire of Adventure — TOP substrate for AtlasEpica (BBEG Oracle).

An Adventure is a stable Target: seed, level, and one BBEG. Meaning grows by
Tags. Session frame = Area (biome/place) + Lair (specific seat), collapsed when
the BBEG is set. Theme Tags remain for a later soft layer (QST-0037.13 / .16).

	Forest(adventure)          # Area
	Tower(adventure)           # Lair
	adventure.bbeg             # the DM character (NPC)

Wave collapse here means Tag-gated seeded choice — same spirit as Titles —
not the WorldBuild grid WFC kit. Tracked under QST-0037.16.
'''

from __future__ import annotations

import hashlib
import random

from TopKit import Tag, Pre, Record


"""		Adventure — the Epica root    """
class Adventure:
	"""Seeded BBEG oracle session for the dungeon master (not a grid map)."""

	TAG_ROOTS = ()

	def __init__(adventure, seed=None, level=5):
		if level < 1:
			raise ValueError("level must be >= 1")

		adventure.seed = int(seed) if seed is not None else random.randint(0, 2**31 - 1)
		adventure.level = int(level)
		adventure._rng = random.Random(adventure.seed)
		adventure.bbeg = None
		adventure.card_index = 0  # how many inspiration cards drawn

	def choose(adventure, options):
		"""Collapse one option from a non-empty sequence using the adventure's RNG."""
		if not options:
			raise ValueError("choose() called with an empty sequence")
		return adventure._rng.choice(list(options))

	def fork_rng(adventure, *salts):
		"""Deterministic RNG fork (stable digest — not Python's salted hash())."""
		material = "|".join(str(s) for s in (adventure.seed, *salts))
		digest = hashlib.md5(material.encode("utf-8")).hexdigest()
		return random.Random(int(digest[:8], 16))

	def bind_bbeg(adventure, npc):
		"""Attach the DM character. Caller should Collapse_Frame after."""
		adventure.bbeg = npc
		return npc

	def __repr__(adventure):
		bbeg = getattr(adventure.bbeg, "name", None) or "—"
		area = getattr(adventure, "area", None) or "—"
		lair = getattr(adventure, "lair", None) or "—"
		return (
			f"Adventure(seed={adventure.seed!r}, level={adventure.level}, "
			f"bbeg={bbeg!r}, area={area!r}, lair={lair!r})"
		)


"""		Root: every Epica Tag on an Adventure    """
class Adventure_Tag(Tag):
	NAME = "Adventure Tag"
	DESCRIPTION = "Root of every Tag an Adventure may bear. Only Adventure targets."

	@Pre
	def Adventure_Only(agent):
		return isinstance(agent, Adventure)


"""		Area — biome / general place (Dungeon = underground complex)    """
class Area(Adventure_Tag):
	NAME = "Area"
	DESCRIPTION = (
		"The wider place of the session: Urban, Forest, Dungeon (underground complex), "
		"and kin. An adventure bears exactly one."
	)

	@Pre
	def Single_Area(agent):
		count = sum(1 for area in AREAS.values() if agent in area)
		return count <= 1


class Urban(Area):
	NAME = "Urban"
	DESCRIPTION = "City, town, streets, docks, markets."

	@Record
	def area(adventure):
		return "Urban"


class Forest(Area):
	NAME = "Forest"
	DESCRIPTION = "Wild wood, green hold, trail under canopy."

	@Record
	def area(adventure):
		return "Forest"


class Dungeon(Area):
	NAME = "Dungeon"
	DESCRIPTION = "Underground complex — Tragones y Mazmorras sense, not only a crawl grid."

	@Record
	def area(adventure):
		return "Dungeon"


class Swamp(Area):
	NAME = "Swamp"
	DESCRIPTION = "Bog, fen, drowned land."

	@Record
	def area(adventure):
		return "Swamp"


class Mountain(Area):
	NAME = "Mountain"
	DESCRIPTION = "Peak, cliff, high pass."

	@Record
	def area(adventure):
		return "Mountain"


class Desert(Area):
	NAME = "Desert"
	DESCRIPTION = "Sand, waste, dry expanse."

	@Record
	def area(adventure):
		return "Desert"


class Coast(Area):
	NAME = "Coast"
	DESCRIPTION = "Shore, tide, salt wind."

	@Record
	def area(adventure):
		return "Coast"


class Graveyard(Area):
	NAME = "Graveyard"
	DESCRIPTION = "Necropolis edge, tombs above ground, memorial ground."

	@Record
	def area(adventure):
		return "Graveyard"


AREAS = {
	"Urban": Urban,
	"Forest": Forest,
	"Dungeon": Dungeon,
	"Swamp": Swamp,
	"Mountain": Mountain,
	"Desert": Desert,
	"Coast": Coast,
	"Graveyard": Graveyard,
}


"""		Lair — the BBEG's specific seat inside the Area    """
class Lair(Adventure_Tag):
	NAME = "Lair"
	DESCRIPTION = (
		"The concrete construction: tower, temple, castle, catacomb, port den… "
		"An adventure bears exactly one."
	)

	@Pre
	def Single_Lair(agent):
		count = sum(1 for lair in LAIRS.values() if agent in lair)
		return count <= 1


class Tower(Lair):
	NAME = "Tower"
	DESCRIPTION = "Wizard's tower, watchspire, isolated vertical hold."

	@Record
	def lair(adventure):
		return "Tower"


class Temple(Lair):
	NAME = "Temple"
	DESCRIPTION = "Cult temple, ruined shrine, consecrated hall."

	@Record
	def lair(adventure):
		return "Temple"


class Castle(Lair):
	NAME = "Castle"
	DESCRIPTION = "Castle, keep, fortified manor."

	@Record
	def lair(adventure):
		return "Castle"


class Catacomb(Lair):
	NAME = "Catacomb"
	DESCRIPTION = "Catacomb, crypt warren, bone galleries."

	@Record
	def lair(adventure):
		return "Catacomb"


class Port_Den(Lair):
	NAME = "Port Den"
	DESCRIPTION = "Warehouse, smuggler's den, dockside hideout."

	@Record
	def lair(adventure):
		return "Port Den"


class Circle(Lair):
	NAME = "Circle"
	DESCRIPTION = "Druid circle, standing stones, wild sanctum."

	@Record
	def lair(adventure):
		return "Circle"


class Cave(Lair):
	NAME = "Cave"
	DESCRIPTION = "Cave mouth, dragon den, mountain hollow."

	@Record
	def lair(adventure):
		return "Cave"


class Manor(Lair):
	NAME = "Manor"
	DESCRIPTION = "Townhouse, villa, polite face over a rotten core."

	@Record
	def lair(adventure):
		return "Manor"


LAIRS = {
	"Tower": Tower,
	"Temple": Temple,
	"Castle": Castle,
	"Catacomb": Catacomb,
	"Port Den": Port_Den,
	"Circle": Circle,
	"Cave": Cave,
	"Manor": Manor,
}


"""		Theme — soft seam for later (not required for v1 oracle)    """
class Theme(Adventure_Tag):
	NAME = "Theme"
	DESCRIPTION = (
		"What the story is really about. Soft for v1 — structure is Area + Lair + NPC Tags. "
		"Root Themes exclusive; finer Themes inherit (Titles open/close)."
	)
	ABSTRACT = True

	@Pre
	def Single_Root_Theme(agent):
		count = sum(1 for theme in ROOT_THEMES.values() if agent in theme)
		return count <= 1


class Love(Theme):
	NAME = "Love"

	@Record
	def theme(adventure):
		return "Love"


class Hubris(Theme):
	NAME = "Hubris"

	@Record
	def theme(adventure):
		return "Hubris"


class Nest(Theme):
	NAME = "Nest"

	@Record
	def theme(adventure):
		return "Nest"


class Discovery(Theme):
	NAME = "Discovery"

	@Record
	def theme(adventure):
		return "Discovery"


class Mastery(Theme):
	NAME = "Mastery"

	@Record
	def theme(adventure):
		return "Mastery"


class Creation(Theme):
	NAME = "Creation"

	@Record
	def theme(adventure):
		return "Creation"


ROOT_THEMES = {
	"Love": Love,
	"Hubris": Hubris,
	"Nest": Nest,
	"Discovery": Discovery,
	"Mastery": Mastery,
	"Creation": Creation,
}
THEMES = ROOT_THEMES
ALL_THEMES = dict(ROOT_THEMES)


def Assign_Area(adventure, name):
	tag = AREAS.get(str(name))
	if tag is None:
		raise ValueError(f"unknown Area: {name!r}")
	tag(adventure)


def Assign_Lair(adventure, name):
	tag = LAIRS.get(str(name))
	if tag is None:
		raise ValueError(f"unknown Lair: {name!r}")
	tag(adventure)


def Assign_Theme(adventure, name):
	"""Optional Theme apply (v1 does not require Themes)."""
	tag = ALL_THEMES.get(str(name))
	if tag is None:
		raise ValueError(f"unknown Theme: {name!r}")
	if adventure not in tag:
		tag(adventure)


def npc_keys(npc) -> str:
	"""Titles-style probe string: race, archetype, title, name."""
	bits = []
	for attr in ("race", "subrace", "archetype", "title", "name"):
		value = getattr(npc, attr, None)
		if value:
			bits.append(str(value))
	return " ".join(bits)


def Collapse_Frame(adventure):
	"""
	When the BBEG is set: collapse Area + Lair from their keys (Titles-style).
	Requires adventure.bbeg. Idempotent if Area/Lair already applied.
	"""
	if adventure.bbeg is None:
		raise ValueError("Collapse_Frame requires adventure.bbeg")

	# Lodge tables live with the Map so vocabulary grows artistically there
	try:
		from AtlasEpica.Map_of_Scenes import pick_area, pick_lair
	except ImportError:
		from Map_of_Scenes import pick_area, pick_lair  # type: ignore

	keys = npc_keys(adventure.bbeg)
	rng = adventure.fork_rng("frame", keys)

	if adventure not in Area:
		Assign_Area(adventure, pick_area(keys, rng))
	if adventure not in Lair:
		Assign_Lair(adventure, pick_lair(keys, adventure.area, rng))
	return adventure


def Forge_Oracle(bbeg, *, seed=None, level=None):
	"""Fresh Adventure bound to this BBEG with Area + Lair collapsed."""
	level = int(level if level is not None else getattr(bbeg, "level", 5) or 5)
	seed = int(seed if seed is not None else getattr(bbeg, "seed", random.randint(0, 2**16)))
	adventure = Adventure(seed=seed, level=max(1, level))
	adventure.bind_bbeg(bbeg)
	Collapse_Frame(adventure)
	return adventure


Adventure.TAG_ROOTS = (Adventure_Tag,)


if __name__ == "__main__":
	from TopKit import TagCompositionError, TagPreconditionError

	class StubBBEG:
		def __init__(self):
			self.seed = 42
			self.level = 5
			self.race = "Elf"
			self.subrace = "Wood Elf"
			self.archetype = "Druid"
			self.title = "The Verdant"
			self.name = "Alaxandar"

	bbeg = StubBBEG()
	adv = Forge_Oracle(bbeg)
	assert adv.bbeg is bbeg
	assert adv in Area and adv in Lair
	assert adv.area == "Forest"
	assert adv.lair in ("Circle", "Tower", "Cave", "Temple")

	criminal = StubBBEG()
	criminal.archetype = "Criminal"
	criminal.race = "Human"
	criminal.subrace = ""
	urban = Forge_Oracle(criminal, seed=99)
	assert urban.area in AREAS
	assert urban.lair in LAIRS

	again = Forge_Oracle(bbeg, seed=42)
	assert again.area == adv.area and again.lair == adv.lair

	class NotAnAdventure:
		pass

	try:
		Tower(NotAnAdventure())
	except (TagPreconditionError, TagCompositionError):
		pass
	else:
		raise AssertionError("non-Adventure must be rejected")

	print("AtlasEpica.Grimoire_of_Adventure self-test OK")
	print(adv)
