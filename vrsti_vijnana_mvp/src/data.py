"""Documented, unit-aware parser for the supplied IMD homogeneous rainfall text file.

Important: These data are large regional aggregates, not administrative boundaries
or gridded rainfall. The original source labels rainfall as 'in 10th of mm'.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
SECTIONS = {
    "ALL-INDIA": "All India",
    "NORTHWEST INDIA": "Northwest India",
    "WEST CENTRAL INDIA": "West Central India",
    "NORTHEAST INDIA": "Northeast India",
    "CENTRAL NORTHEAST INDIA": "Central Northeast India",
    "PENINSULAR INDIA": "Peninsular India",
}
REGIONS = [
    "All India",
    "Northwest India",
    "West Central India",
    "Northeast India",
    "Central Northeast India",
    "Peninsular India",
]
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
FIELDS = MONTHS + ["JF", "MAM", "JJAS", "OND", "ANN"]


def create_clean_rainfall(source: Path | None = None, destination: Path | None = None) -> pd.DataFrame:
    source = Path(source or RAW / "homogeneous_rainfall_1871_2016.txt")
    destination = Path(destination or DATA / "rainfall_clean_mm.csv")
    lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
    current = None
    entries: list[dict] = []
    for line in lines:
        label_match = re.match(r"^\s*146\s+(.+?)\s+RAINFALL\s*\(1871-2016\)", line, flags=re.I)
        if label_match:
            label = re.sub(r"\s+", " ", label_match.group(1).strip().upper())
            if label not in SECTIONS:
                raise ValueError(f"Unexpected source region: {label}")
            current = SECTIONS[label]
            continue
        if not current or not re.match(r"^\s*(18\d\d|19\d\d|20\d\d)\s+", line):
            continue
        pieces = line.strip().split()
        if len(pieces) != 18:
            raise ValueError(f"Unexpected data width for {current}: {pieces[:5]} ({len(pieces)} fields)")
        year = int(pieces[0])
        values = [float(n) / 10.0 for n in pieces[1:]]  # explicit tenths-of-mm → mm
        row = {"region": current, "year": year}
        row.update(dict(zip(FIELDS, values)))
        entries.append(row)
    df = pd.DataFrame(entries).sort_values(["region", "year"]).reset_index(drop=True)
    if len(df) != 6 * 146 or set(df.region) != set(REGIONS):
        raise ValueError(f"Expected 876 observations from six regions; got {len(df)}")
    for region in REGIONS:
        years = set(df.loc[df.region == region, "year"])
        if years != set(range(1871, 2017)):
            raise ValueError(f"Incomplete 1871–2016 coverage for {region}")
    # Derived JJAS totals nearly match the rounded series; allow 0.2 mm rounding tolerance
    difference = (df[["JUN", "JUL", "AUG", "SEP"]].sum(axis=1) - df["JJAS"]).abs()
    if (difference > 0.21).any():
        bad = df.loc[difference > 0.21, ["region", "year", "JJAS"]]
        raise ValueError(f"JJAS integrity mismatch: {bad.head(5).to_dict('records')}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False, float_format="%.1f")
    return df


def load_rainfall() -> pd.DataFrame:
    path = DATA / "rainfall_clean_mm.csv"
    if not path.is_file():
        return create_clean_rainfall()
    return pd.read_csv(path)


def load_rules() -> pd.DataFrame:
    df = pd.read_csv(RAW / "traditional_rules.csv", encoding="utf-8-sig").fillna("")
    df.insert(0, "Rule ID", [f"TEK-{n:02d}" for n in range(1, len(df) + 1)])
    return df


def risk_label(anomaly_pct: float, threshold: float = 10.0) -> str:
    if anomaly_pct < -threshold:
        return "Below normal"
    if anomaly_pct > threshold:
        return "Above normal"
    return "Near normal"


def annual_with_anomaly(data: pd.DataFrame, reference_end_year: int = 1995) -> pd.DataFrame:
    """Anomaly relative to 1871–1995 training-era per-region reference (fixed)."""
    means = (data[(data.year >= 1871) & (data.year <= reference_end_year)]
             .groupby("region")["JJAS"].mean().rename("reference_mm"))
    df = data.join(means, on="region")
    df["anomaly_pct"] = (df["JJAS"] / df["reference_mm"] - 1) * 100
    df["rainfall_class"] = df["anomaly_pct"].apply(risk_label)
    return df


if __name__ == "__main__":
    d = create_clean_rainfall()
    print(f"Prepared {len(d)} records, {d.region.nunique()} regions; years {d.year.min()}-{d.year.max()}")
    print(f"Rules available: {len(load_rules())}")
