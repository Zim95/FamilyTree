import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname("__file__"),
            '..'
        )
    )
)

from FamilyTree import entity
from FamilyTree import family_tree
from FamilyTree import helpers