import pandas as pd
import math
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, Input, Bidirectional, Dropout, BatchNormalization
from keras.regularizers import l2
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error



def addFeatures(df):
    df["Hour"] = df.index.hour
    df["DoW"] = df.index.day_of_week
    df["Quarter"] = df.index.quarter
    df["Month"] = df.index.month
    df["Year"] = df.index.year
    df["DoY"] = df.index.day_of_year
    
    return df

def generateModel(data: pd.DataFrame, train_size: float = 0.8, val_size: float = 0.15, test_size: float = 0.05):
    def createModel(input_shape):
        model = Sequential([
            Input(shape=input_shape),
            Bidirectional(LSTM(256, return_sequences=True)),
            Dropout(0.3),
            Bidirectional(LSTM(256, return_sequences=True)),
            Dropout(0.3),
            Bidirectional(LSTM(128, return_sequences=False)),
            Dropout(0.3),
            Dense(200, activation="relu", kernel_regularizer=l2(0.01)),
            BatchNormalization(),
            Dense(100, activation="relu", kernel_regularizer=l2(0.01)),
            BatchNormalization(),
            Dense(50, activation="relu", kernel_regularizer=l2(0.01)),
            BatchNormalization(),
            Dense(1)
        ])

        model.compile(optimizer=Adam(learning_rate=0.001), loss="mse")

        return model

    def splitData():
        train, temp = train_test_split(data, train_size=train_size, shuffle=False)
        val, test = train_test_split(temp, test_size=test_size/(val_size + test_size), shuffle=False)

        FEATURES = ["Hour", "DoW", "Quarter", "Month", "Year", "DoY"]
        TARGET = ["Budget"]

        X_train = train[FEATURES]
        y_train = train[TARGET]
        X_val = val[FEATURES]
        y_val = val[TARGET]
        X_test = test[FEATURES]
        y_test = test[TARGET]

        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        X_test = scaler.transform(X_test)

        X_train_reshaped = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        X_val_reshaped = X_val.reshape((X_val.shape[0], 1, X_val.shape[1]))
        X_test_reshaped = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

        return (X_train_reshaped, y_train), (X_val_reshaped, y_val), (X_test_reshaped, y_test)

    (X_train_reshaped, y_train), (X_val_reshaped, y_val), (X_test_reshaped, y_test) = splitData()

    input_shape = (1, X_train_reshaped.shape[2])
    model = createModel(input_shape)

    history = model.fit(
        X_train_reshaped, y_train,
        epochs=100,
        batch_size=32,
        validation_data=(X_val_reshaped, y_val),
        callbacks=[
            EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=0.0001)
        ]
    )

    predictions = model.predict(X_test_reshaped).flatten()

    metric = [
        mean_squared_error(y_test, predictions),
        mean_absolute_error(y_test, predictions),
        math.sqrt(mean_squared_error(y_test, predictions)),
        np.mean(np.abs((np.array(y_test) - np.array(predictions)) / np.array(y_test))) * 100

    ]

    return model, history, metric