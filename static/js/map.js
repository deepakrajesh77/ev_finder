document.addEventListener('DOMContentLoaded', function () {
  const stations = window.MAP_STATIONS || [];
  const userLoc = window.USER_LOCATION;

  let centerLat = 10.8505, centerLng = 76.2711, zoom = 7; // Kerala default
  if (userLoc) { centerLat = userLoc.lat; centerLng = userLoc.lng; zoom = 12; }
  else if (stations.length) { centerLat = stations[0].lat; centerLng = stations[0].lng; zoom = 11; }

  const map = L.map('resultsMap').setView([centerLat, centerLng], zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map);

  const greenIcon = L.divIcon({
    className: 'custom-marker',
    html: '<div style="background:#1a9c4a;width:16px;height:16px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>',
    iconSize: [16, 16],
  });

  const markers = {};
  stations.forEach(function (s) {
    const m = L.marker([s.lat, s.lng], { icon: greenIcon }).addTo(map);
    m.bindPopup('<strong>' + s.name + '</strong><br><a href="' + s.url + '">View details →</a>');
    markers[s.lat + ',' + s.lng] = m;
  });

  if (userLoc) {
    L.circleMarker([userLoc.lat, userLoc.lng], {
      radius: 8, color: '#0b3d24', fillColor: '#22b556', fillOpacity: 1, weight: 3,
    }).addTo(map).bindPopup('You are here');
  }

  document.querySelectorAll('.locate-on-map').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const lat = parseFloat(this.dataset.lat), lng = parseFloat(this.dataset.lng);
      map.setView([lat, lng], 15);
      const key = lat + ',' + lng;
      if (markers[key]) markers[key].openPopup();
    });
  });
});
