.. _latex_etoiles:

Étoiles
=======

J'avais besoin d'une étoile à cinq branches pour illustrer un projet. J'ai écrit la fonction ``\etoile{rayon}{sommets}{décalage}`` :

- ``rayon`` : rayon du cercle dans lequel est inscrit l'étoile ;
- ``sommets`` : nombre de pointes de l'étoile (en fait, il s'agit du nombre de sommets du polygone régulier utilisé pour construire l'étoile) ;
- ``décalage`` : deux pointes de l'étoile sont reliées par un segment (tronqué) ; cet argument donne le nombre de pointes situées entre deux sommets (dans le sens direct).

Voici quelques exemples.

+-----------------------------------+----------------------+
| .. image:: etoiles/etoiles-01.svg | ``\etoile{1}{5}{2}`` |
+-----------------------------------+----------------------+
| .. image:: etoiles/etoiles-02.svg | ``\etoile{1}{6}{2}`` |
+-----------------------------------+----------------------+
| .. image:: etoiles/etoiles-03.svg | ``\etoile{1}{7}{2}`` |
+-----------------------------------+----------------------+
| .. image:: etoiles/etoiles-04.svg | ``\etoile{1}{7}{3}`` |
+-----------------------------------+----------------------+
| .. image:: etoiles/etoiles-05.svg | ``\etoile{1}{8}{2}`` |
+-----------------------------------+----------------------+
| .. image:: etoiles/etoiles-06.svg | ``\etoile{1}{8}{3}`` |
+-----------------------------------+----------------------+

.. collapse:: Voir le code source

   .. literalinclude:: ../../latex/etoiles/etoiles.tex
      :language: latex


Quelques explications pour l'étoile
-----------------------------------

Voici comment sont construites les étoiles suivantes : |etoiles03| |etoiles04|.

.. |etoiles03| image:: etoiles/etoiles-03.svg

.. |etoiles04| image:: etoiles/etoiles-04.svg

1. Prenons d'abord le cercle trigonométrie, et plaçons les septs sommets d'un polygone régulier à sept branches (en prenant les points de coordonnées polaires :math:`(1 ; 360k/7)` (pour :math:`k` allant de 0 à 6).

   .. image:: etoiles/etoiles-explications-01.png

2. À partir de là, pour l'étoile avec un *décalage* de 2 (``\etoile{1}{7}{2}``), chaque sommet est relié au deuxième sommet dans le sens horaire.

   .. figure:: etoiles/etoiles-explications-02.png

3. Et pour l'étoile avec un *décalage* de 3 (``\etoile{1}{7}{3}``), chaque sommet est relié au troisième dans le sens horaire.

   .. figure:: etoiles/etoiles-explications-03.png

4. Il ne reste plus qu'à calculer les positions des intersections de ces segments, pour ne pas tracer les segments intérieurs, et le tour est joué.

J'ai écrit ce code il y a plusieurs années, donc je ne me souviens plus des détails de calcul, et j'ai la flemme de refaire les calculs (et les figures qui vont avec). Bon courage !
