"""Formatting helpers. ``Entry`` is the self-formatting primitive in Venustas."""

from AtlasVenustas import Entry


def Entry_Text(
		title: str,
		rules: str = "",
		flavor: str = "",
		) -> str:
	"""
	An entry written straight into sheet HTML, for the NonPlayer maps.

	The NonPlayer maps (``AtlasPugna``, the NonPlayer magic in
	``Map_of_Magic``) do not keep Entries: they glue their text together
	with ``+`` and ``join``, nest one entry inside another's text, and
	write HTML tags into it. Until the NonPlayer station of QST-0142 ports
	them to real Entries, they build text with this function, which
	returns exactly the markup the old string-shaped ``Entry`` produced.

	It is a text builder, not a second Entry: nothing here is Markdown,
	and nothing reads it back as data.
	"""
	if not title:
		return ""
	if not rules:
		return f"<b>{title}</b>"
	if not flavor:
		return f"<b>{title}:</b> <i>{rules}</i>"
	return (
			f"<b>{title}:</b>\n"
			f'<div class="bc4">{flavor}</div>'
			f"<i>{rules}</i>"
			)


def Type(npc) -> str:
	#Initialized("<< Map of Formats: <Type<>")
	""" Generate a description string
	rom NPC details. """
	try:
		pc = npc.NPCfy
	except:
		pc = npc
	text = f"{pc.race} {pc.subrace} {pc.archetype} {pc.alignment}"
	text = " ".join(text.split()).title()

	#Inform(f"Generating type description from NPC details: {text}")

	return text

def Genus(lusor):
	"""
	Returns a descriptive genus string for a lusor (NPC or PC).

	- If lusor is already a string, return it.
	- If it has a `.genus` property, use that.
	- Else, build it manually from attributes.
	"""
	# Case 1: already a string
	if isinstance(lusor, str):
		return lusor

	# Case 2: has a genus property
	if hasattr(lusor, "genus"):
		try:
			return lusor.genus
		except Exception as e:
			pass  # fallback to manual if it fails

	# Case 3: build manually (best-effort fallback)
	archetype = getattr(lusor, "archetype", None) or getattr(lusor, "char_class", "")
	attributes = [
		str(getattr(lusor, "race", "") or ""),
		str(getattr(lusor, "subrace", "") or ""),
		str(archetype),
		str(getattr(lusor, "gender", "") or ""),
		str(getattr(lusor, "alignment", "") or ""),
	]
	return " , ".join(filter(None, attributes))
