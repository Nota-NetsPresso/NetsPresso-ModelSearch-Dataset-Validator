#Import the Tkinter library
from run import main
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


#Create an instance of Tkinter frame
win= Tk()
#Define the geometry



def select_dir():    
    input_dir = filedialog.askdirectory()
    open_dir.set(input_dir)

def select_yaml():
    input_path = filedialog.askopenfilename()
    yaml_path.set(input_path)

def run():
    main(open_dir.get(), data_format.get(), task.get(), data_type.get(), yaml_path.get())


open_dir = StringVar()
data_button = ttk.Button(win, text="data set path", command=select_dir)
data_button.pack()

yaml_path = StringVar()
yaml_button = ttk.Button(win, text="yaml path", command=select_yaml)
yaml_button.pack()

data_type = StringVar(None, "train")
data_type_r1 = ttk.Radiobutton(win, text="train", variable=data_type, value="train")
data_type_r1.pack()
data_type_r2 = ttk.Radiobutton(win, text="test", variable=data_type, value="test")
data_type_r2.pack()
data_type_r3 = ttk.Radiobutton(win, text="val", variable=data_type, value="val")
data_type_r3.pack()

data_format = StringVar(None, "yolo")
dataset_r1 = ttk.Radiobutton(win, text="yolo", variable=data_format, value="yolo")
dataset_r1.pack()
dataset_r2 = ttk.Radiobutton(win, text="coco", variable=data_format, value="coco")
dataset_r2.pack()
dataset_r3 = ttk.Radiobutton(win, text="voc", variable=data_format, value="voc")
dataset_r3.pack()

task = StringVar(None, "object_detection")
task_r1 = ttk.Radiobutton(win, text="object detection", variable=task, value="object_detection")
task_r1.pack()

open_dir_label = ttk.Label(win, textvariable=open_dir)
open_dir_label.pack()
yaml_label = ttk.Label(win, textvariable=yaml_path)
yaml_label.pack()
data_type_label = ttk.Label(win, textvariable=data_type)
data_type_label.pack()
data_format_label = ttk.Label(win, textvariable=data_format)
data_format_label.pack()
task_label = ttk.Label(win, textvariable=task)
task_label.pack()


run_button = ttk.Button(win, text="run", command=run)
run_button.pack()


win.mainloop()
