## ML Package: Logistic Regression, KNN, and Linear SVM

This package, mlpackage, provides implementations of three popular machine learning algorithms:

- Logistic Regression with Softmax

- K-Nearest Neighbors (KNN) Classifier

- Linear Support Vector Machine (SVM)

It also includes test scripts to validate each module's functionality.

## Usage

# Logistic Regression with Softmax

Example:

```python

from mlpackage.logistic_regression import LogisticRegressionSoftmax
import numpy as np

# Sample data
X = np.array([[1, 2], [2, 3], [3, 4]])
y = np.array([0, 1, 0])

# Train the model
model = LogisticRegressionSoftmax(learning_rate=0.1, epochs=1000)
model.fit(X, y)

# Make predictions
predictions = model.predict(X)
print(predictions)
```
# K-Nearest Neighbors (KNN) Classifier

Example:

```python
from mlpackage.knn import KNNClassifier
import numpy as np

# Sample data
X = np.array([[1, 1], [2, 2], [3, 3]])
y = np.array([0, 1, 0])

# Train and predict
model = KNNClassifier(k=1)
model.fit(X, y)
predictions = model.predict(X)
print(predictions)
```

# Linear Support Vector Machine (SVM)
Example:

```python
from mlpackage.linear_svm import LinearSVM
import numpy as np

# Sample data
X = np.array([[1, 2], [2, 3], [3, 4]])
y = np.array([1, -1, 1])

# Train the model
model = LinearSVM(learning_rate=0.001, epochs=1000, lambda_param=0.01)
model.fit(X, y)

# Make predictions
predictions = model.predict(X)
print(predictions)
```
# Running Tests

To verify the implementation, you can run the unit tests located in the tests/ directory.

# Run All Tests:
```python
python -m unittest discover -s tests -p "*.py" -v

#Example Output
test_fit_predict (tests.test_logistic_regression.TestLogisticRegression) ... ok
test_fit_predict (tests.test_knn.TestKNNClassifier) ... ok
test_fit_predict (tests.test_linear_svm.TestLinearSVM) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.XXXs

OK
```

# Dependencies

- Python 3.6+

- NumPy

