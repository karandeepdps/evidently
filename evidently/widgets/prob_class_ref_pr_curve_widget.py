#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd

import numpy as np

from sklearn import metrics, preprocessing
from pandas.api.types import is_numeric_dtype

import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ProbClassRefPRCurveWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def analyzers(self):
        return []

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("No prediction or target data provided")

    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping, analyzes_results):
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            #target_names = column_mapping.get('target_names')
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

            #target_names = None

        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            #array_prediction = reference_data[prediction_column].to_numpy()

            #prediction_ids = np.argmax(array_prediction, axis=-1)
            #prediction_labels = [prediction_column[x] for x in prediction_ids]
            if len(prediction_column) <= 2:
                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = pd.DataFrame(binaraizer.transform(reference_data[target_column]))
                binaraized_target.columns = ['target']

                p, r, thrs = metrics.precision_recall_curve(binaraized_target, reference_data[prediction_column[0]]) #problem!!!
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x = p,
                    y = r,
                    mode = 'lines',
                    name='PR',
                    marker=dict(
                        size=6,
                        color=red,
                    )
                ))

                fig.update_layout(
                        yaxis_title="Precision",
                        xaxis_title="Recall",
                        showlegend=True
                    )

                fig_json = json.loads(fig.to_json())

                self.wi = BaseWidgetInfo(
                    title=self.title,
                    type="big_graph",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=1 if production_data is not None else 2,
                    params={
                        "data": fig_json['data'],
                        "layout": fig_json['layout']
                    },
                    additionalGraphs=[],
                )
            else:
                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = pd.DataFrame(binaraizer.transform(reference_data[target_column]))
                binaraized_target.columns = prediction_column
                #plot support bar
                graphs = []

                for label in prediction_column:
                    p, r, thrs = metrics.precision_recall_curve(binaraized_target[label], reference_data[label])
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x = p,
                        y = r,
                        mode = 'lines',
                        name='PR',
                        marker=dict(
                            size=6,
                            color=red,
                        )
                    ))

                    fig.update_layout(
                        yaxis_title="Precision",
                        xaxis_title="Recall",
                        showlegend=True
                    )

                    fig_json = json.loads(fig.to_json())

                    graphs.append({
                        "id": "tab_" + str(label),
                        "title": str(label),
                        "graph":{
                            "data":fig_json["data"],
                            "layout":fig_json["layout"],
                            }
                        })

                self.wi = BaseWidgetInfo(
                    title=self.title,
                    type="tabbed_graph",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=1 if production_data is not None else 2,
                    params={
                        "graphs": graphs
                    },
                    additionalGraphs=[],
                )
        else:
            self.wi = None

