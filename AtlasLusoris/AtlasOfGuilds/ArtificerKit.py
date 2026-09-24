"""Artificer Specializations."""

from AtlasLusoris.GuildKit import Artificer
from AtlasLusoris.GuildKit import Make_Specialization


Alchemist = Make_Specialization(
	guild=Artificer,
	name="Alchemist",
	module=__name__,
	)
Armorer = Make_Specialization(
	guild=Artificer,
	name="Armorer",
	module=__name__,
	)
Artillerist = Make_Specialization(
	guild=Artificer,
	name="Artillerist",
	module=__name__,
	)
BattleSmith = Make_Specialization(
	guild=Artificer,
	name="Battle Smith",
	module=__name__,
	)

SPECIALIZATIONS = (
	Alchemist,
	Armorer,
	Artillerist,
	BattleSmith,
	)
