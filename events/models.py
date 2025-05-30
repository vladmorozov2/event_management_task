from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(AbstractUser):
    name = models.CharField(max_length=40, blank=True)
    surname = models.CharField(max_length=60, blank=True)

    USERNAME_FIELD = "username"


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    date = models.DateField()
    event_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    participants = models.ManyToManyField(Participant, through="EventParticipation")


class EventParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    is_organizer = models.BooleanField(default=False)
