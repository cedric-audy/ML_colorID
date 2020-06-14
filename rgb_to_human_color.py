import numpy as np
import csv
import keras
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD


TRAINING_DATA = './data/color_training.csv'

# ===============================================================================================
class Model:
    # ===============================================================================================
    def __init__(self,epochs =5000, learning_rate=0.99,momentum = 0.8):
        self.colorDict = {'red':0, 'orange':1, 'yellow':2, 'green':3, 'blue':4,'purple':5,'brown':6,'pink':7, 'gray':8}
        self.colorIndexDict = {b:a for a,b in self.colorDict.items()}
        self.model = None
        self.epochs = epochs
        self.sgd = SGD(lr=learning_rate, momentum=momentum, decay=learning_rate/epochs , nesterov=True)

    def train(self):
        with open(TRAINING_DATA, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        for d in data:
            d[0] = self.colorDict[d[0]]
        rgb_vals = [[r,g,b] for c,r,g,b in data]
        X = np.array(rgb_vals) #training rgb vals
        
        #answers(human color)
        rows = []
        for c,r,g,b in data:
            r = [0,0,0,0,0,0,0,0,0]
            r[c]=1
            rows.append(r)
        y = np.array(rows)
        self.model.compile(loss='mean_squared_error', optimizer=self.sgd, metrics=['accuracy'])
        self.model.fit(X, y, batch_size=256, epochs=self.epochs)

    def buildModel(self):
        self.model = Sequential()
        self.model.add(Dense(9, input_dim=3))
        self.model.add(Activation('sigmoid'))
        self.model.add(keras.layers.Dropout(0.05))
        self.model.add(keras.layers.Dense(9, activation='sigmoid'))
        self.model.add(keras.layers.Dropout(0.05))
        # Add a dropout layer for previous hidden layer
        self.model.add(keras.layers.Dense(9, activation='softmax'))
    
    def predictResults(self, arr):
        return self.model.predict(arr)

def verify():
    with open('./data/color_verif.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

if __name__ == '__main__':
    print("Verification data, good answers shown here : ")
    data = verify()
    test_rgb = [[r,g,b] for c,r,g,b in data]
    test_rgb = np.array(test_rgb)
    m = Model()
    m.buildModel()
    m.train()
    results = m.predictResults(test_rgb)

    good_guesses = 0
    total = 0
    i = 0
    for r in results:
        doubleR = []
        j = 0
        for c in r:
            doubleR.append((m.colorIndexDict[j],c))
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
    print('efficiency : ' + str(good_guesses) + '/' + str(total))