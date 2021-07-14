
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pregunta_2.utilities import *

def evaluate(dataframe : pd.DataFrame) -> pd.DataFrame:
    """Method for evaluating the models with respect to mean absolute
    error and root mean square error, for a certain dataset (respective
    to a particular year)."""

    # First we partition the data
    X_train, X_test, y_train, y_test = split(dataframe)

    # Then create a dataframe to store the results.
    regression_model_name_list = ["Linear Regression", "Elastic Net",
                                  "Gradient Boosting Regression", 
                                  "Bayesian Ridge", "Naive"]

    result = pd.DataFrame(columns=["RMSE", "MAE"], index=regression_model_name_list)

    # We instantiate the regression models
    linear_regression = LinearRegression()
    elastic_net = ElasticNet()
    gradient_boosting = GradientBoostingRegressor(n_estimators=20)
    bayesian_ridge = BayesianRidge()

    model_list = [linear_regression, elastic_net, gradient_boosting, 
                  bayesian_ridge]

    timer = Timer()  # For timing training and prediction times

    for i, model in enumerate(model_list):

        # For the current model we make the prediction and take times
        print("Training with {}".format(regression_model_name_list[i]))
        timer.start()
        model.fit(X_train, y_train)
        elapsed = timer.stop()
        print("Time spent training: {:.4f} s".format(elapsed))
        print("Predicting with {}".format(regression_model_name_list[i]))
        timer.start()
        y_pred = model.predict(X_test)
        elapsed = timer.stop()
        print("Time spent predicting: {:.4f} s".format(elapsed), '\n')

        # Now we compute loss using both metrics
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mae = mean_absolute_error(y_test, y_pred)

        # Finally we store the results
        result.iloc[i] = [rmse, mae]

    # After evaluating each model we store the result of the naive
    # prediction (assigning each instance to the median value of the
    # training set y_train).
    median = np.median(y_train)
    naive_rmsl = np.sqrt(np.mean((median - y_test) ** 2))
    naive_mal = np.mean(abs(median - y_test))
    result.loc["Naive"] = [naive_rmsl, naive_mal]

    return result


if __name__ == "__main__":

    dataframe_2002 = csv_to_df(2018)
    dataframe_2002 = encode_categorical_data(dataframe_2002)
    results = evaluate(dataframe_2002)
    print(results)
