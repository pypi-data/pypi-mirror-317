# syspathmodif

## FRANÇAIS

Cette bibliothèque offre des manières concises de modifier la liste `sys.path`.
L'utilisateur ne devrait pas avoir besoin d'interagir directement avec cette
liste.

### Contenu

Les fonctions de `syspathmodif` prennent un chemin de type `str` ou
`pathlib.Path` comme argument.
Elles convertissent les arguments de type `pathlib.Path` en `str` puisque
`sys.path` n'est censée contenir que des chaînes de caractères.

* `sp_append` ajoute le chemin donné à la fin de `sys.path`.
* `sp_contains` indique si `sys.path` contient le chemin donné.
* `sp_remove` enlève le chemin donné de `sys.path`.

Dès son instanciation, la classe `SysPathBundle` contient plusieurs chemins et
les ajoute à `sys.path`. Quand on vide (*clear*) une instance, elle efface son
contenu et l'enlève de `sys.path`. Ainsi, cette classe facilite l'ajout et le
retrait d'un groupe de chemins.

Il est possible d'utiliser `SysPathBundle` comme un gestionnaire de contexte
(*context manager*). Dans ce cas, l'instance est vidée à la fin du bloc `with`.

Pour plus d'informations, consultez la documentation des fonctions et les démos
dans le dépôt de code source.

### Dépendances

Installez les dépendances de `syspathmodif` avant de l'utiliser.
```
pip install -r requirements.txt
```

Cette commande installe les dépendances de développement en plus des
dépendances ordinaires.
```
pip install -r requirements-dev.txt
```

### Démos

Les scripts dans le dossier `demos` montrent comment `syspathmodif` permet
d'importer un paquet qui est indisponible tant qu'on n'a pas ajouté son chemin
à `sys.path`. Toutes les démos dépendent du paquet `demo_package`.

`demo_bundle.py` ajoute la racine du dépôt et `demo_package` à `sys.path` à
l'aide de la classe `SysPathBundle`. Après les importations, la démo annule
cette modification en vidant l'instance de `SysPathBundle`.
```
python demos/demo_bundle.py
```

`demo_bundle_context.py` effectue la même tâche que `demo_bundle.py` en
utilisant `SysPathBundle` comme un gestionnaire de contexte.
```
python demos/demo_bundle_context.py
```

`demo_functions.py` ajoute la racine du dépôt à `sys.path` à l'aide de la
fonction `sp_append`. Après les importations, la démo annule cette modification
à l'aide de la fonction `sp_remove`.
```
python demos/demo_functions.py
```

### Tests automatiques

Cette commande exécute les tests automatiques.
```
pytest tests
```

## ENGLISH

This library offers concise manners to modify list `sys.path`.
The user should not need to directly interact with that list.

### Content

The functions in `syspathmodif` take a path of type `str` or `pathlib.Path`
as an argument.
They convert arguments of type `pathlib.Path` to `str` since `sys.path` is
supposed to contain only character strings.

* `sp_append` appends the given path to the end of `sys.path`.
* `sp_contains` indicates whether `sys.path` contains the given path.
* `sp_remove` removes the given path from `sys.path`.

Upon instantiation, class `SysPathBundle` stores several paths and adds them to
`sys.path`. When a bundle is cleared, it erases its content and removes it from
`sys.path`. Thus, this class facilitates adding and removing a group of paths.

`SysPathBundle` can be used as a context manager. In that case, the instance is
cleared at the `with` block's end.

For more information, consult the functions' documentation and the demos in the
source code repository.

### Dependencies

Install the dependencies before using `syspathmodif`.
```
pip install -r requirements.txt
```

This command installs the development dependencies in addition to the ordinary
dependencies.
```
pip install -r requirements-dev.txt
```

### Demos

The scripts in directory `demos` show how `syspathmodif` allows to import a
package unavailable unless its path is added to `sys.path`. All demos depend
on `demo_package`.

`demo_bundle.py` adds the repository's root and `demo_package` to `sys.path`
with class `SysPathBundle`. After the imports, the demo undoes this
modification by clearing the `SysPathBundle` instance.
```
python demos/demo_bundle.py
```

`demo_bundle_context.py` performs the same task as `demo_bundle.py` by using
`SysPathBundle` as a context manager.
```
python demos/demo_bundle_context.py
```

`demo_functions.py` adds the repository's root to `sys.path` with function
`sp_append`. After the imports, the demo undoes this modification with function
`sp_remove`.
```
python demos/demo_functions.py
```

### Automated Tests

This command executes the automated tests.
```
pytest tests
```
