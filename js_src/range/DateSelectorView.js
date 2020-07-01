import React from 'react';

import Loader from 'utils/Loader';
import DateSelector from 'range/DateSelector';

class DateSelectorView extends Loader {
    apiEndpoint = '/api/range/';

    renderLoaded(data) {
        return (
            (<DateSelector dates={ data.dates } />)
        )
    }
}

export default DateSelectorView;
