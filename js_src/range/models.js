class BookableDate {
    constructor({ api, pretty, title, notes }) {
        this.api = api;
        this.pretty = pretty;
        this.title = title;
        this.notes = notes;
    }
}

class Slot {
    constructor({ start, end, duration, target, venue = '', bRange = false, face = '', numberOfTargets = 1, booked = false, details = '', groupName = '', editable = false, canReportAbsence = false }) {
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
        this.canReportAbsence = canReportAbsence;
        this.venue = venue;
    }

    reference() {
        let range = '';
        if (this.bRange) {
            range = 'B';
        }
        let reference = `${this.start.split('T')[1]}/${range}${this.target}${this.face}`;
        if (this.venue) {
            reference = `${this.venue}/` + reference;
        }
        return reference;
    }
}

class Archer {
    constructor({ id, name }) {
        this.id = id;
        this.name = name;
    }
}

export default { Archer, BookableDate, Slot };
