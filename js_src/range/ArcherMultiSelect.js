import React from 'react';

import Loader from 'utils/Loader';

class ArcherMultiSelect extends Loader {
    apiEndpoint = '/api/range/archers/';

    constructor(props) {
        super(props);
        this.state = {
            selected: [],
        };
    }

    toggle(id) {
        return (e) => {
            let archers = [].concat(this.state.selected);
            if (this.state.selected.includes(id)) {
                archers = archers.filter(item => item !== id)
            } else {
                archers.push(id);
            }
            this.setState({
                selected: archers,
            }, () => {
                this.props.onChange(this.state.selected)
            });
        };
    }

    renderLoaded(data) {
        const archers = [];
        data.archers.forEach((archer) => {
            let className = 'selector__link';
            if (this.state.selected.includes(archer.id)) {
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
                <label>Archer(s):</label>
                <div className="selector">
                    { archers }
                </div>
            </div>
        );
    }
}

export default ArcherMultiSelect;
