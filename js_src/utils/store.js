import models from 'range/models';
import deepForEach from 'deep-for-each';

class Store {
    constructor() {
        this.cache = {};
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
}

const store = new Store();

export default store;
