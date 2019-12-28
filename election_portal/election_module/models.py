from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Candidate(models.Model):
    username=models.CharField(max_length=100)
    CandidateName=models.CharField(max_length=100)
    party=models.CharField(max_length=100, default='Independent')
    constituency=models.CharField(max_length=100)
    symbol=models.ImageField(upload_to='images/')
    VotedFor=models.CharField(max_length=100, default='Not Voted Yet')
    HasAlreadyVoted=models.BooleanField(default=False,)
    NumberOfVotes=models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Voter(models.Model):
    username=models.CharField(max_length=100)
    VoterName=models.CharField(max_length=100)
    constituency=models.CharField(max_length=100)
    VotedFor=models.CharField(max_length=100, default='Not Voted Yet')
    HasAlreadyVoted=models.BooleanField(default=False)

    def __str__(self):
        return self.username

def validate_only_one_instance(obj):
    model=obj.__class__
    if (model.objects.count()>0 and obj.id != model.objects.get().id):
        raise ValidationError("Can create only one instance of Preferences")

class Preferences(models.Model):
    Allow_Registrations=models.BooleanField(default=True)
    Allow_Voting=models.BooleanField(default=False)

    def clean(self):
        validate_only_one_instance(self)
