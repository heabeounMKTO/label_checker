from tkinter import *
from PIL import Image, ImageTk
import cv2
from fileutils import FilesLoader
from tkinter import filedialog
from pathlib import Path
import numpy as np
from fileutils import LabelsLoader , FilesFinder
import os 
from pprint import pprint
import shutil

def draw_lab(imarr, pts, lab):
    for idx ,label in enumerate(lab):
        for ptsarr in pts:
            imarr = cv2.rectangle(imarr,  (int(ptsarr[0][0]),int(ptsarr[0][1])),(int(ptsarr[1][0]),int(ptsarr[1][1])), (255,12,0), 2)
        _pts = pts[idx]
        imarr = cv2.rectangle(imarr, (int(_pts[0][0]), int(_pts[0][1])), (int(_pts[0][0]+60), int(_pts[0][1]-50)), (255,12,0), -1)
        imarr = cv2.putText(imarr, label, (int(_pts[0][0]), int(_pts[0][1]-10)), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    return imarr        

def load_img(imgpath):
    global labels
    global all_img_paths
    global filename
    all_img_paths = FilesLoader(Path(filename)).file_array
    yea.set(current_imageidx)
    jsonfile = os.path.splitext(all_img_paths[current_imageidx])[0] + ".json" 
    labels.set("labels: " + str(LabelsLoader(jsonfile).get_labels()))
    pts, lab = LabelsLoader(jsonfile).get_coords()
    img = cv2.cvtColor(cv2.imread(imgpath), cv2.COLOR_BGR2RGB)
    img = draw_lab(img, pts, lab)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
    return imgtk

def next_img():
    global current_imageidx 
    global photo
    if current_imageidx < 0:
        current_imageidx = 0
    current_imageidx += 1
    jsonfile = os.path.splitext(all_img_paths[current_imageidx])[0] + ".json" 
    labels.set(str(LabelsLoader(jsonfile).get_labels()))
    photo = load_img(all_img_paths[current_imageidx]) 
    img_label.config(image=photo)

def prev_img():
    global current_imageidx 
    global photo
    if current_imageidx < 0:
        current_imageidx = 0
    current_imageidx -= 1
    jsonfile = os.path.splitext(all_img_paths[current_imageidx])[0] + ".json" 
    labels.set(str(LabelsLoader(jsonfile).get_labels()))
    photo = load_img(all_img_paths[current_imageidx]) 
    img_label.config(image=photo)

def a_ok():
    global all_img_paths
    global filename
    all_img_paths = FilesLoader(Path(filename)).file_array
    checked_dir = os.path.join(filename, "checked")
    if not os.path.exists(checked_dir):
        os.makedirs(checked_dir)
        
    imgstem = os.path.basename(all_img_paths[current_imageidx])
    jsonstem = os.path.basename(os.path.splitext(all_img_paths[current_imageidx])[0] + ".json")
    
    print(imgstem, jsonstem)
    
    old_pathimg = os.path.join(filename, imgstem)
    old_pathjson = os.path.join(filename, jsonstem)
    
    new_pathimg = os.path.join(checked_dir, imgstem)
    new_pathjson = os.path.join(checked_dir, jsonstem)
    shutil.move(old_pathimg, new_pathimg)
    shutil.move(old_pathjson, new_pathjson)
    next_img()
    prev_img() 
def hkey_ok(e):
    a_ok() 

def hkey_next(e):
    next_img()
    
def hkey_prev(e):
    prev_img() 

     
current_imageidx = 0
window = Tk()
window.resizable()
window.title("MONKEFY")
window.geometry("1280x720")

labels = StringVar()
filename = filedialog.askdirectory()
all_img_paths = FilesLoader(Path(filename)).file_array
yea = StringVar()

window.bind('<space>', hkey_ok)
window.bind('d', hkey_next)
window.bind('a', hkey_prev)

Button(window, text="NEXT IMAGE",relief = 'groove', command=next_img,height= 20, width=30).pack(side=RIGHT, padx=10, pady=10)
Button(window, text="PREV IMAGE", relief = 'groove',command=prev_img,height= 20, width=30).pack(side=LEFT, padx=10, pady=10)
Button(window, text = "A-OK" , bg='#00ff00', font=('Arial', 8), command=a_ok,height= 8, width=30).pack(side=BOTTOM, padx=10, pady=10) 
# photo = ImageTk.PhotoImage(Image.open("load.png"))
photo = load_img(all_img_paths[current_imageidx])
label_preview = Label(window, font=("Arial", 20) ,textvariable=labels).pack(side=BOTTOM)

img_label = Label(window, image=photo)
img_label.pack(side=TOP)
Label(window, anchor=CENTER,textvariable=yea).pack(side=BOTTOM)

window.mainloop()