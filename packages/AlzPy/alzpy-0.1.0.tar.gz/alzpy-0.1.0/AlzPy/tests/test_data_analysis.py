# tests/test_data_analysis.py

import unittest
import pandas as pd
import numpy as np
from your_library.data_analysis import (
    analyze_groups,
    mixed_effects_analysis
)

class TestDataAnalysis(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            'age': [25, 35, 45, 55, 65, 75],
            'blood_pressure': [120, 130, 125, 135, 140, 150],
            'sex': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
            'diabetes': [0, 1, 0, 1, 0, 1],
            'group': [0, 0, 1, 1, 0, 1],
            'subject_id': [1, 2, 3, 4, 5, 6]
        })
        self.cat_columns = ['sex', 'diabetes']
        self.con_columns = ['age', 'blood_pressure']
        self.column_of_interest = 'group'
        self.dependent_variables = ['blood_pressure', 'age']
        self.feature_of_interest = 'group'
        self.confounding_variables = ['age', 'sex']
        self.group_variable = 'subject_id'
        self.categorical_variables = ['sex']
        self.scale_variables = {'age': 'I(age / 10)'}

    def test_analyze_groups(self):
        results = analyze_groups(self.df, self.cat_columns, self.con_columns, self.column_of_interest)
        self.assertIsInstance(results, pd.DataFrame)
        self.assertFalse(results.empty)
        self.assertIn('Characteristic', results.columns)

    def test_analyze_groups_missing_columns(self):
        with self.assertRaises(KeyError):
            analyze_groups(self.df, ['nonexistent_column'], self.con_columns, self.column_of_interest)

    def test_analyze_groups_invalid_column_of_interest(self):
        df_invalid = self.df.copy()
        df_invalid['group'] = [0, 0, 0, 0, 0, 0]
        with self.assertRaises(ValueError):
            analyze_groups(df_invalid, self.cat_columns, self.con_columns, 'group')

    def test_mixed_effects_analysis(self):
        results = mixed_effects_analysis(
            df=self.df,
            dependent_variables=self.dependent_variables,
            feature_of_interest=self.feature_of_interest,
            confounding_variables=self.confounding_variables,
            group_variable=self.group_variable,
            categorical_variables=self.categorical_variables,
            scale_variables=self.scale_variables,
            verbose=False
        )
        self.assertIsInstance(results, pd.DataFrame)
        self.assertFalse(results.empty)
        self.assertIn('Dependent Variable', results.columns)
        self.assertIn('Coefficient', results.columns)

    def test_mixed_effects_analysis_missing_columns(self):
        with self.assertRaises(KeyError):
            mixed_effects_analysis(
                df=self.df,
                dependent_variables=['nonexistent_var'],
                feature_of_interest=self.feature_of_interest,
                confounding_variables=self.confounding_variables,
                group_variable=self.group_variable,
                verbose=False
            )

    def test_mixed_effects_analysis_feature_not_in_model(self):
        df_collinear = self.df.copy()
        df_collinear['group'] = df_collinear['age']  # Make feature of interest collinear with age
        results = mixed_effects_analysis(
            df=df_collinear,
            dependent_variables=self.dependent_variables,
            feature_of_interest='group',
            confounding_variables=['age', 'sex'],
            group_variable='subject_id',
            categorical_variables=['sex'],
            scale_variables={'age': 'I(age / 10)'},
            verbose=False
        )
        # Should handle the case where feature is not in model due to collinearity
        self.assertIsInstance(results, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
