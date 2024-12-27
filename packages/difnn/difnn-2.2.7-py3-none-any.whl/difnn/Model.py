from typing import Any
import pandas as pd
from difnn.forecast_utility import DIFNN, ExogClassificationStrategy, ExogRegressionStrategy

def fit_and_predict(time_series: pd.DataFrame,
                    exog_classification: list[pd.DataFrame],
                    exog_regression: list[pd.DataFrame],
                    horizon: int,
                    optimization: bool,
                    extras: list[Any] = None,
                    show_graph: bool = False):
    model = DIFNN()
    return model.fit_and_predict(dataframe=time_series,
                                 with_optimization=optimization,
                                 horizon=horizon,
                                 exog_classification={
                                   'strategy': ExogClassificationStrategy.Mode9,
                                   'data': exog_classification
                                 } if exog_classification is not None else None,
                                 exog_regression=exog_regression,
                                 extras=extras,
                                 show_graph=show_graph)

def validate(time_series: pd.DataFrame,
             exog_classification: list[pd.DataFrame],
             exog_regression: list[pd.DataFrame],
             validation_size: int,
             optimization: bool,
             extras: list[Any] = None):
    model = DIFNN()
    return model.validate(dataframe=time_series,
                          exog_classification={
                            'strategy': ExogClassificationStrategy.Mode9,
                            'data': exog_classification
                          } if exog_classification is not None else None,
                          exog_regression=exog_regression,
                          validation_size = validation_size,
                          with_optimization=optimization,
                          extras=extras)
