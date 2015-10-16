// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Go = React.createClass({
    render: function() {
    	if (this.props.gender !== '' && this.props.thumbnail !== '') {
	        return (
	        	<div className="control -go">
		            <input
		                className="button -primary"
		                type="submit"
		                value="Match Me"
		            />
		        </div>
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
