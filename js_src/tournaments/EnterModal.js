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

const EnterModalArcherDetails = ({ tournament }) => {
    const [name, setName] = useState('');
    const [agb, setAgb] = useState('');
    const [club, setClub] = useState('');
    const [gender, setGender] = useState(null);
    const [bowstyle, setBowstyle] = useState(null);
    const [ageGroup, setAgeGroup] = useState(null);

    return (
        <>
            <h3>Step 1 - Archer details</h3>
            <form className="form">
                <FormInput value={ name } setValue={ setName } label="Name" autoFocus={ true } />
                <FormInput value={ agb } setValue={ setAgb } label="AGB Number" />
                <FormInput value={ club } setValue={ setClub } label="Club" />
                <Selector value={ gender } onChange={ setGender } label="Gender" options={ ['Men', 'Women'] } />
                <Selector value={ bowstyle } onChange={ setBowstyle } label="Bowstyle" options={ tournament.bowstyles } />
                <Selector value={ ageGroup } onChange={ setAgeGroup } label="Age group" options={ ['50+', 'Adult', 'U21', 'U18', 'U16', 'U15', 'U14', 'U12'] } />
            </form>
            <Link className="btn" to="/enter/entry-information/">Add archer details</Link>
        </>
    );
};

const EnterModalEntryInformation = () => {
    return (
        <>
            <h3>Step 2 - Entry information</h3>
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

    if (close) {
        return <Redirect to="/" />;
    };

    return (
        <Modal wide close={ () => setClose(true) } className="modal--tournament-entry">
            <h2>Enter</h2>
            <Switch>
                <Route path="/enter/archer-details/" render={ () => {
                    return <EnterModalArcherDetails tournament={ tournament } />
                } } />
                <Route path="/enter/entry-information/" component={ EnterModalEntryInformation } />
                <Route path="/enter/payment/" component={ EnterModalPayment } />
                <Route path="" exact render={ () => {
                    return <EnterModalEntryList entries={ [] } />
                } } />
            </Switch>
        </Modal>
    );
};

export default EnterModal;
