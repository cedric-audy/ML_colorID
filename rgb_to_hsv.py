import numpy as np

# code is inspired from this tutorial : https://realpython.com/python-windows-machine-learning-setup/#introducing-anaconda-and-conda

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

X = np.array([
[]
              ])
y = np.array([])

model = Sequential()
model.add(Dense(2, input_dim=2))
model.add(Activation('sigmoid'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

sgd = SGD(lr=0.1)
model.compile(loss='mean_squared_error', optimizer=sgd)

model.fit(X, y, batch_size=1, epochs=5000)

if __name__ == '__main__':
    print("TRAINING DATA : ")
    print(y)
    print(model.predict(X))
    print(type(model.predict(X)))