"""Guild-owned libraries of more-specific Guild Shapes."""

from importlib import import_module

_GUILD_LIBRARIES = (
	"ArtificerKit",
	"BarbarianKit",
	"BardKit",
	"ClericKit",
	"DruidKit",
	"FighterKit",
	"MonkKit",
	"PaladinKit",
	"RangerKit",
	"RogueKit",
	"SorcererKit",
	"WarlockKit",
	"WizardKit",
	)


def Load_Guild_Libraries(
		) -> None:
	"""Load each Guild's own Specialization declarations once."""
	for library in _GUILD_LIBRARIES:
		import_module(
			f"{__name__}.{library}"
			)


def Validate_Guild_Specializations(
		) -> None:
	"""
	Validate that all Guilds have at least one Specialization.
	
	This should be called after Load_Guild_Libraries() to ensure all
	Specializations are registered before validation.
	
	Raises AssertionError if any Guild is missing Specializations.
	"""
	from AtlasLusoris.AtlasOfGuilds.validation import assert_guild_specializations_valid
	from AtlasLusoris.Grimoire_of_Guilds import SPECIALIZATIONS_BY_GUILD
	from AtlasLusoris.GuildKit import GUILDS
	
	assert_guild_specializations_valid(
		dict(GUILDS),
		dict(SPECIALIZATIONS_BY_GUILD),
		)


__all__ = (
	"Load_Guild_Libraries",
	"Validate_Guild_Specializations",
	)
