import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()                
root.set_theme("radiance")         
root['background'] = '#82E7DC'

status = ttk.Label(root, text="Welcome to Music Player", relief=SUNKEN, anchor=W, font='Times 10 italic')
status.pack(side=BOTTOM, fill=X)

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu, tearoff=0)

playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Music Player', 'This music player build by using Python Tkinter by Divyang Yadav')


subMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  

root.title("Music Player")
root.iconbitmap(r'images/icon.ico')


lframe = Frame(root)
lframe.pack(side=LEFT, padx=30, pady=30)

playbox = Listbox(lframe)
playbox.pack()


addPhoto = PhotoImage(file='images/add.png')
Button(lframe, image=addPhoto, command=browse_file).pack(side=LEFT)


def del_song():
    selectsong = playbox.curselection()
    selectsong = int(selectsong[0])
    playbox.delete(selectsong)
    playlist.pop(selectsong)
    mixer.music.stop()
    status['text'] = "Music Stopped"


delPhoto = PhotoImage(file='images/del.png')
Button(lframe, image=delPhoto, command=del_song).pack(side=RIGHT)

rframe = Frame(root)
rframe.pack(pady=30)

tframe = Frame(rframe)
tframe.pack()

lenlabel = ttk.Label(tframe, text='Total Duration - 00 : 00')
lenlabel.pack(pady=5)

ctlabel = ttk.Label(tframe, text='Current Duration - 00 : 00')
ctlabel.pack()


def details_show(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lenlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=count_start, args=(total_length,))
    t1.start()

def count_start(t):
    global paused
    
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            ctlabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def music_play():
    global paused

    if paused:
        mixer.music.unpause()
        status['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            music_stop()
            time.sleep(1)
            selectsong = playbox.curselection()
            selectsong = int(selectsong[0])
            play_it = playlist[selectsong]
            mixer.music.load(play_it)
            mixer.music.play()
            status['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            details_show(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Music Player could not find the file. Please check again!!!!')


def music_stop():
    mixer.music.stop()
    status['text'] = "Music Stopped"


paused = FALSE


def music_pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    status['text'] = "Music Paused"


def music_rewind():
    music_play()
    status['text'] = "Music Rewinded"


def vol_set(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = FALSE


def music_mute():
    global muted
    if muted:  
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


mframe = Frame(rframe)
mframe.pack(pady=30, padx=30)

plyPhoto = PhotoImage(file='images/play.png')
plyBtn = ttk.Button(mframe, image=plyPhoto, command=music_play)
plyBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(mframe, image=stopPhoto, command=music_stop)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(mframe, image=pausePhoto, command=music_pause)
pauseBtn.grid(row=0, column=2, padx=10)


bframe = Frame(rframe)
bframe.pack()

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bframe, image=rewindPhoto, command=music_rewind)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bframe, image=volumePhoto, command=music_mute)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bframe, from_=0, to=100, orient=HORIZONTAL, command=vol_set)
scale.set(70)  
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=30, padx=30)


def on_closing():
    music_stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()