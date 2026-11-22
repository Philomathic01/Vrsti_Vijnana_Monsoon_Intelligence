# Vṛṣṭi-Vijñāna — Monsoon Intelligence v2

**Bilingual Hindi + English · 7 pages · India reference map · genuine historical ML evaluation**

Built from the team's existing IIT Indore Sustainability Hackathon 2026 prototype. All rainfall records, evaluation routines and original traditional-rule CSV are included in this ZIP.

## Run

Requires **Python 3.10–3.13**, with internet available **once** to install packages.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open **http://localhost:8501** (or the URL printed in the terminal). Windows users can double-click `run_windows.bat` after installation. Mac/Linux: `bash run_mac_linux.sh`.

No API key or external data service is required after packages are installed. Maps, data, and graphics are bundled; HTML screenshots/export depend only on local Plotly.

## Seven pages

1. **Dashboard** — bilingual hero, KPI cards, regional anomaly bars, 146-year rainfall trend and comparison.
2. **Monsoon Atlas** — interactive offline India reference outline with five *illustrative marker locations*, selected-region metrics and two-year comparisons. The All-India aggregate is shown separately elsewhere. **No invented region polygons, state or district rainfall values.**
3. **Historical Analysis** — year window, rainfall trend, 11-year mean, monthly distribution, anomaly heatmap and extreme-season tables.
4. **AI Model Lab** — 1996–2016 held-out MAE/RMSE/F1, observed-vs-hindcast plots, individual hindcast lookup, Ridge coefficients, CSV export. Models use Jan–May rainfall and three prior JJAS seasons, not target-year JJAS.
5. **Traditional Knowledge** — all 49 user-supplied CSV records, search, filters, original source passages, notes, and research-validation plan. Claims are **unverified**.
6. **Insights & Reports** — simple bilingual historical interpretation, CSV export and editable Markdown report download.
7. **Methodology** — data/units, features, holdout design, limitations, clear experimental status.

Controls for **language, historical year and rainfall region** live in the shared left sidebar and work across all pages.

## Scientific caveats

- Source: `data/raw/homogeneous_rainfall_1871_2016.txt`; **876 rows** (6 series × 146 years). The raw source is in **tenths of millimetres**, and the cleaned data is in millimetres.
- All India overlaps the five regional series; they are *not* six disjoint zones. Regional marker locations on the map are approximate **label anchors**, not measurement sites or region boundaries. Country outline is Natural Earth low-res reference data, not a substitute for official political or IMD geospatial boundaries.
- Fixed training-era seasonal reference 1871–1995; training years for lagged ML 1874–1995; untouched evaluation 1996–2016. The ±10% rainfall classes are **illustrative**, not official drought classifications.
- Forecast cutoff is assumed to be **31 May**. The ML inputs are rainfall-history features only. Verified ENSO/IOD, precession-adjusted astronomical features, future forecasts, and the hybrid model are **not** implemented or claimed.
- Traditional knowledge CSV source attributions and scientific validity require independent verification. Source passages are deliberately shown as given; surrounding UI can be switched to Hindi.
- Existing separately supplied historical archives are preserved in `data/raw` but are not automatically combined into the primary dataset.

## Scientific and functional checks

```bash
python -m unittest discover -s tests -v
python -m src.data
python -m generate_report
```

The original `src/data.py`, `src/models.py`, `generate_report.py`, and `tests/test_mvp.py` are retained from v1 to preserve reproducibility. Additional v2 tests cover map geometry, report generation, and chart builders.

## Tech stack

Streamlit native `st.navigation` / `st.Page`, Plotly offline charts, pandas, scikit-learn. No paid APIs. All UI code is directly editable.

## Future experiments

1. Acquire issue-date-correct ENSO/IOD and other conventional meteorological predictor series.
2. Carefully formalize a few source-verified astronomical rules into date-aligned features.
3. Compare **A: climate-only**, **B: climate plus traditional indicators**, and **C: climate plus randomised control**, with predeclared validation and holdout years.
4. Add official rainfall grids and trustworthy boundaries before making gridded or district-level maps.
