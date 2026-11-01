"""
Map of Marks — every piece a Tiefling's aspect can be made of.

One row is one mark: its part (which slot it fills), the legacies that lend
it, its text, and its keys (the salient words it brings; no two marks in one
aspect may share a key).  The grammar each part's text must follow is written
on the part itself, in ``pins``.

What each legacy lends, in short (QST-0151, Julio's rulings of 2026-10-31):

- **Chthonic**: horns worn close like a crown, a tiara, a diadem (the least
  demonised of the three); pale, quiet materials; black eyes with one vivid
  colour; the coats of foxes, wolves and bulls, or the grey of a corpse;
  silver, pewter, iron; incense, myrrh, earth and stone.
- **Infernal**: horns that curl like a ram's or sweep back perfectly matched;
  jet, onyx, black iron; black eyes with a gold or ember iris; black or a
  flame's colours; gold, brass, copper; sulfur, a campfire just put out; the
  arrow-tipped tail.
- **Abyssal**: horns that twist, branch and spiral and never match; agate,
  nacre, a beetle's shell; eyes that will not keep one colour; the brightest
  coats, and markings that drift; bismuth, verdigris, electrum; storms, brine
  and things gone too sweet.

The hells themselves are never described here or anywhere on the page: the
aspect only suggests where a bloodline starts (``Fiendish_Aspect``).

The old fixed paragraphs (one per legacy, before QST-0151) were the source of
these rows; they are reworked into parts, not kept.
"""

from __future__ import annotations

from AtlasActorLudi.SpeciesKit.Tieflings.pins import Abyssal_Marks
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Chthonic_Marks
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Coat
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Coat_Pattern
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Eyes
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Horn_Material
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Horn_Shape
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Infernal_Marks
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Make_Mark
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Make_Structure
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Scent
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Sheen
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Tail


ABYSS = ( Abyssal_Marks, )
HADES = ( Chthonic_Marks, )
HELLS = ( Infernal_Marks, )
EVERY_LEGACY = (
		Abyssal_Marks,
		Chthonic_Marks,
		Infernal_Marks,
		)


# ---------------------------------------------------------------------------
# Structures: the order the sentences come in.  Each sentence is a symbol of
# the aspect's grammar (``Grammar_of_Aspect``), rewritten when the aspect is
# drawn; FUR and SHEEN always travel together, since the sheen says "it".
# ---------------------------------------------------------------------------

STRUCTURES = (
		Make_Structure(
				"Horns_First",
				"{HORNS}",
				"{EYES}",
				"{FUR} {SHEEN}",
				"{TAIL}",
				"{SCENT}",
				"{PLACE}",
				),
		Make_Structure(
				"Scent_First",
				"{SCENT_OPENING}",
				"{HORNS}",
				"{EYES}",
				"{FUR} {SHEEN}",
				"{TAIL}",
				"{PLACE}",
				),
		Make_Structure(
				"Place_First",
				"{PLACE_OPENING}",
				"{FUR} {SHEEN}",
				"{HORNS}",
				"{EYES}",
				"{TAIL}",
				"{SCENT}",
				),
		Make_Structure(
				"Eyes_First",
				"{EYES}",
				"{HORNS}",
				"{FUR} {SHEEN}",
				"{TAIL}",
				"{SCENT}",
				"{PLACE}",
				),
		)


# ---------------------------------------------------------------------------
# Horns: every legacy has its own shapes and its own materials.
# ---------------------------------------------------------------------------

HORN_SHAPES = (
		Make_Mark( "Horns_Crown", part=Horn_Shape, lent_by=HADES, keys=( "crown", "close" ),
				text="sit close to your head like a crown" ),
		Make_Mark( "Horns_Tiara", part=Horn_Shape, lent_by=HADES, keys=( "tiara", ),
				text="lie low along your temples like a tiara" ),
		Make_Mark( "Horns_Diadem", part=Horn_Shape, lent_by=HADES, keys=( "diadem", ),
				text="ring your brow in short points like a diadem" ),
		Make_Mark( "Horns_Ram", part=Horn_Shape, lent_by=HELLS, keys=( "ram", "back" ),
				text="curl back over your ears like a ram's" ),
		Make_Mark( "Horns_Swept", part=Horn_Shape, lent_by=HELLS, keys=( "swept", "back" ),
				text="sweep back from your brow in a perfectly matched pair" ),
		Make_Mark( "Horns_Spires", part=Horn_Shape, lent_by=HELLS, keys=( "spire", ),
				text="rise from your brow like two ridged spires" ),
		Make_Mark( "Horns_Twisted", part=Horn_Shape, lent_by=ABYSS, keys=( "twisted", ),
				text="grow in twisted spikes that never match" ),
		Make_Mark( "Horns_Barbed", part=Horn_Shape, lent_by=ABYSS, keys=( "barb", ),
				text="branch into barbs that never grow alike on both sides" ),
		Make_Mark( "Horns_Spiral", part=Horn_Shape, lent_by=ABYSS, keys=( "spiral", ),
				text="spiral in opposite directions as if neither asked the other" ),
		)

HORN_MATERIALS = (
		Make_Mark( "Horn_Ivory", part=Horn_Material, lent_by=HADES, keys=( "ivory", ),
				text="old ivory" ),
		Make_Mark( "Horn_Bone", part=Horn_Material, lent_by=HADES, keys=( "bone", ),
				text="sun-bleached bone" ),
		Make_Mark( "Horn_Antler", part=Horn_Material, lent_by=HADES, keys=( "antler", ),
				text="antler" ),
		Make_Mark( "Horn_Jet", part=Horn_Material, lent_by=HELLS, keys=( "jet", ),
				text="polished jet" ),
		Make_Mark( "Horn_Onyx", part=Horn_Material, lent_by=HELLS, keys=( "onyx", ),
				text="onyx" ),
		Make_Mark( "Horn_Black_Iron", part=Horn_Material, lent_by=HELLS, keys=( "iron", ),
				text="black iron" ),
		Make_Mark( "Horn_Agate", part=Horn_Material, lent_by=ABYSS, keys=( "agate", ),
				text="banded agate" ),
		Make_Mark( "Horn_Nacre", part=Horn_Material, lent_by=ABYSS, keys=( "pearl", ),
				text="mother-of-pearl" ),
		Make_Mark( "Horn_Beetle", part=Horn_Material, lent_by=ABYSS, keys=( "beetle", ),
				text="beetle shell" ),
		)


# ---------------------------------------------------------------------------
# Eyes.
# ---------------------------------------------------------------------------

EYES = (
		Make_Mark( "Eyes_Violet_Iris", part=Eyes, lent_by=HADES, keys=( "violet", "vivid" ),
				text="are black, all but a vivid violet iris" ),
		Make_Mark( "Eyes_Green_Iris", part=Eyes, lent_by=HADES, keys=( "green", "vivid" ),
				text="are black, all but a vivid green iris" ),
		Make_Mark( "Eyes_Ice_Iris", part=Eyes, lent_by=HADES, keys=( "ice", ),
				text="are black as a well, with irises of pale ice" ),
		Make_Mark( "Eyes_Coal_Iris", part=Eyes, lent_by=HELLS, keys=( "gold", "coal" ),
				text="are black, all but a golden iris that burns like a coal" ),
		Make_Mark( "Eyes_Ember_Iris", part=Eyes, lent_by=HELLS, keys=( "red", "ember" ),
				text="are black, with irises the red of embers in a grate" ),
		Make_Mark( "Eyes_Candle_Iris", part=Eyes, lent_by=HELLS, keys=( "gold", "candle", "flame" ),
				text="are black, and the gold of each iris flickers like a candle flame" ),
		Make_Mark( "Eyes_Moved", part=Eyes, lent_by=ABYSS, keys=( "mood", ),
				text="look ordinary until something moves you, and then their colour moves with it" ),
		Make_Mark( "Eyes_Mornings", part=Eyes, lent_by=ABYSS, keys=( "morning", ),
				text="are never the same colour two mornings running" ),
		Make_Mark( "Eyes_Blush", part=Eyes, lent_by=ABYSS, keys=( "mood", ),
				text="change colour with your mood, quick as a blush" ),
		)


# ---------------------------------------------------------------------------
# Fur: a coat colour, a pattern, and sometimes a second colour (the accent,
# drawn from the same coats).
# ---------------------------------------------------------------------------

COATS = (
		Make_Mark( "Coat_Electric_Blue", part=Coat, lent_by=ABYSS, keys=( "blue", ),
				text="electric blue" ),
		Make_Mark( "Coat_Acid_Green", part=Coat, lent_by=ABYSS, keys=( "green", ),
				text="acid green" ),
		Make_Mark( "Coat_Bright_Violet", part=Coat, lent_by=ABYSS, keys=( "violet", ),
				text="bright violet" ),
		Make_Mark( "Coat_Vivid_Magenta", part=Coat, lent_by=ABYSS, keys=( "magenta", "vivid" ),
				text="vivid magenta" ),
		Make_Mark( "Coat_Fox_Red", part=Coat, lent_by=HADES, keys=( "red", "fox" ),
				text="fox red" ),
		Make_Mark( "Coat_Wolf_Grey", part=Coat, lent_by=HADES, keys=( "grey", "wolf" ),
				text="wolf grey" ),
		Make_Mark( "Coat_Bull_Brown", part=Coat, lent_by=HADES, keys=( "brown", "bull" ),
				text="bull brown" ),
		Make_Mark( "Coat_Corpse_Grey", part=Coat, lent_by=HADES, keys=( "grey", "corpse" ),
				text="the grey-white of a corpse" ),
		Make_Mark( "Coat_Onyx_Black", part=Coat, lent_by=HELLS, keys=( "black", "onyx" ),
				text="onyx black" ),
		Make_Mark( "Coat_Flame_Red", part=Coat, lent_by=HELLS, keys=( "red", "flame" ),
				text="flame red" ),
		Make_Mark( "Coat_Ember_Orange", part=Coat, lent_by=HELLS, keys=( "orange", "ember" ),
				text="ember orange" ),
		Make_Mark( "Coat_Brimstone_Yellow", part=Coat, lent_by=HELLS, keys=( "yellow", "brimstone" ),
				text="brimstone yellow" ),
		)

COAT_PATTERNS = (
		# One colour.
		Make_Mark( "Pattern_Plain", part=Coat_Pattern, lent_by=EVERY_LEGACY,
				text="{a}" ),
		Make_Mark( "Pattern_Darker_Back", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "back", ),
				text="{a}, darker along your back" ),
		Make_Mark( "Pattern_Paler_Beneath", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "beneath", ),
				text="{a}, paler beneath" ),
		Make_Mark( "Pattern_Hound_Sleek", part=Coat_Pattern, lent_by=HADES, keys=( "hound", "close" ),
				text="{a}, sleek and close like a hound's" ),
		Make_Mark( "Pattern_Charred_Tips", part=Coat_Pattern, lent_by=HELLS, keys=( "tips", ),
				text="{a}, darkening at the tips like charred wood" ),
		# Two colours.
		Make_Mark( "Pattern_Spotted", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "spots", ),
				text="{a}, spotted with {b}" ),
		Make_Mark( "Pattern_Striped", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "stripes", ),
				text="{a}, striped with {b}" ),
		Make_Mark( "Pattern_Faded_Tips", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "tips", ),
				text="{a}, fading to {b} at the tips" ),
		Make_Mark( "Pattern_Back_And_Beneath", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "back", "beneath" ),
				text="{a} along your back and {b} beneath" ),
		Make_Mark( "Pattern_Mask", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "mask", ),
				text="{a}, with a mask of {b} around your eyes" ),
		Make_Mark( "Pattern_Blaze", part=Coat_Pattern, lent_by=HADES, keys=( "blaze", ),
				text="{a}, with a blaze of {b} on your chest" ),
		Make_Mark( "Pattern_Licking_Flame", part=Coat_Pattern, lent_by=HELLS, keys=( "flame", "tips" ),
				text="{a}, with {b} licking up from the tips like flame" ),
		Make_Mark( "Pattern_Drifting_Spots", part=Coat_Pattern, lent_by=ABYSS, keys=( "spots", ),
				text="{a}, with spots of {b} that drift a little every night" ),
		Make_Mark( "Pattern_Wandering_Stripes", part=Coat_Pattern, lent_by=ABYSS, keys=( "stripes", ),
				text="{a}, with stripes of {b} that never sit in the same place twice" ),
		)


# ---------------------------------------------------------------------------
# The sheen: every Tiefling's fur catches the light like metal, subtly.
# ---------------------------------------------------------------------------

SHEENS = (
		Make_Mark( "Sheen_Silver", part=Sheen, lent_by=HADES, keys=( "silver", ),
				text="silver" ),
		Make_Mark( "Sheen_Pewter", part=Sheen, lent_by=HADES, keys=( "pewter", ),
				text="pewter" ),
		Make_Mark( "Sheen_Iron", part=Sheen, lent_by=HADES, keys=( "iron", "cold" ),
				text="cold iron" ),
		Make_Mark( "Sheen_Gold", part=Sheen, lent_by=HELLS, keys=( "gold", ),
				text="gold" ),
		Make_Mark( "Sheen_Brass", part=Sheen, lent_by=HELLS, keys=( "brass", ),
				text="brass" ),
		Make_Mark( "Sheen_Copper", part=Sheen, lent_by=HELLS, keys=( "copper", ),
				text="copper" ),
		Make_Mark( "Sheen_Bismuth", part=Sheen, lent_by=ABYSS, keys=( "bismuth", ),
				text="bismuth" ),
		Make_Mark( "Sheen_Verdigris", part=Sheen, lent_by=ABYSS, keys=( "verdigris", ),
				text="verdigris" ),
		Make_Mark( "Sheen_Electrum", part=Sheen, lent_by=ABYSS, keys=( "electrum", ),
				text="electrum" ),
		)


# ---------------------------------------------------------------------------
# Scents: faint, and never explained.
# ---------------------------------------------------------------------------

SCENTS = (
		Make_Mark( "Scent_Incense", part=Scent, lent_by=HADES, keys=( "incense", ),
				text="incense" ),
		Make_Mark( "Scent_Myrrh", part=Scent, lent_by=HADES, keys=( "myrrh", ),
				text="myrrh" ),
		Make_Mark( "Scent_Stone_After_Rain", part=Scent, lent_by=HADES, keys=( "stone", "rain", "cold" ),
				text="cold stone after rain" ),
		Make_Mark( "Scent_Turned_Earth", part=Scent, lent_by=HADES, keys=( "earth", ),
				text="freshly turned earth" ),
		Make_Mark( "Scent_Sulfur", part=Scent, lent_by=HELLS, keys=( "sulfur", ),
				text="sulfur" ),
		Make_Mark( "Scent_Campfire", part=Scent, lent_by=HELLS, keys=( "campfire", ),
				text="a doused campfire" ),
		Make_Mark( "Scent_Hot_Iron", part=Scent, lent_by=HELLS, keys=( "iron", ),
				text="hot iron" ),
		Make_Mark( "Scent_Snuffed_Candle", part=Scent, lent_by=HELLS, keys=( "candle", ),
				text="a snuffed candle" ),
		Make_Mark( "Scent_Storm", part=Scent, lent_by=ABYSS, keys=( "storm", ),
				text="the air before a storm" ),
		Make_Mark( "Scent_Brine", part=Scent, lent_by=ABYSS, keys=( "brine", ),
				text="brine" ),
		Make_Mark( "Scent_Old_Flowers", part=Scent, lent_by=ABYSS, keys=( "flowers", ),
				text="flowers left too long in the vase" ),
		Make_Mark( "Scent_Spilled_Wine", part=Scent, lent_by=ABYSS, keys=( "wine", ),
				text="spilled wine" ),
		)


# ---------------------------------------------------------------------------
# Tails: only the Nine Hells lend one.  A blood with another legacy in it may
# also have none (``Fiendish_Aspect``).
# ---------------------------------------------------------------------------

TAILS = (
		Make_Mark( "Tail_Arrow", part=Tail, lent_by=HELLS, keys=( "arrow", ),
				text="You also have a long tail that ends in an arrow-shaped tip." ),
		Make_Mark( "Tail_Barb", part=Tail, lent_by=HELLS, keys=( "arrow", "barb" ),
				text="A thin tail follows you, ending in a barb like an arrowhead." ),
		)


ROSTER = (
		*STRUCTURES,
		*HORN_SHAPES,
		*HORN_MATERIALS,
		*EYES,
		*COATS,
		*COAT_PATTERNS,
		*SHEENS,
		*SCENTS,
		*TAILS,
		)
