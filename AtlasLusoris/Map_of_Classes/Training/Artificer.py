"""
Legacy Artificer Progression — ASI / Epic Boon when TOP owns the rest.

Core lessons and Specialties live in
``AtlasOfTraining/Map_of_Artificer_Training.py``.
Spellcasting lives in ``Grimoire_of_Spellcasters.Artificer``.
"""

from ..Grimoire_of_Health import roll_health
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import Feature, ApplyRandomFeats, ApplyEpicBoon


# ── Progression ───────────────────────────────────────────────────────────



class Artificer(Progression):

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
			'Artificer'
			):
			# ASI cadence (2024): the catalogue owns every other lesson;
			# this legacy Progression only deals the feats and the boon.
			for asi_level in (4, 8, 12, 16):
				if level >= asi_level:
					feats.extend(
						ApplyRandomFeats(
							self.char,
							n=1,
							level=asi_level,
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
				'Artificer',
				'See Eberron: Forge of the Artificer — Training Map unavailable.',
				)
			)

		return feats
