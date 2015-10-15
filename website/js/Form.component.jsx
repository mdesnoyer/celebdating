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
                <label htmlFor="filename">Filename</label>
                <input
                    id="filename"
                    name="filename"
                    type="file"
                    value={this.props.filename}
                    onChange={this.props._handleFilenameChange}
                />
                <Gender 
                    value={this.props.gender}
                    onChange={this.props._handleGenderChange}
                />
                <input
                    type="submit"
                    value="Search"
                />
            </form>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
