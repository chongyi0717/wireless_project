from math import sqrt,log10
import tkinter as tk
from tkinter.constants import CENTER, LEFT, NW, SUNKEN, TRUE
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pickle
import pathlib
DISTANCE = 2.5
PROBABILITY_OF_CAR_ENTRY=1/12
SPEED = 0.02
CALL_TIME=5
MAP_TIME=3600
BEST_EFFORT_FILE_NAME="best_effort.txt"
THRESHOLD_FILE_NAME="threshold.txt"
ENTROPY_FILE_NAME="entropy.txt"
MY_ALGO_FILE_NAME="my_algo.txt"
def adjust_for_map(num):
        return 20*num

class Car:
    def __init__(self,x,y,direction):
        self.x=x
        self.y=y
        self.direction=direction
        self.signal=0
        self.signal_array={}
        self.base_station_picked=0
        self.mode="release"
        self.call_time=0
        self.real_call_time=0
        self.speed=adjust_for_map(SPEED)
        self.lb=tk.Label(background="red")
        self.lb.place(x=x,y=y,width=5,height=5)
    def move_straight(self,seed):
        if(self.direction=="TOP"):
            if(seed==-1):
                pass
            elif(seed>0 and seed <= 0.5):
                self.direction="TOP"
            elif(seed>0.5 and seed <= 0.5625):
                self.direction="BOTTOM"
            elif(seed>0.5625 and seed <= 0.78125):
                self.direction="LEFT"
            elif(seed>0.78125 and seed <= 1):
                self.direction="RIGHT"
        elif(self.direction=="BOTTOM"):
            if(seed==-1):
                pass
            elif(seed>0 and seed <= 0.5):
                self.direction="BOTTOM"
            elif(seed>0.5 and seed <= 0.5625):
                self.direction="TOP"
            elif(seed>0.5625 and seed <= 0.78125):
                self.direction="LEFT"
            elif(seed>0.78125 and seed <= 1):
                self.direction="RIGHT"

        elif(self.direction=="LEFT"):
            if(seed==-1):
                pass
            elif(seed>0 and seed <= 0.5):
                self.direction="LEFT"
            elif(seed>0.5 and seed <= 0.5625):
                self.direction="RIGHT"
            elif(seed>0.5625 and seed <= 0.78125):
                self.direction="TOP"
            elif(seed>0.78125 and seed <= 1):
                self.direction="BOTTOM"
        elif(self.direction=="RIGHT"):
            if(seed==-1):
                pass
            elif(seed>0 and seed <= 0.5):
                self.direction="RIGHT"
            elif(seed>0.5 and seed <= 0.5625):
                self.direction="LEFT"
            elif(seed>0.5625 and seed <= 0.78125):
                self.direction="TOP"
            elif(seed>0.78125 and seed <= 1):
                self.direction="BOTTOM"
        if(self.direction=="RIGHT"):
            self.x+=self.speed
        elif(self.direction=="LEFT"):
            self.x-=self.speed
        elif(self.direction=="TOP"):
            self.y-=self.speed
        elif(self.direction=="BOTTOM"):
            self.y+=self.speed
        self.lb.place(x=self.x,y=self.y)

class Intersection:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def generate_car(self):
        car = Car(self.x,self.y)

class Base_station:
    def __init__(self,x,y,num,frequency):
        self.x=x
        self.y=y
        self.num=num
        self.frequency=frequency
        self.lb=tk.Label(background="blue",text=num)
        self.lb.place(x=x,y=y,width=10,height=10)
        self.signal=120

class Map:
    def __init__(self,mode):
        self.win=tk.Tk()
        self.win.state("icon")
        self.win.title("handoff simulator")
        self.win.geometry("505x505")
        self.win.resizable(0,0)
        self.intersections=[]
        self.cars=[]
        self.base_station=[]
        self.handoff_count=0
        self.gaussin_count=0
        self.handoff_global=0
        self.time_count=0
        self.mode=mode
        self.handoff_list=[]
        self.time_list=[]
        self.pmin=15
        self.gate=25
        self.gaussin=np.random.normal(CALL_TIME*60,10,1000)
        i=0
        j=0
        z=1
        while(i<adjust_for_map(DISTANCE)*10):
            while(j<adjust_for_map(DISTANCE)*10):
                lb=tk.Label(borderwidth=3,relief=SUNKEN)
                lb.place(x=i,y=j,width=adjust_for_map(DISTANCE),height=adjust_for_map(DISTANCE),anchor=NW)
                rand = random.random()
                if(rand<0.1):
                    x=0
                    y=0
                    rand1=random.random()
                    if(rand1>0 and rand1<=0.25):
                        x=adjust_for_map(0.1)
                    elif(rand1>0.25 and rand1<=0.5):
                        x=-adjust_for_map(0.1)
                    elif(rand1>0.5 and rand1<=0.75):
                        y=adjust_for_map(0.1)
                    elif(rand1>0.75 and rand1<=1):
                        y=-adjust_for_map(0.1)
                    rand2=random.randint(1,10)*100
                    base=Base_station(i+x+adjust_for_map(DISTANCE)/2,j+y+adjust_for_map(DISTANCE)/2,z,rand2)
                    z+=1
                    self.base_station.append(base)
                    
                j+=adjust_for_map(DISTANCE)
            j=0
            i+=adjust_for_map(DISTANCE)
        for i in range(1,10):
            p1=int(adjust_for_map(DISTANCE))
            inter = Intersection(i*p1,0)
            self.intersections.append(inter)
        for i in range(1,10):
            p1=int(adjust_for_map(DISTANCE))
            inter = Intersection(i*p1,500)
            self.intersections.append(inter)
        for i in range(1,10):
            p1=int(adjust_for_map(DISTANCE))
            inter = Intersection(0,i*p1)
            self.intersections.append(inter)
        for i in range(1,10):
            p1=int(adjust_for_map(DISTANCE))
            inter = Intersection(500,i*p1)
            self.intersections.append(inter)
        self.win.after(0,self.update_clock)

    def update_clock(self):
        self.handoff_global+=self.handoff_count
        self.handoff_count=0
        self.time_count+=1
        for i in self.intersections:
            rand=random.random()
            if(rand<PROBABILITY_OF_CAR_ENTRY):
                direction=""
                if(i.x==0):
                    direction="RIGHT"
                elif(i.x==500):
                    direction="LEFT"
                elif(i.y==0):
                    direction="BOTTOM"
                elif(i.y==500):
                    direction="TOP"
                car = Car(i.x,i.y,direction)
                self.cars.append(car)

        for i in self.cars:
            if(i.mode=="call"):
                for j in self.base_station:
                    distance=sqrt((i.x-j.x)**2+(i.y-j.y)**2)
                    i.signal_array[j.num]=j.signal-(32.45+20*log10(1000)+20*log10(distance/20))
                key_max=max(i.signal_array.keys(), key=(lambda k: i.signal_array[k]))
                if(i.real_call_time==0):
                    i.signal=i.signal_array[key_max]
                    i.base_station_picked=key_max
                else:
                    # algorithm best effort
                    if(self.mode=="best_effort"):
                        if(i.base_station_picked!=key_max and i.base_station_picked!=0):
                            #print("%d %f %d %f"%(i.base_station_picked,i.signal_array[i.base_station_picked],key_max,i.signal_array[key_max]))
                            i.base_station_picked=key_max
                            i.signal=i.signal_array[i.base_station_picked]
                            self.handoff_count+=1
                        else:
                            i.signal=i.signal_array[i.base_station_picked]
                    #algorithm threshold
                    elif(self.mode=="threshold"):
                        if(i.signal<self.pmin and i.base_station_picked!=0 and i.base_station_picked!=key_max):
                            #print("%d %f %d %f"%(i.base_station_picked,i.signal_array[i.base_station_picked],key_max,i.signal_array[key_max]))
                            i.base_station_picked=key_max
                            i.signal=i.signal_array[i.base_station_picked]
                            self.handoff_count+=1
                        else:
                            i.signal=i.signal_array[i.base_station_picked]
                    #algorithm entropy
                    elif(self.mode=="entropy"):
                        if(key_max-i.signal>self.gate and i.base_station_picked!=0 and i.base_station_picked!=key_max):
                            #print("%d %f %d %f"%(i.base_station_picked,i.signal_array[i.base_station_picked],key_max,i.signal_array[key_max]))
                            i.base_station_picked=key_max
                            i.signal=i.signal_array[i.base_station_picked]
                            self.handoff_count+=1
                        else:
                            i.signal=i.signal_array[i.base_station_picked]
                    #algorithm new
                    elif(self.mode=="my_algorithm"):
                        if(i.base_station_picked!=0 and i.base_station_picked!=key_max 
                        and(i.x % adjust_for_map(1)==0 or i.y % adjust_for_map(1)==0)):
                            #print("%d %f %d %f"%(i.base_station_picked,i.signal_array[i.base_station_picked],key_max,i.signal_array[key_max]))
                            i.base_station_picked=key_max
                            i.signal=i.signal_array[i.base_station_picked]
                            #print("%d %d"%(i.x,i.y))
                            self.handoff_count+=1
                        else:
                            i.signal=i.signal_array[i.base_station_picked]
                    else:
                        print(self.mode)
                i.real_call_time+=1
                if(i.real_call_time>=i.call_time):
                    i.mode="release"
                    i.call_time=0
                    i.real_call_time=0
            if(int(i.x) % int(adjust_for_map(2.5)) == 0 and int(i.y) % int(adjust_for_map(2.5)) ==0):
                rand=random.random()
            else:
                rand=-1
            i.move_straight(rand)
            if(i.x>500 or i.x<0 or i.y<0 or i.y>500):
                i.lb.destroy()
                self.cars.remove(i)
            rand=random.random()
            if(rand<(1/1800)):
                i.mode="call"
                i.call_time=self.gaussin[self.gaussin_count%1000]
                self.gaussin_count+=1
        self.handoff_list.append(self.handoff_count)
        self.time_list.append(self.time_count)
        if(self.time_count>MAP_TIME):
            self.win.quit()
        else:
            self.win.after(10,self.update_clock)
            
        

def main():
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
    filename=""
    count=90
    for i in range(count):
        mp=Map("best_effort")
        mp.win.mainloop()
        mp.win.destroy()
        if(mp.mode=="best_effort"):
            filename=BEST_EFFORT_FILE_NAME
        elif(mp.mode=="threshold"):
            filename=THRESHOLD_FILE_NAME
        elif(mp.mode=="entropy"):
            filename=ENTROPY_FILE_NAME
        elif(mp.mode=="my_algorithm"):
            filename=MY_ALGO_FILE_NAME
        with open(filename,"rb") as fp:
            try:
                list=pickle.load(fp)
            except EOFError:
                list=[]
        list.append(mp.handoff_global)
        print(list)
        
        with open(filename,"wb") as fp:
            pickle.dump(list,fp)
    for i in range(count):
        mp=Map("threshold")
        mp.win.mainloop()
        mp.win.destroy()
        if(mp.mode=="best_effort"):
            filename=BEST_EFFORT_FILE_NAME
        elif(mp.mode=="threshold"):
            filename=THRESHOLD_FILE_NAME
        elif(mp.mode=="entropy"):
            filename=ENTROPY_FILE_NAME
        elif(mp.mode=="my_algorithm"):
            filename=MY_ALGO_FILE_NAME
        with open(filename,"rb") as fp:
            try:
                list=pickle.load(fp)
            except EOFError:
                list=[]
        list.append(mp.handoff_global)
        print(list)
        
        with open(filename,"wb") as fp:
            pickle.dump(list,fp)
    for i in range(count):
        mp=Map("entropy")
        mp.win.mainloop()
        mp.win.destroy()
        if(mp.mode=="best_effort"):
            filename=BEST_EFFORT_FILE_NAME
        elif(mp.mode=="threshold"):
            filename=THRESHOLD_FILE_NAME
        elif(mp.mode=="entropy"):
            filename=ENTROPY_FILE_NAME
        elif(mp.mode=="my_algorithm"):
            filename=MY_ALGO_FILE_NAME
        with open(filename,"rb") as fp:
            try:
                list=pickle.load(fp)
            except EOFError:
                list=[]
        list.append(mp.handoff_global)
        print(list)
        
        with open(filename,"wb") as fp:
            pickle.dump(list,fp)
    for i in range(count):
        mp=Map("my_algorithm")
        mp.win.mainloop()
        mp.win.destroy()
        if(mp.mode=="best_effort"):
            filename=BEST_EFFORT_FILE_NAME
        elif(mp.mode=="threshold"):
            filename=THRESHOLD_FILE_NAME
        elif(mp.mode=="entropy"):
            filename=ENTROPY_FILE_NAME
        elif(mp.mode=="my_algorithm"):
            filename=MY_ALGO_FILE_NAME
        with open(filename,"rb") as fp:
            try:
                list=pickle.load(fp)
            except EOFError:
                list=[]
        list.append(mp.handoff_global)
        print(list)
        
        with open(filename,"wb") as fp:
            pickle.dump(list,fp)
    with open("gaussin.txt","wb") as fp:
        pickle.dump(mp.gaussin,fp)
    print(len(list))

if __name__=="__main__":
    main()
