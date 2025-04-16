#! python3

from tkinter import *
from tkinter import ttk

import os
import vlc

from common import ExperimentFrame, Measure, InstructionsFrame, InstructionsAndUnderstanding
from questionnaire import Questionnaire
from gui import GUI
from login import Login






imiInstructions = """Nyní Vás prosíme o hodnocení zhlédnutého videa. 
U každého z následujících tvrzení uveďte, nakolik je pro vás pravdivé."""

imiScale = ["vůbec nepravdivé", "spíše nepravdivé", "do jisté míry pravdivé", "spíše pravdivé", "zcela pravdivé"]

imiItems = ["Velmi jsem si užil(a) sledování tohoto videa",
"Sledování tohoto videa bylo zábavné.",
"Myslel(a) jsem, že toto video bylo nudné.",
"Toto video mě vůbec nezaujalo.",
"Popsal(a) bych toto video jako velmi zajímavé.",
"Myslel(a) jsem, že toto video bylo docela příjemné.",
"Během sledování tohoto videa jsem si uvědomoval(a), jak moc mě bavilo.",
"Věřím, že toto video pro mě může mít nějakou hodnotu.",
"Myslím si, že sledování tohoto videa je užitečné pro mé znalosti.",
"Myslím si, že sledování tohoto videa je důležité, protože může rozšířit mé znalosti.",
"Byl(a) bych ochotný/á toto video znovu sledovat, protože pro mě má hodnotu.",
"Myslím, že sledování tohoto videa mi může pomoci zlepšit mé znalosti.",
"Věřím, že sledování tohoto videa může být pro mě přínosné.",
"Myslím, že toto video je důležité.",
"Věnoval(a) jsem hodně úsilí sledování tohoto videa.",
"Nesnažil(a) jsem se příliš sledovat toto video pozorně.",
"Snažil(a) jsem se velmi usilovně dávat pozor při sledování videa.",
"Bylo pro mě důležité být soustředěný(á) a dávat pozor při sledování videa.",
"Nevynaložil(a) jsem příliš energie na sledování tohoto videa."]







class Videos(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.video_path = self.getVideo()

        # Create tkinter canvas for video
        self.canvas = Canvas(self, width=1200, height=674, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.canvas.grid(column = 1, row = 1, sticky=(N, S, E, W))

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1) 
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)

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

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.stop)
        self.next.grid(row = 2, column = 1)

    def stop(self):
        self.player.stop()
        self.root.status["videoNumber"] += 1
        self.nextFun()

    def getVideo(self):
        trial = self.root.status["videoNumber"]
        version = self.root.status["versions"][trial - 1]
        file = [f for f in os.listdir(os.path.join(os.getcwd(), "Stuff", "Videos")) if f.startswith(f"{trial}{version}")]             
        return os.path.join(os.getcwd(), "Stuff", "Videos", file[0])


# class Videos(ExperimentFrame):
#     def __init__(self, root):
#         super().__init__(root)

#         self.root = root

#         self.pathtext = ttk.Label(self, text = self.getVideo(), font = 15)
#         self.pathtext.grid(row = 0, column = 1)

#         ttk.Style().configure("TButton", font = "helvetica 15")
#         self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
#         self.next.grid(row = 1, column = 1)

#         self.rowconfigure(0, weight = 1)
#         self.rowconfigure(1, weight = 1)
#         self.columnconfigure(0, weight = 1)
#         self.columnconfigure(2, weight = 1)

#     def getVideo(self):
#         trial = self.root.status["videoNumber"]
#         version = self.root.status["versions"][trial]
#         video_path = os.path.join(os.getcwd(), "Videos/video_{}_{}.mp4".format(trial, version))
#         return video_path


class JOL(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "", proceed = True)

        self.root = root

        q = "Kolik informací z videa si myslíte, že si budete schopni vybavit přibližně za 5 minut?"
        options = ["0 % (nic z toho)", "20 %", "40 %", "60 %", "80 %", "100 % (vše)"]

        self.measure = Measure(self, text = q, values = options, left = "", right = "", questionPosition = "above", filler = 700, function=self.enable)
        self.measure.grid(row = 1, column = 1)

        self.next["state"] = "disabled"

    def enable(self):
        self.next["state"] = "normal"

    # ukladani dat


IMI = (Questionnaire,
                {"words": "imi.txt",
                 "question": imiInstructions,
                 "labels": imiScale,
                 "values": 5,
                 "labelwidth": 11,
                 "text": False,
                 "fontsize": 13,
                 "blocksize": 5,
                 "wraplength": 700,
                 "filetext": "IMI",
                 "fixedlines": 0,
                 "pady": 3})


def getQuestions(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding = "utf-8") as f:
        questions = []        
        q = ["", [], ""]
        count = 0
        for line in f:      
            if count == 0:
                q[0] = line.strip()                
            elif count == 5:                    
                questions.append(q)
                q = ["", [], ""]
                count = -1
            else:
                q[1].append(line.strip())               
            count += 1
    return questions

quizInstructions = """
Nyní odpovězte na následující otázky týkající se obsahu právě zhlédnutého videa na Prokletí znalosti. U každé otázky jsou uvedeny čtyři odpovědi, vždy jen jedna z nich je správná. (výsledek tohoto kvízu nemá vliv na výši odměny).
"""

Quiz1 = (InstructionsAndUnderstanding, {"text": quizInstructions, "height": 5, "width": 80, "name": "Quiz1", "randomize": True, "showFeedback": False, "controlTexts": getQuestions("quiz1.txt"), "fillerheight": 300, "finalButton": "Pokračovat"})
Quiz2 = (InstructionsAndUnderstanding, {"text": quizInstructions, "height": 5, "width": 80, "name": "Quiz2", "randomize": True, "showFeedback": False, "controlTexts": getQuestions("quiz2.txt"), "fillerheight": 300, "finalButton": "Pokračovat"})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login,
         Videos, JOL, IMI, Quiz1])    


    # video_path = os.path.join(os.getcwd(), "Videos/video_2_1.mp4")
    # app = Videos(root, video_path)
    # root.protocol("WM_DELETE_WINDOW", app.stop)
    # root.mainloop()