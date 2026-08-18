from django import forms
from django.contrib import admin
from .models import District, ChargingStation, Connector, OwnerProfile


class ConnectorInline(admin.TabularInline):
    model = Connector
    extra = 1


class ChargingStationAdminForm(forms.ModelForm):
    """
    Keeps latitude/longitude on the model, but makes them read-only and
    auto-filled either by clicking/dragging on the map or by geocoding the
    typed Address field — so admins never have to hand-type coordinates.
    See static/js/admin_station_map.js for the map widget itself.
    """
    class Meta:
        model = ChargingStation
        fields = '__all__'
        widgets = {
            'latitude': forms.TextInput(attrs={'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        help_texts = {
            'latitude': 'Auto-filled from the map picker below — no need to type this.',
            'longitude': 'Auto-filled from the map picker below — no need to type this.',
        }


@admin.action(description="Approve selected stations (set Active)")
def approve_stations(modeladmin, request, queryset):
    queryset.update(status='active')


@admin.action(description="Deactivate selected stations")
def deactivate_stations(modeladmin, request, queryset):
    queryset.update(status='inactive')


@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    form = ChargingStationAdminForm
    list_display = ('name', 'district', 'owner', 'status', 'total_connectors', 'created_at')
    list_filter = ('status', 'district')
    search_fields = ('name', 'address', 'owner__username')
    inlines = [ConnectorInline]
    actions = [approve_stations, deactivate_stations]

    class Media:
        css = {
            'all': ('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',)
        }
        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'js/admin_station_map.js',
        )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    search_fields = ('name',)


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'phone', 'created_at')


admin.site.register(Connector)

admin.site.site_header = "EVCharge Admin"
admin.site.site_title = "EVCharge Admin Portal"
admin.site.index_title = "Manage stations, districts, and owners"
