import React, { useState } from 'react';


const Selector = ({ label, options, onChange, wrap = false }) => {
    const [selected, setSelected] = useState(null);

    const select = (id) => {
        return () => {
            let newSelected = null;
            if (selected !== id) {
                newSelected = id;
            }
            setSelected(newSelected);
            onChange(newSelected);
        };
    }

    const choices = options.map((option) => {
        let linkClassName = "selector__link";
        if (selected === option) {
            linkClassName += " selector__link--selected"
        }
        return (
            <div className="selector__item" key={ option }>
                <a className={ linkClassName } onClick={ select(option) }>
                    { option }
                </a>
            </div>
        )
    });
    return (
        <div>
            <label>{ label }:</label>
            <div className={ 'selector ' + (wrap ? 'selector--wrap' : '') }>
                { choices }
            </div>
        </div>
    );
};

export default Selector;
