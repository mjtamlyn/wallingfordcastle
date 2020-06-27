import React from 'react';
import ReactDOM from 'react-dom';

const app = document.getElementById('app-range-booking');


class DateSelector extends React.Component {
    render() {
        return (
            <div className="date-selector">
                <h3>Pick a date</h3>
            </div>
        );
    }
}


ReactDOM.render(<DateSelector />, app);
