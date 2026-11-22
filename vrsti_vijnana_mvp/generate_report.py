"""Recompute evaluation CSVs from the packaged raw (and cleaned) data."""
from pathlib import Path
from src.data import load_rainfall, load_rules, annual_with_anomaly
from src.models import build_results

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

if __name__ == "__main__":
    observations = load_rainfall()
    holdout, summary, _ = build_results(observations)
    holdout.to_csv(REPORTS / "holdout_predictions.csv", index=False)
    summary.to_csv(REPORTS / "evaluation_by_region.csv", index=False)
    (REPORTS / "model_scores_preview.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(f"Historical observations: {len(observations)}; TEK rule entries: {len(load_rules())}")
    print(summary.query("region=='All India'").to_string(index=False))
    print("Results saved in reports/")
