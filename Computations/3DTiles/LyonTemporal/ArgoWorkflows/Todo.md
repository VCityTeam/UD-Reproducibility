# TODO list

- Constatons que l'exemple AW de loop qui fait un withParam sur la sortie d'un
  job Python est effectif pour
  - fabriquer a la mano  un fichier /data/host/input.tx
  - faire un step python qui lit ce fichier /data/host/input.txt, puis
    envoie sur std-ouput un json (comme le fait l'exemple de loop)
  - prendre cela comme entree de withParam de la tache suivante
  - Note: la logique est ici d'avoir un bout de python qui fait le mapping
    entre deux tâches et qui produit le json pour le withParam suivant

- Deuxième piste: éviter d'avoir a utiliser sprig.last()
  - Pour les boucles faire que chaque run produise un fichiers d'output
  différents (par exemple indexé avec un identifiant automatique)
  - aller striper les attributs qu'il faut dans le resultat de la boucle.

- Regarder si on peut élégamment et conjointement définir les paramètres du 
  workflow en laissant leur valeur dans le yml de de param. Cela aiderait le
  linter

- Regarder si on peut faire des boucles en sequences

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
