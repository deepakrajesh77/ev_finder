document.addEventListener('DOMContentLoaded', function () {
  const station = window.STATION;
  const map = L.map('detailMap').setView([station.lat, station.lng], 15);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map);

  const greenIcon = L.divIcon({
    className: 'custom-marker',
    html: '<div style="background:#1a9c4a;width:20px;height:20px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>',
    iconSize: [20, 20],
  });
  L.marker([station.lat, station.lng], { icon: greenIcon }).addTo(map).bindPopup(station.name).openPopup();

  let routingControl = null;

  // ---- Preview Route: draws the route on the embedded map (good for desktop / planning ahead) ----
  document.getElementById('previewRouteBtn').addEventListener('click', function () {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by this browser. Try "Start Navigation" instead.');
      return;
    }
    const btn = this;
    btn.textContent = 'Locating you…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      btn.textContent = '🗺️ Preview Route on Map';
      const userLat = pos.coords.latitude, userLng = pos.coords.longitude;

      if (routingControl) map.removeControl(routingControl);

      routingControl = L.Routing.control({
        waypoints: [L.latLng(userLat, userLng), L.latLng(station.lat, station.lng)],
        lineOptions: { styles: [{ color: '#1a9c4a', weight: 5 }] },
        createMarker: function (i, wp) {
          return L.marker(wp.latLng, {
            icon: L.divIcon({
              className: 'custom-marker',
              html: i === 0
                ? '<div style="background:#0b3d24;width:16px;height:16px;border-radius:50%;border:3px solid white;"></div>'
                : '<div style="background:#1a9c4a;width:20px;height:20px;border-radius:50%;border:3px solid white;"></div>',
              iconSize: [20, 20],
            }),
          });
        },
        show: true,
        collapsible: true,
      }).addTo(map);
    }, function () {
      btn.textContent = '🗺️ Preview Route on Map';
      alert('Could not get your location. Please allow location access to preview the route.');
    });
  });

  // ---- Start Navigation: hands off to the device's own maps app for real turn-by-turn GPS navigation ----
  document.getElementById('startNavBtn').addEventListener('click', function () {
    const btn = this;
    const destination = station.lat + ',' + station.lng;

    function openNavigation(originParam) {
      const isAppleDevice = /iPhone|iPad|iPod/.test(navigator.userAgent);
      let url;
      if (isAppleDevice) {
        // Apple Maps deep link — falls back to Google Maps if unsupported
        url = 'https://maps.apple.com/?daddr=' + destination + (originParam ? '&saddr=' + originParam : '') + '&dirflg=d';
      } else {
        // Google Maps turn-by-turn directions (works in-browser and hands off to the app if installed)
        url = 'https://www.google.com/maps/dir/?api=1&destination=' + destination + '&travelmode=driving' + (originParam ? '&origin=' + originParam : '');
      }
      window.open(url, '_blank');
    }

    if (!navigator.geolocation) {
      openNavigation(null); // maps app will use device location automatically
      return;
    }
    btn.textContent = 'Locating you…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      btn.textContent = '🚀 Start Navigation';
      openNavigation(pos.coords.latitude + ',' + pos.coords.longitude);
    }, function () {
      btn.textContent = '🚀 Start Navigation';
      openNavigation(null); // still navigate; maps app will ask for / use current location
    });
  });
});
