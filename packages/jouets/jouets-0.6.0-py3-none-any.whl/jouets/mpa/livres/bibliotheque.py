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

"""Calcul du nombre d'histoires possibles au livre-jeu *La Bibliothèque infinie*."""

from ..graphe import Choix, Condition, Effet, Page

pageSurLeRetour = Page()
pageDeRetourAuCampementMalheureusement = Page()

pageTuProfites = Page(
    fin="bof",
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Lilon"),
            cible=pageSurLeRetour,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lilon")),
            cible=pageDeRetourAuCampementMalheureusement,
        ),
    ),
)

pageDeRetourAuCampementIlÉtaitLoin = Page(fin="victoire")
pageCotCotCot = Page(fin="défaite")

pageAprèsToutesCesPéripéties = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.et(
                Condition.compte(valeur="malédiction", sup=0),
                Condition.roue(jaune="livre"),
            ),
            cible=pageDeRetourAuCampementIlÉtaitLoin,
        ),
        Choix(
            code="M",
            condition=Condition.et(
                Condition.compte(valeur="malédiction", inf=1, sup=2),
                Condition.roue(jaune="livre"),
            ),
            cible=pageTuProfites,
        ),
        Choix(
            code="B",
            condition=Condition.roue(rouge="poulet"),
            cible=pageCotCotCot,
        ),
    ),
)

pageViteUneSurface = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="Camille"), Condition.roue(jaune="plastron")
            ),
            effet=Effet.affecte(jaune="livre"),
            cible=pageAprèsToutesCesPéripéties,
        ),
        Choix(
            code="2",
            cible=pageAprèsToutesCesPéripéties,
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="Camille"), Condition.roue(jaune="plastron")
                )
            ),
            effet=Effet.affecte(rouge="poulet"),
        ),
    ),
)

pageLesMeilleuresDéfenses = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="baguette"),
            effet=Effet.affecte(jaune="livre"),
            cible=pageAprèsToutesCesPéripéties,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="baguette")),
            effet=Effet.affecte(rouge="poulet"),
            cible=pageAprèsToutesCesPéripéties,
        ),
    ),
)

pageIlTeFautRapidement = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="fumée"),
            effet=Effet.affecte(jaune="livre"),
            cible=pageAprèsToutesCesPéripéties,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="fumée")),
            effet=Effet.affecte(rouge="poulet"),
            cible=pageAprèsToutesCesPéripéties,
        ),
    ),
)

pageUneFoisLesLivresCalmés = Page(
    choix=(
        Choix(
            code="H",
            cible=pageViteUneSurface,
        ),
        Choix(
            code="M",
            cible=pageLesMeilleuresDéfenses,
        ),
        Choix(
            code="B",
            cible=pageIlTeFautRapidement,
        ),
    )
)

pageLesLivresOnt = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="Lucien"), Condition.roue(bleu="bouclier")
            ),
            cible=pageUneFoisLesLivresCalmés,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="Lucien"), Condition.roue(bleu="bouclier")
                )
            ),
            effet=Effet.affecte(bleu="malédiction"),
            cible=pageUneFoisLesLivresCalmés,
        ),
    )
)

pageTuVoudraisSalir = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="pigment"),
            cible=pageUneFoisLesLivresCalmés,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="pigment")),
            effet=Effet.affecte(bleu="malédiction"),
            cible=pageUneFoisLesLivresCalmés,
        ),
    )
)

pageTuPensesQueCesLivres = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="loupe"),
            cible=pageUneFoisLesLivresCalmés,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.roue(bleu="loupe"),
            ),
            effet=Effet.affecte(bleu="malédiction"),
            cible=pageUneFoisLesLivresCalmés,
        ),
    )
)

pageTeVoilàDans = Page(
    choix=(
        Choix(
            code="H",
            cible=pageLesLivresOnt,
        ),
        Choix(
            code="M",
            cible=pageTuVoudraisSalir,
        ),
        Choix(
            code="B",
            cible=pageTuPensesQueCesLivres,
        ),
    )
)

pageTuPrendsTonÉlan = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="Lilon"), Condition.roue(vert="balai")
            ),
            cible=pageTeVoilàDans,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="Lilon"), Condition.roue(vert="balai")
                )
            ),
            effet=Effet.affecte(vert="malédiction"),
            cible=pageTeVoilàDans,
        ),
    )
)

pageLEscalierFait = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="escargot"),
            cible=pageTeVoilàDans,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="escargot")),
            effet=Effet.affecte(vert="malédiction"),
            cible=pageTeVoilàDans,
        ),
    )
)

pageAussiSoudainement = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.roue(vert="clé"),
            cible=pageTeVoilàDans,
        ),
        Choix(
            code="M",
            condition=Condition.non(Condition.roue(vert="clé")),
            cible=pageTuPrendsTonÉlan,
        ),
        Choix(
            code="B",
            condition=Condition.non(Condition.roue(vert="clé")),
            cible=pageLEscalierFait,
        ),
    )
)

pageTuOuvresLeLivreDesLégendes = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Lucien"),
            cible=pageAussiSoudainement,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lucien")),
            effet=Effet.affecte(bleu="bouclier"),
            cible=pageAussiSoudainement,
        ),
    )
)

pageTuOuvresLeLivreDUnAutreTemps = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Lucien"),
            effet=Effet.affecte(bleu="pigment"),
            cible=pageAussiSoudainement,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lucien")),
            cible=pageAussiSoudainement,
        ),
    )
)

pageTuTeFaufiles = Page(
    choix=(
        Choix(code="H", cible=pageTuOuvresLeLivreDesLégendes),
        Choix(code="M", cible=pageAussiSoudainement, effet=Effet.affecte(bleu="loupe")),
        Choix(code="B", cible=pageTuOuvresLeLivreDUnAutreTemps),
    ),
)

pageTuMontesSurLeToit = Page(
    choix=(
        Choix(
            code="1",
            cible=pageTuTeFaufiles,
        ),
        Choix(
            code="2",
            effet=Effet.affecte(jaune="fumée"),
            cible=pageTuTeFaufiles,
        ),
    )
)

pageÀLIntérieur = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Camille"),
            effet=Effet.affecte(jaune="baguette"),
            cible=pageTuTeFaufiles,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Camille")),
            cible=pageTuTeFaufiles,
        ),
    )
)

pagePourAtteindre = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Camille"),
            cible=pageTuTeFaufiles,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Camille")),
            effet=Effet.affecte(jaune="plastron"),
            cible=pageTuTeFaufiles,
        ),
    )
)

pageUneFoisLeCalme = Page(
    choix=(
        Choix(code="H", cible=pageTuMontesSurLeToit),
        Choix(code="M", cible=pageÀLIntérieur),
        Choix(code="B", cible=pagePourAtteindre),
    )
)

pageTuTÉlances = Page(
    choix=(
        Choix(
            code="1",
            cible=pageUneFoisLeCalme,
        ),
        Choix(
            code="2",
            effet=Effet.affecte(vert="escargot"),
            cible=pageUneFoisLeCalme,
        ),
    )
)
pageTuApproches = Page(
    choix=(
        Choix(
            code="1", cible=pageUneFoisLeCalme, condition=Condition.roue(rouge="Lilon")
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lilon")),
            effet=Effet.affecte(vert="balai"),
            cible=pageUneFoisLeCalme,
        ),
    )
)
pageLeProtecteur = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Lilon"),
            effet=Effet.affecte(vert="clé"),
            cible=pageUneFoisLeCalme,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Lilon")),
            cible=pageUneFoisLeCalme,
        ),
    )
)

pageDeRetourDUnePromenade = Page(
    choix=(
        Choix(code="H", cible=pageTuTÉlances),
        Choix(code="M", cible=pageTuApproches),
        Choix(code="B", cible=pageLeProtecteur),
    )
)

pageQuelMagicien = Page(
    choix=(
        Choix(
            code="Pc",
            effet=Effet.affecte(rouge="Camille"),
            cible=pageDeRetourDUnePromenade,
        ),
        Choix(
            code="Pi",
            effet=Effet.affecte(rouge="Lilon"),
            cible=pageDeRetourDUnePromenade,
        ),
        Choix(
            code="Pu",
            effet=Effet.affecte(rouge="Lucien"),
            cible=pageDeRetourDUnePromenade,
        ),
    ),
    descriptions={
        "": "La Bibliothèque infinie",
        "Pc": "Camille",
        "Pi": "Lilon",
        "Pu": "Lucien",
    },
)

LIVRES = {
    "bibliotheque": pageQuelMagicien,
}
