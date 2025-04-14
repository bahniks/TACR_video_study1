#! python3

from tkinter import *
from tkinter import ttk

import os
import vlc

from common import ExperimentFrame, Measure, InstructionsFrame
from gui import GUI


class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path

        # Create tkinter canvas for video
        self.canvas = Canvas(root, width=640, height=480)
        self.canvas.pack()

        # Initialize VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Set the video output to the tkinter canvas
        self.player.set_hwnd(self.canvas.winfo_id())

        # Load the video file
        media = self.instance.media_new(self.video_path)
        self.player.set_media(media)

        # Play the video
        self.player.play()

    def stop(self):
        self.player.stop()
        self.root.destroy()



class Videos(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root

        self.pathtext = ttk.Label(self, text = self.getVideo(), font = 15)
        self.pathtext.grid(row = 0, column = 1)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 1, column = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def getVideo(self):
        trial = self.root.status["videoNumber"]
        version = self.root.status["versions"][trial]
        video_path = os.path.join(os.getcwd(), "Videos/video_{}_{}.mp4".format(trial, version))
        return video_path


class JOL(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "", proceed = True)

        self.root = root

        q = "Kolik informací z videa si myslíte, že si budete schopni vybavit přibližně za 5 minut?"
        options = ["0 % (nic z toho)", "20 %", "40 %", "60 %", "80 %", "100 % (vše)"]

        self.measure = Measure(self, text = q, values = options, left = "", right = "", questionPosition = "above", filler = 700)
        self.measure.grid(row = 1, column = 1)

    # ukladani dat



if __name__ == "__main__":
    # from login import Login
    # os.chdir(os.path.dirname(os.getcwd()))
    # GUI([JOL, Login,
    #      Videos])    

    root = Tk()
    video_path = os.path.join(os.getcwd(), "Videos/video_2_1.mp4")
    app = VideoPlayer(root, video_path)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()