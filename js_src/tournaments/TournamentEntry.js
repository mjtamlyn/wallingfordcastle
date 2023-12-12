import React from 'react';

import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';

import Loading from '../utils/Loading';
import useQuery from '../utils/useQuery';

import EnterModal from './EnterModal';

const EnterButton = () => {
    return (
        <>
            <h3 className="no-border">Entry is open</h3>
            <Link className="btn" to="/enter/">Enter</Link>
        </>
    );
};

const TournamentEntry = ({ tournamentId }) => {
    const [data, loading] = useQuery(`/api/tournaments/${tournamentId}/`);

    if (loading) {
        return <Loading />;
    }

    return (
        <BrowserRouter basename={ data.tournament.baseUrl }>
            <EnterButton />
            <Switch>
                <Route path="/enter/" render={ () => {
                    return <EnterModal tournament={ data.tournament } />
                } } />
            </Switch>
        </BrowserRouter>
    );
};

export default TournamentEntry;
