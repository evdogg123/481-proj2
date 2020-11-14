import copy


def get_column(queen):
    return int(queen[1:])

def get_queen(col):
    return "Q" + str(col)

def get_pair_key(queen_a, queen_b):
    return queen_a + " " + queen_b

def init_problem(n):
    problem = {}
    variables = {}
    domain = list(range(0,n))
    for i in range(0, n):
        variables[get_queen(i)] = domain.copy()
    
    problem["variables"] = variables
    constraints = {}
    for queen_a in range(0, n):
        for queen_b in range(queen_a + 1 ,n ):
            #Q0 Q1, Q0 Q2...., Qn-2 Qn-1
            queen_pair_key = get_queen(queen_a) + " " + get_queen(queen_b)
            constraints[queen_pair_key] = []

            for a_loc in range(0, n):
                for b_loc in range(0,n):
                    #if not the same row and are not diagonal from eachother
                    if a_loc != b_loc and abs(queen_a - queen_b) != abs(a_loc - b_loc):
                        constraints[queen_pair_key].append( (a_loc,b_loc) )

    problem["constraints"] = constraints
    return problem

def revise(problem, queen_a, queen_b):
    #Returns True if an element was removed from queen_a domain
    constraints = []
    a_num = 0
    b_num = 1
    domain_a_temp = []
    domain_len = len(problem["variables"][queen_a])

    if get_pair_key(queen_a, queen_b) in problem["constraints"]:
        constraints = problem["constraints"][get_pair_key(queen_a, queen_b)]   
    else:
        constraints = problem["constraints"][get_pair_key(queen_b, queen_a)]
        a_num = 1
        b_num = 0

    for a_loc in problem["variables"][queen_a]:
        for constraint in constraints:
            if constraint[a_num] == a_loc and constraint[b_num] in problem["variables"][queen_b]:
                #Found a matching element in queen_b's domain to satisfy constraint for loc_a
                #Add a_loc to queen_a's domain
                domain_a_temp.append(a_loc)
                break
    problem["variables"][queen_a] = domain_a_temp
    return (len(domain_a_temp) != domain_len, problem )

def ac_3(csp):
    queue = []
    for i in range(0, len(csp["variables"])):
        for j in range(0, len(csp["variables"])):
            #Intitalize queue with all arcs
            if i != j:
                queue.append( (get_queen(i) , get_queen(j) ))
    while queue:
        (q1, q2) = queue.pop(0)
        (revised, csp) = revise(csp,q1, q2)
        if revised:
            if len(csp["variables"][q1]) == 0:
                return (False, None)
            
            for variable in csp["variables"].keys():
                if variable != q1 and variable != q2:
                    queue.append((q1, variable))
    return (True, csp)


def min_remaining_values(csp, var_assigns):
    assigned_vars = var_assigns.keys()
    min_domain = 999999
    min_variable = ""
    for variable in csp["variables"].keys():
        if not variable in assigned_vars:
            #variable has not been assigned
            if len(csp["variables"][variable]) < min_domain:
                min_variable = variable
                min_domain = len(csp["variables"][variable])
    
    return min_variable


def backtracking_search(csp):
    return backtrack({}, csp)

def consistent_assign(assigns, var, val):
    for queen in assigns:
        if val == assigns[queen] or abs(get_column(queen) - get_column(var)) == abs(val - assigns[queen]):
            return False
    return True


def csp_assign(csp):
    pass

def csp_unassign(csp):
    pass

def backtrack(assigns, csp):
    if len(assigns) == len(csp["variables"].keys()):
        return assigns
    
    var = min_remaining_values(csp, assigns)

    for value in csp["variables"][var]:
        if consistent_assign(assigns, var, value):
            assigns[var] = value
            ## variable var has been assigned to value, reduce its domain
            csp["variables"][var] = [value]
            csp_new = copy.deepcopy(csp)
            (consistent, csp_new) = ac_3(csp_new)
            if consistent:
                result = backtrack(assigns, csp_new)
                if result:
                    return result
        #Reset Domain
        csp["variables"][var] = [i for i in range(0, len(csp["variables"].keys()))]
        del assigns[var]
    return None




        







    

        

# problem = init_problem(4)
# problem["variables"][get_queen(1)] =[ i for i in problem["variables"][get_queen(0)] if i != 2 and i != 3]
# print(problem["variables"][get_queen(1)])
# removed, new_problem = revise(problem, "Q0", "Q1")
# print(removed)
# print(new_problem)

# print(ac_3(new_problem))

# print(".........")

# problem = {"variables": {"Q1": [0,1,2,3], "Q2": [0,1], "Q3": [1]}}
# assignments = {"Q3": 1}

# print(min_remaining_values( problem, assignments))

problem1 = init_problem(11)

print(backtracking_search(problem1))


