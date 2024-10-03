function initAutocomplete() {
  let locationField = document.querySelector("#id_location");
  // Create the autocomplete object, restricting the search predictions to
  // addresses in the US and Canada.
  const center = { lat: 43.6918116, lng: -116.4135322 };
  // Create a bounding box with sides ~10km away from the center point
  const defaultBounds = {
    north: center.lat + 0.1,
    south: center.lat - 0.1,
    east: center.lng + 0.1,
    west: center.lng - 0.1,
  };
  const options = {
    bounds: defaultBounds,
    componentRestrictions: { country: ["us",] },
    fields: ["formatted_address", "place_id", "geometry"],
    types: ["address"],
    strictBounds: false,
  };
  autocomplete = new google.maps.places.Autocomplete(locationField, options);
  locationField.focus();
  autocomplete.addListener("place_changed", fillInAddress);
}

function fillInAddress() {
  let placeIdField = document.querySelector("#id_place_id");
  let locationField = document.querySelector("#id_location");
  let pointField = document.querySelector("#id_point");

  // Get the place details from the autocomplete object.
  const place = autocomplete.getPlace();

  placeIdField.value = place.place_id;
  locationField.value = place.formatted_address;

  let lat = place.geometry.location.lat();
  let lon = place.geometry.location.lng();
  pointField.value = `SRID=4326;POINT(${lon} ${lat})`;
}

window.initAutocomplete = initAutocomplete;