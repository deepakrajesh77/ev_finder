import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .models import ChargingStation, District, OwnerProfile, Connector
from .forms import OwnerRegisterForm, StationForm, ConnectorFormSet


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def home(request):
    districts = District.objects.all()
    total_stations = ChargingStation.objects.filter(status='active').count()
    return render(request, 'home.html', {
        'districts': districts,
        'total_stations': total_stations,
    })


def search_results(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    district_id = request.GET.get('district')
    query_text = request.GET.get('q', '').strip()
    radius_km = float(request.GET.get('radius', 25))

    stations = ChargingStation.objects.filter(status='active').select_related('district').prefetch_related('connectors')

    results = []
    search_mode = None

    if district_id:
        search_mode = 'district'
        stations = stations.filter(district_id=district_id)
        for s in stations:
            results.append({'station': s, 'distance': None})
    elif lat and lng:
        search_mode = 'location'
        lat, lng = float(lat), float(lng)
        for s in stations:
            d = haversine_km(lat, lng, s.latitude, s.longitude)
            if d <= radius_km:
                results.append({'station': s, 'distance': round(d, 1)})
        results.sort(key=lambda r: r['distance'])
    elif query_text:
        search_mode = 'text'
        stations = stations.filter(Q(name__icontains=query_text) | Q(address__icontains=query_text) | Q(district__name__icontains=query_text))
        for s in stations:
            results.append({'station': s, 'distance': None})
    else:
        for s in stations:
            results.append({'station': s, 'distance': None})

    return render(request, 'search_results.html', {
        'results': results,
        'search_mode': search_mode,
        'lat': lat,
        'lng': lng,
        'districts': District.objects.all(),
        'selected_district': int(district_id) if district_id else None,
        'query_text': query_text,
    })


def station_detail(request, pk):
    station = get_object_or_404(ChargingStation, pk=pk, status='active')
    return render(request, 'station_detail.html', {'station': station})


def register_owner(request):
    if request.method == 'POST':
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'], email=data['email'], password=data['password']
            )
            OwnerProfile.objects.create(
                user=user, company_name=data['company_name'], phone=data['phone'], is_owner=True
            )
            login(request, user)
            messages.success(request, "Welcome! Your owner account is ready. Add your first station below.")
            return redirect('owner_dashboard')
    else:
        form = OwnerRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            return redirect('owner_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def owner_dashboard(request):
    stations = ChargingStation.objects.filter(owner=request.user).prefetch_related('connectors')
    return render(request, 'owner_dashboard.html', {'stations': stations})


@login_required
def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES)
        if form.is_valid():
            station = form.save(commit=False)
            station.owner = request.user
            station.status = 'pending'
            station.save()
            formset = ConnectorFormSet(request.POST, instance=station)
            if formset.is_valid():
                formset.save()
            messages.success(request, "Station submitted! It will appear publicly once approved by an admin.")
            return redirect('owner_dashboard')
        else:
            formset = ConnectorFormSet(request.POST)
    else:
        form = StationForm()
        formset = ConnectorFormSet()
    return render(request, 'add_station.html', {
        'form': form, 'formset': formset, 'districts': District.objects.all(),
    })


@login_required
def edit_station(request, pk):
    station = get_object_or_404(ChargingStation, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES, instance=station)
        formset = ConnectorFormSet(request.POST, instance=station)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Station updated successfully.")
            return redirect('owner_dashboard')
    else:
        form = StationForm(instance=station)
        formset = ConnectorFormSet(instance=station)
    return render(request, 'add_station.html', {
        'form': form, 'formset': formset, 'districts': District.objects.all(), 'editing': True, 'station': station,
    })


@login_required
def delete_station(request, pk):
    station = get_object_or_404(ChargingStation, pk=pk, owner=request.user)
    if request.method == 'POST':
        station.delete()
        messages.success(request, "Station deleted.")
    return redirect('owner_dashboard')
