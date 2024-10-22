# models.py
from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError

class RoomCategory(models.Model):
    name = models.CharField(max_length=50)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.room_number} - {self.category.name}"

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        base_price = self.room.category.base_price
        nights = (self.end_date - self.start_date).days
        special_rates = SpecialRate.objects.filter(
            room_category=self.room.category,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        )

        total_price = 0
        for day in range(nights):
            current_date = self.start_date + timedelta(days=day)
            day_rate = base_price
            for rate in special_rates:
                if rate.start_date <= current_date <= rate.end_date:
                    day_rate *= rate.rate_multiplier
                    break
            total_price += day_rate

        return total_price

class SpecialRate(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rate_multiplier = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
