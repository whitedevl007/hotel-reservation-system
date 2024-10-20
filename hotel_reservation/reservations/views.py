from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from .models import Room, Reservation
from .forms import AvailabilityForm

class HomeView(TemplateView):
    template_name = 'reservations/home.html'

class RoomListView(ListView):
    model = Room
    template_name = 'reservations/room_list.html'
    context_object_name = 'rooms'

def check_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data['category']
            
            available_rooms = Room.objects.filter(category__name=category).exclude(
                reservation__start_date__lt=end_date,
                reservation__end_date__gt=start_date
            )
            
            return render(request, 'reservations/room_list.html', {'rooms': available_rooms})
    else:
        form = AvailabilityForm()
    
    return render(request, 'reservations/check_availability.html', {'form': form})