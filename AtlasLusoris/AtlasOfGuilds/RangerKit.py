"""Ranger Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Ranger


BeastMaster = Make_Specialization(
	guild=Ranger,
	name="Beast Master",
	module=__name__,
	)
FeyWanderer = Make_Specialization(
	guild=Ranger,
	name="Fey Wanderer",
	module=__name__,
	)
GloomStalker = Make_Specialization(
	guild=Ranger,
	name="Gloom Stalker",
	module=__name__,
	)
Hunter = Make_Specialization(
	guild=Ranger,
	name="Hunter",
	module=__name__,
	)

SPECIALIZATIONS = (
	BeastMaster,
	FeyWanderer,
	GloomStalker,
	Hunter,
	)
