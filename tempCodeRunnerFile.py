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