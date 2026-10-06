"""Guild-owned libraries of more-specific Guild Shapes."""

from importlib import import_module

_GUILD_LIBRARIES = (
	"ArtificerKit",
	"BarbarianKit",
	"BardKit",
	"ClericKit",
	"DruidKit",
	"FighterKit",
	"Monk_Kit",
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


__all__ = (
	"Load_Guild_Libraries",
	)
