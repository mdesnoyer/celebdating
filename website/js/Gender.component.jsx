// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Gender = React.createClass({
    propTypes: {
        gender: React.PropTypes.string.isRequired
    },
    _handleChange: function(e) {
        this.props.onChange(
            e.target.value
        );
    },
    render: function() {
        // 0 = not known, 1 = male, 2 = female, 9 = not applicable
        return (
            <div className="control -gender">
                <label className="label" htmlFor="gender">I am interested in dating </label>
                <select
                    id="gender"
                    onChange={this._handleChange}
                    value={this.props.gender}
                    className="dropdown"
                >
                    <option value="0">Either</option>
                    <option value="1">Men</option>
                    <option value="2">Women</option>
                </select>
            </div>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 