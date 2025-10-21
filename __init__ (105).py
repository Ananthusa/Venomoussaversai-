import numpy as np

# Define the cost function (mean squared error)
def cost_function(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Define the gradient descent algorithm
def gradient_descent(X, y, learning_rate=0.01, epochs=1000):
    m, n = X.shape
    theta = np.zeros(n)
    cost_history = []

    for epoch in range(epochs):
        predictions = np.dot(X, theta)
        errors = predictions - y
        gradient = (1/m) * np.dot(X.T, errors)
        theta -= learning_rate * gradient
        cost = cost_function(y, predictions)
        cost_history.append(cost)

    return theta, cost_history

# Generate some dummy data
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Add a bias term to the data
X_b = np.c_[np.ones((100, 1)), X]

# Run gradient descent
theta, cost_history = gradient_descent(X_b, y, learning_rate=0.1, epochs=1000)

print(f'Learned parameters: {theta}')
print(f'Cost history: {cost_history}')