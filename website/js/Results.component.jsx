// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Results = React.createClass({
    render: function() {
        if (this.props.step == 3) {
	        return (
	        	<div>
					You should date:
					{this.props.selection.name}
					<img src={this.props.selection.url} title="{this.props.selection.name}" alt="{this.props.selection.name}" />
					You are like:
					{this.props.alike.name}
					<img src={this.props.alike.url} title="{this.props.alike.name}" alt="{this.props.alike.name}" />
				</div>
	        );
	    }
	    else {
	    	return (<div></div>);
	    }
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

