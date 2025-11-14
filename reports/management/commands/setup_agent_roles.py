"""
Commande Django pour initialiser les rôles des agents et créer des responsables de commune.

Usage:
    python manage.py setup_agent_roles
    
Cette commande:
1. Met à jour les agents existants avec le rôle 'quartier' par défaut
2. Crée des responsables de commune avec le rôle 'commune'
3. Affiche un résumé des modifications
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from reports.models import AgentProfile
from reports.adresse import adresse


class Command(BaseCommand):
    help = 'Initialise les rôles des agents et crée des responsables de commune'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait fait sans modifier la base de données',
        )
        
        parser.add_argument(
            '--create-commune-supervisors',
            action='store_true',
            help='Crée automatiquement des responsables de commune',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        create_supervisors = options['create_commune_supervisors']
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Initialisation du système de rôles pour les agents...\n')
        )

        # 1. Mettre à jour les agents existants
        self.stdout.write('📋 Mise à jour des agents existants...')
        
        existing_agents = AgentProfile.objects.all()
        updated_count = 0
        
        for agent in existing_agents:
            if not hasattr(agent, 'role') or not agent.role:
                if not dry_run:
                    agent.role = 'quartier'  # Par défaut: responsable de quartier
                    agent.save()
                updated_count += 1
                
                self.stdout.write(
                    f'  ✅ {agent.email} → Responsable de Quartier ({agent.commune})'
                )

        # 2. Créer des responsables de commune si demandé
        if create_supervisors:
            self.stdout.write('\n👔 Création des responsables de commune...')
            
            created_supervisors = 0
            
            for commune in adresse.keys():
                supervisor_email = f'responsable.{commune.lower().replace(" ", "")}@regideso.cd'
                
                # Vérifier si un responsable de commune existe déjà
                existing_supervisor = AgentProfile.objects.filter(
                    commune=commune,
                    role='commune'
                ).first()
                
                if not existing_supervisor:
                    if not dry_run:
                        supervisor = AgentProfile.objects.create(
                            email=supervisor_email,
                            phone=f'+243{900000000 + hash(commune) % 100000000}',  # Numéro fictif
                            commune=commune,
                            quartiers_responsable=[],  # Vide car supervise toute la commune
                            role='commune',
                            is_active=True
                        )
                        created_supervisors += 1
                        
                    self.stdout.write(
                        f'  ✅ Créé: {supervisor_email} → Responsable de Commune ({commune})'
                    )
                else:
                    self.stdout.write(
                        f'  ℹ️ Existe déjà: {existing_supervisor.email} → Responsable de Commune ({commune})'
                    )

        # 3. Créer un administrateur système si nécessaire
        admin_email = 'admin@regideso.cd'
        admin_exists = AgentProfile.objects.filter(role='admin').exists()
        
        if not admin_exists:
            self.stdout.write('\n🏛️ Création de l\'administrateur système...')
            
            if not dry_run:
                admin = AgentProfile.objects.create(
                    email=admin_email,
                    phone='+243999999999',
                    commune='Administration',  # Commune fictive pour l'admin
                    quartiers_responsable=[],
                    role='admin',
                    is_active=True
                )
                
            self.stdout.write(f'  ✅ Créé: {admin_email} → Administrateur Système')

        # 4. Résumé
        self.stdout.write('\n📊 RÉSUMÉ:')
        
        total_quartier = AgentProfile.objects.filter(role='quartier').count()
        total_commune = AgentProfile.objects.filter(role='commune').count()
        total_admin = AgentProfile.objects.filter(role='admin').count()
        
        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️ MODE DRY-RUN: Aucune modification appliquée\n'))
        
        self.stdout.write(f'👷‍♂️ Responsables de Quartier: {total_quartier}')
        self.stdout.write(f'👔 Responsables de Commune: {total_commune}')
        self.stdout.write(f'🏛️ Administrateurs: {total_admin}')
        self.stdout.write(f'📈 Total agents: {total_quartier + total_commune + total_admin}')
        
        # 5. Informations de connexion
        if not dry_run and (create_supervisors or not admin_exists):
            self.stdout.write('\n🔐 INFORMATIONS DE CONNEXION:')
            self.stdout.write('Les nouveaux responsables peuvent se connecter avec:')
            self.stdout.write('• Email: leur adresse email')
            self.stdout.write('• Mot de passe: commune+quartier (exemple: gombe+gombe pour Gombe)')
            self.stdout.write('\n💡 Rappel: Les responsables de commune ont uniquement accès en LECTURE SEULE')
            
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Initialisation terminée avec succès!')
        )