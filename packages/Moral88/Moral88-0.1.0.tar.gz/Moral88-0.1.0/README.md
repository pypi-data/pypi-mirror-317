# Moral88
A Python library for regression evaluation metrics.

## Installation
To use the library, simply clone the repository and add it to your project.

## Usage
```python
from Moral88.regression import mean_absolute_error, mean_squared_error, r_squared

y_true = [1, 2, 3]
y_pred = [1, 2, 4]

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
r2 = r_squared(y_true, y_pred)

print(f"MAE: {mae}, MSE: {mse}, R²: {r2}")
