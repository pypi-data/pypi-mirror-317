**AlzPy**

AlzPy is a Python library for efficient data preprocessing and statistical analysis. It includes robust tools for filtering, imputation, duplicate removal, descriptive statistics, and mixed-effects modeling, making it particularly suited for research and data science applications.


**Features**

*Data Processing*

    •	Filter scans based on quality metrics.
    •	Impute missing data using iterative imputation.
    •	Remove duplicates while preserving data integrity.
    •	Select earliest scans for each patient or group.

*Data Analysis*

    •	Perform descriptive analysis of categorical and continuous variables.
    •	Run mixed-effects models to account for hierarchical or grouped data.

**Installation**

To install AlzPy, simply use pip:

```
pip install AlzPy
```

**Usage**

*Importing the Library*
```
import AlzPy
```

*Filter Scans*
```
import pandas as pd
from AlzPy import filter_scans_by_prediction_qa

# Example DataFrame
data = pd.DataFrame({
    "Prediction_qa": [1, 2, 0, 1],
    "Other_Column": [5, 6, 7, 8]
})

# Apply filter
filtered_data = filter_scans_by_prediction_qa(data, prediction_qa_col="Prediction_qa", exclude_value=2)
print(filtered_data)
```
*Impute Missing Data*
```
from AlzPy import impute_missing_data

# Impute missing values in specific columns
imputed_data = impute_missing_data(data, columns_to_impute=["Column1", "Column2"])
```

*Descriptive Analsysis*
```
from AlzPy import analyze_groups

# Perform descriptive analysis
results = analyze_groups(
    df=data,
    cat_columns=["Category_Column"],
    con_columns=["Continuous_Column"],
    column_of_interest="Group_Column"
)
print(results)
```

*Mixed Effect Modelling*
```
from AlzPy import mixed_effects_analysis

# Fit a mixed-effects model
results = mixed_effects_analysis(
    df=data,
    dependent_variables=["Outcome_Variable"],
    feature_of_interest="Feature_Column",
    confounding_variables=["Confounder1", "Confounder2"],
    group_variable="Group_Column"
)
print(results)
```

**Dependencies**

The following libraries are required to use AlzPy:
	•	pandas
	•	numpy
	•	scipy
	•	scikit-learn
	•	statsmodels
	•	matplotlib
	•	patsy

Install dependencies automatically with pip install AlzPy.

**Author**
Developed by Owen James Sweeney. For inquiries or support, please email: owensweeney97@gmail.com