# README - mainController.py

## Description

Le script `mainController.py` est un outil de surveillance système automatisé.  
Il est conçu pour être exécuté automatiquement toutes les minutes via une tâche cron (crontab).  
Son objectif est de surveiller en temps réel les ressources principales du système — **CPU**, **RAM** et **stockage** — et de notifier l'utilisateur en cas de situation critique.

## Fonctionnalités

- **Collecte des statistiques système :**
  - Utilisation du CPU
  - Utilisation de la mémoire (RAM)
  - Espace disque disponible
  - Parseur web
- **Détection de situations de crise :**
  - Utilisation CPU > 90%
  - Mémoire RAM restante < 10%
  - Espace disque disponible < 10%
- **Notification utilisateur en cas de crise** (via mail)
- **Stockage des données** dans une base locale
- **Génération de graphiques** de l'utilisation des ressources

## Installation

1. Assurez-vous d'avoir **Python 3** installé.
2. Installez les bibliothèques nécessaires : `pygal`, `sqlite3`, `json`, `subprocess`
3. Placez le script dans un répertoire accessible.

## Utilisation avec crontab

Pour exécuter `mainController.py` toutes les minutes, ajoutez la ligne suivante à votre crontab :

```bash
*/1 * * * * /usr/bin/python3 /home/utilisateur/chemin/mainController.py >> /home/utilisateur/chemin/cronlog.log 2>&1
