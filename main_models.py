import numpy as np
from sklearn.linear_model import LinearRegression
from tensorflow import keras
import os

dirname = os.path.dirname(__file__)
LSTM_PATH = os.path.join(dirname, 'lstm_save')


class LinearRegressionModel:
    def __init__(self):
        self._model = LinearRegression()

    def predict(self, x, future_points=0):
        input_x = np.array([i for i in range(0, len(x))]).reshape((-1, 1))
        input_y = np.array(x)
        self._model.fit(input_x, input_y)

        return [self._model.predict(np.array(i).reshape((-1, 1)))[0]
                for i in range(0, len(x) + future_points)]


class LSTMModel:
    def __init__(self):
        self._model = keras.models.load_model(LSTM_PATH)

    def predict(self, x, future_points=0):
        x_len_correction = 0
        # Padding input
        if len(x) < 11:
            x_len_correction = 11 - len(x)
            x = [x[0] for _ in range(11-len(x))] + x

        for _ in range(future_points):
            reshaped_input = np.array(x[-11:])\
              .reshape((1, 11, 1))
            prediction = self._model.predict(reshaped_input)[0]
            x.append(prediction[0])

        return x[x_len_correction:]
