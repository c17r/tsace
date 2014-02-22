
$(document).ready(function() {

    CitiesDropdown($("#city_name"), GetSearchWeather);

    $("form.search-city").submit(function(e) {
        e.preventDefault();
    });

    $("div#search-c").on("submit", "form.add-city", function(e) {
        AddCity(this);
        e.preventDefault();
    });

    $("div#saved-c").on("submit", "form.remove-city", function(e) {
        RemoveCity(this);
        e.preventDefault();
    });

    HandleTime();

})
