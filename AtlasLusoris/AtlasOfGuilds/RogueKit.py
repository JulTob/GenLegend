"""Rogue Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Rogue


ArcaneTrickster = Make_Specialization(
	guild=Rogue,
	name="Arcane Trickster",
	module=__name__,
	)
Assassin = Make_Specialization(
	guild=Rogue,
	name="Assassin",
	module=__name__,
	)
Soulknife = Make_Specialization(
	guild=Rogue,
	name="Soulknife",
	module=__name__,
	)
Thief = Make_Specialization(
	guild=Rogue,
	name="Thief",
	module=__name__,
	)

SPECIALIZATIONS = (
	ArcaneTrickster,
	Assassin,
	Soulknife,
	Thief,
	)
