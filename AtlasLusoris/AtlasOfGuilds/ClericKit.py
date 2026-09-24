"""Cleric Specializations.

Voice (Guild paragraph and Domain extends) is seated after the
Shapes exist. Mechanics stay on the Tags; prose lives in
Map_of_Cleric_Prayers.
"""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Cleric
from AtlasLusoris.Map_of_Cleric_Prayers import bind_cleric_voice


Life = Make_Specialization(
	guild=Cleric,
	name="Life",
	module=__name__,
	)
Light = Make_Specialization(
	guild=Cleric,
	name="Light",
	module=__name__,
	)
Trickery = Make_Specialization(
	guild=Cleric,
	name="Trickery",
	module=__name__,
	)
War = Make_Specialization(
	guild=Cleric,
	name="War",
	module=__name__,
	)

SPECIALIZATIONS = (
	Life,
	Light,
	Trickery,
	War,
	)

bind_cleric_voice(
	guild=Cleric,
	domains=SPECIALIZATIONS,
	)
