import React from 'react';
import { Link, withRouter } from 'react-router-dom';
import moment from 'moment';

class BaseBookedSlot extends React.Component {
    render() {
        const { slot, rowSpan } = this.props;

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

        return (
            <td
                className="range-schedule__slot range-schedule__slot--booked"
                rowSpan={ rowSpan }
            >
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
        const schedule = this.props.schedule;
        const firstTime = moment(schedule[0].startTime);
        const lastTime = moment(schedule[this.props.schedule.length - 1].slots[0].end);

        const targets = Math.max(...schedule.map((row) => row.slots.length));

        const startTimes = schedule.map((row) => row.startTime);

        const headerRow = [<td key="corner"></td>];
        const overlaps = [];
        for (let target=1; target<=targets; target++) {
            headerRow.push(
                <th key={ target }>Target { target }</th>
            );
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
                    const linkTarget = `/${ this.props.date }/book/${ time.format('HH:mm') }/${ slot.target }/`;
                    if (slot.booked) {
                        columns.push(
                            <BookedSlot
                                key={ slot.target }
                                rowSpan={ duration }
                                slot={ slot }
                            />
                        );
                    } else {
                        columns.push(
                            <td
                                className="range-schedule__slot range-schedule__slot--free"
                                key={ slot.target }
                                rowSpan={ duration }
                            >
                                <Link className="range-schedule__book" to={ linkTarget }>
                                    <span className="range-schedule__book__inner">Book</span>
                                </Link>
                            </td>
                        );
                    }
                    overlaps[slot.target - 1] = duration - 1;
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
