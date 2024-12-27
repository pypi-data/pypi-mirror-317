# Copyright 2023 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Calcul du nombre d'achats moyen de cartes Panini pour compléter un album."""

import math


def proba(album, paquet, manquantes, trouvées):
    """Probabilité de trouver `trouvées` nouvelles cartes dans un paquet.

    :param int album: Nombre total de cartes dans l'album.
    :param int paquet: Nombre de cartes par paquet acheté.
    :param int manquantes: Nombre de cartes manquantes dans l'album.
    :param int trouvées: Probabilité de trouver ce nombre de cartes manquantes dans le paquet.
    """
    if trouvées > paquet:
        return 0

    return (
        math.comb(album - manquantes, paquet - trouvées)
        * math.comb(manquantes, trouvées)
        / math.comb(album, paquet)
    )


def achats(album, paquet):
    """Calcul du nombre d'achats de cartes nécessaires pour compléter un album.

    :param int album: Nombre total de cartes dans l'album.
    :param int paquet: Nombre de cartes par paquet acheté.
    """

    # `cache[k] = n` signifie :
    # il faut acheter en moyenne `n` paquets pour compléter un album
    # dans lequel `k` cartes manquent.
    cache = [0]

    for manquantes in range(1, album + 1):
        cache.append(
            (
                sum(
                    proba(album, paquet, manquantes, k) * (1 + cache[manquantes - k])
                    for k in range(1, 1 + min(paquet, manquantes))
                )
                + proba(album, paquet, manquantes, 0)
            )
            / (1 - proba(album, paquet, manquantes, 0))
        )

    return paquet * cache.pop()
