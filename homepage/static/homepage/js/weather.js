
$(document).ready(function() {

    CitiesDropdown($("#city_name"), GetCityWeather);

    $("form").submit(function(e) {
        e.preventDefault();
    });

})