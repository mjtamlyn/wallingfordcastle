import React from 'react';
import { Link } from 'react-router-dom';

class SlotBookView extends React.Component {
    render() {
        const { date, target, time } = this.props.match.params;
        const dateUrl = `/${date}/`;

        return (
            <div className="booking-modal">
                <Link to={ dateUrl }>Close</Link>
                <h3>Book</h3>
                <p>Booking target { target } at { time }</p>
            </div>
        );
    }
}

export default SlotBookView;
