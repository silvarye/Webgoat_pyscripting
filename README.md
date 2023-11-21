# Documentation du script `main_challenge_manager`

Voici la documentation de ce script :
## Bibliothèques importées
### os
Cette bibliothèque permet d'utiliser des fonctions propres au système d'exploitation. Elle est utilisée pour accéder aux variables d'environnement.

### pyfiglet
Cette bibliothèque permet d'écrire du texte dans une police particulière. Elle est utilisée ici pour écrire un titre dans la console.

### requests
Cette bibliothèque permet de réaliser des requêtes HTTP en Python. Elle est utilisée pour effectuer des requêtes aux différents challenges.

## Classe ChallRegistry

La classe ChallRegistry permet de gérer les différents challenges et de les enregistrer. Cette classe possède plusieurs méthodes :

`__init__()`
Constructeur de la classe.

`register(self, chall)`
Méthode permettant d'enregistrer un challenge.

`categories(self)`
Méthode renvoyant la liste des catégories de challenges.

`vulnerabilities(self)`
Méthode renvoyant la liste des types de vulnérabilités.

`get_chall_by_name(self, name)`
Méthode renvoyant le challenge correspondant au nom donné en paramètre.

`get_chall_by_category(self, category)`
Méthode renvoyant la liste des challenges correspondant à la catégorie donnée en paramètre.

`run_all_script(self)`
Méthode permettant d'exécuter tous les challenges

## Classe Challenge
La classe Challenge permet de créer un nouveau challenge. Elle prend en paramètres le nom, la catégorie, l'URL, le proxy, la fonction à exécuter et les arguments par défaut.

`checkValidChallenge(cookie, proxy)`
La fonction checkValidChallenge permet de vérifier si un challenge a été validé. Elle prend en paramètres le cookie et le proxy.

`controlleur(registry)`
La fonction controlleur permet de créer tous les challenges et de les enregistrer. Elle prend en paramètre la classe ChallRegistry.

Le script permet donc de gérer les différents challenges, de les enregistrer et de les exécuter selon le envie de l'utilisateur.