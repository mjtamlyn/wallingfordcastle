import React from 'react';

import store from 'utils/store';
import Loading from 'utils/Loading';


class Loader extends React.Component {
    constructor(props) {
        super(props);
        this.state = { loaded: false };
    }

    getApiEndpoint() {
        return this.apiEndpoint;
    }

    componentDidMount() {
        store.load(this.getApiEndpoint()).then((data) => {
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
