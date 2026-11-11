#!/usr/bin/env python3
"""
Rebuild everything: run the analysis, then every table script and every figure script, then compile the
Word files used for submission (All_Tables.docx, All_Figures.docx, Supplementary_Material.docx).

Run: python scripts/make_all.py [--force]   (--force re-runs the analysis even if a cache exists)
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _bootstrap import OUT, core, load_results  # noqa: E402

TITLE = ("Nested geography of health inequality: environmental deprivation, development inequality and the "
         "uneven pursuit of SDG 3 across Sub-Saharan Africa")


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    R = load_results(force=a.force)
    json.dump(core.headline_numbers(R), open(OUT / "results.json", "w"), indent=1, ensure_ascii=False)
    main_tabs, supp_tabs = {}, {}
    for p in sorted((HERE / "tables").glob("table_*.py")):
        tbl = load(p).main()
        (supp_tabs if tbl[0].startswith("Table S") else main_tabs)[tbl[0]] = tbl
    order = lambda d: dict(sorted(d.items(), key=lambda kv: int(kv[0].split()[-1].lstrip("S"))))
    main_tabs, supp_tabs = order(main_tabs), order(supp_tabs)
    for p in sorted((HERE / "figures").glob("*.py")):
        load(p).main()
    docx = OUT / "docx"; docx.mkdir(parents=True, exist_ok=True)
    figs = OUT / "figures"
    core.write_tables_docx(main_tabs, docx / "All_Tables.docx")
    core.write_figures_docx(figs, [f"Figure_{i}" for i in range(1, 9)], docx / "All_Figures.docx")
    core.write_supplement_docx(supp_tabs, figs, docx / "Supplementary_Material.docx", TITLE)
    print("Word files:", docx)


if __name__ == "__main__":
    main()
