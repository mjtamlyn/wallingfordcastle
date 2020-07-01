import React from 'react';

class Schedule extends React.Component {
    render() {
        return (
            <div>
                { JSON.stringify(this.props.schedule) }
            </div>
        );
    }
}

export default Schedule;
