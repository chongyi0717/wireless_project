import pickle
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from tkinter.constants import CENTER, LEFT, NW, SUNKEN, TRUE
BEST_EFFORT_FILE_NAME="best_effort.txt"
THRESHOLD_FILE_NAME="threshold.txt"
ENTROPY_FILE_NAME="entropy.txt"
MY_ALGO_FILE_NAME="my_algo.txt"
listy=[]
list=[]
file=pathlib.Path(BEST_EFFORT_FILE_NAME)
file.touch(exist_ok=TRUE)
file=pathlib.Path(THRESHOLD_FILE_NAME)
file.touch(exist_ok=TRUE)
file=pathlib.Path(ENTROPY_FILE_NAME)
file.touch(exist_ok=TRUE)
file=pathlib.Path(MY_ALGO_FILE_NAME)
file.touch(exist_ok=TRUE)
file=pathlib.Path("gaussin.txt")
file.touch(exist_ok=TRUE)
with open(BEST_EFFORT_FILE_NAME,"rb") as fp:
        try:
            list=pickle.load(fp)
        except EOFError:
            list=[0]
        best_effort_mean=np.mean(list)
        print(best_effort_mean)
        listy.append(best_effort_mean)
with open(THRESHOLD_FILE_NAME,"rb") as fp:
        try:
            list=pickle.load(fp)
        except EOFError:
            list=[0]
        threshold_mean=np.mean(list)
        print(threshold_mean)
        listy.append(threshold_mean)
with open(ENTROPY_FILE_NAME,"rb") as fp:
        try:
            list=pickle.load(fp)
        except EOFError:
            list=[0]
        entropy_mean=np.mean(list)
        print(entropy_mean)
        listy.append(entropy_mean)
with open(MY_ALGO_FILE_NAME,"rb") as fp:
        try:
            list=pickle.load(fp)
        except EOFError:
            list=[0]
        my_algo_mean=np.mean(list)
        print(my_algo_mean)
        listy.append(my_algo_mean)
listx=["best effort","threshold","entropy","my algorithm"]
plt.bar(listx,listy)
plt.title("Average of handoff time in different algorithm")
plt.show()
with open("gaussin.txt","rb") as fp:
    list=pickle.load(fp)
plt.title("Call time distribution")
plt.xlabel("call time (sec)")
plt.ylabel("Frequency of call time")
plt.hist(list)
plt.show()