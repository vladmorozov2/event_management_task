from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    ParticipantSerializer,
    EventSerializer,
    EventParticipationSerializer,
)
from .models import Event, Participant, EventParticipation
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date


class EventListCreateView(APIView):
    """Handles listing and creating events."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "title",
                openapi.IN_QUERY,
                description="Filter by event title",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Filter by event date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "location",
                openapi.IN_QUERY,
                description="Filter by event location",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "event_type",
                openapi.IN_QUERY,
                description="Filter by event type",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: EventSerializer(many=True)},
    )
    def get(self, request):
        events = Event.objects.all()
        title = request.GET.get("title")
        date = request.GET.get("date")
        location = request.GET.get("location")
        event_type = request.GET.get("event_type")

        if title:
            events = events.filter(title__icontains=title)
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                events = events.filter(date=parsed_date)
        if location:
            events = events.filter(location__icontains=location)
        if event_type:
            events = events.filter(event_type__icontains=event_type)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EventSerializer, responses={201: EventSerializer})
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    """Handles retrieve, update, delete of a single event."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: EventSerializer, 404: "Not found"})
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EventSerializer,
        responses={200: EventSerializer, 400: "Bad request"},
    )
    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: "Deleted", 404: "Not found"})
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response(status=204)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)


class UserListCreateView(APIView):
    """Handles listing and creating participants."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ParticipantSerializer(many=True)})
    def get(self, request):
        users = Participant.objects.all()
        serializer = ParticipantSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ParticipantSerializer, responses={201: ParticipantSerializer}
    )
    def post(self, request):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetailView(APIView):
    """Handles retrieve, update, delete of a single participant."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ParticipantSerializer, 404: "Not found"})
    def get(self, request, pk):
        try:
            user = Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        serializer = ParticipantSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ParticipantSerializer,
        responses={200: ParticipantSerializer, 400: "Bad request"},
    )
    def put(self, request, pk):
        try:
            user = Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        serializer = ParticipantSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: "Deleted", 404: "Not found"})
    def delete(self, request, pk):
        try:
            user = Participant.objects.get(pk=pk)
            user.delete()
            return Response(status=204)
        except Participant.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class EventParticipationListCreateView(APIView):
    """Handles listing and creating event participations."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: EventParticipationSerializer(many=True)})
    def get(self, request):
        participations = EventParticipation.objects.all()
        serializer = EventParticipationSerializer(participations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EventParticipationSerializer,
        responses={201: EventParticipationSerializer},
    )
    def post(self, request):
        serializer = EventParticipationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class JoinEventView(APIView):
    """
    API for joining an event.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "event": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Event ID"
                ),
                "is_organizer": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="Is organizer"
                ),
            },
            required=["event"],
        ),
        responses={201: EventParticipationSerializer, 400: "Bad request"},
    )
    def post(self, request):
        participant = request.user
        event_id = request.data.get("event")
        is_organizer = request.data.get("is_organizer", False)

        if not event_id:
            return Response({"error": "Event ID is required"}, status=400)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        # Check for existing participation
        if EventParticipation.objects.filter(
            event=event, participant=participant
        ).exists():
            return Response({"error": "You already joined this event"}, status=400)

        participation = EventParticipation.objects.create(
            event=event, participant=participant, is_organizer=is_organizer
        )
        serializer = EventParticipationSerializer(participation)
        return Response(serializer.data, status=201)
