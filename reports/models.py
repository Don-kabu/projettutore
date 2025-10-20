from django.db import models
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