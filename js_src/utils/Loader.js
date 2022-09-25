import React from 'react';

import store from 'utils/store';
import Loading from 'utils/Loading';


class Loader extends React.Component {
    subscribe = false

    constructor(props) {
        super(props);
        this.state = { loaded: null };
        this.subscriptionFn = ::this.setData;
    }

    getApiEndpoint() {
        return this.props.apiEndpoint || this.apiEndpoint;
    }

    setData(data) {
        this.store = data;
        this.setState({ loaded: new Date() });
    }

    componentDidMount() {
        const url = this.getApiEndpoint(this.props);
        store.load(url).then(::this.setData);
        if (this.subscribe) {
            store.subscribe(url, this.subscriptionFn);
        }
    }

    componentDidUpdate(prevProps) {
        const oldUrl = this.getApiEndpoint(prevProps);
        const url = this.getApiEndpoint(this.props);
        if (oldUrl !== url) {
            store.load(url).then(::this.setData);
            if (this.subscribe) {
                store.unsubscribe(oldUrl, this.subscriptionFn);
                store.subscribe(url, this.subscriptionFn);
            }
        }
    }

    componentWillUnmount() {
        if (this.subscribe) {
            const url = this.getApiEndpoint();
            store.unsubscribe(url, this.subscriptionFn);
        }
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
