import unittest
import numpy as np
from mlpackages.LogisticRegression import LogisticRegression

class TestLogisticRegression(unittest.TestCase):
    def test_fit_predict(self):
        X = np.array([[1, 2], [2, 3], [3, 4]])
        y = np.array([0, 1, 0])
        model = LogisticRegression(learning_rate=0.1, epochs=100)
        model.fit(X, y)
        predictions = model.predict(X)
        self.assertEqual(len(predictions), len(y))
