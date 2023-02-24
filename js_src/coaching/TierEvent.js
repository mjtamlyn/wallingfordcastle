import React from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { regular } from '@fortawesome/fontawesome-svg-core/import.macro';

import store from 'utils/store';


const TierEvent = ({ ev, planId }) => {
    let eventType = null;
    if (ev.tournament) {
        eventType = 'WCA hosted competition';
    } else if (ev.clubEvent) {
        eventType = 'WCA hosted informal';
    } else if (ev.clubTrip) {
        eventType = 'WCA club trip';
    } else {
        eventType = 'DIY event';
    }

    let options = (
        <>
            <option value="">{ ev.registration && 'Delete response' || 'Respond...' }</option>
            <option value="definite">Yes, I am definitely attending</option>
            <option value="booked">Yes, I am booked in</option>
            <option value="maybe">I might be attending</option>
            <option value="no">I will not be attending</option>
        </>
    );
    let defaultValue = ev.registration && ev.registration.status.id;
    if (ev.clubTrip) {
        options = (
            <>
                <option value="">{ ev.registration && 'Delete response' || 'Respond...' }</option>
                <option value="definite">Yes, I am definitely attending</option>
                <option value="booked|required">Booked, I need transport</option>
                <option value="booked|interested">Booked, I would like transport for me</option>
                <option value="booked|plus-parent">Booked, I would like transport for me and a parent</option>
                <option value="booked|own-way">Booked, I do not need transport</option>
                <option value="maybe">I might be attending</option>
                <option value="no">I will not be attending</option>
            </>
        );
        if (ev.registration && ev.registration.status.id === 'booked' && ev.registration.wantsTransport) {
            defaultValue = `booked|${ev.registration.wantsTransport.id}`;
        }
    }

    let link = null;
    let linkText = null;
    if (ev.tournament) {
        link = ev.tournament.link;
        linkText = 'Book via club website';
    } else if (ev.clubEvent) {
        link = ev.clubEvent.link;
        linkText = 'Book via club website';
    } else if (ev.entryLink) {
        link = ev.entryLink;
        linkText = 'External booking';
    }

    const register = (e) => {
        const data = {
            status: e.target.value,
        };
        if (data.status.includes('|')) {
            const [stat, transport] = data.status.split('|');
            data.status = stat;
            data.wantsTransport = transport;
        }
        store.send(ev.registrationLink, data).then((response) => {
            if (response.ok) {
                store.invalidate(`/api/coaching/plan/${planId}/`);
            }
        }).catch((error) => {
            console.error('error', error);
        });
    };

    return (
        <div className="event-plan__event">
            <h4 className="event-plan__event__title">
                { ev.name }
                { ev.registration &&
                    <span>
                        <FontAwesomeIcon icon={ regular('circle-check') } className="event-plan__icon" />
                        { ev.registration.status.display } 
                    </span>
                }
            </h4>
            <p className="event-plan__event__date">
                <FontAwesomeIcon icon={ regular('calendar-days') } className="event-plan__icon" fixedWidth />
                { ev.date.pretty }
                { ev.endDate && <> - { ev.endDate.pretty }</>}
            </p>
            <p className="event-plan__event__location">
                <FontAwesomeIcon icon={ regular('map') } className="event-plan__icon" fixedWidth />
                { ev.venue.name }, { ev.venue.postCode }
            </p>
            <p className="event-plan__event__format">
                <FontAwesomeIcon icon={ regular('rectangle-list') } className="event-plan__icon" fixedWidth />
                { eventType } - { ev.eventFormat }
            </p>
            <p className="event-plan__event__format">
                <FontAwesomeIcon icon={ regular('user') } className="event-plan__icon" fixedWidth />
                { ev.ageGroups }
            </p>
            <select className="event-plan__event__registration" defaultValue={ defaultValue } onChange={ register }>
                { options }
            </select>
            { link && <a className="event-plan__event__booking" href={ link }>{ linkText }</a> }
        </div>
    );
};

export default TierEvent;
