# from django import forms
# from .models import RoomCategory

# class AvailabilityForm(forms.Form):
#     start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     category = forms.ModelChoiceField(queryset=RoomCategory.objects.all())






from django import forms
from .models import RoomCategory, Reservation

class AvailabilityForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(queryset=RoomCategory.objects.all())

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'customer_name']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


