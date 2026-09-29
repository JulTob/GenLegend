"""
Ledger_of_Tools — the kits a tool proficiency is carried in.

A tool is authored once, in ``AtlasInventarium.ToolsKit``: its name, its
governing ability, and its Practice (the flavour, the rules, the Works of
Wonder).  This ledger adds only what a kit weighs and costs, and builds each
item from that one definition, so a rename or a merge made in ToolsKit reaches
the bag without a second list to drift (QST-0116).

A Musical Instrument and a Gaming Set are kinds, not items: every instrument
and every game is its own kit, at its own price, and a Character carries the
ones the training ledger says they know.

Data source for weights and prices: the 2024 equipment table.  Costs are held
in gold: 1 SP = 0.1 GP.
"""

from __future__ import annotations

from AtlasInventarium.ItemKit import Make_Item, Item
from AtlasInventarium.ToolsKit import (
	ARTISAN_TOOLS as _ARTISAN_TOOL_DEFINITIONS,
	GAMING_SETS as _GAMING_SET_DEFINITIONS,
	MUSICAL_INSTRUMENTS as _INSTRUMENT_DEFINITIONS,
	OTHER_TOOLS as _OTHER_TOOL_DEFINITIONS,
	Tool_Definition,
	)


_ABILITY_NAMES = {
	"STR": "Strength",
	"DEX": "Dexterity",
	"CON": "Constitution",
	"INT": "Intelligence",
	"WIS": "Wisdom",
	"CHA": "Charisma",
	"ANY": "Any",
	}

# What each kit weighs (lb) and costs (GP), by ToolsKit key.
_KITS: dict[str, tuple[float, float]] = {
	# Artisan's Tools
	"Alchemist_Supplies": ( 8, 50 ),
	"Brewer_Supplies": ( 9, 20 ),
	"Calligrapher_Supplies": ( 5, 10 ),
	"Woodworker_Tools": ( 6, 8 ),
	"Cartographer_Tools": ( 6, 15 ),
	"Cobbler_Tools": ( 5, 5 ),
	"Cook_Utensils": ( 8, 1 ),
	"Glassblower_Tools": ( 5, 30 ),
	"Jeweler_Tools": ( 2, 25 ),
	"Leatherworker_Tools": ( 5, 5 ),
	"Mason_Tools": ( 8, 10 ),
	"Painter_Supplies": ( 5, 10 ),
	"Potter_Tools": ( 3, 10 ),
	"Smith_Tools": ( 8, 20 ),
	"Tinker_Tools": ( 10, 50 ),
	"Weaver_Tools": ( 5, 1 ),
	# Other tools
	"Disguise_Kit": ( 3, 25 ),
	"Forgery_Kit": ( 5, 15 ),
	"Herbalism_Kit": ( 3, 5 ),
	"Poisoners_Kit": ( 2, 50 ),
	"Thieves_Tools": ( 1, 25 ),
	# Gaming Sets
	"Dice_Set": ( 0, 0.1 ),
	"Dragonchess_Set": ( 0, 1 ),
	"Playing_Card_Set": ( 0, 0.5 ),
	"Three_Dragon_Ante_Set": ( 0, 1 ),
	# Musical Instruments
	"Bagpipes": ( 6, 30 ),
	"Drum": ( 3, 6 ),
	"Dulcimer": ( 10, 25 ),
	"Flute": ( 1, 2 ),
	"Horn": ( 2, 3 ),
	"Lute": ( 2, 35 ),
	"Lyre": ( 2, 30 ),
	"Pan_Flute": ( 2, 12 ),
	"Shawm": ( 1, 2 ),
	"Viol": ( 1, 30 ),
	}


def _kit(
		tool: Tool_Definition,
		) -> Item:
	"""The item one tool proficiency is carried in, described by its Practice."""
	weight, value = _KITS[ tool.key ]
	ability = _ABILITY_NAMES[ tool.ability ]
	item = Make_Item(
			name=tool.name,
			value=value,
			weight=weight,
			description=f"{tool.practice.flavour} (Ability: {ability}.)",
			)
	item.ability = ability
	item.tool = tool
	return item


ARTISANS_TOOLS: tuple[Item, ...] = tuple(
		_kit( tool )
		for tool in _ARTISAN_TOOL_DEFINITIONS
		)
GAMING_SETS: tuple[Item, ...] = tuple(
		_kit( tool )
		for tool in _GAMING_SET_DEFINITIONS
		)
MUSICAL_INSTRUMENTS: tuple[Item, ...] = tuple(
		_kit( tool )
		for tool in _INSTRUMENT_DEFINITIONS
		)
OTHER_TOOLS: tuple[Item, ...] = (
		*(
			_kit( tool )
			for tool in _OTHER_TOOL_DEFINITIONS
			),
		*GAMING_SETS,
		*MUSICAL_INSTRUMENTS,
		)

TOOLS: tuple[Item, ...] = ARTISANS_TOOLS + OTHER_TOOLS

TOOLS_BY_NAME: dict[str, Item] = {
		tool.name: tool
		for tool in TOOLS
		}
# The names a merged tool used to have still find it.
TOOLS_BY_NAME.update(
		{
			"Carpenter's Tools": TOOLS_BY_NAME[ "Woodworker's Tools" ],
			"Woodcarver's Tools": TOOLS_BY_NAME[ "Woodworker's Tools" ],
			"Navigator's Tools": TOOLS_BY_NAME[ "Cartographer's Tools" ],
			}
		)


__all__ = (
		"ARTISANS_TOOLS",
		"GAMING_SETS",
		"MUSICAL_INSTRUMENTS",
		"OTHER_TOOLS",
		"TOOLS",
		"TOOLS_BY_NAME",
		)


def _self_test():
	from AtlasInventarium.ToolsKit import TOOLS as DEFINITIONS

	names = [ tool.name for tool in TOOLS ]
	assert len( names ) == len( set( names ) ), "duplicate tool names in the ledger"
	assert set( _KITS ) == { tool.key for tool in DEFINITIONS }, (
			"every ToolsKit tool needs one kit, and no kit may outlive its tool"
			)
	assert len( ARTISANS_TOOLS ) == 16, len( ARTISANS_TOOLS )
	assert TOOLS_BY_NAME[ "Carpenter's Tools" ] is TOOLS_BY_NAME[ "Woodworker's Tools" ]
	assert TOOLS_BY_NAME[ "Woodcarver's Tools" ] is TOOLS_BY_NAME[ "Woodworker's Tools" ]
	assert TOOLS_BY_NAME[ "Navigator's Tools" ] is TOOLS_BY_NAME[ "Cartographer's Tools" ]
	assert "Musical Instrument" not in TOOLS_BY_NAME
	assert "Gaming Set" not in TOOLS_BY_NAME

	for tool in TOOLS:
		assert tool.ability, f"{tool.name} has no governing ability"
		assert tool.value > 0, f"{tool.name} is free"
		assert tool.tool.practice.flavour in tool.description, (
				f"{tool.name} must be described by its Practice"
				)

	print(
			f"OK — Ledger_of_Tools self-test ({len(TOOLS)} kits, one per ToolsKit tool)"
			)


if __name__ == "__main__":
	_self_test()
