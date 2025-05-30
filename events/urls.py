# urls.py

from django.urls import path
from .views import (
    EventListCreateView,
    EventDetailView,
    UserListCreateView,
    UserDetailView,
    EventParticipationListCreateView,
    JoinEventView,
)

urlpatterns = [
    path("events/", EventListCreateView.as_view(), name="event-list-create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("participants/", UserListCreateView.as_view(), name="participant-list-create"),
    path("participants/<int:pk>/", UserDetailView.as_view(), name="participant-detail"),
    path(
        "participations/",
        EventParticipationListCreateView.as_view(),
        name="event-participation-list-create",
    ),
    path("events/join/", JoinEventView.as_view(), name="join-event"),
]
