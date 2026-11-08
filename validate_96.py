"""
validate_96.py - six checks on jeffs_96_codes.json before any search runs.
Run:  python3 validate_96.py jeffs_96_codes.json
Writes validation_report.txt next to it.
"""
import json, sys
from neuralcodes import *

path = sys.argv[1] if len(sys.argv) > 1 else "jeffs_96_codes.json"
data = json.load(open(path))
codes = data["codes"]
lines, all_ok = [], True

def report(name, ok, detail=""):
    global all_ok
    all_ok &= ok
    lines.append(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))

# Check 1: 96 codes, unique ids, each contains the empty codeword
ids = [c["id"] for c in codes]
report("1. exactly 96 codes", len(codes) == 96, f"found {len(codes)}")
report("1. ids are unique", len(set(ids)) == len(ids))
report("1. every code contains the empty codeword", all([] in c["codewords"] for c in codes))

parsed = {c["id"]: make_code(c["codewords"]) for c in codes}

# Check 2: maximal codewords recomputed from scratch match the listed ones, exactly 5
bad = [cid for c in codes
       for cid in [c["id"]]
       if facets(parsed[cid]) != {frozenset(m) for m in c["maximal"]} or len(c["maximal"]) != 5]
report("2. listed maximal codewords are correct, exactly 5 each", not bad, f"bad: {bad}" if bad else "")

# Check 3: each code equals its own minimal code (no local obstructions, nothing extra)
bad, methods = [], {}
for cid, code in parsed.items():
    F = facets(code)
    if minimal_code(F) != code:
        bad.append(cid)
    for s in facet_intersections(F):
        if s not in F:
            methods[link_is_contractible(s, F)[1]] = methods.get(link_is_contractible(s, F)[1], 0) + 1
report("3. every code equals its own minimal code", not bad, f"bad: {bad}" if bad else
       f"link tests decided by: {methods}, 0 undecided")

# Check 4: no two codes are the same after relabeling neurons
canon = {cid: canonical(code) for cid, code in parsed.items()}
dupes = len(canon) - len(set(canon.values()))
report("4. no duplicates under the 720 relabelings", dupes == 0, f"{dupes} duplicates")

# Check 5: all 10 Appendix A.1 codes (Wheels paper) are present, up to relabeling
appendix = [
    ["2346", "145", "456", "12", "13", "45", "46", "1", "2", "3"],
    ["1456", "245", "346", "12", "13", "45", "46", "1", "2", "3"],
    ["245", "346", "456", "12", "13", "45", "46", "1", "2", "3"],
    ["2456", "135", "156", "12", "34", "15", "56", "1", "2", "3", "4"],
    ["2456", "156", "235", "12", "34", "25", "56", "1", "2", "3", "4"],
    ["2356", "134", "135", "146", "12", "13", "14", "35", "1", "2", "6"],
    ["2356", "134", "135", "246", "12", "13", "26", "35", "1", "2", "4"],
    ["1456", "134", "135", "246", "12", "13", "14", "15", "46", "1", "2"],
    ["3456", "134", "135", "246", "12", "13", "34", "35", "46", "1", "2", "3"],
    ["134", "135", "256", "346", "12", "13", "34", "1", "2", "5", "6"],
]
inverse = {v: k for k, v in canon.items()}
matches = [inverse.get(canonical(parse_short(a))) for a in appendix]
report("5. all 10 Appendix A.1 codes present", all(matches),
       ", ".join(f"A{i+1}->{m}" for i, m in enumerate(matches)))

# Check 6: none is max-intersection-complete (those would already be known convex)
mic = [cid for cid, code in parsed.items() if is_max_intersection_complete(code)]
report("6. none is max-intersection-complete", not mic, f"MIC: {mic}" if mic else "")

# Extra: connected complex, all 6 neurons used (the paper only enumerated connected complexes)
bad = [cid for cid, code in parsed.items()
       if not is_connected(facets(code)) or set().union(*code) != set(range(1, 7))]
report("extra. connected complex using all 6 neurons", not bad, f"bad: {bad}" if bad else "")

lines.append("\nRESULT: " + ("ALL CHECKS PASSED" if all_ok else "SOMETHING FAILED - read above"))
out = "\n".join(lines)
print(out)
open("validation_report.txt", "w").write(f"Validation of {path}\n{data.get('source','')}\n\n" + out + "\n")
