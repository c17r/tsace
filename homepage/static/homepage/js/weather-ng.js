
angular.module("WeatherApp", [
    "ngRoute",
    "ngResource"
])
    .constant("moment", moment)

    .config(["$interpolateProvider", "$routeProvider", "$resourceProvider"
        ,function($interpolateProvider, $routeProvider, $resourceProvider) {

            $interpolateProvider.startSymbol("[[");
            $interpolateProvider.endSymbol("]]");

            $resourceProvider.defaults.stripTrailingSlashes = false;

            $routeProvider
                .when("/", {
                    templateUrl: "/static/homepage/js/templates/index.html"
                });

        }
    ])

    .factory("Weather", ["$resource"
        ,function($resource) {
            return $resource(
                '/api/weather/:name/:lat,:lng/'
            );
        }
    ])

    .factory("City", ["$resource"
        ,function($resource) {

            var csrf = lib.GetCookie("csrftoken");

            return $resource(
                '/api/city/:key/',
                {},
                {
                    add: {
                        method: "PUT",
                        isArray: true,
                        headers: {
                            "X-CSRFToken": csrf
                        }
                    },
                    remove: {
                        method: "DELETE",
                        isArray: true,
                        headers: {
                            "X-CSRFToken": csrf
                        }
                    }
                }
            );
        }
    ])

    .directive("weatherEntry", ["$interval", "moment"
        ,function($interval, moment) {

            function link(scope, element, attrs) {

                var timeId;

                function updateTime() {
                    var elem = element.find("[data-tz-offset]");
                    var tz = elem.attr("data-tz-offset");
                    var time = moment().format("hh:mm a DD-MMM");

                    if (tz.indexOf("[[") == -1)
                        time = moment().tz(tz).format("hh:mm a DD-MMM");

                    elem.html(time);
                }
                updateTime();

                element.on("$destroy", function() {
                    $interval.cancel(timeId)
                });


                timeId = $interval(updateTime, 500);

            }

            return {
                restrict: "E",
                scope: {
                    entry: "=",
                    actionCaption: "@",
                    action: "&"

                },
                templateUrl: "/static/homepage/js/templates/_entry.html",
                link: link
            }
        }
    ])

    .directive("searchForm", ["Weather"
        ,function(Weather) {

            function link(scope, element, attrs) {
                var input = element.find("#city_name")[0];
                var placeholder = input.placeholder;

                function cb() {
                    var place = autocomplete.getPlace();

                    if (place.geometry) {
                        var name = lib.RemoveCountryName(place.formatted_address);
                        var lat = lib.round_place(parseFloat(place.geometry.location.A), 4);
                        var lng = lib.round_place(parseFloat(place.geometry.location.F), 4);
                        var coord = {
                            "name": name,
                            "lat": lat,
                            "lng": lng
                        };

                        Weather.get(coord, function(data) {
                            scope.$parent.setWeather(data);
                            input.value = "";
                        })

                    } else {
                        input.placeholder = placeholder;
                    }
                }
                var autocomplete = new google.maps.places.Autocomplete(input, { types: ['(cities)'] });
                google.maps.event.addListener(autocomplete, "place_changed", cb);
            }

            return {
                restrict: "E",
                transclude: true,
                scope: {
                    placeholder: "@"
                },
                templateUrl: "/static/homepage/js/templates/_search-form.html",
                link: link
            }
        }
    ])

    .controller("WeatherController", ["$scope", "City"
        ,function($scope, City) {

            $scope.setWeather = function(data) {
                $scope.result = data;
            }

            $scope.addCity = function(entry) {
                return City.add({key: entry.key}, {}, function(data) {
                    $scope.entries = data;
                    $scope.result = null;
                }).$promise;
            };

            $scope.removeCity = function(entry) {
                return City.remove({key: entry.key}, {}, function(data) {
                    $scope.entries = data;
                }).$promise;
            };

            $scope.result = null;
            $scope.entries = City.query();
        }
    ]);
