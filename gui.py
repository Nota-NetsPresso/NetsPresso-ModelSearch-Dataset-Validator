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

def yaml_switch():
    if data_format.get() == "yolo":
        yaml_button["state"] = "normal"
    else:
        yaml_button["state"] = "disabled"
        yaml_path.set(None)



open_dir = StringVar()

frame_data_path = Frame(win, relief='sunken', bd=2)
frame_data_path.grid(column=0, row=0)
frame_data_path.pack()
ttk.Label(frame_data_path, text="Step 1. Set data directory").pack()
data_button = ttk.Button(frame_data_path, text="Open", command=select_dir)
data_button.pack()
open_dir_label = ttk.Label(frame_data_path, textvariable=open_dir)
open_dir_label.pack()

frame_data_format = Frame(win, relief='sunken', bd=2)
frame_data_format.pack()
ttk.Label(frame_data_format, text="Step 2. Set data format").pack()
data_format = StringVar(None, "yolo")
dataset_r1 = ttk.Radiobutton(frame_data_format, text="yolo", variable=data_format, value="yolo", command=yaml_switch)
dataset_r1.pack()
dataset_r2 = ttk.Radiobutton(frame_data_format, text="coco", variable=data_format, value="coco", command=yaml_switch)
dataset_r2.pack()
dataset_r3 = ttk.Radiobutton(frame_data_format, text="voc", variable=data_format, value="voc", command=yaml_switch)
dataset_r3.pack()

yaml_path = StringVar()
yaml_button = ttk.Button(frame_data_format, text="yaml path", command=select_yaml)
yaml_button.pack()
yaml_label = ttk.Label(frame_data_format, textvariable=yaml_path)
yaml_label.pack()

data_type = StringVar(None, "train")

frame_data_type = Frame(win, relief='sunken', bd=2)
frame_data_type.pack()
ttk.Label(frame_data_type, text="Step 3. Set data type").pack()
data_type_r1 = ttk.Radiobutton(frame_data_type, text="train", variable=data_type, value="train")
data_type_r1.pack()
data_type_r2 = ttk.Radiobutton(frame_data_type, text="test", variable=data_type, value="test")
data_type_r2.pack()
data_type_r3 = ttk.Radiobutton(frame_data_type, text="val", variable=data_type, value="val")
data_type_r3.pack()


frame_task = Frame(win, relief='sunken', bd=2)
frame_task.pack()

task = StringVar(None, "object_detection")
ttk.Label(frame_task, text="Step 4. Set task type").pack()
task_r1 = ttk.Radiobutton(frame_task, text="object detection", variable=task, value="object_detection")
task_r1.pack()
task_r2 = ttk.Radiobutton(frame_task, text="classification", variable=task, value="classification", state="disabled")
task_r2.pack()

run_button = ttk.Button(win, text="run", command=run)
run_button.pack()


win.mainloop()
