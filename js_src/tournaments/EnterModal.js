import React, { useState } from 'react';

import { Switch, Route, Redirect, Link } from 'react-router-dom';
import FormInput from 'utils/FormInput';
import Selector from 'utils/Selector';
import Modal from 'utils/Modal';


const EnterModalEntryList = ({ entries }) => {
    if (!entries.length) {
        return <Redirect to="/enter/archer-details/" />;
    }
    return (
        <>
            <h3>Entry list</h3>
            <div>Entries go here</div>
        </>
    );
};

const EnterModalArcherDetails = ({ tournament, entry, updateEntry }) => {
    const isValid = !!(
        entry.name !== '' &&
        entry.agb !== '' &&
        entry.club !== '' &&
        entry.gender &&
        entry.ageGroup
    );

    return (
        <>
            <h3>Step 1 - Archer details</h3>
            <form className="form">
                <FormInput value={ entry.name } setValue={ updateEntry('name') } label="Full name" autoFocus={ true } />
                <FormInput value={ entry.agb } setValue={ updateEntry('agb') } label="AGB number" />
                <FormInput value={ entry.club } setValue={ updateEntry('club') } label="Club" />
                <Selector value={ entry.gender } onChange={ updateEntry('gender') } label="Gender" options={ ['Men', 'Women'] } />
                <Selector value={ entry.ageGroup } onChange={ updateEntry('ageGroup') } label="Age group" options={ ['50+', 'Adult', 'U21', 'U18', 'U16', 'U15', 'U14', 'U12'] } />
            </form>
            { !isValid && <a className="btn btn--disabled">Add archer details</a> }
            { isValid && <Link className="btn" to="/enter/entry-information/">Add archer details</Link> }
        </>
    );
};

const EnterModalEntryInformation = ({ tournament, entry, updateEntry }) => {
    return (
        <>
            <h3>Step 2 - Entry information</h3>
            <Link to="/enter/archer-details/">&lt; Back</Link>
            <form className="form">
                <Selector value={ entry.bowstyle } onChange={ updateEntry('bowstyle') } label="Bowstyle" options={ tournament.bowstyles } />
            </form>
            <div>Round, stay on line, notes, drug consent, GDPR</div>
            <Link to="/enter/payment/">Next</Link>
        </>
    );
};

const EnterModalPayment = () => {
    return (
        <>
            <h3>Step 3 - Payment</h3>
            <Link to="/enter/">Pay</Link>
            <div>Or</div>
            <Link to="/enter/archer-details/">Add another</Link>
        </>
    );
};


const EnterModal = ({ tournament }) => {
    const [close, setClose] = useState(false);
    const [pendingEntry, setPendingEntry] = useState({
        name: '',
        agb: '',
        club: '',
        gender: null,
        ageGroup: null,
        bowstyle: null,
    });

    console.log(pendingEntry);

    if (close) {
        return <Redirect to="/" />;
    };

    const updateEntry = (name) => {
        return (value) => {
            const updated = { ...pendingEntry };
            updated[name] = value;
            setPendingEntry(updated);
        };
    };

    return (
        <Modal wide close={ () => setClose(true) } className="modal--tournament-entry">
            <h2>Enter</h2>
            <Switch>
                <Route path="/enter/archer-details/" render={ () => {
                    return <EnterModalArcherDetails tournament={ tournament } entry={ pendingEntry } updateEntry={ updateEntry } />
                } } />
                <Route path="/enter/entry-information/" render={ () => {
                    return <EnterModalEntryInformation tournament={ tournament } entry={ pendingEntry } updateEntry={ updateEntry } />
                } } />
                <Route path="/enter/payment/" component={ EnterModalPayment } />
                <Route path="" exact render={ () => {
                    return <EnterModalEntryList entries={ [] } />
                } } />
            </Switch>
        </Modal>
    );
};

export default EnterModal;
