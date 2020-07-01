import models from 'range/models';
import Cookies from 'cookies-js';
import deepForEach from 'deep-for-each';

class Store {
    constructor() {
        this.cache = {};
        this.subscriptions = {};
    }

    load(url) {
        if (this.cache[url]) {
            return new Promise((resolve) => {
                resolve(this.cache[url]);
            });
        }
        return fetch(url)
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
                this.cache[url] = data;
                return data;
            });
    }

    send(url, data) {
        let csrf = Cookies.get('csrftoken');
        return fetch(url, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            body: JSON.stringify(data),
        }).then((response) => response.json());
    }

    subscribe(url, callback) {
        if (this.subscriptions[url]) {
            this.subscriptions[url].push(callback);
        } else {
            this.subscriptions[url] = [callback];
        }
    }

    unsubscribe(url, callback) {
        if (this.subscriptions[url] && this.subscriptions[url].includes(callback)) {
            this.subscriptions[url].pop(callback);
            if (!this.subscriptions[url].length) {
                delete this.subscriptions[url];
            }
        }
    }

    invalidate(url) {
        delete this.cache[url];
        this.load(url).then((data) => {
            if (this.subscriptions[url]) {
                this.subscriptions[url].forEach((callback) => callback(data));
            }
        });
    }
}

const store = new Store();

export default store;
