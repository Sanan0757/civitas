mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;

window.categoryColors = {  // Define colors for each category
    "Emergency and Public Services": {
        color: "#007bff",  // Blue
        label: "Emergency and Public Services"
    },
    "Food and Drink": {
        color: "#ffc107",  // Yellow
        label: "Food and Drink"
    },
    "Community and Culture": {
        color: "#28a745",  // Green
        label: "Community and Culture"
    },
    "Commercial and Financial":{
        color: "#dc3545",  // Red
        label: "Commercial and Financial"
    },
    "Residential": {
        color: "#17a2b8",  // Cyan
        label: "Residential"
    },
    "Other Amenities":{
        color: "#6f42c1",  // Purple
        label: "Other Amenities"
    }
};

window.maintenanceColors = {
    true: {
        color: '#FF0000',  // Red for buildings needing maintenance
        label: "Needs Maintenance"
    },
    false: {
        color: '#00FF00',
        label: "Good condition"
    }
};
