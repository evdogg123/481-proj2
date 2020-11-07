import copy

def get_column(queen):
    return int(queen[1])

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

def revise(problem, col_a, col_b):
    #Returns True if an element was removed from queen_a domain
    queen_a = get_queen(col_a)
    queen_b = get_queen(col_b)
    constraints = []
    a_num = 0
    b_num = 1
    domain_len = len(problem["variables"][queen_a])

    if get_pair_key(queen_a, queen_b) in problem["constraints"]:
        constraints = problem["constraints"][get_pair_key(queen_a, queen_b)]   
    else:
        constraints = problem["constraints"][get_pair_key(queen_b, queen_a)]
        a_num = 1
        b_num = 0

    for constraint in constraints:
        if constraint[b_num] not in problem["variables"][queen_b]:
            problem["variables"][queen_a] = list(filter(lambda x: x != constraint[a_num], problem["variables"][queen_a]))
    
    return (domain_len != len(problem["variables"][queen_a]), problem)

problem = init_problem(4)
problem["variables"][get_queen(1)] =[ i for i in problem["variables"][get_queen(0)] if i != 2]
print(problem["variables"][get_queen(1)])
removed, new_problem = revise(problem, 0, 1)
print(removed)
print(new_problem)

print(".........")
revise(problem, 0, 1)



