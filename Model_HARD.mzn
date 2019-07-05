include "Model_MEDIUM.mzn";

% maximal number of blocked roads on a given day - only relevant in HARD instances
constraint forall(rs in ROAD_SETS) (
  forall(d in DAYS)
    (
      sum (r in ROAD_CLOSE[rs]) 
      (
        sum(a in ROAD_ACTIVITIES[r]) (activity_start[a] == d)) <= MAX_CLOSED[rs]
      )
  );
