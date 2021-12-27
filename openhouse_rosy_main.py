# from __future__ import print_function
import tkinter as tk
from PIL import Image, ImageTk

import os
import roslibpy
import roslibpy.actionlib

import openhouse_goallist
from openhouse_speechlist import *
from gtts import gTTS


class RobotGui:
    def __init__(self):
        self.dir = 'f'
        self.window = tk.Tk()
        self.window.geometry('1920x1080')
        # self.window.attributes("-fullscreen", True)
        self.window.wm_attributes("-topmost", False)  # keep below the chatbot
        # self.window.bind("<Escape>", lambda event:self.window.destroy())
        self.window.bind("<Escape>", lambda event: self.displayface_off())

        # open house button
        self.photo = ImageTk.PhotoImage(file="images/ngeeann_landscape.PNG")
        self.usherbutton = tk.Button(self.window, text="", command=self.openhouse_move, image=self.photo, width=1920,
                                     height=1080, compound="c", font='TkDefaultFont 40 bold', bg='white',
                                     fg='red', borderwidth=0)
        self.usherbutton.grid(row=0, column=0, sticky="se", padx=(0, 50), pady=(0, 100))

    def openhouse_move(self):
        print(self.dir)
        # self.run_goal(self.dir)
        if self.dir == 'f':
            self.dir = 'b'
        else:
            self.dir = 'f'

    def run_goal(self, direction):
        # speech needed only when moving forward
        if direction == 'f':
            mytext = speechList.list[0]
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("texttospeech.mp3")
            os.system("mpg123 texttospeech.mp3")
            i = 1
            while i < len(openhouse_goallist.list):
                goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(openhouse_goallist.list[i]))
                goal.on('feedback', lambda f: print(f['base_position']['pose']))
                goal.on('status', lambda f: print(f['text']))
                goal.send()
                result = goal.wait(60 * 5)
                print(result)
                i += 1
            action_client.dispose()
            mytext = speechList.list[1]
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("texttospeech.mp3")
            os.system("mpg123 texttospeech.mp3")

        if direction == 'b':
            i = len(openhouse_goallist.list) - 1 - 1
            while i >= 0:
                goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(openhouse_goallist.list[i]))
                goal.on('feedback', lambda f: print(f['base_position']['pose']))
                goal.on('status', lambda f: print(f['text']))
                goal.send()
                result = goal.wait(60 * 5)
                print(result)
                i -= 1
            action_client.dispose()
            mytext = speechList.list[2]
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("texttospeech.mp3")
            os.system("mpg123 texttospeech.mp3")


if __name__ == "__main__":
    rosclient = roslibpy.Ros(host='192.168.1.11', port=9091)
    rosclient.run()
    if rosclient.is_connected:
        print("Base connected successfully")
    action_client = roslibpy.actionlib.ActionClient(rosclient, '/move_base', 'move_base_msgs/MoveBaseAction')

    # run GUI
    app = RobotGui()
    app.window.mainloop()
    exit()
