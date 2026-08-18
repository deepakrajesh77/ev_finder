from django.core.management.base import BaseCommand
from stations.models import District, ChargingStation, Connector


class Command(BaseCommand):
    help = "Seed sample districts and charging stations for demo purposes"

    def handle(self, *args, **options):
        districts_data = ["Kollam", "Kozhikode", "Ernakulam", "Thiruvananthapuram", "Thrissur"]
        districts = {}
        for name in districts_data:
            d, _ = District.objects.get_or_create(name=name, defaults={'state': 'Kerala'})
            districts[name] = d

        sample_stations = [
            {"name": "GreenVolt Hub - Kollam", "district": "Kollam", "address": "MC Road, Kollam",
             "lat": 8.8932, "lng": 76.6141},
            {"name": "EcoCharge Point - Kozhikode", "district": "Kozhikode", "address": "Beach Road, Kozhikode",
             "lat": 11.2588, "lng": 75.7804},
            {"name": "ChargeUp Station - Ernakulam", "district": "Ernakulam", "address": "MG Road, Kochi",
             "lat": 9.9816, "lng": 76.2999},
            {"name": "SwiftVolt - Thiruvananthapuram", "district": "Thiruvananthapuram", "address": "Statue Junction, TVM",
             "lat": 8.5241, "lng": 76.9366},
            {"name": "PowerNode - Thrissur", "district": "Thrissur", "address": "Round South, Thrissur",
             "lat": 10.5276, "lng": 76.2144},
        ]

        for s in sample_stations:
            station, created = ChargingStation.objects.get_or_create(
                name=s["name"],
                defaults={
                    "district": districts[s["district"]],
                    "address": s["address"],
                    "latitude": s["lat"],
                    "longitude": s["lng"],
                    "description": "Reliable fast-charging point with ample parking and a waiting lounge.",
                    "status": "active",
                }
            )
            if created:
                Connector.objects.create(station=station, connector_type="CCS2", power_kw=50, count=2, price_per_kwh=12)
                Connector.objects.create(station=station, connector_type="Type2", power_kw=22, count=4, price_per_kwh=9)

        self.stdout.write(self.style.SUCCESS("Sample districts and stations created."))
