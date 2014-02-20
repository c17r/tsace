/** @jsx React.DOM */

var SearchResults = React.createClass({
   render: function() {
       return (
           <table>
               <tr>
                   <td>{this.props.city_name}</td>
                   <td rowSpan="2">{this.props.current}</td>
                   <td rowSpan="2"><img src={"/static/homepage/img/" + this.props.icon + ".png"} /></td>
                   <td>{this.props.high}</td>
               </tr>
               <tr>
                   <td>{this.props.tz_offset}</td>
                   <td>{this.props.low}</td>
               </tr>
           </table>
           );
   }
});
