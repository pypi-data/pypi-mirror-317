# tests/test_data_processing.py

import unittest
import pandas as pd
import numpy as np
from your_library.data_processing import (
    load_and_merge_data,
    get_subject_and_scan_counts,
    drop_missing_data,
    filter_scans_by_parameters,
    filter_scans_by_quality,
    filter_scans_by_prediction_qa,
    remove_duplicates,
    select_earliest_scans,
    impute_missing_data
)

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.df_population = pd.DataFrame({
            'patient_id_tabs': ['P1', 'P2', 'P3'],
            'age': [65, 70, 75],
            'sex': ['Male', 'Female', 'Male'],
            'htn': [1, 0, 1],
            'dm': [0, 1, 0],
            'ethnicity_group': ['Group1', 'Group2', 'Group1']
        })

        self.df_tabs_automorph = pd.DataFrame({
            'patient_id_tabs': ['P1', 'P2', 'P3'],
            'eye': ['OD', 'OS', 'OD'],
            'date': ['2021-01-01', '2021-02-01', '2021-03-01'],
            'scan_field_mm': [6.0, 6.0, 7.0],
            'valid_pixels_percentage': [95, 94, 96],
            'signal_strength': [8, 7, 9],
            'quality': [60, 65, 70],
            'fovea_position': [0, 1, 0],
            'softmax_good_mean_qa': [0.9, 0.85, 0.88],
            'softmax_usable_mean_qa': [0.1, 0.15, 0.12]
        })

    def test_load_and_merge_data(self):
        # Since the function reads from CSV files, we'll simulate this by writing to temporary CSVs
        self.df_population.to_csv('temp_population.csv', index=False)
        self.df_tabs_automorph.to_csv('temp_tabs_automorph.csv', index=False)

        df_merged = load_and_merge_data(
            population_data_path='temp_population.csv',
            tabs_automorph_path='temp_tabs_automorph.csv'
        )

        self.assertIsInstance(df_merged, pd.DataFrame)
        self.assertEqual(len(df_merged), 3)
        self.assertIn('age', df_merged.columns)
        self.assertIn('scan_field_mm', df_merged.columns)

        # Clean up temporary files
        import os
        os.remove('temp_population.csv')
        os.remove('temp_tabs_automorph.csv')

    def test_get_subject_and_scan_counts(self):
        # This function prints output; capture it to test
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout

        get_subject_and_scan_counts(self.df_tabs_automorph)

        sys.stdout = sys.__stdout__  # Reset redirect
        output = captured_output.getvalue()
        self.assertIn('Number of subjects:', output)
        self.assertIn('Number of scans:', output)

    def test_drop_missing_data(self):
        df = self.df_tabs_automorph.copy()
        df.loc[0, 'signal_strength'] = np.nan
        df_cleaned = drop_missing_data(df)
        self.assertEqual(len(df_cleaned), 2)
        self.assertFalse(df_cleaned['signal_strength'].isnull().any())

    def test_filter_scans_by_parameters(self):
        df = self.df_tabs_automorph.copy()
        df.loc[0, 'scan_field_mm'] = 8.0  # Out of acceptable range
        df_filtered = filter_scans_by_parameters(df)
        self.assertEqual(len(df_filtered), 2)

    def test_filter_scans_by_quality(self):
        df = self.df_tabs_automorph.copy()
        df.loc[0, 'valid_pixels_percentage'] = 89  # Below threshold
        df_filtered = filter_scans_by_quality(df)
        self.assertEqual(len(df_filtered), 2)

    def test_filter_scans_by_prediction_qa(self):
        df = self.df_tabs_automorph.copy()
        df.loc[0, 'softmax_good_mean_qa'] = 0.6  # Below threshold
        df_filtered = filter_scans_by_prediction_qa(df)
        self.assertEqual(len(df_filtered), 2)

    def test_remove_duplicates(self):
        df = pd.concat([self.df_tabs_automorph, self.df_tabs_automorph])
        df_deduped = remove_duplicates(df)
        self.assertEqual(len(df_deduped), 3)

    def test_select_earliest_scans(self):
        df = pd.DataFrame({
            'patient_id_tabs': ['P1', 'P1', 'P2', 'P2'],
            'eye': ['OD', 'OS', 'OD', 'OS'],
            'date': ['2021-01-02', '2021-01-01', '2021-02-02', '2021-02-01'],
            'softmax_good_mean_qa': [0.9, 0.8, 0.85, 0.87],
            'softmax_usable_mean_qa': [0.1, 0.2, 0.15, 0.13]
        })
        df_selected = select_earliest_scans(df, verbose=False)
        self.assertEqual(len(df_selected), 2)
        self.assertListEqual(sorted(df_selected['date'].tolist()), ['2021-01-01', '2021-02-01'])

    def test_impute_missing_data(self):
        df = pd.DataFrame({
            'age': [25, np.nan, 35],
            'sex': ['Male', 'Female', np.nan],
            'htn': [1, np.nan, 0]
        })
        columns_to_impute = ['age', 'sex', 'htn']
        categorical_columns = ['sex', 'htn']
        df_imputed = impute_missing_data(
            df,
            columns_to_impute=columns_to_impute,
            categorical_columns=categorical_columns,
            random_state=0,
            verbose=False
        )
        self.assertFalse(df_imputed[columns_to_impute].isnull().values.any())
        self.assertIn(df_imputed['sex'].iloc[2], ['Male', 'Female'])
        self.assertIn(df_imputed['htn'].iloc[1], [0, 1])

if __name__ == '__main__':
    unittest.main()
