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

"""Tracé d'un graphe représentant le livre."""

import argparse
import collections
import statistics
import sys
import textwrap

from ...utils.aargparse import yesno
from ...utils.erreurs import ErreurUtilisateur
from .. import livres
from ..graphe import Condition, Histoire


def main(args):
    """Affiche le code LaTeX dessinant le graphe représantant le livre."""
    parser = argparse.ArgumentParser(
        description="Affiche le code LaTeX dessinant le graphe représentant le livre.",
        parents=[livres.analyseur()],
    )
    parser.add_argument(
        "--format",
        "-f",
        default="dot",
        choices=["dot"],
        help="""Format de sortie: dot (GraphViz).""",
    )
    options = parser.parse_args(args)
    print(
        textwrap.dedent(
            """\
            digraph {
                node[shape="rectangle"];
            """
        )
    )
    for page in livres.LIVRES[options.livre].iter_pages():
        if page.fin is None:
            print(
                """page{} [label="{}"];""".format(
                    id(page),
                    "\n".join(
                        f"{couleur}: {valeur}"
                        for couleur, valeur in page.roues.items()
                        if valeur is not None
                    ),
                )
            )
        else:
            print(f"""page{id(page)} [label="FIN\n{page.fin}"];""")
        for choix in page.choix:
            if choix.est_direct():
                print(f"page{id(page)} -> page{id(choix.cible)};")
            else:
                print(f"page{id(page)} -> page{id(page)}choix{choix.code}")
                if not isinstance(choix.condition, Condition.vrai):
                    print(f"""[label="{choix.condition.txt}"]""")
                print(";\n")
                print(
                    f"""page{id(page)}choix{choix.code} [label="{choix.effet.txt}"];"""
                )
                if choix.cible:
                    print(
                        f"page{id(page)}choix{choix.code} -> page{id(choix.cible)};\n"
                    )
    print("}")
