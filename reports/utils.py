from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Signalement.settings import DEFAULT_FROM_EMAIL
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fuite, Mission
import random
import string




def send_confirmation_email(fuite):
    """
    Envoie un email de confirmation HTML au signaleur de la fuite.
    
    Args:
        fuite (Fuite): L'objet Fuite pour lequel envoyer la confirmation.
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    try:
        subject = "✅ Confirmation de votre signalement de fuite - Regideso"
        
        # Contexte pour le template
        context = {
            'fuite': fuite,
        }
        
        # Rendu du template HTML
        html_content = render_to_string('email/confirmation.html', context)
        text_content = strip_tags(html_content)
        
        # Création de l'email avec version HTML et texte
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=DEFAULT_FROM_EMAIL,
            to=[fuite.email]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Envoi de l'email
        email.send()
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de confirmation: {e}")
        return False
    















def send_mission_notification_email(mission):
    """
    Envoie un email de notification HTML pour une nouvelle mission.
    
    Args:
        mission (Mission): L'objet Mission pour lequel envoyer la notification.
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    try:
        subject = "🔧 Nouvelle mission d'intervention - Regideso"
        
        # Contexte pour le template
        context = {
            'mission': mission,
            'fuite': mission.fuite,
        }
        
        # Rendu du template HTML
        html_content = render_to_string('email/mission_notification.html', context)
        text_content = strip_tags(html_content)
        
        # Envoi au signaleur (si email fourni)
        emails_sent = 0
        if mission.fuite.email:
            email_signaleur = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=DEFAULT_FROM_EMAIL,
                to=[mission.fuite.email]
            )
            email_signaleur.attach_alternative(html_content, "text/html")
            email_signaleur.send()
            emails_sent += 1
        
        # Envoi au responsable de la mission (si email fourni)
        if mission.resolver_email:
            subject_resolver = "🛠️ Mission assignée - Intervention fuite d'eau"
            email_resolver = EmailMultiAlternatives(
                subject=subject_resolver,
                body=text_content,
                from_email=DEFAULT_FROM_EMAIL,
                to=[mission.resolver_email]
            )
            email_resolver.attach_alternative(html_content, "text/html")
            email_resolver.send()
            emails_sent += 1
            
        return emails_sent > 0
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de notification de mission: {e}")
        return False










@receiver(post_save, sender=Fuite)  
def send_otp_email(sender, instance, created, **kwargs):
    """
    Envoie un email avec le code OTP de vérification.
    
    Args:
        email (str): Email du destinataire
        otp_code (str): Code OTP à envoyer
        fuite_id (int): ID de la fuite pour le lien
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    try:
        subject = "🔐 Code de vérification - Regideso"
        
        # Contexte pour le template
        context = {
            'otp_code': instance.opt,
            'fuite_id': instance.id,
        }
        
        # Rendu du template HTML
        html_content = render_to_string('email/otp_verification.html', context)
        text_content = strip_tags(html_content)
        
        # Création de l'email
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=DEFAULT_FROM_EMAIL,
            to=[instance.email]
        )
        email_message.attach_alternative(html_content, "text/html")
        
        # Envoi de l'email
        email_message.send()
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email OTP: {e}")
        return False











def send_status_update_email(fuite, status, message=None):
    """
    Envoie un email de mise à jour du statut d'un signalement.
    
    Args:
        fuite (Fuite): L'objet Fuite concerné
        status (str): Nouveau statut
        message (str, optional): Message personnalisé
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    try:
        subject = f"Mise à jour signalement #{fuite.id:05d} - Regideso"
        
        # Contexte pour le template
        context = {
            'fuite': fuite,
            'status': status,
            'message': message,
        }
        
        # Rendu du template HTML
        html_content = render_to_string('email/status_update.html', context)
        text_content = strip_tags(html_content)
        
        # Création de l'email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=DEFAULT_FROM_EMAIL,
            to=[fuite.email]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Envoi de l'email
        email.send()
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de mise à jour: {e}")
        return False























def send_welcome_email(email, name=None):
    """
    Envoie un email de bienvenue à un nouvel utilisateur.
    
    Args:
        email (str): Email du destinataire
        name (str, optional): Nom du destinataire
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    try:
        subject = "🎉 Bienvenue chez Regideso - Votre plateforme de signalement"
        
        # Contexte pour le template
        context = {
            'name': name or 'Citoyen',
        }
        
        # Rendu du template HTML
        html_content = render_to_string('email/welcome.html', context)
        text_content = strip_tags(html_content)
        
        # Création de l'email
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=DEFAULT_FROM_EMAIL,
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        
        # Envoi de l'email
        email_message.send()
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de bienvenue: {e}")
        return False