# Thésaurus personnel pour gérer sa documentation

*MyThesaurus : Design and manage your own personal thesaurus to index and retrieve information*

Ce dépôt recense plusieurs petits projets liés à la gestion d'un thésaurus personnel pour un projet de recherche (création, maintien, indexation automatique, principes généraux, etc.).

## Introduction au thésaurus 

Quelques méthodes analogiques (pas de programmation) pour travailler avec un thésaurus : 

- Un chapitre détaillé pour utiliser et se [créer un thésaurus](https://pmartinolli.github.io/QMpRD/chapters/thesaurus.html)
- Un [aide-mémoire (PDF)](https://github.com/pmartinolli/MyThesaurus/blob/master/Affiche/affiche-mythesaurus-v1.1.fr.pdf) sous la forme d'une affichette, à utiliser en formation avec quelques bonnes pratiques de création de mots-clés contrôlés.
- Un billet de blogue pour utiliser un thésaurus avec les marqueurs de Zotero : [Optimiser l’organisation de sa bibliothèque](https://zotero.hypotheses.org/3298).
- Un exemple de thésaurus [en PDF](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/TTRPG_thesaurus.pdf).
- Un modèle de thésaurus simple en tableau [(PDF)](https://github.com/pmartinolli/TM-MyThesaurus/blob/master/ModeleSimple/modelethesaurus.pdf) ([ODT](https://github.com/pmartinolli/MyThesaurus/blob/master/ModeleSimple/modelethesaurus.odt)).


## *Thesaurus builder CSV->PDF*

Cet outil en Python prend un thésaurus rédigé sous la forme d'un tableau CSV (avec colonnes pertinentes) et il le transforme dans un joli fichier PDF facile à consulter. En effet, comme il est en une page (pour un thésaurus de taille raisonnable), il est facilement lisible, plastifiable ou collable comme couverture d'un cahier de laboratoire par exemple. 
- script Python pour [transformer le CSV en PDF](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/mythesaurus_csv2pdf.py)
- exemple de thésaurus à deux niveaux pour le jeu de rôle sur table : [en CSV](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/TTRPG_thesaurus.csv) et [en PDF](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/TTRPG_thesaurus.pdf)

## *Thesaurus formatter*

Cet outil en Python prend un thésaurus rédigé sous la forme d'un tableau CSV (avec colonnes pertinentes, le même format que dans l'outil précédent) et il le transforme en fichier CSV en deux colonnes qui sera utiliser par d'autres outils de traitement automatique listé plus bas. 
- script Python pour [transformer le CSV en deux colonnes](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/thesaurus3to2col.py) 

## Indexer automatiquement des fichiers MarkDown

#### Méthode 1 (recommandée) : plugin [Obsidian-my-thesaurus](https://github.com/Mara-Li/obsidian-my-thesaurus)

Cette extension pour Obsidian.md, codée bénévolement par [Mara-Li](https://github.com/Mara-Li/), permet de rajouter automatiquement des tags dans l'entête YAML de fichiers MarkDown d'un coffre Obsidian, basé sur un fichier CSV avec une colonne de mots à repérer et une colonne de tags correspondants. 

#### Méthode 2 (expérimentale) : MarkDown Tag Indexer

Cet outil en Python permet de parcourir un dossier de fichiers MarkDown et de rajouter automatiquement des tags dans l'entête YAML, basé sur un fichier CSV avec une colonne de mots à repérer et une colonne de tags correspondants. 
*Python script to index automatically MarkDown files (an Obsidian.md vault for example) with a CSV of controlled tags :* 
- [MarkdownTagUpdater](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/MarkdownTagUpdater.py) : *searching keywords and adding corresponding #tags in YAML headers.*

![How does it works?](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/MarkdownTagUpdater_howto.png)

#### Bonus : MarkdownTagHarvester

Cet outil en Python permet de récupérer tous les noms de notes, les aliases et les tags d'un dossier de fichiers MarkDown.
- [MarkdownTagHarvester](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/MarkdownTagHarvester.py) : *helping building the tags.csv*
- *Example of [tags.csv](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/tags.csv)*

## Zotero Tag Indexer (expérimental)

Cet outil en Python permet d'indexer automatiquement des exports de bibliothèques Zotero au format RDF (Bibliontology RDF et Zotero RDF) avec un thésaurus en deux colonnes sous forme de CSV (voir plus haut). Ne fonctionne pas pour les exportations de bibliothèques complexes car le programme Python est un peu codé avec les pieds dans le sens où il n'utilise pas les méthodes XML alors qu'il devrait. Je travaille à établir un cahier des charges fonctionnel pour qu'un codeur bénévole en fasse une extension Zotero en JavaScript.
- [ZoteroRDF_retag](https://github.com/pmartinolli/MyThesaurus/blob/master/ZoteroTag)

![How does it works?](https://github.com/pmartinolli/MyThesaurus/blob/master/ZoteroTag/ZoteroTagUpdate_howto.png)

\
\

## Besoin d'aide ?

N'hésitez pas à consulter votre bibliothécaire disciplinaire pour la conception ou le maintien de votre thésaurus. C'est notre métier, c'est notre expertise, et c'est aussi notre plaisir de vous aider avec cet outil particulièrement stimulant.


## Bibliographie

Dalbin, Sylvie. 2007. « Thésaurus et informatique documentaires. Partenaires de toujours ? » Documentaliste-Sciences de l’Information 44 (1): 42-55. https://doi.org/10.3917/docsi.441.0042.

Dégez, Danièle. 2009. « Construire un thesaurus ». Archimag, 44-45.

Hudon, Michèle. 2008. Guide pratique pour l’élaboration d’un thésaurus documentaire. Montréal: Éditions ASTED.

Keller, L. (2013). Encadrer la réingénierie d’un thesaurus : méthode, enjeux et impacts pour l’équipe d’un service de veille et documentation en entreprise (Mémoire INTD-CNAM). Institut national des techniques de la documentation du CNAM, Paris. Consulté à l’adresse https://memsic.ccsd.cnrs.fr/mem_00945542/document


## Métadonnées

* Author / Auteur : Pascal Martinolli

* Created / Créé le : 2019-02-24

* License / Licence : CC-BY

* Used by / Utilisé par  : [Séminaire PLU6058 - Rechercher et exploiter la documentation, UdeM](https://bib.umontreal.ca/multidisciplinaire/plu6058) ; [formations libres Zotero et EndNote, UdeM](https://bib.umontreal.ca/formations/).

* Comment le citer / *How to cite it* : Martinolli, Pascal. 2019-2020. *Thésaurus personnel pour gérer sa documentation*. Matériel pédagogique. Université de Montréal. https://github.com/pmartinolli/MyThesaurus

* Commments are welcomed at / Commentaires bienvenus : pascal.martinolli [à] umontreal.ca

* Remerciements : Catherine Bernier et Mathieu Thomas pour l'accompagnement des équipes de projet. Danièle Dégez et Sylvie Dalbin, consultantes en thésaurus, dont j’ai eu la chance de suivre les enseignements à l’INTD. Mara-Li pour le codage de l'extension Obsidian. 

\
\
https://github.com/pmartinolli/MyThesaurus
