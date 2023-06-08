mapboxgl.accessToken = 'pk.eyJ1Ijoic3VtZWV0ciIsImEiOiJjbGlsYWRkdXMwM3FwM2Ntamw1ZGx5c2FyIn0.IYe3vklUYR6puqH0U_2uqw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/sumeetr/clilahnon006q01r8dhkqd4nm',
    center: [-74.5, 40], 
    zoom: 1, 
    projection: 'globe'
});

map.on('load', function () {
    map.addSource('heat', {
        type: 'geojson',
        data: '/generate-data' 
    });

    map.addLayer({
        id: 'heat',
        type: 'heatmap',
        source: 'heat',
        paint: {
            'heatmap-weight': ['get', 'Score'],
            'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 9, 3],
            'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0, 'rgba(33,102,172,0)',
                0.02, 'rgb(103,169,207)',
                0.05, 'rgb(209,229,240)',
                0.08, 'rgb(253,219,199)',
                0.1, 'rgb(239,138,98)',
                0.15, 'rgb(178,24,43)'
            ],
            'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 7, 9, 20],
            'heatmap-opacity': ['interpolate', ['linear'], ['zoom'], 7, 1, 9, 0]
        }
    });
});

document.getElementById('submit').addEventListener('click', function () {
    var toggles = [];
    var checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
    for (var i = 0; i < checkboxes.length; i++) {
        toggles.push(parseInt(checkboxes[i].value));
    }
    fetch('/generate-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(toggles)
    })
        .then(response => response.json())
        .then(data => {
            map.getSource('heat').setData(data);
        });
});