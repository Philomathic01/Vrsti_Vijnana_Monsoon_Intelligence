"""Historical reports. Never imply that rainfall observations are forecasts."""
from __future__ import annotations
from src.data import risk_label
from src.translations import TEXT, REGION_KEY, RISK_KEY


def report_markdown(row,language='en'):
    tr=TEXT[language]
    region=tr[REGION_KEY[str(row['region'])]]
    cls=tr[RISK_KEY[risk_label(float(row['anomaly_pct']))]]
    year=int(row['year'])
    obs=float(row['JJAS']); normal=float(row['reference_mm']); anomaly=float(row['anomaly_pct'])
    msg = (
       'The selected historical season recorded rainfall below the fixed reference average.' if anomaly < -10 else
       'The selected historical season recorded rainfall above the fixed reference average.' if anomaly > 10 else
       'The selected historical season was close to the fixed reference average.'
    ) if language=='en' else (
       'चुने गए ऐतिहासिक मौसम में वर्षा संदर्भ औसत से कम रही।' if anomaly < -10 else
       'चुने गए ऐतिहासिक मौसम में वर्षा संदर्भ औसत से अधिक रही।' if anomaly > 10 else
       'चुने गए ऐतिहासिक मौसम में वर्षा संदर्भ औसत के आसपास रही।'
    )
    return (f'# {tr["app"]} — {tr["report_title"]}\n\n'
      f'- **{tr["region"]}:** {region}\n- **{tr["year"]}:** {year}\n'
      f'- **{tr["observed"]}:** {obs:.1f} mm\n'
      f'- **{tr["reference"]} (1871–1995):** {normal:.1f} mm\n'
      f'- **{tr["anomaly"]}:** {anomaly:+.1f}%\n'
      f'- **{tr["category"]}:** {cls}\n\n'
      f'## {tr["interpretation"]}\n{msg}\n\n'
      f'## {tr["impact"]}\n{tr["impact_hint"]}\n\n'
      f'---\n{tr["measurement"]}\n\n{tr["disclaimer"]}\n'
      f'{tr["classification_notice"]}\n')
