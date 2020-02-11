"""
Gale–Shapley stable matching algorithm
Wikipedia: https://en.m.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm

algorithm stable_matching is
    Initialize all m ∈ M and w ∈ W to free
    while ∃ free man m who still has a woman w to propose to do
        w := first woman on m's list to whom m has not yet proposed
        if w is free then
            (m, w) become engaged
        else some pair (m', w) already exists
            if w prefers m to m' then
                m' becomes free
                (m, w) become engaged 
            else
                (m', w) remain engaged
            end if
        end if
    repeat

Data structure

participants = {
    "side_A": {
        "abc": [
            "123", "451", "912"
        ],
        "asd": [
            "123", "912", "451"
        ],
        "pqq": [
            "123", "451", "912"
        ]
    },
    "side_B": {
        "123": [
            "pqq", "asd", "abc"
        ],
        "451": [
            "asd", "pqq", "abc"
        ],
        "912": [
            "pqq", "asd", "abc"
        ]
    }
}

Returns a list of stable matches
[
    ("123", "pqq"),
    ("451", "abc"),
    ("912", "asd")
]
"""
from typing import List, Dict, Tuple

# Declaring types
Person = str
People = List[Person]
Preferences = List[Person]
Side = Dict[Person, Preferences]
Participants = Dict[str, Side]
Pair = Tuple[Person, Person]
Matching = Dict[Person, Person]
Stable_Matching = List[Pair]


class MissingPreferences(Exception):
    pass


def other_side(current_side: str, all_sides: list) -> str:
    """Given a side and all possible sides, returns the opposite side"""
    for s in all_sides:
        if s != current_side:
            return s


def all_preferences(participants: Participants) -> bool:
    """Checks whether all participants have all participants of the other side in their own preference
    """
    sides = list(participants.keys())
    for side, people in participants.items():
        other_side_participants = participants[other_side(side, sides)]
        for name, preferences in people.items():
            for o in other_side_participants:
                if o not in preferences:
                    return False
    else:
        return True


def is_free(person: Person, engaged: Matching) -> bool:
    """Is the person missing from all current pairs?"""
    return person not in engaged


def current_match(person: Person, engaged: Matching) -> bool:
    """Returns the current match for that person"""
    return engaged.get(person)


def free_participants(people: People, engaged: Matching) -> list:
    """Returns all participants are that are still currently free"""
    return filter(lambda x: x not in engaged, people)


def preferred(a: Person, b: Person, preferences: Preferences) -> Person:
    """Is a preferred over b according to the preferences ordering?"""
    for preference in preferences:
        if preference == a:
            return True
        if preference == b:
            return False


def stable_matching(participants: Participants) -> Stable_Matching:
    """"""
    # The algorithm requires each participant expresses a preference that includes all other participants
    if not all_preferences(participants):
        raise MissingPreferences

    sides = list(participants.keys())
    proposing = sides[0]  # Taking the 1st side
    receiving = other_side(proposing, sides)
    proposers = participants[proposing]
    receivers = participants[receiving]
    free_proposers = proposers
    proposal_history = {k: {} for k in proposers}
    engagements = {}

    while free_proposers:
        for proposer in free_proposers:
            preferences = proposers[proposer]
            for target in preferences:
                # Has proposed yet?
                if target not in proposal_history[proposer]:
                    # Record proposal
                    proposal_history[proposer][target] = ""
                    # Is receiver free?
                    if is_free(target, engagements):
                        # Engagement
                        engagements[proposer] = target
                        engagements[target] = proposer
                        print(f"First match: {proposer} - {target}")
                    else:
                        # Pair already exists
                        current = current_match(target, engagements)
                        target_preferences = receivers[target]
                        if preferred(proposer, current, target_preferences):
                            # Proposer replaces the current individual
                            engagements[target] = proposer
                            engagements[proposer] = target
                            # Freeing the incumbent
                            del engagements[current]
                    # Done proposing this round
                    break
        # Updating the list of proposers that are free
        # Must be a list since a generator always evaluates to True
        free_proposers = list(free_participants(free_proposers, engagements))

    # Composing the stable matchings
    stable_matchings = set()
    for a, b in engagements.items():
        # Checking the reverse isn't already in
        if (b, a) not in stable_matchings:
            stable_matchings.add((a, b))


    return list(stable_matchings)

if __name__ == "__main__":
    sample_participants = {
        "side_A": {
            "abc": [
                "123", "451", "912"
            ],
            "asd": [
                "123", "912", "451"
            ],
            "pqq": [
                "123", "451", "912"
            ]
        },
        "side_B": {
            "123": [
                "pqq", "asd", "abc"
            ],
            "451": [
                "asd", "pqq", "abc"
            ],
            "912": [
                "pqq", "asd", "abc"
            ]
        }
    }
    results = stable_matching(sample_participants)
    print(results)