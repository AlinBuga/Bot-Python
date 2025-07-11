import pyautogui
import time
import subprocess
import sys
import random
import win32api
import win32con

butonUpgradeY=490
butonUpgradeX=180

offsetPowerX=142   #offset de la centrul upgradeului pana la primul powerup
offsetPowerY=40

scrollBarX=880
scrollBarY=550

levels10=True

class Erou:
    def __init__(self,nume,scrollUnits):
        global butonUpgradeY
        self.nume=nume
        self.upgradeX=butonUpgradeX
        self.upgradeY=butonUpgradeY
        self.scrollUnits=scrollUnits
        if butonUpgradeY < 946:
            butonUpgradeY=butonUpgradeY+152

    def click_upgrade(self):        #verificam daca este clickable (cand tin cursorul pe buton i se schimba culoarea)
        # global scrollBarY,scrollBarX
        # if self.scrollPixels==True:
        #     pyautogui.moveTo(scrollBarX, scrollBarY)
        #     pyautogui.mouseDown()
        #     pyautogui.move(0, 142, duration=0.1)  # scroll down 100 pixeli
        #     pyautogui.mouseUp()
        #     scrollBarY=scrollBarY+152

        # Convertim pixeli în unități de scroll (empiric)
        # units = int(self.scrollPixels / 3)  # 3 pixeli ≈ 1 unitate (poate varia)
        # win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -units, 0)

        # if levels10 == True:
        #     pyautogui.keyDown('shift')

        pyautogui.moveTo(self.upgradeX,self.upgradeY)
        for i in range(1, self.scrollUnits + 1):
            pyautogui.scroll(-self.scrollUnits)
            pyautogui.move(0, -65)

        # if self.scrollUnits == 9:
        #     pyautogui.scroll(self.scrollUnits)
        #     self.upgradeY=self.upgradeY+152
        
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()

        #dau click pe un powerup random
        random_number = random.randint(0, 6)     # pot sa fie maxim 7 power upuri per erou
        pyautogui.move(offsetPowerX+random_number*54,offsetPowerY)
        pyautogui.click()

        for i in range(1, self.scrollUnits + 1):
            pyautogui.scroll(self.scrollUnits)
            pyautogui.move(0, 65)
        
        # if self.scrollUnits == 9:
        #     pyautogui.scroll(-self.scrollUnits)
        #     self.upgradeY=self.upgradeY-152
    
        # if levels10 == True:
        #     pyautogui.keyUp('shift')
        #     levels10=False
        # else:
        #     levels10=True


eroi = [
    Erou("Cid",0),
    Erou("Treebeast",0),
    Erou("Ivan",0),
    Erou("Brittany",0),
    Erou("Fisherman",1),
    Erou("Betty",2),
    Erou("Samurai",3),
    Erou("Leon",4),
    Erou("Forest",5),
    Erou("Alexa",6),
    Erou("Natalia",7),
    Erou("Mercedes",8)
    #Erou("Bobby",9),
    #Erou("Broyle",10)
]


def check_new_level(template_path, confidence=0.8):
    loc = pyautogui.locateCenterOnScreen('exclamare_clicker.png',confidence=0.8)
    if loc:
        pyautogui.click(loc)
    else:
        print("Inca nu se poate trece la un nivel nou!")

print("Scriptul a inceput")

if sys.argv[1]=="ClickerHeroes":
    # click pe searchbar
    pyautogui.click(730, 1050)

    # caut jocul
    pyautogui.write("Clicker Heroes", interval=0.05)

    # deschid jocul
    pyautogui.press('enter')

    #time.sleep(15)
    

    foundStart=False
    while not foundStart:
        print("A intrat in while")

        try:
            loc = pyautogui.locateCenterOnScreen('start_clicker.png', confidence=0.8)
            pyautogui.moveTo(loc)
            pyautogui.click()
            foundStart=True
        except pyautogui.ImageNotFoundException:
            print("Butonul de start nu a fost gasit!")
            time.sleep(3)

    # astept sa se incarce jocul
    time.sleep(7)


    # inchid notificare daca este nevoie
    closeNotif=False
    attempts=0
    while not closeNotif:
        print("Se cauta notificarea!")

        try:
            loc = pyautogui.locateCenterOnScreen('exit_clicker.png',confidence=0.8)
            pyautogui.click(loc)
            closeNotif=True
        except:
            attempts=attempts+1
            if attempts > 50:
                break

    newLevelPress = time.time()
    newLevelInterval = 60  # 60 secunde

    newUpgradeCheck=time.time()
    newUpgradeInterval=50 # 50 secudne

    abilityActivationPress=time.time()
    abilityActivationInterval=600 # 10 minute

    isBoss=False
    bossInterval=30
    bossStart=-1

    searchBossInterval=10 #verific daca sunt la boss odata la 10 de secudne
    searchBossStart=time.time()

    pyautogui.write("123456789")  # hot keys pentru abilitatile speciale

    # incep farmul
    while True:
        pyautogui.click(1440, 570)

        if time.time() - searchBossStart >= searchBossInterval:
            searchBossStart=time.time()
            try:
                loc = pyautogui.locateCenterOnScreen('boss_clock_clicker.png',confidence=0.8)
                if isBoss==False and loc:
                    bossStart=time.time()
                    isBoss=True
                    print("Sunt la boss")
            except:
                print("Nu sunt la boss")

        if isBoss==True and time.time() - bossStart >= bossInterval:
            isBoss=False
            pyautogui.click(1530, 75)
            time.sleep(0.2)
            try:
                loc1=pyautogui.locateCenterOnScreen('boss_clock_clicker.png',confidence=0.8)
                # 1350 70 coordonatele de la nivelul anterior
                # ma duc 4 nivele in spate
                if loc1:
                    pyautogui.click(1350,70)
                    pyautogui.click(1350,70)
                    pyautogui.click(1350,70)
                    pyautogui.click(1350,70)
                    print("Am trecut la nivelul anterior pentru a farma mai mult!")
            except:
                print("Am reusit sa bat bossul")

        #pyautogui.click(1440, 570)

        if time.time() - newLevelPress >= newLevelInterval:
            pyautogui.click(1530, 75)
            newLevelPress = time.time()  # resetez timerul

        if time.time() - abilityActivationPress >= abilityActivationInterval:
            pyautogui.write("123456789")
            abilityActivationPress=time.time()  # resetez timerul

        if time.time() - newUpgradeCheck >= newUpgradeInterval:
            for erou in eroi:
                erou.click_upgrade()
            newUpgradeCheck = time.time()  # resetez timerul

        #880 550
elif sys.argv[1]=="TicTacToe":
    print("TicTacToe")

    cellsCoordinates=[
        (679,215),
        (866,215),
        (1059,215),
        (679,403),
        (866,403),
        (1059,403),
        (679,595),
        (866,595),
        (1059,595)
    ]

    # click pe searchbar
    pyautogui.click(730, 1050)

    # caut google
    pyautogui.write("Google", interval=0.05)
    time.sleep(1)

    # deschid google
    pyautogui.press('enter')

    time.sleep(1)
    loc=pyautogui.locateCenterOnScreen('google_icon.png',confidence=0.8)
    #pyautogui.click(loc)
    time.sleep(1)

    #caut X si 0
    pyautogui.write("https://playtictactoe.org/",interval=0.05)
    pyautogui.press('enter')

    #astept sa se incarce pagina
    time.sleep(3)

    i=0
    for cell in cellsCoordinates:
        screenshot = pyautogui.screenshot(region=(cell[0], cell[1], 182, 183))
        screenshot.save(f"portiune_screenshot{i}.png")
        i=i+1
else:
    # deschid notepad
    subprocess.Popen('notepad.exe')

    # astept 2 secunde ca sa se deschida
    time.sleep(2)

    # deschid un note nou
    pyautogui.hotkey('ctrl', 'n')

    pyautogui.write("Argumentul dat nu este un nume valid al unui joc pe care il automatizeaza scriptul!")
