import React from 'react';
import ReactDOM from 'react-dom';

import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
import deepForEach from 'deep-for-each';

import models from 'range/models';

const app = document.getElementById('app-range-booking');

class DateSelector extends React.Component {
    render() {
        const dates = this.props.dates.map((date) => {
            return (<Link to={ '/' + date.api + '/' } key={ date.api }>{ date.pretty }</Link>);
        });
        return (
            <div className="date-selector">
                <h3>Pick a date</h3>
                { dates }
            </div>
        );
    }
}


class Loading extends React.Component {
    render() {
        return (
            <div className="loading">Loading</div>
        );
    }
}

class Loader extends React.Component {
    constructor(props) {
        super(props);
        this.store = null;
        this.state = { loaded: false };
    }

    componentDidMount() {
        fetch(this.apiEndpoint)
            .then(response => response.json())
            .then((rawData) => {
                deepForEach(rawData, (value, key, subject) => {
                    if (value.__type) {
                        subject[key] = new models[value.__type](value);
                    }
                });
                return rawData;
            })
            .then((data) => {
                this.store = data;
                this.setState({ loaded: true });
            });
    }

    renderLoaded(data) {
        return (<p>Unimplemented renderLoaded!</p>);
    }

    render() {
        if (!this.store) {
            return (<Loading />);
        }
        return this.renderLoaded(this.store);
    }
}


class DateSelectorView extends Loader {
    apiEndpoint = '/api/range/';

    renderLoaded(data) {
        return (
            (<DateSelector dates={ data.dates } />)
        )
    }
}

class DateView extends React.Component {
    render() {
        return (
            <div className="date-view">
                <Link to='/'>Back to date selector</Link>
                <h3>{ this.props.match.params.date }</h3>
            </div>
        );
    }
}

class NoMatch extends React.Component {
    render() {
        return (
            <h2>Oops - Page not found</h2>
        );
    }
}

class RangeBookingApp extends React.Component {
    render() {
        return (
            <BrowserRouter basename={ 'members/range' }>
                <Switch>
                    <Route exact path="/">
                        <DateSelectorView />
                    </Route>
                    <Route exact path="/:date(\d{4}-\d{2}-\d{2})/" component={ DateView } />
                    <Route component={ NoMatch } />
                </Switch>
            </BrowserRouter>
        );
    }
}


ReactDOM.render(<RangeBookingApp />, app);
