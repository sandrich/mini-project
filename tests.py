#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pytest
import database
import evaluator
import algorithm
import run

import logging

model = None
train_data, train_labels, test_data, test_labels = None, None, None, None


"""Tests the database script"""

def test_downloadDataset():
    
    database.downloadDataset()

    assert os.path.exists("UCI HAR Dataset")
    assert os.path.isdir("UCI HAR Dataset")

    # Check if the right files and folders are present
    entries = os.listdir("UCI HAR Dataset")
    expected_files = ["activity_labels.txt", "features_info.txt", "features.txt",
                        "test", "train"]
    for f in expected_files:
        assert f in entries


def test_transformToTextLabels():

    num_labels = np.array([1, 2, 3, 4, 5, 6])
    labels = database.transformToTextLabels(num_labels)

    assert np.array_equal(labels, np.array(["WALKING", "WALKING_UPSTAIRS", 
                        "WALKING_DOWNSTAIRS", "SITTING", "STANDING", "LAYING"]))


def test_getDatasetSplit():
    train_data, train_labels = database.getDatasetSplit("train")

    assert train_data.shape == (7352, 561)
    assert train_labels.shape == (7352, )
    assert min(train_labels) == 1
    assert max(train_labels) == 6

    test_data, test_labels = database.getDatasetSplit("test")

    assert test_data.shape == (2947, 561)
    assert test_labels.shape == (2947, )
    assert min(test_labels) == 1
    assert max(test_labels) == 6


def test_load(caplog):
    
    caplog.set_level(logging.INFO)

    # Save data for other tests
    pytest.train_data, pytest.train_labels, pytest.test_data, pytest.test_labels = database.load(
        standardized=True, printSize=True
    )

    assert caplog.record_tuples[3][2] == "---Train samples: 7352"
    assert caplog.record_tuples[4][2] == "---Test samples: 2947"
    assert caplog.record_tuples[5][2] == "Dataset standardized."


"""Tests the algorithm script"""

class MockArgs:
  def __init__(self):
    self.model = "rf"
    self.gridsearch = "n"
    self.output_folder = "results"

def test_algorithm():
    args = MockArgs()
    pytest.model = algorithm.train(pytest.train_data, pytest.train_labels, args)

def test_predict():
    pytest.predictions = algorithm.predict(pytest.test_data, pytest.model)



"""Tests the evaluator script"""

def test_getMetricsTable():

    # Fake data
    predictedLabels = np.array([0, 1, 2, 3, 4, 5])
    trueLabels = np.array([0, 1, 2, 1, 2, 3])

    table = evaluator.getMetricsTable(predictedLabels, trueLabels)

    # Check if we get the correct metrics
    assert table.count("0.5") == 4
    assert "Precision" in table
    assert "Recall" in table
    assert "F1 score" in table
    assert "Accuracy" in table


def test_getTableHeader():

    table = evaluator.getTableHeader("rf", pytest.model)

    assert "Model used: rf" in table
    assert "Parameters:" in table
    assert len(table.splitlines()) == 7


def test_evaluate(caplog):
    
    caplog.set_level(logging.INFO)

    evaluator.evaluate(pytest.predictions, pytest.test_data, pytest.test_labels, 
                        "results", "rf", pytest.model)

    assert "Saving table at" in caplog.record_tuples[1][2]
    assert "Saving confusion matrix at" in caplog.record_tuples[2][2]

    assert os.path.isfile(os.getcwd() + "/results/table.rst")
    assert os.path.isfile(os.getcwd() + "/results/confusion_matrix.png")