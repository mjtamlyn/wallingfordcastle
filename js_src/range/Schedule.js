import React from 'react';
import { Link, withRouter } from 'react-router-dom';
import moment from 'moment';

class BaseBookedSlot extends React.Component {
    render() {
        const { slot, rowSpan, colSpan } = this.props;

        let cancelLink = null;
        if (slot.editable) {
            const date = this.props.match.params.date;
            const linkTarget = `/${date}/cancel/${slot.reference()}/`;
            cancelLink = (
                <Link
                    className="range-schedule__cancel"
                    to={ linkTarget }
                >
                    Cancel
                </Link>
            );
        }

        let title = null;
        if (slot.groupName) {
            title = <p className="range-schedule__title">{ slot.groupName }</p>
        }
        return (
            <td
                className="range-schedule__slot range-schedule__slot--booked"
                rowSpan={ rowSpan }
                colSpan={ colSpan }
            >
                { title }
                <p className="range-schedule__description">{ slot.details.names }</p>
                <p className="range-schedule__description">{ slot.details.distance }</p>
                { cancelLink }
            </td>
        );
    }
}

const BookedSlot = withRouter(BaseBookedSlot);

class Schedule extends React.Component {
    formatTime(dateString) {
        return moment(dateString).format('HH:mm');
    }

    render() {
        const { abFaces, schedule } = this.props;
        const firstTime = moment(schedule[0].startTime);
        const lastTime = moment(schedule[this.props.schedule.length - 1].endTime);

        const targets = Math.max(...schedule.map((row) => row.slots.length));

        const startTimes = schedule.map((row) => row.startTime);

        const headerRow = [<td key="corner"></td>];
        const overlaps = [];
        for (let target=1; target<=targets; target++) {
            if (abFaces) {
                if (target % 2) {
                    headerRow.push(
                        <th key={ target }>Target { (target + 1) / 2 }A</th>
                    );
                } else {
                    headerRow.push(
                        <th key={ target }>Target { target / 2 }B</th>
                    );
                }
            } else {
                headerRow.push(
                    <th key={ target }>Target { target }</th>
                );
            }
            overlaps.push(0);
        }

        let time = firstTime;
        let rows = [];
        while (time <= lastTime) {
            let columns = [];
            columns.push(
                <th key="time">{ time.format('HH:mm') }</th>
            );

            if (startTimes.includes(time.format(time._f))) {
                let index = startTimes.indexOf(time.format(time._f));
                let slots = schedule[index].slots;
                slots.forEach((slot) => {
                    if (!slot) {
                        return; // TODO: there's an issue with missing boxes with odd sessions here
                    }
                    let duration = slot.duration / 15;
                    const linkTarget = `/${ this.props.date }/book/${ time.format('HH:mm') }/${ slot.target }${ slot.face }/`;
                    if (slot.booked) {
                        let nSpots = 1;
                        if (slot.numberOfTargets > 1) {
                            nSpots = slot.numberOfTargets * (abFaces ? 2 : 1);
                        }
                        columns.push(
                            <BookedSlot
                                key={ slot.target + slot.face }
                                rowSpan={ duration }
                                colSpan={ nSpots }
                                slot={ slot }
                            />
                        );
                    } else {
                        columns.push(
                            <td
                                className="range-schedule__slot range-schedule__slot--free"
                                key={ slot.target + slot.face }
                                rowSpan={ duration }
                            >
                                <Link className="range-schedule__book" to={ linkTarget }>
                                    <span className="range-schedule__book__inner">Book</span>
                                </Link>
                            </td>
                        );
                    }
                    for (let i=0; i<slot.numberOfTargets; i++) {
                        if (abFaces) {
                            overlaps[slot.target * 2 + i - 2] = duration - 1;
                            overlaps[slot.numberOfTargets + slot.target * 2 + i - 2] = duration - 1;
                        } else {
                            overlaps[slot.target + i - 1] = duration - 1;
                        }
                    }
                });
            } else {
                for (let i=0; i<targets; i++) {
                    if (overlaps[i] === 0) {
                        columns.push(
                            <td
                                className="range-schedule__slot range-schedule__slot--unavailable"
                                key={ i + 1 }
                            ></td>
                        );
                    }
                    overlaps[i] -= 1;
                }
            }

            rows.push(
                <tr key={ time.format() }>
                    { columns }
                </tr>
            )
            time = time.add(15, 'minutes');
        }

        return (
            <div>
                <table className="range-schedule">
                    <thead>
                        <tr>
                            { headerRow }
                        </tr>
                    </thead>
                    <tbody>
                        { rows }
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Schedule;
