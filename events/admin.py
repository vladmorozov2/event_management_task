from django.contrib import admin
from .models import Event, Participant, EventParticipation


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "surname")
    search_fields = ("email", "name", "surname")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "event_type", "location")
    search_fields = ("title", "event_type", "location")
    list_filter = ("event_type", "date")


@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "participant", "is_organizer")
    list_filter = ("is_organizer",)
    autocomplete_fields = ("event", "participant")
