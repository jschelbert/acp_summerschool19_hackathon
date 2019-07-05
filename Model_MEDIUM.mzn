include "Model_EASY.mzn";
%include "Instances/MEDIUM_1000_100.dzn";

% Capacity of the workcenters - relevant only in MEDIUM and HARD instances

%TODO: Use the cumulative constraint?!
constraint forall(c in CENTERS, d in DAYS)
    (sum (a in CENTER_ACTIVITIES[c]) ((activity_start[a] == d) * WORKERS_NEEDED[a]) <= MAX_CAPACITY[c]);

%constraint forall(c in CENTERS)
%(cumulative([activity_start[a] | a in CENTER_ACTIVITIES[c]], 1, [WORKERS_NEEDED[a] | a in CENTER_ACTIVITIES[c]], MAX_CAPACITY[c]));

%cumulative(array[int] of var int: s, array[int] of var int: d,
%           array[int] of var int: r, var int: b)
%
%It requires that a set of tasks given by start times s, durations d, and resource requirements r, never require more than a global resource bound b at any one time.