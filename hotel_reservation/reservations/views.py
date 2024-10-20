# from django.views.generic import TemplateView, ListView
# from django.shortcuts import render
# from .models import Room, Reservation
# from .forms import AvailabilityForm

# class HomeView(TemplateView):
#     template_name = 'reservations/home.html'

# class RoomListView(ListView):
#     model = Room
#     template_name = 'reservations/room_list.html'
#     context_object_name = 'rooms'

# def check_availability(request):
#     if request.method == 'POST':
#         form = AvailabilityForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             category = form.cleaned_data['category']
            
#             available_rooms = Room.objects.filter(category__name=category).exclude(
#                 reservation__start_date__lt=end_date,
#                 reservation__end_date__gt=start_date
#             )
            
#             return render(request, 'reservations/room_list.html', {'rooms': available_rooms})
#     else:
#         form = AvailabilityForm()
    
#     return render(request, 'reservations/check_availability.html', {'form': form})









from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Room, RoomCategory, Reservation
from .forms import AvailabilityForm, ReservationForm
from datetime import datetime

class HomeView(TemplateView):
    template_name = 'reservations/home.html'

class RoomListView(ListView):
    model = Room
    template_name = 'reservations/room_list.html'
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_categories'] = RoomCategory.objects.all()
        return context

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = AvailabilityForm()
    return render(request, 'reservations/room_detail.html', {'room': room, 'form': form})

def check_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data['category']
            
            available_rooms = Room.objects.filter(category=category).exclude(
                reservation__start_date__lt=end_date,
                reservation__end_date__gt=start_date
            )
            
            context = {
                'rooms': available_rooms,
                'room_categories': RoomCategory.objects.all(),
                'start_date': start_date,
                'end_date': end_date
            }
            return render(request, 'reservations/room_list.html', context)
    else:
        form = AvailabilityForm()
    return render(request, 'reservations/check_availability.html', {'form': form})

def reservation_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Check if the room is available for the selected dates
            if Reservation.objects.filter(room=room, start_date__lt=end_date, end_date__gt=start_date).exists():
                messages.error(request, "This room is not available for the selected dates. Please choose different dates or another room.")
                return render(request, 'reservations/reservation_create.html', {'form': form, 'room': room})
            
            reservation = form.save(commit=False)
            reservation.room = room
            reservation.total_price = reservation.calculate_total_price()
            reservation.save()
            messages.success(request, "Reservation created successfully!")
            return redirect('room_list')
    else:
        initial_data = {}
        if 'start_date' in request.GET and 'end_date' in request.GET:
            initial_data['start_date'] = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
            initial_data['end_date'] = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
        form = ReservationForm(initial=initial_data)
    return render(request, 'reservations/reservation_create.html', {'form': form, 'room': room})


