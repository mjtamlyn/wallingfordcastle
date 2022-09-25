import React from 'react';
import { Route, Switch } from 'react-router-dom';

import Loader from 'utils/Loader';
import Loading from 'utils/Loading';

import DateVenue from 'range/DateVenue';
import SlotAbsenceView from 'range/SlotAbsenceView';
import SlotBookView from 'range/SlotBookView';
import SlotBookAdditionalView from 'range/SlotBookAdditionalView';
import SlotCancelView from 'range/SlotCancelView';

class DateView extends Loader {
    subscribe = true

    getApiEndpoint(props) {
        const date = props.match.params.date;
        return `/api/range/${date}/`;
    }

    renderLoading() {
        const date = this.props.match.params.date;
        return (
            <div className="date-view">
                <h3>{ date }</h3>
                <Loading />
            </div>
        );
    }

    renderLoaded(data) {
        const venues = data.venues;
        if (!venues.length) {
            return <p>No bookings found</p>;
        }
        const venuesEls = venues.map((venue) => {
            return (
                <DateVenue
                    date={ this.props.match.params.date }
                    data={ venue }
                    key={ venue.venue.key }
                />
            );
        });
        return (
            <>
                { venuesEls }
                <Switch>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/book/:venue([a-z-]+)/:time(\d{2}:\d{2})/:range(B)?:target(\d+):face(A|B)?/">
                        <SlotBookView options={ venues[0].options } />
                    </Route>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/cancel/:venue([a-z-]+)/:time(\d{2}:\d{2})/:range(B)?:target(\d+):face(A|B)?/">
                        <SlotCancelView schedule={ data.schedule } />
                    </Route>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/absence/:venue([a-z-]+)/:time(\d{2}:\d{2})/:range(B)?:target(\d+):face(A|B)?/">
                        <SlotAbsenceView schedule={ data.schedule } />
                    </Route>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/book-additional/:venue([a-z-]+)/:time(\d{2}:\d{2})/:range(B)?:target(\d+):face(A|B)?/">
                        <SlotBookAdditionalView schedule={ data.schedule } />
                    </Route>
                </Switch>
            </>
        );
    }
}

export default DateView;
