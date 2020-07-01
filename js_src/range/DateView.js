import React from 'react';
import { Link, Route } from 'react-router-dom';

import Loader from 'utils/Loader';
import Loading from 'utils/Loading';

import Schedule from 'range/Schedule';
import SlotBookView from 'range/SlotBookView';

class DateView extends Loader {
    subscribe = true

    getApiEndpoint() {
        const date = this.props.match.params.date;
        return `/api/range/${date}/`;
    }

    renderLoading() {
        const date = this.props.match.params.date;
        return (
            <div className="date-view">
                <Link to='/'>Back to date selector</Link>
                <h3>{ date }</h3>
                <Loading />
            </div>
        );
    }

    renderLoaded(data) {
        const date = this.props.match.params.date;
        return (
            <div className="date-view">
                <Link to='/'>Back to date selector</Link>
                <h3>{ data.date.pretty }</h3>
                <Schedule schedule={ data.schedule } date={ date } />
                <Route path="/:date(\d{4}-\d{2}-\d{2})/book/:time(\d{2}:\d{2})/:target(\d+)/" component={ SlotBookView } />
            </div>
        );
    }
}

export default DateView;
