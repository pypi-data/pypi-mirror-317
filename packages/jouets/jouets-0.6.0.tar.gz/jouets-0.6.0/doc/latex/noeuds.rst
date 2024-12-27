Nœuds
=====

.. contents::
   :local:
   :depth: 2


Première version
----------------

J'ai vu une courte vidéo d'un dessin à la main sur un réseau social quelconque, et j'ai eu envie de le reproduire en :math:`\LaTeX`. Je n'ai pas pu m'empêcher de généraliser.

La commande ``\noeud{sommets}{rayon}{épaisseur}`` dessine un nœud avec :

- ``sommets`` : le nombre de sommets du polygone régulier sur lequel est construit le nœud ;
- ``rayon`` : le rayon du cercle circonscrit au polygone régulier susnommé ;
- ``épaisseur`` : l'épaisseur de la « corde ».

Exemples
""""""""

+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-01.svg | ``\noeud{3}{1}{1}``   |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-02.svg | ``\noeud{4}{1}{.5}``  |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-03.svg | ``\noeud{5}{1}{.3}``  |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-04.svg | ``\noeud{6}{1}{.15}`` |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-05.svg | ``\noeud{7}{1}{.1}``  |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-06.svg | ``\noeud{9}{1}{.05}`` |
+----------------------------------+-----------------------+

Mes calculs supposaient que la corde serait assez fine pour ne pas déborder de la boucle voisine. Je m'attendais à une catastrophe, mais vu la manière dont sont construites ces figures, à ma grande surprise, cela produit des tresses.

+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-07.svg | ``\noeud{5}{1}{.7}``  |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-08.svg | ``\noeud{6}{1}{.5}``  |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-09.svg | ``\noeud{7}{1}{.4}``  |
+----------------------------------+-----------------------+
| .. image:: noeuds/noeuds1-10.svg | ``\noeud{8}{1}{.3}``  |
+----------------------------------+-----------------------+

.. collapse:: Voir le code source

   .. literalinclude:: ../../latex/noeuds/noeuds1.tex
      :language: latex

Explications
""""""""""""

Voici comment est construit le nœud suivant.

.. image:: noeuds/noeuds1-03.svg

Le prodécé est illustré sur l'illustration suivantes.

.. image:: noeuds/noeuds1-explications-01.png

1. Comme pour :ref:`l'étoile <latex_etoiles>`, un polyèdre régulier est construit sur le cercle trigonométrique en utilisant les coordonnées polaires (petit pentagone en noir sur la figure).

2. Puis un second polygone est construit, plus grand que le premier, en respectant l'épaisseur donnée en argument. Ce second polygone est tronqué pour que le raccord des cercles (étape suivante) se fasse correctement.

3. Des arcs de cercle sont tracés pour relier ces différents segments.

4. Enfin, pour que le nœud apparaisse certaines parties de la figure viennent en recouvrir d'autres. Pour cela, le remplissage est fait en deux étapes :

   - d'abord les parties rouges ;
   - puis les parties bleues, qui viennent recouvrir les parties rouge.

Bon courage pour décortiquer les mathématiques derrière tout ça (les *math* ne sont pas si complexes, mais comprendre mon code non documenté l'est beaucoup plus) !


Deuxième version
----------------

Après avoir réalisé les nœuds précédents, je suis tombé sur le paquet `fiziko <https://habr.com/en/articles/454376/>`__ (de Sergey Slyusarev), qui réalise mieux en moins de lignes de code. J'ai donc cherché à améliorer ces nœuds, en remplaçant les cercles par des courbes de Bézier. Le résultat est ici.

La commande ``\noeud{sommets}{saut}{rayon1}{rayon2}{épaisseur}{dureté}`` dessine un nœud avec :

- ``sommets`` : le nombre de sommets du polygone régulier sur lequel est construit le nœud ;
- ``saut`` : indique le nombre d'arêtes que « saute » une courbe issue d'un sommet du polygone avant de rejoindre le sommet suivant ;
- ``rayon1`` : le rayon du cercle inscrit dans le polygone régulier central ;
- ``rayon2`` : le rayon des extrémités des courbes (sans compter l'épaisseur) ;
- ``épaisseur`` : l'épaisseur de la « corde » ;
- ``dureté`` : indique à quel point les courbes doivent êtres « pointues » ou « arrondies ».

Exemples
""""""""

Tresses
'''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-01.svg | ``\noeud{20}{15}{2}{2.2}{.08}{1}`` |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-02.svg | ``\noeud{40}{5}{2}{2.4}{.07}{.4}`` |
+----------------------------------+------------------------------------+

Rosaces
'''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-03.svg | ``\noeud{20}{20}{2}{2.2}{.08}{1}`` |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-04.svg | ``\noeud{20}{25}{2}{2.2}{.08}{1}`` |
+----------------------------------+------------------------------------+

Inclassables
''''''''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-05.svg | ``\noeud{20}{30}{2}{2.2}{.08}{1}`` |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-06.svg | ``\noeud{5}{1}{1}{.8}{.2}{.4}``    |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-07.svg | ``\noeud{7}{3}{1}{2}{.2}{3}``      |
+----------------------------------+------------------------------------+

Nœuds serrés
''''''''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-08.svg | ``\noeud{3}{1}{1}{2}{1}{1}``       |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-09.svg | ``\noeud{4}{1}{1}{1.5}{.5}{.6}``   |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-10.svg | ``\noeud{5}{1}{1}{1.5}{.5}{.4}``   |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-11.svg | ``\noeud{6}{1}{1}{1.5}{.5}{.4}``   |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-12.svg | ``\noeud{8}{1}{1}{1.25}{.25}{.2}`` |
+----------------------------------+------------------------------------+

Nœuds avec du jeu
'''''''''''''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-13.svg | ``\noeud{5}{1}{1}{1.5}{.2}{.4}``   |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-14.svg | ``\noeud{6}{1}{1}{1.5}{.2}{.4}``   |
+----------------------------------+------------------------------------+

Nœuds avec beaucoup de jeu ; Cercles
''''''''''''''''''''''''''''''''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-15.svg | ``\noeud{4}{3}{1}{3}{.2}{3}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-16.svg | ``\noeud{5}{2}{1}{2}{.5}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-17.svg | ``\noeud{5}{3}{1}{3}{.2}{3}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-18.svg | ``\noeud{5}{3}{1}{2}{.2}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-19.svg | ``\noeud{5}{2}{1}{2}{.2}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-20.svg | ``\noeud{7}{2}{1}{2}{.2}{1}``      |
+----------------------------------+------------------------------------+

Fleurs
''''''

+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-21.svg | ``\noeud{5}{4}{1}{2}{.5}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-22.svg | ``\noeud{5}{5}{1}{2}{.5}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-23.svg | ``\noeud{5}{6}{1}{2}{.5}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-24.svg | ``\noeud{5}{7}{1}{2}{.5}{1}``      |
+----------------------------------+------------------------------------+
| .. image:: noeuds/noeuds2-25.svg | ``\noeud{7}{5}{1}{2}{.2}{.5}``     |
+----------------------------------+------------------------------------+

.. collapse:: Voir le code source

   .. literalinclude:: ../../latex/noeuds/noeuds2.tex
      :language: latex


Quelques explications
"""""""""""""""""""""

Voici comment est construit le nœud suivant (sur la base d'un pentagone).

.. image:: noeuds/noeuds2-explications-05.png

Ces explications ne présentent que les grandes lignes. Le reste est laissé au lecteur patient : il faut un peu de trigonométrie et de coordonnées polaires.

#. D'abord, le pentagone intérieur est tracé, ainsi qu'une partie du pentagone extérieur. Notons que chaque segment du (presque) pentagone extérieur est tracé à une distance :math:`e` (l'épaisseur) du pentagone intérieur, perpendiculairement. Cela est fait en ajoutant des coordonnées polaires en TikZ.

   .. image:: noeuds/noeuds2-explications-01.png

#. Puis les coordonnées de l'extérieur de la forme sont calculées, en prenant la moyenne des angles des deux sommets correspondant (c'est-à-dire le sommet de départ, auquel on ajoute la moitié du saut). À ce stade, on obtient la forme demandée, mais la courbe a des « angles ».

   .. image:: noeuds/noeuds2-explications-02.png

#. Pour arrondir ces angles, des courbes de Bézier sont utilisées (notation ``.. controls`` de TikZ), avec les tangentes suivantes (les « points de contrôle » sont les extrémités de chaque tangente). La figure est terminée, sauf que certains brins devraient passer en dessous des autres.

   .. image:: noeuds/noeuds2-explications-03.png

#. Pour cela, la courbe est dessinée en deux fois : d'abord la partie bleue, qui va être ensuite recouverte par la partie rouge.

   .. image:: noeuds/noeuds2-explications-04.png

#. Et voilà ! Le travail est fait.

   .. image:: noeuds/noeuds2-explications-05.png
