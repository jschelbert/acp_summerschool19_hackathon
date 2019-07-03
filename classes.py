def read_data(filename):
    with open(filename) as f:
        mylist = f.read().splitlines()

    q = mylist[0].split()
    nDays = int(q[0])
    nRoads = int(q[1])
    nWC = int(q[2])
    nWS = int(q[3])
    nActivities = int(q[4])
    line_num = 1
    ## Roads
    roads = []
    for i in range(nRoads):
        q = mylist[line_num].split()
        Road_id = int(q[0])
        days = [0] * nDays
        for k in range(len(q) - 1):
            a = q[k + 1]
            b = a.split(":")
            for j in range(int(b[0]), int(b[1])):
                days[j] = int(b[2])
        roads.append(Road(Road_id, days))
        line_num += 1
    ### Work Centers
    workcenters = []
    for i in range(nWC):
        q = mylist[line_num].split()
        workcenters.append(Workcenter(int(q[0]), int(q[1])))
        line_num += 1
    ### worksheets
    worksheets = []
    for i in range(nWS):
        q = mylist[line_num].split()
        worksheet_id = int(q[0])
        workcenter_id = int(q[1])
        mandatory = int(q[2])
        importance = int(q[3])
        est = int(q[4])
        lst = int(q[5])
        duration = int(q[6])
        activities = []
        for l in range(duration):
            activities.append(Activity(rank=l, affected_road_id=int(q[7 + 2 * l]), workers_needed=int(q[8 + 2 * l]),
                                       worksheet_id=worksheet_id))
        worksheets.append(Worksheet(worksheet_id, importance, mandatory, workcenter_id, duration, est, lst, activities))
        line_num += 1
    lines_left = len(mylist) - line_num
    roadblock_constraints = []
    precendence_relations = []
    while (lines_left > 0):
        q = mylist[line_num].split()

        if q[0] == 'M':
            num_roads_blocked = int(q[1])
            roads_blocked = []
            for i in range(len(q) - 1):
                roads_blocked.append(int(q[i + 1]))
            roadblock_constraints.append(RoadblockConstraint(max_number_allowed=num_roads_blocked,
                                                             affected_road_ids=roads_blocked))
        if q[0] == 'P':
            predced = int(q[1])
            successor = int(q[2])
            precendence_relations.append((predced, successor))
        lines_left -= 1
        line_num += 1

    return nDays,nActivities, worksheets, roads, workcenters, roadblock_constraints, precendence_relations


def write_data_file(filename, probleminstance):
    with open(filename, "w") as f:
        f.write(f"""
n_days = {probleminstance.number_of_days};
n_roads = {len(probleminstance.roads)};      
n_centers = {len(probleminstance.workcenters)};    
n_worksheets = {len(probleminstance.worksheets)}; 
n_activitys = {probleminstance.number_of_activities};  
n_road_sets = {len(probleminstance.roadblock_constraints)};  
n_precede = {len(probleminstance.precedence_relations)};""")



class Worksheet(object):

    def __init__(self, id, importance=0, mandatory=0, workcenter=None, duration=1,
                 earliest_start=None, latest_start=None, activities=[]):
        self.id = id
        self.importance = importance
        self.mandatory = mandatory,
        self.workcenter = workcenter,
        self.duration = duration
        self.earliest_start = earliest_start
        self.latest_start = latest_start
        self.activities = activities

    def __str__(self):
        return f"Workcenter(ID {self.id})\nImportance: {self.importance}\nMandatory: {self.mandatory}\nDuration: {self.duration}"


class Activity(object):

    def __init__(self, worksheet_id, rank=None, workers_needed=None, affected_road_id=None, affected_road=None):
        self.worksheet_id = worksheet_id
        self.rank = rank
        self.workers_needed = workers_needed
        self.affected_road_id = affected_road_id
        self.affected_road = affected_road

    def __str__(self):
        return f"Activity within Worksheet ID {self.worksheet_id} with rank {self.rank}\nAffected road: ID {self.affected_road_id}\nWorkers needed: {self.workers_needed}"


class Road(object):

    def __init__(self, id, pertubation=None):
        self.id = id
        self.pertubation = pertubation

    def __str__(self):
        return f"Road(ID {self.id})\nPertubation {self.pertubation}"


class Workcenter(object):

    def __init__(self, id, number_of_workers):
        self.id = id
        self.number_of_workers = number_of_workers

    def __str__(self):
        return f"Workcenter(ID {self.id})\nNumber of workers available per day: {self.number_of_workers}"


class RoadblockConstraint(object):
    def __init__(self, max_number_allowed, affected_road_ids=None, affected_roads=None):
        self.max_number_allowed = max_number_allowed
        self.affected_road_ids = affected_road_ids
        self.affected_roads = affected_roads

    def __str__(self):
        return f"There are maximal {self.max_number_allowed} roads allowed to be closed from {self.affected_road_ids}"


class ProblemInstance(object):

    def __init__(self, filename, output_filename=None):
        self.filename = filename
        self.output_filename = output_filename if output_filename else filename + ".dzn"

        number_of_days, number_of_activities, worksheets, roads, workcenters, roadblock_constraints, precedence_relations = read_data(
            filename)
        self.number_of_days = number_of_days
        self.number_of_activities = number_of_activities
        self.worksheets = worksheets
        self.roads = roads
        self.workcenters = workcenters
        self.roadblock_constraints = roadblock_constraints
        self.precedence_relations = precedence_relations

    def __str__(self):
        return f"Problem instance read from {self.filename} - output in {self.output_filename}"
