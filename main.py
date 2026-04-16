import tkinter as tk
import random

# tuodaan kirjastot
# tkinter = ikkuna ja napit
# random = tietokoneen satunnainen siirto

# -------------------------
# WINDOW
# -------------------------

window = tk.Tk()  # tehdään pääikkuna
window.title("Custom Tic Tac Toe")  # ikkunan nimi
window.minsize(500, 600)  # ikkunan pienin koko

# -------------------------
# GAME STATE
# -------------------------

player_x = ""  # pelaaja X nimi
player_o = ""  # pelaaja O nimi tai AI

vs_ai = False  # pelataanko AI:ta vastaan
difficulty = "easy"  # vaikeustaso aluksi

koko = 3  # pelilaudan koko
voitteen_pituus = 3  # montako merkkiä pitää saada riviin

current_player = "X"  # X aloittaa aina

board = []  # tähän tallennetaan pelilaudan tiedot
buttons = []  # tähän tallennetaan napit
winning_cells = []  # tähän tallennetaan voittorivi

score_x = 0  # X pisteet
score_o = 0  # O pisteet

# -------------------------
# SETUP UI
# -------------------------

setup_frame = tk.Frame(window)  # alkuasetusten kehys
setup_frame.pack(pady=10)  # näytetään se

tk.Label(setup_frame, text="Player X name").pack()  # teksti X pelaajalle
entry_x = tk.Entry(setup_frame)  # kenttä X nimelle
entry_x.pack()

tk.Label(setup_frame, text="Player O name / AI").pack()  # teksti O pelaajalle
entry_o = tk.Entry(setup_frame)  # kenttä O nimelle
entry_o.pack()

tk.Label(setup_frame, text="Board size (3-10)").pack()  # teksti laudan koolle
entry_size = tk.Entry(setup_frame)  # kenttä laudan koolle
entry_size.pack()

tk.Label(setup_frame, text="Win length").pack()  # teksti voiton pituudelle
entry_win = tk.Entry(setup_frame)  # kenttä voiton pituudelle
entry_win.pack()

# -------------------------
# DIFFICULTY BUTTONS
# -------------------------

difficulty_frame = tk.Frame(setup_frame)  # kehys vaikeustason napeille
difficulty_frame.pack(pady=10)

def set_difficulty(level):
    global difficulty  # käytetään yhteistä difficulty-muuttujaa
    difficulty = level  # tallennetaan valittu taso

    # ensin kaikki napit saman värisiksi
    btn_easy.config(bg="lightgray")
    btn_med.config(bg="lightgray")
    btn_hard.config(bg="lightgray")

    # valittu nappi saa eri värin
    if level == "easy":
        btn_easy.config(bg="lightgreen")
    elif level == "medium":
        btn_med.config(bg="orange")
    else:
        btn_hard.config(bg="red")

btn_easy = tk.Button(
    difficulty_frame,
    text="Easy",
    width=8,
    command=lambda: set_difficulty("easy")
)  # easy-nappi
btn_easy.grid(row=0, column=0, padx=5)

btn_med = tk.Button(
    difficulty_frame,
    text="Medium",
    width=8,
    command=lambda: set_difficulty("medium")
)  # medium-nappi
btn_med.grid(row=0, column=1, padx=5)

btn_hard = tk.Button(
    difficulty_frame,
    text="Hard",
    width=8,
    command=lambda: set_difficulty("hard")
)  # hard-nappi
btn_hard.grid(row=0, column=2, padx=5)

set_difficulty("easy")  # oletuksena easy

# -------------------------
# GAME UI
# -------------------------

info_label = tk.Label(window, text="", font=("Arial", 14))  # näyttää vuoron tai lopputuloksen
score_label = tk.Label(window, text="", font=("Arial", 12))  # näyttää pisteet

game_frame = tk.Frame(window)  # pelin kehys
board_frame = tk.Frame(game_frame)  # pelilaudan kehys

# -------------------------
# INFO
# -------------------------

def update_info():
    # päivittää kenen vuoro on
    if current_player == "X":
        info_label.config(text=f"{player_x} turn", fg="blue")
    else:
        if vs_ai:
            info_label.config(text=f"AI ({difficulty}) turn", fg="red")
        else:
            info_label.config(text=f"{player_o} turn", fg="red")

def update_score():
    # päivittää pisteet näytölle
    score_label.config(text=f"{player_x}: {score_x} | {player_o}: {score_o}")

# -------------------------
# WIN CHECK
# -------------------------

def check_winner(r, c):
    global winning_cells  # käytetään yhteistä voittorivilistaa

    # tarkistetaan 4 suuntaa
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dr, dc in directions:
        cells = [(r, c)]  # aloitetaan nykyisestä ruudusta

        # tarkistus eteenpäin
        for i in range(1, koko):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < koko and 0 <= nc < koko and board[nr][nc] == current_player:
                cells.append((nr, nc))
            else:
                break

        # tarkistus taaksepäin
        for i in range(1, koko):
            nr, nc = r - dr * i, c - dc * i
            if 0 <= nr < koko and 0 <= nc < koko and board[nr][nc] == current_player:
                cells.append((nr, nc))
            else:
                break

        # jos merkkejä on tarpeeksi, tulee voitto
        if len(cells) >= voitteen_pituus:
            winning_cells = cells[:voitteen_pituus]
            return True

    return False  # muuten ei voittoa

# -------------------------
# BOARD FULL
# -------------------------

def board_full():
    # tarkistaa onko lauta täynnä
    return all("" not in row for row in board)

# -------------------------
# END GAME
# -------------------------

def end_game(text, is_win=False):
    info_label.config(text=text)  # näyttää lopputekstin

    # jos tuli voitto, voittorivi vihreäksi
    if is_win:
        for r, c in winning_cells:
            buttons[r][c].config(bg="lightgreen")

    # kaikki napit pois käytöstä
    for row in buttons:
        for b in row:
            b.config(state="disabled")

# -------------------------
# AI
# -------------------------

def can_win(player):
    # tarkistaa voiko pelaaja voittaa yhdellä siirrolla
    for r in range(koko):
        for c in range(koko):
            if board[r][c] == "":
                board[r][c] = player
                temp = current_player
                globals()["current_player"] = player
                win = check_winner(r, c)
                globals()["current_player"] = temp
                board[r][c] = ""
                if win:
                    return (r, c)
    return None

def ai_move():
    # etsitään tyhjät ruudut
    empty = [(r, c) for r in range(koko) for c in range(koko) if board[r][c] == ""]

    if not empty:
        return

    # easy = satunnainen siirto
    if difficulty == "easy":
        click(*random.choice(empty))
        return

    # jos AI voi voittaa heti
    win_move = can_win("O")
    if win_move:
        click(*win_move)
        return

    # jos pitää estää X:n voitto
    block_move = can_win("X")
    if block_move:
        click(*block_move)
        return

    # hard yrittää ensin keskelle
    if difficulty == "hard":
        center = koko // 2
        if board[center][center] == "":
            click(center, center)
            return

    # muuten satunnainen siirto
    click(*random.choice(empty))

# -------------------------
# CLICK
# -------------------------

def click(r, c):
    global current_player, score_x, score_o

    # jos ruutu on jo käytössä, ei tehdä mitään
    if board[r][c] != "":
        return

    # tallennetaan merkki lautaan
    board[r][c] = current_player

    # näytetään merkki napissa
    if current_player == "X":
        buttons[r][c].config(text="X", fg="blue")
    else:
        buttons[r][c].config(text="O", fg="red")

    # tarkistetaan voitto
    if check_winner(r, c):
        if current_player == "X":
            score_x += 1
            end_game(f"{player_x} wins!", True)
        else:
            score_o += 1
            end_game(f"{player_o if not vs_ai else 'AI'} wins!", True)

        update_score()
        return

    # tarkistetaan tasapeli
    if board_full():
        end_game("Draw")
        return

    # vaihdetaan pelaajaa
    current_player = "O" if current_player == "X" else "X"
    update_info()

    # jos AI käytössä ja O vuorossa, AI pelaa
    if vs_ai and current_player == "O":
        window.after(300, ai_move)

# -------------------------
# NEW GAME
# -------------------------

def new_game():
    global board, current_player, winning_cells

    # uusi tyhjä lauta
    board = [["" for _ in range(koko)] for _ in range(koko)]
    winning_cells.clear()
    current_player = "X"

    # tyhjennetään kaikki napit
    for r in range(koko):
        for c in range(koko):
            buttons[r][c].config(text="", state="normal", bg="SystemButtonFace")

    update_info()  # päivitetään vuoroteksti

# -------------------------
# BOARD CREATE
# -------------------------

def create_board():
    buttons.clear()  # tyhjennetään vanha nappilista

    # poistetaan vanhat napit ruudulta
    for widget in board_frame.winfo_children():
        widget.destroy()

    # tehdään uusi pelilauta
    for r in range(koko):
        row = []
        for c in range(koko):
            b = tk.Button(
                board_frame,
                text="",
                width=4,
                height=2,
                font=("Arial", 20),
                command=lambda r=r, c=c: click(r, c)
            )
            b.grid(row=r, column=c)
            row.append(b)
        buttons.append(row)

# -------------------------
# START GAME
# -------------------------

def start_game():
    global player_x, player_o, koko, voitteen_pituus, vs_ai, board, winning_cells

    # haetaan nimet kentistä
    player_x = entry_x.get() or "Player X"
    player_o = entry_o.get()

    # tarkistetaan että laudan koko on numero
    try:
        koko = int(entry_size.get())
    except:
        info_label.config(text="Board size must be a number", fg="red")
        info_label.pack()
        return

    # tarkistetaan että koko on sallittu
    if koko < 3 or koko > 10:
        info_label.config(text="Board size must be between 3 and 10", fg="red")
        info_label.pack()
        return

    # tarkistetaan että voittopituus on numero
    try:
        voitteen_pituus = int(entry_win.get())
    except:
        info_label.config(text="Win length must be a number", fg="red")
        info_label.pack()
        return

    # voittopituus ei saa olla liian pieni
    if voitteen_pituus < 3:
        info_label.config(text="Win length must be at least 3", fg="red")
        info_label.pack()
        return

    # voittopituus ei saa olla suurempi kuin lauta
    if voitteen_pituus > koko:
        info_label.config(text="Win length cannot be bigger than board size", fg="red")
        info_label.pack()
        return

    winning_cells.clear()  # tyhjennetään vanha voittorivi

    # jos O nimi on tyhjä, käytetään AI:ta
    vs_ai = (player_o == "")

    if vs_ai:
        player_o = "AI"

    setup_frame.pack_forget()  # piilotetaan alkuasetukset

    info_label.pack()  # näytetään vuoroteksti
    score_label.pack()  # näytetään pisteet

    game_frame.pack()  # näytetään pelin kehys
    board_frame.pack()  # näytetään pelilauta

    # tehdään tyhjä pelilauta
    board = [["" for _ in range(koko)] for _ in range(koko)]

    create_board()  # luodaan napit laudalle

    update_info()  # päivitetään vuoroteksti
    update_score()  # päivitetään pisteet

# -------------------------
# BUTTONS
# -------------------------

start_button = tk.Button(setup_frame, text="Start Game", command=start_game)  # aloitusnappi
start_button.pack(pady=10)

new_button = tk.Button(window, text="New Game", command=new_game)  # uuden pelin nappi
new_button.pack(side="bottom", pady=10)

window.mainloop()  # käynnistetään ohjelma
