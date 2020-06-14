import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
class plotAccuracy:
    def __init__(self, path):
        self.data = self.readData(path)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x=[]
        y=[]
        z=[]
        for acc,lr,m in self.data:
            x.append(float(lr))
            y.append(float(m))
            z.append(float(acc))
            

        ax.scatter(x, y, z, c = 'r', marker='o')

        ax.set_xlabel('Learning rate')
        ax.set_ylabel('Momentum')
        ax.set_zlabel('Accuracy')

        plt.show()

    def readData(self, path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data