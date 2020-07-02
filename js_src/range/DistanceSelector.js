import React from 'react';

class DistanceSelector extends React.Component {
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
                this.props.onChange(this.state.selected)
            });
        };
    }

    render() {
        const distances = ['10m', '20m', '30m', '40m', '50m', '60m', '70m', '90m']
        const options = distances.map((distance) => {
            let linkClassName = "selector__link";
            if (this.state.selected === distance) {
                linkClassName += " selector__link--selected"
            }
            return (
                <div className="selector__item" key={ distance }>
                    <a className={ linkClassName } onClick={ ::this.toggle(distance) }>
                        { distance }
                    </a>
                </div>
            )
        });
        return (
            <div className="distance-selector">
                <label>Distance:</label>
                <div className="selector selector--distance-selector">
                    { options }
                </div>
            </div>
        );
    }
}

export default DistanceSelector;
