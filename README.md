<h1 align="center">Evidently</h1>

![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_4_reports_preview_small.png)
 
<p align="center"><b>Interactive reports and JSON profiles to analyze, monitor and debug machine learning models.</b></p>

<p align="center">
  <a href="https://evidentlyai.gitbook.io/docs/">Docs</a>
  |
  <a href="https://discord.gg/xZjKRaNp8b">Join Discord</a>
  |
  <a href="https://evidentlyai.com/sign-up">Newsletter</a>
  | 
  <a href="https://evidentlyai.com/blog">Blog</a>
  | 
  <a href="https://twitter.com/EvidentlyAI">Twitter</a>
</p>


## What is it?
Evidently helps analyze machine learning models during validation or production monitoring. The tool generates interactive visual reports and JSON profiles from pandas `DataFrame` or `csv` files. Currently 6 reports are available.  

### 1. Data Drift
Detects changes in feature distribution. 
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_github.png)

### 2. Numerical Target Drift
Detects changes in numerical target and feature behavior.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_num_target_drift_github.png)

### 3. Categorical Target Drift
Detects changes in categorical target and feature behavior.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_cat_target_drift_github.png)

### 4. Regression Model Performance
Analyzes the performance of a regression model and model errors.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_regression_performance_report_github.png)

### 5. Classification Model Performance
Analyzes the performance and errors of a classification model. Works both for binary and multi-class models.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_classification_performance_report_github.png)

### 6. Probabilistic Classification Model Performance
Analyzes the performance of a probabilistic classification model, quality of model calibration, and model errors. Works both for binary and multi-class models.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_prob_classification_performance_report_github.png)

## Installing from PyPI
### MAC OS and Linux
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```

The tool allows building interactive reports both inside a Jupyter notebook and as a separate HTML file. If you only want to generate interactive reports as HTML files or export as JSON profiles, the installation is now complete.

To enable building interactive reports inside a Jupyter notebook, we use jupyter nbextension. If you want to create reports inside a Jupyter notebook, then after installing `evidently` you should run the two following commands in the terminal from evidently directory.

To install jupyter nbextention, run:
```sh
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```
To enable it, run:
```sh
jupyter nbextension enable evidently --py --sys-prefix
```
That's it!

**Note**: a single run after the installation is enough. No need to repeat the last two commands every time.

**Note 2**: if you use Jupyter Lab, you may experience difficulties with exploring report inside a Jupyter notebook. However, the report generation in a separate .html file will work correctly.

### Windows
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```
The tool allows building interactive reports both inside a Jupyter notebook and as a separate HTML file. Unfortunately, building reports inside a Jupyter notebook is not yet possible for Windows. The reason is Windows requires administrator privileges to create symlink. In later versions we will address this issue.

## Getting started

### Jupyter Notebook
To start, prepare your data as two pandas `DataFrames`. The first should include your reference data, the second - current production data. The structure of both datasets should be identical. 

* For **Data Drift** report, include the input features only.
* For **Target Drift** reports, include the column with Target and/or Prediction.
* For **Model Performance** reports, include the columns with Target and Prediction.

Calculation results can be available in one of the two formats:
* Option 1: an interactive **Dashboard** displayed inside the Jupyter notebook or exportable as a HTML report.
* Option 2: a JSON **Profile** that includes the values of metrics and the results of statistical tests.  

#### Option 1: Dashboard

After installing the tool, import Evidently **dashboard** and required tabs:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

To generate the **Data Drift** report, run:
```python
iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
iris_data_drift_report.save("reports/my_report.html")
```

To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
```python
iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab, CatTargetDriftTab])
iris_data_and_target_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
iris_data_and_target_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html".
HTML report does not open automatically. To explore it, you should open it from the destination folder.

To generate the **Regression Model Performance** report, run:
```python
regression_model_performance = Dashboard(tabs=[RegressionPerfomanceTab]) 
regression_model_performance.calculate(reference_data, current_data, column_mapping = column_mapping) 
```

You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
```python
regression_single_model_performance = Dashboard(tabs=[RegressionPerformanceTab])
regression_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

To generate the **Classification Model Performance** report, run:
```python
classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, column_mapping = column_mapping)
```
 
For **Probabilistic Classification Model Performance** report, run:
```python
classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, column_mapping = column_mapping)
```
 
You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
```python
classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab])
classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```
or
```python
prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab])
prob_classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

#### Option 2: Profile

After installing the tool, import Evidently **profile** and required sections:

```python
import pandas as pd
from sklearn import datasets

from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

To generate the **Data Drift** profile, run:
```python
iris_data_drift_profile = Profile(sections=[DataDriftProfileSection])
iris_data_drift_profile.calculate(iris_frame, iris_frame, column_mapping = None)
iris_data_drift_profile.json() 
```

To generate the **Data Drift** and the **Categorical Target Drift** profile, run:
```python
iris_target_and_data_drift_profile = Profile(sections=[DataDriftProfileSection, CatTargetDriftProfileSection])
iris_target_and_data_drift_profile.calculate(iris_frame[:75], iris_frame[75:], column_mapping = None) 
iris_target_and_data_drift_profile.json() 
```

You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
```python
regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection])
regression_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

To generate the **Classification Model Performance** profile, run:
```python
classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection])
classification_performance_profile.calculate(reference_data, current_data, column_mapping = column_mapping)
```

For **Probabilistic Classification Model Performance** profile, run:
```python
classification_performance_report = Profile(sections=[ProbClassificationPerformanceProfileSection])
classification_performance_report.calculate(reference_data, current_data, column_mapping = column_mapping)
```

You can also generate either of the **Classification** profiles for a single `DataFrame`. In this case, run:
```python
classification_single_model_performance = Profile(sections=[ClassificationPerformanceProfileSection])
classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```
or
```python
prob_classification_single_model_performance = Profile(sections=[ProbClassificationPerformanceProfileSection])
prob_classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

### Terminal
You can generate **HTML reports** or **JSON profiles** directly from the bash shell. To do this, prepare your data as two `csv` files. In case you run one of the performance reports, you can have only one file. The first one should include your reference data, the second - current production data. The structure of both datasets should be identical. 

To generate a HTML report, run the following command in bash:

```bash
python -m evidently calculate dashboard --config config.json 
--reference reference.csv --current current.csv --output output_folder --report_name output_file_name
```

To generate a JSON profile, run the following command in bash:
```bash
python -m evidently calculate profile --config config.json 
--reference reference.csv --current current.csv --output output_folder --report_name output_file_name

```
Here:
- `reference` is the path to the reference data, 
- `current` is the path to the current data, 
- `output` is the path to the output folder,
- `config` is the path to the configuration file.
- `pretty_print` to print the JSON profile with indents (for profile only)

Currently, you can choose the following Tabs or Sections:
- `data_drift` to estimate the data drift,
- `num_target_drift` to estimate target drift for numerical target,
- `cat_target_drift` to estimate target drift for categorical target,
- `classification_performance` to explore the performance of a classification model,
- `prob_classification_performance` to explore the performance of a probabilistic classification model,
- `regression_performance` to explore the performance of a regression model.

To configure a report or a profile you need to create the `config.json` file. This file configures the way of reading your input data and the type of the report. 

Here is an example of a simple configuration for a report, where we have comma separated `csv` files with headers and there is no `date` column in the data.

**Dashboard**:
```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": null
  },
  "column_mapping" : {},
  "dashboard_tabs": ["cat_target_drift"]
}
```

**Profile**:
```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": null
  },
  "column_mapping" : {},
  "profile_sections": ["data_drift"],
  "pretty_print": true
}
```

Here is an example of a more complicated configuration, where we have comma separated `csv` files with headers and `datetime` column. We also specified the `column_mapping` dictionary to add information about `datetime`, `target` and `numerical_features`. 

**Dashboard**:
```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": "datetime"
  },
  "column_mapping" : {
    "datetime":"datetime",
    "target":"target",
    "numerical_features": ["mean radius", "mean texture", "mean perimeter", 
      "mean area", "mean smoothness", "mean compactness", "mean concavity", 
      "mean concave points", "mean symmetry"]},
  "dashboard_tabs": ["cat_target_drift"]
}
```

**Profile**:
```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": null
  },
  "column_mapping" : {
    "target":"target",
    "numerical_features": ["mean radius", "mean texture", "mean perimeter", 
      "mean area", "mean smoothness", "mean compactness", "mean concavity", 
      "mean concave points", "mean symmetry"]},
  "profile_sections": ["data_drift", "cat_target_drift"],
  "pretty_print": true
}
```
## Documentation

For more information, refer to a complete <a href="https://evidentlyai.gitbook.io/docs/">Documentation</a>.

## Examples
- See Iris **Data Drift**, **Categorical Target Drift** and **Classification Performance** report generation to explore the reports both inside a Jupyter notebook and as a separate .html file: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/iris_data_drift.ipynb) 
- See Boston Housing **Data Drift** and **Numerical Target Drift** report generation to explore the reports with and without column mapping: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/boston_data_drift.ipynb)
- See Breast cancer **Data Drift** and **Probabilistic Classification Performance** report generation to explore the reports with and without datetime specification: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/breast_cancer_data_drift.ipynb)
- See Bike Demand Prediction **Regression Model Performance** report with datetime and column mapping inside a Jupyter notebook: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/bike_sharing_demand_regression_performance.ipynb)

## Stay updated
We will be releasing more reports soon. If you want to receive updates, follow us on [Twitter](https://twitter.com/EvidentlyAI), or sign up for our [newsletter](https://evidentlyai.com/sign-up). You can also find more tutorials and explanations in our [Blog](https://evidentlyai.com/blog). If you want to chat and connect, join our [Discord community](https://discord.gg/xZjKRaNp8b)!
