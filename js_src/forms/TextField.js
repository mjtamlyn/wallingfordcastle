import React, { useId } from 'react';


const TextField = ({ value = '', onChange, label }) => {
    const name = useId();
    return (
        <div className="text-field">
            <label htmlFor={ name }>{ label }:</label>
            <textarea id={ name } className="text-field__textarea" onChange={ (e) => onChange(e.target.value) }>{ value }</textarea>
        </div>
    );
};

export default TextField;
