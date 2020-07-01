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
                archers.pop(id);
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
            let className = 'archer';
            if (this.state.selected.includes(archer.id)) {
                className += ' archer--selected';
            }
            archers.push(
                <div className={ className } key={ archer.id }>
                    <a onClick={ ::this.toggle(archer.id) }>
                        { archer.name }
                    </a>
                </div>
            );
        });
        return (
            <div className="archer-multi-select">
                { archers }
            </div>
        );
    }
}

export default ArcherMultiSelect;
