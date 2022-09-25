import React, { useEffect, useState } from 'react';
import { withRouter, Link, Redirect } from 'react-router-dom';

import store from 'utils/store';
import ArcherMultiSelect from 'range/ArcherMultiSelect';
import Modal from 'utils/Modal';
import TextField from 'utils/TextField';

const isValid = ({ archers, reason }) => {
    return !!archers.length;
};

const SlotAbsenceView = ({ match }) => {
    const { date, time, venue, range, target,face } = match.params;
    const dateUrl = `/${date}/`;
    const apiArcherUrl = `/api/range/absentable-archers/${date}/${venue}/${time}/${range || ''}${target}${face}/`;
    const apiReportUrl = `/api/range/report-absence/${date}/${venue}/${time}/${range || ''}${target}${face}/`;

    const [done, setDone] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [archers, setArchers] = useState([]);
    const [reason, setReason] = useState('');

    useEffect(() => {
        if (submitting) {
            store.send(apiReportUrl, { archers, reason }).then((response) => {
                if (response.ok) {
                    store.invalidate(`/api/range/${date}/`);
                }
                setSubmitting(false);
                setDone(true);
            }).catch((error) => {
                console.error('error', error);
            });
        }
    }, [submitting]);

    if (done) {
        return <Redirect to={ dateUrl } />;
    }

    const submit = () => setSubmitting(true);
    const close = () => setDone(true);
    const submitDisabled = !isValid({ archers, reason }) || submitting;

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
                <ArcherMultiSelect onChange={ setArchers } apiEndpoint={ apiArcherUrl } />
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
