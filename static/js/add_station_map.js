document.addEventListener('DOMContentLoaded', function () {
  const latInput = document.getElementById('id_latitude');
  const lngInput = document.getElementById('id_longitude');
  const coordDisplay = document.getElementById('coordDisplay');
  const initial = window.INITIAL_COORDS || { lat: 10.8505, lng: 76.2711 };

  const map = L.map('pickerMap').setView([initial.lat, initial.lng], window.INITIAL_COORDS ? 15 : 7);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map);

  const greenIcon = L.divIcon({
    className: 'custom-marker',
    html: '<div style="background:#1a9c4a;width:20px;height:20px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>',
    iconSize: [20, 20],
  });

  let marker = window.INITIAL_COORDS ? L.marker([initial.lat, initial.lng], { icon: greenIcon, draggable: true }).addTo(map) : null;

  function setLocation(lat, lng) {
    lat = parseFloat(lat.toFixed(6));
    lng = parseFloat(lng.toFixed(6));
    if (marker) { marker.setLatLng([lat, lng]); }
    else { marker = L.marker([lat, lng], { icon: greenIcon, draggable: true }).addTo(map); marker.on('dragend', onDrag); }
    latInput.value = lat;
    lngInput.value = lng;
    coordDisplay.textContent = lat + ', ' + lng;
  }

  function onDrag(e) {
    const pos = e.target.getLatLng();
    setLocation(pos.lat, pos.lng);
  }

  if (marker) marker.on('dragend', onDrag);

  map.on('click', function (e) {
    setLocation(e.latlng.lat, e.latlng.lng);
  });

  // Address search using OpenStreetMap Nominatim
  const searchInput = document.getElementById('mapSearchInput');
  let searchTimeout;
  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      const query = this.value.trim();
      if (!query) return;
      fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(query))
        .then(res => res.json())
        .then(data => {
          if (data && data.length) {
            const lat = parseFloat(data[0].lat), lng = parseFloat(data[0].lon);
            map.setView([lat, lng], 16);
            setLocation(lat, lng);
          } else {
            alert('Location not found. Try a different search or click directly on the map.');
          }
        })
        .catch(() => alert('Could not search location right now. Please click on the map instead.'));
    }
  });
});
