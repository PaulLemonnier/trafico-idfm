# 🚆 Prochains départs

Projet Python permettant de récupérer les prochains départs de trains à la gare de Maisons-Laffitte, à partir des données d’Île-de-France Mobilités.

## Sources de données
- **Prim IDFM** (Prochains passages - requête unitaire): [API PRIM IDFM — Requête unitaire](https://prim.iledefrance-mobilites.fr/fr/apis/idfm-ivtr-requete_unitaire)
- **Référentiels Lignes et Arrêts** : [Île-de-France Mobilités — Arrêts et lignes](https://data.iledefrance-mobilites.fr/explore/dataset/arrets-lignes/information/?disjunctive.route_long_name&disjunctive.id)


## Données utilisées

| Champ | Description |
|---|---|
| `MonitoringRef.value` | Identifiant de la gare : `STIF:StopArea:SP:473109:` (Maisons-Laffitte) |
| `LineRef.value` | Identifiant de la ligne : `STIF:Line::C01742:` (RER A) |
| `DestinationName` | Nom de la destination du train |
| `DestinationDisplay` | Destination affichée |
| `ExpectedDepartureTime` | Heure de départ estimée à Maisons-Laffitte |
| `DeparturePlatformName` | Quai de départ |

## Installation sur Raspberry Pi

Mettre à jour le système et installer les dépendances :

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install git python3-venv python3-pip -y
```

Cloner le dépôt du projet :

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_PROJET>
```

Créer et activer un environnement virtuel Python :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances Python :

```bash
pip install -e .
```
