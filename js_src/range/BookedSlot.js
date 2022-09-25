import React from 'react';
import { Link, withRouter } from 'react-router-dom';

import BookedSlotMenu from 'range/BookedSlotMenu';

const BaseBookedSlot = ({ slot, rowSpan, colSpan, match }) => {
    let cancelLink = null;
    if (slot.editable) {
        const date = match.params.date;
        const linkTarget = `/${date}/cancel/${slot.reference()}/`;
        cancelLink = (
            <Link
                className="range-schedule__cancel"
                to={ linkTarget }
            >
                Cancel
            </Link>
        );
    }

    let title = null;
    if (slot.groupName) {
        title = <p className="range-schedule__title">{ slot.groupName }</p>
    }

    return (
        <td
            className="range-schedule__slot range-schedule__slot--booked"
            rowSpan={ rowSpan }
            colSpan={ colSpan }
        >
            <BookedSlotMenu slot={ slot } date={ match.params.date } />
            { title }
            <p className="range-schedule__description">{ slot.details.names }</p>
            <p className="range-schedule__description">{ slot.details.distance }</p>
            { cancelLink }
        </td>
    );
};

const BookedSlot = withRouter(BaseBookedSlot);

export default BookedSlot;
