#Import the Tkinter library
from run import execute 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


#Create an instance of Tkinter frame
win= Tk()
#Define the geometry



def select_train_dir():    
    input_dir = filedialog.askdirectory()
    train_dir.set(input_dir)

def select_test_dir():    
    input_dir = filedialog.askdirectory()
    test_dir.set(input_dir)

def select_valid_dir():    
    input_dir = filedialog.askdirectory()
    valid_dir.set(input_dir)

def select_output_dir():
    input_dir = filedialog.askdirectory()
    output_dir.set(input_dir)

def select_yaml():
    input_path = filedialog.askopenfilename()
    yaml_path.set(input_path)

def run():
    # execute(format, task, train_dir, test_dir, valid_dir, output_dir, yaml_path)
    if test_dir.get() == '':
        test_dir_get = None
    else:
        test_dir_get = test_dir.get()
    if valid_dir.get() == '':
        valid_dir_get = None
    else:
        valid_dir_get = valid_dir.get()
    if output_dir.get() == '':
        output_dir_get = None
    else:
        output_dir_get = output_dir.get()
    if yaml_path.get() == '':
        yaml_path_get = None
    else:
        yaml_path_get = yaml_path.get()
    
    execute(data_format.get(), task.get(), train_dir.get(), test_dir_get, valid_dir_get, output_dir_get, yaml_path_get)

def yaml_switch():
    if data_format.get() == "yolo":
        yaml_button["state"] = "normal"
    else:
        yaml_button["state"] = "disabled"
        yaml_path.set(None)



train_dir = StringVar()
test_dir = StringVar()
valid_dir = StringVar()
output_dir = StringVar()

frame_data_path = Frame(win, relief='sunken', bd=2)
frame_data_path.grid(column=0, row=0)
frame_data_path.pack()
ttk.Label(frame_data_path, text="Step 1. Set data directory").pack()
train_data_button = ttk.Button(frame_data_path, text="Open", command=select_train_dir)
train_data_button.pack()
train_dir_label = ttk.Label(frame_data_path, textvariable=train_dir)
train_dir_label.pack()

test_data_button = ttk.Button(frame_data_path, text="Open", command=select_test_dir)
test_data_button.pack()
test_dir_label = ttk.Label(frame_data_path, textvariable=test_dir)
test_dir_label.pack()

valid_data_button = ttk.Button(frame_data_path, text="Open", command=select_valid_dir)
valid_data_button.pack()
valid_dir_label = ttk.Label(frame_data_path, textvariable=valid_dir)
valid_dir_label.pack()

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

frame_task = Frame(win, relief='sunken', bd=2)
frame_task.pack()

task = StringVar(None, "object_detection")
ttk.Label(frame_task, text="Step 4. Set task type").pack()
task_r1 = ttk.Radiobutton(frame_task, text="object detection", variable=task, value="object_detection")
task_r1.pack()
task_r2 = ttk.Radiobutton(frame_task, text="classification", variable=task, value="classification", state="disabled")
task_r2.pack()

frame_output_path = Frame(win, relief='sunken', bd=2)

frame_output_path.pack()
ttk.Label(frame_output_path, text="Step 5. Set output directory").pack()
output_path_button = ttk.Button(frame_output_path, text="Open", command=select_output_dir)
output_path_button.pack()
output_dir_label = ttk.Label(frame_output_path, textvariable=output_dir)
output_dir_label.pack()



run_button = ttk.Button(win, text="run", command=run)
run_button.pack()


win.mainloop()
