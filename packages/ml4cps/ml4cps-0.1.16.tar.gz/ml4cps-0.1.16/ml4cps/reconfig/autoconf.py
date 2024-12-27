"""AutoConf algorithm was proposed in [1].

[1] Balzereit, K., & Niggemann, O. (2022).
AutoConf: A New Algorithm for Reconfiguration of Cyber-Physical Production Systems.
IEEE Transactions on Industrial Informatics. https://doi.org/10.1109/TII.2022.3146940
"""

from z3.z3 import And, Not, Or, Implies
from z3 import z3


def instantiate_solver(preBValues, hs_values, x, lb, ub):
    # instantiate solver
    s = z3.Solver()

    nEdges, nNodes = len(preBValues), len(x)

    # binary input variables
    b = z3.BoolVector('b', nEdges)
    preB = z3.BoolVector('preB', nEdges)

    # binary health status variables
    hs = z3.BoolVector('hs', nEdges)

    # predicates describing intervals of state variables
    low = z3.BoolVector('low', nNodes)
    high = z3.BoolVector('high', nNodes)
    ok = z3.BoolVector('ok', nNodes)

    # set previous values of binary variables
    for i in range(nEdges):
        s.add(preB[i] == bool(preBValues[i]))

    # set previous values of binary variables
    for i in range(nEdges):
        s.add(hs[i] == bool(hs_values[i]))

    # get interval of state variables
    for i in range(nNodes):
        if x[i] < lb[i]:
            s.add(low[i] == True)
            s.add(ok[i] == False)
            s.add(high[i] == False)
        elif x[i] > ub[i]:
            s.add(low[i] == False)
            s.add(ok[i] == False)
            s.add(high[i] == True)
        else:
            s.add(low[i] == False)
            s.add(ok[i] == True)
            s.add(high[i] == False)

    return s, b, preB, hs, low, high, ok


def group_variables(row):
    var_names = row.index
    # preBValues describes the input variables of the current, invalid configuration
    filter_col = [col for col in var_names if col.startswith('b')]
    preBValues = row[filter_col].to_numpy().astype(bool)

    # Read in binary health status (hs) variables
    filter_col = [col for col in var_names if col.startswith('hs')]
    hs_values = row[filter_col].to_numpy().astype(bool)

    # state variables of the current, invalid configuration
    filter_col = [col for col in var_names if col.startswith('x')]
    x = row[filter_col].to_numpy()

    # lower bounds for state variables
    filter_col = [col for col in var_names if col.startswith('lb')]
    lb = row[filter_col].to_numpy()

    # upper bounds for state variables
    filter_col = [col for col in var_names if col.startswith('ub')]
    ub = row[filter_col].to_numpy()
    return preBValues, hs_values, x, lb, ub


def autoconf(biadj_matrix, data):
    """AutoConf needs a causal model in form of a bi-adjacency matrix."""

    config = []  # Dictionary to save assignments in
    for idx1, row in data.iterrows():
        preBValues, hs_values, x, lb, ub = group_variables(row)

        s, b, preB, hs, low, high, ok = instantiate_solver(preBValues, hs_values, x, lb, ub)

        # Create reconfiguration system model SM
        # add reconfiguration hserations for search nodes
        for state_ind, states in biadj_matrix.iterrows(): # Iterate the reconf. parameters
            i = biadj_matrix.index.get_loc(state_ind)

            INFLOWS = [states.index.get_loc(x) for x in states[states == -1].index]
            OUTFLOWS = [states.index.get_loc(x) for x in states[states == 1].index]

            #                INFLOWS                     OUTFLOWS
            # low[i] -> (!preB[j] & b[j] or ...) or (preB[j] & !b[j] or ...)
            s.add(Implies(low[i], Or(Or([And(Not(preB[j]), b[j]) for j in INFLOWS]),
                                     Or([And(preB[j], Not(b[j])) for j in OUTFLOWS]))))

            #             OUTFLOWS                      INFLOWS
            # high[i] -> (!preB[j] & b[j] or ...) or (preB[j] & !b[j] or ...)
            s.add(Implies(high[i], Or(Or([And(Not(preB[j]), b[j]) for j in OUTFLOWS]),
                                      Or([And(preB[j], Not(b[j])) for j in INFLOWS]))))

            # low[i] -> (!preB[j] -> !b[j] & ...)
            s.add(Implies(low[i], And([Implies(Not(preB[j]), Not(b[j])) for j in OUTFLOWS])))

            # high[i] -> (!preB[j] -> !b[j] & ...)
            s.add(Implies(high[i], And([Implies(Not(preB[j]), Not(b[j])) for j in INFLOWS])))

        # check satisfiability
        if s.check() == z3.sat:
            status, model = 'sat', s.model()
        else:
            status, model = 'unsat', s.unsat_core()

        if status == 'sat':
            # print(f'{row.name}: {row.case}: Rcfg true, ** expected: {rcfg}')
            valNam = []
            valPos = []
            for b_i in b:
                val = model.eval(b_i, model_completion=True)
                valNam.append(b_i)
                valPos.append(int(bool(val)))
            # print(valNam)
            # print(valPos)
            config.append(valPos)
        else:
            # print(f'{row.name}: {row.case}: Rcfg false, ** expected: {rcfg}')
            config.append(None)
    return config
