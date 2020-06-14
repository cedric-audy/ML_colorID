import numpy as np
import csv
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

colorDict = {'red':0, 'orange':1, 'yellow':2, 'green':3, 'blue':4,'purple':5,'brown':6,'pink':7, 'gray':8}
colorIndexDict = {b:a for a,b in colorDict.items()}

with open('./data/color_training.csv', newline='') as f:
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
model.add(Dense(9, input_dim=3))
model.add(Activation('sigmoid'))
model.add(keras.layers.Dense(9, activation='sigmoid'))
model.add(keras.layers.Dense(9, activation='sigmoid'))
model.add(keras.layers.Dense(9, activation='softmax'))

ep = 5000
learning_rate = 0.7
decay_rate = learning_rate / ep
momentum = 0.7
sgd = SGD(lr=learning_rate, momentum=momentum, decay=decay_rate, nesterov=False)

model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.fit(X, y, batch_size=256, epochs=ep)

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
    results = model.predict(test_rgb)

    good_guesses = 0
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