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
import os
from datetime import datetime

# Logging class
class TicTacToeLogger:
    def __init__(self, log_file="tictactoe_log.txt"):
        self.log_file = log_file
        self.current_user = self.get_current_user()
        self.game_number = 0
        self.session_start = datetime.now()
        
        # Write session start
        self.write_log(f"=== SESSION START ===")
        self.write_log(f"User: {self.current_user}")
        self.write_log(f"Start time: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        self.write_log(f"====================")
    
    def get_current_user(self):
        """Get current Windows user using whoami command"""
        try:
            result = subprocess.run(['whoami'], capture_output=True, text=True, shell=True)
            return result.stdout.strip()
        except Exception as e:
            return f"Unknown_User"
    
    def write_log(self, message):
        """Write message to log file with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(log_entry.strip())  # Also print to console
    
    def log_game_start(self, game_number, player_starts):
        """Log the start of a new game"""
        self.game_number = game_number
        self.game_start_time = datetime.now()
        
        self.write_log(f"--- GAME {game_number} START ---")
        self.write_log(f"Player starts: {'Yes' if player_starts else 'No'}")
        self.write_log(f"Initial board: Empty")
    
    def log_move(self, player, x, y, board_state):
        """Log a move made by player or enemy"""
        self.write_log(f"Move: {player} -> Position ({x},{y})")
        self.write_log(f"Board state: {self.format_board(board_state)}")
    
    def log_game_end(self, result, final_board):
        """Log the end of a game"""
        game_duration = datetime.now() - self.game_start_time
        
        self.write_log(f"Game result: {result}")
        self.write_log(f"Final board: {self.format_board(final_board)}")
        self.write_log(f"Game duration: {game_duration.total_seconds():.2f} seconds")
        self.write_log(f"--- GAME {self.game_number} END ---")
        self.write_log("")  # Empty line for readability
    
    def log_error(self, error_message):
        """Log an error"""
        self.write_log(f"ERROR: {error_message}")
    
    def log_info(self, info_message):
        """Log general information"""
        self.write_log(f"INFO: {info_message}")
    
    def format_board(self, board):
        """Format board state for logging"""
        board_str = ""
        for i in range(3):
            for j in range(3):
                board_str += board[i][j] if board[i][j] != '-' else ' '
            if i < 2:
                board_str += "|"
        return board_str
    
    def log_session_end(self):
        """Log session end"""
        session_duration = datetime.now() - self.session_start
        self.write_log(f"=== SESSION END ===")
        self.write_log(f"Total session time: {session_duration.total_seconds():.2f} seconds")
        self.write_log(f"Total games played: {self.game_number}")
        self.write_log(f"==================")

# Initialize logger
logger = TicTacToeLogger()

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
        pyautogui.moveTo(self.upgradeX,self.upgradeY)
        for i in range(1, self.scrollUnits + 1):
            pyautogui.scroll(-self.scrollUnits)
            pyautogui.move(0, -65)
        
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
                    logger.log_info(f"Nu s-a facut mutarea in celula ({i},{j})")
                else:
                    table[i][j]='0'
                    logger.log_move('0', i, j, table)
                    logger.log_info(f"Adversarul a facut mutarea in celula ({i},{j})")
                    return

print("Scriptul a inceput")

if sys.argv[1]=="ClickerHeroes":
    logger.log_info("Starting ClickerHeroes automation")
    
    # click pe searchbar
    pyautogui.click(730, 1050)

    # caut jocul
    pyautogui.write("Clicker Heroes", interval=0.05)

    # deschid jocul
    pyautogui.press('enter')

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
                if loc1:
                    pyautogui.click(1350,70)
                    pyautogui.click(1350,70)
                    pyautogui.click(1350,70)
                    pyautogui.click(1350,70)
                    print("Am trecut la nivelul anterior pentru a farma mai mult!")
            except:
                print("Am reusit sa bat bossul")

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

elif sys.argv[1]=="TicTacToe":
    logger.log_info("Starting TicTacToe automation")

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
    time.sleep(1)

    #caut X si 0
    pyautogui.write("https://playtictactoe.org/",interval=0.05)
    pyautogui.press('enter')

    #astept sa se incarce pagina
    time.sleep(3)

    game=0
    game_counter=0  # Counter separat pentru logging
    try:
        while True:
            gameOver=False
            game_counter += 1  # Incrementez counter-ul pentru logging
            
            player_starts = (game == 0)
            logger.log_game_start(game_counter, player_starts)
            
            if game == 0:
                yourTurn=True
                game=1
            else:
                yourTurn=False
                game=0
                
            while gameOver==False:
                if yourTurn==True:
                    logger.log_info("Player's turn")

                    (x,y)=get_next_move_ttt(table,'X')
                    if x != -1 and y != -1:
                        table[x][y]='X'
                        logger.log_move('X', x, y, table)
                        pyautogui.click(cellsCoordinates[3*x+y])
                    yourTurn=False
                else:
                    logger.log_info("Enemy's turn")
                    get_enemy_move(table,cellsCoordinates)
                    yourTurn=True

                win=check_win_ttt(table)
                if win != '-':
                    if win == 'X':
                        result = "WIN"
                    else:
                        result = "LOSS"
                    logger.log_game_end(result, table)
                    gameOver=True
                    time.sleep(1)
                    pyautogui.click(cellsCoordinates[0][0], cellsCoordinates[0][1])
                elif win=='-' and is_board_full(table)==True:
                    logger.log_game_end("DRAW", table)
                    gameOver=True
                    time.sleep(1)
                    pyautogui.click(cellsCoordinates[0][0], cellsCoordinates[0][1])
                    
                time.sleep(1)

            # Reset board
            for i in range(0,3):
                for j in range(0,3):
                    table[i][j]='-'

            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.log_info("Game interrupted by user")
        logger.log_session_end()
    except Exception as e:
        logger.log_error(f"Unexpected error: {str(e)}")
        logger.log_session_end()

else:
    logger.log_error(f"Invalid argument: {sys.argv[1]}")
    
    # deschid notepad
    subprocess.Popen('notepad.exe')

    # astept 2 secunde ca sa se deschida
    time.sleep(2)

    # deschid un note nou
    pyautogui.hotkey('ctrl', 'n')

    pyautogui.write("Argumentul dat nu este un nume valid al unui joc pe care il automatizeaza scriptul!")

# Log session end when script terminates
logger.log_session_end()