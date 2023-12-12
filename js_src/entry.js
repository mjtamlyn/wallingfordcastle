import React from 'react';
import { createRoot } from 'react-dom/client';

import { BrowserRouter, Switch, Route } from 'react-router-dom';

import NoMatch from 'utils/NoMatch';
import DateSelectorView from 'range/DateSelectorView';
import DateView from 'range/DateView';
import PlanView from 'coaching/PlanView';
import TournamentEntry from 'tournaments/TournamentEntry';

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
    const rangeRoot = createRoot(rangeApp);
    rangeRoot.render(<RangeBookingApp />, rangeApp);
}

const eventPlanApp  = document.getElementById('app-event-plan');

if (eventPlanApp) {
    const planId = eventPlanApp.dataset.plan;
    const planRoot = createRoot(eventPlanApp);
    planRoot.render(<PlanView planId={ planId } />, eventPlanApp);
}

const tournamentEntryApp = document.getElementById('app-tournament-entry');
if (tournamentEntryApp) {
    const tournamentId = tournamentEntryApp.dataset.tournament;
    const tournamentRoot = createRoot(tournamentEntryApp);
    tournamentRoot.render(<TournamentEntry tournamentId={ tournamentId } />);
}
