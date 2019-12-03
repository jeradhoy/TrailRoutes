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

var hoverPointId = null;


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

        // Create a new div with the class 'details' for each store
        // and fill it with the city and phone number
        //let details = listing.appendChild(document.createElement('div'));
        //details.innerHTML = currentPath["dist"];
        //details.innerHTML += " miles"
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

map.on('style.load', function() {
    // Triggered when `setStyle` is called.
});


// Creates hover effect when you mouse over junction
map.on("mousemove", "junctions-all", function(e) {
    map.getCanvas().style.cursor = 'pointer';

    if (e.features.length > 0) {


        console.log(e.features[0].properties["junct_id"])
        map.setFilter("junction-highlighted", ['in', "junct_id", e.features[0].properties["junct_id"]])

        // if (hoverPointId) {
        //     map.setFeatureState({ source: 'junctions', id: hoverPointId, sourceLayer: "juncts_split5-03ug6s" }, { hover: false });
        // }
        // hoverPointId = e.features[0].id;
        // console.log(hoverPointId)
        // map.setFeatureState({ source: 'junctions', id: hoverPointId, sourceLayer: "juncts_split5-03ug6s" }, { hover: true });
    }
});

// Removes hover effect when you mouse over junction
map.on("mouseleave", "junctions-all", function() {

    map.getCanvas().style.cursor = '';
    map.setFilter("junction-highlighted", ['in', "junct_id", ""])
        // if (hoverPointId) {
        //     map.setFeatureState({ source: 'junctions', id: hoverPointId, sourceLayer: "juncts_split5-03ug6s" }, { hover: false });
        // }
        // hoveredStateId = null;
});

map.on("click", "trails-all", function(e) {
    console.log(e.features[0].properties)
});

let junct_selected = null

// Logs the junct_id of the feature you are mousing over
map.on("click", "junctions-all", function(e) {

    //let maxMiles = document.getElementById("maxMileInput").value;
    let maxMiles = document.getElementById("distSlider").value
    junct_selected = e.features[0].properties["junct_id"];
    //map.setFilter("junction-highlighted", ['in', "junct_id", junct_selected])

    get_paths_and_build(maxMiles, junct_selected);

});

function get_paths_and_build(maxMiles, junct_id) {

    document.getElementById('listings').innerHTML = "Loading..."

    var request = new XMLHttpRequest();

    let requestString = 'http://trails.jerad.co/routes/' + junct_id + "&" + maxMiles

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

//document.getElementById("maxMileInput").addEventListener('input', inputChangeTrigger)

document.getElementById("distSlider").addEventListener('change', sliderSetTrigger)

document.getElementById("distSlider").addEventListener('input', sliderSlideTrigger)

document.getElementById("routeType").addEventListener('click', routeTypeTrigger)

function routeTypeTrigger(e) {
    let routeTypeValue = document.getElementById("routeType").value
    console.log(routeTypeValue)
    if (routeTypeValue == "pointToPoint") {
        document.getElementById("distSlider").disabled = true;
    } else {
        document.getElementById("distSlider").disabled = false;
    }
}


function sliderSlideTrigger(e) {
    let maxMiles = document.getElementById("distSlider").value
    document.getElementById("sliderLabel").innerHTML = maxMiles + " miles"
}

function sliderSetTrigger(e) {

    let maxMiles = document.getElementById("distSlider").value;

    if (junct_selected !== null) {
        get_paths_and_build(maxMiles, junct_selected);
    }

}

// document.getElementById("basemapControl").addEventListener('click', switchLayer)

// function switchLayer() {
//     let newStyle = document.getElementById("basemapControl").value;
//     let oldStyle = map.getStyle()["sprite"]
//     console.log(newStyle)
//     console.log(oldStyle)
//     map.setStyle(newStyle);
//     document.getElementById("basemapControl").value = oldStyle
// }

// function inputChangeTrigger(e){
//   console.log("input changed!")
//   console.log(junct_selected)
//   let maxMiles = document.getElementById("maxMileInput").value;
//   if(junct_selected !== null){
//     console.log("building!")
//     get_paths_and_build(maxMiles, junct_selected);
//   }
// }



function highlight_trails(trail_id_array) {
    map.setFilter("trails-highlighted", ['in', "id", ...trail_id_array])
}

map.on('click', 'trails-all', function(e) {

    //var coordinates = e.features[0].geometry.coordinates[0];
    let coordinates = e.lngLat;
    console.log(coordinates)
    var description = e.features[0].properties["name"];
    console.log(description)

    function toTitleCase(str) {
        str = str.toLowerCase().split(' ');
        for (var i = 0; i < str.length; i++) {
            str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
        }
        return str.join(' ');
    };

    // Ensure that if the map is zoomed out such that multiple
    // copies of the feature are visible, the popup appears
    // over the copy being pointed to.
    // while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
    //     coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    // }

    popupHtml = "<b>" + toTitleCase(description) + "</b>"

    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(popupHtml)
        .addTo(map);
});