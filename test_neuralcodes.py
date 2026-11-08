"""
Tests on codes whose answers are stated in the papers.
Run:  python3 test_neuralcodes.py
"""
from neuralcodes import *

def check(name, condition):
    print(("PASS  " if condition else "FAIL  ") + name)
    assert condition, name

# Wheels paper, Example 2.7: C* is its own minimal code, has no local obstruction,
# and is NOT max-intersection-complete (codeword 1 is missing, and 1 is not mandatory).
C_star = parse_short(["2345", "123", "134", "145", "13", "14", "23", "34", "45", "3", "4"])
check("C* equals its minimal code", minimal_code(facets(C_star)) == C_star)
check("C* has no local obstruction", not has_local_obstruction(C_star))
check("C* not max-intersection-complete", not is_max_intersection_complete(C_star))
check("link of 1 in C* is contractible (a path)", link_is_contractible(frozenset({1}), facets(C_star))[0])

# Ahmed et al. Example 2.25: C24 is the minimal code of its complex.
C24 = parse_short(["123", "1246", "145", "356", "12", "14", "3", "5", "6"])
check("C24 equals its minimal code", minimal_code(facets(C24)) == C24)

# Wheels paper, Prop 4.13: C_TL has no local obstructions, 4 is not mandatory.
C_TL = parse_short(["123", "145", "245", "246", "346", "24", "45", "46", "1", "2", "3"])
check("C_TL equals its minimal code", minimal_code(facets(C_TL)) == C_TL)
check("4 not mandatory in C_TL", frozenset({4}) not in mandatory_faces(facets(C_TL)))

# Wheels paper, Example 2.6: convex, not max-intersection-complete, 1 not mandatory.
ex26 = parse_short(["123", "134", "145", "13", "14"])
check("Example 2.6 equals its minimal code", minimal_code(facets(ex26)) == ex26)

# Wheels paper, Example 4.17: {12,13,23,1,2} HAS a local obstruction (3 is mandatory, missing).
ex417 = parse_short(["12", "13", "23", "1", "2"])
check("Example 4.17 has a local obstruction", has_local_obstruction(ex417))
check("3 is mandatory in Example 4.17", frozenset({3}) in mandatory_faces(facets(ex417)))

# A max-intersection-complete code: add 1 to C*.
check("C* + {1} is max-intersection-complete",
      is_max_intersection_complete(C_star | {frozenset({1})}))

# Homology sanity: hollow triangle has one 1-dim hole; filled triangle has none.
hollow = [frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3})]
check("hollow triangle not collapsible", not is_collapsible(hollow))
check("hollow triangle has a 1-cycle", reduced_betti_gf2(hollow) == [0, 0, 1])
check("filled triangle collapsible", is_collapsible([frozenset({1, 2, 3})]))
check("two points: not collapsible", not is_collapsible([frozenset({1}), frozenset({2})]))

# Canonical form: a relabeled copy matches, a different code does not.
swapped = {frozenset({ {1: 2, 2: 1}.get(i, i) for i in c}) for c in C24}
check("relabeled C24 matches C24", canonical(swapped) == canonical(C24))
check("C24 differs from C_TL", canonical(C24) != canonical(C_TL))

print("\nAll tests passed.")
