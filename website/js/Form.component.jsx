// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Form = React.createClass({
    _handleSubmit: function(e) {
        e.preventDefault();
        this.props._handleSubmit();
    },
    render: function() {
        return (
            <form
                onSubmit={this._handleSubmit}
            >
                <legend className="instructions">Upload a photo of yourself and we&rsquo;ll tell you which celebrity you match with based on who they&rsquo;ve dated.</legend>
                <Upload
                    _handleFileChange={this.props._handleFileChange}
                    thumbnail={this.props.thumbnail}
                />
                <Thumbnail
                    thumbnail={this.props.thumbnail}
                />
                <Gender 
                    gender={this.props.gender}
                    onChange={this.props._handleGenderChange}
                />
                <Go
                    gender={this.props.gender}
                    thumbnail={this.props.thumbnail}
                />
            </form>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
