import React from 'react';

import Loader from 'utils/Loader';

class SlotBookAdditionalInfo extends Loader {
    getApiEndpoint() {
        const { date, time, venue, range, target,face } = this.props.match.params;
        return `/api/range/group-booking-info/${date}/${venue}/${time}/${range || ''}${target}${face}/`;
    }

    renderLoaded(data) {
        if (data.booked >= data.maxBookable) {
            return (
                <p className="booking-modal__text">
                    This session is now full, please do not book it.
                </p>
            );
        } else if (data.booked >= data.maxShooting) {
            return (
                <p className="booking-modal__text">
                    You can book in for this session, but all the targets are
                    allocated so you may not be able to shoot. Skills and drills,
                    strength and conditioning and equipment areas should still be
                    available.
                </p>
            );
        }
        return null;
    }
}

export default SlotBookAdditionalInfo;
