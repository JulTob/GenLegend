"""Traits shared by more than one Species Atlas."""

from TopKit import Imprint

from AtlasLusoris.FeaturesKit import Trait


def Darkvision_Rules(
	range_feet: int,
	) -> str:
	"""
	State the shared Darkvision rules at one resolved range.

	The 2024 glossary reads: "you can see in Dim Light within a specified range
	as if it were Bright Light and in Darkness **within that range** as if it
	were Dim Light. You discern colors **in that Darkness** only as shades of
	gray."  Both scopes are load-bearing, and an earlier wording lost both: the
	range never reached the Darkness clause, which promised unlimited darkvision
	in true Darkness, and the colour limit was unscoped, which claimed a Dwarf
	could not tell red from blue at noon.

	The Disadvantage note is not in the glossary's Darkvision entry.  It follows
	from Darkness-seen-as-Dim-Light being Lightly Obscured, and it is worth
	printing because a player reading this sheet will otherwise assume darkvision
	cancels the penalty.  It is scoped to that Darkness for the same reason the
	other two are: it does not apply to the Dim Light you are seeing as Bright.
	"""
	return (
		f"You can see in Dim Light within {range_feet} feet as if it were "
		"Bright Light. In Darkness within that range you can see as if it "
		"were Dim Light (you have Disadvantage on Wisdom (Perception) checks "
		"that rely on sight, and colors are only shades of gray)."
		)


class Darkvision(Trait):
	"""Sight in darkness, measured by the Character's range Record."""

	RANGE = 60

	@Imprint
	def Set_Range(
		target,
		):
		target.darkvision = max(
			int(
				getattr(
					target,
					"darkvision",
					0,
					)
				),
			Darkvision.RANGE,
			)
