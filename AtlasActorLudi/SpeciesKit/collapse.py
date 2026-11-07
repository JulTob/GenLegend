"""
Collapse — a small wave-function collapse over named slots.

A **wave** is a handful of slots, and each slot holds the candidates it may
still become.  Collapsing repeats three steps until every slot holds exactly
one value:

1. **Choose the slot.**  The open slot with the fewest candidates left (the
   lowest entropy) goes first; on a tie, the one declared first.
2. **Draw its value.**  One of its candidates, with the Character's own dice
   (Decree 0002).  A slot with a single candidate takes it without rolling.
3. **Propagate.**  Every rule may narrow the other slots, given what has been
   drawn so far, and the rules run again until nothing changes.

A slot left with no candidates is a contradiction.  The wave then starts again
from its first state, drawing on from the same dice, so the result is still a
pure function of the Character's seed.  After ``ATTEMPTS`` contradictions in a
row the collapse fails loudly: the data cannot be satisfied.

``ABSENT`` is a candidate like any other, meaning "this slot stays empty".

Nothing here knows about Tieflings.  A rule is a plain function

	rule( drawn, domains ) -> domains

where ``drawn`` maps each collapsed slot to its value, and ``domains`` maps
every slot to the candidates it still holds.  A rule returns the domains it
narrowed; it never adds a candidate back.  A rule that did could undo another
rule's work forever, so propagation checks every rule's answer and fails
loudly (``Collapse_Rule_Error``) on a rule that widens a slot, adds one or
drops one.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


ATTEMPTS = 12


class _Absent:
	"""The value of a slot that stays empty."""

	def __repr__(
			self,
			) -> str:
		return "ABSENT"


ABSENT = _Absent()


@dataclass(
		frozen=True,
		)
class Slot:
	"""One place in the wave, and every candidate it starts with."""

	name: str
	candidates: tuple


Domains = dict[str, tuple]
Drawn = dict[str, object]
Rule = Callable[[Drawn, Domains], Domains]


class Collapse_Contradiction(RuntimeError):
	"""The rules left a slot with no candidate, every time."""


class Collapse_Rule_Error(ValueError):
	"""A rule broke the contract: it may only narrow the slots it is given."""


def _lowest_entropy(
		slots: tuple[Slot, ...],
		drawn: Drawn,
		domains: Domains,
		) -> str:
	"""The open slot with the fewest candidates; the first declared on a tie."""
	open_slots = [
			slot.name
			for slot in slots
			if slot.name not in drawn
			]
	return min(
			open_slots,
			key=lambda name: len( domains[name] ),
			)
		#-- min() keeps the first of equals, so declaration order breaks ties.


def _draw(
		target,
		candidates: tuple,
		dice,
		):
	"""One candidate: the only one, or one drawn from the Character's dice."""
	if len( candidates ) == 1:
		return candidates[0]
	return target.Pick(
			list( candidates ),
			dice=dice,
			)


def _rule_name(
		rule: Rule,
		) -> str:
	"""A rule's name for an error message (a partial has none of its own)."""
	return getattr(
			rule,
			"__name__",
			repr( rule ),
			)


def _check_only_narrows(
		rule: Rule,
		before: Domains,
		after: Domains,
		) -> None:
	"""Fail loudly unless the rule kept every slot and only removed candidates."""
	if set( after ) != set( before ):
		raise Collapse_Rule_Error(
				f"Collapse: rule {_rule_name( rule )} added or dropped a slot."
				)
	for name, candidates in after.items():
		if not set( candidates ) <= set( before[name] ):
			raise Collapse_Rule_Error(
					f"Collapse: rule {_rule_name( rule )} added a candidate "
					f"back to slot {name!r}."
					)


def _propagate(
		rules: tuple[Rule, ...],
		drawn: Drawn,
		domains: Domains,
		) -> Domains:
	"""
	Run every rule until no domain narrows any further.

	This ends because every pass either removes a candidate or stops, and a
	wave holds finitely many.  That holds only while rules never add a
	candidate back, so each rule's answer is checked (``_check_only_narrows``).
	"""
	while True:
		narrowed = dict( domains )
		for rule in rules:
			answer = rule(
					drawn,
					narrowed,
					)
			_check_only_narrows(
					rule,
					narrowed,
					answer,
					)
			narrowed = answer
		if narrowed == domains:
			return domains
		domains = narrowed


def _has_contradiction(
		domains: Domains,
		) -> bool:
	return any(
			len( candidates ) == 0
			for candidates in domains.values()
			)


def _collapse_once(
		target,
		slots: tuple[Slot, ...],
		rules: tuple[Rule, ...],
		dice,
		) -> Drawn | None:
	"""One attempt at the whole wave; ``None`` on a contradiction."""
	drawn: Drawn = {}
	domains: Domains = {
			slot.name: tuple( slot.candidates )
			for slot in slots
			}
	domains = _propagate(
			rules,
			drawn,
			domains,
			)
	while len( drawn ) < len( slots ):
		if _has_contradiction( domains ):
			return None
		name = _lowest_entropy(
				slots,
				drawn,
				domains,
				)
		value = _draw(
				target,
				domains[name],
				dice,
				)
		drawn[name] = value
		domains[name] = ( value, )
		domains = _propagate(
				rules,
				drawn,
				domains,
				)
	if _has_contradiction( domains ):
		return None
	return drawn


def Collapse(
		target,
		slots: tuple[Slot, ...],
		rules: tuple[Rule, ...],
		dice,
		) -> Drawn:
	"""
	Collapse the wave into one value per slot, with the Character's dice.

	Deterministic for a given seed and Dice Bag: the slot order, the rules and
	the dice decide everything, and no set or hash order is ever consulted.
	"""
	if not slots:
		raise ValueError(
				"Collapse: a wave needs at least one slot."
				)
	names = [
			slot.name
			for slot in slots
			]
	if len( set( names ) ) != len( names ):
		raise ValueError(
				"Collapse: every slot needs its own name."
				)
	for _attempt in range( ATTEMPTS ):
		drawn = _collapse_once(
				target,
				slots,
				rules,
				dice,
				)
		if drawn is not None:
			return drawn
	raise Collapse_Contradiction(
			f"Collapse: the rules left a slot empty {ATTEMPTS} times in a row."
			)
