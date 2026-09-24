"""Barbarian Specializations."""

from AtlasLusoris.GuildKit import Barbarian
from AtlasLusoris.GuildKit import Make_Specialization


BERSERKER_DESCRIPTION = (
	"Most people hold something back. You don't. You are a wild horse. Untamed.\n\n"
	"When you go, you go all the way. Furious in a fight. Delighted by a meal. "
	"Crying at a poem. Dancing through a song. Whatever the moment is, you are "
	"the whole of it. Pain quiets. Fear vanishes. You belong in that moment. "
	"Nothing else exists. One purpose.\n\n"
	"Some find that unsettling. But you could not be any other way. You are "
	"the eye of the storm."
	)
Berserker = Make_Specialization(
	guild=Barbarian,
	name="Berserker",
	module=__name__,
	extends=BERSERKER_DESCRIPTION,
	heading="Path of the Berserker",
	)

WILD_HEART_DESCRIPTION = (
	"Your rage comes from a primal instinct. A connection to your "
	"animalistic nature. A harmony with the bestial spirit. Your heart "
	"beats to the rhythms of nature. Rage is how you listen to it.\n\n"
	"You listen to the wolves and to the bears. Both the ones you hunt "
	"with and the ones you carry in your spirit. You listen to your "
	"place in the wilds, and you know you belong.\n\n"
	"Now the world of civilization calls, and you carry the wild things "
	"in your heart."
	)
WildHeart = Make_Specialization(
	guild=Barbarian,
	name="Wild Heart",
	module=__name__,
	extends=WILD_HEART_DESCRIPTION,
	heading="Path of the Wild Heart",
	)

WORLD_TREE_DESCRIPTION = (
	"Rage comes to you as awe. A cosmic connection. A veil being lifted "
	"from your eyes.\n\n"
	"All boundaries are illusions. Now you see the whole: energy flowing "
	"under the sea, streams of light through the night skies, every living "
	"thing hanging from the same enormous tree. All connected through time "
	"and space. It is beautiful. You are very small. You are part of it. "
	"You are not alone. If you can see through the veil, you can cross them."
	)
WorldTree = Make_Specialization(
	guild=Barbarian,
	name="World Tree",
	module=__name__,
	extends=WORLD_TREE_DESCRIPTION,
	heading="Path of the World Tree",
	)

ZEALOT_DESCRIPTION = (
	"Ecstasy. Fervor. Revelation.\n\n"
	"You are taken by one of the Gods themselves. {name} is nothing more "
	"than a vessel for the divine, and a conduit for their wrath and their "
	"glory. Guided in your rage by a holy commandment. You can sense exactly "
	"what the God wants of you, and you feel honored and moved. You are no "
	"longer there, a God is. And facing you is blasphemous."
	)
Zealot = Make_Specialization(
	guild=Barbarian,
	name="Zealot",
	module=__name__,
	extends=ZEALOT_DESCRIPTION,
	heading="Path of the Zealot",
	)

SPECIALIZATIONS = (
	Berserker,
	WildHeart,
	WorldTree,
	Zealot,
	)
