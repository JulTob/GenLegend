"""
Legacy Bard Progression — ASI / Epic Boon when TOP owns the rest.

Core lessons and Colleges live in
``AtlasOfTraining/Map_of_Bard_Training.py``.
Spellcasting lives in ``Grimoire_of_Spellcasters.Bard``.

This file used to carry a second, older copy of every Bard lesson. That copy
had drifted: it printed four College paragraphs word for word from the 2024
rulebook, labelled Extra Attack "College of Valor" so the heading appeared
twice, opened Battle Magic at level 6 instead of 14, and still dealt the
2014-only Song of Rest. The Training Map carries all of it correctly, so the
duplicate is gone rather than repaired (QST-0093.1).
"""

from ..Grimoire_of_Health import roll_health
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import Feature, ApplyRandomFeats, ApplyEpicBoon


# ── Progression ───────────────────────────────────────────────────────────


class Bard(Progression):

	HIT_DIE = 8

	def features(self, character=None):

		if character is None:
			character = self.char
		else:
			self.char = character

		from AtlasLusoris.TrainingKit import has_training_catalogue

		feats = []
		level = self.char.Level

		if level >= 2:
			roll_health(
				self.char
				)

		if has_training_catalogue(
			'Bard'
			):
			# ASI cadence (2024): the catalogue owns every other lesson;
			# this legacy Progression only deals the feats and the boon.
			for asi_level in (4, 8, 12, 16):
				if level >= asi_level:
					feats.extend(
						ApplyRandomFeats(
							self.char,
							n=1,
							)
						)

			if level >= 19:
				feats.extend(
					ApplyEpicBoon(
						self.char,
						n=1,
						)
					)

			return feats

		feats.append(
			Feature(
				'Bard',
				'Training Map unavailable.',
				)
			)

		return feats
