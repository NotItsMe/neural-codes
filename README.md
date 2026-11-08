# neural-codes

Working code for my project on the 96 open neural codes of Remark 2.33 ([arXiv:2510.20323](https://arxiv.org/abs/2510.20323)): 6 neurons, 5 maximal codewords each, convexity unknown.

The finished results (certificates, exact checker, interactive viewer) are in [neural-codes-96](https://github.com/NotItsMe/neural-codes-96). This repo is the toolkit and the raw results bundle behind them.

## Files

- `neuralcodes.py`: exact helpers for combinatorial codes (facets, minimal codes, links, local obstructions, relabelings). No floating point.
- `box_checker.py`: the referee for box drawings. Given one open box per neuron, it finds every overlap pattern exactly (Fractions) and compares it with the target code.
- `validate_96.py`: six checks on `jeffs_96_codes.json` before any search runs. Output is in `validation_report.txt` (all checks pass).
- `test_neuralcodes.py`, `test_box_checker.py`: tests on codes whose answers are stated in the papers.
- `neural-codes-results-2026-11-07.tar.gz`: the full Nov 7 bundle. Certificates, SAT / exact / 3D polytope search results, the non-planarity proofs, every search and checker script, and the 96-code list.

## Run

```
python3 test_neuralcodes.py
python3 test_box_checker.py
mkdir results && tar -xzf neural-codes-results-2026-11-07.tar.gz -C results
cd results && python3 validate_96.py jeffs_96_codes.json
```

Plain Python 3, no installs needed for these. Some scripts inside the bundle use `z3-solver`.

Zaid Mohammed
