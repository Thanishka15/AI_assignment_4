from itertools import permutations


def solve(variables, domains, neighbors):
    def is_consistent(var, val, assignment):
        return all(assignment.get(n) != val for n in neighbors.get(var, []))

    def forward_check(var, val, assignment):
        removed = {}
        for n in neighbors.get(var, []):
            if n not in assignment:
                removed[n] = [v for v in domains[n] if v == val]
                for v in removed[n]:
                    domains[n].remove(v)
                if not domains[n]:
                    for k, vs in removed.items():
                        domains[k].extend(vs)
                    return None
        return removed

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment
        var = min((v for v in variables if v not in assignment), key=lambda v: len(domains[v]))
        for val in list(domains[var]):
            if is_consistent(var, val, assignment):
                assignment[var] = val
                removed = forward_check(var, val, assignment)
                if removed is not None:
                    result = backtrack(assignment)
                    if result:
                        return result
                del assignment[var]
                if removed:
                    for k, vs in removed.items():
                        domains[k].extend(vs)
        return None

    return backtrack({})


variables = ['WA', 'NT', 'SA', 'Queensland', 'NSW', 'V', 'T']
colors = ['Red', 'Green', 'Blue', 'Yellow']
neighbors = {
    'WA':         ['NT', 'SA'],
    'NT':         ['WA', 'SA', 'Queensland'],
    'SA':         ['WA', 'NT', 'Queensland', 'NSW', 'V'],
    'Queensland': ['NT', 'SA', 'NSW'],
    'NSW':        ['SA', 'Queensland', 'V'],
    'V':          ['SA', 'NSW'],
    'T':          []
}

solution = solve(variables, {v: list(colors) for v in variables}, neighbors)

if solution:
    print(f"{'State':<15} Color")
    print("-" * 25)
    for v in variables:
        print(f"  {v:<13} {solution[v]}")
    valid = all(solution[s] != solution[n] for s, ns in neighbors.items() for n in ns)
    print("\n  All constraints satisfied! ✓" if valid else "\n  CONFLICT found!")
else:
    print("No solution found.")