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

"""Tracé d'un graphe présentant toutes les manières de gagner."""

import argparse
import collections
import statistics
import sys

from ...utils.aargparse import yesno
from ...utils.erreurs import ErreurUtilisateur
from .. import livres
from ..graphe import Condition, Histoire


def _digits2str(key):
    """Transforme les chiffres en texte (sans chiffres)."""
    return {"0": "zero", "1": "un", "2": "deux"}.get(key, key)


class Graphe(collections.UserDict):
    """Représentation de toutes les histoires possibles du livre."""

    def __init__(self, histoire=None, *, label="", condition=None, statut=None):
        #  pylint: disable=too-many-arguments
        super().__init__()
        self.fin = None if histoire is None else histoire.page.fin
        self.condition = condition
        self.label = label
        self.statut = statut
        self.angle = 0  # Sera définit proprement plus tard

        if histoire is not None:
            self.descriptions = histoire.page.descriptions
            for suivant, condition in histoire.suivantes(condition=True):
                self[suivant.codes[-1]] = Graphe(
                    suivant,
                    condition=condition,
                    label=(self.label if self.label else "") + suivant.codes[-1],
                )

    @property
    def racine(self):
        """Renvoit `True` si cet objet est la racine de l'arbre."""
        return not self.label

    @property
    def labels(self):
        """Renvoit l'ensemble des codes des choix de l'arbre."""
        return set(self.keys()).union(*(suivant.labels for suivant in self.values()))

    def nettoie(self, fins):
        """Supprime les branches ne menant pas à une des fins données en argument.

        Les branches *après* une fin valide sont conservées.
        """
        if self.fin in fins:
            return
        for key in tuple(self):
            self[key].nettoie(fins)
            if not (self[key].fin in fins or self[key]):
                del self[key]

    def élague(self):
        """Élague le graphe, c'est à dire supprime les sommets inutiles.

        Les sommets inutiles sont ceux pour lesquels la lectrice du livre n'a pas le choix.
        """
        for key in self:
            # pylint: disable=comparison-with-callable
            while (
                len(self[key]) == 1
                and not isinstance(
                    self[key][tuple(self[key])[0]].condition, Condition.vrai
                )
                and self[key][tuple(self[key])[0]].statut != "persistant"
            ):
                self[key] = list(self[key].values())[0]
            self[key].élague()

    def to_dot(self, *, descriptions=None):
        """Renvoit le code Dot (GraphViz) représentant ce graphe."""
        if descriptions is None:
            descriptions = self.descriptions
        if self.racine:
            print("digraph {")
            print(f"""node[label="{ self.descriptions.get("", "") }"] DEBUT;""")
        for key, value in self.items():
            print(f"""node[label="{ descriptions.get(key, key) }"] {value.label};""")
            print(f"""{self.label if self.label else "DEBUT"} -> {value.label};""")
            value.to_dot(descriptions=descriptions)
        if self.racine:
            print("}")

    @property
    def depth(self):
        """Renvoit la profondeur de l'arbre."""
        if self:
            return 1 + max(suivant.depth for suivant in self.values())
        return 0

    def enforce_depth(self, depth):
        """Rajoute des sommets invisibles pour que toutes les branches aient la même profondeur."""
        if depth == 0:
            return

        if not self:
            self["X"] = Graphe(None, statut="caché", label=self.label + "X")
        for suivant in self.values():
            suivant.enforce_depth(depth - 1)

    def ajoute_fin(self, fin=None):
        if self.fin is not None:
            fin = self.fin

        if self:
            for suivant in self.values():
                suivant.ajoute_fin(fin)
        else:
            label = "F" + fin[0]
            self[label] = Graphe(None, label=self.label + label, statut="persistant")
            self[label].fin = fin

    def feuilles(self):
        """Itère sur les feuilles de l'arbre (sommets sans descendants."""
        if self.depth == 0:
            yield self
        else:
            for key in sorted(self):
                yield from self[key].feuilles()

    def calcule_angles(self):
        """Affecte les angles aux sommets de l'arbre.

        Les feuilles sont réparties équitablement autour d'un cercle.
        Les autres sommets ont pour angle la moyenne de leurs descendants.
        """
        if self.racine:
            feuilles = list(self.feuilles())
            for i, feuille in enumerate(feuilles):
                feuille.angle = 360 * i / len(feuilles)

        if self:
            for suivant in self.values():
                suivant.calcule_angles()
            self.angle = statistics.mean(suivant.angle for suivant in self.values())

    def to_tikz(self, *, rayon=0):
        """Affiche le code LaTeX traçant ce graphe."""
        # pylint: disable=line-too-long
        if self.racine:
            self.enforce_depth(self.depth)
            self.calcule_angles()
            print(r"\documentclass[tikz]{standalone}")
            for label in self.labels:
                print(
                    rf"\newcommand{{\sommet{ _digits2str(label) }}}{{{ self.descriptions.get(label, label) }}}"
                )
            print(
                rf"""\newcommand{{\sommetDebut}}{{{ self.descriptions.get("", "") }}}"""
            )
            print(r"\begin{document}")
            print(r"\begin{tikzpicture}[scale=1.4]")
            print(
                rf"""\node ({ self.label if self.label else "DEBUT" }) at ({ self.angle }:{ rayon }) {{\sommetDebut}};"""
            )

        for key in sorted(self):
            if self[key].statut != "caché":
                print(
                    rf"""\node[rotate={self[key].angle-90}] ({ self[key].label }) at ({ self[key].angle }:{ rayon+2 }) {{\sommet{ _digits2str(key) }}};"""
                )
                print(
                    rf"""\draw[-latex] ({ self.label if self.label else "DEBUT"  }) -- ({ self[key].label });"""
                )
                self[key].to_tikz(rayon=rayon + 1)

        if self.racine:
            print(r"\end{tikzpicture}")
            print(r"\end{document}")


def victoires(page, *, fins, format, élague=False):
    """Affiche le code LaTeX dessinant l'ensemble des histoires victorieuses."""
    graphe = Graphe(page)
    if len(fins) != 1:
        graphe.ajoute_fin()
    graphe.nettoie(fins)
    if élague:
        graphe.élague()
    if format == "tex":
        graphe.to_tikz()
    elif format == "dot":
        graphe.to_dot()
    else:
        raise ErreurUtilisateur(f"Format de sortie {format} invalide.")


def _fins(livre, fins):
    if fins == "*":
        return livre.fins()
    fins = set(fins.split(","))
    if absentes := fins - livre.fins():
        raise ErreurUtilisateur(
            "Erreur: Fins inexistantes : {}.".format(", ".join(absentes))
        )
    return fins


def main(args):
    """Affiche le code LaTeX dessinant l'arbre de toutes les histoires victorieuses."""
    parser = argparse.ArgumentParser(
        description="Affiche le code LaTeX dessinant l'arbre de toutes les fins possibles",
        parents=[livres.analyseur()],
    )
    parser.add_argument(
        "--elague",
        "-e",
        choices=[True, False],
        default=False,
        nargs="?",
        const="oui",
        help="Supprime les choix inutiles (ceux pour lesquels le chemin est contraint).",
        type=yesno,
    )
    parser.add_argument(
        "--fins",
        "-F",
        default="victoire",
        help="""N'affiche que les histoires menant à ces fins là (sous la forme d'une liste séparée par des virgules, ou "*" pour toutes les fins.). Remarquez qu'avec autre chose que `--fin=victoire`, le graphe obtenu pourra être bien trop grand et illisible. Par défaut, n'affiche que les victoires.""",
    )
    parser.add_argument(
        "--format",
        "-f",
        default="tex",
        choices=["tex", "dot"],
        help="""Format de sortie: tex (LaTeX) ou dot (GraphViz).""",
    )
    options = parser.parse_args(args)
    livre = Histoire(livres.LIVRES[options.livre])
    try:
        victoires(
            livre,
            élague=options.elague,
            fins=_fins(livre, options.fins),
            format=options.format,
        )
    except ErreurUtilisateur as erreur:
        print(erreur)
        sys.exit(1)
