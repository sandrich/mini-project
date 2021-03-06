#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.svm import SVC
import logging
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier


logging.basicConfig(level=logging.INFO)


def train(X, Y, args):
    """
    Train a model given the arguments, the dataset and 
    the corresponding labels (ground-truth)

    Parameters
    ----------

    X : array
        features of the dataset
    Y : array
        corresponding labels
    args : dict
        arguments to prepare the model

    Returns
    -------

    model : object
        trained model

    """

    # SVM model selected
    if args.model == "svm":
        logging.info(f"Training SVM model...")

        # Using predefined parameters
        if args.gridsearch == "n":
            logging.info(f"Using predefined parameters.")

            # Training SVM model using radial kernel and predefined parameters
            kernel = "rbf"
            gamma = 0.0001
            C = 1000

            svm_model = SVC(kernel=kernel, gamma=gamma, C=C)
            svm_model.fit(X, Y)

            return svm_model

        # Grid search
        elif args.gridsearch == "y":
            logging.info(f"Doing grid search, it may take a while...")

            # Create the parameter grid
            params_grid = [
                {"kernel": ["rbf"], "gamma": [1e-2, 1e-3, 1e-4], "C": [10, 100, 1000],},
                {"kernel": ["linear"], "C": [10, 100, 1000]},
                {
                    "kernel": ["poly"],
                    "gamma": [1e-2, 1e-3, 1e-4],
                    "degree": [3, 4, 5],
                    "C": [10, 100, 1000],
                },
                {
                    "kernel": ["sigmoid"],
                    "gamma": [1e-2, 1e-3, 1e-4],
                    "C": [10, 100, 1000],
                },
            ]

            svm_model = GridSearchCV(SVC(), params_grid, cv=3, verbose=10, n_jobs=-1)
            svm_model.fit(X, Y)

            logging.info(f"Using hyperparameters: {svm_model.best_params_}")

            return svm_model

    # Random forest model selected
    elif args.model == "rf":
        logging.info(f"Training RF model...")

        # Using predefined parameters
        if args.gridsearch == "n":
            logging.info(f"Using predefined parameters.")

            # Training RF model using predefined parameters
            n_estimators = 50
            max_depth = 25
            min_samples_split = 2
            min_samples_leaf = 4
            bootstrap = True

            rf_model = RandomForestClassifier(
                max_depth=max_depth,
                n_estimators=n_estimators,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                bootstrap=bootstrap,
                random_state=42,
            )

            rf_model.fit(X, Y)

            return rf_model

        # Grid search
        elif args.gridsearch == "y":
            logging.info(f"Doing grid search, it may take a while...")

            n_estimators = [50, 75, 100]
            max_depth = [10, 25, 50]
            min_samples_split = [2, 4, 6]
            min_samples_leaf = [1, 2, 4]
            bootstrap = [True]

            param_grid = {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "min_samples_leaf": min_samples_leaf,
                "bootstrap": bootstrap,
            }

            rf = RandomForestClassifier(random_state=42)

            rf_model = GridSearchCV(
                estimator=rf, param_grid=param_grid, cv=3, verbose=10, n_jobs=-1
            )
            rf_model.fit(X, Y)

            logging.info(f"Using hyperparameters: {rf_model.best_params_}")

            return rf_model


def predict(X, model):
    """
    Predict labels given the features and the trained model

    Parameters
    ----------

    X : array
        features to predict on
    model : object
        trained model

    Returns
    -------

    predictions : array
        Array with the predicted labels

    """
    Y_pred = model.predict(X)

    return Y_pred
