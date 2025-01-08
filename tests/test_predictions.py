from app.Predictions import calculate_sma, calculate_linear_regression
import numpy as np

def test_calculate_sma():
    prices = [1, 2, 3, 4, 5, 6]
    sma = calculate_sma(prices, window=3)
    assert sma == [None, None, 2.0, 3.0, 4.0, 5.0]

def test_calculate_linear_regression():
    prices = [1, 2, 3, 4, 5]
    dates = ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"]
    model, predictions = calculate_linear_regression(prices, dates)
    assert model is not None
    assert len(predictions) == len(prices)