import React from 'react';
import ReactDOM from 'react-dom';

import { BrowserRouter, Switch, Route } from 'react-router-dom';

import NoMatch from 'utils/NoMatch';
import DateSelectorView from 'range/DateSelectorView';
import DateView from 'range/DateView';

const app = document.getElementById('app-range-booking');

class RangeBookingApp extends React.Component {
    render() {
        return (
            <BrowserRouter basename={ 'members/range' }>
                <Switch>
                    <Route exact path="/">
                        <DateSelectorView />
                    </Route>
                    <Route path="/:date(\d{4}-\d{2}-\d{2})/" component={ DateView } />
                    <Route component={ NoMatch } />
                </Switch>
            </BrowserRouter>
        );
    }
}


ReactDOM.render(<RangeBookingApp />, app);
