import React, { useState } from 'react';

import Explainer from 'utils/Explainer';
import Loader from 'utils/Loader';
import ClassificationExplainer from './ClassificationExplainer';
import EventCalendar from './EventCalendar';
import Tier from './Tier';


class PlanView extends Loader {
    subscribe = true

    getApiEndpoint(props) {
        const planId = props.planId;
        return `/api/coaching/plan/${planId}/`;
    }

    renderLoaded(data) {
        const tiers = data.tracks.map(tier => <Tier tier={ tier } key={ tier.tier } planId={ this.props.planId }/>);
        return (
            <div className="event-plan">
                <div className="event-plan__section">
                    <h2 className="event-plan__heading">Goals</h2>
                    <p className="event-plan__content">
            We believe that { data.archer } should be aiming for <strong>{ data.ageGroup } { data.targetClassification.name }</strong> classification. This is based on indoor form and experience.
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
            The system was redesigned for the 2023 season, and it's a key way
            we track progress and achievement across years. We are hoping that
            many of the junior archers will get involved with achieving a
            classification this year by taking part in appropriate competitive
            events. The classifications come with badges and will be presented
            at the end of season awards.
                        </Explainer.p>
                    </Explainer>

                    <ClassificationExplainer classification={ data.targetClassification } />

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
                                    <td>1974 or earlier</td>
                                    <td>60m</td>
                                    <td>70m or 80y</td>
                                    <td>60m or 60y</td>
                                </tr>
                                <tr>
                                    <td>Adult</td>
                                    <td>1975-2003</td>
                                    <td>70m</td>
                                    <td>90m or 100y</td>
                                    <td>70m or 80y</td>
                                </tr>
                                <tr>
                                    <td>U21</td>
                                    <td>2004-2006</td>
                                    <td>70m</td>
                                    <td>90m or 100y</td>
                                    <td>70m or 80y</td>
                                </tr>
                                <tr>
                                    <td>U18</td>
                                    <td>2007-2008</td>
                                    <td>60m</td>
                                    <td>70m or 80y</td>
                                    <td>60m or 60y</td>
                                </tr>
                                <tr className="highlight">
                                    <td>U16</td>
                                    <td>2009</td>
                                    <td>50m</td>
                                    <td>60m or 60y</td>
                                    <td>50m or 50y</td>
                                </tr>
                                <tr>
                                    <td>U15</td>
                                    <td>2010</td>
                                    <td>50m</td>
                                    <td colSpan="2">50m or 50y</td>
                                </tr>
                                <tr>
                                    <td>U14</td>
                                    <td>2011-2012</td>
                                    <td>40m</td>
                                    <td colSpan="2">40m or 40y</td>
                                </tr>
                                <tr>
                                    <td>U12</td>
                                    <td>2013 or later</td>
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
                    <Explainer title="What is SCAYT?">
                        <Explainer.p>
            SCAYT is the <strong>Southern Counties Archery Youth Tour</strong>,
            a collection of events which take place across the south east
            through the season. Archers can accumulate points based on their
            placing from attending any of the competitions, with the majority
            of points being claimed from attending at least 3 competitions.
                        </Explainer.p>
                        <Explainer.p>
            Archers then attend the SCAS regional championships, which are
            worth double points. The archer in each age group with the most
            points over the season is the winner!
                        </Explainer.p>
                        <Explainer.p>
            Events vary from small junior focused events at shorter distances
            right up to national level junior competitions, but archers of all
            levels and experience are encouraged to take part.
                        </Explainer.p>
                    </Explainer>
                    <Explainer title="How do I get a national junior ranking?">
                        <Explainer.p>
            To obtain a junior national ranking, you need to take part in a
            minimum of three record status competitions through the season.
            They need to be either 720s, Metrics or Bristols, with at least one
            of the events being a Metric or Bristol. Even if you just attended
            all the competitions we are hosting at Wallingford without going
            elsewhere, that would be sufficient to achieve a ranking.
                        </Explainer.p>
                        <Explainer.p>
            The rankings are based on the handicap system, which is the maths
            which underlies the classification system. The club will submit
            your ranking claim for you in October, unless you ask us not to or
            tell us you have done it yourself.
                        </Explainer.p>
                    </Explainer>
                </div>

                <div className="event-plan__section">
                    <h2 className="event-plan__heading">Event Plan</h2>
                    <p className="event-plan__content">
            There are over 30 events that junior archers could be attending this summer. In order to try and make some sense of everything that’s going on, I’ve divided the events club archers are attending into four tiers.
                    </p>
                    <ul>
                        <li>Tier 1 is the <strong>Archery GB Junior Archery Series</strong>, the blue riband events for the most competitive junior archers in the country.</li>
                        <li>Tier 2 is the <strong>Ranking events</strong>, including everything from National Championships to most of our own hosted competitions.</li>
                        <li>Tier 3 is the <strong>SCAYT</strong> events which are shot at shorter distances and don't take all day, these are enjoyable junior focused competitions we attend at other clubs.</li>
                        <li>Tier 4 are <strong>Target day</strong> events at the club, low key semi-competitive events which we are holding on Saturdays through the season.</li>

                    </ul>
                    { tiers }
                </div>

                <div className="event-plan__section">
                    <h2 className="event-plan__heading">Full calendar</h2>
                    <EventCalendar tracks={ data.tracks } />
                </div>
            </div>
        );
    }
}

export default PlanView;
