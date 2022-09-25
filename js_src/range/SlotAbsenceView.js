import React, { useState } from 'react';
import { withRouter, Link, Redirect } from 'react-router-dom';

import ArcherMultiSelect from 'range/ArcherMultiSelect';
import Modal from 'utils/Modal';
import TextField from 'utils/TextField';

const SlotAbsenceView = ({ match }) => {
    const [done, setDone] = useState(false);
    const [archers, setArchers] = useState([]);
    const [reason, setReason] = useState('');

    const { date } = match.params;
    const dateUrl = `/${date}/`;

    if (done) {
        return <Redirect to={ dateUrl } />;
    }

    const submit = () => {};
    const close = () => setDone(true);
    const submitDisabled = false;

    return (
        <Modal className="booking-modal" wide close={ close }>
            <h4 className="booking-modal__title">Report Absence</h4>
            <Link className="booking-modal__close" to={ dateUrl }>Close</Link>
            <p className="booking-modal__text booking-modal__text--help">
                Thanks for letting us know you won’t be able to attend this session. It
                helps make sure that sessions can be planned effectively, as well as
                allowing as many people as possible to make use of the facilities.  You
                can add a message for the coache(es) below if you have anything to pass on.
            </p>
            <div className="booking-modal__row">
                <ArcherMultiSelect onChange={ setArchers } />
            </div>
            <div className="booking-modal__row">
                <TextField label="Message (optional):" onChange={ setReason } />
            </div>
            <div className="booking-modal__row">
                <input className="booking-modal__button" type="submit" value="Report Absence" disabled={ submitDisabled } onClick={ submit } />
            </div>
        </Modal>
    );
};

export default withRouter(SlotAbsenceView);
