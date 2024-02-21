import React from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid, regular } from '@fortawesome/fontawesome-svg-core/import.macro';


const EventCalendar = ({ tracks }) => {
    const events = [];
    tracks.forEach((track) => {
        track.events.forEach((ev) => {
            const e = { ...ev, tier: track.tierName };
            e.date.compare = new Date(e.date.api);
            events.push(e);
        });
    });
    events.sort((e1, e2) => e1.date.compare > e2.date.compare ? 1 : -1);

    const formattedEvents = events.map((ev) => {
        return (
            <React.Fragment key={ `${ev.date} / ${ev.name}` }>
                <div className="event-plan__calendar__date">
                    <FontAwesomeIcon icon={ regular('calendar-days') } className="event-plan__icon" />
                    { ev.date.pretty }
                    { ev.endDate && <> - { ev.endDate.pretty }</>}
                </div>
                <div className="event-plan__calendar__tier">
                    <FontAwesomeIcon icon={ solid('layer-group') } className="event-plan__icon" />
                    { ev.tier }
                </div>
                <div className="event-plan__calendar__format">
                    <FontAwesomeIcon icon={ regular('rectangle-list') } className="event-plan__icon" />
                    { ev.eventFormat }
                </div>
                <div className="event-plan__calendar__location">
                    <FontAwesomeIcon icon={ regular('map') } className="event-plan__icon" />
                    { ev.venue.name }, { ev.venue.postCode }
                </div>
                <div className="event-plan__calendar__name">
                    { ev.name }
                </div>
            </React.Fragment>
        );
    });

    return (
        <div className="event-plan__calendar">{ formattedEvents }</div>
    );
};

export default EventCalendar;
