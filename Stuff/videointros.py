#! python3

import os

from common import InstructionsFrame
from gui import GUI
from constants import LIMIT
from login import Login


instructions1 = """
Než přistoupíme k hlavní části studie, připravili jsme pro vás krátkou úvodní část, ve které Vás seznámíme s podobou videí, jejich strukturou a způsobem následného vyplňování úkolů.

Nejprve představíme téma, o kterém všechna videa jsou - tedy jak pořádat pracovní schůzky a porady. Poté uvidíte dvě krátká videa. Každé z nich je zpracováno v odlišném formátu.

Cílem této části je, abyste se seznámili s oběma formáty videí, dali na ně zpětnou vazbu a zároveň si osvojili způsob, jakým probíhá krátký kvíz o obsahu videí. Tato část není nijak peněžně odměněna, slouží k seznámení s průběhem další části studie.
"""

instructions2 = """
Vítejte v lekci zaměřené na porady a pracovní schůzky. Možná se vám při slově „porada“ vybaví spíše frustrace než efektivní komunikace – a účast na školení o poradách může působit ještě o něco absurdněji. Nejste sami.

Podle studií z oblasti organizační psychologie je více než polovina času stráveného na poradách zcela neefektivní. Průměrný zaměstnanec tráví na poradách přibližně 6 hodin týdně, u vedoucích pracovníků to může být až 23 hodin. Schůzky často bývají vnímány jako ztráta času – bez jasného cíle, bez využití schopností účastníků a bez skutečného dopadu na práci.

Všechna videa v této lekci Vám nabídnou konkrétní rady, jak porady vést efektivněji a jak se na nich lépe uplatnit i jako účastník. Doporučení vycházejí z výzkumů v oblasti psychologie a projektového managementu z různých částí světa.

První část videí se zaměří na psychologické aspekty – tedy proč porady často nefungují, jaké tendence vedou ke zbytečnému komplikování problémů a proč někdy ztrácíme čas. Následující videa nabídnou praktické tipy – nejprve pro organizátory porad, dále pro samotné účastníky a nakonec se zaměříme na specifika online meetingů.
"""

instructions3 = """
V následujícím kroku uvidíte první video ve formátu {}. Po jeho zhlédnutí Vás čeká krátké hodnocení videa a znalostní test.
"""

instructions4 = """
Děkujeme! Právě jste dokončili první část studie.
Zhlédli jste dvě videa ve dvou různých formátech a poskytli nám své hodnocení i odpovědi na kvízové otázky.
"""

braces = "{}"
instructions5 = f"""
Čeká Vás dále série pěti videí, jejich ohodnocení a závěrečný kvíz k této sérii videí, za který již budete odměněni. 

Pokud v závěrečném kvízu obdržíte alespoň {LIMIT} bodů z 25, obdržíte dodatečnou finanční odměnu ve výši {braces} Kč.

Nyní vás čeká rozhodnutí, ve kterém formátu videí byste chtěli pokračovat pro sérii pěti videí. Po zhlédnují všech videí Vás opět čeká jejich hodnocení a finální kvíz z těchto 5 videí. 
Váš výběr je důležitý – výše vaší odměny závisí na úspěšnosti tohoto finálního kvízu.
"""


VideoIntro1 = (InstructionsFrame, {"text": instructions1, "proceed": True, "height": 15})
VideoIntro2 = (InstructionsFrame, {"text": instructions2, "proceed": True, "height": 25})
VideoIntro3 = (InstructionsFrame, {"text": instructions3, "proceed": True, "height": 10, "update": ["version1"]})
VideoIntro4 = (InstructionsFrame, {"text": instructions4, "proceed": True, "height": 10})
VideoIntro5 = (InstructionsFrame, {"text": instructions5, "proceed": True, "height": 25, "update": ["condition"]})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login, 
        VideoIntro1,
        VideoIntro2,
        VideoIntro3,
        VideoIntro4,
        VideoIntro5])
