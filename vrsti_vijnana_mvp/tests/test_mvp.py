from pathlib import Path
import unittest
import numpy as np
from src.data import load_rainfall, annual_with_anomaly, load_rules, REGIONS
from src.models import build_results, make_features, FEATURES

class TestMonsoonPrototype(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rain = load_rainfall()
        cls.pred, cls.metrics, cls.trained = build_results(cls.rain)

    def test_data_coverage_and_units(self):
        self.assertEqual(len(self.rain), 876)
        self.assertEqual(set(self.rain.region), set(REGIONS))
        self.assertEqual(self.rain.year.min(), 1871)
        self.assertEqual(self.rain.year.max(), 2016)
        # All-India 1871 JJAS original file=8487 tenths mm -> 848.7 mm.
        self.assertAlmostEqual(float(self.rain.query("region == 'All India' and year == 1871").iloc[0].JJAS), 848.7)

    def test_jjas_is_sum_of_june_september(self):
        month_sum = self.rain[["JUN","JUL","AUG","SEP"]].sum(axis=1)
        self.assertLessEqual(float((month_sum - self.rain.JJAS).abs().max()),0.21)

    def test_rules(self):
        self.assertEqual(len(load_rules()), 49)

    def test_target_year_monsoon_not_in_features(self):
        forbidden = {"JUN","JUL","AUG","SEP","JJAS","ANN","OND"}
        self.assertFalse(forbidden.intersection(FEATURES))
        df = make_features(self.rain)
        one = df.query("region == 'All India' and year == 2002").iloc[0]
        prior = self.rain.query("region == 'All India' and year == 2001").iloc[0]
        self.assertAlmostEqual(float(one.jj_lag1), float(prior.JJAS))

    def test_sealed_holdout_and_hindcast_cardinality(self):
        self.assertEqual(set(self.pred.year), set(range(1996, 2017)))
        self.assertEqual(len(self.pred), 6 * 21 * 4)
        self.assertTrue((self.pred.observed_mm >= 0).all())
        self.assertTrue((self.pred.predicted_mm >= 0).all())
        self.assertEqual(len(self.metrics), 6 * 4)

    def test_fixed_reference_is_training_only(self):
        anomalized = annual_with_anomaly(self.rain)
        ai = anomalized.query("region=='All India' and year==2002").iloc[0]
        train_mean = self.rain.query("region=='All India' and year <= 1995").JJAS.mean()
        self.assertAlmostEqual(float(ai.reference_mm), float(train_mean))
        score_mean = self.pred.query("region=='All India' and model=='Climatology'").predicted_mm.unique()
        self.assertEqual(len(score_mean), 1)
        self.assertAlmostEqual(float(score_mean[0]), float(train_mean), places=3)

if __name__ == '__main__':
    unittest.main()
