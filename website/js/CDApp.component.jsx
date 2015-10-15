// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var CDApp = React.createClass({
    propTypes: {
    	value: React.PropTypes.number,
    	filename: React.PropTypes.string,
    	step: React.PropTypes.number
    },
    getDefaultProps: function() {
        return {
        	gender: 2, // 0 = not known, 1 = male, 2 = female, 9 = not applicable
        	filename: '',
        	step: 1 // 1 = choose, 2 = processing, 3 = results, 4 = error
        };
    },
    getInitialState: function() {
        return {
        	gender: this.props.gender,
        	filename: this.props.filename,
        	step: this.props.step,
        	class: 'cdapp -state-' + this.props.step,
        	selection: {},
        	alike: {}
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
    _handleStepChange: function(step) {
        this.setState({
            step: step,
            class: 'cdapp -state-' + step
        });
    },
    _handleSubmit: function() {
        if (this.state.gender !== '' && this.state.filename !== '') {
            this._getResults();
        }
    },
    _getResults: function() {
        this._handleStepChange(2);
        var url = 'TODO';
        /*$.ajax({
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
                this._handleStepChange(0);
            },
            complete: function() {
                this._handleStepChange(3);
            }.bind(this)
        });*/
		/* TEST */
		debugger;
        var selection = { name: 'Peewee Herman', url: 'https://pbs.twimg.com/profile_images/362060137/Pee-wee_Twitter_Profile.png' },
        	alike = { name: 'Donald Trump', url: 'http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg' }
        ;
		this.setState({
			selection: selection,
			alike: alike
		});
		/* TEST */
    },
    render: function() {
        return (
        	<article className={this.state.class}>
	            <section className="choose">
	            	<Form
	            		_handleFilenameChange={this._handleFilenameChange}
	            		_handleGenderChange={this._handleGenderChange}
	            		_handleSubmit={this._handleSubmit}
	            	/>
	            </section>
	            <section className="processing">
	            	LOADING
	            </section>
	            <section className="results">
	            	<Results
	            		step={this.state.step}
	            		selection={this.state.selection}
	            		alike={this.state.alike}
	            	/>
	            </section>
	            <section className="error">
	            	ERROR
	            </section>
	        </article>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

