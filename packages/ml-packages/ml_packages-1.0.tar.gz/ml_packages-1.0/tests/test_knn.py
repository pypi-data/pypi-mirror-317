import unittest
import numpy as np
from mlpackages.knn import KNNClassifier

class TestKNNClassifier(unittest.TestCase):
    def test_fit_predict(self):
        X = np.array([[1, 1], [2, 2], [3, 3]])
        y = np.array([0, 1, 0])
        model = KNNClassifier(k=1)
        model.fit(X, y)
        predictions = model.predict(X)
        self.assertTrue((predictions == y).all())