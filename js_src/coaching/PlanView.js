import React, { useState } from 'react';

import Loader from 'utils/Loader';


const Tier = ({ tier }) => {
    return (
        <div className="event_plan__tier">
            <h3 className="event-plan__heading">{ tier.tierName } - { tier.name }</h3>
            <p className="event-plan__content">{ tier.comments }</p>
        </div>
    );
};


const Explainer = ({ title, children }) => {
    const [open, setOpen] = useState(false);
    let cls = 'explainer';
    if (open) {
        cls += ' explainer--open';
    }
    return (
        <div className={ cls }>
            <h3 className="explainer__question" onClick={ () => setOpen(!open) }>{ title }</h3>
            { open && children || null }
        </div>
    );
};
Explainer.p = ({ children }) => {
    return <p className="explainer__content">{ children }</p>;
};
Explainer.table = ({ children }) => {
    return <table className="explainer__table">{ children }</table>;
};


class PlanView extends Loader {
    getApiEndpoint(props) {
        const planId = props.planId;
        return `/api/coaching/plan/${planId}/`;
    }

    renderLoaded(data) {
        const tiers = data.tracks.map(tier => <Tier tier={ tier } key={ tier.tier } />);
        return (
            <div className="event-plan">
                <div className="event-plan__section">
                    <h2 className="event-plan__heading">Goals</h2>
                    <p className="event-plan__content">
            We believe that { data.archer } should be aiming for <strong>{ data.ageGroup } { data.targetClassification.name }</strong> classification. This is based on her indoor form and experience.
                    </p>
                    <p className="event-plan__content">
                        <strong>Coach comments:</strong> { data.personalisedTargetComments }
                    </p>

                    <Explainer title="What is a classification?">
                        <Explainer.p>
            For many archers, the outdoor season is focused around putting the
            hard work on technique from the winter into practice, and working
            towards achieving a classification. The exact process of achieving
            it varies depending on what level you are looking to achieve, but
            it always involves shooting a number of scores of a certain level
            at particular events.
                        </Explainer.p>
                        <Explainer.p>
            The system has been redesigned for the 2023 season, a project which
            Marc has been heavily involved with, and we are excited to put it
            into practice. We are hoping that many of the junior archers will
            get involved with achieving a classification this year by taking
            part in appropriate competitive events. The classifications come
            with badges and will be presented at the end of season awards.
                        </Explainer.p>
                    </Explainer>

                    <Explainer title="How do I achieve a Bowman 1st class classification?">
                        <Explainer.p>
            In order to achieve a Bowman 1st class classification, you need to shoot 18
            dozen arrows (equivalent to 1.5 days of competition) at competitive
            events, with each event being over the relevant threshold score.
            Any competitive event is suitable, whether it’s a club target day,
            club champs, or anything else all the way up to National
            Championships. The only requirement is that it either includes
            your longest distance, or is your 720 round.
                        </Explainer.p>
                        <Explainer.p>
            Full classification tables can be found at <a href="https://archerygeekery.co.uk/mobile-friendly-classification-tables">Archery Geekery</a>.
                        </Explainer.p>
                    </Explainer>

                    <Explainer title="What rounds and distances do I shoot?">
                        <Explainer.p>
            Archery age groups are based on the year of birth, with the
            distances recommended depending on your age group and your gender
            for U16 and older.
                        </Explainer.p>

                        <Explainer.table>
                            <thead>
                                <tr>
                                    <th>Age Group</th>
                                    <th>
                                        Years of Birth<br />
                                        <small>for the { data.season } season</small>
                                    </th>
                                    <th>
                                        720 Distance <br />
                                        <small>for recurve archers</small>
                                    </th>
                                    <th>Full distance - Men</th>
                                    <th>Full distance - Women</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>50+</td>
                                    <td>1973 or earlier</td>
                                    <td>60m</td>
                                    <td>70m or 80y</td>
                                    <td>60m or 60y</td>
                                </tr>
                                <tr>
                                    <td>Adult</td>
                                    <td>1974-2002</td>
                                    <td>70m</td>
                                    <td>90m or 100y</td>
                                    <td>70m or 80y</td>
                                </tr>
                                <tr>
                                    <td>U21</td>
                                    <td>2003-2005</td>
                                    <td>70m</td>
                                    <td>90m or 100y</td>
                                    <td>70m or 80y</td>
                                </tr>
                                <tr>
                                    <td>U18</td>
                                    <td>2006-2007</td>
                                    <td>60m</td>
                                    <td>70m or 80y</td>
                                    <td>60m or 60y</td>
                                </tr>
                                <tr className="highlight">
                                    <td>U16</td>
                                    <td>2008</td>
                                    <td>50m</td>
                                    <td>60m or 60y</td>
                                    <td>50m or 50y</td>
                                </tr>
                                <tr>
                                    <td>U15</td>
                                    <td>2009</td>
                                    <td>50m</td>
                                    <td colSpan="2">50m or 50y</td>
                                </tr>
                                <tr>
                                    <td>U14</td>
                                    <td>2010-2011</td>
                                    <td>40m</td>
                                    <td colSpan="2">40m or 40y</td>
                                </tr>
                                <tr>
                                    <td>U12</td>
                                    <td>2012 or later</td>
                                    <td>30m</td>
                                    <td colSpan="2">30m or 30y</td>
                                </tr>
                            </tbody>
                        </Explainer.table>

                        <Explainer.p>
            The most common rounds we shoot are the 720 family, also known as
            “Metric 122” rounds, and the Metric (or 1440) family. 720 rounds
            consist of 6 dozen arrows shot at the same distance, whereas Metric
            rounds have 3 dozen arrows at each of 4 different distances. They
            may also shoot Bristol rounds, which are 12 dozen imperial rounds
            shot at 3 different distances measured in yards.
                        </Explainer.p>
                        <Explainer.p>
            Many lower level competitions at other clubs consist of other
            traditional round families - usually Westerns or Windsors. These
            are also shot at distances in yards, and have 8 dozen or 9 dozen
            arrows respectively. These events are often held at one distance
            less than the maximum for your age group, but you can also choose
            to “shoot up” in the older age category if you wish.
                        </Explainer.p>
                        <Explainer.p>
            You can always achieve scores shot at longer distances than those
            required of your age group, but we tend not to encourage this much
            as it often requires higher poundages.
                        </Explainer.p>
                    </Explainer>
                </div>

                <div className="event-plan__section">
                    <h2 className="event-plan__heading">Event Plan</h2>
                    <p className="event-plan__content">
            There are almost 30 events that junior archers could be attending this summer. In order to try and make some sense of everything that’s going on, I’ve divided the events club archers are attending into four tiers.
                    </p>
                    <ul>
                        <li>Tier 1 is the <strong>Archery GB Junior Archery Series</strong>, the blue riband events for the most competitive junior archers in the country.</li>
                        <li>Tier 2 is the <strong>Full distance events</strong>, including everything from National Championships to most of our own hosted competitions.</li>
                        <li>Tier 3 is the <strong>Fun shoots</strong> typically at shorter distances and not taking all day, these are enjoyable junior focused competitions we attend at other clubs.</li>
                        <li>Tier 4 are <strong>Target day</strong> events at the club, low key semi-competitive events which we are holding on Saturdays through the season.</li>

                    </ul>
                    { tiers }
                </div>
            </div>
        );
    }
}

export default PlanView;
