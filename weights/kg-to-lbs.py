#!/usr/bin/env python3.9

import math

def to_lbs(weight_in_kg):
    return 2.20462 * weight_in_kg

_weights_in_kg = (0.125, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5)
_weights_in_lbs = tuple(map(to_lbs, _weights_in_kg))
target_weights_in_lbs= (2.5, 5.0)

# brute force solution (2**7! = 128 distinct solutions)
def find_best_combination(target_weight_in_lbs):
        
    min_val = math.inf
    arg_min = None
    for i in range(2**7):
        indices = tuple(k for k, v in enumerate(bin(i)[2:][::-1]) if v == '1')
        total = sum(_weights_in_lbs[k] for k in indices)
        diff = abs(total - target_weight_in_lbs)
        if diff < min_val or diff == min_val and (arg_min is None or len(indices) < len(arg_min[1])):
            min_val = diff
            arg_min = (i, indices)
    return tuple(_weights_in_kg[k] for k in arg_min[1])

for w in target_weights_in_lbs:
    best_combination = find_best_combination(w)
    w_in_kg = tuple(f'{kg}kg' for kg in best_combination)
    w_in_lbs = sum(map(to_lbs, best_combination))
    print(f'For {w}lbs use plates {w_in_kg} = {w_in_lbs}lbs')
    
