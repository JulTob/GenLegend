# AtlasLusoris/Map_of_Classes/__init__.py

"""Public façade: `from AtlasLusoris.Map_of_Classes import Wizard`"""

# Re-export the abstract base & helpers
from .Scroll_of_Constants import CLASSES, SUBCLASSES
from .Grimoire_of_Health  import roll_health, health_dice, HIT_DIE_TABLE
from .Codex_of_Progression  import (
		Progression,
		get_class_progression,
		get_features,
		)

# Import concrete classes
try:
	from .Training.Barbarian import Barbarian
	from .Training.Bard      import Bard
	from .Training.Cleric    import Cleric
	from .Training.Druid     import Druid
	from .Training.Fighter   import Fighter
	from .Training.Monk      import Monk
	from .Training.Paladin   import Paladin
	from .Training.Ranger    import Ranger
	from .Training.Rogue     import Rogue
	from .Training.Sorcerer  import Sorcerer
	from .Training.Warlock   import Warlock
	from .Training.Wizard    import Wizard
	from .Training.Multiclass import Multiclass
except Exception:
	pass  # optional: log load failure

# ── backward-compat shim for Flask route ─────────────
classes = list(CLASSES)        # same data, old variable name
subclasses = SUBCLASSES          # same dict, different alias

GetClassProgression = get_class_progression   # function's CamelCase alias

__all__ = [
	# data
	"HIT_DIE_TABLE", "CLASSES", "SUBCLASSES",
	# helpers
	"roll_health", "health_dice", "Progression",
	"get_features", "get_class_progression",
	# concrete
	"Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
	"Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
	"Multiclass",
	"classes", "subclasses",
	"get_class_progression", "GetClassProgression",
	"apply_class_features"]

GetFeatures = get_features # legacy Camel-Case alias so old code continues to work
__all__.extend(["get_features", "GetFeatures"])
