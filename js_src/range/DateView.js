import React from 'react';
import { Link } from 'react-router-dom';

import Loader from 'utils/Loader';
import Loading from 'utils/Loading';

import Schedule from 'range/Schedule';

class DateView extends Loader {
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
        return (
            <div className="date-view">
                <Link to='/'>Back to date selector</Link>
                <h3>{ data.date.pretty }</h3>
                <Schedule schedule={ data.schedule } />
            </div>
        );
    }
}

export default DateView;
