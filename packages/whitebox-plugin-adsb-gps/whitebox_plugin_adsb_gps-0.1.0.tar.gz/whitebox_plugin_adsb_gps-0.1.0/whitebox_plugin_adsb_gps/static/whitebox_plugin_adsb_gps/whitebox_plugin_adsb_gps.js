const staleTrafficTimeout = 1000 * 10;
const removeIntervalForStaleTraffic = 1000 * 1;
const trafficState = [];

socket.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "location_update":
      updateCurrentLocation(
        data.latitude,
        data.longitude,
        data.altitude,
        data.gps_timestamp
      );
      break;
    case "traffic_update":
      updateTrafficData(data);
      break;
  }
});

function updateCurrentLocation(lat, lon, alt, ts) {
  const latitude = document.getElementById("gps-data-latitude");
  const longitude = document.getElementById("gps-data-longitude");
  const altitude = document.getElementById("gps-data-altitude");
  const gps_timestamp = document.getElementById("gps-data-timestamp");

  latitude.textContent = lat;
  longitude.textContent = lon;
  altitude.textContent = alt;
  gps_timestamp.textContent = ts;
}

function addTrafficToState(traffic) {
  let trafficData = { ...traffic, lastUpdate: Date.now() };

  const existingTraffic = trafficState.find(
    (traffic) => traffic.Icao_addr === trafficData.Icao_addr
  );

  if (existingTraffic) {
    Object.assign(existingTraffic, trafficData);
  } else {
    trafficState.push(trafficData);
  }
}

function removeTrafficFromState() {
  const currentTime = Date.now();

  for (let i = trafficState.length - 1; i >= 0; i--) {
    if (currentTime - trafficState[i].lastUpdate > staleTrafficTimeout) {
      console.log("Removing stale traffic", trafficState[i]);
      trafficState.splice(i, 1);
    }
  }
}

function formatLocation(lat, lng) {
  if (!lat || !lng) return "N/A";
  const latDeg = Math.abs(Math.floor(lat));
  const latMin = Math.abs(Math.round((lat - Math.floor(lat)) * 60));
  const lngDeg = Math.abs(Math.floor(lng));
  const lngMin = Math.abs(Math.round((lng - Math.floor(lng)) * 60));
  return `${latDeg}° ${latMin}' ${lat >= 0 ? "N" : "S"} ${lngDeg}° ${lngMin}' ${
    lng >= 0 ? "E" : "W"
  }`;
}

function renderTrafficBody() {
  const trafficTableBody = document.getElementById("traffic-table-body");
  trafficTableBody.innerHTML = "";

  trafficState.forEach((trafficData) => {
    const newRow = document.createElement("tr");
    newRow.setAttribute("data-icao", trafficData.Icao_addr);

    const displayData = {
      callsign: trafficData.Tail || "Unknown",
      code: trafficData.Icao_addr.toString(),
      location: formatLocation(trafficData.Lat, trafficData.Lng),
      altitude: trafficData.Alt.toLocaleString(),
      speed: trafficData.Speed_valid ? Math.round(trafficData.Speed) : "N/A",
      course: trafficData.Track ? `${Math.round(trafficData.Track)}°` : "N/A",
      power: trafficData.SignalLevel.toFixed(2),
      age: trafficData.Age.toFixed(1),
    };

    Object.values(displayData).forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      newRow.appendChild(cell);
    });

    trafficTableBody.appendChild(newRow);
  });
}

function updateTrafficData(data) {
  addTrafficToState(data);
  renderTrafficBody();
}

setInterval(() => {
  removeTrafficFromState();
  renderTrafficBody();
}, removeIntervalForStaleTraffic);
