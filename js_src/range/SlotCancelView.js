import React from 'react';
import { Link, Redirect, withRouter } from 'react-router-dom';

import Modal from 'utils/Modal';
import store from 'utils/store';

class SlotCancelView extends React.Component {
    constructor(props) {
        super(props);
        const { date, target, face, time, range } = props.match.params;
        this.submitData = { date, target, face, time };
        this.submitData.bRange = (range === 'B');
        this.state = {
            submitting: false,
            done: false,
        };
    }

    close() {
        this.setState({ done: true });
    }

    submit() {
        let data = {
            ...this.submitData,
        }
        this.setState({
            submitting: true,
        }, () => {
            store.send('/api/range/cancel/', data).then((response) => {
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

        const submitDisabled = this.state.submitting;

        return (
            <Modal className="booking-modal" close={ ::this.close }>
                <h4 className="booking-modal__title">Cancel your session?</h4>
                <Link className="booking-modal__close" to={ dateUrl }>Close</Link>
                <p className="booking-modal__text">You are booked for target { this.submitData.target }{ this.submitData.face } at { this.submitData.time }.</p>
                <div className="booking-modal__row">
                    <input className="booking-modal__button" type="submit" value="Confirm" disabled={ submitDisabled } onClick={ ::this.submit } />
                </div>
            </Modal>
        );
    }
};

export default withRouter(SlotCancelView);
