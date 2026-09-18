"""
GuildKit — public TOP API for Guild Tags.

The Character is the Target. Guild Shapes (Barbarian, Cleric, Wizard, …)
are Tags. Apply with Apply_Guild / Join_Guild. Query with Find_Guild,
Has, and Field membership (`agent in Cleric`).

Mage, Martial, and Adept Pin Guild cards. That Field is the catalog;
do not keep a parallel list of classes. Specialization Tags are
more-specific Guild Shapes declared in AtlasOfGuilds.

This module is the Ada spec. Construction lives in Grimoire_of_Guilds.

The Guild libraries load last, and from here. Each kit in AtlasOfGuilds
imports Build_Specialization off this spec, so the spec has to finish
re-exporting the body before the first kit is read.
"""

from AtlasLusoris.Grimoire_of_Guilds import *
from AtlasLusoris.Grimoire_of_Guilds import __all__ as __all__
from AtlasLusoris.AtlasOfGuilds import Load_Guild_Libraries

Load_Guild_Libraries()
