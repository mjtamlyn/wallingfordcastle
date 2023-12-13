import React, { useState, useEffect } from 'react';
import Mousetrap from 'mousetrap';


const Selector = ({ label, options, onChange, value = null, wrap = false }) => {
    const [selected, setSelected] = useState(value);
    const [focused, setFocused] = useState(false);

    useEffect(() => {
        if (!focused || selected) return;
        const selectFirst = () => {
            select(options[0])();
        };
        Mousetrap.bind('space', selectFirst);
        return () => Mousetrap.unbind('space');
    });

    useEffect(() => {
        if (!focused) return;
        const selectNext = () => {
            if (selected) {
                const idx = options.indexOf(selected);
                if (idx > -1 && idx + 1 < options.length) {
                    select(options[idx + 1])();
                }
            } else {
                select(options[0])();
            }
        };
        Mousetrap.bind('right', selectNext);
        return () => Mousetrap.unbind('right');
    }, [selected, focused]);

    useEffect(() => {
        if (!focused) return;
        const selectPrev = () => {
            if (selected) {
                const idx = options.indexOf(selected);
                if (idx > 0) {
                    select(options[idx - 1])();
                }
            } else {
                select(options[0])();
            }
        };
        Mousetrap.bind('left', selectPrev);
        return () => Mousetrap.unbind('left');
    }, [selected, focused]);

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
            <div tabIndex="0" onFocus={ () => setFocused(true) } onBlur={ () => setFocused(false) } className={ 'selector ' + (wrap ? 'selector--wrap' : '') }>
                { choices }
            </div>
        </div>
    );
};

export default Selector;
