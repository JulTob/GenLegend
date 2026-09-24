"""MetaTOP Pins for complete Species declarations.

A new homebrew Species needs one declaration after defining its Form:

	Homebrew(
		My_Species,
		weight=20,
		size_options=("Medium",),
		speed=30,
		source_title="My Bestiary",
		)
"""

from TopKit import Pin
from TopKit import Pre
from TopKit import Record
from TopKit import Tag

from AtlasActorLudi.SpeciesKit.bases import Heritage
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasLusoris.FeaturesKit import Trait


def _tuple_report(
	values,
	) -> tuple:
	return tuple(
		values or ()
		)


@Pin
class Declared_Species(Tag):
	"""Root Pin for Species known to the generator."""

	@Pre
	def Species_Tag_Only(
		target,
		):
		return (
			isinstance(
				target,
				type,
				)
			and issubclass(
				target,
				Species,
				)
			and target not in (
				Species,
				Heritage,
				)
			)

	@Record
	def WEIGHT(
		target,
		*,
		weight=0,
		) -> int:
		if weight is None:
			return 0

		if (
			isinstance(
				weight,
				bool,
				)
			or not isinstance(
				weight,
				int,
				)
			or weight < 0
			):
			raise ValueError(
				"A Species generation weight must be a non-negative integer."
				)

		return weight

	@Record
	def SIZE_OPTIONS(
		target,
		*,
		size_options=(),
		) -> tuple[str, ...]:
		resolved = _tuple_report( size_options )

		if any(
			not isinstance(
				size,
				str,
				)
			or not size.strip()
			for size in resolved
			):
			raise ValueError(
				"Species Size options must be non-empty strings."
				)

		if len(
			set(
				resolved
				)
			) != len(
				resolved
				):
			raise ValueError(
				"Species Size options cannot contain duplicates."
				)

		return resolved

	@Record
	def SIZE_WEIGHTS(
		target,
		*,
		size_options=(),
		size_weights=None,
		) -> tuple[int, ...] | None:
		if size_weights is None:
			return None

		resolved_options = _tuple_report( size_options )
		resolved_weights = _tuple_report( size_weights )

		if len(
			resolved_weights
			) != len(
				resolved_options
				):
			raise ValueError(
				"Species Size weights must match its Size options."
				)

		if (
			not resolved_weights
			or any(
				isinstance(
					weight,
					bool,
					)
				or not isinstance(
					weight,
					int,
					)
				or weight < 0
				for weight in resolved_weights
				)
			or sum(
				resolved_weights
				) <= 0
			):
			raise ValueError(
				"Species Size weights must contain a positive integer total."
				)

		return resolved_weights

	@Record
	def SPEED(
		target,
		*,
		speed=None,
		) -> int | None:
		if speed is None:
			return None

		if (
			isinstance(
				speed,
				bool,
				)
			or not isinstance(
				speed,
				int,
				)
			or speed <= 0
			):
			raise ValueError(
				"A Species Speed must be a positive integer."
				)

		return speed

	@Record
	def DESCRIPTION(
		target,
		*,
		description=None,
		) -> str:
		"""
		What this Species is, for the person playing one.

		The docstrings elsewhere in this Kit are written for whoever maintains
		the rules.  This is the other audience: it says what it is like to be
		one of these, and it closes on a small suggestion rather than a hook,
		because a Species is not an adventure the way a Background is.
		"""
		if description is None:
			return ""

		if not isinstance(
			description,
			str,
			):
			raise ValueError(
				"A Species description must be text."
				)

		return description.strip()

	@Record
	def HERITAGES(
		target,
		*,
		heritages=(),
		) -> tuple[type[Heritage], ...]:
		resolved = _tuple_report( heritages )

		if len(
			set(
				resolved
				)
			) != len(
				resolved
				):
			raise ValueError(
				"A Species cannot declare one Heritage twice."
				)

		for heritage in resolved:
			if (
				not isinstance(
					heritage,
					type,
					)
				or not issubclass(
					heritage,
					Heritage,
					)
				or not issubclass(
					heritage,
					target,
					)
				):
				raise ValueError(
					f"{heritage!r} is not a Heritage of "
					f"{target.__name__}."
					)

		return resolved

	@Record
	def TRAITS(
		target,
		) -> tuple[type[Trait], ...]:
		return tuple(
			base
			for base in target.__bases__
			if (
				isinstance(
					base,
					type,
					)
				and issubclass(
					base,
					Trait,
					)
				)
			)


class Available(Declared_Species):
	"""Pin for Species available to the Player generator."""

	@Pre
	def Complete_Generator_Metadata(
		target,
		weight=0,
		size_options=(),
		speed=None,
		):
		return (
			weight > 0
			and bool(
				size_options
				)
			and speed is not None
			)


class NonPlayer_Only(Declared_Species):
	"""Pin for interim Species used only by NonPlayer generation."""


class Player_Handbook_2024(Available):
	"""Source Pin for the 2024 Player's Handbook Species."""

	@Record
	def SOURCE_TITLE(
		target,
		) -> str:
		return "Player's Handbook (2024)"

	@Record
	def SOURCE_URL(
		target,
		) -> str:
		return "https://www.dndbeyond.com/sources/dnd/phb-2024"

	@Record
	def SOURCE_LOCATOR(
		target,
		) -> str:
		return "Chapter 4: Character Origins — Species Descriptions"

	@Record
	def SOURCE_KIND(
		target,
		) -> str:
		return "official-reference"


class Homebrew(Available):
	"""Source Pin for project or third-party Species declarations."""

	@Record
	def SOURCE_TITLE(
		target,
		*,
		source_title=None,
		) -> str:
		resolved = (
			source_title
			or "Homebrew"
			)

		if not isinstance(
			resolved,
			str,
			):
			raise ValueError(
				"A homebrew Species source title must be text."
				)

		return resolved

	@Record
	def SOURCE_URL(
		target,
		*,
		source_url=None,
		) -> str:
		if source_url is None:
			return ""

		if not isinstance(
			source_url,
			str,
			):
			raise ValueError(
				"A homebrew Species source URL must be text."
				)

		return source_url

	@Record
	def SOURCE_LOCATOR(
		target,
		*,
		source_locator=None,
		) -> str:
		if source_locator is None:
			return ""

		if not isinstance(
			source_locator,
			str,
			):
			raise ValueError(
				"A homebrew Species source locator must be text."
				)

		return source_locator

	@Record
	def SOURCE_KIND(
		target,
		) -> str:
		return "homebrew"


class Legacy_NonPlayer(NonPlayer_Only):
	"""Source Pin for Species retained by the legacy NPC bridge."""

	@Record
	def SOURCE_TITLE(
		target,
		) -> str:
		return "GenLegend Legacy NPC Atlas"

	@Record
	def SOURCE_URL(
		target,
		) -> str:
		return ""

	@Record
	def SOURCE_LOCATOR(
		target,
		) -> str:
		return "AtlasAlusoris migration bridge"

	@Record
	def SOURCE_KIND(
		target,
		) -> str:
		return "project-legacy"


__all__ = (
	"Available",
	"Declared_Species",
	"Homebrew",
	"Legacy_NonPlayer",
	"NonPlayer_Only",
	"Player_Handbook_2024",
	)
