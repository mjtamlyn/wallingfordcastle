import React from 'react';

class DateView extends React.Component {
    render() {
        return (
            <div className="date-view">
                <Link to='/'>Back to date selector</Link>
                <h3>{ this.props.match.params.date }</h3>
            </div>
        );
    }
}

export default DateView;
