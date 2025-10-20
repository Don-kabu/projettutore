from django.core.mail import send_mail
from Signalement.settings import DEFAULT_FROM_EMAIL




def send_confirmation_email(fuite):
    """
    Envoie un email de confirmation au signaleur de la fuite.
    
    Args:
        fuite (Fuite): L'objet Fuite pour lequel envoyer la confirmation.
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    # Logique d'envoi d'email ici
    # Par exemple, utiliser Django's send_mail function
    subject = "Confirmation de votre signalement de fuite"
    
    # Générer le lien avec OTP automatique
    verification_link = f"http://127.0.0.1:8000/signaler/{fuite.pk}/otp?otp={fuite.opt}"
    
    message = f"""
        Merci d'avoir signalé la fuite. Votre référence est {fuite.opt}. 
        
        Pour compléter votre signalement, cliquez sur ce lien :
        {verification_link}
    """
    recipient_list = [fuite.email]
    
    try:
        send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list)
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False
    





def send_mission_notification_email(mission):
    """
    Envoie un email de notification au résolveur de la mission.
    
    Args:
        mission (Mission): L'objet Mission pour lequel envoyer la notification.
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon.
    """
    subject = "Nouvelle mission de réparation de fuite assignée"
    message = f"""
        Une nouvelle mission a été créée pour réparer une fuite.
        
        Détails de la mission:
        Description: {mission.description}
        Fuite ID: {mission.fuite.id}
        Adresse: {mission.fuite.address}
        Date du signalement: {mission.fuite.date_signalement}
        
        Veuillez prendre les mesures nécessaires pour résoudre cette fuite.
    """
    recipient_list = [mission.resolver_email]
    
    try:
        send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list)
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de notification: {e}")
        return False