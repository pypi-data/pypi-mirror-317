let map;
let marker;

// In case `whiteboxSockets` is undefined, we are running in template mode,
// meaning that the mission control has defined the `socket` object for us.
//
// In case it is defined, we are running within the frontend encapsulation,
// and have the socket already connected for us, so let's use it
if (typeof window.whiteboxSockets !== 'undefined') {
    window.socket = window.whiteboxSockets['flight'];
}

document.addEventListener("DOMContentLoaded", (event) => {
  map = L.map("map").setView([0, 0], 2);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  marker = L.marker([0, 0]).addTo(map);
});

// Function to update map with new GPS coordinates
function updateGPSLocation(lat, lon) {
  if (map && marker) {
    marker.setLatLng([lat, lon]);
    map.setView([lat, lon], 10);
  }
}

// Listen for GPS updates from the WebSocket
socket.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "location_update") {
    updateGPSLocation(data.latitude, data.longitude);
  }
});
