// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Results = React.createClass({
    render: function() {
        if (this.props.step == 3) {
			var alikeStyle = {
				backgroundImage: 'url(' + this.props.alike.url + ')'
			},
			selectionStyle = {
				backgroundImage: 'url(' + this.props.selection.url + ')'
			}
	        return (
	        	<div>
		        	<div className="control -results">
						<h2 className="beta"><b>{this.props.selection.name}</b> would want to date you!</h2>
						<div className="clearfix">
							<div className="verso">
								<small className="tops">&nbsp;</small>
								<figure className="reveal" style={selectionStyle} title={this.props.selection.name} alt={this.props.selection.name} />
								<small className="bottoms">&nbsp;</small>
							</div>
							<div className="recto">
								<small className="tops">Because {this.props.pronoun} dated</small>
								<figure className="reveal" style={alikeStyle} title={this.props.alike.name} alt={this.props.alike.name} />
								<small className="bottoms">{this.props.alike.name}</small>
							</div>
						</div>
					</div>

					<div className="control -share">Sharing Buttons to go here</div>
				</div>
	        );
	    }
	    else {
	    	return (<div></div>);
	    }
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

