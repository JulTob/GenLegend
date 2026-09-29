"""
AtlasOfTraining — Guild Training Tag catalogues.

Each Map registers core (non-subclass) lessons for one Guild via
``Make_Training``.  TrainingKit loads these Maps at import time;
import Maps from here only for explicit access, not for registration.
"""

# [Reconstructed 2026-08-29 from compiled bytecode after the working-tree
#  wipe. Declarations are verbatim; see Documenta/Questae for the incident.]

from AtlasLusoris.AtlasOfTraining.Map_of_Fighter_Training import Second_Wind
from AtlasLusoris.AtlasOfTraining.Map_of_Fighter_Training import Weapon_Mastery
__all__ = ('Second_Wind', 'Weapon_Mastery')
