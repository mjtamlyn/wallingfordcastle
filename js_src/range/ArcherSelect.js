import React from 'react';

import Loader from 'utils/Loader';

class ArcherMultiSelect extends Loader {
    apiEndpoint = '/api/range/archers/';

    constructor(props) {
        super(props);
        this.state = {
            selected: null,
        };
    }

    toggle(id) {
        return (e) => {
            let selected = null;
            if (this.state.selected !== id) {
                selected = id;
            }
            this.setState({ selected }, () => {
                if (this.state.selected) {
                    this.props.onChange([this.state.selected]);
                } else {
                    this.props.onChange([]);
                }
            });
        };
    }

    renderLoaded(data) {
        const archers = [];
        data.archers.forEach((archer) => {
            let className = 'selector__link';
            if (this.state.selected === archer.id) {
                className += ' selector__link--selected';
            }
            archers.push(
                <div className="selector__item" key={ archer.id }>
                    <a className={ className } onClick={ ::this.toggle(archer.id) }>
                        { archer.name }
                    </a>
                </div>
            );
        });
        return (
            <div className="archer-multi-select">
                <label>Archer:</label>
                <div className="selector">
                    { archers }
                </div>
            </div>
        );
    }
}

export default ArcherMultiSelect;

