"""Package-level checks not dependent on having a graphical browser."""
from pathlib import Path
import json
import unittest
from src.data import load_rainfall,annual_with_anomaly,load_rules
from src.reports import report_markdown
from src.translations import TEXT

ROOT=Path(__file__).resolve().parents[1]

class TestVersion2(unittest.TestCase):
    def test_bilingual_keys(self):
        self.assertEqual(set(TEXT['en']),set(TEXT['hi']))
        self.assertGreater(len(TEXT['en']),85)
    def test_offline_geometry(self):
        p=ROOT/'assets'/'india_outline.geojson'
        self.assertTrue(p.is_file())
        geom=json.loads(p.read_text(encoding='utf-8'))['geometry']
        self.assertIn(geom['type'],('Polygon','MultiPolygon'))
        self.assertTrue(len(geom['coordinates'])>0)
    def test_bilingual_historical_report(self):
        rain=annual_with_anomaly(load_rainfall())
        row=rain.query('region=="Northwest India" and year==2002').iloc[0]
        for lang in ('en','hi'):
            report=report_markdown(row,lang)
            self.assertIn('2002',report)
            self.assertIn('279.7',report)
            self.assertIn('1995',report)
            self.assertTrue(len(report)>250)
    def test_evidence_is_not_2026_forecast(self):
        self.assertEqual(int(load_rainfall().year.max()),2016)
        self.assertEqual(len(load_rules()),49)
if __name__=='__main__':unittest.main()
