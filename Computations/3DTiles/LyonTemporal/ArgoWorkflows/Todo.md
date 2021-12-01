# TODO list

- Pour une boucle on doit différencier les noms des fichiers intermédiaires
  ou on fera le valueFrom LORSQUE "le" fichier de sortie est sur la partition
  partagée. Afin d'éviter cette différenciation, peut-on utiliser des
  répertoires différents dans chacun des conteneurs (avec e.g. la directive
  emptyDir ?)

- Constatons que l'exemple AW de loop qui fait un withParam sur la sortie d'un
  job Python est effectif pour
  - README_FIRST: en fait le bout de python DOIT faire l'extraction/traitement
     puisque cela merdoie avec expt/templatelib
  - fabriquer a la mano  un fichier /data/host/input.tx
  - faire un step python qui lit ce fichier /data/host/input.txt, puis
    envoie sur std-ouput un json (comme le fait l'exemple de loop)
  - prendre cela comme entree de withParam de la tache suivante
  - Note: la logique est ici d'avoir un bout de python qui fait le mapping
    entre deux tâches et qui produit le json pour le withParam suivant

- Peut-on faire reference a un step qui se trouve dans une loop ? (dans une
  structure iterative). Et peut-on faire reference relativement au contexte ?
  (i.e. le step d'avant dans cet boucle?)
  Tip: pythonsay a l'interieur de de la boucle

- Regarder si on peut élégamment et conjointement définir les paramètres du
  workflow en laissant leur valeur dans le yml de de param. Cela aiderait le
  linter

- A mettre dans les Lesson learned: 
  - il faut systématiquement promouvoir tous les fichiers de sortie en 
    paramètre d'un traitement
  - de manière générale, c'est une bonne pratique que toutes les entrees et
    sorties doivent être paramétrables.
  - Écrire la logique de systématiquement décrire un fichier décrivant les
    sorties d'un traitement en json. Le penser comme une feature imposé d'un
    traitement ? i.e. généraliser l'approche de AW a d'autres modes d'écriture
    de workflow ?

- Use case: restart partiel on fail (re-execution partielle)
  - Peut-on changer l'entrypoint comme un argument de la ligne de commande
  - Peut-on lui dire de re-utiliser le même volume.

Olivier said:

- apprendre à monter un FS s3 remote avec le client local
  [goofys](https://github.com/kahing/goofys#installation)
- regarder comment AW peut faire usage d'un S3 bucket

## Done

- Regarder si on peut faire des boucles en sequences

- Deuxième piste: éviter d'avoir a utiliser sprig.last()
  - Pour les boucles faire que chaque run produise un fichiers d'output
  différents (par exemple indexé avec un identifiant automatique)
  - aller striper les attributs qu'il faut dans le résultat de la boucle.
