# Blog Django Application

## Description
Ce projet est une application Django permettant de gérer un blog avec des fonctionnalités telles que la création, la modification, la suppression et l'affichage des articles de blog. L'application inclut également une gestion des auteurs.

## Installation

Clonez le dépôt :
```
git clone https://github.com/votre-repo/blog.git
cd blog
```

Créez un environnement virtuel et activez-le :
```
python -m venv env
source env/bin/activate # Sur Windows : env\Scripts\activate
```

Installez les dépendances :
```
pip install -r requirements.txt
```

Appliquez les migrations de la base de données :
```
python manage.py migrate
```

Lancez le serveur de développement :
```
python manage.py runserver
```

## Applications Blog

### URLS
Les URLs de l'application sont définies dans `urls.py` :

`home` : Liste des articles du blog.
`create-author` : Créer un auteur (nécessite une authentification).
`list-author` : Lister les auteurs (nécessite une authentification).
`create` : Créer un article de blog (nécessite une authentification).
`detail` : Afficher les détails d'un article de blog.
`edit` : Modifier un article de blog (nécessite une authentification).
`delete` : Supprimer un article de blog (nécessite une authentification).

### Modèles

#### Author
Modèle représentant un auteur avec les champs `firstname` et `lastname`.

Méthodes :
`str` : Retourne le nom complet de l'auteur.
`clean` : Valide l'unicité de l'auteur avant de le sauvegarder.
`save` : Appelle la méthode `clean` avant de sauvegarder.

#### BlogPost
Modèle représentant un article de blog avec des métadonnées, du contenu et un auteur optionnel.

Méthodes :
`str` : Retourne le titre de l'article.
`save` : Génère un `slug` basé sur le titre s'il n'est pas fourni.
`get_absolute_url` : Retourne l'URL de l'article basé sur son `slug`.
`author_or_default` : Retourne le nom complet de l'auteur ou 'auteur inconnu' s'il n'y a pas d'auteur.

### Admin
L'interface d'administration est configurée dans `admin.py` pour le modèle `BlogPost` avec des configurations personnalisées :

Champs affichés : `title`, `published`, `created_on`, `last_updated`.
Champs éditables : `published`.
Fieldsets : Organisation des champs dans l'interface d'administration pour les objets existants et nouveaux.

### Tests
Les tests sont implémentés dans `tests.py` en utilisant `pytest`.

Author Tests :

Création d'un auteur.
Gestion des doublons.
Vérification de la méthode `str`.
BlogPost Tests :

Vérification de la méthode `str`.
Génération du `slug`.
Propriété `author_or_default`.
Méthode `get_absolute_url`.

### Vues
Les vues génériques basées sur les classes sont définies dans `views.py` pour gérer les opérations CRUD sur les articles et auteurs :

`BlogHome` : Liste les articles.
`BlogPostCreate` : Crée un nouvel article.
`BlogPostUpdate` : Met à jour un article existant.
`BlogPostDetail` : Affiche les détails d'un article.
`BlogPostDelete` : Supprime un article.
`AuthorCreateView` : Crée un nouvel auteur.
`AuthorListView` : Liste les auteurs.

## Applications Accounts

### Accounts

Configuration : Le module `apps.py` contient la configuration de l'application `accounts` en utilisant la classe `AccountsConfig` qui définit le champ de clé primaire par défaut comme `BigAutoField`.

### URLS
Les URLs de l'application sont définies dans `urls.py` :

`login` : Connexion de l'utilisateur (géré par `django.contrib.auth.urls`).
`logout` : Déconnexion de l'utilisateur (géré par `django.contrib.auth.urls`).
`password_change` : Changement de mot de passe (géré par `django.contrib.auth.urls`).
`signup` : Inscription de l'utilisateur.
`profile` : Profil de l'utilisateur (nécessite une authentification).
`confirm` : Confirmation après inscription.

### Modèles

#### CustomUser
Modèle représentant un utilisateur personnalisé utilisant l'adresse e-mail comme identifiant unique.

Attributs :

`email` : Adresse e-mail unique et obligatoire.
`is_active` : Indique si le compte utilisateur est actif.
`is_staff` : Indique si l'utilisateur peut accéder au site d'administration.
`is_superuser` : Indique si l'utilisateur a tous les privilèges.
`zip_code` : Champ optionnel pour stocker le code postal de l'utilisateur.
Méthodes :

`str` : Retourne l'adresse e-mail de l'utilisateur.

#### CustomUserManager
Gestionnaire personnalisé pour le modèle `CustomUser` avec des méthodes pour créer des utilisateurs et des super-utilisateurs.

Méthodes :
`create_user` : Crée et retourne un utilisateur standard.
`create_superuser` : Crée et retourne un super-utilisateur avec des privilèges administratifs.

### Admin
L'interface d'administration est configurée dans `admin.py` pour le modèle `CustomUser` avec des configurations personnalisées :

Champs affichés : `email`, `is_staff`, `is_active`, `is_superuser`.
Champs de recherche : `email`.
Fieldsets : Organisation des champs dans l'interface d'administration pour les utilisateurs existants et nouveaux.

### Formulaires

#### UserRegistrationForm
Formulaire d'inscription personnalisée basé sur le modèle `CustomUser`.

Champs : `email`.

### Vues
Les vues génériques basées sur les classes sont définies dans `views.py` pour gérer les opérations liées aux utilisateurs :

`SignupView` : Affiche le formulaire d'inscription et traite les soumissions de formulaire.
`ConfirmView` : Affiche une page de confirmation après une inscription réussie.
`ProfileView` : Affiche la page de profil de l'utilisateur connecté (nécessite une authentification).

### Tests
Les tests sont implémentés dans `tests.py` en utilisant `pytest`.

CustomUser Tests :

Création d'un utilisateur standard et vérification des champs.
Création d'un super-utilisateur et vérification des privilèges.
Vérification de la méthode `str`.
UserRegistrationForm Tests :

Validation du formulaire d'inscription avec des mots de passe correspondants.
Vérification de l'erreur du formulaire lorsque les mots de passe ne correspondent pas.
Views Tests :

Vérification de l'affichage du formulaire d'inscription.
Vérification de la création de l'utilisateur après soumission du formulaire.
Vérification de la redirection vers la page de connexion pour les utilisateurs non authentifiés essayant d'accéder au profil.

## License
Ce projet est sous licence MIT. Voir le fichier 

