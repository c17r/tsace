
$(document).ready(function() {

    CitiesDropdown($("#city_name"), GetSearchWeather);

    $("form").submit(function(e) {
        e.preventDefault();
    });

    HandleTime();

})
