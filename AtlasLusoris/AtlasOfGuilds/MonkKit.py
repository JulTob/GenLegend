"""Monk Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Monk


Mercy = Make_Specialization(
	guild=Monk,
	name="Mercy",
	module=__name__,
	)
OpenHand = Make_Specialization(
	guild=Monk,
	name="Open Hand",
	module=__name__,
	)
Shadow = Make_Specialization(
	guild=Monk,
	name="Shadow",
	module=__name__,
	)
Elements = Make_Specialization(
	guild=Monk,
	name="Elements",
	module=__name__,
	)

SPECIALIZATIONS = (
	Mercy,
	OpenHand,
	Shadow,
	Elements,
	)
