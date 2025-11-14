"""
URL configuration for Signalement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('base/', views.base, name='base'),
    path('signaler/', views.signaler1, name='signaler.step1'),
    path('signaler/<int:pk>', views.signaler2, name='signaler.step2'),
    path('signaler/<int:pk>/otp', views.verifyotp, name='verify_otp'),
    path('suivi/<str:otp_code>/', views.suivi_signalement, name='suivi_signalement'),
    path('recherche/', views.recherche_signalement, name='recherche_signalement'),
    path('test-css/', views.test_css, name='test_css'),
    
    # URLs Agent
    path('agent/', views.agent_login, name='agent_login'),
    path('agent/test/', views.agent_test, name='agent_test'),
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent/logout/', views.agent_logout, name='agent_logout'),
    path('agent/missions/', views.agent_missions_list, name='agent_missions_list'),
    path('agent/mission/<int:mission_id>/', views.agent_mission_detail, name='agent_mission_detail'),
    path('agent/init/', views.init_agents, name='init_agents'),
    path('agent/clean/', views.clean_agents, name='clean_agents'),
]
