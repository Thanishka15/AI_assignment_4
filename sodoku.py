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


puzzle = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7],
]

def print_grid(grid, label):
    print(f"\n{label}:")
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("  ------+-------+------")
        line = "  "
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                line += "| "
            line += (str(val) if val != 0 else ".") + " "
        print(line)

print_grid(puzzle, "Initial Puzzle")

cells = [(r, c) for r in range(9) for c in range(9)]
domains = {(r, c): [puzzle[r][c]] if puzzle[r][c] else list(range(1, 10)) for r, c in cells}

def cell_neighbors(r, c):
    nbrs = {(r, col) for col in range(9) if col != c}
    nbrs |= {(row, c) for row in range(9) if row != r}
    br, bc = 3 * (r // 3), 3 * (c // 3)
    nbrs |= {(br+dr, bc+dc) for dr in range(3) for dc in range(3) if (br+dr, bc+dc) != (r, c)}
    return list(nbrs)

neighbors = {(r, c): cell_neighbors(r, c) for r, c in cells}
solution = solve(cells, domains, neighbors)

if solution:
    result = [[solution[(r, c)] for c in range(9)] for r in range(9)]
    print_grid(result, "Solved Sudoku")
    print("\n  Solved successfully! ✓")
else:
    print("No solution found.")