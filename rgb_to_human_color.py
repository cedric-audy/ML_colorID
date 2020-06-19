import numpy as np
import csv
import time

import tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import TensorBoard


# ===============================================================================================
COLORDICT = {'red':0, 'orange':1, 'yellow':2, 'green':3, 'blue':4,'purple':5,'brown':6,'pink':7, 'gray':8}
# ===============================================================================================
NAME = f"3x9_dense{int(time.time())}"
# ===============================================================================================
class Model:
    # ===============================================================================================
    def __init__(self, training_path, verif_path, epochs =5000, learning_rate=0.99,momentum = 0.8):
        self.training_path = training_path
        self.verif_path = verif_path
        self.colorIndexDict = {b:a for a,b in COLORDICT.items()}
        self.model = None
        self.tensorboard = None
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.sgd = SGD(lr=learning_rate, momentum=self.momentum, decay=self.learning_rate/self.epochs , nesterov=False)
    # ===============================================================================================
    def buildModel(self):
        self.model = Sequential()
        self.model.add(Dense(9, input_dim=3))
        self.model.add(Activation('sigmoid'))
        self.model.add(keras.layers.Dense(9, activation='sigmoid'))
        self.model.add(keras.layers.Dense(9, activation='softmax'))
        self.tensorboard = TensorBoard(f'.\logs\{NAME}_{self.learning_rate}_{self.momentum}')
    # ===============================================================================================
    def train(self):
        data = self.readData(self.training_path)
        for d in data:
            d[0] = COLORDICT[d[0]]
        rgb_vals = [[float(r),float(g),float(b)] for c,r,g,b in data]
        X = np.array(rgb_vals) #training rgb vals
        
        #answers(human color)
        rows = []
        for c,r,g,b in data:
            r = [0,0,0,0,0,0,0,0,0]
            r[c]=1
            rows.append(r)
        y = np.array(rows)
        self.model.compile(loss='mean_squared_error', optimizer=self.sgd, metrics=['accuracy'])
        self.model.fit(X, y, callbacks=[self.tensorboard],batch_size=256, epochs=self.epochs)
    # ===============================================================================================
    def predictResults(self, arr):
        return self.model.predict(arr)
    # ===============================================================================================
    def readData(self, path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data
    # ===============================================================================================
    def verify(self):
        data = self.readData(self.verif_path)
        test_rgb = np.array([[float(r),float(g),float(b)] for c,r,g,b in data])

        test_rgb = self.predictResults(test_rgb)
        good_guesses = 0
        total = 0
        i = 0

        for r in test_rgb:
            doubleR = []
            j = 0
            for c in r:
                doubleR.append((self.colorIndexDict[j],c))
                j+=1
            topcolor = sorted(doubleR, key = lambda c:c[1])[::-1]
            topcolor = topcolor[0:3]
            if topcolor[0][0] == data[i][0]:
                print(topcolor[0][0] + ' @ rgb(' + str(data[i][1]) +','+ str(data[i][2]) +','+ str(data[i][3]) +')    at ' + str(topcolor[0][1]))
                good_guesses+=1

            else:
                print('Wrong guess with rgb(' + str(data[i][1]) +','+ str(data[i][2]) +','+ str(data[i][3]) +')')
                for c in topcolor:
                    print(str(c[0]) +' at '+str(c[1]))
                print('good guess was : ' + str(data[i][0]))
            print('__________________________________________________________')
            total+=1
            i+=1
        efficiency = good_guesses/total
        print('efficiency : ' + str(efficiency))
        return efficiency
# ===============================================================================================
    def save(self, ask=False):
        if ask:
            if input('save model? Y/N : ') != 'Y':
                return
        self.model.save(f'.\saved_model\{NAME}_{self.learning_rate}_{self.momentum}')

# ===============================================================================================
