from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
from tkinter.ttk import Combobox
from tkinter import StringVar
import numpy as np
from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
import matplotlib
from datetime import datetime
matplotlib.use("TkAgg")
from PIL import Image, ImageTk
import os
import pathlib

cwd=pathlib.Path(__file__).parent.absolute()
file_list = os.listdir('C:\\UteriAN\\CSV')
sorted_files =  sorted(file_list)
last_file = len(sorted_files)
A = 'C:\\UteriAN\\CSV\\' + str(sorted_files[last_file-1])
print(A)
 
now=datetime.now()
new_date = now.strftime("%d/%m/%Y , %H:%M:%S")


LARGE_FONT= ("Verdana", 12)
style.use("dark_background")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

f1 = Figure(figsize=(5,5), dpi=100)
a1 = f1.add_subplot(211)
a2 = f1.add_subplot(212)


f2 = Figure(figsize=(5,5), dpi=80)
a3 = f2.add_subplot(421)
a4 = f2.add_subplot(422)
a5 = f2.add_subplot(423)
a6 = f2.add_subplot(424)
a7 = f2.add_subplot(425)
a8 = f2.add_subplot(426)
a9 = f2.add_subplot(427)
a10 = f2.add_subplot(428)


def getParam(wantedParam):
    switcher = {
        'numOfChannels': 4, # number of channels (coloumns) to use from the data file (max 8)
        'numShow': 6000, # number of samples to show each iteration (6000 => 10 min when sample rate = 0.1)
        'epsilon': 0.01, # small number to add when numerator is very small
        'firstValues': 10, # choose number of first values to mean
        'lastValues': 5, # choose number of last values to mean
        'samplingRate': 0.1, # 0.1 => 10 samples each sec
        'filename': 'C:\\UteriAN\\CSV\\' + str(sorted_files[last_file-1]) , # path to file + file name of the data
    }
    return switcher.get(wantedParam)


def animate(i):
    file_name = getParam('filename') # path to file + file name
    df = pd.read_csv(file_name)

    k=getParam('numOfChannels') # choose number of columns (channels)
    numShow = getParam('numShow') 
    samplingRate = getParam('samplingRate')
    factor = []
    meanList = []
    if k == 1:
        factor = 1.05
    if k != 1:
        factor = 3        

    for j in range (0,len(df)):
        
        if df.iloc[j,0:k].count() == k:
            meanList.append(np.mean(df.iloc[j,0:k]))
        
       
    time1 = np.arange(0,len(meanList)*samplingRate,samplingRate)
    startTime = time1
    meanListNew = meanList
    if len(meanList)>numShow:
        startTime = time1[(len(meanList)-numShow):len(meanList)] 
        meanListNew = meanList[(len(meanList)-numShow):len(meanList)]  
    
    a.clear()
    a.title.set_text('First Plot')
    a.grid(True, linewidth=0.3, color='white', linestyle='-')
    a.set_xlabel('Time [sec]')
    a.set_ylabel('Potential [mv]')
    if len(meanList)!= 0 and file_name == str(cwd) + '\\TestWithMatlab.csv':
        a.axis(xmin=0,xmax=600,ymin=-1.05,ymax=1.05)  # set xlim and ylim
    if len(meanList) != 0 and file_name == str(cwd) + '\\ExampleDataFile.csv':
        a.axis(xmin=0,xmax=600,ymin=meanList[0]/1.05,ymax=meanList[0]*factor)  # set xlim and ylim
    if len(meanList) != 0 and file_name == 'C:\\UteriAN\\CSV\\' + str(sorted_files[last_file-1]):
        a.axis(xmin=0,xmax=600,ymin=meanList[0]/1.05,ymax=meanList[0]*factor)  # set xlim and ylim   
    if file_name == 'C:\\UteriAN\\CSV\\' + str(sorted_files[last_file-1]) and len(meanListNew) != 0  and len(meanListNew) < 20:
        f.canvas.draw()
        print('!')    
    return a.plot(startTime,meanListNew)


def animate2(i):
    file_name = getParam('filename') # path to file + file name
    df = pd.read_csv(file_name)

    k=getParam('numOfChannels') # choose number of columns (channels)
    eps = getParam('epsilon')
    numShow = getParam('numShow') # 10 min
    samplingRate = getParam('samplingRate')
    relative = []
    first = []
    time2 = []
    n = getParam('firstValues') # choose number of first values
    m = getParam('lastValues')  # choose number of last values

    if df.iloc[:,k-1].count() < n:
        relative = []

    if (df.iloc[:,k-1].count() > n and df.iloc[:,k-1].count() < (n+m)):
        first = np.mean(df.iloc[0:n,0:k])
        for j in range (n,df.iloc[:,k-1].count()):
            if df.iloc[j,0:k].count() == k:
                relative.append(np.sum(abs((df.iloc[j,0:k]-first)/first)))
                if (abs(relative[len(relative)-1]/(relative[len(relative)-2]+0.00001)) > 10):
                    relative[len(relative)-1] = np.sum(abs(((df.iloc[j,0:k]-first)/(first + eps))))

    if df.iloc[:,k-1].count() > (n+m):
        first = np.mean(df.iloc[0:n,0:k]) 
        for i in range (n+m+1,df.iloc[:,k-1].count()+1):
            if df.iloc[i-1,0:k].count() == k:
                relative.append(np.sum(abs((np.mean(df.iloc[i-m:i-1,0:k])-first)/first)))
                if (abs(relative[len(relative)-1]/(relative[len(relative)-2]+0.00001)) > 10):
                    relative[len(relative)-1] = np.sum(abs((np.mean(df.iloc[i-m:i-1,0:k])-first)/(first + eps)))

    time2 = np.arange(samplingRate,(len(relative)+1)*samplingRate,samplingRate)
    startTime = []
    relativeNew = []
    if df.iloc[:,k-1].count()-(n+m) <= numShow:
        startTime = time2[0:df.iloc[:,k-1].count()-(n+m)] 
        relativeNew = relative[0:df.iloc[:,k-1].count()-(n+m)]
    elif df.iloc[:,k-1].count()-(n+m) > numShow:
        startTime = time2[(df.iloc[:,k-1].count()-(n+m)-numShow):df.iloc[:,k-1].count()-(n+m)] 
        relativeNew = relative[(df.iloc[:,k-1].count()-(n+m)-numShow):df.iloc[:,k-1].count()-(n+m)]
    
    a1.clear()
    a1.set_title('Sum Based Relative',size=10)
    a1.xaxis.set_ticklabels([])
    a1.grid(True, linewidth=0.3, color='white', linestyle='-')
    a1.set_ylabel('Relative Potential [A.U.]')
    a1.axis(xmin=0,xmax=600,ymin=-0.5,ymax=k*2.15)  # set xlim and ylim
    return a1.plot(startTime,relativeNew,'turquoise')

def animate4(i):
    file_name = getParam('filename') # path to file + file name
    df = pd.read_csv(file_name)

    k=getParam('numOfChannels') # choose number of columns (channels)
    numShow = getParam('numShow') # 10 min
    samplingRate = getParam('samplingRate')
    absolute = []
    first = []
    time2 = []
    n = getParam('firstValues') # choose number of first values
    m = getParam('lastValues')  # choose number of last values
    factor = []
    if k == 1 or k==7 or k==8:
        factor = 3
    elif k == 2 or k==3:
        factor = 500   
    elif k == 4 or k==5:
        factor = 250 
    elif k == 6:
        factor = 200 

    if df.iloc[:,k-1].count() < n:
        absolute = []

    if (df.iloc[:,k-1].count() > n and df.iloc[:,k-1].count() < (n+m)):
        first = np.mean(df.iloc[0:n,0:k])
        for j in range (n,df.iloc[:,k-1].count()):
            if df.iloc[j,0:k].count() == k:
                absolute.append(np.sum(abs(df.iloc[j,0:k]-first)))

    if df.iloc[:,k-1].count() > (n+m):
        first = np.mean(df.iloc[0:n,0:k]) 
        for i in range (n+m+1,df.iloc[:,k-1].count()+1):
            if df.iloc[i-1,0:k].count() == k:
                absolute.append(np.sum(abs(np.mean(df.iloc[i-m:i-1,0:k])-first)))

    time2 = np.arange(samplingRate,(len(absolute)+1)*samplingRate,samplingRate)
    startTime = []
    absoluteNew = []
    if df.iloc[:,k-1].count()-(n+m) <= numShow:
        startTime = time2[0:df.iloc[:,k-1].count()-(n+m)] 
        absoluteNew = absolute[0:df.iloc[:,k-1].count()-(n+m)] 
    elif df.iloc[:,k-1].count()-(n+m) > numShow:
        startTime = time2[(df.iloc[:,k-1].count()-(n+m)-numShow):df.iloc[:,k-1].count()-(n+m)] 
        absoluteNew = absolute[(df.iloc[:,k-1].count()-(n+m)-numShow):df.iloc[:,k-1].count()-(n+m)]  
        
    a2.clear()
    a2.set_title('Sum Based Absolute',size=10)
    a2.set_xlabel('Time [sec]')
    a2.set_ylabel('Absolute Potential [A.U.]')
    a2.grid(True, linewidth=0.3, color='white', linestyle='-')
    if len(absoluteNew) != 0 and file_name == str(cwd) + '\\TestWithMatlab.csv':
        a2.axis(xmin=0,xmax=600,ymin=-0.5,ymax=k*2.15)  # set xlim and ylim
    if len(absoluteNew) != 0 and file_name == str(cwd) + '\\ExampleDataFile.csv':
        a2.axis(xmin=0,xmax=600,ymin=-0.5,ymax=absoluteNew[0]*factor*k)  # set xlim and ylim
    if len(absoluteNew) != 0 and file_name == 'C:\\UteriAN\\CSV\\' + str(sorted_files[last_file-1]):
        a2.axis(xmin=0,xmax=600,ymin=-0.5,ymax=absoluteNew[0]*factor*k)  # set xlim and ylim
    # a2.axis(xmin=0,xmax=600)  # set xlim
    if file_name == 'C:\\UteriAN\\CSV\\' + str(sorted_files[last_file-1]) and len(absoluteNew) != 0  and len(absoluteNew) < 40:
        f1.canvas.draw()
        print('?')    
    return a2.plot(startTime,absoluteNew,'deepskyblue')


def animate3(i):
    file_name = getParam('filename') # path to file + file name
    df = pd.read_csv(file_name)
    samplingRate = getParam('samplingRate')  
    k=getParam('numOfChannels') # choose number of columns (channels) 
    #time3 = np.arange(0,len(df.iloc[:,0])*samplingRate,samplingRate)
    a3.clear()
    a4.clear()
    a5.clear()
    a6.clear()
    a7.clear()
    a8.clear()
    a9.clear()
    a10.clear()
    
    a=[a3,a4,a5,a6,a7,a8,a9,a10]
    for j in range(k):
        time3 = np.arange(0,len(df.iloc[:,j])*samplingRate,samplingRate)
        a[j].plot(time3,df.iloc[:,j])
        a[j].set_title('Channel{}'.format(j+1),size=8)
        if j<k-2:
            a[j].xaxis.set_ticklabels([])
        a[j].grid(True, linewidth=0.3, color='white', linestyle='-')
    
    f2.text(0.5, 0.04, 'Time [sec]', ha='center')
    f2.text(0.02, 0.5, 'Potential [mv]', va='center', rotation='vertical')

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "UteriAN Real Time Monitoring")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def validate(self, *args):
            if (len(Test_Type.get())>2) and Test_Name.get() and Patient_Name.get(): #if both StringVars has content
                # print("normal")
                button.config(state='normal')
            else:
                # print("disabled")
                button.config(state='disabled')
        tk.Frame.__init__(self, parent, bg='#101010')
        global Patient_Name
        Patient_Name = StringVar() #create StringVars for request
        label = tk.Label(self, text="Patient Name:", font=(
            'calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=80)
        e = tk.Entry(self, bg="#696969", fg="white",textvariable=Patient_Name)
        e.place(x=150, y=85, height=25, width=150)
        Patient_Name.trace("w",validate) #trace changes on StringVar
        global Test_Name
        Test_Name = StringVar() #ditto for execution
        label = tk.Label(self, text="Test Name:", font=(
            'calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=110)
        e = tk.Entry(self, bg="#696969", fg="white",textvariable=Test_Name)
        e.place(x=150, y=115, height=25, width=150)
        Test_Name.trace("w",validate)

        

        label = tk.Label(self, text="Test Date:", font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=50)

        v = StringVar(self)
        label = tk.Label(self, textvariable=v, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=150, y=55)
        v.set(new_date)

        combostyle = ttk.Style()

        combostyle.theme_create('custom_style',
                         parent='alt',
                         settings={'TCombobox':
                                   {'configure':
                                     {'selectforeground': 'white',
                                    'selectbackground': '#696969',
                                    'fieldforeground': 'white',
                                    'fieldbackground': '##696969',
                                    'background': '#696969'}}})
        combostyle.theme_use('custom_style')
        Test_Type = StringVar(self)
        # var.set("1")
        # data = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
        #         '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
        # cb = Combobox(self,foreground="white", values=data)
        self.option_add("*TCombobox*Listbox*Background", '#696969')
        self.option_add("*TCombobox*Listbox*foreground", 'white')
        # self.option_add('*TCombobox*Listbox.selectBackground', 'yellow')
        self.option_add('*TCombobox*Listbox.selectForeground', 'white')
        # cb.place(x=150, y=115, height=25, width=40)

        # var.set("January")
        # data = (' January',
        #         ' February',
        #         ' March',
        #         ' April',
        #         ' May',
        #         ' June',
        #         ' July',
        #         ' August',
        #         ' September',
        #         ' October',
        #         ' November',
        #         ' December')
        # cb = Combobox(self,foreground="white", values=data)
        # cb.place(x=192, y=115, height=25, width=90)
        # var.set("2020")
        # data = (' 2020', ' 2021', ' 2022')
        # cb = Combobox(self, foreground="white",values=data)
        # cb.place(x=284, y=115, height=25, width=60)


        label = tk.Label(self, text="Test Type:", font=(
            'calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=140)
        # var=StringVar()
        Test_Type.set(" ")
        data = ("Phantom A", "Phantom B", "Animal", "Patient")
        cb = Combobox(self,foreground="white", values=data, textvariable=Test_Type)
        Test_Type.trace("w",validate) #trace changes on StringVar
        cb.place(x=150, y=145, height=25, width=150)

        #e = tk.Entry(self)
        # e.place(x=self.winfo_screenmmheight()/2+250,y=145,height=25,width=150)

        # button = ttk.Button(self, text="Visit Page 1",
        #                    command=lambda: controller.show_frame(PageOne))
        # button.pack()

        # button2 = ttk.Button(self, text="Visit Page 2",
        #                    command=lambda: controller.show_frame(PageTwo))
        # button2.pack()

        # style = ttk.Style()
        #style = ThemedStyle(self)
        # style.set_theme("plastik")
        # style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '10',
        # foreground='blue',width=20)

        button = tk.Button(self, text="Start Monitoring", bg='#3399FF', fg='black', font=('calibri', 20, 'bold'),
                           borderwidth='10', width=20, command=lambda: controller.show_frame(PageThree))
        button.config(state='disabled')
        button.place(x=self.winfo_screenmmheight(),
                     y=self.winfo_screenmmwidth()-40)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#101010')
        v = StringVar(self)
        label = tk.Label(self, textvariable=v, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=30)
        v.set(new_date)
        global Test_Name
        label = tk.Label(self, textvariable=Test_Name, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=10)
        global Patient_Name
        label = tk.Label(self, textvariable=Patient_Name, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=100, y=10)
        ico = Image.open(str(cwd) + '\\HomeIcon.png')
        self.photo = ImageTk.PhotoImage(ico)
        
        button1 = tk.Button(self, image = self.photo, compound=tk.TOP,bg='#3399FF',
                           borderwidth='10', width=100, height=30,command=lambda: controller.show_frame(StartPage))

        button1.place(x=(self.winfo_screenwidth()/2)-120,y=0)
        # button1.pack()
        button = tk.Button(self, text="Plot 1",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: controller.show_frame(PageThree))
        button.pack()

        button2 = tk.Button(self, text="Plot 3",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button3 = tk.Button(self, text="Save Figure",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: f1.savefig(str(cwd) + '\\{}_{}_{}_RelativeANDAbsolute.png'.format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),Patient_Name.get(),Test_Name.get())))
        button3.place(x=(self.winfo_screenwidth()/2)-120,y=50)
        # button3.place(x=50, y=60)
        # button3.pack()



        canvas = FigureCanvasTkAgg(f1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#101010')
        v = StringVar(self)
        label = tk.Label(self, textvariable=v, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=30)
        v.set(new_date)
        global Test_Name
        label = tk.Label(self, textvariable=Test_Name, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=10)
        global Patient_Name
        label = tk.Label(self, textvariable=Patient_Name, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=100, y=10)
        ico = Image.open(str(cwd) +'\\HomeIcon.png')
        self.photo = ImageTk.PhotoImage(ico)
        
        button1 = tk.Button(self, image = self.photo, compound=tk.TOP,bg='#3399FF',
                           borderwidth='10', width=100, height=30,command=lambda: controller.show_frame(StartPage))

        button1.place(x=(self.winfo_screenwidth()/2)-120,y=0)
        # button1.pack()
        button = tk.Button(self, text="Plot 1",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: controller.show_frame(PageThree))
        button.pack()

        button2 = tk.Button(self, text="Plot 2",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: controller.show_frame(PageOne))
        button2.pack()
        button3 = tk.Button(self, text="Save Figure",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: f2.savefig(str(cwd) +'\\{}_{}_{}_Channels.png'.format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),Patient_Name.get(),Test_Name.get())))
        button3.place(x=(self.winfo_screenwidth()/2)-120,y=50)
        # button3.place(x=50, y=60)
        # button3.pack()

        canvas = FigureCanvasTkAgg(f2, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#101010')
        v = StringVar(self)
        label = tk.Label(self, textvariable=v, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=30)
        v.set(new_date)
        global Test_Name
        label = tk.Label(self, textvariable=Test_Name, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=20, y=10)
        global Patient_Name
        label = tk.Label(self, textvariable=Patient_Name, font=('calibri', 14), fg="white", bg="#101010")
        label.place(x=100, y=10)
        

        ico = Image.open(str(cwd) +'\\HomeIcon.png')
        self.photo = ImageTk.PhotoImage(ico)
        
        button1 = tk.Button(self, image = self.photo, compound=tk.TOP,bg='#3399FF',
                           borderwidth='10', width=100, height=30,command=lambda: controller.show_frame(StartPage))

        button1.place(x=(self.winfo_screenwidth()/2)-120,y=0)
        # button1.pack()
        button = tk.Button(self, text="Plot 2",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = tk.Button(self, text="Plot 3",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text="Save Figure",bg='#3399FF', fg='black', font=('calibri', 12, 'bold'),
                           borderwidth='10', width=12,command=lambda: a.figure.savefig(str(cwd) +'\\{}_{}_{}_Potential.png'.format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),Patient_Name.get(),Test_Name.get())))
        button3.place(x=(self.winfo_screenwidth()/2)-120,y=50)
        # button3.place(x=50, y=60)
        # button3.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = SeaofBTCapp()
width_2 = app.winfo_screenwidth()/2
height = app.winfo_screenheight()
app.wm_geometry(str(int(width_2)) + 'x' + str(int(height)) + '+0+0')
ani = animation.FuncAnimation(f, animate, interval=10000, blit=True)
ani1 = animation.FuncAnimation(f1, animate2, interval=10000, blit=True)
ani3 = animation.FuncAnimation(f1, animate4, interval=10000, blit=True)
ani2 = animation.FuncAnimation(f2, animate3, interval=10000)
ico = Image.open(str(cwd) +'\\icon.png')
photo = ImageTk.PhotoImage(ico)
app.wm_iconphoto(False, photo)
app.mainloop()
