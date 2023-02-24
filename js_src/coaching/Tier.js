import React from 'react';

import TierEvent from './TierEvent';


const Tier = ({ tier, planId }) => {
    const events = tier.events.map(ev => <TierEvent ev={ ev } key={ `${ev.date.api} / ${ev.name}` } planId={ planId } />);
    return (
        <div className="event-plan__tier">
            <h3 className="event-plan__heading">{ tier.tierName } - { tier.name }</h3>
            <p className="event-plan__content">{ tier.comments }</p>
            <div className="event-plan__events">
                { events }
            </div>
        </div>
    );
};

export default Tier;
