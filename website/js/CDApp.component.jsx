// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var CDApp = React.createClass({
    propTypes: {
    	gender: React.PropTypes.string,
        pronoun: React.PropTypes.string,
        thumbnail: React.PropTypes.string,
    	step: React.PropTypes.number
    },
    getDefaultProps: function() {
        return {
        	gender: '2', // 0 = not known, 1 = male, 2 = female, 9 = not applicable
            pronoun: 'she',
            thumbnail: '',
        	step: 1 // 1 = choose, 2 = processing, 3 = results, 4 = error
        };
    },
    getInitialState: function() {
        return {
        	gender: this.props.gender,
            pronoun: this.props.pronoun,
            thumbnail: this.props.thumbnail,
        	step: this.props.step,
        	class: 'cdapp state-' + this.props.step,
        	selection: {},
        	alike: {}
        };
    },
    _handleGenderChange: function(gender) {
        var pronoun = '';
        switch (gender) {
            case "0":
                pronoun = 'they';
                break;
            case "1":
                pronoun = 'he';
                break;
            case "2":
                pronoun = 'she';
                break;
            case "3":
                pronoun = 'they';
                break;
        }
        this.setState({
            gender: gender,
            pronoun: pronoun
        });
    },
    _handleFileChange: function(e) {
        var self = this,
            reader = new FileReader(),
            file = e.target.files[0]
        ;
        reader.onload = function(upload) {
            self.setState({
                thumbnail: upload.target.result
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
        if (this.state.gender !== '' && this.state.thumbnail !== '') {
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
        var selection = { name: 'Hillary Clinton', url: 'http://a4.files.biography.com/image/upload/c_fill,cs_srgb,dpr_1.0,g_face,h_300,q_80,w_300/MTE4MDAzNDEwMDU4NTc3NDIy.jpg' },
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
                        thumbnail={this.state.thumbnail}
	            	/>
	            </section>
	            <section className="processing">
                    <div className="control -loading">
	            	  <img src="img/ajax-loader.gif" alt="" title="" />
                    </div>
	            </section>
	            <section className="results">
	            	<Results
	            		step={this.state.step}
	            		selection={this.state.selection}
	            		alike={this.state.alike}
                        pronoun={this.state.pronoun}
	            	/>
	            </section>
	            <section className="error">
	            	<p className="instructions">Sorry, our new service is being upgraded right now. Check back soon.</p>
	            </section>
	        </article>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

