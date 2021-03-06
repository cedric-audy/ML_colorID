import tkinter as tk
from csv import writer
from datetime import datetime
import random as rand

class Application(tk.Frame):
    def __init__(self, path, master=None):
        self.path = path
        rand.seed(datetime.now())
        super().__init__(master)
        self.master = master
        self.pack()
        self.data = (0,0,0)
        self.color = ""
        self.create_widgets()
        self.rgb_sample
        self.training_data = []


    def random_rgb_as_hex(self):
        self.data = (
            rand.randrange(255),
            rand.randrange(255),
            rand.randrange(255)
            )
        return "#%02x%02x%02x" % self.data   

    def curColor(self,c):
        self.color = c
        self.update()

    def create_widgets(self):
        self.rgb_sample = tk.Label(self, width=50, height=20)
        self.rgb_sample.configure(bg=self.random_rgb_as_hex())
        self.rgb_sample.pack(side="top")
        
        buttonArr = []
        buttonArr.append(tk.Button(self, text='red', font=("arial",32), command =lambda:self.curColor('red')))
        buttonArr.append(tk.Button(self, text='yellow',font=("arial",32), command =lambda:self.curColor('yellow')))
        buttonArr.append(tk.Button(self, text='orange', font=("arial",32),command =lambda:self.curColor('orange')))
        buttonArr.append(tk.Button(self, text='green', font=("arial",32),command =lambda:self.curColor('green')))
        buttonArr.append(tk.Button(self, text='blue', font=("arial",32),command =lambda:self.curColor('blue')))
        buttonArr.append(tk.Button(self, text='purple', font=("arial",32),command =lambda:self.curColor('purple')))
        buttonArr.append(tk.Button(self, text='brown', font=("arial",32),command =lambda:self.curColor('brown')))
        buttonArr.append(tk.Button(self, text='pink', font=("arial",32),command =lambda:self.curColor('pink')))
        buttonArr.append(tk.Button(self, text='gray', font=("arial",32),command =lambda:self.curColor('gray')))
        
        for b in buttonArr:
            b.pack(side="right")

    def append_list_as_row(self, file_name, list_of_elem):
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)

    def update(self):
        print(self.color)
        print(self.data)
        print()

        row_contents = [self.color, self.data[0], self.data[1], self.data[2]]
        self.append_list_as_row(self.path, row_contents)
        self.training_data.append((self.color,))
        self.rgb_sample.configure(bg=self.random_rgb_as_hex())

if __name__ == '__main__':
    for i in range(0,255):
         with open('data\color_training.csv', 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(['gray', i, i, i])
           