"""
Grammar of Aspect — the rewrite rules a Tiefling's aspect is written with.

The collapse (``Fiendish_Aspect``) chooses *what* a Tiefling looks like: the
marks.  This grammar chooses *how it is said*.  Each structure is a sequence
of sentence symbols (``Map_of_Marks``), and every symbol here has several
productions, some of them nesting further symbols.  The marks are the
lexicon, slotted in by name:

- ``{horn_shape}``  a verb phrase, plural ("sit close to your head like a crown")
- ``{horn_material}`` a bare noun phrase ("old ivory", "polished jet")
- ``{eyes}``        a verb phrase, plural ("are black, all but a vivid green iris")
- ``{fur}``         a noun phrase ("fox red, spotted with onyx black")
- ``{sheen}``       a metal ("silver", "cold iron")
- ``{scent}``       a noun phrase ("incense", "a doused campfire")
- ``{tail}``        a whole sentence, or nothing
- ``{place}``       where the bloodline is suggested to start ("Hades")

Every production must read as English for every item its slots can hold.
The self-test checks that the grammar is closed (every symbol has a rule,
every rule is used, every lexical item is one the aspect fills); whether
each derivation reads well is checked by reading them (QST-0151 review).
Words a production adds are not keyed, so a production should not reuse a
word a mark may bring ("short", "back", "close").
"""

from __future__ import annotations


GRAMMAR: dict[str, tuple[str, ...]] = {

	# --- Sentences -------------------------------------------------------

	"HORNS": (
		"Your horns {horn_shape}, and {LIKENESS}.",
		"Your horns {horn_shape}; {LIKENESS}.",
		"Your horns, {AS_IF_MADE}, {horn_shape}.",
		"Your horns {SEEM_MADE} {horn_material} and {horn_shape}.",
		),

	# Every framing must fit every eye mark, including the ones that change.
	"EYES": (
		"Your eyes {eyes}.",
		"As for your eyes, they {eyes}.",
		"Then there are your eyes: they {eyes}.",
		"Anyone who knows you can tell you that your eyes {eyes}.",
		),

	# Every production makes the fur or the coat its subject, so the "it" of
	# SHEEN that follows always has one.
	"FUR": (
		"Your fur is {fur}.",
		"Fine fur covers you: {fur}.",
		"Your coat is {fur}.",
		"A sleek coat covers you: {fur}.",
		),

	# Always follows FUR: "it" is the coat.
	"SHEEN": (
		"Where the light catches it, it shows a sheen of {sheen}.",
		"In lamplight it takes on a sheen of {sheen}.",
		"When you move, it shows a subtle sheen of {sheen}.",
		"It holds a sheen of {sheen}, the way old coins do.",
		),

	"TAIL": (
		"{tail}",
		),

	"SCENT": (
		"Whoever stands close enough catches a faint {SMELL} of {scent} about you.",
		"There is always a {SMELL} of {scent} about you, faint enough to doubt.",
		"You carry a faint {SMELL} of {scent}, though nobody can say where it comes from.",
		"A {SMELL} of {scent} lingers wherever you have been.",
		"The rooms you leave keep, for a moment, a {SMELL} of {scent}.",
		),

	"SCENT_OPENING": (
		"People notice it before they notice the horns: a faint {SMELL} of {scent} that follows you from room to room.",
		"The first thing anyone notices is the {SMELL} of {scent}: faint, and never quite explained.",
		),

	"PLACE": (
		"Your looks suggest your {LINE} {BEGINS} {place}.",
		"{WHO} would say your {LINE} {BEGINS} {place}.",
		),

	# No "back" at the end: BEGINS may already have said "back to".
	"PLACE_OPENING": (
		"Your looks suggest your {LINE} {BEGINS} {place}, though nobody can say how many generations ago.",
		"{WHO} would say your {LINE} {BEGINS} {place}, long ago.",
		),

	# --- Phrases ---------------------------------------------------------

	"LIKENESS": (
		"they hold the deep lustre of {horn_material}",
		"they resemble the finest {horn_material}",
		"they might have been carved from {horn_material}",
		"they gleam like {horn_material}",
		"they could pass for {horn_material} worked by a patient hand",
		),

	"AS_IF_MADE": (
		"as if carved from {horn_material}",
		"the colour of {horn_material}",
		"smooth as {horn_material}",
		"worked, it seems, from {horn_material}",
		),

	"SEEM_MADE": (
		"look like",
		"seem carved from",
		),

	"SMELL": (
		"smell",
		"scent",
		"hint",
		"breath",
		),

	"WHO": (
		"Anyone who knows the old signs",
		"Those who read such things",
		"A scholar of such matters",
		"The old stories",
		),

	"LINE": (
		"bloodline",
		"line",
		"blood",
		),

	"BEGINS": (
		"starts in",
		"begins in",
		"runs back to",
		"goes back to",
		),
	}
