import React from 'react';


const TextField = ({ onChange, label }) => {
    return (
        <div className="text-field">
            <label>{ label }</label>
            <textarea className="text-field__textarea" onChange={ (e) => onChange(e.target.value) }></textarea>
        </div>
    );
};

export default TextField;
