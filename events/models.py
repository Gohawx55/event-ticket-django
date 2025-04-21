from django.db import models
from django.contrib.auth.models import User  
from django.core.files import File
from io import BytesIO
import qrcode

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.event.title} — {self.quantity} шт."

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr = qrcode.make(f"Ticket for {self.event.title} — {self.purchase_date}")
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            filename = f"qr_{self.event.title}_{self.purchase_date}.png"
            self.qr_code.save(filename, File(buffer), save=False)
        super().save(*args, **kwargs)
