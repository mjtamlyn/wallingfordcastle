import React from 'react';
import deepForEach from 'deep-for-each';

import models from 'range/models';
import Loading from 'utils/Loading';


class Loader extends React.Component {
    constructor(props) {
        super(props);
        this.store = null;
        this.state = { loaded: false };
    }

    getApiEndpoint() {
        return this.apiEndpoint;
    }

    componentDidMount() {
        fetch(this.getApiEndpoint())
            .then(response => response.json())
            .then((rawData) => {
                deepForEach(rawData, (value, key, subject) => {
                    if (value.__type) {
                        subject[key] = new models[value.__type](value);
                    }
                });
                return rawData;
            })
            .then((data) => {
                this.store = data;
                this.setState({ loaded: true });
            });
    }

    renderLoaded(data) {
        return (<p>Unimplemented renderLoaded!</p>);
    }

    render() {
        if (!this.store) {
            return (<Loading />);
        }
        return this.renderLoaded(this.store);
    }
}

export default Loader;
