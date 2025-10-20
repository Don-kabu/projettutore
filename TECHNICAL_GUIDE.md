# 🔧 Guide Technique - Architecture et Développement

## 📐 Architecture Détaillée

### Structure des Données

```python
# Flux de données principal
Citoyen → ComplaintForm → Fuite(NOK) → OTP → Verification → Fuite(OK) → Mission → Email Technicien
```

### Modèles et Relations

```python
class Fuite(models.Model):
    # Données citoyens
    complaint_name = CharField()     # Nom du signaleur
    phone = CharField()              # Téléphone contact
    email = EmailField()             # Email pour notifications
    is_owner = BooleanField()        # Propriétaire/Locataire
    
    # Localisation
    commune = CharField(choices=...)  # Commune sélectionnée
    quartier = CharField(choices=...) # Quartier sélectionné
    address = CharField()            # Adresse précise
    
    # Signalement
    description = TextField()        # Description de la fuite
    photo = ImageField()            # Photo de la fuite
    date_signalement = DateTimeField() # Date automatique
    
    # Workflow
    status = CharField(default="NOK") # NOK → OK
    opt = CharField()                # Code OTP généré
    verified_opt = BooleanField()    # OTP validé
    
    # Méthodes
    @property
    def generate_otp(self):
        """Génère un OTP unique basé sur l'ID + random"""
        self.opt = f'{self.pk}{random.randint(100,999)}'
        self.save()
        
class Mission(models.Model):
    # Relation
    fuite = OneToOneField(Fuite)    # Une mission par fuite
    
    # Mission
    description = TextField()        # Description auto-générée
    created_at = DateTimeField()    # Date création
    resolved_at = DateTimeField()   # Date résolution
    status = CharField()            # Status mission
    remember_count = IntegerField() # Compteur rappels
    
    # Assignation
    resolver_phone = CharField()    # Téléphone technicien
    resolver_email = EmailField()   # Email technicien
```

### Signaux Django - Architecture Événementielle

```python
@receiver(post_save, sender=Fuite)
def workflow_fuite(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque sauvegarde de Fuite
    Gère le workflow automatique selon le contexte
    """
    fuite = instance
    
    # Nouveau signalement → Email confirmation
    if created and fuite.email:
        send_confirmation_email(fuite)
        print(f"📧 Email confirmation envoyé à {fuite.email}")
    
    # Signalement validé → Création mission
    if fuite.status == "OK" and not hasattr(fuite, 'mission'):
        mission = Mission.objects.create(
            description=generate_mission_description(fuite),
            fuite=fuite,
            resolver_phone=get_resolver_contact(fuite.commune, fuite.quartier)['phone'],
            resolver_email=get_resolver_contact(fuite.commune, fuite.quartier)['email']
        )
        print(f"🔧 Mission {mission.pk} créée pour fuite {fuite.pk}")

@receiver(post_save, sender=Mission)  
def workflow_mission(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque sauvegarde de Mission
    Gère les notifications aux équipes techniques
    """
    mission = instance
    
    # Nouvelle mission → Email technicien
    if created:
        email_sent = send_mission_notification_email(mission)
        if email_sent:
            print(f"✅ Notification mission envoyée à {mission.resolver_email}")
        else:
            print(f"❌ Échec notification pour mission {mission.pk}")
    
    # Mission résolue → Email confirmation (futur)
    if mission.status == "RESOLVED" and mission.resolved_at:
        print(f"🎉 Mission {mission.pk} marquée comme résolue")
```

---

## 🔄 États et Transitions

### Machine à États - Signalement

```
[INITIAL] → ComplaintForm → [FUITE_CREATED(NOK)]
    ↓
[OTP_SENT] → Verification → [OTP_VERIFIED] 
    ↓
[DETAILS_FORM] → Photo+Description → [FUITE_VALIDATED(OK)]
    ↓
[MISSION_CREATED] → Email Technicien → [WORKFLOW_COMPLETE]
```

### Statuts Possibles

| Modèle | Champ | Valeurs | Description |
|--------|-------|---------|-------------|
| Fuite | status | NOK | Signalement non finalisé |
| Fuite | status | OK | Signalement validé et complet |
| Fuite | verified_opt | False | OTP non vérifié |
| Fuite | verified_opt | True | OTP vérifié |
| Mission | status | NOT RESOLVED | Mission en attente |
| Mission | status | IN PROGRESS | Mission en cours |
| Mission | status | RESOLVED | Mission terminée |

---

## 🔧 Formulaires et Validation

### Étape 1 : ComplaintForm
```python
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Fuite
        fields = ['complaint_name', 'phone', 'is_owner', 'commune', 'email']
    
    # Validation personnalisée
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\+?[\d\s-]{10,15}$', phone):
            raise ValidationError("Format de téléphone invalide")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if email and not email.endswith(('.com', '.org', '.net')):
            raise ValidationError("Domaine email non autorisé")
        return email
```

### Étape 2 : OTPForm
```python
class OptForm(forms.Form):
    otp = forms.CharField(
        max_length=7,
        min_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'Code de vérification',
            'class': 'form-control'
        })
    )
    
    def clean_otp(self):
        otp = self.cleaned_data['otp']
        if not otp.isdigit():
            raise ValidationError("Le code OTP doit contenir uniquement des chiffres")
        return otp
```

### Étape 3 : FuiteForm  
```python
class FuiteForm(forms.ModelForm):
    class Meta:
        model = Fuite
        fields = ['quartier', 'photo', 'description', 'address']
    
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            if photo.size > 5 * 1024 * 1024:  # 5MB max
                raise ValidationError("Image trop grande (max 5MB)")
            if not photo.content_type.startswith('image/'):
                raise ValidationError("Seules les images sont autorisées")
        return photo
```

---

## 🌐 Vues et Logique Métier

### Vue Principale - signaler1()
```python
def signaler1(request):
    """
    Étape 1: Collecte des informations personnelles
    Génère un OTP et redirige vers la vérification
    """
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # Sauvegarde avec status NOK par défaut
            fuite = form.save(commit=False)
            fuite.save()  # Déclenche le signal post_save
            
            # Génération OTP automatique
            fuite.generate_otp  # Property qui génère et sauvegarde
            
            # Redirection vers vérification
            return redirect("verify_phone_number", fuite.pk)
    else:
        form = ComplaintForm()
    
    return render(request, 'signaler.html', {'form': form})
```

### Vue OTP - verifyotp()
```python
def verifyotp(request, pk):
    """
    Étape 2: Vérification OTP (manuel ou automatique)
    Support des query parameters pour vérification automatique
    """
    fuite = get_object_or_404(Fuite, pk=pk)
    otp_from_url = request.GET.get('otp')  # Paramètre automatique
    
    if not fuite.verified_opt:
        # Vérification automatique via URL
        if otp_from_url and fuite.opt == otp_from_url:
            fuite.verified_opt = True
            fuite.save()
            return redirect("signaler.step2", fuite.pk)
        
        # Vérification manuelle via formulaire
        if request.method == 'POST':
            form = OptForm(request.POST)
            if form.is_valid() and fuite.opt == form.data.get("otp"):
                fuite.verified_opt = True
                fuite.save()
                return redirect("signaler.step2", fuite.pk)
            else:
                fuite.generate_otp  # Nouveau OTP en cas d'erreur
        
        form = OptForm()
        return render(request, 'signaler.html', {'form': form})
    
    return redirect('accueil')  # Déjà vérifié
```

### Vue Finalisation - signaler2()
```python
def signaler2(request, pk):
    """
    Étape 3: Finalisation avec photo et détails
    Change le status à OK, déclenchant la création de mission
    """
    fuite = get_object_or_404(Fuite, pk=pk)
    
    # Vérifications de sécurité
    if not fuite.verified_opt or fuite.status == "OK":
        return redirect("accueil")
    
    if request.method == 'POST':
        form = FuiteForm(request.POST, request.FILES, instance=fuite)
        if form.is_valid():
            fuite = form.save(commit=False)
            fuite.status = "OK"  # Déclenche création mission
            fuite.save()
            
            return render(request, "base.html", {
                'success': True,
                'fuite_id': fuite.pk
            })
    else:
        form = FuiteForm()
        # Choix dynamiques selon commune
        if fuite.commune in adresse:
            quartiers_list = adresse[fuite.commune]
            form.fields["quartier"].choices = zip(quartiers_list, quartiers_list)
    
    return render(request, 'signaler.html', {'form': form})
```

---

## 📧 Système d'Emails Avancé

### Configuration Multi-Backend
```python
# settings.py
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

### Templates d'Emails
```python
def send_confirmation_email(fuite):
    """Email de confirmation avec template HTML"""
    context = {
        'fuite': fuite,
        'verification_link': f"http://127.0.0.1:8000/signaler/{fuite.pk}/otp?otp={fuite.opt}",
        'manual_link': f"http://127.0.0.1:8000/signaler/{fuite.pk}/otp",
        'otp_code': fuite.opt
    }
    
    # Template HTML
    html_content = render_to_string('email/confirmation.html', context)
    text_content = render_to_string('email/confirmation.txt', context)
    
    email = EmailMultiAlternatives(
        subject="Confirmation de votre signalement",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[fuite.email]
    )
    email.attach_alternative(html_content, "text/html")
    
    return email.send()

def send_mission_notification_email(mission):
    """Email de notification mission avec détails complets"""
    context = {
        'mission': mission,
        'fuite': mission.fuite,
        'admin_link': f"http://127.0.0.1:8000/admin/reports/mission/{mission.pk}/",
        'contact_signaleur': {
            'nom': mission.fuite.complaint_name,
            'phone': mission.fuite.phone,
            'email': mission.fuite.email
        }
    }
    
    html_content = render_to_string('email/mission_notification.html', context)
    text_content = render_to_string('email/mission_notification.txt', context)
    
    email = EmailMultiAlternatives(
        subject=f"Nouvelle Mission #{mission.pk} - {mission.fuite.commune}",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[mission.resolver_email]
    )
    email.attach_alternative(html_content, "text/html")
    
    return email.send()
```

---

## 🔐 Sécurité et Validation

### Validation des Uploads
```python
def validate_image_upload(image):
    """Validation sécurisée des images"""
    # Taille maximum
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Image trop grande")
    
    # Type MIME
    if not image.content_type.startswith('image/'):
        raise ValidationError("Format non autorisé")
    
    # Extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError("Extension non autorisée")
    
    return image
```

### Protection CSRF et XSS
```python
# Dans les templates
{% csrf_token %}  # Protection CSRF automatique

# Échappement automatique des variables
{{ fuite.description|escape }}

# Pour HTML sûr uniquement
{{ safe_html_content|safe }}
```

### Validation OTP Sécurisée
```python
def verify_otp_secure(fuite, provided_otp):
    """Vérification OTP avec protection timing attack"""
    import hmac
    
    # Comparaison constante pour éviter timing attacks
    expected = str(fuite.opt).encode()
    provided = str(provided_otp).encode()
    
    return hmac.compare_digest(expected, provided)
```

---

## 📊 Monitoring et Logging

### Configuration des Logs
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'reports': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### Métriques Importantes
```python
import logging

logger = logging.getLogger('reports')

def track_signalement_metrics(fuite):
    """Tracking des métriques de signalement"""
    logger.info(f"SIGNALEMENT_CREATED fuite_id={fuite.pk} commune={fuite.commune}")
    
def track_otp_verification(fuite, success):
    """Tracking des vérifications OTP"""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"OTP_VERIFICATION fuite_id={fuite.pk} status={status}")
    
def track_mission_creation(mission):
    """Tracking des créations de mission"""
    logger.info(f"MISSION_CREATED mission_id={mission.pk} fuite_id={mission.fuite.pk}")
```

---

*🔧 Cette documentation technique complète le README principal avec tous les détails d'implémentation.*