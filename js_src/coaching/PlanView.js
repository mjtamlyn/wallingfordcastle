import React from 'react';

import Loader from 'utils/Loader';


class PlanView extends Loader {
    getApiEndpoint(props) {
        const planId = props.planId;
        return `/api/coaching/plan/${planId}/`;
    }

    renderLoaded(data) {
        return (
            <div>
                <p>{ JSON.stringify(data) }</p>
            </div>
        );
    }
}

export default PlanView;
