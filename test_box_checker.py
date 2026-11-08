"""
Tests for the referee. Run:  python3 test_box_checker.py
Each drawing below was worked out by hand, so I know the right answer in advance.
"""
from box_checker import check, show

def code(*words):
    return [[int(ch) for ch in w] for w in words]

def expect(name, target, cert, should_pass, extra=None, missing=None):
    ok, miss, ext, _ = check(target, cert)
    good = ok == should_pass
    if extra is not None:
        good &= show(ext) == extra
    if missing is not None:
        good &= show(miss) == missing
    print(("PASS  " if good else "FAIL  ") + name +
          ("" if ok else f"   (missing {show(miss)}, extra {show(ext)})"))
    assert good, name

# 1. Tiny 1D example: two overlapping intervals give {1}, {12}, {2}.
expect("two intervals", code("1", "12", "2"),
       {1: [[0, 4]], 2: [[2, 6]]}, True)

# 2. The sliver trap: 1=(0,2), 2=(2,4), 3=(0,4). The point x=2 is in 3 only -> extra {3}.
expect("boundary sliver is caught", code("13", "23"),
       {1: [[0, 2]], 2: [[2, 4]], 3: [[0, 4]]}, False, extra=["3"])

# 3. Ahmed et al. Example 2.29: C_min = {134, 1357, 356, 13, 35} as a 1D path of regions
#    134 | 13 | 1357 | 35 | 356.
c229 = code("134", "13", "1357", "35", "356")
expect("Example 2.29 path realization", c229,
       {1: [[0, 3]], 3: [[0, 5]], 4: [[0, 1]], 5: [[2, 5]], 6: [[4, 5]], 7: [[2, 3]]}, True)

# 4. Wheels paper Example 2.6: {123,134,145,13,14} is convex; 1D drawing 123|13|134|14|145.
ex26 = code("123", "134", "145", "13", "14")
good26 = {1: [[0, 5]], 2: [[0, 1]], 3: [[0, 3]], 4: [[2, 5]], 5: [[4, 5]]}
expect("Example 2.6 realization", ex26, good26, True)

# 5. Same code, but 3 and 4 now just touch at x=2 instead of overlapping:
#    the point x=2 is covered by 1 only, so the forbidden codeword {1} appears.
bad26 = dict(good26); bad26[3] = [[0, 2]]
expect("Example 2.6 broken: touching boxes leak {1}", ex26, bad26, False, extra=["1"])

# 6. Ahmed et al. Example 3.11, C18^b T-shaped 2D realization:
#    {123, 1346, 145, 67, 13, 14, 6}.
c18b = code("123", "1346", "145", "67", "13", "14", "6")
t_shape = {1: [[0, 5], [2, 3]], 2: [[0, 1], [2, 3]], 3: [[0, 3], [2, 3]],
           4: [[2, 5], [2, 3]], 5: [[4, 5], [2, 3]],
           6: [[2, 3], [0, 3]], 7: [[2, 3], [0, 1]]}
expect("C18^b T-shape (2D)", c18b, t_shape, True)

# 7. Same T-shape with neuron 7 pushed out of neuron 6: codeword 67 goes missing, 7 appears.
broken = dict(t_shape); broken[7] = [[3, 4], [0, 1]]
expect("C18^b broken: 67 missing, 7 extra", c18b, broken, False, extra=["7"], missing=["67"])

# 8. Fractions work, not just integers.
expect("fractional coordinates", code("1", "12", "2"),
       {1: [["0", "1/3"]], 2: [["1/7", "1/2"]]}, True)

print("\nAll referee tests passed.")
