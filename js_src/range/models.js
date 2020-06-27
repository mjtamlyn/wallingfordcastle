class BookableDate {
    constructor({ api, pretty }) {
        this.api = api;
        this.pretty = pretty;
    }
}

class Slot {
    constructor({ start, end, duration, target, booked = false, details = '' }) {
        this.start = start;
        this.end = end;
        this.duration = duration;  // in minutes
        this.target = target;
        this.booked = booked;
        this.details = details;
    }
}

export default { BookableDate, Slot };
