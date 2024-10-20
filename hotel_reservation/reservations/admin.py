from django.contrib import admin
from .models import Room, RoomCategory, Reservation, SpecialRate

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('room_number', 'category__name')

admin.site.register(Room, RoomAdmin)
admin.site.register(RoomCategory)
admin.site.register(Reservation)
admin.site.register(SpecialRate)
