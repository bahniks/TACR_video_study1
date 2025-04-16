#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from intros import Initial, Intro, Ending
from demo import Demographics
from comments import Comments
from login import Login
from videointros import VideoIntro1, VideoIntro2, VideoIntro3, VideoIntro4, VideoIntro5, Selection, VideoIntro6
from videos import Videos, JOL, IMI, Quiz1, Quiz2, IMI2, Quiz3
from quest import QuestInstructions, Hexaco




frames = [Initial,
          Intro,
          Login,    
          VideoIntro1,
          VideoIntro2,
          VideoIntro3,
          Videos, JOL, IMI, Quiz1,
          VideoIntro4,
          Videos, JOL, IMI, Quiz2,
          VideoIntro5,
          Selection,
          VideoIntro6,
          Videos, Videos, Videos, Videos, Videos,
          IMI2,
          Quiz3,
          QuestInstructions,
          Hexaco,
          Demographics,
          Comments,
          Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))