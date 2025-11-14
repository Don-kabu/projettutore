# 🚰 Système de Signalement de Fuites d'Eau
## Application Django pour la Gestion des Signalements et Missions de Réparation

![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)

---

## 📋 Table des Matières
- [Vue d'ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API et Endpoints](#api-et-endpoints)
- [Modèles de données](#modèles-de-données)
- [Workflow de l'application](#workflow-de-lapplication)
- [Système d'emails](#système-demails)
- [Administration](#administration)
- [Dépannage](#dépannage)

---

## 🎯 Vue d'ensemble

Cette application Django permet aux citoyens de **signaler des fuites d'eau** dans leur commune et automatise la gestion des **missions de réparation** pour les équipes techniques. Le système intègre un processus de validation par OTP (One-Time Password) et un système de notifications par email.

### Problème résolu
- **Signalement simplifié** des fuites d'eau par les citoyens
- **Vérification automatique** des signalements via OTP
- **Attribution automatique** des missions aux équipes techniques  
- **Notifications email** pour toutes les parties prenantes
- **Traçabilité complète** des signalements et réparations

---

## ✨ Fonctionnalités

### 👤 Pour les Citoyens
- ✅ **Signalement en 3 étapes** : Informations personnelles → Vérification OTP → Détails de la fuite
- ✅ **Vérification par OTP** envoyé par email ou SMS
- ✅ **Upload de photos** de la fuite
- ✅ **Sélection géographique** : Commune et quartier
- ✅ **Email de confirmation** automatique

### 🔧 Pour les Équipes Techniques
- ✅ **Création automatique de missions** quand un signalement est validé
- ✅ **Notifications email** avec tous les détails de la mission
- ✅ **Interface d'administration** pour gérer les missions
- ✅ **Suivi du statut** des réparations

### 🏛️ Pour les Administrateurs
- ✅ **Interface Django Admin** complète
- ✅ **Gestion des utilisateurs** et permissions
- ✅ **Statistiques** sur les signalements et missions
- ✅ **Configuration** des communes et quartiers

---

## 🏗️ Architecture

### 📁 Arborescence Complète du Projet

```
projettutore/
├── 📄 .gitignore                    # Fichiers ignorés par Git
├── 📄 CHANGELOG.md                  # Journal des modifications
├── 📄 EMAIL_TEMPLATES_README.md     # Documentation des templates email
├── 📄 QUICKSTART.md                 # Guide de démarrage rapide
├── 📄 README.md                     # Documentation principale (ce fichier)
├── 📄 TECHNICAL_GUIDE.md            # Guide technique détaillé
├── 📄 manage.py                     # Script de gestion Django
├── 📄 requirements.txt              # Dépendances Python
├── 📄 db.sqlite3                    # Base de données SQLite
│
├── 📁 Signalement/                  # 🏛️ Configuration principale Django
│   ├── __init__.py
│   ├── asgi.py                      # Configuration ASGI (async)
│   ├── settings.py                  # Configuration de l'application
│   ├── urls.py                      # URLs principales du projet
│   ├── views.py                     # Vues globales
│   ├── wsgi.py                      # Configuration WSGI
│   └── __pycache__/                 # Cache Python compilé
│
├── 📁 reports/                      # 🚰 Application principale de signalement
│   ├── __init__.py
│   ├── admin.py                     # Interface d'administration Django
│   ├── adresse.py                   # Données géographiques (communes/quartiers)
│   ├── apps.py                      # Configuration de l'application
│   ├── forms.py                     # Formulaires Django (FuiteForm, complaintForm)
│   ├── models.py                    # Modèles de données (Fuite, Mission, AgentProfile)
│   ├── tests.py                     # Tests unitaires
│   ├── urls.py                      # URLs de l'application reports
│   ├── utils.py                     # Utilitaires (emails, OTP, notifications)
│   ├── views.py                     # Logique métier et contrôleurs
│   ├── __pycache__/                 # Cache Python compilé
│   │
│   ├── 📁 migrations/               # 🗃️ Migrations de base de données
│   │   ├── __init__.py
│   │   ├── 0001_initial.py          # Migration initiale
│   │   ├── 0002_fuite_delete_report.py
│   │   ├── 0003_remove_fuite_latitude_remove_fuite_longitude_and_more.py
│   │   ├── 0004_fuite_is_owner.py
│   │   ├── 0005_rename_comname_fuite_complaint_name_fuite_commune_and_more.py
│   │   ├── 0006_alter_fuite_quartier.py
│   │   ├── 0007_alter_fuite_quartier.py
│   │   ├── 0008_alter_fuite_quartier.py
│   │   ├── 0009_alter_fuite_quartier.py
│   │   ├── 0010_fuite_opt.py
│   │   ├── 0011_fuite_verified_opt.py
│   │   ├── 0012_mission.py
│   │   ├── 0013_mission_resolver_email_mission_resolver_phone.py
│   │   ├── 0014_fuite_email_alter_mission_resolver_email_and_more.py
│   │   ├── 0015_agentprofile_mission_mission_status.py
│   │   ├── 0016_alter_agentprofile_email.py
│   │   └── __pycache__/
│   │
│   ├── 📁 static/                   # 🎨 Fichiers statiques de l'app
│   │   ├── 📁 css/
│   │   │   ├── base.css             # Styles CSS de base (variables, layout responsive)
│   │   │   ├── forms.css            # Styles spécifiques aux formulaires
│   │   │   └── override-tailwind.css # Override pour forcer les couleurs de texte
│   │   └── 📁 js/
│   │       └── forms-enhancement.js  # JavaScript pour l'UX des formulaires
│   │
│   └── 📁 templates/                # 🌐 Templates HTML
│       ├── base.html                # Template de base (header, nav, footer)
│       ├── accueil.html             # Page d'accueil redesignée
│       ├── accueil_old.html         # Ancienne version de l'accueil
│       ├── signaler.html            # Formulaire de signalement principal
│       ├── recherche_signalement.html # Recherche de signalements
│       ├── suivi_signalement.html   # Suivi des signalements
│       ├── test_css.html            # Page de test pour les styles CSS
│       │
│       ├── 📁 agent/                # 👷 Interface agent/technicien
│       │   ├── dashboard.html       # Tableau de bord agent
│       │   ├── init_success.html    # Page de succès d'initialisation
│       │   ├── login.html           # Connexion agent
│       │   ├── mission_detail.html  # Détails d'une mission
│       │   ├── missions_list.html   # Liste des missions
│       │   └── test.html            # Page de test agent
│       │
│       └── 📁 email/                # 📧 Templates d'emails HTML
│           ├── base.html            # Template de base pour emails
│           ├── confirmation.html    # Email de confirmation de signalement
│           ├── mission_notification.html # Notification de nouvelle mission
│           ├── otp_verification.html # Email de vérification OTP
│           ├── status_update.html   # Mise à jour de statut de mission
│           └── welcome.html         # Email de bienvenue
│
├── 📁 media/                        # 📸 Fichiers médias uploadés
│   └── 📁 fuites/                   # Photos des fuites signalées
│
└── � static/                       # 🌐 Fichiers statiques globaux
    └── [fichiers statiques collectés par Django]
```

### 🔧 Architecture Technique

#### Frontend Stack
- **🎨 CSS Framework** : Tailwind CSS + CSS personnalisé
- **🎭 Icons** : Heroicons, Feather Icons
- **🔤 Polices** : Poppins (Google Fonts)
- **📱 Responsive** : Mobile-first design
- **⚡ JavaScript** : Vanilla JS pour l'UX

#### Backend Stack  
- **🐍 Framework** : Django 5.2
- **🗃️ Base de données** : SQLite (dev) / PostgreSQL (prod)
- **📧 Emails** : Django Email Backend (SMTP)
- **📁 Fichiers** : Django FileField avec upload vers /media/
- **🔐 Authentification** : Django Auth + système OTP personnalisé

#### Sécurité & Performance
- **🛡️ CSRF Protection** : Tokens Django
- **🔒 XSS Protection** : Template escaping automatique
- **📝 Validation** : Forms Django + validation JavaScript
- **⚡ Cache** : Django template cache (futur)

---

## ⚙️ Installation

### Prérequis
- **Python 3.12+**
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel)

### 1. Cloner le projet
```bash
git clone https://github.com/benitobapela/signalement-fuite-eau.git
cd signalement-fuite-eau
```

### 2. Créer l'environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# ou
env\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install django
pip install pillow  # Pour la gestion des images
```

### 4. Configuration de la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

L'application sera accessible sur : **http://127.0.0.1:8000/**

---

## 🔧 Configuration

### Configuration Email (dans `settings.py`)

#### Pour Gmail :
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'  # Mot de passe d'application
DEFAULT_FROM_EMAIL = 'votre-email@gmail.com'
```

#### Pour le développement (console) :
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Configuration des Communes et Quartiers
Modifiez le fichier `reports/adresse.py` :
```python
adresse = {
    'Kinshasa': ['Gombe', 'Kalamu', 'Lingwala', 'Bandalungwa'],
    'Lubumbashi': ['Kenya', 'Katuba', 'Annexe'],
    # Ajoutez vos communes et quartiers
}
```

---

## 🚀 Utilisation

### 1. Processus de Signalement Citoyen

#### Étape 1 : Informations du Signaleur
- **URL** : `/signaler/`
- **Champs** : Nom, téléphone, email, commune, propriétaire/locataire
- **Action** : Génération automatique d'un OTP et envoi par email

#### Étape 2 : Vérification OTP  
- **URL** : `/signaler/{id}/otp`
- **Méthodes** :
  - Saisie manuelle du code OTP
  - Vérification automatique via lien email (`?otp=123456`)
- **Action** : Validation du signalement

#### Étape 3 : Détails de la Fuite
- **URL** : `/signaler/{id}`
- **Champs** : Description, photo, adresse précise, quartier
- **Action** : Finalisation du signalement

### 2. Processus Automatique de Mission

Quand un signalement est finalisé (`status = "OK"`) :

1. **Création automatique** d'une mission
2. **Attribution** à l'équipe technique de la zone
3. **Envoi d'email** de notification avec tous les détails
4. **Traçabilité** complète dans l'interface admin

---

## 🔗 API et Endpoints

| Endpoint | Méthode | Description | Paramètres |
|----------|---------|-------------|------------|
| `/` | GET | Page d'accueil | Aucun |
| `/signaler/` | GET/POST | Étape 1 : Infos signaleur | form: complaintForm |
| `/signaler/{id}/otp` | GET/POST | Vérification OTP | pk, ?otp (query param) |
| `/signaler/{id}` | GET/POST | Étape 2 : Détails fuite | pk, form: FuiteForm |
| `/admin/` | GET | Interface administration | Auth requise |

### Exemples d'URLs avec paramètres :
```
# Vérification OTP automatique
/signaler/1/otp?otp=1234567

# Vérification OTP manuelle  
/signaler/1/otp (formulaire)

# Finalisation du signalement
/signaler/1 (upload photo + détails)
```

---

## 📊 Modèles de Données

### 🚰 Modèle `Fuite`
```python
class Fuite(models.Model):
    description = models.TextField()                    # Description de la fuite
    photo = models.ImageField(upload_to="fuites/")     # Photo de la fuite
    date_signalement = models.DateTimeField(auto_now_add=True)  # Date automatique
    status = models.CharField(default="NOK")            # NOK → OK (validé)
    phone = models.CharField(max_length=15)             # Téléphone signaleur
    complaint_name = models.CharField(max_length=100)   # Nom signaleur
    email = models.EmailField()                         # Email pour notifications
    address = models.CharField(max_length=255)          # Adresse précise
    is_owner = models.BooleanField(default=False)       # Propriétaire/Locataire
    commune = models.CharField(choices=...)             # Commune sélectionnée
    quartier = models.CharField(choices=...)            # Quartier sélectionné
    opt = models.CharField()                            # Code OTP généré
    verified_opt = models.BooleanField(default=False)   # OTP vérifié
```

### 🔧 Modèle `Mission`
```python  
class Mission(models.Model):
    description = models.TextField()                    # Description automatique
    fuite = models.OneToOneField(Fuite)                # Relation 1:1 avec Fuite
    created_at = models.DateTimeField(auto_now_add=True) # Date création
    resolved_at = models.DateTimeField(null=True)      # Date résolution
    status = models.CharField(default='NOT RESOLVED')  # Statut mission
    remember_count = models.IntegerField(default=0)    # Compteur rappels
    resolver_phone = models.CharField()                 # Téléphone technicien
    resolver_email = models.EmailField()               # Email technicien
```

---

## ⚡ Workflow de l'application

```mermaid
graph TD
    A[👤 Citoyen accède à /signaler/] --> B[📝 Remplit infos personnelles]
    B --> C[🔢 Génération OTP automatique]
    C --> D[📧 Envoi email avec lien OTP]
    D --> E{✅ Vérification OTP}
    E -->|❌ Échec| F[🔄 Nouveau OTP généré]
    E -->|✅ Succès| G[📋 Formulaire détails fuite]
    F --> D
    G --> H[📸 Upload photo + description]
    H --> I[✅ Signalement validé status=OK]
    I --> J[🔧 Création automatique Mission]
    J --> K[📧 Email notification équipe technique]
    K --> L[🏁 Fin du processus]
```

### Détail des Signaux Django

#### Signal `post_save` sur `Fuite` :
```python
@receiver(post_save, sender=Fuite)
def affecter_travail(sender, instance, created, **kwargs):
    # Si nouvelle fuite créée avec email → Envoi confirmation
    if created and instance.email:
        send_confirmation_email(instance)
    
    # Si fuite validée → Création mission automatique
    if instance.status == "OK":
        Mission.objects.create(...)
```

#### Signal `post_save` sur `Mission` :
```python
@receiver(post_save, sender=Mission)  
def send_notification(sender, instance, created, **kwargs):
    # Si nouvelle mission → Email équipe technique
    if created:
        send_mission_notification_email(instance)
```

---

## 📧 Système d'Emails

### Types d'emails automatiques :

#### 1. **Email de Confirmation Citoyen**
- **Déclencheur** : Création d'une nouvelle fuite
- **Destinataire** : Email du signaleur
- **Contenu** :
  - Code OTP
  - Lien de vérification automatique
  - Instructions

#### 2. **Email de Mission Technique**  
- **Déclencheur** : Création d'une nouvelle mission
- **Destinataire** : Email de l'équipe technique
- **Contenu** :
  - Détails complets de la fuite
  - Localisation précise
  - Photo de la fuite
  - Contact du signaleur

### Configuration avancée :
```python
# Dans reports/utils.py
def send_confirmation_email(fuite):
    subject = "Confirmation de votre signalement de fuite"
    verification_link = f"http://127.0.0.1:8000/signaler/{fuite.pk}/otp?otp={fuite.opt}"
    
    message = f"""
    Merci pour votre signalement !
    
    Code de vérification : {fuite.opt}
    Lien automatique : {verification_link}
    """
    
    send_mail(subject, message, DEFAULT_FROM_EMAIL, [fuite.email])
```

---

## 👨‍💼 Administration

### Accès à l'interface admin :
**URL** : `http://127.0.0.1:8000/admin/`

### Fonctionnalités admin disponibles :

#### Gestion des Fuites :
- ✅ Liste de tous les signalements
- ✅ Filtrage par commune, quartier, statut
- ✅ Recherche par nom, téléphone, email
- ✅ Modification du statut
- ✅ Visualisation des photos

#### Gestion des Missions :
- ✅ Liste de toutes les missions
- ✅ Attribution à différentes équipes
- ✅ Suivi des résolutions
- ✅ Historique des interventions
- ✅ Compteur de rappels

#### Statistiques (à développer) :
- 📊 Nombre de signalements par commune
- 📊 Temps moyen de résolution
- 📊 Équipes les plus actives

---

## 🛠️ Dépannage

### Problèmes courants :

#### ❌ **Erreur "No module named 'PIL'"**
```bash
pip install pillow
```

#### ❌ **Erreur d'envoi d'email**
- Vérifiez la configuration EMAIL_* dans settings.py
- Pour Gmail : Utilisez un mot de passe d'application
- Pour développement : Utilisez console backend

#### ❌ **Images ne s'affichent pas**
```python
# Dans settings.py, ajoutez :
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Dans urls.py principal :
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [...] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### ❌ **OTP ne fonctionne pas**
- Vérifiez que l'OTP est bien généré : `fuite.generate_otp`
- Vérifiez les logs email dans la console
- Testez avec le lien direct : `/signaler/1/otp?otp=123456`

### Logs de débogage :
```python
# Dans settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## 🚀 Déploiement en Production

### Checklist de sécurité :
- [ ] `DEBUG = False` dans settings.py
- [ ] Configuration des `ALLOWED_HOSTS`
- [ ] Variables d'environnement pour les secrets
- [ ] Base de données PostgreSQL/MySQL
- [ ] Serveur web (nginx + gunicorn)
- [ ] HTTPS activé
- [ ] Sauvegarde automatique de la DB

### Variables d'environnement recommandées :
```bash
export DJANGO_SECRET_KEY="votre-clé-secrete"
export EMAIL_HOST_USER="votre-email@gmail.com"
export EMAIL_HOST_PASSWORD="votre-mot-de-passe"
export DATABASE_URL="postgres://user:pass@localhost/db"
```

---

## 📝 Développement et Contribution

### Structure du code :
- **Models** : Logique métier et base de données
- **Views** : Contrôleurs et logique de présentation  
- **Forms** : Validation et rendu des formulaires
- **Templates** : Interface utilisateur HTML
- **Utils** : Fonctions utilitaires (emails, etc.)

### Tests (à développer) :
```bash
python manage.py test reports
```

### Améliorations futures :
- [ ] API REST pour mobile
- [ ] Notifications SMS
- [ ] Géolocalisation automatique
- [ ] Dashboard statistiques
- [ ] Multi-langue
- [ ] Système de ratings des réparations

---

## 📞 Support et Contact

**Développeur** : Benito Bapela  
**Repository** : [signalement-fuite-eau](https://github.com/benitobapela/signalement-fuite-eau)  
**Issues** : Utilisez GitHub Issues pour signaler des bugs

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

*Application développée avec ❤️ en Django pour améliorer la gestion des services publics*