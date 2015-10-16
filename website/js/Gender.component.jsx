// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

var Gender = React.createClass({
    propTypes: {
        gender: React.PropTypes.number.isRequired
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
                <label htmlFor="gender">Gender</label>
                <select
                    id="gender"
                    onChange={this._handleChange}
                    value={this.props.gender}
                >
                    <option value="0">Not Known</option>
                    <option value="1">Male</option>
                    <option value="2">Female</option>
                    <option value="9">Not Applicable</option>
                </select>
            </div>
        );
    }
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 