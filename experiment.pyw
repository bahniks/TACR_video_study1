#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from intros import Initial, Intro, Ending
from demo import Demographics
from comments import Comments
from login import Login
from videointros import VideoIntro1, VideoIntro2, VideoIntro3
from videos import Videos, JOL, IMI, Quiz1, Quiz2




frames = [Initial,
          Intro,
          Login,    
          VideoIntro1,
          VideoIntro2,
          VideoIntro3,
          Videos, JOL, IMI, Quiz1,
          Videos, JOL, IMI, Quiz2,
          Demographics,
          Comments,
          Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))