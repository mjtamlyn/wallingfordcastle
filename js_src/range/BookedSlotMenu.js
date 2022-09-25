import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';

import useClickOff from 'utils/useClickOff';

const BookedSlotMenu = ({ slot, date }) => {
    const [menuOpen, setMenuOpen] = useState(false);
    const ref = useRef(null);

    const menuToggle = () => {
        setMenuOpen(!menuOpen);
    };
    useClickOff(ref, () => {
        setMenuOpen(false);
    });

    let opener = null;
    let tools = [];

    if (slot.canReportAbsence) {
        tools.push(
            <Link key="absence" className="range-schedule__menu__item" to={ `/${date}/absence/${slot.reference()}/` }>
                Report absence
            </Link>
        );
    }
    // <li className="range-schedule__menu__item">Book in</li>
    // <li className="range-schedule__menu__item">View schedule</li>

    let toolsClass = 'range-schedule__tools';
    if (menuOpen) {
        toolsClass += ' range-schedule__tools--active';
    }

    if (!tools.length) {
        return null;
    }

    return (
        <div ref={ ref }>
            <a className={ toolsClass } onClick={ menuToggle }>Info</a>
            { menuOpen &&
                <div className="range-schedule__menu">
                    { tools }
                </div>
            }
        </div>
    );
};

export default BookedSlotMenu;