// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Go = React.createClass({
    render: function() {
    	if (this.props.gender !== '' && this.props.thumbnail !== '') {
	        return (
	            <input
	                className="primary"
	                type="submit"
	                value="Match Me"
	            />
	        );
    	}
    	else {
    		return (
	            <span></span>
	        );
	    }
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
