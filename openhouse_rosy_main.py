# from __future__ import print_function
import tkinter as tk
from PIL import Image, ImageTk
import threading

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
        self.window.geometry('1080x1920')
        # self.window.attributes("-fullscreen", True)
        self.window.wm_attributes("-topmost", False)  # keep below the chatbot
        # self.window.bind("<Escape>", lambda event:self.window.destroy())
        self.window.bind("<Escape>", lambda event: self.displayface_off())

        # open house button
        self.photo = ImageTk.PhotoImage(file="images/ngeeann_portrait_2.png")
        self.usherbutton = tk.Button(self.window, text="", command=self.openhouse_move, image=self.photo, width=1080,
                                     height=1920, compound="c", font='TkDefaultFont 40 bold', bg='white',
                                     fg='red', borderwidth=0)
        self.usherbutton.grid(row=0, column=0, sticky="se", padx=(0, 50), pady=(0, 100))


    def openhouse_move(self):
        self.run_goal(self.dir)

    def run_goal(self, direction):
        # speech needed only when moving forward
        print("The direction is now: " + self.dir)
        if direction == 'f':
            os.system("mpg123 texttospeech_0.mp3")
            i = 1
            while i < len(openhouse_goallist.goalList.list):
                print(i)
                goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(openhouse_goallist.goalList.list[i]))
                goal.on('feedback', lambda f: print(f['base_position']['pose']))
                goal.on('status', lambda f: print(f['text']))
                goal.send()
                result = goal.wait(60 * 5)
                print(result)
                i += 1
            print(i)
            self.dir = 'b'

        if direction == 'b':
            self.dir = 'f'
            os.system("taskkill /im mpg123.exe /t /f")
            i = len(openhouse_goallist.goalList.list) - 1 - 1
            while i >= 0:
                print(i)
                goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(openhouse_goallist.goalList.list[i]))
                goal.on('feedback', lambda f: print(f['base_position']['pose']))
                goal.on('status', lambda f: print(f['text']))
                goal.send()
                result = goal.wait(60 * 5)
                print(result)
                i -= 1
            print(i)
            os.system("mpg123 texttospeech_2.mp3")


    def speech_repeat_thread(self):
        print("The repeat message is processed")
        while True:
            if self.dir == 'b':
                print("Playing repeat message.")
                os.system("mpg123 texttospeech_1.mp3")


if __name__ == "__main__":
    rosclient = roslibpy.Ros(host='192.168.31.200', port=9090)
    rosclient.run()
    if rosclient.is_connected:
        print("Base connected successfully")
    action_client = roslibpy.actionlib.ActionClient(rosclient, '/move_base', 'move_base_msgs/MoveBaseAction')

    # run GUI
    app = RobotGui()

    welcomemsg = threading.Thread(target=app.speech_repeat_thread)
    welcomemsg.daemon = True
    welcomemsg.start()

    app.window.mainloop()
    exit()
