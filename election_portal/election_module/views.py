from django.shortcuts import render, redirect
from .models import Candidate, Voter, Preferences
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.postgres.search import *
from django.core.exceptions import *

# Create your views here.

def home(request):
    return render(request, 'home.html')

def CallRegisterAsCandidate(request):
    return render(request, 'RegisterAsCandidate.html')

def RegisterAsCandidate(request):
    preference=Preferences.objects.get(id=1)
    if preference.Allow_Registrations==False :
        return render(request,'RegisterAsCandidate.html',{"message":"Registration Closed"})
    username=request.POST['username']
    password1=request.POST['password1']
    password2=request.POST['password2']

    if(password1==password2):
            if User.objects.filter(username=username).exists():
                return render(request,'RegisterAsCandidate.html',{"message":"Username already exists"})
            else:
                user=User.objects.create_user(username=username, password=password1, first_name=request.POST['CandidateName'])
                user.save()

                newcandidate=Candidate()
                newcandidate.username=username
                newcandidate.CandidateName=request.POST['CandidateName']
                newcandidate.party=request.POST['party']
                newcandidate.constituency=request.POST['constituency']
                newcandidate.symbol=request.FILES['symbol']
                newcandidate.save()

                return render(request,'RegisterAsCandidate.html',{"message":"Registration Complete"})
    else:
            return render(request,'RegisterAsCandidate.html',{"message":"Passwords Do Not Match"})

def CallRegisterAsVoter(request):
    return render(request, 'RegisterAsVoter.html')

def RegisterAsVoter(request):
    preference=Preferences.objects.get(id=1)
    if preference.Allow_Registrations==False :
        return render(request,'RegisterAsVoter.html',{"message":"Registration Closed"})

    username=request.POST['username']
    password1=request.POST['password1']
    password2=request.POST['password2']

    if(password1==password2):
            if User.objects.filter(username=username).exists():
                return render(request,'RegisterAsVoter.html',{"message":"Username already exists"})
            else:
                user=User.objects.create_user(username=username, password=password1, first_name=request.POST['VoterName'])
                user.save()

                newvoter=Voter()
                newvoter.username=username
                newvoter.VoterName=request.POST['VoterName']
                newvoter.constituency=request.POST['constituency']
                newvoter.save()
                
                return render(request,'RegisterAsVoter.html',{"message":"Registration Complete"})
    else:
            return render(request,'RegisterAsVoter.html',{"message":"Passwords Do Not Match"})

def CallLoginAsCandidate(request):
    return render(request, 'LoginAsCandidate.html')

def LoginAsCandidate(request):
    username=request.POST['username']
    password=request.POST['password']

    user=auth.authenticate(username=username,password=password)

    if user is not None:
        userdata=Candidate.objects.get(username=username)
        auth.login(request,user)
        return render(request,'CandidateHome.html',{"userdata":userdata})

    else:
        return render(request,'LoginAsCandidate.html',{"message":"invalid username or password"})

def CallLoginAsVoter(request):
    return render(request, 'LoginAsVoter.html')

def LoginAsVoter(request):
    username=request.POST['username']
    password=request.POST['password']

    user=auth.authenticate(username=username,password=password)

    if user is not None:
        userdata=Voter.objects.get(username=username)
        auth.login(request,user)
        return render(request,'VoterHome.html',{"userdata":userdata})
    else:
        return render(request,'LoginAsVoter.html',{"message":"invalid username or password"})

def Logout(request):
    auth.logout(request)
    return redirect('/')

def CallVotePage(request):
    preference=Preferences.objects.get(id=1)
    try :
        voter=Voter.objects.get(username=request.GET['username'])
    except:
        voter=None

    if voter is None :
        voter=Candidate.objects.get(username=request.GET['username'])
        if preference.Allow_Voting == False :
            return render(request,'CandidateHome.html',{"userdata":voter, "message":"Voting closed"})

    if preference.Allow_Voting == False :
            return render(request,'VoterHome.html',{"userdata":voter, "message":"Voting closed"})

    candidates_list=Candidate.objects.filter(constituency=voter.constituency)
    return render(request, 'Vote.html', {"username":request.GET['username'], "candidates_list":candidates_list})

def VoteCasted(request):
    preference=Preferences.objects.get(id=1)
    gotvoted=Candidate.objects.get(username=request.POST['VotedFor'])
    try :
        voter=Voter.objects.get(username=request.POST['Voter_username'])
    except :
        voter=None

    if voter is None:
        voter=Candidate.objects.get(username=request.POST['Voter_username'])

    if voter.HasAlreadyVoted==True :
        candidates_list=Candidate.objects.filter(constituency=voter.constituency)
        return render(request, 'Vote.html', {"username":request.POST['Voter_username'], "candidates_list":candidates_list, "message":"Already Voted"})
    
    else :
        candidates_list=Candidate.objects.filter(constituency=voter.constituency)
        if preference.Allow_Voting == False :
             return render(request, 'Vote.html', {"username":request.POST['Voter_username'], "candidates_list":candidates_list, "message":"Vote Registered"})
        gotvoted.NumberOfVotes+=1
        gotvoted.save()
        if gotvoted is voter:
            voter.NumberOfVotes+=1
        voter.VotedFor=gotvoted.CandidateName + " " + gotvoted.party
        voter.HasAlreadyVoted=True
        voter.save()
        return render(request, 'Vote.html', {"username":request.POST['Voter_username'], "candidates_list":candidates_list, "message":"Vote Registered"})