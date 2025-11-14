# 📧 Templates Email - Regideso

## Vue d'ensemble

Cette documentation présente le système de templates email mis en place pour la plateforme de signalement de fuites d'eau de Regideso. Les templates utilisent un design moderne, responsive et professionnel pour améliorer l'expérience utilisateur.

## 🎨 Design System

### Couleurs principales
- **Bleu principal**: `#3b82f6` (Boutons, liens)
- **Bleu foncé**: `#1d4ed8` (Headers, accents)
- **Vert succès**: `#10b981` (Confirmations, statuts positifs)
- **Orange attention**: `#f59e0b` (Alertes, priorités moyennes)
- **Rouge critique**: `#dc2626` (Urgences, erreurs)
- **Gris texte**: `#4b5563` (Texte secondaire)
- **Gris fond**: `#f4f7fa` (Arrière-plan)

### Typographie
- **Font principale**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Font monospace**: 'Courier New' (codes OTP)
- **Tailles**: 16px (texte), 24px (h2), 18px (h3)

## 📁 Structure des fichiers

```
reports/templates/email/
├── base.html                 # Template de base commun
├── confirmation.html         # Confirmation de signalement
├── mission_notification.html # Notification de mission
├── otp_verification.html     # Code de vérification OTP
├── status_update.html        # Mise à jour de statut
└── welcome.html              # Email de bienvenue
```

## 🧩 Templates disponibles

### 1. base.html
**Template parent** utilisé par tous les autres templates.

**Fonctionnalités:**
- Header avec logo et titre personnalisables
- Styles CSS complets pour email (compatibilité Outlook)
- Footer avec informations de contact
- Liens sociaux et désabonnement
- Design responsive

**Blocks disponibles:**
- `title`: Titre de la page
- `header_title`: Titre dans le header
- `header_subtitle`: Sous-titre dans le header
- `content`: Contenu principal

### 2. confirmation.html
**Email envoyé** après un signalement réussi.

**Contexte requis:**
- `fuite`: Objet Fuite contenant les détails du signalement

**Contenu:**
- Confirmation du signalement avec numéro de référence
- Détails complets du signalement
- Prochaines étapes du processus
- Conseils en attendant l'intervention
- Contact d'urgence

### 3. mission_notification.html
**Email envoyé** quand une mission d'intervention est planifiée.

**Contexte requis:**
- `mission`: Objet Mission avec les détails
- `fuite`: Objet Fuite associé

**Contenu:**
- Informations de la mission planifiée
- Coordonnées de l'équipe d'intervention
- Instructions pour le jour J
- Boutons d'action (contact équipe, suivi)

### 4. otp_verification.html
**Email avec le code OTP** pour vérification.

**Contexte requis:**
- `otp_code`: Code de vérification à 6 chiffres

**Contenu:**
- Code OTP mis en évidence
- Instructions d'utilisation
- Informations de sécurité
- Aide en cas de problème

### 5. status_update.html
**Email de mise à jour** du statut d'un signalement.

**Contexte requis:**
- `fuite`: Objet Fuite concerné
- `status`: Nouveau statut (verified, in_progress, resolved, closed)
- `message`: Message personnalisé (optionnel)

**Contenu adaptatif selon le statut:**
- Progression visuelle avec étapes
- Messages contextuels
- Actions disponibles selon l'état

### 6. welcome.html
**Email de bienvenue** pour nouveaux utilisateurs.

**Contexte requis:**
- `name`: Nom du destinataire (optionnel)

**Contenu:**
- Guide de démarrage rapide
- Fonctionnalités principales
- Conseils d'utilisation
- Statistiques de la plateforme
- Ressources utiles

## 🛠️ Utilisation dans le code

### Configuration des fonctions utils.py

```python
from reports.utils import (
    send_confirmation_email,
    send_mission_notification_email,
    send_otp_email,
    send_status_update_email,
    send_welcome_email
)

# Confirmation après signalement
send_confirmation_email(fuite_obj)

# Notification de mission
send_mission_notification_email(mission_obj)

# Code OTP
send_otp_email("user@email.com", "123456")

# Mise à jour de statut
send_status_update_email(fuite_obj, "verified", "Message optionnel")

# Bienvenue
send_welcome_email("user@email.com", "Nom Utilisateur")
```

## 📱 Compatibilité

### Clients email testés
- ✅ Gmail (Web, Mobile)
- ✅ Outlook (2016+, Web, Mobile)
- ✅ Apple Mail (macOS, iOS)
- ✅ Thunderbird
- ✅ Yahoo Mail
- ✅ Clients mobiles génériques

### Fonctionnalités responsive
- Adaptation automatique mobile (< 600px)
- Grilles flexibles
- Images adaptatives
- Navigation simplifiée sur mobile

## 🎯 Bonnes pratiques

### Contenu
- **Concis et clair**: Messages directs et informatifs
- **Action-oriented**: Boutons d'action visibles
- **Contextualisé**: Informations personnalisées
- **Progressif**: Guidance étape par étape

### Technique
- **Inline CSS**: Pour compatibilité email
- **Tables pour layout**: Support Outlook
- **Alt text**: Sur toutes les images
- **Fallbacks**: Couleurs et polices de sécurité

### Accessibilité
- **Contraste**: Minimum WCAG AA (4.5:1)
- **Taille de police**: Minimum 16px
- **Zone de clic**: Minimum 44px
- **Structure sémantique**: Headers hiérarchiques

## 🧪 Tests

### Script de test
```bash
cd /home/mandi-stone/Documents/projettutore
python manage.py shell < reports/test_email_templates.py
```

### Fichiers générés
Le script génère des fichiers HTML de prévisualisation dans `/tmp/`:
- `test_confirmation.html`
- `test_mission.html`
- `test_otp.html`
- `test_status_verified.html`
- `test_status_in_progress.html`
- `test_status_resolved.html`
- `test_welcome.html`

## 🔧 Maintenance

### Modification des styles
1. Éditer `base.html` pour les styles généraux
2. Tester dans multiple clients email
3. Valider la responsivité
4. Vérifier l'accessibilité

### Ajout d'un nouveau template
1. Créer le fichier dans `email/`
2. Étendre `base.html`
3. Ajouter la fonction dans `utils.py`
4. Documenter le contexte requis
5. Ajouter aux tests

### Personnalisation
- **Logo**: Modifier l'emoji dans `base.html` header
- **Couleurs**: Ajuster les variables CSS
- **Contact**: Mettre à jour le footer
- **Liens sociaux**: Modifier les URLs dans le footer

## 📊 Métriques et suivi

### Données à suivre
- Taux d'ouverture des emails
- Taux de clic sur les boutons d'action
- Temps de validation OTP
- Satisfaction utilisateur

### Optimisations possibles
- A/B testing des sujets
- Personnalisation avancée
- Segmentation par type d'utilisateur
- Optimisation mobile continue

---

**Note**: Ces templates sont optimisés pour une expérience utilisateur moderne tout en maintenant une compatibilité maximale avec les différents clients email. Ils constituent une base solide pour la communication professionnelle de Regideso.