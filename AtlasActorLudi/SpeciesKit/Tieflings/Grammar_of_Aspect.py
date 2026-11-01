"""
Grammar of Aspect — the rewrite rules a Tiefling's aspect is written with.

The collapse (``Fiendish_Aspect``) chooses *what* a Tiefling looks like and
which few things the presentation dwells on.  This grammar chooses *how it is
said*.  Each structure is a sequence of sentence symbols (``Map_of_Marks``);
every symbol here rewrites to one of several productions.  The marks are the
lexicon, slotted in by name, and the marks said on their own bring whole
sentences of their own, several each:

- ``{horns}``       a horn shape's sentences, with ``{horn_material}`` inside
- ``{horn_material}`` a bare noun phrase ("old ivory", "polished jet")
- ``{eyes}``        the eyes' sentences
- ``{fur}``         a noun phrase ("fox red, spotted with onyx black")
- ``{sheen}``       a bare metal ("silver", "copper")
- ``{scent}``       a scent's sentences
- ``{tail}``        a tail's sentences
- ``{place}``       where the bloodline is suggested to start ("Hades")

Every production must read as English for every item its slots can hold, and
none breaks the flow with a semicolon.  The self-test checks that the grammar
is closed (every symbol has a rule, every rule is used, every lexical item is
one the aspect fills); whether each derivation reads well is checked by
reading them.  Words a production adds are not keyed, so a production should
not reuse a word a mark may bring.
"""

from __future__ import annotations


GRAMMAR: dict[str, tuple[str, ...]] = {

	# --- Sentences -------------------------------------------------------

	"HORNS": (
		"{horns}",
		),

	"EYES": (
		"{eyes}",
		),

	# The fur and its sheen are one image.  {fur} may carry commas of its own
	# ("wolf grey, striped with onyx black"), so it never sits between two
	# more commas: it ends a clause.
	"FUR": (
		"Your fur is {fur}, and where the light catches it, it gleams like {sheen}.",
		"Your coat is {fur}, and it holds a sheen of {sheen}, the way old coins do.",
		"Your fur takes the light like {sheen}, and its colour is {fur}.",
		"A glint of {sheen} runs through your fur, which is {fur}.",
		),

	"TAIL": (
		"{tail}",
		),

	"SCENT": (
		"{scent}",
		),

	"PLACE": (
		"Your looks suggest your {LINE} {BEGINS} {place}.",
		"{WHO} would say your {LINE} {BEGINS} {place}.",
		"{WHO} would trace your {LINE} back to {place}.",
		),

	# No "back" at the end: BEGINS may already have said "back to".
	"PLACE_OPENING": (
		"Your looks suggest your {LINE} {BEGINS} {place}, though nobody can say how many generations ago.",
		"{WHO} would trace your {LINE} back to {place}, though not how far.",
		),

	# --- Phrases ---------------------------------------------------------

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
