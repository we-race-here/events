function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {lat: -33, lng: 151},
    });

    var marker = new google.maps.Marker({
        map: map,
        draggable: true,
    });

    google.maps.event.addListener(marker, 'dragend', function() {
        document.querySelector('.latitude').value = marker.getPosition().lat();
        document.querySelector('.longitude').value = marker.getPosition().lng();
    });

    map.addListener('click', function(event) {
        marker.setPosition(event.latLng);
        document.querySelector('.latitude').value = event.latLng.lat();
        document.querySelector('.longitude').value = event.latLng.lng();
    });
}
