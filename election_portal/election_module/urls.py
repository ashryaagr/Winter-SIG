from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('CallRegisterAsCandidate', views.CallRegisterAsCandidate, name='CallRegisterAsCandidate'),
    path('CallRegisterAsVoter', views.CallRegisterAsVoter, name='CallRegisterAsVoter'),
    path('CallLoginAsCandidate', views.CallLoginAsCandidate, name='CallLoginAsCandidate'),
    path('CallLoginAsVoter', views.CallLoginAsVoter, name='CallLoginAsVoter'),
    path('RegisterAsCandidate', views.RegisterAsCandidate, name='RegisterAsCandidate'),
    path('RegisterAsVoter', views.RegisterAsVoter, name='RegisterAsVoter'),
    path('LoginAsCandidate', views.LoginAsCandidate, name='LoginAsCandidate'),
    path('LoginAsVoter', views.LoginAsVoter, name='LoginAsVoter'),
    path('CallVotePage', views.CallVotePage, name='CallVotePage'),
    path('VoteCasted', views.VoteCasted, name='VoteCasted'),
    path('Logout',views.Logout,name='Logout'),
]