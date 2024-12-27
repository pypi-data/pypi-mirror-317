from typing import Any
import pandas as pd
from difnn.autotm_utility import AutoTM, ExogClassificationStrategy

def fit_and_predict(time_series: pd.DataFrame,
                    exog_classification: list[pd.DataFrame],
                    exog_regression: list[pd.DataFrame],
                    horizon: int,
                    optimization: bool,
                    extras: list[Any],
                    show_graph: bool,
                    ensemble_models: list[Any],
                    optimizer: Any):
    model = AutoTM()
    return model.fit_and_predict(dataframe=time_series,
                                 with_optimization=optimization,
                                 horizon=horizon,
                                 exog_classification={
                                   'strategy': ExogClassificationStrategy.Mode9,
                                   'data': exog_classification
                                 } if exog_classification is not None else None,
                                 exog_regression={
                                   'window': 24,
                                   'data': exog_regression
                                 } if exog_regression is not None else None,
                                 extras=extras,
                                 ensemble=ensemble_models,
                                 optimizer=optimizer,
                                 show_graph=show_graph)

def validate(time_series: pd.DataFrame,
             exog_classification: list[pd.DataFrame],
             exog_regression: list[pd.DataFrame],
             validation_size: int,
             optimization: bool,
             extras: list[Any],
             ensemble_models: list[Any],
             optimizer: Any):
    model = AutoTM()
    return model.validate(dataframe=time_series,
                          exog_classification={
                            'strategy': ExogClassificationStrategy.Mode9,
                            'data': exog_classification
                          } if exog_classification is not None else None,
                          exog_regression={
                            'window': 24,
                            'data': exog_regression
                          } if exog_regression is not None else None,
                          validation_size=validation_size,
                          with_optimization=optimization,
                          extras=extras,
                          ensemble=ensemble_models,
                          optimizer=optimizer)
