import React from 'react';

import Explainer from 'utils/Explainer';


const ClassificationExplainer = ({ classification }) => {
    let description = null;
    if (['MB', 'GMB', 'EMB'].includes(classification.id)) {
        description = <>
            In order to achieve a { classification.name } classification, you
            need to shoot 36 dozen arrows (equivalent to 3 full days of
            competition) at UKRS or WRS events, with each event being over
            the relevant threshold score.  Each event must either be a 720, a
            Metric or a Bristol of the relevant round for your gender and age
            group.  All Tier 1 and Tier 2 events are suitable.
        </>;
    } else if (['B1', 'B2'].includes(classification.id)) {
        description = <>
            In order to achieve a { classification.name } classification, you
            need to shoot 18 dozen arrows (equivalent to 1.5 days of competition)
            at competitive events, with each event being over the relevant
            threshold score.  Any competitive event is suitable, whether it’s a
            club target day, club champs, or anything else all the way up to
            National Championships. The only requirement is that it either includes
            your longest distance, or is your 720 round.
        </>;
    } else if (classification.id === 'B3') {
        description = <>
            In order to achieve a Bowman 3rd class classification, you need to shoot 18
            dozen arrows (equivalent to 1.5 days of competition) at competitive
            events, with each event being over the relevant threshold score.
            Any competitive event is suitable, whether it’s a club target day,
            club champs, or anything else all the way up to National
            Championships. There is a minimum distance requirement, which is one
            distance shorter than your full metric distance.
        </>;
    } else if (['A1', 'A2', 'A3'].includes(classification.id)) {
        description = <>
            In order to achieve an Archer Tier classification, you need to shoot 12
            dozen arrows in properly scored rounds. Any time you shoot the rounds
            is fine at this level, practice scores at training sessions are
            absolutely fine. We recommend 720 rounds at this standard, starting
            with the 30m round and moving back if you need to for each
            classification. Required distances vary depending on the age group and
            gender, and may change as you progress through the levels.
        </>;
    }
    return (
        <Explainer title={ `How do I achieve a ${classification.name} classification?` }>
            <Explainer.p>{ description }</Explainer.p>
            <Explainer.p>
Full classification tables can be found at <a href="https://archerygeekery.co.uk/mobile-friendly-classification-tables">Archery Geekery</a>.
            </Explainer.p>
        </Explainer>
    );
};

export default ClassificationExplainer;
