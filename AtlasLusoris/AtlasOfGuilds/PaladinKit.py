"""Paladin Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Paladin


Ancients = Make_Specialization(
	guild=Paladin,
	name="Ancients",
	module=__name__,
	)
Devotion = Make_Specialization(
	guild=Paladin,
	name="Devotion",
	module=__name__,
	)
Glory = Make_Specialization(
	guild=Paladin,
	name="Glory",
	module=__name__,
	)
Vengeance = Make_Specialization(
	guild=Paladin,
	name="Vengeance",
	module=__name__,
	)

SPECIALIZATIONS = (
	Ancients,
	Devotion,
	Glory,
	Vengeance,
	)
