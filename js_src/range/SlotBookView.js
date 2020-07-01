import React from 'react';
import { Link } from 'react-router-dom';

import ArcherMultiSelect from 'range/ArcherMultiSelect';

class SlotBookView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            archers: [],
            distance: null,
            submitting: false,
        };
    }

    setArchers(archers) {
        this.setState({ archers });
    }

    setDistance(e) {
        this.setState({ distance: e.target.value });
    }

    isValid(state) {
        return (state.archers.length && state.distance);
    }

    submit() {
        console.log('Time to submit!', this.state);
    }

    render() {
        const { date, target, time } = this.props.match.params;
        const dateUrl = `/${date}/`;

        let submitDisabled = !this.isValid(this.state);

        return (
            <div className="booking-modal">
                <Link to={ dateUrl }>Close</Link>
                <h3>Book</h3>
                <p>Booking target { target } at { time }</p>
                <ArcherMultiSelect onChange={ ::this.setArchers } />
                <div>
                    <label htmlFor="id-distance">* Distance:</label>
                    <input id="id-distance" onChange={ ::this.setDistance } />
                </div>
                <input type="submit" value="Book" disabled={ submitDisabled } onClick={ ::this.submit } />
            </div>
        );
    }
}

export default SlotBookView;
