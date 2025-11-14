from django.shortcuts import render, redirect,get_object_or_404
from.forms import FuiteForm,complaintForm,OptForm
from.models import Fuite,Mission,AgentProfile
from .adresse import adresse
from django.db.models.signals import post_save,pre_save,m2m_changed
from django.dispatch import receiver
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from.utils import send_confirmation_email,send_mission_notification_email,send_otp_email,send_status_update_email




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
            return redirect("verify_otp",fuite.id)
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
                return render(request, 'signaler.html', {
                    'form': form, 
                    'error': 'Code OTP incorrect ou expiré.'
                })
        else:
            form = OptForm()
                
        return render(request, 'signaler.html', {'form': form})
    return redirect("signaler.step2", fuite.pk)
















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
    if not created and fuite.status == "OK":
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












def suivi_signalement(request, otp_code):
    """
    Vue pour suivre l'état d'un signalement via son code OTP
    Permet de voir l'état actuel et faire des rappels
    """
    try:
        # Rechercher le signalement par code OTP
        fuite = get_object_or_404(Fuite, opt=otp_code)
        
        # Récupérer la mission associée si elle existe
        mission = None
        try:
            mission = Mission.objects.get(fuite=fuite)
        except Mission.DoesNotExist:
            pass
        
        # Déterminer l'état actuel
        if fuite.status == "OK" and mission:
            # Pour l'instant, on considère qu'une mission existante = en cours
            # (vous pourrez ajouter un champ statut à Mission plus tard)
            status = "in_progress"
            status_label = "En cours"
            status_color = "info"
            status_icon = "🔄"
        elif fuite.verified_opt:
            status = "verified"
            status_label = "Vérifié"
            status_color = "warning"
            status_icon = "✅"
        else:
            status = "pending"
            status_label = "En attente"
            status_color = "secondary"
            status_icon = "⏳"
        
        # Traitement du formulaire de rappel
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'rappel':
                # Envoyer un rappel selon l'état
                rappel_sent = False
                
                if status == "pending":
                    # Rappel pour vérification
                    send_otp_email(fuite.email, fuite.opt, fuite.pk)
                    messages.success(request, "📧 Code de vérification renvoyé par email !")
                    rappel_sent = True
                    
                elif status == "verified":
                    # Rappel pour planification mission
                    send_status_update_email(fuite, "verified", 
                        "Rappel : Votre signalement est vérifié et sera traité prochainement.")
                    messages.success(request, "📧 Rappel envoyé ! Nous examinerons votre demande.")
                    rappel_sent = True
                    
                elif status == "in_progress" and mission:
                    # Rappel pour mission en cours
                    send_status_update_email(fuite, "in_progress", 
                        "Rappel : L'intervention est en cours. Nos équipes travaillent sur votre signalement.")
                    messages.success(request, "📧 Rappel envoyé à l'équipe d'intervention !")
                    rappel_sent = True
                
                if rappel_sent and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Rappel envoyé avec succès !'})
        
        context = {
            'fuite': fuite,
            'mission': mission,
            'status': status,
            'status_label': status_label,
            'status_color': status_color,
            'status_icon': status_icon,
            'otp_code': otp_code
        }
        
        return render(request, 'suivi_signalement.html', context)
        
    except Fuite.DoesNotExist:
        messages.error(request, "❌ Code de suivi invalide. Vérifiez votre code OTP.")
        return redirect('accueil')













def recherche_signalement(request):
    """
    Vue pour rechercher un signalement par code OTP
    """
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        if otp_code:
            return redirect('suivi_signalement', otp_code=otp_code)
        else:
            messages.error(request, "❌ Veuillez saisir un code OTP valide.")
    
    return render(request, 'recherche_signalement.html')


# ===== VUES D'AGENT =====















def agent_login(request):
    """
    Vue de connexion pour les agents
    Utilise l'email et un mot de passe au format commune-quartier
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.error(request, "❌ Veuillez saisir votre email et mot de passe.")
            return render(request, 'agent/login.html')
        
        # Vérifier le format du mot de passe (commune-quartier)
        if '-' not in password:
            messages.error(request, "❌ Format du mot de passe incorrect. Utilisez: commune-quartier")
            return render(request, 'agent/login.html')
            
        # Extraire commune et quartier du mot de passe
        parts = password.split('-', 1)  # Séparer seulement sur le premier tiret
        if len(parts) != 2:
            messages.error(request, "❌ Format du mot de passe incorrect. Utilisez: commune-quartier")
            return render(request, 'agent/login.html')
            
        commune = parts[0].strip().title()  # Capitaliser la première lettre
        quartier = parts[1].strip().title()  # Capitaliser la première lettre
        
        try:
            print(f"Tentative de connexion avec: {email}, {commune}, {quartier}")
            
            # Trouver l'agent par email et commune d'abord
            agents = AgentProfile.objects.filter(
                email=email,
                commune=commune,
                is_active=True
            )
            
            if not agents.exists():
                messages.error(request, "❌ Agent non trouvé pour cette commune.")
                return render(request, 'agent/login.html')
            
            # Vérifier si le quartier est dans la liste des quartiers responsables
            agent = None
            for a in agents:
                if quartier in a.quartiers_responsable:
                    agent = a
                    break
            
            if not agent:
                messages.error(request, "❌ Vous n'êtes pas responsable de ce quartier.")
                return render(request, 'agent/login.html')
            
            # Si on arrive ici, c'est que l'agent existe et que le mot de passe commune-quartier est valide
            # Connexion réussie
            agent.last_login = timezone.now()
            agent.save()
            
            # Stocker l'agent en session
            request.session['agent_id'] = agent.pk
            request.session['agent_email'] = agent.email
            request.session['agent_commune'] = agent.commune
            
            messages.success(request, f"🎉 Bienvenue agent de {agent.commune} !")
            return redirect('agent_dashboard')
            
        except Exception as e:
            messages.error(request, f"❌ Erreur de connexion: {str(e)}")
            print(f"Erreur lors de la connexion agent: {e}")
    
    return render(request, 'agent/login.html')













def agent_logout(request):
    """
    Déconnexion de l'agent
    """
    agent_email = request.session.get('agent_email', 'Agent')
    
    # Nettoyer la session
    for key in ['agent_id', 'agent_email', 'agent_commune']:
        if key in request.session:
            del request.session[key]
    
    messages.success(request, f"👋 Au revoir {agent_email} !")
    return redirect('agent_login')
















def agent_required(view_func):
    """
    Décorateur pour vérifier qu'un agent est connecté
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get('agent_id'):
            messages.error(request, "🔒 Vous devez être connecté pour accéder à cette page.")
            return redirect('agent_login')
        return view_func(request, *args, **kwargs)
    return wrapper
















@agent_required
def agent_dashboard(request):
    """
    Dashboard principal de l'agent avec permissions basées sur le rôle
    """
    try:
        agent = AgentProfile.objects.get(id=request.session['agent_id'])
        
        # Statistiques selon le rôle
        if agent.role == 'quartier':
            # Statistiques spécifiques aux quartiers de l'agent
            stats = agent.get_quarterly_stats()
            context = {
                'agent': agent,
                'stats': stats,
                'can_modify': True,  # Responsable de quartier peut modifier
                'view_type': 'quartier',
                'recent_missions': agent.get_missions_assigned()[:5],
            }
        
        elif agent.role == 'commune':
            # Vue d'ensemble de la commune (lecture seule)
            stats = agent.get_commune_stats()
            context = {
                'agent': agent,
                'stats': stats,
                'can_modify': False,  # Responsable de commune : lecture seule
                'view_type': 'commune',
                'recent_missions': agent.get_missions_assigned()[:10],
            }
        
        elif agent.role == 'admin':
            # Vue administrateur complète
            all_missions = Mission.objects.all()
            context = {
                'agent': agent,
                'stats': {
                    'total': all_missions.count(),
                    'pending': all_missions.filter(mission_status='pending').count(),
                    'in_progress': all_missions.filter(mission_status='in_progress').count(),
                    'resolved': all_missions.filter(mission_status='resolved').count(),
                },
                'can_modify': True,  # Admin peut tout modifier
                'view_type': 'admin',
                'recent_missions': all_missions.order_by('-created_at')[:10],
            }
        
        else:
            messages.error(request, "❌ Rôle non reconnu.")
            return redirect('agent_login')
        
        return render(request, 'agent/dashboard.html', context)
        
    except AgentProfile.DoesNotExist:
        messages.error(request, "❌ Profil agent non trouvé.")
        return redirect('agent_login')
















@agent_required
def agent_missions_list(request):
    """
    Liste complète des missions de l'agent
    """
    try:
        agent = AgentProfile.objects.get(id=request.session['agent_id'])
        
        # Filtrage par statut
        status_filter = request.GET.get('status', 'all')
        
        if status_filter == 'pending':
            missions = agent.get_missions_pending()
        elif status_filter == 'in_progress':
            missions = agent.get_missions_in_progress()
        elif status_filter == 'resolved':
            missions = agent.get_missions_resolved()
        else:
            missions = agent.get_missions_assigned()
        
        context = {
            'agent': agent,
            'missions': missions,
            'status_filter': status_filter,
        }
        
        return render(request, 'agent/missions_list.html', context)
        
    except AgentProfile.DoesNotExist:
        messages.error(request, "❌ Profil agent non trouvé.")
        return redirect('agent_login')
















@agent_required
def agent_mission_detail(request, mission_id):
    """
    Détail et mise à jour d'une mission avec permissions basées sur le rôle
    """
    try:
        agent = AgentProfile.objects.get(id=request.session['agent_id'])
        mission = get_object_or_404(Mission, pk=mission_id)
        
        # Vérifier les permissions de visualisation
        if not agent.can_view_mission(mission):
            messages.error(request, "❌ Vous n'avez pas l'autorisation de voir cette mission.")
            return redirect('agent_dashboard')
        
        # Vérifier les permissions de modification
        can_modify = agent.can_modify_mission(mission)
        
        if request.method == 'POST':
            if not can_modify:
                messages.error(request, "❌ Vous n'avez pas l'autorisation de modifier cette mission (mode lecture seule).")
                return redirect('agent_mission_detail', mission_id=mission_id)
            
            action = request.POST.get('action')
            
            if action == 'start':
                mission.mission_status = 'in_progress'
                mission.save()
                send_status_update_email(mission.fuite, 'in_progress', 
                    f"L'équipe de {agent.commune} a commencé l'intervention.")
                messages.success(request, "✅ Mission marquée comme en cours !")
                
            elif action == 'resolve':
                mission.mission_status = 'resolved'
                mission.resolved_at = timezone.now()
                mission.save()
                send_status_update_email(mission.fuite, 'resolved', 
                    f"Problème résolu par l'équipe de {agent.commune}. Merci pour votre signalement !")
                messages.success(request, "🎉 Mission marquée comme résolue !")
                
            elif action == 'cancel':
                mission.mission_status = 'cancelled'
                mission.save()
                send_status_update_email(mission.fuite, 'cancelled', 
                    f"Mission annulée par l'équipe de {agent.commune}.")
                messages.success(request, "❌ Mission annulée.")
                
            elif action == 'comment':
                comment = request.POST.get('comment', '').strip()
                if comment:
                    send_status_update_email(mission.fuite, 'comment', 
                        f"Commentaire de l'équipe {agent.commune}: {comment}")
                    messages.info(request, "📝 Commentaire envoyé !")
                
            return redirect('agent_mission_detail', mission_id=mission.pk)
        
        context = {
            'agent': agent,
            'mission': mission,
            'fuite': mission.fuite,
            'can_modify': can_modify,
            'role_display': agent.get_role_display(),
            'is_readonly': not can_modify,
        }
        
        return render(request, 'agent/mission_detail.html', context)
        
    except AgentProfile.DoesNotExist:
        messages.error(request, "❌ Profil agent non trouvé.")
        return redirect('agent_login')
















def test_css(request):
    """
    Vue de test pour vérifier les styles CSS des formulaires
    """
    return render(request, 'test_css.html')


def agent_test(request):
    """
    Vue de test pour l'interface agent
    """
    return render(request, 'agent/test.html')


def clean_agents(request):
    """
    Vue utilitaire pour nettoyer les doublons d'agents
    """
    from .models import AgentProfile
    
    try:
        # Supprimer tous les agents existants
        count_deleted = AgentProfile.objects.all().count()
        AgentProfile.objects.all().delete()
        
        messages.success(request, f"🗑️ {count_deleted} agents supprimés avec succès !")
        return redirect('init_agents')
        
    except Exception as e:
        messages.error(request, f"❌ Erreur lors du nettoyage: {str(e)}")
        return redirect('accueil')















def init_agents(request):
    """
    Vue utilitaire pour initialiser les agents depuis adresse.py
    À utiliser une seule fois pour créer tous les agents
    """
    from .models import AgentProfile
    
    try:
        # Nettoyer d'abord les doublons potentiels
        AgentProfile.objects.all().delete()
        
        agents = AgentProfile.create_agents_from_adresse()
        
        count = agents.count()
        messages.success(request, f"✅ {count} agents créés/mis à jour avec succès !")
        
        # Lister les agents créés
        agent_list = []
        for agent in agents:
            agent_list.append(f"• {agent.commune}: {agent.email}")
        
        context = {
            'agents': agents,
            'agent_list': agent_list,
            'count': count
        }
        
        return render(request, 'agent/init_success.html', context)
        
    except Exception as e:
        messages.error(request, f"❌ Erreur lors de la création des agents: {str(e)}")
        return redirect('accueil')