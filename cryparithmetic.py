from itertools import permutations

print("     S E N D")
print("   + M O R E")
print("   ---------")
print("   M O N E Y\n")

letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
for perm in permutations(range(10), len(letters)):
    a = dict(zip(letters, perm))
    if a['S'] == 0 or a['M'] == 0:
        continue
    SEND  = 1000*a['S'] + 100*a['E'] + 10*a['N'] + a['D']
    MORE  = 1000*a['M'] + 100*a['O'] + 10*a['R'] + a['E']
    MONEY = 10000*a['M'] + 1000*a['O'] + 100*a['N'] + 10*a['E'] + a['Y']
    if SEND + MORE == MONEY:
        print(f"{'Letter':<8} Digit")
        print("-" * 16)
        for l in letters:
            print(f"  {l:<6} {a[l]}")
        print(f"\n  {SEND} + {MORE} = {MONEY}  ✓")
        break