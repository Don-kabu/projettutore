# 📋 Guide de Démarrage Rapide

## Installation en 5 minutes

### 1. Prérequis
```bash
# Vérifier Python
python --version  # Python 3.12+

# Vérifier pip
pip --version
```

### 2. Installation rapide
```bash
# Cloner et naviguer
git clone https://github.com/benitobapela/signalement-fuite-eau.git
cd signalement-fuite-eau

# Environnement virtuel
python -m venv env
source env/bin/activate  # Linux/Mac
# env\Scripts\activate   # Windows

# Dépendances
pip install django pillow

# Base de données
python manage.py makemigrations
python manage.py migrate

# Superuser (optionnel)
python manage.py createsuperuser

# Lancer l'app
python manage.py runserver
```

### 3. Accès rapide
- **Application** : http://127.0.0.1:8000/
- **Admin** : http://127.0.0.1:8000/admin/
- **Signaler** : http://127.0.0.1:8000/signaler/

---

## 🧪 Test rapide du système

### Scenario de test complet :

1. **Aller sur** : http://127.0.0.1:8000/signaler/
2. **Remplir** : Nom, téléphone, email, commune
3. **Noter l'OTP affiché** dans la console Django
4. **Aller sur** : http://127.0.0.1:8000/signaler/1/otp
5. **Saisir l'OTP** ou utiliser le lien avec `?otp=123456`
6. **Finaliser** avec photo et description
7. **Vérifier dans l'admin** la mission créée automatiquement

---

## 📧 Configuration Email Rapide

### Mode Console (Développement)
Dans `settings.py` :
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Les emails s'affichent dans la console Django.

### Mode Gmail (Production)
1. **Générer mot de passe d'application Gmail**
2. **Modifier settings.py** :
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'
DEFAULT_FROM_EMAIL = 'votre-email@gmail.com'
```

---

## 🛠️ Personnalisation Rapide

### Ajouter vos communes
Dans `reports/adresse.py` :
```python
adresse = {
    'VotreVille': ['Quartier1', 'Quartier2', 'Quartier3'],
    'AutreVille': ['Zone1', 'Zone2'],
}
```

### Modifier les templates
- **Page d'accueil** : `reports/templates/accueil.html`
- **Formulaires** : `reports/templates/signaler.html`
- **Base template** : `reports/templates/base.html`

---

## 🎯 Cas d'Usage Principaux

### 1. Signalement Citoyen Standard
```
Citoyen → /signaler/ → Infos personnelles → OTP email → Détails + photo → Mission créée
```

### 2. Signalement avec Vérification Automatique
```
Email reçu → Clic lien OTP → Vérification automatique → Étape 2 directement
```

### 3. Gestion Administrative
```
Admin → /admin/ → Consulter signalements → Assigner missions → Suivre résolutions
```

---

## 📱 Améliorations Suggérées

### Court terme :
- [ ] Interface responsive mobile
- [ ] Validation JavaScript des formulaires
- [ ] Aperçu photo avant upload
- [ ] Notification toast de succès

### Moyen terme :
- [ ] API REST pour application mobile
- [ ] Géolocalisation automatique
- [ ] Notifications SMS
- [ ] Système de rating des réparations

### Long terme :
- [ ] Dashboard analytics
- [ ] Multi-tenant (plusieurs villes)
- [ ] IA pour catégorisation automatique
- [ ] Integration avec systèmes municipaux

---

*🚀 Votre application est prête ! Pour plus de détails, consultez le README.md principal.*