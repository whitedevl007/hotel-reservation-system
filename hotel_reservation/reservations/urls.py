# from django.urls import path
# from .views import HomeView, RoomListView, check_availability

# urlpatterns = [
#     path('', HomeView.as_view(), name='home'),
#     path('rooms/', RoomListView.as_view(), name='room_list'),
#     path('check-availability/', check_availability, name='check_availability'),
# ]





from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomeView, RoomListView, check_availability, room_detail, reservation_create

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<int:room_id>/', room_detail, name='room_detail'),
    path('check-availability/', check_availability, name='check_availability'),
    path('reservation/create/<int:room_id>/', reservation_create, name='reservation_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)