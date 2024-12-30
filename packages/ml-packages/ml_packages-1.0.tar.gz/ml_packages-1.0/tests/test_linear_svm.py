import unittest
import numpy as np
from mlpackages.linear_svm import LinearSVM

class TestLinearSVM(unittest.TestCase):
    def test_fit_predict(self):
        X = np.array([[1, 2], [2, 3], [3, 4]])
        y = np.array([1, -1, 1])
        model = LinearSVM(learning_rate=0.1, epochs=100)
        model.fit(X, y)
        predictions = model.predict(X)
        self.assertEqual(len(predictions), len(y))