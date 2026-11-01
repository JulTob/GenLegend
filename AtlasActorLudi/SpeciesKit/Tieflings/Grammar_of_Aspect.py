"""
Grammar of Aspect — the rewrite rules a Tiefling's aspect is written with.

An Aasimar's talaria and halo are emotional anchors: they make the reader
feel something.  A Tiefling's anchor is how the world takes them.  Nobody
describes a Tiefling neutrally: every word said about them rings of insult or
fear, and what they feel back is frustration, fear and anger, and the
constant arithmetic of passing or hiding.  So this grammar does not only say
what a Tiefling looks like; it says what the looks *mean* to the people
looking (QST-0153, an experiment on Julio's idea of 2026-11-01).

The collapse (``Fiendish_Aspect``) chooses what is said; this grammar chooses
how.  Sentences are built the generative way, with a start that several
endings can finish: "Strangers see the horns first, and you a long time
after:" + any horn phrase.  The marks are the lexicon:

- ``{horns}`` / ``{eyes}`` / ``{scent}`` / ``{tail}`` / ``{bearing}``: a mark's
  own sentences
- ``{horn_phrase}`` / ``{eyes_phrase}`` / ``{scent_phrase}``: the same marks as
  noun phrases, to finish someone else's sentence
- ``{omen}``: what people say a scent means ("a funeral")
- ``{horn_material}``, ``{fur}``, ``{sheen}``, ``{place}``: as before
- ``{full_name}``: kept as it is and filled when the sheet is printed, since
  the name is settled after the Species (``{full_name}`` rather than
  ``{name}`` until #124: a name may start with a title)

Every production must read as English for every item its slots can hold, and
none breaks the flow with a semicolon.  Words a production adds are not
keyed, so a production should not reuse a word a mark may bring.
"""

from __future__ import annotations


GRAMMAR: dict[str, tuple[str, ...]] = {

	# --- Sentences -------------------------------------------------------

	# A lead is listed twice beside a mark's own sentence on purpose: two in
	# three times, the look is said through how someone else meets it.
	"HORNS": (
		"{horns}",
		"{HORNS_LEAD}: {horn_phrase}.",
		"{HORNS_LEAD}: {horn_phrase}.",
		),

	"EYES": (
		"{eyes}",
		"{EYES_LEAD}: {eyes_phrase}.",
		"{EYES_LEAD}: {eyes_phrase}.",
		),

	# {fur} may carry commas of its own, so every sentence ends on it.
	"FUR": (
		"Your fur carries {SCARS}, and no cloak quite covers it: {fur}.",
		"{FUR_LEAD}, a glint of {sheen} gives you away in your fur, which is {fur}.",
		"Lamplight finds {sheen} in your fur, which is {fur}.",
		"Your fur carries {SCARS}, and its colour is {fur}.",
		),

	"SCENT": (
		"{scent}",
		"{SAY_SCENT} you smell like {omen}, of {scent_phrase}.",
		"{SAY_SCENT} you smell like {omen}.",
		),

	"TAIL": (
		"{tail}",
		),

	"BEARING": (
		"{bearing}",
		),

	"PLACE": (
		"{WHO} would say your {LINE} {BEGINS} {place}.",
		"{HOSTILE} say your {LINE} {BEGINS} {place}, as if that settled anything.",
		"{HOSTILE} say your {LINE} {BEGINS} {place}, and they say it loudly.",
		"Some whisper that your {LINE} comes from {place} itself.",
		),

	# --- Leads: how the world meets the look -----------------------------

	"HORNS_LEAD": (
		"{full_name}'s face is of great beauty, but most people only notice the horns",
		"Strangers see the horns first, and you a long time after",
		"Children point at the horns before their parents pull them away",
		"No hat has ever sat right on you, and no innkeeper has ever missed why",
		),

	"EYES_LEAD": (
		"Few people hold your gaze for long",
		"Innkeepers look anywhere but at your eyes",
		"Priests make a quiet sign when they meet your eyes",
		"Mothers tell their children not to look at your eyes",
		),

	"FUR_LEAD": (
		"However you dress",
		"Under any hood",
		"In any crowd",
		),

	"SCARS": (
		"old scars, the kind a crowd leaves",
		"a scar for every town that wanted you gone",
		"the marks of more than one thrown stone",
		),

	"SAY_SCENT": (
		"People say",
		"Behind your back, they say",
		"You have been told, more than once, that",
		),

	# --- The place: named, never described --------------------------------

	"WHO": (
		"Anyone who knows the signs",
		"Those who read such things",
		"A scholar of such matters",
		),

	"HOSTILE": (
		"Those who spit at your feet",
		"The priests who turned you away",
		"The ones who throw stones",
		),

	"LINE": (
		"bloodline",
		"line",
		"blood",
		),

	"BEGINS": (
		"starts in",
		"begins in",
		"rises from",
		"was first kindled in",
		),
	}
