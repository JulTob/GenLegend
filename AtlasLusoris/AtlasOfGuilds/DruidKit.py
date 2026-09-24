"""Druid Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Druid


Land = Make_Specialization(
	guild=Druid,
	name="Land",
	module=__name__,
	)
Moon = Make_Specialization(
	guild=Druid,
	name="Moon",
	module=__name__,
	)
Sea = Make_Specialization(
	guild=Druid,
	name="Sea",
	module=__name__,
	)
Stars = Make_Specialization(
	guild=Druid,
	name="Stars",
	module=__name__,
	)

SPECIALIZATIONS = (
	Land,
	Moon,
	Sea,
	Stars,
	)
