import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Активационные функции
# -----------------------------
def elu(x, alpha=1.0):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))

def elu_derivative(x, alpha=1.0):
    return np.where(x > 0, 1.0, elu(x, alpha) + alpha)

# -----------------------------
# Класс слоя
# -----------------------------
class Layer:
    def __init__(self, input_size, output_size):
        # Инициализация весов с нормализацией Xavier
        self.W = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.b = np.zeros(output_size)
        self.z = None
        self.a = None
        self.delta = None

    def forward(self, X):
        self.z = X @ self.W + self.b
        self.a = elu(self.z)
        return self.a

    def backward(self, X, delta_next, W_next, learning_rate):
        self.delta = (delta_next @ W_next.T) * elu_derivative(self.z)
        grad_W = X.T @ self.delta
        grad_b = self.delta.sum(axis=0)
        self.W += learning_rate * grad_W
        self.b += learning_rate * grad_b
        return self.delta

# -----------------------------
# Класс нейронной сети
# -----------------------------
class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            self.layers.append(Layer(layer_sizes[i], layer_sizes[i + 1]))

    def forward(self, X):
        a = X
        for layer in self.layers:
            a = layer.forward(a)
        return a

    def backward(self, X, y, learning_rate):
        # Градиент на выходном слое
        output_layer = self.layers[-1]
        error = y - output_layer.a
        output_layer.delta = error * elu_derivative(output_layer.z)

        # Обратное распространение через скрытые слои
        delta = output_layer.delta
        for i in range(len(self.layers) - 2, -1, -1):
            delta = self.layers[i].backward(
                X if i == 0 else self.layers[i - 1].a,
                delta,
                self.layers[i + 1].W,
                learning_rate
            )

    def predict(self, X):
        preds = []
        for xi in X:
            pred = self.forward(xi[None, :])[0]
            preds.append(pred)
        return np.array(preds)

    def train(self, X_train, y_train, X_test, y_test, learning_rate, epochs, batch_size=32):
        losses_train = []
        losses_test = []
        mae_scores = []
        n_samples = X_train.shape[0]

        for epoch in range(epochs):
            permutation = np.random.permutation(n_samples)
            X_shuffled = X_train[permutation]
            y_shuffled = y_train[permutation]

            total_loss = 0.0
            for i in range(0, n_samples, batch_size):
                X_batch = X_shuffled[i:i + batch_size]
                y_batch = y_shuffled[i:i + batch_size]

                for xi, yi in zip(X_batch, y_batch):
                    pred = self.forward(xi[None, :])
                    loss = np.mean((yi - pred) ** 2)
                    total_loss += loss
                    self.backward(xi[None, :], yi[None, :], learning_rate)

            # MSE на обучении
            preds_train = self.predict(X_train)
            loss_train = np.mean((y_train - preds_train) ** 2)
            losses_train.append(loss_train)

            # MSE на тесте
            preds_test = self.predict(X_test)
            loss_test = np.mean((y_test - preds_test) ** 2)
            losses_test.append(loss_test)

            # MAE
            mae = np.mean(np.abs(y_test - preds_test))
            mae_scores.append(mae)

            if (epoch + 1) % 50 == 0:
                print(f"Epoch {epoch + 1}, Train Loss: {loss_train:.6f}, Test Loss: {loss_test:.6f}, MAE: {mae:.6f}")

        return losses_train, losses_test, mae_scores, preds_test, y_test

    def predict_iterative(self, X_start, n_steps, feature_dim=3):
        predictions = []
        current_window = X_start.copy()

        for _ in range(n_steps):
            pred = self.forward(current_window[np.newaxis, :])
            first_pred = pred[0, 0]
            predictions.append(first_pred)
            current_window = np.roll(current_window, -feature_dim)
            current_window[-feature_dim:] = 0
            current_window[-1] = first_pred

        return np.array(predictions)

# -----------------------------
# Генерация данных
# -----------------------------
def generate_data():
    t_values = np.arange(0, 50 + 0.05, 0.05)
    n_samples = len(t_values)
    epsilon_1 = np.random.normal(0, 0.30**2, n_samples)
    epsilon_2 = np.random.normal(0, 0.05**2, n_samples)
    epsilon_y = np.random.normal(0, 0.03**2, n_samples)
    x1 = np.exp(0.2 * np.sin(0.1 * t_values) + epsilon_1)
    x2 = np.sin(0.30 * t_values) + epsilon_2
    x3 = np.random.normal(0, 1, n_samples)
    y = np.exp(-x1) * (0.8 * x2**2 - 0.2) + epsilon_y
    X = np.column_stack([x1, x2, x3])
    y = y.reshape(-1, 1)
    return X, y

# -----------------------------
# Создание временного окна
# -----------------------------
def create_sequences_multi_step(X, y, window_size=3, n_steps_ahead=5):
    X_seq, y_seq = [], []
    for i in range(window_size, len(X) - n_steps_ahead + 1):
        X_seq.append(X[i - window_size:i].flatten())
        y_seq.append(y[i:i + n_steps_ahead].flatten())
    return np.array(X_seq), np.array(y_seq)

# -----------------------------
# Деление на train/test
# -----------------------------
def train_test_split(X, y, test_size=0.2, seed=None):
    if seed is not None:
        np.random.seed(seed)
    indices = np.random.permutation(len(X))
    test_size = int(len(X) * test_size)
    test_indices = indices[:test_size]
    train_indices = indices[test_size:]
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

# -----------------------------
# Подготовка данных
# -----------------------------
X_raw, y_raw = generate_data()
window_size = 3
n_steps_ahead = 1

X, y = create_sequences_multi_step(X_raw, y_raw, window_size, n_steps_ahead)
X = X.reshape(len(X), -1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, seed=42)

# -----------------------------
# Создание и обучение сети
# -----------------------------
input_size = X_train.shape[1]
hidden_size1 = 20
hidden_size2 = 15
output_size = n_steps_ahead

layer_sizes = [input_size, hidden_size1, hidden_size2, output_size]
nn = NeuralNetwork(layer_sizes)

learning_rate = 0.01
epochs = 100
batch_size = 64

losses_train, losses_test, mae_scores, preds_test, y_true = nn.train(
    X_train, y_train, X_test, y_test, learning_rate, epochs, batch_size
)

# -----------------------------
# Итерационное предсказание
# -----------------------------
print("\nПример итерационного предсказания:")
X_start = X_test[0].copy()
iterative_preds = nn.predict_iterative(X_start, n_steps=n_steps_ahead, feature_dim=3)
print("Итерационные предсказания:", iterative_preds)

print(preds_test)

# -----------------------------
# Визуализация
# -----------------------------
if n_steps_ahead > 1:
    for i in range(0, n_steps_ahead):
        pred = [point[i] for point in preds_test]
        true = [point[i] for point in y_true]
        plt.figure(figsize=(12, 5))
        plt.plot(pred, label=f'Предсказания {i} точек', alpha=0.7)
        plt.plot(true, label='Истинные значения', alpha=0.7)
        plt.title("Предсказания vs Истинные значения")
        plt.xlabel("Примеры")
        plt.ylabel("Значение y")
        plt.legend()
        plt.grid(True)
        plt.show()
else:
    plt.figure(figsize=(12, 5))
    plt.plot(preds_test, label='Предсказания', alpha=0.7)
    plt.plot(y_true, label='Истинные значения', alpha=0.7)
    plt.title("Предсказания vs Истинные значения")
    plt.xlabel("Примеры")
    plt.ylabel("Значение y")
    plt.legend()
    plt.grid(True)
    plt.show()

print(f"\nЛучшее значение MAE: {min(mae_scores):.6f}")