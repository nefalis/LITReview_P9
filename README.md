# LITRevu

LITRevu est une application qui permet aux utilisateurs de poster des critiques ou des demandes de critique sur des livres ou d'articles.

L'application permet de :
- se connecter ou de s'inscrire
- demander des critiques de livres ou d'articles
- lire des critiques
- publier des critiques
- l'utilisateur peut suivre d'autres utilisateurs

L'application est développée en utilisant le framework Django et l'utilisation de Tailwind pour le css.

## Mise en place du projet

Pour ce projet, vous avez besoin d'avoir Python 🐍 d'installer sur votre ordinateur. Vous pouvez le télécharger depuis le site officiel de Python .

### Téléchargement du repo

Créez un nouveau dossier sur votre bureau avec le nom que vous souhaitez
- Télécharger le contenu du projet ou clonez le avec le lien suivant :
```
https://github.com/nefalis/LITReview_P9.git
```
- ou dans le terminale 
``` 
git clone https://github.com/nefalis/LITReview_P9.git
```

### Configuration de l'environnement virtuel
Mettez vous dans le dossier LITReview_P9 si vous n'y etes pas
```
cd LITReview_P9
```

Création de l'environnement virtuel
```
python -m venv env
```

- pour l'activé sous Windows

```
env\Scripts\activate
```
- pour l'activé sous Linux

```
source env/bin/activate
```

### Installation des dépendances
```
pip install -r requirements.txt
```

### Effectuer les migrations de la base de données
```
python manage.py migrate
```

### Lancement du serveur
Déplacez vous dans le dossier src
```
cd src
```

Lancement du serveur
```
python manage.py runserver
```


### Etape facultative
Si vous souhaitez faire des modifications css, il vous faudra activé Tailwind sinon les modifications ne seront pas prise en compte
- Ouvrez un nouveau terminal
- Activez l'environnement virtuel au niveau du dossier 'LITReview_P9'

  Pour l'activé sous Windows
  ```
  env\Scripts\activate
  ```
  Pour l'activé sous Linux

  ```
  source env/bin/activate
  ```
- Déplacez vous dans le dossier 'src'
- Activation de Tailwind
  ```
  python manage.py tailwind start
  ```

## Visualisation de l'application
Entrer l'adresse suivante dans votre navigateur
```
 http:/127.0.0.1:8000/
```
Il ne vous reste plus qu'à vous inscrire pour tester l'application

## Auteur

Charron Emilie
