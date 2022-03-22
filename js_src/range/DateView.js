import React from 'react';
import { Route, Switch } from 'react-router-dom';

import Loader from 'utils/Loader';
import Loading from 'utils/Loading';

import Schedule from 'range/Schedule';
import SlotBookView from 'range/SlotBookView';
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
        const date = this.props.match.params.date;

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
                <Schedule schedule={ data.schedule.mainRange } date={ date } abFaces={ data.options.abFaces } bRange={ false } />
                <h3 className="date-view__title">Right Range</h3>
                <Schedule schedule={ data.schedule.bRange } date={ date } abFaces={ data.options.abFaces } bRange={ true } />
            </>;
        } else {
            schedule = <Schedule schedule={ data.schedule.mainRange } date={ date } abFaces={ data.options.abFaces } bRange={ false } />;
        }

        return (
            <div className="date-view">
                { title }
                { notes }
                { venue }
                { schedule }
                <Switch>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/book/:time(\d{2}:\d{2})/:range(B)?:target(\d+):face(A|B)?/">
                        <SlotBookView options={ data.options } />
                    </Route>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/cancel/:time(\d{2}:\d{2})/:range(B)?:target(\d+):face(A|B)?/">
                        <SlotCancelView schedule={ data.schedule } />
                    </Route>
                </Switch>
            </div>
        );
    }
}

export default DateView;
