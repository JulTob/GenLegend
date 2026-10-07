"""
Map of Familiars — the special forms Pact of the Chain unlocks.

Find Familiar's ordinary forms are animals.  Pact of the Chain adds eight that
are not, and a Warlock who takes the invocation is choosing one of *these*, so
the choice belongs on the sheet rather than as a list of names in a paragraph
nobody reads twice.

The choice is drawn, not enumerated: one form arrives on the sheet, the way a
Background draws one tool from the Artisan list.  But it is not drawn blind.
Each form declares an ``affinity``, and a caster whose patron matches is far
more likely to be answered by it — a Fiend patron gets an Imp long before it
gets a Sphinx of Wonder.  That is **Familial Preference**, and it is the same
idea the Find Familiar spell should use for ordinary animals.

Stat blocks are deliberately absent.  This is a sheet generator, and the eight
forms are printed in the Monster Manual; what the sheet needs is *which one
answered*, and why it would.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# How much a matching patron outweighs an indifferent one.  High enough that
# preference reads as preference at the table, low enough that a Fiend warlock
# can still, occasionally, be answered by something unexpected.
AFFINITY_WEIGHT = 8


@dataclass(
	frozen=True,
	)
class Familiar:
	"""One special familiar form, and who it tends to answer."""

	name: str
	kind: str
	size: str = "Tiny"
	# Words that, appearing in what the caster *is*, pull this form forward.
	affinity: tuple[str, ...] = field(
		default_factory=tuple,
		)
	note: str = ""

	def line(
			self,
			) -> str:
		"""One-line summary for the sheet."""
		tail = f" — {self.note}" if self.note else ""

		return f"{self.name} ({self.size} {self.kind}){tail}"


PACT_FAMILIARS = {
	record.name: record
	for record in (
		Familiar(
			name="Imp",
			kind="Fiend",
			affinity=(
				"Fiend",
				),
			note="shapechanger, invisible at will, and a liar by construction",
			),
		Familiar(
			name="Quasit",
			kind="Fiend",
			affinity=(
				"Fiend",
				),
			note="shapechanger, and frightening on purpose",
			),
		Familiar(
			name="Sphinx of Wonder",
			kind="Celestial",
			affinity=(
				"Celestial",
				),
			note="small, radiant, and better read than you are",
			),
		Familiar(
			name="Sprite",
			kind="Fey",
			affinity=(
				"Archfey",
				),
			note="invisible, and knows whether you are lying",
			),
		Familiar(
			name="Pseudodragon",
			kind="Dragon",
			affinity=(
				"Archfey",
				"Draconic",
				"Sorcerer",
				),
			note="companionable, and stings",
			),
		Familiar(
			name="Slaad Tadpole",
			kind="Aberration",
			affinity=(
				"Great Old One",
				"Aberrant",
				),
			note="wrong in a way nobody can name",
			),
		Familiar(
			name="Skeleton",
			kind="Undead",
			size="Medium",
			affinity=(
				"Undead",
				"Necromancy",
				"Death",
				),
			note="obedient, tireless, and entirely past caring",
			),
		Familiar(
			name="Venomous Snake",
			kind="Beast",
			affinity=(),
			note="asks nothing and answers anyone",
			),
		)
	}


def _caster_marks(
		char,
		) -> str:
	"""What the caster is, as one searchable string."""
	return " ".join(
		str(
			mark or ""
			)
		for mark in (
			getattr(
				char,
				"char_class",
				None,
				),
			getattr(
				char,
				"subclass",
				None,
				),
			getattr(
				char,
				"species",
				None,
				),
			# TagKit composes a Target's Tags into its type name, so this is
			# Tag membership asked in the cheapest way available here.
			type(
				char
				).__name__,
			)
		)


def pick_familiar(
		char,
		pool=None,
		*,
		dice,
		) -> Familiar:
	"""
	Draw one familiar form, weighted by Familial Preference.

	A form whose affinity matches what the caster is comes forward far more
	readily.  Nothing is excluded: an unexpected answer is a story.
	"""
	forms = list(
		pool
		or PACT_FAMILIARS.values()
		)
	marks = _caster_marks(
		char
		)
	weights = [
		AFFINITY_WEIGHT
		if any(
			word.lower() in marks
			for word in record.affinity
			)
		else 1
		for record in forms
	]
	names = [
		record.name
		for record in forms
		]

	return PACT_FAMILIARS[
		char.Pick(
			names,
			weights,
			dice=dice,
			)
		]
		#-- ``dice`` is the bag the offering Tag opened (Pact_Familiar.familiar)


__all__ = (
	"AFFINITY_WEIGHT",
	"Familiar",
	"PACT_FAMILIARS",
	"pick_familiar",
	)
