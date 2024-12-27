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

"""Patron pour le calcul du nombre d'histoires possibles aux jeux *Ma Première Aventure*."""

from ..graphe import Choix, Condition, Effet, Page

pageTODO = Page()
pageTODO = Page()

pageTODO = Page(
    fin="défaite",
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            cible=pageTODO,
        ),
    ),
)

pageTODO = Page(fin="victoire")
pageTODO = Page(fin="bof")

pageTODO = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.compte(valeur="TODO", sup=0),
            cible=pageTODO,
        ),
        Choix(
            code="M",
            condition=Condition.compte(valeur="TODO", inf=1, sup=2),
            cible=pageTODO,
        ),
        Choix(
            code="B",
            condition=Condition.compte(valeur="TODO", inf=3),
            cible=pageTODO,
        ),
    ),
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(bleu="TODO"), Condition.roue(rouge="TODO")
            ),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            cible=pageTODO,
            condition=Condition.non(
                Condition.ou(Condition.roue(bleu="TODO"), Condition.roue(rouge="TODO"))
            ),
            effet=Effet.affecte(bleu="TODO"),
        ),
    ),
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="TODO")),
            cible=pageTODO,
            effet=Effet.affecte(bleu="TODO"),
        ),
    ),
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="TODO")),
            cible=pageTODO,
            effet=Effet.affecte(bleu="TODO"),
        ),
    ),
)

pageTODO = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTODO,
        ),
        Choix(
            code="M",
            cible=pageTODO,
        ),
        Choix(
            code="B",
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="TODO")),
            effet=Effet.affecte(jaune="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="TODO")),
            effet=Effet.affecte(jaune="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(jaune="TODO"),
                Condition.roue(rouge="TODO"),
            ),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(jaune="TODO"),
                    Condition.roue(rouge="TODO"),
                )
            ),
            effet=Effet.affecte(jaune="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTODO,
        ),
        Choix(
            code="M",
            cible=pageTODO,
        ),
        Choix(
            code="B",
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(vert="TODO"), Condition.roue(rouge="TODO")
            ),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(Condition.roue(vert="TODO"), Condition.roue(rouge="TODO"))
            ),
            effet=Effet.affecte(vert="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="TODO")),
            effet=Effet.affecte(vert="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="TODO")),
            effet=Effet.affecte(vert="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTODO,
        ),
        Choix(
            code="M",
            cible=pageTODO,
        ),
        Choix(
            code="B",
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            effet=Effet.affecte(bleu="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(code="1", effet=Effet.affecte(bleu="TODO"), cible=pageTODO),
        Choix(code="2", cible=pageTODO),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            effet=Effet.affecte(bleu="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(code="H", cible=pageTODO),
        Choix(code="M", cible=pageTODO),
        Choix(code="B", cible=pageTODO),
    ),
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            effet=Effet.affecte(jaune="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(code="1", cible=pageTODO),
        Choix(
            code="2",
            effet=Effet.affecte(jaune="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            effet=Effet.affecte(jaune="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(code="H", cible=pageTODO),
        Choix(code="M", cible=pageTODO),
        Choix(code="B", cible=pageTODO),
    )
)

pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            effet=Effet.affecte(vert="TODO"),
            cible=pageTODO,
        ),
    )
)
pageTODO = Page(
    choix=(
        Choix(code="1", cible=pageTODO),
        Choix(code="2", effet=Effet.affecte(vert="TODO"), cible=pageTODO),
    )
)
pageTODO = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="TODO"),
            effet=Effet.affecte(vert="TODO"),
            cible=pageTODO,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="TODO")),
            effet=Effet.affecte(vert="TODO"),
            cible=pageTODO,
        ),
    )
)

pageTODO = Page(
    choix=(
        Choix(code="H", cible=pageTODO),
        Choix(code="M", cible=pageTODO),
        Choix(code="B", cible=pageTODO),
    )
)

pageTODO = Page(
    choix=(
        Choix(code="P1", effet=Effet.affecte(rouge="Perso1"), cible=pageTODO),
        Choix(code="P2", effet=Effet.affecte(rouge="Perso2"), cible=pageTODO),
        Choix(code="P3", effet=Effet.affecte(rouge="Perso3"), cible=pageTODO),
    ),
    descriptions={
        "": "TODO Titre",
        "P1": "TODO personnage 1",
        "P2": "TODO personnage 2",
        "P3": "TODO personnage 3",
    },
)

LIVRES = {
    # "TODO": pageTODO,
}
