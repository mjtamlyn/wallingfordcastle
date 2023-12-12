import React, { useState } from 'react';

import { Switch, Route, Redirect, Link } from 'react-router-dom';
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

const EnterModalArcherDetails = () => {
    return (
        <>
            <h3>Step 1 - Archer details</h3>
            <div>Name, AGB, Club, Gender, Bowstyle, DOB/Age group</div>
            <Link to="/enter/entry-information/">Next</Link>
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
        <Modal close={ () => setClose(true) } className="modal--tournament-entry">
            <h2>Enter</h2>
            <Switch>
                <Route path="/enter/archer-details/" component={ EnterModalArcherDetails } />
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
