# My first try at Machine learning : Guessing colors from RGB values

In this home project, I learned to set up a machine learning environment, using Anaconda (MiniConda3), Python 3.7.7 and Keras 2.3.1(high level API for TensorFlow 2.1.0). 

The goal of the program is to accurately guess a color's name among 9 choices (grayscale, pink, brown, purple, blue, green, orange, yellow, red) based on its RGB value.

For training, I wrote a small tkinter program that displays a random rgb value, which you have to assign to one of the 9 values. Training data are written in a csv file. The same process is performed for the verification data.


![trainer](/img/trainer.jpg)


The results are fairly disappointing, with the accuracy of the algorithm oscillating between 60% and 75% (eyeball). A plausible explanation is the inefficiency of the small supervised training program I wrote, combined with my own inability to label edge cases in a consistent and satisfying way, or then again the lack of choices. The program notably fails at identifying orange or brown at all, and distinguishing between red,pink, and purple.


![results](/img/results.jpg)