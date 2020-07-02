import React from 'react';
import { NavLink } from 'react-router-dom';

class DateSelector extends React.Component {
    render() {
        const dates = this.props.dates.map((date) => {
            return (
                <div className="selector__item" key={ date.api }>
                    <NavLink
                        to={ '/' + date.api + '/' }
                        className="selector__link"
                        activeClassName="selector__link--selected"
                    >{ date.pretty }</NavLink>
                </div>
            );
        });
        return (
            <div className="selector">
                { dates }
            </div>
        );
    }
}

export default DateSelector;
