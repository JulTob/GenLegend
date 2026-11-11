"""
Fiendish Blood — which legacies a Tiefling carries.

Every Tiefling has one Heritage Tag (Abyssal, Chthonic or Infernal), and that
Tag keeps every rule it carries today.  The blood adds a second legacy, drawn
from the whole list at uniform random; the same legacy may come up twice,
which makes a pure blood, neither rarer nor commoner than any particular pair.
That is the Aasimar's rule for its two Ideals (``Map_of_Ideals``).

The blood is structure, and it stays hidden: the page never says a Tiefling
carries two hells.  What shows is the **aspect** (``Fiendish_Aspect``), the
look both legacies lend, collapsed once from their marks.

The blood also lends the **rules** (QST-0152, a house rule).  Each of the
three legacy spells (levels 1, 3 and 5) is lent by a legacy of the blood as
the dice fall: nothing forces a mixed blood to cast from both.  The one damage
Resistance is lent the same way.  A pure blood lends its legacy's own three
spells and Resistance, exactly as the published rule.

The draw happens once, in the Heritage's Imprint, from named Dice Bags that do
not depend on the level, so a level-up never hands anybody a different aspect
or different spells.  Reading the blood afterwards never rolls.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from AtlasActorLudi.SpeciesKit.Tieflings.Fiendish_Aspect import Collapse_Aspect
from AtlasActorLudi.SpeciesKit.Tieflings.Fiendish_Aspect import Fiendish_Aspect


@dataclass(
		frozen=True,
		)
class Fiendish_Blood:
	"""One Tiefling's legacies and the aspect they lend, drawn once and kept."""

	# One legacy for a pure blood, two for a mixed one; the Heritage first.
	legacies: tuple[type, ...]
	aspect: Fiendish_Aspect
	# The legacy that lends each spell place, in level order (1, 3, 5).
	spell_lenders: tuple[type, ...]
	# The legacy that lends the one damage Resistance.
	resistance_lender: type

	def __post_init__(
			self,
			) -> None:
		"""Check the blood as it is made: a broken legacy fails at the draw."""
		_check_spell_lenders(
				self.spell_lenders,
				)

	# A cached_property on a frozen dataclass: it works because the cache is
	# written straight into the instance's __dict__, past the frozen
	# __setattr__.  The value is derived only from frozen fields, so keeping
	# it never changes what the blood says.
	@cached_property
	def spells(
			self,
			) -> tuple[tuple[int, str], ...]:
		"""
		The legacy spells as ``(level, spell key)`` rows, like ``SPELLS``.

		Derived on the first read and kept: every later read is a lookup.  The
		lenders were checked when the blood was made; ``_spell_at_level`` still
		fails loudly if a legacy's ``SPELLS`` were changed since.
		"""
		return tuple(
				_spell_at_level(
						lender,
						level,
						)
				for level, lender in zip(
						SPELL_LEVELS,
						self.spell_lenders,
						strict=True,
						)
				)

	@property
	def resistance(
			self,
			) -> str:
		"""The one damage type this Tiefling resists."""
		return self.resistance_lender.DAMAGE_RESISTANCE

	@property
	def mixed(
			self,
			) -> bool:
		return len( self.legacies ) > 1

	@property
	def names(
			self,
			) -> tuple[str, ...]:
		return tuple(
				legacy.__name__
				for legacy in self.legacies
				)


# The character level each spell place arrives at, in place order.
SPELL_LEVELS = ( 1, 3, 5 )


def _spell_at_level(
		legacy,
		level: int,
		) -> tuple[int, str]:
	"""
	The one row of a legacy's ``SPELLS`` that arrives at ``level``.

	Looked up by level, never by position, so a legacy that lists its spells
	in another order still lends the right one; a legacy missing the level,
	or carrying it twice, fails loudly.
	"""
	rows = [
			row
			for row in legacy.SPELLS
			if row[0] == level
			]
	if len( rows ) != 1:
		raise ValueError(
				f"{legacy.__name__} must declare exactly one spell "
				f"at level {level}, not {len( rows )}."
				)
	return rows[0]


def _check_spell_lenders(
		spell_lenders: tuple[type, ...],
		) -> None:
	"""
	Fail loudly unless the blood has one lender per spell place, and every
	lender declares exactly one spell at its place's level.
	"""
	if len( spell_lenders ) != len( SPELL_LEVELS ):
		raise ValueError(
				f"A fiendish blood needs one spell lender per "
				f"place ({len( SPELL_LEVELS )}), not "
				f"{len( spell_lenders )}."
				)
	for level, lender in zip(
			SPELL_LEVELS,
			spell_lenders,
			strict=True,
			):
		_spell_at_level(
				lender,
				level,
				)


def _open_blood_dice(
		target,
		):
	"""The Dice Bag the second legacy is drawn from."""
	return target.Dice_Bag(
			"identity.species.Tiefling.fiendish_blood",
			version="1",
			namespace="GenLegendActor",
			)


def _draw_legacies(
		target,
		heritage,
		dice,
		) -> tuple[type, ...]:
	"""The Heritage, then a second legacy from the whole list (it may repeat)."""
	from AtlasActorLudi.SpeciesKit.Tieflings.base import Tiefling

	pool = list( Tiefling.HERITAGES )
	if heritage not in pool:
		raise ValueError(
				f"{heritage!r} is not a Tiefling legacy."
				)
	second = target.Pick(
			pool,
			dice=dice,
			)
	if second is heritage:
		return ( heritage, )
	return (
			heritage,
			second,
			)


def _open_rule_dice(
		target,
		):
	"""The Dice Bag the spell places and the Resistance are drawn from."""
	return target.Dice_Bag(
			"identity.species.Tiefling.fiendish_blood.rules",
			version="1",
			namespace="GenLegendActor",
			)


def _draw_spell_lenders(
		target,
		legacies,
		dice,
		) -> tuple[type, ...]:
	"""Which legacy lends each spell place: one draw per place, nothing forced."""
	return tuple(
			target.Pick(
					list( legacies ),
					dice=dice,
					)
			for _level in SPELL_LEVELS
			)


def _draw_resistance_lender(
		target,
		legacies,
		dice,
		) -> type:
	"""Which legacy lends the one damage Resistance."""
	return target.Pick(
			list( legacies ),
			dice=dice,
			)


def Draw_Fiendish_Blood(
		target,
		heritage,
		) -> Fiendish_Blood:
	"""
	Draw this Tiefling's blood, once and for life.

	Called from the Heritage's Imprint.  The replay contract, in one place:
	every draw of the blood has a Dice Bag of its own, each fresh for its
	purpose, so changing one draw never moves another.

	- ``identity.species.Tiefling.fiendish_blood``: the second legacy (here).
	- ``identity.species.Tiefling.fiendish_blood.rules``: the legacy that
	  lends each spell place, then the one that lends the Resistance (here).
	  Places before the Resistance: that order is part of the contract.
	- ``identity.species.Tiefling.fiendish_blood.rumour``: the place the
	  aspect suggests (opened in ``Collapse_Aspect``).
	- ``identity.species.Tiefling.fiendish_blood.aspect``: the collapse of the
	  look (opened in ``Collapse_Aspect``).
	- ``identity.species.Tiefling.fiendish_blood.voice``: the words the
	  grammar derives (opened in ``Collapse_Aspect``).
	"""
	legacies = _draw_legacies(
			target,
			heritage,
			_open_blood_dice( target ),
			)
	rule_dice = _open_rule_dice( target )
	spell_lenders = _draw_spell_lenders(
			target,
			legacies,
			rule_dice,
			)
	resistance_lender = _draw_resistance_lender(
			target,
			legacies,
			rule_dice,
			)
	return Fiendish_Blood(
			legacies=legacies,
			aspect=Collapse_Aspect(
					target,
					legacies,
					),
			spell_lenders=spell_lenders,
			resistance_lender=resistance_lender,
			)
