from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep

import random
import os
import urllib.request
import urllib.parse

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice, InstructionsAndUnderstanding
from gui import GUI
from constants import TESTING, URL, TRUST
from questionnaire import Questionnaire
from login import Login


################################################################################
# TEXTS
instructionsT1 = """Vaše rozhodnutí v této úloze budou mít finanční důsledky pro Vás a pro dalšího přítomného účastníka v laboratoři. Pozorně si přečtěte pokyny, abyste porozuměl(a) studii a své roli v ní. 

V rámci této úlohy jste spárován(a) s dalším účastníkem studie. Oba obdržíte {} Kč.

Bude Vám náhodně přidělena jedna ze dvou rolí: budete buď hráčem A, nebo hráčem B.

<i>Hráč A:</i> Má možnost poslat hráči B od 0 do {} Kč (po {} Kč). Poslaná částka se ztrojnásobí a obdrží ji hráč B.
<i>Hráč B:</i> Může poslat zpět hráči A jakékoli množství peněz získaných v této úloze, tedy úvodních {} Kč a ztrojnásobenou částku poslanou hráčem A.

Předem nebudete vědět, jaká je Vaše role a uvedete tedy rozhodnutí pro obě role.

Tuto úlohu budete hrát v rámci studie celkem pětkrát. Vždy dostanete popis druhého hráče, s kterým hrajete (tj. informaci o tom, jaké skupiny jsou jim blízké). Pouze jeden popis bude nicméně odpovídat skutečnému účastníkovi studie. Zbývající čtyři popisy budou uměle vytvořené. Vaše odměna za úlohu bude záviset pouze na Vaší hře se skutečným účastníkem studie. Ostatní hry Vaší konečnou odměnu nijak neovlivní.

Na konci studie se dozvíte, jaká byla Vaše role a jaký je celkový výsledek rozhodnutí Vás a druhého účastníka. 
"""


instructionsT2 = """<b>Pro účastníka studie, s kterým jste spárován(a), jsou blízké tyto skupiny:
{}</b>

On(a) podobně bude vědět, jaké skupiny jsou blízké Vám.

<i>Hráč A:</i> Má možnost poslat hráči B od 0 do {} Kč (po {} Kč). Poslaná částka se ztrojnásobí a obdrží ji hráč B.
<i>Hráč B:</i> Může poslat zpět hráči A jakékoli množství peněz získaných v této úloze, tedy úvodních {} Kč a ztrojnásobenou částku poslanou hráčem A.

Předem nebudete vědět, jaká je Vaše role a uvedete tedy rozhodnutí pro obě role.

Svou volbu učiňte posunutím modrých ukazatelů níže.

Až se rozhodnete u všech možností, uveďte pomocí ukazatele, kolik očekáváte, že Vám pošle zpět hráč B, pokud bude náhodně vybráno, že jste hráč A."""



trustControl1 = "Jaká je role hráče A a hráče B ve studii?"
trustAnswers1 = ["Hráč A rozhoduje, kolik vezme hráči B peněz a hráč B se rozhoduje, kolik vezme hráči A peněz na oplátku.",
"Hráč A rozhoduje, kolik hráči B pošle peněz. Poslané peníze se ztrojnásobí a hráč B může poslat hráči A\njakékoli množství dostupných peněz zpět.", 
"Hráči A a B se rozhodují, kolik si navzájem pošlou peněz. Transfer peněz mezi nimi je dán rozdílem poslaných peněz.", 
"Hráč A se rozhoduje, kolik hráči B pošle peněz. Poslané peníze se ztrojnásobí. Hráč B může vzít hráči A\njakékoli množství zbylých peněz."]
trustFeedback1 = ["Chybná odpověď. Hráč A rozhoduje, kolik hráči B pošle peněz. Poslané peníze se ztrojnásobí a hráč B může poslat hráči B jakékoli množství dostupných peněz zpět.", 
"Správná odpověď.", "Chybná odpověď. Hráč A rozhoduje, kolik hráči B pošle peněz. Poslané peníze se ztrojnásobí a hráč B může poslat hráči B jakékoli množství dostupných peněz zpět.", 
"Chybná odpověď. Hráč A rozhoduje, kolik hráči B pošle peněz. Poslané peníze se ztrojnásobí a hráč B může poslat hráči B jakékoli množství dostupných peněz zpět."]


trustControl2 = "Jakou odměnu obdrží hráč A, pokud hráči B pošle 40 Kč a ten mu pošle zpět 60 Kč?"
trustAnswers2 = ["40 Kč (100 - 3 × 40 + 60)", "120 Kč (100 - 40 + 60)", "160 Kč (100 + 3 × (60 - 40))", "240 Kč (100 - 40 + 3 × 60)"]
trustFeedback2 = ["Chybná odpověď. Hráč A obdrží 100 Kč, z kterých 40 Kč pošle hráči B, zbyde mu tedy 60 Kč, ke kterým obdrží od hráče B 60 Kč, tj. na konec obdrží 120 Kč (100 - 40 + 60).", "Správná odpověď.", "Chybná odpověď. Hráč A obdrží 100 Kč, z kterých 40 Kč pošle hráči B, zbyde mu tedy 60 Kč, ke kterým obdrží od hráče B 60 Kč, tj. na konec obdrží 120 Kč (100 - 40 + 60).", "Chybná odpověď. Hráč A obdrží 100 Kč, z kterých 40 Kč pošle hráči B, zbyde mu tedy 60 Kč, ke kterým obdrží od hráče B 60 Kč, tj. na konec obdrží 120 Kč (100 - 40 + 60)."]


trustControl3 = "Jakou odměnu obdrží hráč B, pokud hráč A pošle 40 Kč a hráč B mu pošle zpět 60 Kč?"
trustAnswers3 = ["80 Kč (100 + 40 - 60)", "160 Kč (100 + 3 × 40 - 60)", "240 Kč (100 + 3 × 60 - 40)", "280 Kč (100 + 3 × 40 + 60)"]
trustFeedback3 = ["Chybná odpověď. Hráč B obdrží 100 Kč, ke kterým obdrží 120 Kč od hráče A (poslaných 40 Kč se ztrojnásobí) a následně pošle hráči A 60 Kč, tj. na konec obdrží 160 Kč (100 + 3 × 40 - 60).", "Správná odpověď.", "Chybná odpověď. Hráč B obdrží 100 Kč, ke kterým obdrží 120 Kč od hráče A (poslaných 40 Kč se ztrojnásobí) a následně pošle hráči A 60 Kč, tj. na konec obdrží 160 Kč (100 + 3 × 40 - 60).", "Chybná odpověď. Hráč B obdrží 100 Kč, ke kterým obdrží 120 Kč od hráče A (poslaných 40 Kč se ztrojnásobí) a následně pošle hráči A 60 Kč, tj. na konec obdrží 160 Kč (100 + 3 × 40 - 60)."]




trustResultTextA = """V úloze s dělením peněz Vám byla při hře hrané se skutečným účastníkem studie náhodně vybrána role hráče A.

<b>Rozhodl(a) jste se poslat {} Kč.</b>
Tato částka byla ztrojnásobena na {} Kč.
<b>Ze svých {} Kč Vám poslal hráč B {} Kč.</b>

<b>V této úloze jste tedy získal(a) {} Kč a hráč B {} Kč.</b>
"""

trustResultTextB = """V úloze s dělením peněz Vám byla při hře hrané se skutečným účastníkem studie náhodně vybrána role hráče B.

<b>Hráč A se rozhodl(a) poslat {} Kč.</b>
Tato částka byla ztrojnásobena na {} Kč.
<b>Ze svých {} Kč jste poslal(a) hráči B {} Kč.</b>

<b>V této úloze jste tedy získal(a) {} Kč a hráč A {} Kč.</b>
"""


checkButtonText = "Rozhodl(a) jsem se u všech možností"
checkButtonText2 = "Uvedl(a) jsem svou předpověď"


################################################################################


class ScaleFrame(Canvas):
    def __init__(self, root, font = 15, maximum = 0, player = "A", returned = 0, endowment = 100):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.parent = root
        self.root = root.root
        self.rounding = maximum / 5 if player == "A" else 10
        self.player = player
        self.returned = returned
        self.font = font
        self.endowment = endowment
        self.maximum = maximum

        self.valueVar = StringVar()
        self.valueVar.set("0")

        ttk.Style().configure("TScale", background = "white")

        self.value = ttk.Scale(self, orient = HORIZONTAL, from_ = 0, to = maximum, length = 400,
                            variable = self.valueVar, command = self.changedValue)
        self.value.bind("<Button-1>", self.onClick)

        self.playerText1 = "Já:" if player == "A" else "Hráč A:"
        self.playerText2 = "Hráč B:" if player == "A" else "Já:"
        self.totalText1 = "{0:3d} Kč" if player == "A" else "{0:3d} Kč"
        self.totalText2 = "{0:3d} Kč" if player == "A" else "{0:3d} Kč"

        self.valueLab = ttk.Label(self, textvariable = self.valueVar, font = "helvetica {}".format(font), background = "white", width = 3, anchor = "e")
        self.currencyLab = ttk.Label(self, text = "Kč", font = "helvetica {}".format(font), background = "white", width = 6)

        self.value.grid(column = 1, row = 1, padx = 10)
        self.valueLab.grid(column = 3, row = 1)        
        self.currencyLab.grid(column = 4, row = 1)

        fg = "white" if not self.player else "black"

        self.playerLab1 = ttk.Label(self, text = self.playerText1, font = "helvetica {}".format(font), background = "white", width = 6, anchor = "e", foreground = fg) 
        self.playerLab2 = ttk.Label(self, text = self.playerText2, font = "helvetica {}".format(font), background = "white", width = 6, anchor = "e", foreground = fg) 
        self.totalLab1 = ttk.Label(self, text = self.totalText1.format(0), font = "helvetica {}".format(font), background = "white", width = 6, anchor = "e", foreground = fg)
        self.totalLab2 = ttk.Label(self, text = self.totalText2.format(0), font = "helvetica {}".format(font), background = "white", width = 6, anchor = "e", foreground = fg)
        self.spaces = ttk.Label(self, text = " ", font = "helvetica {}".format(font), background = "white", width = 1)

        self.playerLab1.grid(column = 5, row = 1, padx = 3)
        self.totalLab1.grid(column = 6, row = 1, padx = 3, sticky = "ew")
        self.playerLab2.grid(column = 8, row = 1, padx = 3)        
        self.totalLab2.grid(column = 9, row = 1, padx = 3, sticky = "ew")
        self.spaces.grid(column = 7, row = 1)        
        
        self.changedValue(0)


    def onClick(self, event):
        click_position = event.x
        newValue = int((click_position / self.value.winfo_width()) * self.value['to'])
        self.changedValue(newValue)
        self.update()


    def changedValue(self, value):           
        value = str(min([max([eval(str(value)), 0]), self.maximum]))
        self.valueVar.set(value)
        newval = int(round(eval(self.valueVar.get())/self.rounding, 0)*self.rounding)
        self.valueVar.set("{0:3d}".format(newval))
        if self.player == "A":
            self.totalLab1["text"] = self.totalText1.format(self.endowment - newval)
            self.totalLab2["text"] = self.totalText2.format(self.endowment + newval * 3)
            self.totalLab1["font"] = "helvetica {} bold".format(self.font)
            self.playerLab1["font"] = "helvetica {} bold".format(self.font)
        elif self.player == "B":
            self.totalLab1["text"] = self.totalText1.format(self.endowment - self.returned + newval)
            self.totalLab2["text"] = self.totalText2.format(self.returned * 3 + self.endowment - newval)
            self.totalLab2["font"] = "helvetica {} bold".format(self.font)
            self.playerLab2["font"] = "helvetica {} bold".format(self.font)
        #self.parent.checkAnswers()
              


class Trust(InstructionsFrame):
    def __init__(self, root):

        if not "trustblock" in root.status:
            root.status["trustblock"] = 1
        else:
            root.status["trustblock"] += 1

        endowment = TRUST
     
        otherInfo = [f"Skupina {x}" for x in range(1, 31)]
        random.shuffle(otherInfo)
        otherInfo = "\n".join(otherInfo[:4])
        text = instructionsT2.format(otherInfo, endowment, endowment, int(endowment/5), endowment)

        height = 20
        width = 102

        super().__init__(root, text = text, height = height, font = 15, width = width)

        self.labA = ttk.Label(self, text = "Pokud budu hráč A", font = "helvetica 15 bold", background = "white")
        self.labA.grid(column = 0, row = 2, columnspan = 3, pady = 10)        

        # ta x-pozice tady je hnusny hack, idealne by se daly texty odmen vsechny sem ze slideru
        self.labR = ttk.Label(self, text = "Rozdělení odměn po tomto kroku", font = "helvetica 15 bold", background = "white", anchor = "center", width = 30)
        self.labR.grid(column = 1, row = 2, pady = 5, sticky = E)

        self.labX = ttk.Label(self, text = "Finální rozdělení odměn", font = "helvetica 15 bold", background = "white", anchor = "center", width = 28)
        self.labX.grid(column = 1, row = 6, pady = 5, sticky = E)

        self.frames = {}
        for i in range(8):            
            if i < 6:
                text = "Pokud hráč A pošle {} Kč, pošlu hráči A zpět:".format(int(i*endowment/5))
                ttk.Label(self, text = text, font = "helvetica 15", background = "white").grid(column = 0, row = 7 + i, pady = 1, sticky = E)
                player = "B"
            elif i == 6:
                ttk.Label(self, text = "Pošlu hráči B:", font = "helvetica 15", background = "white").grid(column = 0, row = 3, pady = 1, sticky = E)            
                player = "A"
            else:
                ttk.Label(self, text = "Očekávám, že hráč B pošle zpět:", font = "helvetica 15", background = "white").grid(column = 0, row = 4, pady = 1, sticky = E)  
                player = None
            maximum = int(i * 3 * endowment / 5 + endowment) if i < 6 else endowment            
            self.frames[i] = ScaleFrame(self, maximum = maximum, player = player, returned = int(i*endowment/5), endowment = endowment)
            row = 7 + i if i < 6 else i - 3
            self.frames[i].grid(column = 1, row = row, pady = 1)
            if i == 7:
                self.frames[i].value["state"] = "disabled"
        
        self.labB = ttk.Label(self, text = "Pokud budu hráč B", font = "helvetica 15 bold", background = "white")
        self.labB.grid(column = 0, row = 6, columnspan = 3, pady = 10)

        self.checkVar = BooleanVar()
        ttk.Style().configure("TCheckbutton", background = "white", font = "helvetica 15")
        self.checkBut = ttk.Checkbutton(self, text = checkButtonText, command = self.checkbuttoned, variable = self.checkVar, onvalue = True, offvalue = False)
        self.checkBut.grid(row = 19, column = 0, columnspan = 3, pady = 10)

        self.next.grid(column = 0, row = 20, columnspan = 3, pady = 5, sticky = N)            
        self.next["state"] = "disabled"
        
        self.text.grid(row = 1, column = 0, columnspan = 3)

        self.deciding = True

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(18, weight = 2)
        self.rowconfigure(20, weight = 2)

        self.columnconfigure(0, weight = 2)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 2)

    def checkbuttoned(self):
        self.next["state"] = "normal" if self.checkVar.get() else "disabled"
      
    def nextFun(self):
        if self.deciding:
            for i, frame in self.frames.items():
                if i != 7:
                    frame.value["state"] = "normal" if not self.checkVar.get() else "disabled"
                else:
                    frame.value["state"] = "normal" if self.checkVar.get() else "disabled"
                    frame.maximum = TRUST + int(self.frames[6].valueVar.get()) * 3
                    frame.value["to"] = frame.maximum
            self.deciding = False
            self.checkBut["text"] = checkButtonText2
            self.next["state"] = "disabled"
            self.checkVar.set(False)
        else:
            self.send()
            self.write()
            super().nextFun()

    def send(self):        
        self.responses = [self.frames[i].valueVar.get().strip() for i in range(7)]
        data = {'id': self.id, 'round': "trust" + str(self.root.status["trustblock"]), 'offer': "_".join(self.responses)}
        self.sendData(data)

    def write(self):
        block = self.root.status["trustblock"]
        self.file.write("Trust\n")        
        d = [self.id, str(block + 2), self.root.status["trust_pairs"][block-1], list(self.root.status["trust_roles"])[block-1]]
        self.file.write("\t".join(map(str, d + self.responses)))
        if URL == "TEST":
            if self.root.status["trust_roles"][block-1] == "A":                        
                self.root.status["trustTestSentA"] = int(self.frames[6].valueVar.get())
            else:
                self.root.status["trustTestSentB"] = [int(self.frames[i].valueVar.get()) for i in range(6)]       
        self.file.write("\n\n")




class WaitResults(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "", height = 3, font = 15, proceed = False, width = 45)
        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def checkUpdate(self):
        t0 = perf_counter() - 4
        while True:
            self.update()
            if perf_counter() - t0 > 5:
                t0 = perf_counter()
                block = self.root.status["trustblock"]
                endowment = 100 # TO DO

                data = urllib.parse.urlencode({'id': self.id, 'round': block, 'offer': "trust"})                
                data = data.encode('ascii')
                if URL == "TEST":                    
                    if self.root.status["trust_roles"][block - 1] == "A":                        
                        sentA = self.root.status["trustTestSentA"]
                        sentB = random.randint(0, int((sentA * 3 + endowment) / 10)) * 10
                    else:
                        chose = random.randint(0,5)
                        sentA = int(chose * 2 * endowment / 10)
                        sentB = self.root.status["trustTestSentB"][chose]
                    response = "_".join(map(str, [self.root.status["trust_pairs"][block - 1], sentA, sentB]))
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception as e:
                        continue

                if response:               
                    pair, sentA, sentB = response.split("_")
                    sentA, sentB = int(sentA), int(sentB)
                    
                    if int(self.root.status["winning_trust"]) == block + 2:
                        reward = endowment - sentA + sentB if self.root.status["trust_roles"][block-1] == "A" else endowment + sentA*3 - sentB    
                        self.root.texts["trust"] = str(reward)

                    if self.root.status["trust_roles"][block - 1] == "A": 
                        text = trustResultTextA.format(sentA, sentA*3, endowment + sentA*3, sentB, endowment - sentA + sentB, endowment + sentA*3 - sentB)
                    else:
                        text = trustResultTextB.format(sentA, sentA*3, endowment + sentA*3, sentB, endowment + sentA*3 - sentB, endowment - sentA + sentB)
                    self.root.texts["trustResult"] = text

                    self.write(response)
                    self.progressBar.stop()
                    self.nextFun()  
                    return

    def run(self):
        self.progressBar.start()
        self.checkUpdate()

    def write(self, response):
        self.file.write("Trust Results" + "\n")
        self.file.write(self.id + "\t" + response.replace("_", "\t") + "\n\n") 



TrustResult = (InstructionsFrame, {"text": "{}", "update": ["trustResult"]})

controlTexts = [[trustControl1, trustAnswers1, trustFeedback1], [trustControl2, trustAnswers2, trustFeedback2], [trustControl3, trustAnswers3, trustFeedback3]]
InstructionsTrust = (InstructionsAndUnderstanding, {"text": instructionsT1.format(TRUST, TRUST, int(TRUST/5), TRUST) + "\n\n", "height": 23, "width": 100, "name": "Trust Control Questions", "randomize": False, "controlTexts": controlTexts, "fillerheight": 300, "finalButton": "Pokračovat k volbě"})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login,    
         #InstructionsTrust,
         Trust,         
         Trust,
         WaitResults,
         TrustResult
         ])