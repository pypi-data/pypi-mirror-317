# Copyright 2023 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Test de panini"""

import unittest

from jouets.panini.achats import achats


# pylint: disable=too-many-public-methods
class TestProba(unittest.TestCase):
    """Vérification de jouets.panini.achats.achats"""

    def test_achats(self):
        """Vérification de jouets.panini.achats.achats"""
        # Résultat trouvé dans https://www.cardiff.ac.uk/news/view/1136091-world-cup-stickers
        self.assertEqual(
            round(achats(682, 5)),
            4832,
        )
