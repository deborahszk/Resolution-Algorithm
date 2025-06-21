import time
import tracemalloc

MAX_RESOLUTION_STEPS = 10000

def pl_resolution(cnf, max_steps=MAX_RESOLUTION_STEPS):
    cnf = set(cnf)
    new = set()
    steps = 0
    while True:
        pairs = [(ci, cj) for i, ci in enumerate(cnf) for cj in list(cnf)[i+1:]]
        for (ci, cj) in pairs:
            if steps >= max_steps:
                return None  # Timeout
            resolvents = pl_resolve(ci, cj)
            steps += 1
            if frozenset() in resolvents:
                return False  # UNSAT
            new.update(resolvents)
        if new.issubset(cnf):
            return True  # SAT
        cnf.update(new)

def pl_resolve(ci, cj):
    resolvents = set()
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                resolvent = (ci - {di}) | (cj - {dj})
                resolvents.add(frozenset(resolvent))
    return resolvents

def negate(literal):
    return literal[1:] if literal.startswith('¬') else '¬' + literal

def print_cnf(cnf):
    return ' ∧ '.join(['(' + ' ∨ '.join(sorted(clause)) + ')' for clause in cnf])

cnf_examples = [
    {'name': 'Trivial SAT', 'cnf': [{ 'A' }]},
    {'name': 'Trivial UNSAT', 'cnf': [{ 'A' }, { '¬A' }]},
    {'name': 'Simple SAT', 'cnf': [{ 'A', 'B' }, { '¬A' }]},
    {'name': 'Simple UNSAT', 'cnf': [{ 'A' }, { 'B' }, { '¬A', '¬B' }]},
    {'name': 'Chain SAT', 'cnf': [{ 'A', 'B' }, { '¬B', 'C' }, { '¬C', 'D' }]},
    {'name': 'Chain UNSAT', 'cnf': [{ 'A' }, { '¬A', 'B' }, { '¬B', 'C' }, { '¬C', '¬A' }]},
    {'name': '3-SAT SAT', 'cnf': [{ 'A', 'B', 'C' }, { '¬A', 'D', 'E' }, { '¬B', '¬E', 'F' }]},
    {'name': '3-SAT UNSAT', 'cnf': [{ 'A' }, { 'B' }, { 'C' }, { '¬A', '¬B' }, { '¬B', '¬C' }, { '¬C', '¬A' }]},
    {'name': 'Redundant SAT', 'cnf': [{ 'A' }, { 'A', 'B' }, { 'A', 'B', 'C' }]},
    {'name': 'Deep Contradiction', 'cnf': [{ 'A', 'B' }, { '¬B', 'C' }, { '¬C', 'D' }, { '¬D', 'E' }, { '¬E', '¬A' }]},
    {'name': 'Pure Literal SAT', 'cnf': [{ 'A' }, { 'B', 'C' }, { 'C', 'D' }]},
    {'name': 'Unit Propagation SAT', 'cnf': [{ 'A' }, { '¬A', 'B' }, { '¬B', 'C' }]},
    {'name': 'Deep UNSAT', 'cnf': [{ 'A' }, { '¬A', 'B' }, { '¬B', 'C' }, { '¬C', 'D' }, { '¬D', 'E' }, { '¬E', '¬A' }]},
    {'name': 'Complex 3-SAT SAT', 'cnf': [{ 'A', 'B', 'C' }, { '¬A', 'D', 'E' }, { '¬B', '¬E', 'F' }, { '¬C', 'F', 'G' }, { '¬D', '¬F', 'G' }]},
    {'name': 'Hard contradiction', 'cnf': [{ 'A' }, { '¬A', 'B' }, { '¬B', 'C' }, { '¬C', 'D' }, { '¬D', 'E' }, { '¬E', 'F' }, { '¬F', '¬A' }]},
]

for i, example in enumerate(cnf_examples, start=1):
    name = example['name']
    cnf = {frozenset(clause) for clause in example['cnf']}

    print(f"Example {i}: {name}")
    print("CNF:", print_cnf(cnf))

    tracemalloc.start()
    start = time.perf_counter()
    result = pl_resolution(cnf)
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result is None:
        print("Result:️ Too complex")
    elif result is True:
        print("Result: SATISFIABLE")
    else:
        print("Result: UNSATISFIABLE")

    print(f" Time: {(end - start) * 1e6:.2f} μs")
    print(f" Peak memory: {peak / 1024:.2f} KB")
