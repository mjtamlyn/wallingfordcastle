import React, { useId } from 'react';


const FormInput = ({ value, onChange, label, autoFocus = false }) => {
    const name = useId();

    return (
        <div>
            <label htmlFor={ name }>{ label }:</label>
            <input id={ name } value={ value } onChange={ (e) => onChange(e.target.value) } autoFocus={ autoFocus } />
        </div>
    );
};

export default FormInput;
