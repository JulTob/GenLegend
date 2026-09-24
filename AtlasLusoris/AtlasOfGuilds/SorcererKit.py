"""Sorcerer Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Sorcerer


AberrantSorcery = Make_Specialization(
	guild=Sorcerer,
	name="Aberrant Sorcery",
	module=__name__,
	)
ClockworkSorcery = Make_Specialization(
	guild=Sorcerer,
	name="Clockwork Sorcery",
	module=__name__,
	)
DraconicSorcery = Make_Specialization(
	guild=Sorcerer,
	name="Draconic Sorcery",
	module=__name__,
	)
WildMagicSorcery = Make_Specialization(
	guild=Sorcerer,
	name="Wild Magic Sorcery",
	module=__name__,
	)

SPECIALIZATIONS = (
	AberrantSorcery,
	ClockworkSorcery,
	DraconicSorcery,
	WildMagicSorcery,
	)
