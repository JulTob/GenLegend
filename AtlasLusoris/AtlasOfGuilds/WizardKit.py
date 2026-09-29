"""Wizard Specializations."""

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Wizard


Abjurer = Make_Specialization(
	guild=Wizard,
	name="Abjurer",
	module=__name__,
	)
Diviner = Make_Specialization(
	guild=Wizard,
	name="Diviner",
	module=__name__,
	)
Evoker = Make_Specialization(
	guild=Wizard,
	name="Evoker",
	module=__name__,
	)
Illusionist = Make_Specialization(
	guild=Wizard,
	name="Illusionist",
	module=__name__,
	)
Bladesinger = Make_Specialization(
	guild=Wizard,
	name="Bladesinger",
	module=__name__,
	)

SPECIALIZATIONS = (
	Abjurer,
	Diviner,
	Evoker,
	Illusionist,
	Bladesinger,
	)
