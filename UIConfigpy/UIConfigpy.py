# from pyvisa  import *
# from time import sleep
from pathlib import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import os

class Application(Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self,master)
        self.pack()
        self.initWidgets()
    

    def initWidgets(self):
        self.dv = DoubleVar()
        self.dt = DoubleVar()
        self.T  = DoubleVar()
        self.n  = IntVar()

        fm1 = ttk.Frame(self.master)
        fm1.pack(side=RIGHT,fill=BOTH,expand=YES)
        w = ttk.Label(fm1)
        bm = PhotoImage(file="C:\\Project\\HKMC_Python_Scripts\\UIConfigpy\\UIConfigpy.png")
        w.x = bm
        w["image"] = bm
        w.pack()    

        fm2 = ttk.Frame(self.master)
        fm2.pack(side=LEFT,padx=50,expand=YES)  #fill=BOTH,
        """ 
        # createButton["background"] = "gray"
        # createButton["activebackground"] = "green"
        # createButton["width"] = "7"
        # createButton["height"] = "1"
        # createButton["borderwidth"] = "10"
        # createButton["font"] = ("Times,14")  #Helvetica  Courier
        only apply to tkinter rather than ttk
        """
        tiltle_dv = ttk.Label(fm2,text="Please input an value to set dv:V (Necessary)")
        tiltle_dv.pack()
        self.f_dv=ttk.Entry(fm2,textvariable=self.dv,text="dv",width=5,font=("Times",13,"bold"),foreground="red")   #highlightbackgroud="blue",
        self.f_dv.pack(side=TOP,fill=BOTH,pady=10,expand=YES)
        
        tiltle_dt = ttk.Label(fm2,text="Please input an value to set dt:ms (Necessary)")
        tiltle_dt.pack()
        self.f_dt=ttk.Entry(fm2,textvariable=self.dt,text="dt",width=5,font=("Times",13,"bold"),foreground="red")   #highlightbackgroud="blue",
        self.f_dt.pack(side=TOP,fill=BOTH,pady=10,expand=YES)

        tiltle_T = ttk.Label(fm2,text="Please input an value to set T:ms (Necessary)")
        tiltle_T.pack()
        self.f_T=ttk.Entry(fm2,textvariable=self.T,text="T",width=5,font=("Times",13,"bold"),foreground="red")   #highlightbackgroud="blue",
        self.f_T.pack(side=TOP,fill=BOTH,pady=10,expand=YES)

        tiltle_n = ttk.Label(fm2,text="Please input an value to set n with integer type (Necessary)")
        tiltle_n.pack()
        self.f_n=ttk.Entry(fm2,textvariable=self.n,text="n",width=5,font=("Times",13,"bold"),foreground="red")   #highlightbackgroud="blue",
        self.f_n.pack(side=TOP,fill=BOTH,pady=10,expand=YES)

        createButton = ttk.Button(fm2,text="exit")
        createButton.pack(side=BOTTOM,fill=Y,pady=30,expand=YES)
        createButton.bind('<Button-1>',self.exit)

        createButton = ttk.Button(fm2,text="creat")
        createButton.pack(side=BOTTOM,fill=Y,pady=30,expand=YES)
        createButton.bind('<Button-1>',self.create)

        createButton = ttk.Button(fm2,text="confirm")
        createButton.pack(side=BOTTOM,fill=Y,pady=30,expand=YES)
        createButton.bind('<Button-1>',self.confirm)


    def create(self,event):
        # content = 'Configure={\n\t"dv"='+str(self.dv)+",\n\t"+'"dt"='+str(self.dt)+",\n\t"+'"T"='+str(self.T)+",\n\t"+'"n"='+str(self.n)+"\n}"
        # with open("Configure.json",mode='w',buffering=-1,encoding='UTF-8') as f:
        #     f.write(content)
        with open(os.path.dirname(os.path.realpath(__file__)).replace("\\","\\\\")+"\\Configure.json",mode='w',buffering=1,encoding='UTF-8') as f:
            result = []
            temp = {}
            temp['dv'] = self.dv
            temp['dt'] = self.dt
            temp['T'] = self.T
            temp['n'] = self.n
            result.append(temp)
            f.write(json.dumps(result,ensure_ascii=False))


    def exit(self,event):
        exit()


    def confirm(self,event):
        self.dv=self.f_dv.get()
        self.dt=self.f_dt.get()
        self.T=self.f_T.get()
        self.n=self.f_n.get()
        if((self.dv=="") or (self.n=="")):
            messagebox.showinfo(title="Warnning",message="There's one or more parameters not defined")
        if((self.dt=="")):
            self.dt = 0
        if((self.T=="")):
            self.T = 0
        

app = Application()
app.master.title("oscilliscope configuration")
app.mainloop()
        

