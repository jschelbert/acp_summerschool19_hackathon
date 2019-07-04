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
    activity_rank = 0
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
            activity_rank += 1

            activities.append(Activity(rank=activity_rank, affected_road_id=int(q[7 + l]),
                                       workers_needed=int(q[7 + duration + l]), worksheet_id=worksheet_id))
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

    return nDays, nActivities, worksheets, roads, workcenters, roadblock_constraints, precendence_relations


def print_perturbation(roads):
    s = "["
    for road in roads:
        s = s + "|"
        for r in road.pertubation:
            s = s + str(r) + ","
    s = s[:-1] + "|]"
    return s


def print_usedcenter(worksheets):
    s = "["
    for worksheet in worksheets:
        # print(worksheet.workcenter)
        s = s + str(worksheet.workcenter[0] + 1) + ","
    s = s[:-1] + "]"
    return s


def print_mandatory(worksheets):
    s = "["
    for worksheet in worksheets:
        # print(worksheet.workcenter)
        s = s + str(worksheet.mandatory[0]) + ","
    s = s[:-1] + "]"
    return s


def print_importance(worksheets):
    s = "["
    for worksheet in worksheets:
        s = s + str(worksheet.importance) + ","
    s = s[:-1] + "]"
    return s


def print_est(worksheets):
    s = "["
    for worksheet in worksheets:
        s = s + str(worksheet.earliest_start + 1) + ","
    s = s[:-1] + "]"
    return s


def print_lst(worksheets):
    s = "["
    for worksheet in worksheets:
        s = s + str(worksheet.latest_start + 1) + ","
    s = s[:-1] + "]"
    return s


def print_duration(worksheets):
    s = "["
    for worksheet in worksheets:
        s = s + str(worksheet.duration) + ","
    s = s[:-1] + "]"
    return s


def print_maxclosed(roadblocks):
    if len(roadblocks) > 0:
        s = "["
        for roadblock in roadblocks:
            s = s + str(roadblock.max_number_allowed) + ","
        s = s[:-1] + "]"
    else:
        s = "[]"

    return s


def print_roadclosed(roadblocks):
    if len(roadblocks) > 0:
        s = "[{"
        for roadblock in roadblocks:
            for road in roadblock.affected_road_ids:
                s = s + str(road) + ","
            s=s[:-1]+"},{"
        s = s[:-2] + "]"
    else:
        s = "[]"

    return s


def print_preceed(precedence_relations):
    if len(precedence_relations) > 0:
        s = "[|"
        for precedence in precedence_relations:
            s = s + str(precedence[0]) + "," + str(precedence[1]) + ",|"
        s = s[:-2] + "|]"
    else:
        s = "[]"

    return s


def print_capacity(workcenters):
    s = "["
    for w in workcenters:
        s = s + str(w.number_of_workers)
    s = s + "]"
    return s


# USED_ROADS
def print_useroads(workcenters):
    s = "["
    for w in workcenters:
        for a in w.activities:
            s = s + str(a.affected_road_id + 1) + ","
    s = s[:-1] + "]"
    return s


# WORKERS_NEEDED
def print_workrsneeded(workcenters):
    s = "["
    for w in workcenters:
        for a in w.activities:
            s = s + str(a.workers_needed) + ","
    s = s[:-1] + "]"
    return s


# ACTIVITY_CENTER
def print_activitycenter(workcenters):
    s = "["
    for w in workcenters:
        for a in w.activities:
            s = s + str(w.workcenter[0] + 1) + ","
    s = s[:-1] + "]"
    return s


# W_TO_A
def print_w2a(worksheets, nActivities):
    L = []
    c_index = 0

    for worksheet in worksheets:
        rank = 1
        s = [0] * nActivities
        print(s)
        for a in worksheet.activities:
            print(c_index + rank - 1)
            s[c_index + rank - 1] = rank
            rank += 1
        c_index += rank - 1
        L.append(s)
    op = "[|"
    for l in L:
        for b in l:
            op = op + str(b) + ","
        op = op + "|"
    op = op[:-2] + "|]"
    return op


def write_data_file(filename, probleminstance):
    with open(filename, "w") as f:
        f.write(f"""
n_days = {probleminstance.number_of_days};
n_roads = {len(probleminstance.roads)};      
n_centers = {len(probleminstance.workcenters)};    
n_worksheets = {len(probleminstance.worksheets)}; 
n_activities = {probleminstance.number_of_activities};  
n_road_sets = {len(probleminstance.roadblock_constraints)};  
n_precede = {len(probleminstance.precedence_relations)};
PERTUBATION=  {print_perturbation(probleminstance.roads)};
USED_CENTER= {print_usedcenter(probleminstance.worksheets)};
MANDATORY= {print_mandatory(probleminstance.worksheets)};
IMPORTANCE= {print_importance(probleminstance.worksheets)};
EST= {print_est(probleminstance.worksheets)};
LST= {print_lst(probleminstance.worksheets)};
DURATION= {print_duration(probleminstance.worksheets)};
MAX_CLOSED ={print_maxclosed(probleminstance.roadblock_constraints)};
ROAD_CLOSE ={print_roadclosed(probleminstance.roadblock_constraints)};
PRECEDE= {print_preceed(probleminstance.precedence_relations)};
MAX_CAPACITY = {print_capacity(probleminstance.workcenters)};
W_TO_A = {print_w2a(probleminstance.worksheets, probleminstance.number_of_activities)};
WORKERS_NEEDED = {print_workrsneeded(probleminstance.worksheets)};
USED_ROADS = {print_useroads(probleminstance.worksheets)};
ACTIVITY_CENTER = {print_activitycenter(probleminstance.worksheets)};
""")


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
