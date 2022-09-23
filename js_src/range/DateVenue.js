import React from 'react';

import Schedule from 'range/Schedule';

const DateVenue = ({ data, date }) => {
    let title = null;
    let notes = null;
    let venue = null;
    if (data.date.title) {
        title = <h3 className="date-view__title">{ data.date.title }</h3>;
    }
    if (data.date.notes) {
        notes = <p className="date-view__notes">{ data.date.notes }</p>;
    }
    if (data.venue) {
        venue = <p className="date-view__venue"><a href={ data.venue.link }>Directions to { data.venue.name }</a></p>;
    }

    let schedule = null;
    if (data.options.bRange) {
        schedule = <>
            <h3 className="date-view__title">Left Range</h3>
            <Schedule schedule={ data.schedule.mainRange } date={ date } abFaces={ data.options.abFaces } bRange={ false } venue={ data.venue } />
            <h3 className="date-view__title">Right Range</h3>
            <Schedule schedule={ data.schedule.bRange } date={ date } abFaces={ data.options.abFaces } bRange={ true } venue={ data.venue } />
        </>;
    } else {
        schedule = <Schedule schedule={ data.schedule.mainRange } date={ date } abFaces={ data.options.abFaces } bRange={ false } venue={ data.venue } />;
    }

    return (
        <div className="date-view">
            { title }
            { notes }
            { venue }
            { schedule }
        </div>
    );
};

export default DateVenue;
