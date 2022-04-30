# Projet_Flask

############### MODULES À INSTALLER #############################
-folium:pour la localisation;

-flask_paginate: pour la pagination;

-psycopg2-binary:pour l'engine(connexion à la BD);

-requests: pour les requêtes sur les API's;

-Flask-SQLAlchemy;

-flask;

-sqlalchemy;

###### Connexion à la base de données postgresql #########################
Pour nous la connexion à la BD nous avons importé la fonction create_engine() du module "sqlalchemy" 
qui prend en argument le string suivant:"postgresql://votre_nom_utilisateur_postgres:votre_mot_de_passe@localhost:5432/le_nom_votre_Base_de_données".

-Donc vous devez tout d'abord modifier la varible engine dans le fichier base.py  à la ligne 17 avant d'exécuter le fichier;
<!-- #################### APP #################################### -->
Exécutez le fichier appFlask.py pour lancer l'application.



