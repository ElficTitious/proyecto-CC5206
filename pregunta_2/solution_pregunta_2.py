import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pregunta_2.utilities import *

def predict_year(year : int) -> tuple:
    """Predicts the grades for a given year trainig the model with
    instances for the previous 3 years. It returns a tuple with the
    mean absolute error of the predictions, and its standard deviaton,
    and the mean absolute error naive approach."""

    print("Year: {}".format(year), "\n")

    # We partition the data, where X_train contains the instances of
    # the three previous years, and X_test the instances of the year
    # given as parameter.
    X_train, X_test, y_train, y_test = split_pregunta_2(year)

    # We instanciate the Linear Regressor
    linear_regressor = LinearRegression()


    print("Training...")
    linear_regressor.fit(X_train, y_train)
    print("Predicting...", "\n")
    y_pred = linear_regressor.predict(X_test)

    absolute_error_arr = np.abs(y_pred - y_test)
    std = np.std(absolute_error_arr)
    mae = np.mean(absolute_error_arr)

    # After evaluating the model, we compute the result of the naive
    # prediction (assigning each instance to the median value of the
    # training set y_train).
    median = np.median(y_train)
    naive_mae = np.mean(abs(median - y_test))

    return mae, std, naive_mae


if __name__ == "__main__":

    mae_list = []
    naive_mae_list = []
    std_list = []

    years = range(2005, 2021)

    for year in years:
        tmp = predict_year(year)
        mae_list.append(tmp[0])
        std_list.append(tmp[1])
        naive_mae_list.append(tmp[2])

    plt.clf()
    plt.figure()
    plt.plot(years, mae_list, linestyle='--', marker='o',
             label="Predicciones Regresor Lineal")
    plt.plot(years, naive_mae_list, linestyle='--', marker='o',
             label="Predicciones Naive")
    plt.ylabel("MAE (Mean Absolute Error)")
    plt.xlabel("Año")
    plt.legend()
    plt.show()

    percentage_improve = np.array([100 * (np.abs(mae_list[i] 
                                   - naive_mae_list[i])/naive_mae_list[i])
                                   for i in range(16)])

    plt.clf()
    plt.figure()
    plt.plot(years, percentage_improve, linestyle="--", marker="o")
    plt.xlabel("Año")
    plt.ylabel("Porcentaje mejoría sobre Naive (%)")
    plt.show()

    



