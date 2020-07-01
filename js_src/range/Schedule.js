import React from 'react';
import { Link } from 'react-router-dom';
import moment from 'moment';

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
                    let duration = slot.duration / 15;
                    const linkTarget = `/${ this.props.date }/book/${ time.format('HH:mm') }/${ slot.target }/`;
                    if (slot.booked) {
                        columns.push(
                            <td key={ slot.target } rowSpan={ duration }>
                                { slot.details }
                            </td>
                        );
                    } else {
                        columns.push(
                            <td key={ slot.target } rowSpan={ duration }>
                                Free slot
                                <br />
                                <Link to={ linkTarget }>Book</Link>
                            </td>
                        );
                    }
                    overlaps[slot.target - 1] = duration - 1;
                });
            } else {
                for (let i=0; i<targets; i++) {
                    if (overlaps[i] === 0) {
                        columns.push(
                            <td key={ i + 1 }></td>
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
        );
    }
}

export default Schedule;
