//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

/*
// Google Maps Scripts
var map = null;
// When the window has finished loading create our google map below
google.maps.event.addDomListener(window, 'load', init);
google.maps.event.addDomListener(window, 'resize', function() {
    map.setCenter(new google.maps.LatLng(41.380837,2.175884));
});

function init() {
    // Basic options for a simple Google Map
    // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    var myLatLng = new google.maps.LatLng(41.380837, 2.175884);

    var mapOptions = {
        // How zoomed in you want the map to start at (always required)
        zoom: 15,

        // The latitude and longitude to center the map (always required)
        center: myLatLng, 

        // Disables the default Google Maps UI components
        disableDefaultUI: true,
        scrollwheel: false,
        draggable: false

    //     // How you would like to style the map. 
    //     // This is where you would paste any style found on Snazzy Maps.
    //     styles: [{
    //         "featureType": "water",
    //         "elementType": "geometry",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 17
    //         }]
    //     }, {
    //         "featureType": "landscape",
    //         "elementType": "geometry",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 20
    //         }]
    //     }, {
    //         "featureType": "road.highway",
    //         "elementType": "geometry.fill",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 17
    //         }]
    //     }, {
    //         "featureType": "road.highway",
    //         "elementType": "geometry.stroke",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 29
    //         }, {
    //             "weight": 0.2
    //         }]
    //     }, {
    //         "featureType": "road.arterial",
    //         "elementType": "geometry",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 18
    //         }]
    //     }, {
    //         "featureType": "road.local",
    //         "elementType": "geometry",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 16
    //         }]
    //     }, {
    //         "featureType": "poi",
    //         "elementType": "geometry",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 21
    //         }]
    //     }, {
    //         "elementType": "labels.text.stroke",
    //         "stylers": [{
    //             "visibility": "on"
    //         }, {
    //             "color": "#000000"
    //         }, {
    //             "lightness": 16
    //         }]
    //     }, {
    //         "elementType": "labels.text.fill",
    //         "stylers": [{
    //             "saturation": 36
    //         }, {
    //             "color": "#000000"
    //         }, {
    //             "lightness": 40
    //         }]
    //     }, {
    //         "elementType": "labels.icon",
    //         "stylers": [{
    //             "visibility": "off"
    //         }]
    //     }, {
    //         "featureType": "transit",
    //         "elementType": "geometry",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 19
    //         }]
    //     }, {
    //         "featureType": "administrative",
    //         "elementType": "geometry.fill",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 20
    //         }]
    //     }, {
    //         "featureType": "administrative",
    //         "elementType": "geometry.stroke",
    //         "stylers": [{
    //             "color": "#000000"
    //         }, {
    //             "lightness": 17
    //         }, {
    //             "weight": 1.2
    //         }]
    //     }]
    };

    // Get the HTML DOM element that will contain your map 
    // We are using a div with id="map" seen below in the <body>
    var mapElement = document.getElementById('map');

    // Create the Google Map using out element and options defined above
    map = new google.maps.Map(mapElement, mapOptions);

    
    var marker = new google.maps.Marker({
        position: myLatLng,
        title: "Otticode"
    });
    marker.setMap(map);
}*/
