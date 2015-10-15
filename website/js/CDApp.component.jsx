// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
//
// # IMPApp
// 
// Big wrapper around all of the IMP functionality. Doesn't do too much apart
// from hold the state for the application and handle all of the changes to the
// UI.
// 
// - IMPApp
//   - APIType
//   - Filters
//   - Controls
//   - Thumbnails
//
// Also deals with the loading state and the API calls to get the data.
//
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var CDApp = React.createClass({
    propTypes: {
    	gender: React.PropTypes.string,
    	filename: React.PropTypes.string,
    	loading: React.PropTypes.bool
    },
    getDefaultProps: function() {
        return {
        	// 0 = not known, 1 = male, 2 = female, 9 = not applicable
        	gender: 2,
        	filename: '',
        	loading: false
        };
    },
    getInitialState: function() {
        return {
        	gender: this.props.gender,
        	filename: this.props.filename,
        	loading: this.props.loading,
        };
    },
    _handleGenderChange: function(gender) {
        this.setState({
            gender: gender
        });
    },
    _handleFilenameChange: function(filename) {
        this.setState({
            filename: filename
        });
    },
    _handleLoadingChange: function(loading) {
        this.setState({
            loading: loading
        });
    },
    _handleSubmit: function() {
        if (this.state.gender !== '' && this.state.filename !== '') {
            this._getResults();
        }
    },
    _getResults: function() {
        this._handleLoadingChange(true);
        var url = 'TODO';
        $.ajax({
            crossDomain: true,
            url: url, 
            type: 'GET',
            dataType: 'json',
            jsonp: false,
            data: {
                filename: filename,
                gender: gender
            },
            success: function(data, textStatus, jqXHR) {
                var selection = data.selection,
                	alike = data.alike
                ;
                this.setState({
                    selection: selection,
                    alike: alike
                });
            }.bind(this),
            error: function(qXHR, textStatus, errorThrown) {
                // TODO
            },
            complete: function() {
                this._handleLoadingChange(false);
            }.bind(this)
        });
    },
    render: function() {
        return (
        	<div className="cdapp">
	            <div className="beginning">
	            	GENDER and FILENAME
	            </div>
	            <div className="middle">
	            	LOADING
	            </div>
	            <div className="end">
	            	RESULTS
	            </div>
	        </div>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

