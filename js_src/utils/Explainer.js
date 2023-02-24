import React, { useState } from 'react';


const Explainer = ({ title, children }) => {
    const [open, setOpen] = useState(false);
    let cls = 'explainer';
    if (open) {
        cls += ' explainer--open';
    }
    return (
        <div className={ cls }>
            <h3 className="explainer__question" onClick={ () => setOpen(!open) }>{ title }</h3>
            { open && children || null }
        </div>
    );
};
Explainer.p = ({ children }) => {
    return <p className="explainer__content">{ children }</p>;
};
Explainer.table = ({ children }) => {
    return <table className="explainer__table">{ children }</table>;
};


export default Explainer;
