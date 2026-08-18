(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var latField = document.getElementById('id_latitude');
    var lngField = document.getElementById('id_longitude');
    var addressField = document.getElementById('id_address');
    if (!latField || !lngField || typeof L === 'undefined') return; // not the station form, or Leaflet not loaded

    latField.readOnly = true;
    lngField.readOnly = true;
    latField.style.background = '#f4f7f5';
    lngField.style.background = '#f4f7f5';

    var lngRow = lngField.closest('.form-row') || lngField.closest('.field-longitude') || lngField.parentElement;

    var wrapper = document.createElement('div');
    wrapper.className = 'form-row field-map-picker';
    wrapper.style.marginTop = '10px';
    wrapper.innerHTML =
      '<div>' +
        '<label style="display:block;font-weight:600;margin-bottom:6px;">Pick the station location</label>' +
        '<button type="button" id="adminLocateBtn" style="margin-bottom:10px;padding:8px 16px;border-radius:6px;border:1.5px solid #1a9c4a;background:#e6f7ec;color:#0b3d24;font-weight:600;cursor:pointer;">📍 Locate typed Address on map</button>' +
        '<div id="adminPickerMap" style="width:100%;max-width:640px;height:380px;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.15);"></div>' +
        '<p style="color:#666;font-size:12px;margin-top:6px;max-width:640px;">' +
          'Click anywhere on the map or drag the pin to set the exact spot — or type an address in the ' +
          '"Address" field above and click "Locate typed Address on map". Latitude/longitude fill in automatically, ' +
          'no manual typing needed.' +
        '</p>' +
      '</div>';

    lngRow.parentNode.insertBefore(wrapper, lngRow.nextSibling);

    var initLat = parseFloat(latField.value) || 10.8505;
    var initLng = parseFloat(lngField.value) || 76.2711;
    var hasInitial = !!(latField.value && lngField.value);

    var map = L.map('adminPickerMap').setView([initLat, initLng], hasInitial ? 15 : 7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    var greenIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background:#1a9c4a;width:20px;height:20px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>',
      iconSize: [20, 20],
    });

    var marker = hasInitial ? L.marker([initLat, initLng], { icon: greenIcon, draggable: true }).addTo(map) : null;
    if (marker) marker.on('dragend', onDrag);

    function setLocation(lat, lng) {
      lat = parseFloat(lat.toFixed(6));
      lng = parseFloat(lng.toFixed(6));
      if (marker) {
        marker.setLatLng([lat, lng]);
      } else {
        marker = L.marker([lat, lng], { icon: greenIcon, draggable: true }).addTo(map);
        marker.on('dragend', onDrag);
      }
      latField.value = lat;
      lngField.value = lng;
    }

    function onDrag(e) {
      var pos = e.target.getLatLng();
      setLocation(pos.lat, pos.lng);
    }

    map.on('click', function (e) { setLocation(e.latlng.lat, e.latlng.lng); });

    document.getElementById('adminLocateBtn').addEventListener('click', function () {
      var query = addressField ? addressField.value.trim() : '';
      if (!query) { alert('Type an address in the "Address" field first, then click this button.'); return; }
      fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(query))
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data && data.length) {
            var lat = parseFloat(data[0].lat), lng = parseFloat(data[0].lon);
            map.setView([lat, lng], 16);
            setLocation(lat, lng);
          } else {
            alert('Location not found for that address. Try refining it, or click directly on the map.');
          }
        })
        .catch(function () { alert('Could not search right now. Please click on the map instead.'); });
    });
  });
})();
