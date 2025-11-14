from django.db import models
from django.contrib.auth.models import User
from .adresse import adresse,quartiers
import random



class Fuite(models.Model):
    description = models.TextField()
    photo = models.ImageField(upload_to="fuites/")
    date_signalement = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="NOK")
    phone = models.CharField(max_length=15, null=True, blank=True)
    complaint_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, help_text="Email du signaleur pour les notifications")
    address = models.CharField(max_length=255, null=True, blank=True)
    is_owner = models.BooleanField(null=False,default=False)
    commune  = models.CharField(null=True,choices=zip(adresse,adresse))
    quartier = models.CharField(null=True,choices=zip(quartiers,quartiers))
    opt      = models.CharField(null=True,blank=True)
    verified_opt = models.BooleanField(default=False)

    # Keep the related_name as-is to avoid DB migrations/renames; see alias on Post
    # post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='Fuites')
    def __str__(self):
        
        return f"Fuite du {self.date_signalement.strftime('%d/%m/%Y %H:M')}"
    
    @property
    def generate_otp(self):
        self.opt =f'{self.pk}{random.randint(100,999)}'
        self.save()
        print(self.opt)









class Mission(models.Model):
    description = models.TextField()
    fuite       = models.OneToOneField(Fuite,on_delete=models.DO_NOTHING)
    created_at  = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True)
    status      = models.CharField(null=False,default='NOT RESOLVED')
    remember_count = models.IntegerField(null=False,default=0)
    resolver_phone = models.CharField(verbose_name="phone",max_length=12,default='+243892649177')
    resolver_email = models.EmailField(verbose_name='email',default='kabudon19@gmail.com')
    
    CHOICES_STATUS = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
        ('cancelled', 'Annulé'),
    ]
    
    mission_status = models.CharField(max_length=20, choices=CHOICES_STATUS, default='pending')
    
    def __str__(self):
        return f"Mission #{self.pk} - {self.fuite.commune}/{self.fuite.quartier}"


class AgentProfile(models.Model):
    """
    Profil d'agent basé sur les données d'adresse.py
    Un agent est responsable d'un ou plusieurs quartiers
    """
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    commune = models.CharField(max_length=100, choices=[(k, k) for k in adresse.keys()])
    quartiers_responsable = models.JSONField(default=list, help_text="Liste des quartiers dont l'agent est responsable")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Agent {self.email} - {self.commune}"
    
    def get_missions_assigned(self):
        """Retourne toutes les missions assignées à cet agent"""
        return Mission.objects.filter(
            resolver_email=self.email,
            fuite__commune=self.commune
        ).order_by('-created_at')
    
    def get_missions_pending(self):
        """Retourne les missions en attente"""
        return self.get_missions_assigned().filter(mission_status='pending')
    
    def get_missions_in_progress(self):
        """Retourne les missions en cours"""
        return self.get_missions_assigned().filter(mission_status='in_progress')
    
    def get_missions_resolved(self):
        """Retourne les missions résolues"""
        return self.get_missions_assigned().filter(mission_status='resolved')
    
    @classmethod
    def create_agents_from_adresse(cls):
        """
        Créer automatiquement des agents basés sur les données d'adresse.py
        """
        for commune, quartiers_data in adresse.items():
            if not quartiers_data:  # Skip empty communes like Kisenso
                continue
                
            # Prendre le premier quartier pour obtenir email et téléphone
            first_quartier = list(quartiers_data.keys())[0]
            contact_info = quartiers_data[first_quartier]
            
            email = contact_info.get('email')
            phone = contact_info.get('phone')
            
            if email and phone:
                # Créer ou mettre à jour l'agent
                agent, created = cls.objects.get_or_create(
                    email=email,
                    commune=commune,
                    defaults={
                        'phone': phone,
                        'quartiers_responsable': list(quartiers_data.keys())
                    }
                )
                
                if not created:
                    # Mettre à jour les quartiers responsables
                    agent.quartiers_responsable = list(quartiers_data.keys())
                    agent.phone = phone
                    agent.save()
                    
        return cls.objects.all()