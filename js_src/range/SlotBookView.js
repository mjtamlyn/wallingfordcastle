import React from 'react';
import { Link, Redirect } from 'react-router-dom';

import store from 'utils/store';
import ArcherMultiSelect from 'range/ArcherMultiSelect';
import DistanceSelector from 'range/DistanceSelector';

class SlotBookView extends React.Component {
    constructor(props) {
        super(props);
        const { date, target, time } = props.match.params;
        this.submitData = { date, target, time };
        this.state = {
            archers: [],
            distance: null,
            submitting: false,
            done: false,
        };
    }

    setArchers(archers) {
        this.setState({ archers });
    }

    setDistance(distance) {
        this.setState({ distance });
    }

    isValid(state) {
        return (state.archers.length && state.distance);
    }

    submit() {
        let data = {
            archers: this.state.archers,
            distance: this.state.distance,
            ...this.submitData,
        }
        this.setState({
            submitting: true,
        }, () => {
            store.send('/api/range/book/', data).then((response) => {
                if (response.ok) {
                    store.invalidate(`/api/range/${data.date}/`);
                }
                this.setState({ submitting: false, done: true });
            }).catch((error) => {
                console.error('error', error);
            });
        });
    }

    render() {
        const { date, target, time } = this.props.match.params;
        const dateUrl = `/${date}/`;

        if (this.state.done) {
            return <Redirect to={ dateUrl } />;
        }

        let submitDisabled = !this.isValid(this.state) && !this.state.submitting;

        return (
            <div className="booking-modal">
                <div className="booking-modal__content">
                    <h4 className="booking-modal__title">Booking target { target } at { time }</h4>
                    <Link className="booking-modal__close" to={ dateUrl }>Close</Link>
                    <div className="booking-modal__row">
                        <ArcherMultiSelect onChange={ ::this.setArchers } />
                    </div>
                    <div className="booking-modal__row">
                        <DistanceSelector onChange={ ::this.setDistance } />
                    </div>
                    <div className="booking-modal__row">
                        <input className="booking-modal__button" type="submit" value="Book" disabled={ submitDisabled } onClick={ ::this.submit } />
                    </div>
                </div>
            </div>
        );
    }
}

export default SlotBookView;
