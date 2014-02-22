/** @jsx React.DOM */

var SearchResults = React.createClass({
   render: function() {
       return (
           <table id="search-result">
               <tr>
                   <td className="name" colSpan="3">{this.props.name}</td>
                   <td className="high">H: {this.props.temp.high}</td>
                   <td className="add" rowSpan="2">
                       <form className="add-city" action="" method="POST">
                           <input name="key" type="hidden" value={this.props.key} />
                           <input type="image" src="/static/homepage/img/plus.png" />
                       </form>
                   </td>
               </tr>
               <tr>
                   <td className="time"><span data-tz-offset={this.props.tz_offset} /></td>
                   <td className="current">{this.props.temp.current}</td>
                   <td className="icon"><img src={"/static/homepage/img/" + this.props.temp.icon + ".png"} /></td>
                   <td className="low">L: {this.props.temp.low}</td>
               </tr>
           </table>
           );
   }
});
