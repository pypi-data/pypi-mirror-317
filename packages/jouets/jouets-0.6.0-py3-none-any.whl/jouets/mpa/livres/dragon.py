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

"""Calcul du nombre d'histoires possibles aux jeux *Ma Première Aventure : En quête du dragon*."""

from ..graphe import Choix, Condition, Effet, Page

pageSiTuNeVeux = Page()
pageTuTentesDeRemonter = Page()

pageUnPeuSecouéTu = Page(
    fin="défaite",
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Timon"),
            cible=pageSiTuNeVeux,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Timon")),
            cible=pageTuTentesDeRemonter,
        ),
    ),
)

pageImpressionnéParTaBravoure = Page(fin="victoire")
pageLeDragonDécideDe = Page(fin="bof")

pageRapideCommeLÉclair = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.compte(valeur="bobo", sup=0),
            cible=pageImpressionnéParTaBravoure,
        ),
        Choix(
            code="M",
            condition=Condition.compte(valeur="bobo", inf=1, sup=2),
            cible=pageLeDragonDécideDe,
        ),
        Choix(
            code="B",
            condition=Condition.compte(valeur="bobo", inf=3),
            cible=pageUnPeuSecouéTu,
        ),
    ),
)

pageEnLuiTapantSur = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(bleu="marteau"), Condition.roue(rouge="Lina")
            ),
            cible=pageRapideCommeLÉclair,
        ),
        Choix(
            code="2",
            cible=pageRapideCommeLÉclair,
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(bleu="marteau"), Condition.roue(rouge="Lina")
                )
            ),
            effet=Effet.affecte(bleu="bobo"),
        ),
    ),
)

pageEnLuiOffrantQuelque = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="poulet"),
            cible=pageRapideCommeLÉclair,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="poulet")),
            cible=pageRapideCommeLÉclair,
            effet=Effet.affecte(bleu="bobo"),
        ),
    ),
)

pageEnLuiCriantDessus = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="grimoire"),
            cible=pageRapideCommeLÉclair,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="grimoire")),
            cible=pageRapideCommeLÉclair,
            effet=Effet.affecte(bleu="bobo"),
        ),
    ),
)

pageLeDragonTeScrute = Page(
    choix=(
        Choix(
            code="H",
            cible=pageEnLuiTapantSur,
        ),
        Choix(
            code="M",
            cible=pageEnLuiOffrantQuelque,
        ),
        Choix(
            code="B",
            cible=pageEnLuiCriantDessus,
        ),
    )
)

pageEnDétournantSonAttention = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="grelot"),
            cible=pageLeDragonTeScrute,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="grelot")),
            effet=Effet.affecte(jaune="bobo"),
            cible=pageLeDragonTeScrute,
        ),
    )
)

pageEnFonçantSurLui = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="bouclier"),
            cible=pageLeDragonTeScrute,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="bouclier")),
            effet=Effet.affecte(jaune="bobo"),
            cible=pageLeDragonTeScrute,
        ),
    )
)

pageDiscrètementSansFaireUn = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(jaune="chaussons"),
                Condition.roue(rouge="Sachat"),
            ),
            cible=pageLeDragonTeScrute,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(jaune="chaussons"),
                    Condition.roue(rouge="Sachat"),
                )
            ),
            effet=Effet.affecte(jaune="bobo"),
            cible=pageLeDragonTeScrute,
        ),
    )
)

pageLaUnÉnormeRonflement = Page(
    choix=(
        Choix(
            code="H",
            cible=pageEnDétournantSonAttention,
        ),
        Choix(
            code="M",
            cible=pageEnFonçantSurLui,
        ),
        Choix(
            code="B",
            cible=pageDiscrètementSansFaireUn,
        ),
    )
)

pageTOrienterDansLe = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(vert="pierre"), Condition.roue(rouge="Timon")
            ),
            cible=pageLaUnÉnormeRonflement,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(vert="pierre"), Condition.roue(rouge="Timon")
                )
            ),
            effet=Effet.affecte(vert="bobo"),
            cible=pageLaUnÉnormeRonflement,
        ),
    )
)

pageEntrerDansLeLabyrinthe = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="carte"),
            cible=pageLaUnÉnormeRonflement,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="carte")),
            effet=Effet.affecte(vert="bobo"),
            cible=pageLaUnÉnormeRonflement,
        ),
    )
)

pageTricherEnEscaladantLes = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="corde"),
            cible=pageLaUnÉnormeRonflement,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="corde")),
            effet=Effet.affecte(vert="bobo"),
            cible=pageLaUnÉnormeRonflement,
        ),
    )
)

pageUneFoisLesMontagnes = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTOrienterDansLe,
        ),
        Choix(
            code="M",
            cible=pageEntrerDansLeLabyrinthe,
        ),
        Choix(
            code="B",
            cible=pageTricherEnEscaladantLes,
        ),
    )
)

pageLaGrandeMontéeVers = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Timon"),
            cible=pageUneFoisLesMontagnes,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Timon")),
            effet=Effet.affecte(bleu="marteau"),
            cible=pageUneFoisLesMontagnes,
        ),
    )
)

pageLeRaccourciSousLa = Page(
    choix=(
        Choix(
            code="1", effet=Effet.affecte(bleu="poulet"), cible=pageUneFoisLesMontagnes
        ),
        Choix(code="2", cible=pageUneFoisLesMontagnes),
    )
)

pageLeDétourAuTravers = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Timon"),
            effet=Effet.affecte(bleu="grimoire"),
            cible=pageUneFoisLesMontagnes,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Timon")),
            cible=pageUneFoisLesMontagnes,
        ),
    )
)

pageAprèsUneLongueMarche = Page(
    choix=(
        Choix(code="H", cible=pageLaGrandeMontéeVers),
        Choix(code="M", cible=pageLeRaccourciSousLa),
        Choix(code="B", cible=pageLeDétourAuTravers),
    ),
)

pageAuTraversDeLa = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Lina"),
            cible=pageAprèsUneLongueMarche,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lina")),
            effet=Effet.affecte(jaune="chaussons"),
            cible=pageAprèsUneLongueMarche,
        ),
    )
)

pageSurLePetitChemin = Page(
    choix=(
        Choix(code="1", cible=pageAprèsUneLongueMarche),
        Choix(
            code="2",
            effet=Effet.affecte(jaune="grelot"),
            cible=pageAprèsUneLongueMarche,
        ),
    )
)

pageParLaGrandeRoute = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Lina"),
            effet=Effet.affecte(jaune="bouclier"),
            cible=pageAprèsUneLongueMarche,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lina")),
            cible=pageAprèsUneLongueMarche,
        ),
    )
)

pageAlorsQueTuQuittes = Page(
    choix=(
        Choix(code="H", cible=pageAuTraversDeLa),
        Choix(code="M", cible=pageSurLePetitChemin),
        Choix(code="B", cible=pageParLaGrandeRoute),
    )
)

pageDemanderDeLAide = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Sachat"),
            cible=pageAlorsQueTuQuittes,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Sachat")),
            effet=Effet.affecte(vert="pierre"),
            cible=pageAlorsQueTuQuittes,
        ),
    )
)
pageFouillerLaGrangeAbandonnée = Page(
    choix=(
        Choix(code="1", cible=pageAlorsQueTuQuittes),
        Choix(code="2", effet=Effet.affecte(vert="corde"), cible=pageAlorsQueTuQuittes),
    )
)
pageVolerUneCarteChez = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Sachat"),
            effet=Effet.affecte(vert="carte"),
            cible=pageAlorsQueTuQuittes,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Sachat")),
            cible=pageAlorsQueTuQuittes,
        ),
    )
)

pageTuVisDansUn = Page(
    choix=(
        Choix(code="H", cible=pageDemanderDeLAide),
        Choix(code="M", cible=pageFouillerLaGrangeAbandonnée),
        Choix(code="B", cible=pageVolerUneCarteChez),
    )
)

pageChoisisTonPersonnage = Page(
    choix=(
        Choix(code="Pl", effet=Effet.affecte(rouge="Lina"), cible=pageTuVisDansUn),
        Choix(code="Ps", effet=Effet.affecte(rouge="Sachat"), cible=pageTuVisDansUn),
        Choix(code="Pt", effet=Effet.affecte(rouge="Timon"), cible=pageTuVisDansUn),
    ),
    descriptions={
        "": "En quête du dragon",
        "Pl": "Lina",
        "Ps": "Sachat",
        "Pt": "Timon",
    },
)

LIVRES = {
    "dragon": pageChoisisTonPersonnage,
}
