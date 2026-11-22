# Vṛṣṭi-Vijñāna — 3-minute hackathon demonstration (v2)

**0:00–0:30 · Home Dashboard**

“Vṛṣṭi-Vijñāna is a bilingual monsoon-intelligence research platform. It uses 146 years of regional rainfall records to explain climate variability, benchmark AI models, and objectively test possible additional information from traditional Indian astronomical meteorology.”

Set global year to **2002** and region to **Northwest India**. Show the national vs regional historical anomaly chart. These are **observations**, not predictions.

**0:30–1:05 · Monsoon Atlas**

Switch to the Atlas. Hover the Northwest and Northeast regional markers. Say: “The reference India outline and labels aid navigation; the markers are not rainfall-zone boundaries. Our next data step is validated IMD gridded rainfall for spatial maps.”

**1:05–1:35 · Historical Analysis**

Show the monsoon trend, monthly profile and year-by-region anomaly heatmap. Explain that source data were converted from **tenths of mm to mm** and anomalies are calculated against a fixed **1871–1995 reference**.

**1:35–2:20 · AI Model Lab**

Show the 1996–2016 holdout model comparison; on All India, **Climatology MAE 63.06 mm**, Ridge **66.34 mm**, Random Forest **70.01 mm**. “These rainfall-history-only ML models do not necessarily beat climatology; this is why the proposed climate-plus-traditional-feature hypothesis needs rigorous ablation rather than assumed gains.”

**2:20–2:45 · Traditional Knowledge**

Show an original rule, its attributed source and its “Not scientifically validated” status. Explain the proposed A/B/C controlled experiment: **A conventional ENSO/IOD predictors, B adds calendar-corrected rules, C adds matched random controls**. This is a **planned experiment**, not a result of the existing historical model.

**2:45–3:00 · Language + Reports**

Switch to Hindi; show translated UI. Open Insights & Reports and export an editable bilingual historical summary. “The intended users are communities and planners who need understandable, transparent climate-risk context. This is a research prototype, not a replacement for IMD warnings.”

## Backup / anticipated judge questions

- **Is this a forecast for 2026?** No. Available rainfall data end in 2016. Historical hindcasts cover 1996–2016.
- **Is traditional astrology proven?** No. Rules are falsifiable hypotheses; the feature-ablation experiment has not yet been run.
- **Are regional locations official boundaries?** No. The map intentionally uses schematic anchors on a Natural Earth reference outline; detailed polygons and rainfall grids require sourced geodata.
- **Which model wins?** For the All-India holdout shown here, climatology has lower MAE. We show negative results openly.
- **Can it run without internet?** Yes, after installing the Python packages. Data and map shape are bundled.
