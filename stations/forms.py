from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import ChargingStation, Connector, OwnerProfile, District


class OwnerRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Choose a username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@company.com'}))
    company_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder': 'Company / Business name'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Contact number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        cpw = cleaned_data.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class StationForm(forms.ModelForm):
    class Meta:
        model = ChargingStation
        fields = [
            'name', 'district', 'address', 'latitude', 'longitude',
            'description', 'image', 'open_24_hours', 'opening_time',
            'closing_time', 'contact_number',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. GreenVolt Charging Hub'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street, City'}),
            'latitude': forms.TextInput(attrs={'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Amenities, parking info, etc.'}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Station contact number'}),
        }


ConnectorFormSet = inlineformset_factory(
    ChargingStation, Connector,
    fields=['connector_type', 'power_kw', 'count', 'price_per_kwh'],
    extra=1, can_delete=True,
)
