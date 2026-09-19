"""
Bard Colleges.

The Guild's core is **attention**. Each College does something different to
that one substance rather than spending it: Dance watches, Glamour commands,
Lore keeps, Valor holds. Every text is a song, and each carries a refrain
that returns changed.

The songs and the lesson lines are Julio's, settled on the wiki pages
"Class: Bard" and "Class: Bard: College of ...".

Breaks are explicit per Documenta/Canon/Feature-Text.md. Nothing may reflow
these, and a renderer that inserted its own breaks would destroy the verses.
"""

from AtlasLusoris.GuildKit import Bard
from AtlasLusoris.GuildKit import Build_Specialization


# Julio's, from the wiki.  **Watching.**  "They watch you. You watch them.
# Your crew watches you watching."  The eye is the whole economy here, and
# the dancer is the one place all three lines of sight meet.
#
# This is the one College a mute Character can play the whole way up, so
# the song opens by refusing speech: Bardic Inspiration reaches a creature
# that can see *or* hear, and a wordless performer inspires by the rules
# rather than by our indulgence.
#
# The joke underneath is the dancefloor that is also a killing floor. The
# room claps along, reads a party, and does not notice the floor thinning.
# "Stay on the beat" is the refrain and the whole defence, because the
# Armor Class this College buys is bought by being watched.
DANCE_DESCRIPTION = (
	"Do not speak.<br>"
	"Speaking would only slow you down.<br>"
	"No sound, but the sound of your feet.<br>"
	"There are plenty of ways you can win this.<br>"
	"Let them clap.<br>"
	"Let them think this is a party.<br>"
	"Stay on the beat."
	)
Dance = Build_Specialization(
	guild=Bard,
	name="Dance",
	module=__name__,
	extends=DANCE_DESCRIPTION,
	heading="College of Dance",
	)
# Julio's, from the wiki.  **Commands.**  Attention that obeys.  Here
# attention is the weapon rather than the means: they look, and then they
# comply.  The organising idea is royalty nobody ever audited.  You are the
# master of your destiny because you say so and carry it without blinking,
# and the only work in the whole College is convincing the room you are
# right about that.
#
# Julio calls it the pyrite problem, and the last line is where it lands:
# gold is what it looks like, not what it was assayed as.  The College is
# glorious and it is fool's gold, and both at once is the point.  The
# earlier draft closed on burning out rather than fading, which was a
# borrowed line; this one is ours and says more.
GLAMOUR_DESCRIPTION = (
	"Here you are, born to shine.<br>"
	"You glow like a shooting star.<br>"
	"Head high. Hands wide open.<br>"
	"Presence is the word.\n\n"
	"Master of your destiny.<br>"
	"Ruler of your own world.<br>"
	"And you must carry yourself as such.<br>"
	"They only have to believe you.<br>"
	"They do. They will.\n\n"
	"You are a bright light.<br>"
	"Shining, glittering, just like gold."
	)
Glamour = Build_Specialization(
	guild=Bard,
	name="Glamour",
	module=__name__,
	extends=GLAMOUR_DESCRIPTION,
	heading="College of Glamour",
	)
# Julio's, from the wiki.  **Keeps.**  Memory is attention that survived,
# so this College is the one that never let go.  The anaphora on "One"
# answers the "Somebody has to" of Valor, and each College keeps its own
# device.
#
# "You are what is left" is the whole College in four words, and it earns
# the three losses stacked in front of it.  The close is Cutting Words
# written as fantasy and never as a rule.
LORE_DESCRIPTION = (
	"They are counting on you to forget.<br>"
	"One promise. One name nobody says.<br>"
	"One treaty nobody kept.<br>"
	"One story everybody agreed to replace.<br>"
	"You keep all of it. Word for word.<br>"
	"The books burn. The witnesses die.<br>"
	"The song gets the ending wrong.<br>"
	"You are what is left."
	)
Lore = Build_Specialization(
	guild=Bard,
	name="Lore",
	module=__name__,
	extends=LORE_DESCRIPTION,
	heading="College of Lore",
	)
# Julio's, from the wiki.  **Holds.**  Legends are attention made immortal.
# To hold attention on something is to refuse to look away from it:
# cowardice is the flinch, and valor is the held gaze.  This Bard holds the
# eye, their own and their allies' and the whole hall's, on the terror and
# the glory, in the one place attention is hardest to hold, which is the
# open field under threat where every instinct says run or look away.
# Holding the line and holding the gaze are the same act.  That is why this
# is a College of Valor and not some other colour of Bard.
#
# So the song is an elegy and not a stomp.  Nobody in the line gets old and
# the singer knows it first.  The anaphora on "Somebody has to" builds to
# "That should be you", which is the whole decision the College makes, and
# the last two lines are the deal: you may live forever in a song, and you
# will not be holding the pen.  The lesson lines keep the same grip, each
# one a form of hold.
VALOR_DESCRIPTION = (
	"Nobody wants to live forever. Not in your line of work.\n\n"
	"Somebody has to fill the dreams.<br>"
	"Somebody has to go out there and record the stories.<br>"
	"Somebody has to inspire the heroes yet to be.<br>"
	"Somebody has to stand up against an immense threat. And, hopefully, "
	"come out victorious.<br>"
	"That should be you.<br>"
	"You may get to live forever in a song.<br>"
	"Make it worth writing down.<br>"
	"Even when you will not be the one writing it down."
	)
Valor = Build_Specialization(
	guild=Bard,
	name="Valor",
	module=__name__,
	extends=VALOR_DESCRIPTION,
	heading="College of Valor",
	)

SPECIALIZATIONS = (
	Dance,
	Glamour,
	Lore,
	Valor,
	)
