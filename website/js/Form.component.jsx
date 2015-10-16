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
                <label htmlFor="file">File</label>
                <input
                    id="file"
                    name="file"
                    type="file"
                    value={this.props.file}
                    onChange={this.props._handleFileChange}
                />
                <Thumbnail
                    thumbnail={this.props.thumbnail}
                />
                <Gender 
                    gender={this.props.gender}
                    onChange={this.props._handleGenderChange}
                />
                <input
                    type="submit"
                    value="Match Me"
                />
            </form>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
