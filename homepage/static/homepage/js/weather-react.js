/** @jsx React.DOM */

var SearchResults = React.createClass({
   render: function() {
       return (
           <table id="search-result">
               <tr>
                   <td id="name">{this.props.name}</td>
                   <td id="current" rowSpan="2">{this.props.temp.current}</td>
                   <td id="icon" rowSpan="2"><img src={"/static/homepage/img/" + this.props.temp.icon + ".png"} /></td>
                   <td id="high">{this.props.temp.high}</td>
               </tr>
               <tr>
                   <td id="time"><span data-tz-offset={this.props.tz_offset} /></td>
                   <td id="low">{this.props.temp.low}</td>
               </tr>
           </table>
           );
   }
});
