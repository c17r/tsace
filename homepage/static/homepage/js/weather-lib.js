
function round_place(num, place) {
    var p = Math.pow(10, place);
    return Math.round(num * p)/p;
}

function GetSearchWeather(coord) {
    $.getJSON("/api/weather", coord).done(DisplaySearchWeather)
}

function DisplaySearchWeather(data) {
    React.renderComponent(
        SearchResults(data),
        document.getElementById("search-c")
    )
}

function RemoveCountryName(name) {
    var t = name.split(", ");
    t.pop();
    return t.join(", ");
}

function CitiesDropdown($input, cityChangedFunc) {
    var input = $input[0];
    var placeholder = input.placeholder;

    function inner_callback() {
        var place = autocomplete.getPlace();

        if (place.geometry) {
            var name = RemoveCountryName(place.formatted_address);
            var lat = round_place(parseFloat(place.geometry.location.d), 4);
            var lng = round_place(parseFloat(place.geometry.location.e), 4);
            var coord = {
                "name": name,
                "lat": lat,
                "lng": lng
            };

            cityChangedFunc(coord);
        }
        else
            input.placeholder = placeholder;
    }

    var autocomplete = new google.maps.places.Autocomplete(input, { types: ['(cities)'] });
    google.maps.event.addListener(autocomplete, "place_changed", inner_callback);
}

function HandleTime() {
    $("[data-tz-offset]").each(function(i) {
        var tz = $(this).attr("data-tz-offset");
        var time = moment().tz(tz).format("hh:mm a DD-MMM");
        this.innerHTML = time;
    })

    setTimeout(HandleTime, 500);
}
