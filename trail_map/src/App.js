import "mapbox-gl/dist/mapbox-gl.css"
//import "react-map-gl-geocoder/dist/mapbox-gl-geocoder.css"
import React, { Component } from 'react'
import MapGL, { GeolocateControl, NavigationControl } from "react-map-gl";
import "./App.css"
//import DeckGL, { GeoJsonLayer } from "deck.gl";
//import Geocoder from "react-map-gl-geocoder";

const TOKEN = "pk.eyJ1IjoiamVyYWRob3kiLCJhIjoib1A4Y3RFayJ9.ve4v3jODJ71s2Bra6Q_xHw"

class Map extends Component {
  state = { 
    viewport :{
      latitude: 45.6770,
      longitude: -111.0429,
      zoom: 10
    }
  }

    render(){
      //const { viewport, searchResultLayer} = this.state
      return (
        <div style={{ height: '100vh'}}>
          <MapGL 
            {...this.state.viewport}
            mapStyle="mapbox://styles/mapbox/outdoors-v11"
            width="100%"
            height="100%"
            onViewportChange={(viewport) => this.setState({viewport})}
            mapboxApiAccessToken={TOKEN}
            >
              <GeolocateControl />
              <NavigationControl />
            </MapGL>
        </div>
      )
    }
}

export default Map;