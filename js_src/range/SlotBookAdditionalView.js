import React, { useEffect, useState } from 'react';
import { withRouter, Link, Redirect } from 'react-router-dom';

import store from 'utils/store';
import ArcherMultiSelect from 'range/ArcherMultiSelect';
import Modal from 'utils/Modal';

const isValid = ({ archers }) => {
    return !!archers.length;
};

const SlotBookAdditionalView = ({ match }) => {
    const { date, time, venue, range, target,face } = match.params;
    const dateUrl = `/${date}/`;
    const apiArcherUrl = `/api/range/additional-bookable-archers/${date}/${venue}/${time}/${range || ''}${target}${face}/`;
    const apiReportUrl = `/api/range/book-in/${date}/${venue}/${time}/${range || ''}${target}${face}/`;

    const [done, setDone] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [archers, setArchers] = useState([]);

    useEffect(() => {
        if (submitting) {
            store.send(apiReportUrl, { archers }).then((response) => {
                if (response.ok) {
                    store.invalidate(`/api/range/${date}/`);
                    store.invalidate(`/api/range/additional-bookable-archers/${date}/${venue}/${time}/${range || ''}${target}${face}/`);
                    store.invalidate(`/api/range/absentable-archers/${date}/${venue}/${time}/${range || ''}${target}${face}/`);
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
    const submitDisabled = !isValid({ archers }) || submitting;

    return (
        <Modal className="booking-modal" wide close={ close }>
            <h4 className="booking-modal__title">Book Additional Session</h4>
            <Link className="booking-modal__close" to={ dateUrl }>Close</Link>
            <p className="booking-modal__text booking-modal__text--help">
                Archers may attend additional sessions which run at the same level,
                subject to space.  If you are attending multiple sessions in the same
                week, coaches’ first priority will be those who are normally on this
                day.
            </p>
            <div className="booking-modal__row">
                <ArcherMultiSelect onChange={ setArchers } apiEndpoint={ apiArcherUrl } />
            </div>
            <div className="booking-modal__row">
                <input className="booking-modal__button" type="submit" value="Book in" disabled={ submitDisabled } onClick={ submit } />
            </div>
        </Modal>
    );
};

export default withRouter(SlotBookAdditionalView);
