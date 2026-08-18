from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OwnerProfile(models.Model):
    """Extra profile info for station-owner accounts."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    company_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_owner = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} (Owner)"


class ChargingStation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stations', null=True, blank=True)
    name = models.CharField(max_length=150)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='stations')
    address = models.CharField(max_length=255)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='station_images/', blank=True, null=True)
    open_24_hours = models.BooleanField(default=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def total_connectors(self):
        return self.connectors.count()


class Connector(models.Model):
    TYPE_CHOICES = (
        ('CCS2', 'CCS2'),
        ('CHAdeMO', 'CHAdeMO'),
        ('Type2', 'Type 2 (AC)'),
        ('GBT', 'GB/T'),
        ('Bharat_AC001', 'Bharat AC-001'),
        ('Bharat_DC001', 'Bharat DC-001'),
    )
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE, related_name='connectors')
    connector_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    power_kw = models.DecimalField(max_digits=6, decimal_places=2, help_text="Power output in kW")
    count = models.PositiveIntegerField(default=1, help_text="Number of this connector type available")
    price_per_kwh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.connector_type} - {self.power_kw}kW"
