import React from 'react';
import { Link } from 'react-router-dom';

import ArcherMultiSelect from 'range/ArcherMultiSelect';

class SlotBookView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            archers: [],
        };
    }

    setArchers(archers) {
        this.setState({ archers });
    }

    render() {
        const { date, target, time } = this.props.match.params;
        const dateUrl = `/${date}/`;

        return (
            <div className="booking-modal">
                <Link to={ dateUrl }>Close</Link>
                <h3>Book</h3>
                <p>Booking target { target } at { time }</p>
                <ArcherMultiSelect onChange={ ::this.setArchers } />
            </div>
        );
    }
}

export default SlotBookView;
