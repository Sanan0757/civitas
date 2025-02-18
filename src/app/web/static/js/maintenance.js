const map = initMap('map');

function addBuildingsLayer(geojson) {
    if (map.getSource('buildings-source')) {
        map.getSource('buildings-source').setData(geojson);
        return;
    }
    map.addSource('buildings-source', {type: 'geojson', data: geojson});

    map.addLayer({
        id: 'buildings-layer',
        type: 'fill',
        source: 'buildings-source',
        paint: {
            'fill-color': [
                'case',
                ['==', ['get', 'requires_maintenance'], true], window.maintenanceColors.true.color, // Color based on requires_maintenance
                window.maintenanceColors.false.color // Default color (no maintenance needed)
            ],
            'fill-opacity': 0.5
        }
    });

    map.addLayer({
        id: 'buildings-outline',
        type: 'line',
        source: 'buildings-source',
        paint: {'line-color': '#000', 'line-width': 1}
    });

    map.on('click', 'buildings-layer', (e) => {
        const properties = e.features[0].properties;
        const buildingId = properties.id;

        // Highlight selected building (improved)
        map.setPaintProperty('buildings-layer', 'fill-color', [
            'case',
            ['==', ['get', 'id'], properties.id],
            '#ff6600', // Highlight color
            [ // Restore original color
                'case',
                ['==', ['get', 'requires_maintenance'], true], window.maintenanceColors.true.color,
                window.maintenanceColors.false.color
            ]
        ]);

    const form = document.createElement('form');
    form.id = 'maintenance-form';

    // Set default values based on properties:
    const requiresMaintenanceValue = properties.requires_maintenance ? 'true' : 'false'; // Convert boolean to string
    const updatedByValue = properties.updated_by || ''; // Use empty string if updated_by is not present
    console.log(properties)
    form.innerHTML = `
        <h3>Update Maintenance Status</h3>
        <label for="requires_maintenance">Requires Maintenance:</label>
        <select id="requires_maintenance" name="requires_maintenance">
            <option value="true" ${requiresMaintenanceValue === 'true' ? 'selected' : ''}>Yes</option>
            <option value="false" ${requiresMaintenanceValue === 'false' ? 'selected' : ''}>No</option>
        </select><br><br>
        <label for="information">Additional Information:</label><br>
        <textarea id="information" name="information">${properties.information || ''}</textarea><br><br>
        <label for="updated_by">Updated By:</label>
        <input type="text" id="updated_by" name="updated_by" value="${updatedByValue}"><br><br>
        <button type="submit">Update</button>
    `;

        // 2. Add event listener to the form:
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            const newStatus = document.getElementById('requires_maintenance').value === 'true';
            const additionalInfo = document.getElementById('information').value;
            const updatedBy = document.getElementById('updated_by').value;

            updateMaintenanceStatus(buildingId, newStatus, additionalInfo, updatedBy);

            form.remove(); // Remove the form after submission
        });

        // 3. Display the form (e.g., in the sidebar):
        const buildingInfoDiv = document.getElementById('building-info');
        buildingInfoDiv.innerHTML = ""; // Clear existing info
        buildingInfoDiv.appendChild(form);

    });

    map.on('mouseenter', 'buildings-layer', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'buildings-layer', () => {
        map.getCanvas().style.cursor = '';
    });
}

// Click event to toggle maintenance status
map.on('click', 'buildings', (e) => {
    const feature = e.features[0];
    const buildingId = feature.properties.id;
    const currentStatus = feature.properties.requires_maintenance;

    const newStatus = !currentStatus; // Toggle maintenance status

    // Open a prompt to allow updating `information`, `updated_by`, `amenity_id`
    const additionalInfo = prompt("Enter additional information:");
    const updatedBy = prompt("Your name:");

    updateMaintenanceStatus(buildingId, newStatus, additionalInfo, updatedBy);
});

// Update maintenance status in backend
function updateMaintenanceStatus(buildingId, newStatus, information, updatedBy) {
    fetch(`${API_URL}/buildings/${buildingId}`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            requires_maintenance: newStatus,
            information: {notes: information},
            updated_by: updatedBy,
        })
    })
        .then(response => response.json())
        .then(updatedBuilding => {
            console.log("Updated:", updatedBuilding);
            fetchAndCacheData(addBuildingsLayer);
        })
        .catch(error => console.error("Error updating maintenance:", error));
}

map.on('load', () => {
    getCachedData().then(cachedData => {
        if (cachedData) {
            console.log("Using cached data.");
            addBuildingsLayer(cachedData);
        } else {
            console.log("Fetching fresh data.");
            fetchAndCacheData(addBuildingsLayer);
        }
    });
    console.log(window.maintenanceColors);
    const legend = createLegend("Buildings status", window.maintenanceColors); // Create the legend
    document.getElementById('map').parentNode.appendChild(legend); // Append legend
});
