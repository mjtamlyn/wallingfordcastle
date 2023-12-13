import React, { useId } from 'react';

import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';


const DateInput = ({ value, onChange, label }) => {
    const name = useId();
    return (
        <div>
            <label htmlFor={ name }>{ label }:</label>
            <DatePicker
                selected={ value }
                onChange={ onChange }
                showMonthDropdown
                showYearDropdown
                yearDropdownItemNumber={ 100 }
                dropdownMode="select"
                calendarStartDay={ 1 }
                maxDate={ new Date() }
            />
        </div>
    );
};

export default DateInput;

