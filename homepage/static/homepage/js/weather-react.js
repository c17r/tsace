
var WeatherForm = React.createClass({

    childContextTypes: {
        addCity: React.PropTypes.func,
        removeCity: React.PropTypes.func,
        getWeather: React.PropTypes.func
    },

    getChildContext: function() {
        return {
            addCity: this.addCity,
            removeCity: this.removeCity,
            getWeather: this.getWeather
        };
    },

    getInitialState: function() {
        return {
            search: "Enter a City",
            result: {},
            cities: []
        }
    },

    componentDidMount: function() {
        var _this = this;

        lib.RestCall("/api/city/", "GET")
            .done(function(data) {
                _this.setState({
                    cities: data
                });
            })
            .fail(lib.DisplayAPIError);

        this.timer = lib.HandleTime();
    },

    componentWillUnmount: function() {
        lib.HandleTime(this.timer);
    },

    addCity: function(key) {
        var _this = this;

        return this.cityAction(key, "PUT")
            .done(function() {
                _this.setState({
                    result: {}
                });
            });
    },

    removeCity: function(key) {
        return this.cityAction(key, "DELETE");
    },

    cityAction: function(key, method) {
        var _this = this;

        return lib.RestCall(
            "/api/city/" + key + "/",
            method
        ).done(function(data) {
                _this.setState({
                    cities: data
                });
            })
            .fail(lib.DisplayAPIError)
    },

    getWeather: function(coord) {
        var _this = this;
        var url = "/api/weather/";

        url += coord.name + "/";
        url += coord.lat + "," + coord.lng + "/";

        return lib.RestCall(url, "GET")
            .done(function(data) {
                _this.setState({
                    search: "Enter a City",
                    result: data
                });
            })
            .fail(lib.DisplayAPIError);
    },

    render: function() {
        return (
                <div id="weather-c">
                    <div id="my-weather-c">
                        <SearchForm search={this.state.search} />
                    </div>
                    <SearchResult result={this.state.result} />

                    <span id="saved-h">Saved Cities:</span>
                    <SavedCities cities={this.state.cities} />

                    <div id="recent-searches-c">
                    </div>
                </div>
            );
    }
});

var SearchForm = React.createClass({

    contextTypes: {
        getWeather: React.PropTypes.func
    },

    componentDidMount: function() {
        var _this = this;
        var $node = $(this.getDOMNode(this));
        var input = $node.find("#city_name")[0];
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

                _this.context.getWeather(coord)
                    .done(function() {
                        input.value = "";
                    })
            } else {
                input.placeholder = placeholder;
            }
        }

        var autocomplete = new google.maps.places.Autocomplete(input, { types: ['(cities)'] });
        google.maps.event.addListener(autocomplete, "place_changed", cb);
    },

    formSubmit: function(e) {
        e.preventDefault();
    },

    render: function() {
       return (
           <div id="form-c">
               <form className="search-city" onSubmit={this.formSubmit}>
                   <input id="city_name" type="text" placeholder={this.props.search} />
               </form>
           </div>
           );
    }
});

var SearchResult = React.createClass({
    render: function() {
        if ($.isEmptyObject(this.props.result))
            return (
                <div id="search-c"></div>
                );

        return (
            <div id="search-c">
               <WeatherEntry action="add" key={this.props.result.key} entry={this.props.result} />
            </div>
           );
    }
});

var SavedCities = React.createClass({
    render: function() {
       return (
           <div id="saved-c">
           {this.props.cities.map(function(item) {
               return (
                   <WeatherEntry action="remove" key={item.key} entry={item} />
                   );
           })}
           </div>
           );
   }
});

var WeatherEntry = React.createClass({

    contextTypes: {
        addCity: React.PropTypes.func,
        removeCity: React.PropTypes.func
    },

    actionClick: function() {
        var action = null;
        var $node = $(this.getDOMNode(this));

        switch(this.props.action) {
            case "remove":
                action = this.context.removeCity;
                break;
            case "add":
                action = this.context.addCity;
                break;
        }

        if (action) {
            $node.block({ message: null });
            action(this.props.entry.key)
                .always(function() {
                    $node.unblock();
                })
        }
    },

    render: function() {
        var tz = this.props.entry.tz_offset;
        var time = moment().tz(tz).format("hh:mm a DD-MMM");
        return (
            <table>
                <tr>
                    <td className="name" colSpan="3">{this.props.entry.name}</td>
                    <td className="high">H: {this.props.entry.temp.high}</td>
                    <td className="action" rowSpan="3">
                        <img
                            src={"/static/homepage/img/" + this.props.action + ".png"}
                            onClick={this.actionClick}
                        />
                    </td>
                </tr>
                <tr>
                    <td className="time"><span data-tz-offset={this.props.entry.tz_offset}>{time}</span></td>
                    <td className="current">{this.props.entry.temp.current}</td>
                    <td className="icon"><img src={"/static/homepage/img/" + this.props.entry.temp.icon + ".png"} /></td>
                    <td className="low">L: {this.props.entry.temp.low}</td>
                </tr>
                <tr>
                    <td colSpan="2">&nbsp;</td>
                    <td className="summary">{this.props.entry.temp.summary}</td>
                    <td>&nbsp;</td>
                </tr>
            </table>
            );
    }
});

React.render(
    <WeatherForm />,
    document.getElementById("content")
);
