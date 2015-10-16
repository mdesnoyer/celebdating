// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Upload = React.createClass({
	_handleSecondaryClick: function() {
 		file.click();
	},
    render: function() {
    	if (this.props.thumbnail == '') {
	        return (
	        	<div className="control -upload">
	        		<button
	        			className="button -secondary"
	        			onClick={this._handleSecondaryClick}
	        		>Browse for Image</button>
		        	<label className="label visuallyhidden" htmlFor="file">File</label>
		            <input
		            	className="visuallyhidden"
		                id="file"
		                name="file"
		                type="file"
		                onChange={this.props._handleFileChange}
		            />
		        </div>
	        );
	    }
	    else {
	    	return (<span></span>);
	    }
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
