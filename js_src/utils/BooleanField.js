import React, { useId } from 'react';


const BooleanField = ({ value, onChange, label }) => {
    const name = useId();
    return (
        <div>
            <label htmlFor={ name }>
                <input type="checkbox" id={ name } checked={ value } onChange={ (e) => onChange(e.target.checked) } />
                { label }
            </label>
        </div>
    );
};

export default BooleanField;
