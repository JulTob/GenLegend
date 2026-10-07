"""Legacy Cleric Progression — ASI / Epic Boon only.

Core and Domain lessons live in ``Map_of_Cleric_Training`` (2024 PHB).
This module must not re-emit 2014 class feature blurbs.
"""

from __future__ import annotations

from ..Codex_of_Progression import Progression
from AtlasLusoris.Grimoire_of_Features import (
	ApplyEpicBoon,
	ApplyRandomFeats,
	Feature,
	)


class Cleric(Progression):
	HIT_DIE = 8

	def features(
			self,
			character,
			):
		feats = []
		level = character.level

		# 2024: Ability Score Improvement (feat) at 4 / 8 / 12 / 16.
		for threshold in (
				4,
				8,
				12,
				16,
				):
			if level >= threshold:
				try:
					feats.extend(
						ApplyRandomFeats(
							character,
							n=1,
							level=threshold,
							) or ()
						)
				except Exception:
					feats.append(
						Feature(
							"Ability Score Improvement",
							"You gain the Ability Score Improvement feat or "
							"another feat of your choice for which you qualify.",
							"Class: Cleric",
							)
						)

		# 2024: Epic Boon at 19 (not another ASI).
		if level >= 19:
			try:
				feats.extend(
					ApplyEpicBoon(
						character,
						n=1,
						) or ()
					)
			except Exception:
				feats.append(
					Feature(
						"Epic Boon",
						"You gain an Epic Boon feat or another feat of your "
						"choice for which you qualify. Boon of Fate is "
						"recommended.",
						"Class: Cleric",
						)
					)

		return feats
