# 🎭 Système de Rôles et Permissions - Guide Complet

## 📋 Vue d'ensemble

Le système de signalement de fuites d'eau intègre maintenant un système de rôles sophistiqué qui permet une gestion hiérarchique des missions avec différents niveaux de permissions.

## 👥 Types de Rôles

### 1. 👷‍♂️ Responsable de Quartier (`quartier`)
- **Responsabilité** : Gestion opérationnelle des fuites dans leurs quartiers assignés
- **Permissions** :
  ✅ Voir les missions de leurs quartiers uniquement
  ✅ Modifier le statut des missions (démarrer, résoudre, annuler)
  ✅ Ajouter des commentaires aux missions
  ✅ Accès complet aux actions de terrain

### 2. 👔 Responsable de Commune (`commune`)
- **Responsabilité** : Supervision et vue d'ensemble de toute leur commune
- **Permissions** :
  ✅ Voir TOUTES les missions de leur commune
  ✅ Statistiques détaillées par quartier
  ❌ **LECTURE SEULE** : Ne peut PAS modifier les missions
  ❌ Ne peut pas changer le statut des missions
  ℹ️ Rôle de supervision et coordination uniquement

### 3. 🏛️ Administrateur (`admin`)
- **Responsabilité** : Administration système globale
- **Permissions** :
  ✅ Accès complet à toutes les missions
  ✅ Modification de toutes les missions
  ✅ Vue globale sur tous les quartiers et communes
  ✅ Gestion des agents et permissions

## 🔐 Matrice des Permissions

| Action                    | Responsable Quartier | Responsable Commune | Administrateur |
|---------------------------|---------------------|---------------------|----------------|
| Voir missions quartier   | ✅                  | ✅                  | ✅             |
| Voir missions commune    | ❌                  | ✅                  | ✅             |
| Voir toutes missions     | ❌                  | ❌                  | ✅             |
| Démarrer mission         | ✅                  | ❌                  | ✅             |
| Résoudre mission         | ✅                  | ❌                  | ✅             |
| Annuler mission          | ✅                  | ❌                  | ✅             |
| Ajouter commentaire      | ✅                  | ❌                  | ✅             |
| Statistiques quartier    | ✅                  | ✅                  | ✅             |
| Statistiques commune     | ❌                  | ✅                  | ✅             |

## 🚀 Configuration Initiale

### Commandes de gestion

#### 1. Initialiser le système de rôles
```bash
python manage.py setup_agent_roles
```
Cette commande :
- Met à jour les agents existants avec le rôle 'quartier'
- Affiche un résumé des agents par rôle

#### 2. Créer des responsables de commune
```bash
python manage.py setup_agent_roles --create-commune-supervisors
```
Cette commande :
- Crée automatiquement des responsables pour chaque commune
- Email format : `responsable.{commune}@regideso.cd`
- Rôle : 'commune' (lecture seule)

#### 3. Mode test (dry-run)
```bash
python manage.py setup_agent_roles --dry-run --create-commune-supervisors
```
Affiche ce qui serait fait sans modifier la base de données.

## 🔑 Connexion des Agents

### Responsables de Quartier
- **Email** : Leur adresse email existante
- **Mot de passe** : `commune+quartier` (exemple: `gombe+gombe`)

### Responsables de Commune
- **Email** : `responsable.{commune}@regideso.cd`
- **Mot de passe** : `commune+commune` (exemple: `gombe+gombe`)

### Administrateur
- **Email** : `admin@regideso.cd`  
- **Mot de passe** : `admin+admin`

## 🎯 Workflow par Rôle

### Workflow Responsable de Quartier
1. **Connexion** → Dashboard avec statistiques de leurs quartiers
2. **Missions en attente** → Peut démarrer les interventions
3. **Missions en cours** → Peut marquer comme résolue ou annuler
4. **Communication** → Peut ajouter des commentaires aux signaleurs

### Workflow Responsable de Commune  
1. **Connexion** → Dashboard avec vue d'ensemble de la commune
2. **Supervision** → Voit toutes les missions de la commune
3. **Statistiques** → Répartition par quartier et performance
4. **Lecture seule** → Ne peut pas modifier les statuts

### Workflow Administrateur
1. **Connexion** → Dashboard global avec toutes les communes
2. **Gestion** → Accès complet à toutes les missions
3. **Administration** → Peut modifier tous les statuts
4. **Supervision** → Vue d'ensemble du système entier

## 🔧 Fonctionnalités Techniques

### Méthodes du modèle AgentProfile

```python
# Vérification des permissions
agent.can_modify_mission(mission)  # True/False
agent.can_view_mission(mission)    # True/False

# Récupération des missions
agent.get_missions_assigned()      # Selon le rôle
agent.get_missions_pending()       # En attente
agent.get_missions_in_progress()   # En cours
agent.get_missions_resolved()      # Résolues

# Statistiques
agent.get_quarterly_stats()        # Pour responsables quartier
agent.get_commune_stats()          # Pour responsables commune
```

### Interface Utilisateur

#### Indicateurs Visuels
- 👷‍♂️ Icône responsable de quartier
- 👔 Icône responsable de commune  
- 🏛️ Icône administrateur
- 👁️ Mode lecture seule (commune)
- 🔧 Actions disponibles (quartier/admin)

#### Alertes et Messages
- Alerte jaune pour mode lecture seule
- Messages d'erreur si tentative de modification non autorisée
- Confirmation des actions importantes

## 📊 Exemples d'Usage

### Scenario 1: Fuite signalée à Gombe
1. **Citoyen** signale fuite → Mission créée automatiquement
2. **Responsable Quartier Gombe** reçoit notification → Peut traiter
3. **Responsable Commune Gombe** voit la mission → Mode supervision
4. **Admin** a accès complet → Peut intervenir si nécessaire

### Scenario 2: Supervision communale
```python
# Responsable commune consulte ses statistiques
responsable_gombe = AgentProfile.objects.get(
    email='responsable.gombe@regideso.cd'
)

stats = responsable_gombe.get_commune_stats()
# Retourne statistiques détaillées par quartier
```

## ⚠️ Points d'Attention

### Sécurité
- Les responsables de commune ne peuvent **jamais** modifier les missions
- Seuls les responsables de quartier et admin peuvent changer les statuts
- Vérification des permissions à chaque action

### Performance  
- Requêtes optimisées selon le rôle
- Filtrage automatique des missions visibles
- Statistiques calculées en temps réel

### Maintenance
- Commande de nettoyage disponible : `python manage.py clean_agents`
- Logs détaillés des actions selon les rôles
- Possibilité d'audit des modifications

## 🔄 Migration depuis l'ancien système

Si vous avez des agents existants sans rôles :

1. **Backup** de la base de données
2. **Migration** : `python manage.py migrate`
3. **Initialisation** : `python manage.py setup_agent_roles`
4. **Test** : Connexion avec différents rôles
5. **Création superviseurs** : `--create-commune-supervisors`

## 🆘 Dépannage

### Problème : Agent ne peut pas modifier mission
**Cause** : Rôle 'commune' ou permissions insuffisantes
**Solution** : Vérifier `agent.role` et `agent.can_modify_mission(mission)`

### Problème : Responsable commune ne voit pas toutes les missions
**Cause** : Filtre de commune incorrect
**Solution** : Vérifier `agent.commune` correspond aux missions

### Problème : Erreur de connexion  
**Cause** : Format mot de passe incorrect
**Solution** : Utiliser format `commune+quartier`

---

*Système développé pour optimiser la gestion des signalements avec une hiérarchie claire et des permissions adaptées à chaque niveau de responsabilité.*