"""Shared start-up for every script: paths, cached results and output writers."""
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sdg3_nested_geography import core  # noqa: E402

DATA = ROOT / "data" / "Study_Data_Sources_updated_v1.xlsx"
OUT = ROOT / "outputs"
CACHE = OUT / "cache" / "results.pkl"
TABLES = OUT / "tables"
TABLES_DOCX = OUT / "tables_docx"
FIGURES = OUT / "figures"


def load_results(force=False):
    """Return the analysis results, running Sections 1-8 once and caching them in outputs/cache."""
    if CACHE.exists() and not force:
        with open(CACHE, "rb") as fh:
            return pickle.load(fh)
    R = core.run_analysis(DATA)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE, "wb") as fh:
        pickle.dump(R, fh)
    return R


def save_table(tbl):
    """Write one table as CSV and as a Word file (black text, horizontal rules only)."""
    label, title, df, note, landscape = tbl
    TABLES.mkdir(parents=True, exist_ok=True); TABLES_DOCX.mkdir(parents=True, exist_ok=True)
    stem = label.replace(" ", "_")
    df.to_csv(TABLES / f"{stem}.csv", index=False, encoding="utf-8-sig")
    core.write_tables_docx({stem: tbl}, TABLES_DOCX / f"{stem}.docx")
    print(f"{label}: {TABLES / (stem + '.csv')}")
    return tbl


def figure_path(name):
    FIGURES.mkdir(parents=True, exist_ok=True)
    return FIGURES / f"{name}.png"
