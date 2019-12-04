mapboxgl.accessToken = 'pk.eyJ1IjoiamVyYWRob3kiLCJhIjoiY2szZXd5dnBuMDA0NzNobnRhNDBvMjJpNSJ9.QxDHGJ-5MQD--0c7XpVOVA'; //'pk.eyJ1IjoiamVyYWRob3kiLCJhIjoib1A4Y3RFayJ9.ve4v3jODJ71s2Bra6Q_xHw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/outdoors-v10',
    // style: 'mapbox://styles/mapbox/satellite-streets-v10',

    center: [-111.0429, 45.6770],
    zoom: 10
});
//map.addControl(new mapboxgl.FullscreenControl());

// map.addControl(new mapboxgl.GeolocateControl({
//   positionOptions: {
//     enableHighAccuracy: true
//   },
//   trackUserLocation: true
// }));


document.getElementById("sliderLabel").innerHTML = document.getElementById("distSlider").value + " miles"
document.getElementById("listings").innerHTML = "<b>Begin by selecting a starting point on any trail!</b>"



function buildPathList(data) {

    function linkEventListener(e) {

        let clickedTrail = data[this.dataPosition]
        let activeItem = document.getElementsByClassName('active');

        highlight_trails(clickedTrail["trails"])

        if (activeItem[0]) {
            activeItem[0].classList.remove('active');
        }
        this.parentNode.classList.add('active');
    }

    let listings = document.getElementById('listings');
    highlight_trails([""])

    listings.innerHTML = ""
        // Iterate through the list of stores
    for (let i = 0; i < data.length; i++) {

        let currentPath = data[i];

        // Select the listing container in the HTML and append a div
        // with the class 'item' for each store
        let listing = listings.appendChild(document.createElement('div'));
        listing.className = 'item';
        listing.id = 'listing-' + i;

        // Create a new link with the class 'title' for each store
        // and fill it with the store address
        let link = listing.appendChild(document.createElement('a'));
        link.href = '#';
        link.className = 'title';
        link.dataPosition = i;
        link.innerHTML = Math.round(currentPath["dist"] * 100) / 100 + " miles";
        link.addEventListener('mouseover', linkEventListener)

        if (i == 0) {
            const mouseoverEvent = new Event('mouseover');
            link.dispatchEvent(mouseoverEvent);
        }

    }



}



map.on('load', function(e) {

    map.addSource("junctions", {
        type: 'vector',
        url: 'mapbox://jeradhoy.bo7xlhfs',
    });

    map.addSource("trails", {
        type: 'vector',
        url: 'mapbox://jeradhoy.8nvbs1fn'
    });

    map.addLayer({
        id: "trails-all",
        type: "line",
        source: "trails",
        "source-layer": "trail_rel_split5-7gfg4m",
        layout: {
            "line-join": "round",
            "line-cap": "round"
        },
        paint: {
            "line-color": "#228B22",
            "line-width": 2,
            "line-dasharray": [1, 2]

        }
    });

    map.addLayer({
        id: "trails-highlighted",
        type: "line",
        source: "trails",
        "source-layer": "trail_rel_split5-7gfg4m",
        layout: {
            "line-join": "round",
            "line-cap": "round"
        },
        paint: {
            "line-color": "#ffff00",
            "line-width": 3
                //"line-offset": 2
        },
        filter: ["in", "id", ""]
    });

    map.addLayer({
        id: "junction-highlighted",
        type: "circle",
        source: "junctions",
        minzoom: 9,
        "source-layer": "juncts_split5-03ug6s",
        paint: {
            "circle-radius": 10,
            "circle-color": "#B42222",
            "circle-opacity": 1
        },
        filter: ["in", "junct_id", ""]
    });

    map.addLayer({
        id: "junctions-all",
        type: "circle",
        source: "junctions",
        minzoom: 9,
        "source-layer": "juncts_split5-03ug6s",
        paint: {
            "circle-radius": 10,
            "circle-color": "#B42222",
            "circle-opacity": 0
        }
    });

});


// Creates hover effect when you mouse over junction
map.on("mousemove", "junctions-all", function(e) {
    map.getCanvas().style.cursor = 'pointer';

    if (e.features.length > 0) {
        map.setFilter("junction-highlighted", ['in', "junct_id", ...juncts_selected, e.features[0].properties["junct_id"]])
    }
});


// Removes hover effect when you mouse over junction
map.on("mouseleave", "junctions-all", function() {

    map.getCanvas().style.cursor = '';

    map.setFilter("junction-highlighted", ['in', "junct_id", ...juncts_selected])
});

map.on("click", "trails-all", function(e) {
    console.log(e.features[0].properties)
});

let juncts_selected = [];
let mouseover_junct = [];
let maxMiles = document.getElementById("distSlider").value;

// Logs the junct_id of the feature you are mousing over
map.on("click", "junctions-all", function(e) {

    if (juncts_selected.length >= 2 || document.getElementById("routeType1").checked == true) {
        juncts_selected = []
    }

    juncts_selected.push(e.features[0].properties["junct_id"])
    map.setFilter("junction-highlighted", ['in', "junct_id", ...juncts_selected, ...mouseover_junct])

    if (document.getElementById("routeType1").checked == true || juncts_selected.length == 2) {
        get_paths_and_build(maxMiles, ...juncts_selected); //TODO: change to ...juncts_selected
    }

});

function get_paths_and_build(maxMiles, junct_id1, junct_id2) {

    document.getElementById('listings').innerHTML = "Loading..."

    var request = new XMLHttpRequest();

    let requestString = 'http://trails.jerad.co/routes/' + junct_id1 + "&"
    if (junct_id2) {
        requestString += junct_id2
    } else {
        requestString += "null"
    }

    requestString += "&" + maxMiles
    console.log(requestString)

    // Open a new connection, using the GET request on the URL endpoint
    request.open('GET', requestString, true)

    request.onload = function() {
        // Begin accessing JSON data here
        let data = JSON.parse(this.response)
        buildPathList(data)
    }

    // Send request
    request.send()

}

document.getElementById("routeType1").addEventListener('click', routeTypeTrigger)
document.getElementById("routeType2").addEventListener('click', routeTypeTrigger)

function routeTypeTrigger(e) {

    let routeTypeValue = e.target.value

    console.log(routeTypeValue)

    if (routeTypeValue == "pointToPoint") {
        // document.getElementById("distSlider").disabled = true;
    } else {
        juncts_selected.splice(0, 1)
        map.setFilter("junction-highlighted", ['in', "junct_id", ...juncts_selected])
        document.getElementById("distSlider").disabled = false;
        get_paths_and_build(maxMiles, ...juncts_selected);
    }
}


document.getElementById("distSlider").addEventListener('change', sliderSetTrigger)
document.getElementById("distSlider").addEventListener('input', sliderSlideTrigger)

function sliderSlideTrigger(e) {
    let maxMilesSlide = e.target.value
    document.getElementById("sliderLabel").innerHTML = maxMilesSlide + " miles"
}

function sliderSetTrigger(e) {

    maxMiles = e.target.value
    if (juncts_selected.length !== 0 && document.getElementById("routeType1").checked == true) {
        get_paths_and_build(maxMiles, juncts_selected[0]);
    } else if (juncts_selected.length == 2 && document.getElementById("routeType2").checked == true) {
        get_paths_and_build(maxMiles, ...juncts_selected);
    }

}

function highlight_trails(trail_id_array) {
    map.setFilter("trails-highlighted", ['in', "id", ...trail_id_array])
}

map.on('click', 'trails-all', function(e) {

    let coordinates = e.lngLat;
    var description = e.features[0].properties["name"];

    function toTitleCase(str) {
        str = str.toLowerCase().split(' ');
        for (var i = 0; i < str.length; i++) {
            str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
        }
        return str.join(' ');
    };

    popupHtml = "<b>" + toTitleCase(description) + "</b>"

    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(popupHtml)
        .addTo(map);
});