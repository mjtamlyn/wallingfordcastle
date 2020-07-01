import React from 'react';
import { Link } from 'react-router-dom';

class DateSelector extends React.Component {
    render() {
        const dates = this.props.dates.map((date) => {
            return (<Link to={ '/' + date.api + '/' } key={ date.api }>{ date.pretty }</Link>);
        });
        return (
            <div className="date-selector">
                <h3>Pick a date</h3>
                { dates }
            </div>
        );
    }
}

export default DateSelector;
