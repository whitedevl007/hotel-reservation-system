# views.py
from django.http import JsonResponse
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
    availability_form = AvailabilityForm()
    reservation_form = ReservationForm()

    context = {
        'room': room,
        'availability_form': availability_form,
        'reservation_form': reservation_form,
    }
    return render(request, 'reservations/room_detail.html', context)

def get_reserved_dates(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    reservations = Reservation.objects.filter(room=room)
    events = []
    for reservation in reservations:
        events.append({
            'title': 'Reserved',
            'start': reservation.start_date.strftime('%Y-%m-%d'),
            'end': reservation.end_date.strftime('%Y-%m-%d'),
            'color': 'red'
        })
    return JsonResponse(events, safe=False)

def check_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            room_id = request.POST.get('room_id')
            room = get_object_or_404(Room, id=room_id)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Check if the room is available for the selected dates
            if Reservation.objects.filter(room=room, start_date__lt=end_date, end_date__gt=start_date).exists():
                return JsonResponse({'available': False})
            else:
                return JsonResponse({'available': True})
    return JsonResponse({'available': False})

# def reservation_create(request, room_id):
#     room = get_object_or_404(Room, id=room_id)
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']

#             # Check if the room is available for the selected dates
#             if Reservation.objects.filter(room=room, start_date__lt=end_date, end_date__gt=start_date).exists():
#                 messages.error(request, "This room is not available for the selected dates. Please choose different dates or another room.")
#                 return render(request, 'reservations/room_detail.html', {'room': room, 'availability_form': AvailabilityForm(), 'reservation_form': form})

#             reservation = form.save(commit=False)
#             reservation.room = room  # Ensure the room is assigned
#             reservation.total_price = reservation.calculate_total_price()
#             reservation.save()
#             messages.success(request, "Reservation created successfully!")
#             return redirect('room_list')
#         else:
#             messages.error(request, "Form is not valid. Please check the input.")
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#             return render(request, 'reservations/room_detail.html', {'room': room, 'availability_form': AvailabilityForm(), 'reservation_form': form})
#     else:
#         initial_data = {}
#         if 'start_date' in request.GET and 'end_date' in request.GET:
#             initial_data['start_date'] = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
#             initial_data['end_date'] = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
#         form = ReservationForm(initial=initial_data)
#     return render(request, 'reservations/room_detail.html', {'room': room, 'availability_form': AvailabilityForm(), 'reservation_form': form})


def reservation_create(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.room = room
            reservation.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation_create.html', {'form': form, 'room': room})