%SETS
int : n_days;       %Number of Working Days
int : n_roads;      %Number of days
int : n_centers;    %Number Workcenters
int : n_worksheets; %Number of Worksheets
int : n_activities;  %Number activities
int : n_road_sets;  %Number of different sets with road constraints
int : n_precede;    %Number of precedes
set of int : DAYS = 1..n_days;              %Set of Working Days
set of int : ROADS = 1..n_roads;              %Set of Roas; n_road is a dummy road 
set of int : CENTERS = 1..n_centers;        %Set Workcenters
set of int : WORKSHEETS = 1..n_worksheets;  %Set of Worksheets
set of int : ACTIVITIES = 1..n_activities;   %Set activities
set of int : ROAD_SETS = 1..n_road_sets;    %Set of road block sets
set of int : PRECEDE_SET = 1..n_precede;      %Set of precede Definitions

%PARAMETERS
array[ROADS,DAYS] of int : PERTUBATION;          %Pertubation costs per road and day, n_roads must be all 0
array[WORKSHEETS] of int : USED_CENTER;          %The used center for each worksheet ID
array[WORKSHEETS] of int : MANDATORY;           %True if Worksheet is mandatory
array[WORKSHEETS] of int : IMPORTANCE;           %Importance of the worksheet, higher-> more important
array[WORKSHEETS] of int : EST;                  %Earliest starting time of the Worksheet
array[WORKSHEETS] of int : LST;                  %Latest starting time of the Worksheet
array[WORKSHEETS] of int : DURATION;             %Duration of the worksheet == number of succesiv tasks
%array[WORKSHEETS,DAYS] of int : USED_ROADS;     %Road_ID that is closed of each day in DURATION, the remaining are filled with the DUmmy Road n_roads --> we have to find something better
%array[WORKSHEETS,DAYS] of int : WORKERS_NEEDED; %Number of workers that are needed of each day in DURATION, the remaining day are filled with 0 --> we have to find something better
array[ROAD_SETS] of int : MAX_CLOSED;            %Maximal number of roads in each set that can be closed simultaneously
array[ROAD_SETS] of set of int: ROAD_CLOSE;      %Set of roads which refer to MAX_CLOSED
array[PRECEDE_SET,1..2] of int : PRECEDE;        %The first Workbook_ID has to be finished before the second 
array[ACTIVITIES] of int
 : USED_ROADS;
array[ACTIVITIES] of int : WORKERS_NEEDED;
array[WORKSHEETS,ACTIVITIES] of int : W_TO_A;
array[CENTERS] of int : MAX_CAPACITY;


%Variables
array[WORKSHEETS] of var DAYS : start;
array[WORKSHEETS] of var bool : used;
array[ACTIVITIES] of var DAYS : activity_start;
array[ACTIVITIES] of var bool : activity_used;


%Earliest and latest starting time
constraint forall(w in WORKSHEETS )
    ((start[w] >= EST[w] /\ start[w] <= LST[w]) \/ (used[w] == false));

%Mandatory Worksheet
constraint forall(w in WORKSHEETS where MANDATORY[w] == 1)
    (used[w] = true);
    
%Precedence between Worksheet

constraint forall(p in PRECEDE_SET)
%output [ "start:" , join(",",[show(p)| p in PRECEDE_SET]), join(",", [show(IMPORTANCE[0]) | p in PRECEDE_SET])];
((used[PRECEDE[p,1]] /\ used[PRECEDE[p,2]]) -> (start[PRECEDE[p,1]] + DURATION[PRECEDE[p,1]] <= start[PRECEDE[p,2]]));
  
    
%All Activities of used WORKSHEETS have to be assigned
%constraint forall(w in WORKSHEETS)

    

   

