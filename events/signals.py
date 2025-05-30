# events/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import EventParticipation


@receiver(post_save, sender=EventParticipation)
def send_event_registration_email(sender, instance, created, **kwargs):
    if created:
        participant = instance.participant
        event = instance.event
        if participant.email:
            print(
                f"Sending registration email to {participant.email} for event {event.title}"
            )
            send_mail(
                subject=f"Registration Confirmed: {event.title}",
                message=f"Hello {participant.username},\n\nYou have successfully registered for '{event.title}' happening on {event.date} at {event.location}.",
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[participant.email],
                fail_silently=False,
            )
