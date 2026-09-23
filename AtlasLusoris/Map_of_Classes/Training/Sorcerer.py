"""
Legacy Sorcerer Progression — ASI / Epic Boon when TOP owns the rest.

Core lessons and Origins live in
``AtlasOfTraining/Map_of_Sorcerer_Training.py``, declared by
``AtlasOfGuilds/SorcererKit.py``.
Spellcasting lives in ``Grimoire_of_Spellcasters.Sorcerer``.

This file used to carry a second, older copy of the Sorcerer.  It printed a
Metamagic block in markdown asterisks beside the Training Map's own, told the
reader "see PHB '24 pp145-150" in place of the Origin, and gave the Sorcerer
a Sorcery Point at level 1.  The Training Map carries all of it correctly,
so the duplicate is gone rather than repaired, as the Bard's was.
"""

from ..Grimoire_of_Health import roll_health
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import Feature, ApplyRandomFeats, ApplyEpicBoon


# ── Progression ───────────────────────────────────────────────────────────


class Sorcerer(Progression):

	HIT_DIE = 6

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
			'Sorcerer'
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
				'Sorcerer',
				'Training Map unavailable.',
				)
			)

		return feats
