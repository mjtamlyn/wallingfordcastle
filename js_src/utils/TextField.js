import React from 'react';


const TextField = ({ onChange, label }) => {
    return (
        <div className="text-field">
            <label>{ label }</label>
            <textarea className="text-field__textarea" onChange={ onChange }></textarea>
        </div>
    );
};

export default TextField;
