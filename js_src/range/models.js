class BookableDate {
    constructor({ api, pretty, title, notes }) {
        this.api = api;
        this.pretty = pretty;
        this.title = title;
        this.notes = notes;
    }
}

class Slot {
    constructor({ start, end, duration, target, bRange = false, face = '', numberOfTargets = 1, booked = false, details = '', groupName = '', editable = false }) {
        this.start = start;
        this.end = end;
        this.duration = duration;  // in minutes
        this.target = target;
        this.bRange = bRange;
        this.face = face || '';
        this.numberOfTargets = numberOfTargets;
        this.booked = booked;
        this.details = details;
        this.groupName = groupName;
        this.editable = editable;
    }

    reference() {
        let range = '';
        if (this.bRange) {
            range = 'B';
        }
        return `${this.start.split('T')[1]}/${range}${this.target}${this.face}`;
    }
}

class Archer {
    constructor({ id, name }) {
        this.id = id;
        this.name = name;
    }
}

export default { Archer, BookableDate, Slot };
