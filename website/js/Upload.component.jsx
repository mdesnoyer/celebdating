// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Upload = React.createClass({
    render: function() {
        return (
        	<div>
	        	<label className="label" htmlFor="file">File</label>
	            <input
	                id="file"
	                name="file"
	                type="file"
	                onChange={this.props._handleFileChange}
	            />
	        </div>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
