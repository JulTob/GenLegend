"""Druid Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Druid


LAND_DESCRIPTION = """You learn about this land, and the lands beyond the horizon. You learn where water runs after rain, which grasses return first, why foxes hunt rabbits, and how a field dies when one small insect disappears. The Circle of the Land studies habitat as a living system. Every answer creates another question. Every connection opens another investigation.

Your Circle studies and shares this knowledge to preserve the natural order. You do not guard nature because it is innocent. You guard the experiment because you understand how much disappears when it is broken."""

MOON_DESCRIPTION = """Your study begins with tracks. Not just the shape of the paw, but the distance between them, the weight in the mud, the moment the animal stopped and looked back. The Circle of the Moon studies the animal from inside. You learn hunger, caution, territory, and the need to run. There is no honest way to observe a living thing without being changed by it.

Your Circle studies change, difference, and the connections among all living things. You learn that every form belongs to one tree of life. The observation then takes you: fur, muscle, talon, scale. You try not to ask why it is so easy for you to understand the beast, or whether, after changing, you will still want to return."""

SEA_DESCRIPTION = """Life began in the sea. Life remains in motion. What becomes static drowns. You study currents, flux, cycles, migration, and the first invisible difference that becomes a storm. The sea is ever changing. It is the oldest experiment. You learned to flow with it.

The Circle of the Sea studies change at its largest scale. You learn that calm is not kindness and violence is not anger. Water follows forces. You let those forces shape you, until adapting becomes instinct. You breathe where others cannot, move as the current moves, and bring the sea ashore. You become one with the sea, and you guide it."""

STARS_DESCRIPTION = """At dusk, the first stars appear before the eye that looks up. One becomes two, two become a pattern, and the universe slowly opens for you. And you open yourself to the universe. You are one of the wanderers: a living thing that looks up from a small world and discovers that it, too, is moving through the dark. The light you watch began before your ancestors had names.

Some stars are more than fires. They are principles made visible, ordered by influence and omen. You study the heavens to learn the patterns by which to guide your own life. You become infinite by discovering how much world can fit inside one observing life. You are the cosmos looking at itself."""


Land = Make_Specialization(
	guild=Druid,
	name="Land",
	module=__name__,
	extends=LAND_DESCRIPTION,
	heading="Circle of the Land",
	)
Moon = Make_Specialization(
	guild=Druid,
	name="Moon",
	module=__name__,
	extends=MOON_DESCRIPTION,
	heading="Circle of the Moon",
	)
Sea = Make_Specialization(
	guild=Druid,
	name="Sea",
	module=__name__,
	extends=SEA_DESCRIPTION,
	heading="Circle of the Sea",
	)
Stars = Make_Specialization(
	guild=Druid,
	name="Stars",
	module=__name__,
	extends=STARS_DESCRIPTION,
	heading="Circle of Stars",
	)

SPECIALIZATIONS = (
	Land,
	Moon,
	Sea,
	Stars,
	)
