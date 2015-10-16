// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Thumbnail = React.createClass({
    render: function() {
        if (this.props.thumbnail) {
	        return (
	        	<img className="thumbnail" src={this.props.thumbnail} alt="Your upload" title="Your upload" />
	        );
	    }
	    else {
	    	return (<span></span>);
	    }
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

