import pyautogui
import time
import subprocess
import sys
import random
import win32api
from PIL import Image, ImageChops
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

def check_win_ttt(table):
    winner = '-'
    
    # Verifică liniile și coloanele
    for i in range(0, 3):
        if table[i][0] == table[i][1] and table[i][1] == table[i][2] and table[i][0] != '-':
            winner = table[i][0]
        if table[0][i] == table[1][i] and table[1][i] == table[2][i] and table[0][i] != '-':
            winner = table[0][i]
    
    # Verifică diagonalele
    if table[0][0] == table[1][1] and table[1][1] == table[2][2] and table[0][0] != '-':
        winner = table[0][0]
    if table[0][2] == table[1][1] and table[1][1] == table[2][0] and table[1][1] != '-':
        winner = table[1][1]
    
    return winner

def is_board_full(table):
    """Verifică dacă tabla e plină (pentru remiză)"""
    for i in range(3):
        for j in range(3):
            if table[i][j] == '-':
                return False
    return True

def minimax(table, depth, is_maximizing, player, opponent):
    """
    Algoritmul minimax pentru a găsi cea mai bună mișcare.
    """
    winner = check_win_ttt(table)
    
    # Cazuri terminale
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif is_board_full(table):  # Remiză - tabla plină, fără câștigător
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if table[i][j] == '-':
                    table[i][j] = player
                    score = minimax(table, depth + 1, False, player, opponent)
                    table[i][j] = '-'
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if table[i][j] == '-':
                    table[i][j] = opponent
                    score = minimax(table, depth + 1, True, player, opponent)
                    table[i][j] = '-'
                    best_score = min(score, best_score)
        return best_score

def get_next_move_ttt(table, player='X'):
    """
    Găsește cea mai bună mișcare pentru jucătorul specificat.
    
    Args:
        table: Tabla de joc 3x3 (listă de liste)
        player: Jucătorul curent ('X' sau '0')
    
    Returns:
        Tuple (i, j) cu cea mai bună mișcare sau (-1, -1) dacă tabla e plină
    """
    # Determină adversarul - CORECTAT: '0' în loc de 'O'
    opponent = '0' if player == 'X' else 'X'
    
    # Verifică dacă jocul s-a terminat
    if check_win_ttt(table) != '-' or is_board_full(table):
        return (-1, -1)
    
    best_score = float('-inf')
    best_move = (-1, -1)
    
    # Încearcă toate mișcările posibile
    for i in range(3):
        for j in range(3):
            if table[i][j] == '-':
                # Simulează mișcarea
                table[i][j] = player
                score = minimax(table, 0, False, player, opponent)
                table[i][j] = '-'  # Anulează mișcarea
                
                # Actualizează cea mai bună mișcare
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    return best_move


def get_enemy_move(table,cellsCoordinates):
    for i in range(0,3):
        for j in range(0,3):
            if table[i][j]=='-':
                screenshot = pyautogui.screenshot(region=(cellsCoordinates[3*i+j][0], cellsCoordinates[3*i+j][1], 182, 183))
                img = Image.open(f"portiune_screenshot{3*i+j}.png")

                #vreau sa vad celula in care exista diferente de pixeli (adica in care adversarul a facut mutarea)
                diff = ImageChops.difference(screenshot, img)

                if diff.getbbox() is None:
                    print("Nu s-a facut mutarea in aceasta celula")
                else:
                    table[i][j]='0'


    

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
            if attempts > 100:
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

    table=[['-','-','-'],['-','-','-'],['-','-','-']]

    # click pe searchbar
    pyautogui.click(730, 1050)

    # caut google
    pyautogui.write("Google", interval=0.05)
    time.sleep(1)

    # deschid google
    pyautogui.press('enter')

    time.sleep(1)
    #loc=pyautogui.locateCenterOnScreen('google_icon.png',confidence=0.8)
    #pyautogui.click(loc)
    time.sleep(1)

    #caut X si 0
    pyautogui.write("https://playtictactoe.org/",interval=0.05)
    pyautogui.press('enter')

    #astept sa se incarce pagina
    time.sleep(3)

    # i=0
    # for cell in cellsCoordinates:
    #     screenshot = pyautogui.screenshot(region=(cell[0], cell[1], 182, 183))
    #     screenshot.save(f"portiune_screenshot{i}.png")
    #     i=i+1

    game=0
    while True:
        print("yey")
        gameOver=False
        
        if game == 0:
            yourTurn=True
            game=1
        else:
            yourTurn=False
            game=0
        while gameOver==False:
            print("yeey")
            
            if yourTurn==True:
                print("Your Turn")

                (x,y)=get_next_move_ttt(table,'X')
                table[x][y]='X'
                pyautogui.click(cellsCoordinates[3*x+y])
                yourTurn=False
            else:
                print("Enemy Turn")

                get_enemy_move(table,cellsCoordinates)
                yourTurn=True

            win=check_win_ttt(table)
            if win != '-' or (win=='-' and is_board_full(table)==True):
                gameOver=True
                time.sleep(1)
                pyautogui.click(cellsCoordinates[0][0], cellsCoordinates[0][1])
            time.sleep(1)


        for i in range(0,3):
            for j in range(0,3):
                table[i][j]='-'

        time.sleep(1)
else:
    # deschid notepad
    subprocess.Popen('notepad.exe')

    # astept 2 secunde ca sa se deschida
    time.sleep(2)

    # deschid un note nou
    pyautogui.hotkey('ctrl', 'n')

    pyautogui.write("Argumentul dat nu este un nume valid al unui joc pe care il automatizeaza scriptul!")
