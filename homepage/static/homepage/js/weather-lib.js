
var lib = (function($, moment) {

    function round_place(num, place) {
        var p = Math.pow(10, place);
        return Math.round(num * p)/p;
    }

    function RemoveCountryName(name) {
        var t = name.split(", ");
        t.pop();
        return t.join(", ");
    }

    function HandleTime(timeId) {

        function action() {
            $("[data-tz-offset]").each(function(i) {
                var tz = $(this).attr("data-tz-offset");
                var time = moment().tz(tz).format("hh:mm a DD-MMM");
                this.innerHTML = time;
            });
        }

        if (arguments.length == 0) {
            return setInterval(action, 500);
        }

        return clearInterval(timeId);
    }

    function DisplayAPIError(xhr, textStatus, errorThrown) {
        var msg = textStatus + "\n" + errorThrown;
        alert(msg);
    }

    function RestCall(url, type, data) {
        function getCookie(name) {
            var rtn = null;
            if (!document.cookie || document.cookie == "")
                return null;
            document.cookie.split("; ").forEach(function(crumb) {
                var pieces = crumb.split("=");
                if (pieces[0] == name)
                    rtn = pieces[1];
            });
            return rtn;
        }

        var csrf = getCookie("csrftoken");

        return $.ajax({
            url: url,
            type: type,
            dataType: "json",
            data: data,
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain)
                    xhr.setRequestHeader("X-CSRFToken", csrf)
            }
        })
    }

    return {
        round_place: round_place,
        RemoveCountryName: RemoveCountryName,
        HandleTime: HandleTime,
        DisplayAPIError: DisplayAPIError,
        RestCall: RestCall
    }
})($, moment);










