from django.urls import path
from .views import HomeView, RoomListView, check_availability

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('check-availability/', check_availability, name='check_availability'),
]