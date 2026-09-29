"""
Monk_Kit — the Monk Guild, one file per design unit.

Thought pattern
	1. Core_Kit holds every Monk's lessons and the readers the Warriors share.
	2. Each Warrior Kit holds one Warrior: its Specialization Tag and its lessons.
	3. This index loads them in draw order and names the Warriors, so the
	   folder reads from outside like the one file it replaced.
	4. A new Warrior is one new Kit file and one line here. Nothing else moves.
"""

from AtlasLusoris.AtlasOfGuilds.Monk_Kit import Core_Kit
from AtlasLusoris.AtlasOfGuilds.Monk_Kit.Mercy_Kit import Mercy
from AtlasLusoris.AtlasOfGuilds.Monk_Kit.Open_Hand_Kit import OpenHand
from AtlasLusoris.AtlasOfGuilds.Monk_Kit.Shadow_Kit import Shadow
from AtlasLusoris.AtlasOfGuilds.Monk_Kit.Elements_Kit import Elements


SPECIALIZATIONS = (
	Mercy,
	OpenHand,
	Shadow,
	Elements,
	)


__all__ = (
	"Core_Kit",
	"Mercy",
	"OpenHand",
	"Shadow",
	"Elements",
	"SPECIALIZATIONS",
	)
