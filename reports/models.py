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
    ROLE_CHOICES = [
        ('quartier', 'Responsable de Quartier'),
        ('commune', 'Responsable de Commune'),
        ('admin', 'Administrateur'),
    ]
    
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    commune = models.CharField(max_length=100, choices=[(k, k) for k in adresse.keys()])
    quartiers_responsable = models.JSONField(default=list, help_text="Liste des quartiers dont l'agent est responsable")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='quartier', help_text="Rôle et niveau de permissions")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Profil Agent"
        verbose_name_plural = "Profils Agents"
        ordering = ['commune', 'role', 'email']
    
    def __str__(self):
        role_display = self.get_role_display()
        return f"{role_display} - {self.email} ({self.commune})"
    
    def can_modify_mission(self, mission):
        """
        Vérifie si l'agent peut modifier une mission
        - Responsable de quartier : peut modifier les missions de ses quartiers
        - Responsable de commune : LECTURE SEULE (ne peut pas modifier)
        - Admin : peut tout modifier
        """
        if self.role == 'admin':
            return True
        elif self.role == 'quartier':
            # Peut modifier si la mission concerne un de ses quartiers
            return (mission.fuite.commune == self.commune and 
                   mission.fuite.quartier in self.quartiers_responsable)
        elif self.role == 'commune':
            # Responsable de commune : LECTURE SEULE uniquement
            return False
        return False
    
    def can_view_mission(self, mission):
        """
        Vérifie si l'agent peut voir une mission
        - Responsable de quartier : voit ses quartiers
        - Responsable de commune : voit toute sa commune
        - Admin : voit tout
        """
        if self.role == 'admin':
            return True
        elif self.role in ['quartier', 'commune']:
            return mission.fuite.commune == self.commune
        return False
    
    def get_missions_assigned(self):
        """Retourne toutes les missions visibles pour cet agent"""
        if self.role == 'admin':
            return Mission.objects.all().order_by('-created_at')
        elif self.role == 'commune':
            # Responsable de commune voit toute sa commune
            return Mission.objects.filter(
                fuite__commune=self.commune
            ).order_by('-created_at')
        elif self.role == 'quartier':
            # Responsable de quartier voit seulement ses quartiers
            return Mission.objects.filter(
                fuite__commune=self.commune,
                fuite__quartier__in=self.quartiers_responsable
            ).order_by('-created_at')
        return Mission.objects.none()
    
    def get_missions_pending(self):
        """Retourne les missions en attente visibles"""
        return self.get_missions_assigned().filter(mission_status='pending')
    
    def get_missions_in_progress(self):
        """Retourne les missions en cours visibles"""
        return self.get_missions_assigned().filter(mission_status='in_progress')
    
    def get_missions_resolved(self):
        """Retourne les missions résolues visibles"""
        return self.get_missions_assigned().filter(mission_status='resolved')
    
    def get_quarterly_stats(self):
        """Statistiques pour les responsables de quartier"""
        if self.role == 'quartier':
            missions = self.get_missions_assigned()
            return {
                'total': missions.count(),
                'pending': missions.filter(mission_status='pending').count(),
                'in_progress': missions.filter(mission_status='in_progress').count(),
                'resolved': missions.filter(mission_status='resolved').count(),
                'quartiers': self.quartiers_responsable
            }
        return None
    
    def get_commune_stats(self):
        """Statistiques pour les responsables de commune (lecture seule)"""
        if self.role in ['commune', 'admin']:
            missions = Mission.objects.filter(fuite__commune=self.commune)
            quartiers_stats = {}
            
            for quartier in adresse.get(self.commune, []):
                quartier_missions = missions.filter(fuite__quartier=quartier)
                quartiers_stats[quartier] = {
                    'total': quartier_missions.count(),
                    'pending': quartier_missions.filter(mission_status='pending').count(),
                    'in_progress': quartier_missions.filter(mission_status='in_progress').count(),
                    'resolved': quartier_missions.filter(mission_status='resolved').count(),
                }
            
            return {
                'total': missions.count(),
                'pending': missions.filter(mission_status='pending').count(),
                'in_progress': missions.filter(mission_status='in_progress').count(),
                'resolved': missions.filter(mission_status='resolved').count(),
                'quartiers': quartiers_stats
            }
        return None
    
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