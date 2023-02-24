import React from 'react';
import ReactDOM from 'react-dom';

import { BrowserRouter, Switch, Route } from 'react-router-dom';

import NoMatch from 'utils/NoMatch';
import DateSelectorView from 'range/DateSelectorView';
import DateView from 'range/DateView';
import PlanView from 'coaching/PlanView';
import initTournamentEntry from 'tournamentEntry';

const rangeApp = document.getElementById('app-range-booking');

const RangeBookingApp = () => {
    return (
        <BrowserRouter basename={ 'members/range' }>
            <DateSelectorView />
            <Switch>
                <Route exact path="/"></Route>
                <Route path="/:date(\d{4}-\d{2}-\d{2})/" component={ DateView } />
                <Route component={ NoMatch } />
            </Switch>
        </BrowserRouter>
    );
}

if (rangeApp) {
    ReactDOM.render(<RangeBookingApp />, rangeApp);
}

const eventPlanApp  = document.getElementById('app-event-plan');

if (eventPlanApp) {
    const planId = eventPlanApp.dataset.plan;
    ReactDOM.render(<PlanView planId={ planId } />, eventPlanApp);
}

const tournamentEntry = document.getElementById('tournament-entry');
if (tournamentEntry) {
    initTournamentEntry(tournamentEntry);
}
