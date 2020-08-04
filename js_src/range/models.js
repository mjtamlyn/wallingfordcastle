class BookableDate {
    constructor({ api, pretty, title, notes }) {
        this.api = api;
        this.pretty = pretty;
        this.title = title;
        this.notes = notes;
    }
}

class Slot {
    constructor({ start, end, duration, target, booked = false, details = '', editable = false }) {
        this.start = start;
        this.end = end;
        this.duration = duration;  // in minutes
        this.target = target;
        this.booked = booked;
        this.details = details;
        this.editable = editable;
    }

    reference() {
        return `${this.start.split('T')[1]}/${this.target}`;
    }
}

class Archer {
    constructor({ id, name }) {
        this.id = id;
        this.name = name;
    }
}

export default { Archer, BookableDate, Slot };
