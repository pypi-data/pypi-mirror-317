#!/usr/bin/env python3

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

"""Calcul du nombre de cartes à acheter pour compléter un album Panini."""

import argparse
import textwrap

from jouets.utils import aargparse, erreurs

from . import achats


def _normalise_intervalle(intervalle):
    if intervalle[0] is None:
        intervalle[0] = 1
    if intervalle[1] is None:
        raise erreurs.ErreurUtilisateur(
            "La borne supérieure de l'intervalle doit être définie."
        )
    return intervalle


def analyse():
    """Renvoit un analyseur de ligne de commande."""
    parser = argparse.ArgumentParser(
        prog="panini",
        description=textwrap.dedent(
            "Calcule lu nombre moyen de cartes Panini à acheter pour compléter un album."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            - Les arguments ALBUM et PAQUET peuvent être soit des nombres, soit des intervalles sous la forme "DÉBUT:FIN" (par exemple 2:10 pour tous les nombres entiers de 2 à 10). La borne inférieure peut être omise, et vaut alors 1.
            - Si ALBUM et PAQUET sont deux nombres (ou deux intervalle d'étendue 0), le programme affiche un nombre, qui est le nombre moyen d'achats avec les paramètres demandés. Si ALBUM ou PAQUET est un intervalle, le programme affiche tous les résultats demandés sous la forme d'un tableau à double entrée au format CSV.

            Remarquez bien que quel que soit le nombre de paquet donné en argument, le programme calcule et affiche le nombre de *cartes* à acheter (c'est-à-dire le nombre de paquet multiplié par le nombre de cartes par paquet).
        """,
    )
    parser.add_argument(
        "album",
        metavar="ALBUM",
        type=aargparse.type_intervalle,
        help="Nombre de cartes par album.",
    )
    parser.add_argument(
        "paquet",
        metavar="PAQUET",
        type=aargparse.type_intervalle,
        help="Nombre de cartes par paquet.",
    )

    return parser


def main():
    """Fonction principale."""
    options = analyse().parse_args()
    intervalle_album = _normalise_intervalle(options.album)
    intervalle_paquet = _normalise_intervalle(options.paquet)

    if (
        intervalle_album[0] == intervalle_album[1]
        and intervalle_paquet[0] == intervalle_paquet[1]
    ):
        print(achats(intervalle_album[0], intervalle_paquet[0]))
    else:
        print(
            ",",
            ", ".join(
                str(i) for i in range(intervalle_album[0], intervalle_album[1] + 1)
            ),
        )
        for paquet in range(intervalle_paquet[0], intervalle_paquet[1] + 1):
            print(paquet, end="")
            for album in range(intervalle_album[0], intervalle_album[1] + 1):
                print(", ", achats(album, paquet), end="")
            print()


if __name__ == "__main__":
    main()
