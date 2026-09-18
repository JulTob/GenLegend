"""
Bard Colleges.

The Guild's core is **attention**, and each College does something different
to it rather than spending it: Dance distracts, Glamour attracts, Lore keeps,
Valor misdirects. Every text is a song, in the register the class settled on,
and each carries a refrain that returns changed.

Breaks are explicit per Documenta/Canon/Feature-Text.md. Nothing may reflow
these, and a renderer that inserted its own breaks would destroy the verses.
"""

from AtlasLusoris.GuildKit import Bard
from AtlasLusoris.GuildKit import Build_Specialization


# Julio's, 2026-09-18.  **Distracts.**  The eye is a thing you can move, so
# you move it somewhere useless and leave it there.  This is the one College
# a mute Character can play the whole way up: Bardic Inspiration reaches a
# creature that can see *or* hear, so a wordless performer inspires by the
# rules rather than by our indulgence, and the text opens by refusing speech.
#
# The song underneath is the band's funk record, and the joke it carries is
# the dancefloor that is actually a killing floor: the room claps along,
# reads a party, and does not notice the floor getting less crowded.  "Stay
# on the beat" is the refrain and the whole defence, because the Armor Class
# this College buys is bought by being watched.
DANCE_DESCRIPTION = (
	"Do not speak.<br>"
	"Speaking would only slow you down.<br>"
	"No sound, but the sound of your feet.<br>"
	"There are plenty of ways you can win this match.<br>"
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
# Julio's, 2026-09-18.  **Attracts.**  Attention is the weapon here rather
# than the means: they look, and then they comply.  The organising idea is
# royalty nobody ever audited.  You are the master of your destiny because
# you say so and carry it without blinking, and the only work in the whole
# College is convincing the room you are right about that.
#
# The register is the imperious fanfare, and it closes on burning out rather
# than fading, which is the duende this class needs to stay out of whimsy:
# the light is worth it because it is spent.
GLAMOUR_DESCRIPTION = (
	"Here you are, born to shine.<br>"
	"You pass like a shooting star.<br>"
	"Head high. Hands gesturing.<br>"
	"Presence is the word.\n\n"
	"You are the master of your destiny.<br>"
	"The ruler of your own world.<br>"
	"And you carry yourself as such.<br>"
	"Your only job, to convince others you are right on that.\n\n"
	"You are a bright light.<br>"
	"And it's better to burn out, than to fade away."
	)
Glamour = Build_Specialization(
	guild=Bard,
	name="Glamour",
	module=__name__,
	extends=GLAMOUR_DESCRIPTION,
	heading="College of Glamour",
	)
# Julio's, 2026-09-18.  **Keeps.**  Memory is attention that survived, so
# this College is the one that never let go of the thread.  The anaphora on
# "One" is the College's own device, answering the "Somebody has to" of
# Valor, and it comes from the single-minded song underneath: one vision,
# held while everybody else agrees to a more comfortable version.
#
# "You are what is left" is the whole College in four words.  The close is
# Cutting Words written as fantasy and never as a rule: the small true thing,
# said at exactly the wrong moment, and a house coming down on one sentence.
LORE_DESCRIPTION = (
	"They are counting on you to forget.\n\n"
	"One night. One promise. One name nobody says out loud any more.<br>"
	"One treaty nobody kept. One story everybody agreed to tell "
	"differently.<br>"
	"You keep all of it. Word for word. For thirty years, if that is what "
	"it takes.\n\n"
	"The books burn. The witnesses die. The song gets the ending wrong.<br>"
	"You are what is left.\n\n"
	"So follow the thread back, through the toasts and the very convenient "
	"silences,<br>"
	"down to the one small true thing at the end.<br>"
	"Then say it out loud at exactly the wrong moment,<br>"
	"and watch a great house come apart on a single sentence."
	)
Lore = Build_Specialization(
	guild=Bard,
	name="Lore",
	module=__name__,
	extends=LORE_DESCRIPTION,
	heading="College of Lore",
	)
# Julio's, 2026-09-18.  **Misdirects.**  The song underneath is an elegy
# rather than a stomp, and that is what makes this College work: nobody in
# the line gets old, and the singer knows it first.  So Valor is not
# cheerleading.  It is the war elegy, sung at death rather than about it,
# and the misdirection is what the chant does to a soldier's attention when
# the alternative is counting the enemy.
#
# The anaphora on "Somebody has to" builds to "That should be you", which is
# the whole decision this College makes.  The last two lines are the deal:
# you may live forever in a song, and you will not be holding the pen.
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
