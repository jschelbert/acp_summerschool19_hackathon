%SETS
int : n_days;       %Number of Working Days
int : n_roads;      %Number of days
int : n_centers;    %Number Workcenters
int : n_worksheets; %Number of Worksheets
int : n_activitys;  %Number activities
int : n_road_sets;  %Number of different sets with road constraints
int : n_precede;    %Number of precedes
set of int : DAYS = 0..n_days-1;              %Set of Working Days
set of int : ROADS = 0..n_roads;            %Set of Roas; n_road is a dummy road 
set of int : CENTERS = 0..n_centers-1;        %Set Workcenters
set of int : WORKSHEETS = 0..n_worksheets-1;  %Set of Worksheets
set of int : ACTIVITIES = 0..n_activitys-1;   %Set activities
set of int : ROAD_SETS = 0..n_road_sets-1;    %Set of road block sets
set of int : PRECEDE_SET = 0..n_precede;      %Set of precede Definitions

%PARAMETERS
array[ROADS,DAYS] of int : PERTUBATION;    %Pertubation costs per road and day, n_roads must be all 0
array[WORKSHEETS] of int : USED_CENTER;    %The used center for each worksheet ID
array[WORKSHEETS] of bool : MANDATORY;     %True if Worksheet is mandatory
array[WORKSHEETS] of int : IMPORTANCE;     %Importance of the worksheet, higher-> more important
array[WORKSHEETS] of int : EST;            %Earliest starting time of the Worksheet
array[WORKSHEETS] of int : LST;            %Latest starting time of the Worksheet
array[WORKSHEETS] of int : DURATION;       %Duration of the worksheet == number of succesiv tasks
array[WORKSHEETS,DAYS] of int : USED_ROADS; %Road_ID that is closed of each day in DURATION, the remaining are filled with the DUmmy Road n_roads --> we have to find something better
array[WORKSHEETS,DAYS] of int : WORKERS_NEEDED; %Number of workers that are needed of each day in DURATION, the remaining day are filled with 0 --> we have to find something better
array[ROAD_SETS] of int : MAX_CLOSED;      %Maximal number of roads in each set that can be closed simultaneously
array[ROAD_SETS] of set of int: ROAD_CLOSE;      %Set of roads which refer to MAX_CLOSED
array[PRECEDE_SET,0..1] of int : PRECEDE;  %The first Workbook_ID has to be finished before the second 


%Variables
array[WORKSHEETS] of var DAYS : start;
array[WORKSHEETS] of var bool : used;

%Earliest starting time

   

