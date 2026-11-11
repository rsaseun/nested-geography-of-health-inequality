#!/usr/bin/env python3
"""
Step 0: run the full analysis (Sections 1-8 of src/sdg3_nested_geography/core.py) on the study workbook and
cache the results in outputs/cache/results.pkl. Every table and figure script reads this cache; if it is
missing they create it automatically, so running this step first is optional.

Run: python scripts/00_run_analysis.py [--boot 250] [--gapref 100]
"""
import argparse
import json
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _bootstrap import CACHE, DATA, OUT, core  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default=str(DATA))
    ap.add_argument("--boot", type=int, default=250, help="bootstrap draws per imputation (x 20 imputations)")
    ap.add_argument("--gapref", type=int, default=100, help="reference datasets for the gap statistic")
    a = ap.parse_args()
    R = core.run_analysis(a.data, boot=a.boot, gapref=a.gapref)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE, "wb") as fh:
        pickle.dump(R, fh)
    json.dump(core.headline_numbers(R), open(OUT / "results.json", "w"), indent=1, ensure_ascii=False)
    print("cached:", CACHE)
    print("headline numbers:", OUT / "results.json")


if __name__ == "__main__":
    main()
