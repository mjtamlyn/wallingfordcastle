import React, { useState } from 'react';

import { Switch, Route, Redirect, Link } from 'react-router-dom';
import BooleanField from 'utils/BooleanField';
import DateInput from 'utils/DateInput';
import FormInput from 'utils/FormInput';
import TextField from 'utils/TextField';
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
    return (
        <>
            <h3>Step 1 - Archer details</h3>
            <form className="form">
                <FormInput value={ entry.name } onChange={ updateEntry('name') } label="Full name" autoFocus={ true } />
                <FormInput value={ entry.agb } onChange={ updateEntry('agb') } label="AGB number" />
                <FormInput value={ entry.club } onChange={ updateEntry('club') } label="Club" />
                <Selector value={ entry.gender } onChange={ updateEntry('gender') } label="Gender" options={ ['Men', 'Women'] } />
                <DateInput value={ entry.dob } onChange={ updateEntry('dob') } label="Date of Birth" />
                <Selector value={ entry.ageGroup } onChange={ updateEntry('ageGroup') } label="Age group" options={ ['50+', 'Adult', 'U21', 'U18', 'U16', 'U15', 'U14', 'U12'] } />
            </form>
            { !entry.page1Valid && <a className="btn btn--disabled">Add archer details</a> }
            { entry.page1Valid && <Link className="btn" to="/enter/entry-information/">Add archer details</Link> }
        </>
    );
};

const EnterModalEntryInformation = ({ tournament, entry, updateEntry }) => {
    if (!entry.page1Valid) {
        return <Redirect to="/enter/archer-details" />;
    }

    const gdprLabel = 'I consent that some of the information here provided will be shared with tournament organisers, scoring systems, other competitors and ArcheryGB. I also consent that I may be contacted with further details of the event via email.';

    return (
        <>
            <h3>Step 2 - Entry information</h3>
            <Link to="/enter/archer-details/">&lt; Back</Link>
            <form className="form">
                <Selector value={ entry.bowstyle } onChange={ updateEntry('bowstyle') } label="Bowstyle" options={ tournament.bowstyles } />
                <Selector value={ entry.round } onChange={ updateEntry('round') } label="Round" options={ tournament.rounds } />
                { (tournament.hasWrs || tournament.hasUkrs) && <BooleanField value={ entry.drugConsent } onChange={ updateEntry('drugConsent') } label="I consent to drugs testing as required under WRS rules." /> }
                <BooleanField value={ entry.gdprConsent } onChange={ updateEntry('gdprConsent') } label={ gdprLabel } />
                <BooleanField value={ entry.marketingConsent } onChange={ updateEntry('marketingConsent') } label="Please contact me about future competitions at Wallingford Castle Archers" />
                <TextField value={ entry.notes } onChange={ updateEntry('notes') } label="Anything else to tell us?" />
            </form>
            <div>TODO: stay on line, novice/intermediate, sessions</div>
            { !entry.page2Valid && <a className="btn btn--disabled">Complete entry</a> }
            { entry.page2Valid && <Link className="btn" to="/enter/payment/">Complete entry</Link> }
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
        round: tournament.rounds.length === 1 ? tournament.rounds[0] : null,
        notes: '',
        drugConsent: false,
        gdprConsent: false,
        marketingConsent: false,

        page1Valid: false,
        page2Valid: false,
    });

    if (close) {
        return <Redirect to="/" />;
    };

    const updateEntry = (name) => {
        return (value) => {
            const updated = { ...pendingEntry };
            updated[name] = value;

            updated.page1Valid = !!(
                updated.name !== '' &&
                updated.agb !== '' &&
                updated.club !== '' &&
                updated.gender &&
                updated.ageGroup
            );
            updated.page2Valid = !!(
                updated.bowstyle &&
                updated.round &&
                ((tournament.hasWrs || tournament.hasUkrs) && updated.drugConsent) &&
                updated.gdprConsent
            );

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
