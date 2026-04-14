import tkinter as tk

# Luodaan pääikkuna
window = tk.Tk()
window.title("Ristinolla")
window.minsize(400, 550)

# -------------------------
# MUUTTUJAT
# -------------------------

# Pelaajien nimet
player_x = ""
player_o = ""

# Pelilaudan koko ja voittorivin pituus
koko = 3
voitteen_pituus = 3

# Kumpi pelaaja on vuorossa
current_player = "X"

# Pelilauta (2D lista)
board = []

# Lista nappeja varten (GUI)
buttons = []

# Tänne tallennetaan voittorivin ruudut
winning_cells = []

# Pelaajien pisteet
score_x = 0
score_o = 0

# -------------------------
# ASETUSNÄYTTÖ (PELIASETUKSET)
# -------------------------

# Kehys jossa kysytään pelaajien nimet ja pelin asetukset
setup_frame = tk.Frame(window)
setup_frame.pack(pady=20)

# Pelaaja X nimi
tk.Label(setup_frame, text="Pelaaja X nimi").pack()
entry_x = tk.Entry(setup_frame)
entry_x.pack()

# Pelaaja O nimi
tk.Label(setup_frame, text="Pelaaja O nimi").pack()
entry_o = tk.Entry(setup_frame)
entry_o.pack()

# Pelilaudan koko
tk.Label(setup_frame, text="Pelilaudan koko (3-10)").pack()
entry_size = tk.Entry(setup_frame)
entry_size.pack()

# Montako merkkiä tarvitaan voittoon
tk.Label(setup_frame, text="Voiton pituus").pack()
entry_win = tk.Entry(setup_frame)
entry_win.pack()

# -------------------------
# PELINÄKYMÄ
# -------------------------

# Kehys varsinaiselle pelille
game_frame = tk.Frame(window)

# Teksti joka näyttää kenen vuoro on
info_label = tk.Label(window, text="", font=("Arial", 14))

# Teksti joka näyttää pisteet
score_label = tk.Label(window, text="", font=("Arial", 12))

# Kehys pelilaudalle
board_frame = tk.Frame(game_frame)

# -------------------------
# INFO TEKSTIT
# -------------------------

def update_info():
    # Päivittää tekstin joka kertoo kenen vuoro on
    if current_player == "X":
        info_label.config(text=f"{player_x} vuoro", fg="blue")
    else:
        info_label.config(text=f"{player_o} vuoro", fg="red")

def update_score():
    # Päivittää pelaajien pisteet näytölle
    score_label.config(text=f"{player_x}: {score_x} | {player_o}: {score_o}")

# -------------------------
# VOITON TARKISTUS
# -------------------------

def check_winner(r, c):

    # Tallennetaan voittorivi tähän listaan
    global winning_cells

    # Tarkistetaan 4 suuntaa
    directions = [(1,0),(0,1),(1,1),(1,-1)]

    for dr,dc in directions:

        # Lista joka sisältää kaikki saman merkin ruudut
        cells = [(r,c)]

        # Tarkistus eteenpäin
        i=1
        while True:
            nr=r+dr*i
            nc=c+dc*i

            if 0<=nr<koko and 0<=nc<koko and board[nr][nc]==current_player:
                cells.append((nr,nc))
                i+=1
            else:
                break

        # Tarkistus taaksepäin
        i=1
        while True:
            nr=r-dr*i
            nc=c-dc*i

            if 0<=nr<koko and 0<=nc<koko and board[nr][nc]==current_player:
                cells.append((nr,nc))
                i+=1
            else:
                break

        # Jos merkkejä on tarpeeksi -> voitto
        if len(cells) >= voitteen_pituus:
            winning_cells = cells[:voitteen_pituus]
            return True

    return False

# -------------------------
# TARKISTETAAN ONKO LAUTA TÄYNNÄ
# -------------------------

def board_full():
    for row in board:
        if "" in row:
            return False
    return True

# -------------------------
# PELIN LOPETUS
# -------------------------

def end_game(text):

    # Näytetään voittaja tai tasapeli
    info_label.config(text=text)

    # Väritetään voittorivi vihreäksi
    for r,c in winning_cells:
        buttons[r][c].config(bg="lightgreen")

    # Estetään lisäklikkaukset
    for row in buttons:
        for b in row:
            b.config(state="disabled")

# -------------------------
# KUN RUUTUA KLIKATAAN
# -------------------------

def click(r,c):

    global current_player, score_x, score_o

    # Jos ruutu on jo käytössä -> ei tehdä mitään
    if board[r][c]!="":
        return

    # Tallennetaan merkki pelilautaan
    board[r][c]=current_player

    # Päivitetään napin teksti
    if current_player=="X":
        buttons[r][c].config(text="X", fg="blue")
    else:
        buttons[r][c].config(text="O", fg="red")

    # Tarkistetaan voitto
    if check_winner(r,c):

        if current_player=="X":
            score_x+=1
            end_game(f"{player_x} voitti!")
        else:
            score_o+=1
            end_game(f"{player_o} voitti!")

        update_score()
        return

    # Tarkistetaan tasapeli
    if board_full():
        end_game("Tasapeli")
        return

    # Vaihdetaan vuoro
    current_player="O" if current_player=="X" else "X"

    update_info()

# -------------------------
# UUSI PELI
# -------------------------

def new_game():

    global board,current_player,winning_cells

    # Tyhjennetään pelilauta
    board=[["" for _ in range(koko)] for _ in range(koko)]
    winning_cells=[]

    # X aloittaa aina
    current_player="X"

    # Tyhjennetään napit
    for r in range(koko):
        for c in range(koko):
            buttons[r][c].config(text="",state="normal",bg="SystemButtonFace")

    update_info()

# -------------------------
# LUODAAN PELILAUTA
# -------------------------

def create_board():

    for r in range(koko):

        row=[]

        for c in range(koko):

            # Luodaan nappi jokaiselle ruudulle
            b=tk.Button(
                board_frame,
                text="",
                width=4,
                height=2,
                font=("Arial",20),
                command=lambda r=r,c=c:click(r,c)
            )

            # Sijoitetaan nappi ruudukkoon
            b.grid(row=r,column=c)

            row.append(b)

        buttons.append(row)

# -------------------------
# PELIN ALOITUS
# -------------------------

def start_game():

    global player_x,player_o,koko,voitteen_pituus,board

    # Haetaan pelaajien nimet
    player_x = entry_x.get() or "Pelaaja X"
    player_o = entry_o.get() or "Pelaaja O"

    # Luetaan pelilaudan koko
    try:
        koko = int(entry_size.get())
        if koko <3 or koko>10:
            koko=3
    except:
        koko=3

    # Luetaan voittorivin pituus
    try:
        voitteen_pituus=int(entry_win.get())
        if voitteen_pituus<3 or voitteen_pituus>koko:
            voitteen_pituus=3
    except:
        voitteen_pituus=3

    # Piilotetaan asetukset
    setup_frame.pack_forget()

    # Näytetään pelin elementit
    info_label.pack()
    score_label.pack()

    game_frame.pack()
    board_frame.pack()

    # Luodaan tyhjä pelilauta
    board=[["" for _ in range(koko)] for _ in range(koko)]

    create_board()

    update_info()
    update_score()

# -------------------------
# START NAPPI
# -------------------------

start_button = tk.Button(
    setup_frame,
    text="Aloita peli",
    command=start_game
)

start_button.pack(pady=10)

# -------------------------
# UUSI PELI NAPPI
# -------------------------

new_button=tk.Button(
    window,
    text="Uusi peli",
    command=new_game
)

new_button.pack(side="bottom",pady=10)

# Käynnistetään ohjelma
window.mainloop()