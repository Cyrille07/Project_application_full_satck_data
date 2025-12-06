# Project_application_full_satck_data


## Introduction

Dans le cadre du module **E5_DSIA_4201C - Application Full Stack Data**, nous avons eu l’opportunité de mettre en pratique les concepts étudiés en cours à travers la réalisation d’un projet complet.  
Ce projet consistait à **développer une application Web API**, **concevoir une base de données relationnelle** stockée dans **PostgreSQL**, créér un service de **tests automatisés avec Pytest** afin de valider la logique métier et les différentes routes implémentées, , le tout **conteneurisé avec Docker**. 
En bonus, nous avons conçu un **Front end web interactive** permettant d’afficher et de manipuler les informations de manière optimale.

Encadré par **Monsieur Courivaud** et son équipe, ce projet a été développé par le binôme composé de **Cyrille KOUMA** et **Franck NGUIMKEU ZAFACK**.

Nous avons choisi de travailler sur la mise en place d’un **système de gestion des tâches dans un restaurant**.  
Dans un contexte réel de restauration (rapide ou classique), les tâches sont aujourd’hui largement automatisées :  
- la prise de commande se fait via des tablettes,  
- les factures et bons de tâches sont envoyés automatiquement,  
- l’accueil, le service et le nettoyage des tables sont coordonnés numériquement.  

Notre application illustre cette modernisation à travers **quatre acteurs principaux** :
- le **serveur**,  
- le **caissier**,  
- le **cuisinier**,  
- et le **chef du restaurant**, qui supervise l’ensemble.

### Exemple de scénario concret

Un client entre dans le restaurant.  
Le serveur l’accueille, l’installe et enregistre sa commande depuis sa tablette.  
La commande est automatiquement transmise au cuisinier via une **tâche** créée dans le système.  
Lorsque le plat est prêt, le serveur reçoit une nouvelle **tâche**  pour récupérer le plat et le servir à la table.  
Pour l’addition, une requête est envoyée au caissier, qui crée la note et la transmet au client.  
L’ensemble de ce processus est **numérisé et géré par notre application web**.  
Le **directeur du restaurant** (ou chef) dispose d’un rôle de **super utilisateur** : il peut ajouter ou supprimer des employés, supprimer des tâches terminées ou assigner des tâches spécifiques.


## Objectif du projet 
Nous avons orienté notre application Full Stack afin de :

- **Gérer efficacement les employés**, leurs rôles et leurs fonctions ;  
- **Optimiser la gestion et la répartition des tâches** au sein du restaurant, grâce à une interface simple et intuitive.  



---
## Sommaire

### I. [Guide Utilisateur](#guide-utilisateur)
- [1. Installation et fonctionnement](#installation-et-fonctionnement)  
- [2. Famework](#Framework)  

### II. [Guide Développeur](#guide-développeur)
- [1. Répertoires et fichiers](#répertoires-et-fichiers)  

### III. [Fonctionnement des différentes dépendances](#fonctionnement-des-différentes-dépendances)
- [1. API](#api)  
- [2. Base de données](#base-de-données)  
- [3. Tests](#tests)  
- [4. Frontend](#frontend)  

### IV. [Conclusion](#conclusion)
---



## **Guide utilisateur**
### Installation et fonctionnement

Pour lancer le projet, suivez ces étapes :

0. Clonez le dépôt Git :
    ```bash
    git clone https:......
    ```

1. Se placer dans le dossier `app` avec la commande :
   ```bash
   cd app
   ```

2. Lancer le projet avec  la commande :
    ```bash
    docker-compose up
    ```

3. Accédez aux différentes interfaces <br>
Frontend : [localhost:5173](http://localhost:5173/) <br>
Backend : [localhost:5001](http://localhost:5001/)


4. Interagisser comme vous le sentez



## Framework 
Ce projet est une application **Full Stack** conteneurisée, conçue autour d'une architecture modulaire séparant le frontend, le backend et la persistance des données.


### Organisation des fichiers
![arborescence](app/assets/arborescence.png)

###  Description des éléments principaux

| Élément | Rôle principal |
|----------|----------------|
| **docker-compose.yml** | Orchestre les services `frontend`, `API`, `database` et `pytest`. |
| **dockerfile** | Définit la configuration du conteneur backend (installation de Python, dépendances, etc.). |
| **main.py** | Lance le serveur FastAPI et enregistre les routes et middlewares. |
| **frontend/** | Contient l’interface utilisateur Vue.js (pages, composants, styles). |
| **models/** | Définit les tables et les relations de la base via SQLAlchemy. |
| **serializer/** | Utilise Pydantic pour valider et transformer les données échangées entre l’API et la BDD. |
| **services_crud/** | Implémente la logique CRUD pour interagir avec la base de données. |
| **routers/** | Définit les routes FastAPI correspondant à chaque entité (Employee, Task, etc.). |
| **database/** | Gère la connexion PostgreSQL et la création des tables au démarrage. |
| **tests/** | Contient les tests unitaires et fonctionnels exécutés avec Pytest. |

---

### Architecture Globale

L'application repose sur 4 services principaux orchestrés par **Docker Compose** :

1.  **Frontend (Vue.js)** : Interface utilisateur réactive.
2.  **Backend (FastAPI)** : API RESTful performante gérant la logique métier.
3.  **Database (PostgreSQL)** : Persistance des données relationnelles.
4. **test (pytest)**:test des logiques métiers et des routes 

sous l'architecture suivante : ![architecture](app/assets/architecture.png)



## Explication du contexte de l'App 
Cette app est pensé pour une gestion des taches dans un restaurant ,
La base de données est organisé en tables: Employee et Task

![table](app/assets/table_dtb.png)

On distingue 4 roless :

