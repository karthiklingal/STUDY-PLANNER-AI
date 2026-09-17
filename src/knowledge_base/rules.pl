% rules.pl
% ---------
% Knowledge Representation Module (Prolog facts + rules).
% Encodes topic prerequisites and difficulty levels.

% prerequisite(Topic, RequiresTopic).
prerequisite(machine_learning, probability_theory).
prerequisite(machine_learning, linear_algebra).
prerequisite(classification, machine_learning).
prerequisite(clustering, machine_learning).
prerequisite(sentiment_analysis, classification).
prerequisite(search_strategies, agents_and_environments).
prerequisite(knowledge_representation, propositional_logic).

% difficulty(Topic, Level). Level: easy | medium | hard
difficulty(probability_theory, medium).
difficulty(linear_algebra, medium).
difficulty(agents_and_environments, easy).
difficulty(search_strategies, medium).
difficulty(propositional_logic, medium).
difficulty(knowledge_representation, hard).
difficulty(machine_learning, hard).
difficulty(classification, hard).
difficulty(clustering, hard).
difficulty(sentiment_analysis, hard).

% can_skip(Topic, Known) :- true if Known already covers Topic's prerequisite.
can_skip(Topic, Known) :-
    prerequisite(Topic, Known).

% recommend_before(Topic, X) :- X must be studied before Topic.
recommend_before(Topic, X) :-
    prerequisite(Topic, X).

% all_prerequisites(Topic, List) :- recursively find every prerequisite.
all_prerequisites(Topic, []) :-
    \+ prerequisite(Topic, _), !.
all_prerequisites(Topic, Prereqs) :-
    findall(P, prerequisite(Topic, P), Direct),
    findall(Sub, (member(D, Direct), all_prerequisites(D, Sub)), NestedLists),
    flatten(NestedLists, Nested),
    append(Direct, Nested, Combined),
    list_to_set(Combined, Prereqs).
