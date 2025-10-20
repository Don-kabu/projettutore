from django.shortcuts import render, redirect,get_object_or_404
from.forms import FuiteForm,complaintForm,OptForm
from.models import Fuite,Mission
from .adresse import adresse
from django.db.models.signals import post_save,pre_save,m2m_changed
from django.dispatch import receiver
from.utils import send_confirmation_email,send_mission_notification_email




def accueil(request):
    return render(request, 'accueil.html')







def base(request):
    return render(request , 'base.html')






def signaler1(request):
    if request.method == 'POST':
        form = complaintForm(request.POST)
        
        if form.is_valid():
            fuite = form.save(commit=False)
            fuite.save()
            fuite.generate_otp
            # check phone number
            return redirect("verify_phone_number",fuite.id)
    else:
        form = complaintForm()
            
    return render(request, 'signaler.html', {'form': form})









def verifyotp(request, pk):
    fuite = get_object_or_404(Fuite, pk=pk)
    
    # Récupérer l'OTP depuis l'URL si présent (?otp=123456)
    otp_from_url = request.GET.get('otp')
    
    if not fuite.verified_opt:
        if request.method == 'POST':
            form = OptForm(request.POST)
            
            if form.is_valid():
                otp_from_form = form.data.get("otp")
                if fuite.opt == otp_from_form:
                    fuite.verified_opt = True
                    fuite.save()
                    return redirect("signaler.step2", fuite.pk)
                else:
                    fuite.generate_otp
        
        elif otp_from_url:
            # Vérification automatique si OTP dans l'URL
            if fuite.opt == otp_from_url:
                fuite.verified_opt = True
                fuite.save()
                return redirect("signaler.step2", fuite.pk)
            else:
                # OTP incorrect dans l'URL
                form = OptForm()
                print(fuite.opt, otp_from_url)
                return render(request, 'signaler.html', {
                    'form': form, 
                    'error': 'Code OTP incorrect ou expiré.'
                })
        else:
            form = OptForm()
                
        return render(request, 'signaler.html', {'form': form})
    return redirect('accueil')
















def signaler2(request,pk):
    fuite = get_object_or_404(Fuite,pk=pk)
    if fuite.verified_opt and not fuite.status=="OK":
        if request.method == 'POST':
            form = FuiteForm(request.POST,request.FILES,instance=fuite)
            
            if form.is_valid():
                fuite = form.save(commit=False)
                fuite.status = "OK"
                fuite.save()
                # check phone number
                return render(request,"base.html")
        else:
            form = FuiteForm()
            # Sécuriser l'accès à adresse
            if fuite.commune and fuite.commune in adresse:
                quartiers_list = adresse[fuite.commune]
                form.fields["quartier"].choices = zip(quartiers_list, quartiers_list)
                
        return render(request, 'signaler.html', {'form': form})
    return redirect("accueil")











@receiver(post_save, sender=Fuite)
def affecter_travail(sender, instance, created, **kwargs):
    """
    Fonction appelée après la sauvegarde d'une Fuite
    
    Args:
        sender: La classe Fuite
        instance: L'objet Fuite qui vient d'être sauvegardé (c'est votre objet modifié!)
        created: True si l'objet vient d'être créé, False s'il a été mis à jour
    """
    fuite = instance    

    if fuite.status == "OK":
        try:
            mission = Mission.objects.create(
                description=f"""
                    Panne au quartier {fuite.quartier}, dans la commune de {fuite.commune}
                    Adresse complète: {fuite.address}
                    Signalé le: {fuite.date_signalement}
                """,
                fuite=fuite,
                resolver_phone=adresse.get(fuite.commune, {}).get(fuite.quartier, {}).get('phone', '+243892649177'),
                resolver_email=adresse.get(fuite.commune, {}).get(fuite.quartier, {}).get('email', 'kabudon19@gmail.com')
            )
            mission.save()
        except Exception as e:
            print(e)
            # print(f"Erreur lors de la création de la mission: {e}")

    else:
        send_confirmation_email(fuite)








@receiver(post_save, sender=Mission)
def send_notification(sender, instance, created, **kwargs):
    """
    Fonction appelée après la sauvegarde d'une Mission
    
    Args:
        sender: La classe Mission
        instance: L'objet Mission qui vient d'être sauvegardé
        created: True si l'objet vient d'être créé
    """
    mission = instance  # L'objet Mission modifié
    
    if created:
        send_mission_notification_email(mission)