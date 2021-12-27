from __future__ import print_function

import os
import roslibpy
import roslibpy.actionlib

import openhouse_goallist
from openhouse_speechlist import *
from gtts import gTTS

rosclient = roslibpy.Ros(host='192.168.1.11', port=9091)
rosclient.run()

if rosclient.is_connected:
    print("Base connected successfully")

action_client = roslibpy.actionlib.ActionClient(rosclient, '/move_base', 'move_base_msgs/MoveBaseAction')


def run_goal(self, direction):
    if direction == 'f':
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
        mytext = speechList.list[i]
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("texttospeech.mp3")
        os.system("mpg123 texttospeech.mp3")

    if direction == 'b':
        i = len(openhouse_goallist.list)
        while i >= 1:
            goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(goalList.list[i]))
            goal.on('feedback', lambda f: print(f['base_position']['pose']))
            goal.on('status', lambda f: print(f['text']))
            goal.send()
            result = goal.wait(60 * 5)
            print(result)
            i -= 1
        action_client.dispose()
        mytext = speechList.list[i]
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("texttospeech.mp3")
        os.system("mpg123 texttospeech.mp3")
