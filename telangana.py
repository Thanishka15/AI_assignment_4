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


neighbors = {
    'Adilabad':                ['KumurambheemAsifabad', 'Nirmal', 'Mancherial'],
    'KumurambheemAsifabad':    ['Adilabad', 'Mancherial'],
    'Mancherial':              ['Adilabad', 'KumurambheemAsifabad', 'Jagtial', 'Peddapalli', 'Nirmal'],
    'Nirmal':                  ['Adilabad', 'Mancherial', 'Nizamabad', 'Kamareddy', 'Jagtial'],
    'Nizamabad':               ['Nirmal', 'Kamareddy', 'Medak', 'Siddipet', 'Rajanna_Sircilla', 'Jagtial'],
    'Jagtial':                 ['Nirmal', 'Mancherial', 'Nizamabad', 'Karimnagar', 'Peddapalli', 'Rajanna_Sircilla'],
    'Peddapalli':              ['Mancherial', 'Jagtial', 'Karimnagar', 'Jayashankar_Bhupalpally', 'Mulugu'],
    'Karimnagar':              ['Jagtial', 'Peddapalli', 'Rajanna_Sircilla', 'Siddipet', 'Jayashankar_Bhupalpally'],
    'Rajanna_Sircilla':        ['Nizamabad', 'Jagtial', 'Karimnagar', 'Siddipet'],
    'Kamareddy':               ['Nirmal', 'Nizamabad', 'Medak', 'Sangareddy'],
    'Mulugu':                  ['Peddapalli', 'Jayashankar_Bhupalpally', 'Mahabubabad', 'BhadradiKothagudem', 'Hanamkonda'],
    'Jayashankar_Bhupalpally': ['Peddapalli', 'Karimnagar', 'Mulugu', 'Hanamkonda', 'Siddipet'],
    'Medak':                   ['Kamareddy', 'Nizamabad', 'Sangareddy', 'Siddipet', 'Medchal_Malkajgiri'],
    'Siddipet':                ['Nizamabad', 'Rajanna_Sircilla', 'Karimnagar', 'Jayashankar_Bhupalpally', 'Medak', 'Sangareddy', 'Yadadri_Bhongir', 'Jangaon'],
    'Jangaon':                 ['Siddipet', 'Hanamkonda', 'Yadadri_Bhongir', 'Medchal_Malkajgiri'],
    'Hanamkonda':              ['Jayashankar_Bhupalpally', 'Mulugu', 'Mahabubabad', 'Jangaon', 'Siddipet'],
    'Mahabubabad':             ['Hanamkonda', 'Mulugu', 'BhadradiKothagudem', 'Khammam', 'Suryapet', 'Jangaon'],
    'BhadradiKothagudem':      ['Mulugu', 'Mahabubabad', 'Khammam'],
    'Khammam':                 ['BhadradiKothagudem', 'Mahabubabad', 'Suryapet', 'Nalgonda'],
    'Rangareddy':              ['Vikarabad', 'Hyderabad', 'Medchal_Malkajgiri', 'Yadadri_Bhongir', 'Mahabubnagar', 'Nagarkurnool', 'Nalgonda'],
    'Hyderabad':               ['Rangareddy', 'Medchal_Malkajgiri', 'Sangareddy'],
    'Medchal_Malkajgiri':      ['Medak', 'Sangareddy', 'Hyderabad', 'Rangareddy', 'Jangaon', 'Yadadri_Bhongir'],
    'Yadadri_Bhongir':         ['Medchal_Malkajgiri', 'Jangaon', 'Siddipet', 'Rangareddy', 'Nalgonda', 'Suryapet'],
    'Suryapet':                ['Yadadri_Bhongir', 'Mahabubabad', 'Khammam', 'Nalgonda'],
    'Nalgonda':                ['Yadadri_Bhongir', 'Suryapet', 'Khammam', 'Rangareddy', 'Mahabubnagar', 'Nagarkurnool'],
    'Mahabubnagar':            ['Rangareddy', 'Nalgonda', 'Nagarkurnool', 'Wanaparthy', 'Narayanpet'],
    'Narayanpet':              ['Mahabubnagar', 'Wanaparthy', 'Jogulamba_Gadwal'],
    'Jogulamba_Gadwal':        ['Narayanpet', 'Wanaparthy', 'Nagarkurnool'],
    'Wanaparthy':              ['Mahabubnagar', 'Narayanpet', 'Jogulamba_Gadwal', 'Nagarkurnool'],
    'Nagarkurnool':            ['Mahabubnagar', 'Nalgonda', 'Rangareddy', 'Wanaparthy', 'Jogulamba_Gadwal'],
    'Vikarabad':               ['Rangareddy', 'Sangareddy'],
    'Sangareddy':              ['Kamareddy', 'Medak', 'Vikarabad', 'Hyderabad', 'Medchal_Malkajgiri'],
}

colors = ['Red', 'Green', 'Blue', 'Yellow', 'Orange']
solution = solve(list(neighbors.keys()), {v: list(colors) for v in neighbors}, neighbors)

if solution:
    print(f"{'District':<30} Color")
    print("-" * 40)
    for d in neighbors:
        print(f"  {d:<28} {solution[d]}")
    valid = all(solution[d] != solution[n] for d, ns in neighbors.items() for n in ns if n in solution)
    print("\n  All constraints satisfied! ✓" if valid else "\n  CONFLICT found!")
else:
    print("No solution found.")