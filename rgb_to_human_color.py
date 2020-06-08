import numpy as np
import csv

# code is inspired from this tutorial : https://realpython.com/python-windows-machine-learning-setup/#introducing-anaconda-and-conda

import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

colorDict = {'red':0, 'orange':1, 'yellow':2, 'green':3, 'blue':4,'purple':5,'brown':6,'pink':7, 'gray':8}
colorIndexDict = {b:a for a,b in colorDict.items()}

with open('./color_training.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
for d in data:
    d[0] = colorDict[d[0]]

rgb_vals = [[r,g,b] for c,r,g,b in data]
X = np.array(rgb_vals)

rows = []
for c,r,g,b in data:
    r = [0,0,0,0,0,0,0,0,0]
    r[c]=1
    rows.append(r)
y = np.array(rows)

model = Sequential()
model.add(Dense(3, input_dim=3))
model.add(Activation('softsign'))
model.add(Dense(9))
model.add(Activation('softmax'))

ep = 10000
learning_rate = 0.09
decay_rate = learning_rate / ep
momentum = 0.7
sgd = SGD(lr=learning_rate, momentum=momentum, decay=decay_rate, nesterov=False)
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

# sgd = SGD(lr=0.2, momentum=0.07)
# model.compile(loss='mean_squared_error', optimizer=sgd)


model.fit(X, y, batch_size=64, epochs=ep)

def get_key(result, val): 
    for key, value in result.items(): 
         if val == value: 
             return key 

def verify():
    with open('./color_verif.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

if __name__ == '__main__':
    print("Verification data, good answers shown here : ")
    data = verify()
    test_rgb = [[r,g,b] for c,r,g,b in data]
    test_rgb = np.array(test_rgb)
    results = model.predict(test_rgb)

    good_guess = 0
    total = 0
    i = 0
    for r in results:
        doubleR = []
        j = 0
        for c in r:
            doubleR.append((colorIndexDict[j],c))
            j+=1
        topcolor = sorted(doubleR, key = lambda c:c[1])[::-1]
        topcolor = topcolor[0:3]
        # print('top candidate colors (desc) for: ')
        # for c in topcolor:
        #     print(str(c[0]))
        # print()
        # print('most likely : ' + topcolor[0][0])
        # print('selon ced : ' + data[i][0])
        if topcolor[0][0] == data[i][0]:
            print(topcolor[0][0] + ' @ rgb(' + str(data[i][1]) +','+ str(data[i][2]) +','+ str(data[i][3]) +')    at ' + str(topcolor[0][1]))
            good_guess+=1

        # elif topcolor[1][0] == data[i][0]:
        #     print('ALMOST : ' + topcolor[1][0] + ' @ rgb(' + str(data[i][1]) +','+ str(data[i][2]) +','+ str(data[i][3]) +')    at ' + str(topcolor[1][1]))
        #     print('first was : ' + topcolor[0][0] + ' @ rgb(' + str(data[i][1]) +','+ str(data[i][2]) +','+ str(data[i][3]) +')    at ' + str(topcolor[0][1]))
        #     good_guess+=1
        #     print('__________________________________________________________')
        else:
            print('Wrong guess with rgb(' + str(data[i][1]) +','+ str(data[i][2]) +','+ str(data[i][3]) +')')
            for c in topcolor:
                print(str(c[0]) +' at '+str(c[1]))
            print('good guess was : ' + str(data[i][0]))


        print('__________________________________________________________')
        total+=1
        i+=1
    print('efficiency : ' + str(good_guess) + '/' + str(total))