"""
Kinship Tags: what a Character *resembles*, which is never what the rules call
them.

``Creature_Type`` in ``bases`` answers the rules question, and for every
playable Species the answer is ``Humanoid``: an Aasimar is not a Celestial, and
a spell that seeks Celestials does not find one.  This answers the other
question, the one every flavour system actually asks.  Aasimar take their names
from Celestials.  Gnomes get read as Fae whether or not they have ever seen the
Feywild.  A Goliath is spoken of the way giants are spoken of.

Kinship is carried as a Tag rather than as a field because that is exactly what
a Tag is for.  A Species declares its kin as a base, and nothing has to keep a
list of which Species happen to be celestial-ish.  Nothing here grants
anything: no Resistance, no sense, no trait.  It is classification, for names,
titles, gear vocabulary and familiar affinity.

**These share their names with the Creature Types deliberately.**  Each is a
TopKit ``@Flag``, so ``"Celestial" in character`` resolves by Tag *name*, so an Aasimar passes every
flavour filter that asks for the word, while ``character in
bases.Celestial`` stays False and no spell that seeks Celestials finds one.
The word is the vibe; the class is the rule; only one of them is load-bearing
for the game.  Import these under a ``Kin_`` alias wherever both trees are in
scope, so the reader can tell which question is being asked.
"""

from TopKit import Flag
from TopKit import Tag
from TopKit import Pre

from AtlasActorLudi.CharactersKit import Character


@Flag
class Kinship(Tag):
	"""What a Character resembles, for everything that is not a rule."""

	@Pre
	def Character_Only(
		target,
		):
		return isinstance(
			target,
			Character,
			)


@Flag
class Celestial(Kinship):
	"""Read as of the Upper Planes: aasimar, and those who carry a spark."""


@Flag
class Fey(Kinship):
	"""Read as of the Feywild: elves, gnomes, and anything asked to go back."""


@Flag
class Fiend(Kinship):
	"""Read as of the Lower Planes: tieflings, and the inconveniently horned."""


@Flag
class Dragon(Kinship):
	"""Read as draconic: dragonborn, kobolds, and the scaled."""


@Flag
class Giant(Kinship):
	"""Read as of the giants: goliaths, and whoever else looms."""


@Flag
class Undead(Kinship):
	"""Read as no longer entirely alive: dhampirs, reborn, and the returned."""


@Flag
class Elemental(Kinship):
	"""Read as of the elements: genasi, and anything that smells of storm."""


KINSHIPS = (
	Celestial,
	Dragon,
	Elemental,
	Fey,
	Fiend,
	Giant,
	Undead,
	)


def Kinships_Of(
	character,
	) -> tuple[str, ...]:
	"""
	Every kinship a Character carries, as plain words.

	``("Celestial",)`` rather than ``(Celestial,)``, because the callers are
	name tables and affinity weights that want a word to match on.  ``word in
	character`` answers the same question one kinship at a time; this is for
	when you want the whole list.
	"""
	return tuple(
		tag.__name__
		for tag in KINSHIPS
		if character in tag
		)


__all__ = (
	"Celestial",
	"Dragon",
	"Elemental",
	"Fey",
	"Fiend",
	"Giant",
	"KINSHIPS",
	"Kinship",
	"Kinships_Of",
	"Undead",
	)
