'''
Map of Titles — mythic title composition and vocabulary (AtlasEpica).

Syntax of stories: descriptors, ranks, origins for lusors and adventures.
Phonotactics / NewName remain in AtlasNomina. Tracked under QST-0037.14.
'''
from Minion import changeling, print_record, report_bug
from Minion import CHANGELING_MINION, CHANGELING_COLOR

#-- Map_of_Titles is a package: the composer lives here and every vocabulary
#-- in a file of its own (descriptors, ranks, places, elements, artifacts,
#-- masters, animals, origins), with Genus in _glue so no vocabulary ever
#-- imports the package back. Each name the single file defined is imported
#-- here so ``from AtlasEpica.Map_of_Titles import Title`` and its kin, and
#-- ``Map_of_Titles.Descriptor`` and the rest, keep working unchanged.
from ._glue import Genus
from .descriptors import Descriptor
from .ranks import Rank
from .places import Place
from .elements import Element
from .artifacts import Artifact
from .masters import Master
from .animals import Animal
from .origins import Origin

# The last rung of the title ladder, in the spirit of LAST_RESORT_NAMES over
# in AtlasNomina.Map_of_Names: plain strings, so they cannot fail. A title
# off this roster should read as somebody's character, not as an error
# message, because that is exactly when it is used.

LAST_RESORT_TITLES = (
	"The Wanderer", "The Quiet", "The Bold", "The Nameless",
	"The Sworn", "The Far-Travelled", "The Steadfast",
	"The Unlooked-For", "The Stranger", "The Patient",
	"The Unbowed", "The Late-Come",
	)

def LastResortTitle(lusor):
	"""A title that cannot fail to be produced, for when composition can."""
	try:
		return lusor.Pick(
			LAST_RESORT_TITLES,
			dice=lusor.Dice_Bag(
				"Epica.Title.LastResort",
				version="1",
				),
			)
	except Exception as exc:
		report_bug(exc)
		from zlib import crc32
		identity = str(
			getattr(lusor, "seed", "") or id(lusor)
			).encode("utf-8")
		return LAST_RESORT_TITLES[crc32(identity) % len(LAST_RESORT_TITLES)]

def _part(lusor, maker, dice):
	'''
One piece of a title, or None if that piece cannot be made.

Reported either way: a title quietly losing its origin every time is a
vocabulary bug that would otherwise look like a stylistic choice.
'''
	try:
		return maker(
			lusor,
			dice=dice,
			)
	except Exception as exc:
		report_bug(exc)
		print_record(
			f"{CHANGELING_MINION} [titles] {maker.__name__} raised "
			f"{type(exc).__name__}; the title goes without it.",
			CHANGELING_COLOR,
			)

		return None

def custom_cases(s):
	'''
Converts a string to title case.
Normalizes separator symbols to spaces, then title-cases with possessive 's left lowercase.
'''
	accepted_symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 1234567890 '"
	for symbol in s:
		if symbol not in accepted_symbols:
			s = s.replace(symbol, " ")
	s = " ".join(s.split())
	return s.title().replace("'S", "'s")

@changeling(LastResortTitle)
def Title(lusor):
	'''
Compose a mythic title from a descriptor, a rank and an origin.

Only the rank is load-bearing. A missing descriptor or origin removes the
patterns that needed it and leaves the rest standing, so one gap in the
vocabulary costs a shade of the title instead of all of it.
'''
	dice = lusor.Dice_Bag(
		"Epica.Title",
		version="1",
		)

	descriptor = _part(lusor, Descriptor, dice)
	rank = _part(lusor, Rank, dice)
	origin = _part(lusor, Origin, dice)

	if not rank:
		raise ValueError(
			"Title: no rank, and every pattern is built on one.",
			)

	patterns = [
		(f"The {descriptor} {rank}", 20, (descriptor,)),
		(f"The {rank} {origin}", 15, (origin,)),
		(f"The {rank}", 4, ()),
		(f"The {descriptor} {rank} {origin}", 1, (descriptor, origin)),
		]

	usable = [
		(text, weight)
		for text, weight, needs in patterns
		if all(needs)
		]

	title = lusor.Pick(
		[text for text, _ in usable],
		[weight for _, weight in usable],
		dice=dice,
		)

	return custom_cases(title)
