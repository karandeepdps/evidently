#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import math

from scipy.stats import ks_2samp
from sklearn import metrics, preprocessing


from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ProbClassRefQualityMetricsWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def analyzers(self):
        return []

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("No reference data with target and prediction provided")

    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping, analyzes_results):
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            if num_feature_names is None:
                num_feature_names = []
            else:
                num_feature_names = [name for name in num_feature_names if is_numeric_dtype(reference_data[name])] 

            cat_feature_names = column_mapping.get('categorical_features')
            if cat_feature_names is None:
                cat_feature_names = []
            else:
                cat_feature_names = [name for name in cat_feature_names if is_numeric_dtype(reference_data[name])] 
        
        else:
            date_column = 'datetime' if 'datetime' in reference_data.columns else None
            id_column = None
            target_column = 'target' if 'target' in reference_data.columns else None
            prediction_column = 'prediction' if 'prediction' in reference_data.columns else None

            utility_columns = [date_column, id_column, target_column, prediction_column]

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            binaraizer = preprocessing.LabelBinarizer()
            binaraizer.fit(reference_data[target_column])
            binaraized_target = binaraizer.transform(reference_data[target_column])

            array_prediction = reference_data[prediction_column].to_numpy()

            prediction_ids = np.argmax(array_prediction, axis=-1)
            prediction_labels = [prediction_column[x] for x in prediction_ids]

            labels = sorted(set(reference_data[target_column]))

            #calculate quality metrics
            if len(prediction_column) > 2:
                roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average='macro')
                log_loss = metrics.log_loss(binaraized_target, array_prediction)
            else:
                roc_auc = metrics.roc_auc_score(binaraized_target, reference_data[prediction_column[0]], #problem!!!
                average='macro')
                log_loss = metrics.log_loss(binaraized_target, reference_data[prediction_column[0]]) #problem!!!

            accuracy_score = metrics.accuracy_score(reference_data[target_column], prediction_labels)
            avg_precision = metrics.precision_score(reference_data[target_column], prediction_labels, 
                average='macro')
            avg_recall = metrics.recall_score(reference_data[target_column], prediction_labels, 
                average='macro')
            avg_f1 = metrics.f1_score(reference_data[target_column], prediction_labels, 
                average='macro')

            self.wi = BaseWidgetInfo(
                title=self.title,
                type="counter",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=2,
                params={   
                    "counters": [
                      {
                        "value": str(round(accuracy_score, 3)),
                        "label": "Accuracy"
                      },
                      {
                        "value": str(round(avg_precision, 3)),
                        "label": "Precision"
                      },
                      {
                        "value": str(round(avg_recall, 3)),
                        "label": "Recall"
                      },
                      {
                        "value": str(round(avg_f1, 3)),
                        "label": "F1"
                      },
                      {
                        "value": str(round(roc_auc, 3)),
                        "label": "ROC AUC"
                      },
                      {
                        "value": str(round(log_loss, 3)),
                        "label": "LogLoss"
                      }
                    ]
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None

