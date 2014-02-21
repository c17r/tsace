/** @jsx React.DOM */

var SearchResults = React.createClass({
   render: function() {
       return (
           <table>
               <tr>
                   <td>{this.props.name}</td>
                   <td rowSpan="2">{this.props.temp.current}</td>
                   <td rowSpan="2"><img src={"/static/homepage/img/" + this.props.temp.icon + ".png"} /></td>
                   <td>{this.props.temp.high}</td>
               </tr>
               <tr>
                   <td>{this.props.tz_offset}</td>
                   <td>{this.props.temp.low}</td>
               </tr>
           </table>
           );
   }
});
