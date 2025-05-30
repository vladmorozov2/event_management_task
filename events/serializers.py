from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Event, Participant, EventParticipation


class ParticipantSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = Participant
        fields = ("id", "email", "username", "password", "name", "surname")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = Participant(
            email=validated_data.get("email"),
            username=validated_data.get("username"),
            name=validated_data.get("name", ""),
            surname=validated_data.get("surname", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class EventSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "event_type",
            "location",
            "participants",
        ]


class EventParticipationSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)

    class Meta:
        model = EventParticipation
        fields = ["id", "event", "participant", "is_organizer"]
        read_only_fields = ["id", "event", "participant"]
