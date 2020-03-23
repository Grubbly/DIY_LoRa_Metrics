<template>
  <center>
    <div>
      <gmap-map
        :center="center"
        :zoom="12"
        style="width:75%;  height: 800px;"
      >
        <gmap-marker
          :key="index"
          v-for="(m, index) in markers"
          :position="m.position"
          @click="center=m.position"
        ></gmap-marker>
      </gmap-map>
    </div>
  </center>
</template>

<script>

import position_data from '../../test_data.json'

export default {
  name: "Map",
  data() {
    return {
      // default to Montreal to keep it simple
      // change this to whatever makes sense
      center: { lat: 45.508, lng: -73.587 },
      markers: [],
      places: [],
      currentPlace: null
    };
  },

  methods: {
    // receives a place object via the autocomplete component
    setPlace(place) {
      this.currentPlace = place;
    },
    geolocate: function() {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    }
  },

  mounted() {
    position_data.forEach(pos => {
      const marker = {
          lat: parseFloat(pos.lat),
          lng: parseFloat(pos.long)
        };
        this.markers.push({ position: marker });
        this.center = marker;
        this.currentPlace = null;
    });

    console.log(position_data[0].lat)
  },
};
</script>