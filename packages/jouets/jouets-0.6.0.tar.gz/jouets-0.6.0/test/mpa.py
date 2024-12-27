# Copyright 2024 Louis Paternault
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

"""Test de mpa (Ma Première Aventure)"""

import unittest

from jouets.mpa.graphe import Choix, Condition, Effet, Histoire, Page

pageVictoire = Page(fin="victoire")
pageDéfaite = Page(fin="défaite")

pageMilieu = Page(
    choix=(
        Choix(
            code="V",
            condition=Condition.intervalle(roue="bleu", inf=2),
            cible=pageVictoire,
        ),
        Choix(
            code="D",
            condition=Condition.intervalle(roue="bleu", sup=1),
            cible=pageDéfaite,
        ),
    )
)

pageHaut = Page()
pageBas = Page()

pageHaut.choix = (
    Choix(
        code="M",
        cible=pageMilieu,
    ),
    Choix(
        code="B",
        cible=pageBas,
        effet=Effet.ajoute(bleu=1),
    ),
)
pageBas.choix = (
    Choix(
        code="M",
        cible=pageMilieu,
    ),
    Choix(
        code="H",
        cible=pageHaut,
        effet=Effet.ajoute(bleu=1),
    ),
)

livre1 = Page(
    roues={"bleu": 0},
    choix=(
        Choix(
            code="H",
            cible=pageHaut,
            effet=Effet.ajoute(bleu=1),
        ),
        Choix(
            code="M",
            cible=pageMilieu,
        ),
        Choix(
            code="B",
            cible=pageBas,
            effet=Effet.ajoute(bleu=1),
        ),
    ),
)


class TestMPA(unittest.TestCase):
    """Différents tests sur des livres fictifs"""

    def test_fins(self):
        """Vérifie la méthode `fins()`"""
        self.assertEqual(Histoire(livre1).fins(), {"victoire", "défaite"})

    def test_proba(self):
        """Vérifie la méthode `proba()`"""
        self.assertEqual(Histoire(livre1).proba("victoire"), 1 / 3)
        self.assertEqual(Histoire(livre1).proba("défaite"), 2 / 3)

    def test_histoires(self):
        """Vérifie la méthode `histoires()`"""
        self.assertEqual(
            {"".join(histoire.codes) for histoire in Histoire(livre1).histoires()},
            {
                "HMD",
                "HBMV",
                "MD",
                "BHMV",
                "BMD",
            },
        )

    def test_proba_préfixe(self):
        """Vérifie l'argument `préfixe` de la méthode `proba()`"""
        self.assertEqual(Histoire(livre1).proba("victoire", préfixe=["M"]), 0)
        self.assertEqual(Histoire(livre1).proba("victoire", préfixe=["B"]), 1 / 2)
        self.assertEqual(Histoire(livre1).proba("victoire", préfixe=["B", "H"]), 1)
        self.assertEqual(Histoire(livre1).proba("victoire", préfixe=["X"]), 0)


pageImpossible = Page(fin="impossible")
pageFin = Page(fin="fin")
livre2 = Page(
    choix=(
        Choix(
            code="I", condition=Condition.non(Condition.vrai()), cible=pageImpossible
        ),
        Choix(code="F", cible=pageFin),
    )
)


class TestImpossible(unittest.TestCase):
    """Quelques tests avec une fin impossible à atteindre."""

    def test_fin(self):
        """Vérifie que les fins impossibles sont quand même retournées."""
        self.assertIn("impossible", Histoire(livre2).fins())

    def test_proba(self):
        """Vérifie que la fin impossible est inatteignable"""
        self.assertEqual(Histoire(livre2).proba("impossible"), 0)
