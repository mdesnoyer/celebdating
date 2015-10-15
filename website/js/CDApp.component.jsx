// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var CDApp = React.createClass({
    propTypes: {
    	value: React.PropTypes.number,
    	file: React.PropTypes.string,
    	step: React.PropTypes.number
    },
    getDefaultProps: function() {
        return {
        	gender: 2, // 0 = not known, 1 = male, 2 = female, 9 = not applicable
        	file: '',
        	step: 1 // 1 = choose, 2 = processing, 3 = results, 4 = error
        };
    },
    getInitialState: function() {
        return {
        	gender: this.props.gender,
        	file: this.props.file,
        	step: this.props.step,
        	class: 'cdapp state-' + this.props.step,
        	selection: {},
        	alike: {}
        };
    },
    _handleGenderChange: function(gender) {
        this.setState({
            gender: gender
        });
    },
    _handleFileChange: function(e) {
        var self = this,
            reader = new FileReader(),
            file = e.target.files[0];
        reader.onload = function(upload) {
            self.setState({
                file: upload.target.result,
            });
        }
        reader.readAsDataURL(file);
    },
    _handleStepChange: function(step) {
        this.setState({
            step: step,
            class: 'cdapp state-' + step
        });
    },
    _handleSubmit: function() {
        if (this.state.gender !== '' && this.state.file !== '') {
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
                file: file,
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
        var selection = { name: 'Peewee Herman', url: 'https://pbs.twimg.com/profile_images/362060137/Pee-wee_Twitter_Profile.png' },
        	alike = { name: 'Donald Trump', url: 'http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg' }
        ;
		this.setState({
			selection: selection,
			alike: alike
		});
        setTimeout(function() {
            this._handleStepChange(3);
        }.bind(this), 2000);
		/* TEST */
    },
    render: function() {
        return (
        	<article className={this.state.class}>
	            <section className="choose">
	            	<Form
	            		_handleFileChange={this._handleFileChange}
	            		_handleGenderChange={this._handleGenderChange}
	            		_handleSubmit={this._handleSubmit}
                        gender={this.state.gender}
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

