import React, { useState } from 'react';
import { Link, withRouter } from 'react-router-dom';

const BaseBookedSlot = ({ slot, rowSpan, colSpan, match }) => {
    const [menuOpen, setMenuOpen] = useState(false);

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

    let toolsClass = 'range-schedule__tools';
    if (menuOpen) {
        toolsClass += ' range-schedule__tools--active';
    }

    let menu = null;
    if (slot.canReportAbsence) {
        menu = <a className={ toolsClass } onClick={ () => setMenuOpen(!menuOpen) }>Info</a>;
    }

    return (
        <td
            className="range-schedule__slot range-schedule__slot--booked"
            rowSpan={ rowSpan }
            colSpan={ colSpan }
        >
            { menu }
            { menuOpen &&
                <div className="range-schedule__menu">
                    <ul className="range-schedule__menu__list">
                        <li className="range-schedule__menu__item">Report absence</li>
                        <li className="range-schedule__menu__item">Book in</li>
                        <li className="range-schedule__menu__item">View schedule</li>
                    </ul>
                </div>
            }
            { title }
            <p className="range-schedule__description">{ slot.details.names }</p>
            <p className="range-schedule__description">{ slot.details.distance }</p>
            { cancelLink }
        </td>
    );
};

const BookedSlot = withRouter(BaseBookedSlot);

export default BookedSlot;
