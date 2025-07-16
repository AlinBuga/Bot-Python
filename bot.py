import pyautogui
import time
import subprocess
import sys
import random
import win32api
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
import pytesseract
import re
import win32con
import cv2
import numpy as np

# def process_image_for_ocr(image):
#     """Procesează imaginea pentru a îmbunătăți recunoașterea OCR"""
    
#     # Convertește PIL Image la numpy array pentru OpenCV
#     img_array = np.array(image)
    
#     # Convertește la grayscale
#     if len(img_array.shape) == 3:
#         gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
#     else:
#         gray = img_array
    
#     # Măărește dimensiunea imaginii (scale up)
#     scale_factor = 4
#     width = int(gray.shape[1] * scale_factor)
#     height = int(gray.shape[0] * scale_factor)
#     resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)
    
#     # Aplică threshold pentru a obține o imagine binar (alb-negru)
#     _, thresh = cv2.threshold(resized, 127, 255, cv2.THRESH_BINARY)
    
#     # Aplică blur pentru a netezi marginile
#     blurred = cv2.GaussianBlur(thresh, (1, 1), 0)
    
#     # Convertește înapoi la PIL Image
#     processed_image = Image.fromarray(blurred)
    
#     return processed_image


# # Configurează calea către Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# cnt=0

# def extract_single_number_optimized(x,y):
#     """Extrage un singur număr cu configurarea optimă"""

#     global cnt
    
#     # Fă screenshot-ul
#     screenshot1 = pyautogui.screenshot(region=(x+438, y-40, 80, 40))      #x y width height
    
#     # Mărește imaginea cu factor 6 (mai mare pentru mai multă precizie)
#     scaled_img = screenshot1.resize((screenshot1.width * 6, screenshot1.height * 6), Image.LANCZOS)
    
#     # Convertește la grayscale
#     gray_img = scaled_img.convert('L')
    
#     # Îmbunătățește contrastul
#     enhancer = ImageEnhance.Contrast(gray_img)
#     contrast_img = enhancer.enhance(2.5)
    
#     # Aplică sharpening pentru margini mai clare
#     sharpened = contrast_img.filter(ImageFilter.SHARPEN)
    
#     # Salvează imaginea procesată pentru debugging
#     sharpened.save(f"processed_number{cnt}.png")
#     cnt=cnt+1
    
#     # PSM 8 - configurarea optimă pentru un singur cuvânt/număr
#     config_optimal = '--psm 8 -c tessedit_char_whitelist=0123456789'
    
#     try:
#         # Încearcă cu configurarea optimă
#         text = pytesseract.image_to_string(sharpened, config=config_optimal).strip()
#         print(f"PSM 8 rezultat: '{text}'")
        
#         if text and text.isdigit():
#             return int(text)
        
#         # Dacă PSM 8 nu funcționează, încearcă PSM 7
#         config_backup = '--psm 7 -c tessedit_char_whitelist=0123456789'
#         text_backup = pytesseract.image_to_string(sharpened, config=config_backup).strip()
#         print(f"PSM 7 rezultat: '{text_backup}'")
        
#         if text_backup and text_backup.isdigit():
#             return int(text_backup)
        
#         # Ultima încercare cu PSM 6
#         config_last = '--psm 6 -c tessedit_char_whitelist=0123456789'
#         text_last = pytesseract.image_to_string(sharpened, config=config_last).strip()
#         print(f"PSM 6 rezultat: '{text_last}'")
        
#         # Extrage numerele din orice rezultat
#         numere = re.findall(r'\d+', text + text_backup + text_last)
#         if numere:
#             return int(numere[0])
        
#         return None
        
#     except Exception as e:
#         print(f"Eroare OCR: {e}")
#         return None


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

butonUpgradeY=490
butonUpgradeX=180

offsetPowerX=142   #offset de la centrul upgradeului pana la primul powerup
offsetPowerY=40

scrollBarX=880
scrollBarY=550
#550 455
#370 -35 offset pana la LVL

#700 480
#150 25 height si width LVL
levels10=True

class Erou:
    def __init__(self,nume,scrollUnits):
        global butonUpgradeY
        self.nume=nume
        self.upgradeX=butonUpgradeX
        self.upgradeY=butonUpgradeY
        self.scrollUnits=scrollUnits
        if butonUpgradeY < 946:
            butonUpgradeY=butonUpgradeY+155  #152

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

    # def get_level(self):
    #     pyautogui.moveTo(self.upgradeX,self.upgradeY)
    #     for i in range(1, self.scrollUnits + 1):
    #         pyautogui.scroll(-self.scrollUnits)
    #         pyautogui.move(0, -65)

    #     x, y = pyautogui.position()
    #     number=extract_single_number_optimized(x,y)

    #     print(number)

    #     for i in range(1, self.scrollUnits + 1):
    #         pyautogui.scroll(self.scrollUnits)
    #         pyautogui.move(0, 65)



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
    
    # verifica liniile și coloanele
    for i in range(0, 3):
        if table[i][0] == table[i][1] and table[i][1] == table[i][2] and table[i][0] != '-':
            winner = table[i][0]
        if table[0][i] == table[1][i] and table[1][i] == table[2][i] and table[0][i] != '-':
            winner = table[0][i]
    
    # verifica diagonalele
    if table[0][0] == table[1][1] and table[1][1] == table[2][2] and table[0][0] != '-':
        winner = table[0][0]
    if table[0][2] == table[1][1] and table[1][1] == table[2][0] and table[1][1] != '-':
        winner = table[1][1]
    
    return winner

def is_board_full(table):
    #verifica daca tabela e full
    for i in range(3):
        for j in range(3):
            if table[i][j] == '-':
                return False
    return True

def minimax(table, depth, is_maximizing, player, opponent):
    #gasim cele mai bune cazuri
    winner = check_win_ttt(table)
    
    # cazuri terminale
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif is_board_full(table):  # egal
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
    #cea mai buna miscare pentru un jucator

    opponent = '0' if player == 'X' else 'X'
    
    # verifica daca jocul s a terminat
    if check_win_ttt(table) != '-' or is_board_full(table):
        return (-1, -1)
    
    best_score = float('-inf')
    best_move = (-1, -1)
    
    # incearca toate miscarile posibile
    for i in range(3):
        for j in range(3):
            if table[i][j] == '-':
                # simuleaza miscarea
                table[i][j] = player
                score = minimax(table, 0, False, player, opponent)
                table[i][j] = '-'  # anuleaza miscarea
                
                # actualizeaza cea mai buna miscare
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    return best_move


def get_enemy_move(table,cellsCoordinates):
    for i in range(0,3):
        for j in range(0,3):
            if table[i][j]=='-':
                screenshot = pyautogui.screenshot(region=(cellsCoordinates[3*i+j][0], cellsCoordinates[3*i+j][1], 182, 183))
                img = Image.open("empty_cell.png")

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

    # print(pytesseract.get_tesseract_version())

    # screenshot1 = pyautogui.screenshot(region=(618, 450, 80, 40))  # x, y, width, height
    # screenshot1.save("zona.png")  # doar pentru debug
    # # OCR pe imagine
    # text = pytesseract.image_to_string(screenshot1)

    # # Extrage doar cifrele
    # numere = re.findall(r'\d+', text)
    # print("Numere detectate:", numere)

    # number = extract_single_number_optimized()
    # if number:
    #     print(f"✅ Numărul detectat: {number}")
    # else:
    #     print("❌ Nu s-a putut detecta numărul")

    # quit()
    # exit()

    # time.sleep(100)

    # for erou in eroi:
    #     erou.get_level()

    # time.sleep(100)

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

    cnt=0

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
            cnt=cnt+1
            if cnt<4:
                for erou in reversed(eroi):
                    erou.click_upgrade()
            else:
                cnt=0
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
