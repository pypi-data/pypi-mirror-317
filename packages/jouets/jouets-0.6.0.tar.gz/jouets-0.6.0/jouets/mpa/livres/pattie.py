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

"""Calcul du nombre d'histoires possibles au livre-jeu *Pattie et l'Épreuve des dieux*.

https://ma-premiere-aventure.fr/livres/pattie-lepreuve-des-dieux
"""

from ..graphe import Choix, Condition, Effet, Page

pageLesDieuxGrondent = Page()
pageLesDieuxSontIdifférents = Page()

pageLesDieuxNeSontPasRavis = Page(
    fin="défaite",
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="casque"),
            cible=pageLesDieuxSontIdifférents,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="casque")),
            cible=pageLesDieuxGrondent,
        ),
    ),
)

pagePoséidonEstFier = Page(fin="victoire")
pageZeusEstFier = Page(fin="victoire")

pageÉpilogue = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.compte(valeur="Zeus", inf=2),
            cible=pageZeusEstFier,
        ),
        Choix(
            code="M",
            condition=Condition.compte(valeur="Poséidon", inf=2),
            cible=pagePoséidonEstFier,
        ),
        Choix(
            code="B",
            condition=Condition.et(
                Condition.compte(valeur="Zeus", sup=1),
                Condition.compte(valeur="Poséidon", sup=1),
            ),
            cible=pageLesDieuxNeSontPasRavis,
        ),
    ),
)

pageLesCyclopesArrivent = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="bouclier"),
            effet=Effet.affecte(jaune="casque", vert="Zeus"),
            cible=pageÉpilogue,
        ),
        Choix(
            code="2",
            cible=pageÉpilogue,
            condition=Condition.non(Condition.roue(vert="bouclier")),
            effet=Effet.affecte(bleu=None),
        ),
    ),
)

pageSIlsSontOccupés = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="recette"),
            effet=Effet.affecte(jaune="casque", vert="Poséidon"),
            cible=pageÉpilogue,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="recette")),
            cible=pageÉpilogue,
        ),
    ),
)

pageLesRayonsDuSoleil = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="miroir"),
            effet=Effet.affecte(jaune="casque", vert="Poséidon"),
            cible=pageÉpilogue,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="miroir")),
            cible=pageÉpilogue,
        ),
    ),
)

pageActeVI = Page(
    choix=(
        Choix(
            code="H",
            cible=pageLesCyclopesArrivent,
        ),
        Choix(
            code="M",
            cible=pageSIlsSontOccupés,
            condition=Condition.non(Condition.roue(jaune="alerte")),
        ),
        Choix(
            code="B",
            cible=pageLesRayonsDuSoleil,
            condition=Condition.non(Condition.roue(jaune="alerte")),
        ),
    )
)

pageTuTApproches = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="pierre"),
            cible=pageActeVI,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="pierre")),
            effet=Effet.affecte(jaune="alerte"),
            cible=pageActeVI,
        ),
    )
)

pageLaCréatureNAPasLAir = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="masque"),
            cible=pageActeVI,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="masque")),
            effet=Effet.affecte(jaune="alerte"),
            cible=pageActeVI,
        ),
    )
)

pageLaCréatureSemble = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="poudre"),
            cible=pageActeVI,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.roue(jaune="poudre"),
            ),
            effet=Effet.affecte(jaune="alerte"),
            cible=pageActeVI,
        ),
    )
)

pageActeV = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTuTApproches,
        ),
        Choix(
            code="M",
            cible=pageLaCréatureNAPasLAir,
        ),
        Choix(
            code="B",
            cible=pageLaCréatureSemble,
        ),
    )
)

pageLeThéâtre = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Sam"),
            effet=Effet.affecte(jaune="masque"),
            cible=pageActeV,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Sam")),
            cible=pageActeV,
        ),
    )
)

pageTuTEngages = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Sam"),
            cible=pageActeV,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Sam")),
            effet=Effet.affecte(jaune="poudre"),
            cible=pageActeV,
        ),
    )
)

pageLaZoneEstCalme = Page(
    choix=(
        Choix(
            code="1",
            effet=Effet.affecte(jaune="pierre"),
            cible=pageActeV,
        ),
        Choix(
            code="2",
            cible=pageActeV,
        ),
    )
)

pageActeIV = Page(
    choix=(
        Choix(
            code="H",
            cible=pageLeThéâtre,
        ),
        Choix(
            code="M",
            cible=pageTuTEngages,
        ),
        Choix(
            code="B",
            cible=pageLaZoneEstCalme,
        ),
    )
)

pageLesPremièresGouttes = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="conque"),
            effet=Effet.affecte(bleu="Poséidon"),
            cible=pageActeIV,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="conque")),
            cible=pageActeIV,
        ),
    )
)

pageTuGonflesLesVoiles = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="ailes"),
            effet=Effet.affecte(bleu="Zeus"),
            cible=pageActeIV,
        ),
        Choix(
            code="2",
            cible=pageActeIV,
            condition=Condition.non(Condition.roue(bleu="ailes")),
        ),
    )
)

pageUneFoisDansLaCaverne = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="harpon"),
            effet=Effet.affecte(bleu="Zeus"),
            cible=pageActeIV,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="harpon")),
            effet=Effet.affecte(bleu="Poséidon"),
            cible=pageActeIV,
        ),
    )
)

pageActeIII = Page(
    choix=(
        Choix(code="H", cible=pageLesPremièresGouttes),
        Choix(code="M", cible=pageTuGonflesLesVoiles),
        Choix(code="B", cible=pageUneFoisDansLaCaverne),
    ),
)

pageDeuxCérémonies = Page(
    choix=(
        Choix(
            code="1",
            effet=Effet.affecte(vert="bouclier"),
            cible=pageActeIII,
        ),
        Choix(
            code="2",
            effet=Effet.affecteSiVide(bleu="ailes"),
            cible=pageActeIII,
        ),
    )
)

pageLesÉtagères = Page(
    choix=(
        Choix(code="1", condition=Condition.roue(rouge="Pattie"), cible=pageActeIII),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Pattie")),
            effet=Effet.affecte(vert="recette"),
            cible=pageActeIII,
        ),
    )
)

pageÀLEntrée = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Pattie"),
            effet=Effet.affecte(vert="miroir"),
            cible=pageActeIII,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Pattie")),
            effet=Effet.affecte(vert="bouclier"),
            cible=pageActeIII,
        ),
    )
)

pageActeII = Page(
    choix=(
        Choix(code="H", cible=pageDeuxCérémonies),
        Choix(code="M", cible=pageLesÉtagères),
        Choix(code="B", cible=pageÀLEntrée),
    )
)

pageLaToisonDOr = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Chickos"),
            effet=Effet.affecte(bleu="ailes"),
            cible=pageActeII,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Chickos")),
            cible=pageActeII,
        ),
    )
)
pageAvantDeTeJeter = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Chickos"),
            cible=pageActeII,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Chickos")),
            effet=Effet.affecte(bleu="conque"),
            cible=pageActeII,
        ),
    )
)
pageLesRatsNinjas = Page(
    choix=(
        Choix(
            code="1",
            cible=pageActeII,
        ),
        Choix(
            code="2",
            effet=Effet.affecte(bleu="harpon"),
            cible=pageActeII,
        ),
    )
)

pageActeI = Page(
    choix=(
        Choix(code="H", cible=pageLaToisonDOr),
        Choix(code="M", cible=pageAvantDeTeJeter),
        Choix(code="B", cible=pageLesRatsNinjas),
    )
)

pageChoisisTonPersonnage = Page(
    choix=(
        Choix(code="Ps", effet=Effet.affecte(rouge="Sam"), cible=pageActeI),
        Choix(code="Pp", effet=Effet.affecte(rouge="Pattie"), cible=pageActeI),
        Choix(code="Pc", effet=Effet.affecte(rouge="Chickos"), cible=pageActeI),
    ),
    descriptions={
        "": "Pattie et l'Épreuve des dieux",
        "Ps": "Sam",
        "Pp": "Pattie",
        "Pc": "Chickos",
    },
)

LIVRES = {
    "pattie": pageChoisisTonPersonnage,
}
