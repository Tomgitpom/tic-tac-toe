import tkinter as tk
import random
from database import init_db, get_player_wins, save_win

# Käynnistetään tietokanta heti ohjelman alussa.
# Tietokantaan tallennetaan pelaajien voitot.
init_db()

# -------------------------
# IKKUNA
# -------------------------

window = tk.Tk()
window.title("Muokattava ristinolla")
window.minsize(500, 600)

# -------------------------
# PELIN TILA
# -------------------------
# Näissä muuttujissa säilytetään pelin tämänhetkinen tilanne.

player_x = ""
player_o = ""

vs_ai = False
difficulty = "easy"

koko = 3
voitteen_pituus = 3

current_player = "X"

board = []
buttons = []
winning_cells = []

score_x = 0
score_o = 0

# -------------------------
# ALOITUSNÄKYMÄ
# -------------------------
# Tässä käyttäjä antaa nimet, pelilaudan koon ja voiton pituuden.

setup_frame = tk.Frame(window)
setup_frame.pack(pady=10)

tk.Label(setup_frame, text="Pelaaja X nimi").pack()
entry_x = tk.Entry(setup_frame)
entry_x.pack()

tk.Label(setup_frame, text="Pelaaja O nimi / AI").pack()
entry_o = tk.Entry(setup_frame)
entry_o.pack()

tk.Label(setup_frame, text="Pelilaudan koko (3-10)").pack()
entry_size = tk.Entry(setup_frame)
entry_size.pack()

tk.Label(setup_frame, text="Voiton pituus").pack()
entry_win = tk.Entry(setup_frame)
entry_win.pack()

# -------------------------
# VAIKEUSTASON VALINTA
# -------------------------
# Jos O-pelaajan nimi jätetään tyhjäksi, peliä pelataan AI:ta vastaan.

difficulty_frame = tk.Frame(setup_frame)
difficulty_frame.pack(pady=10)


def difficulty_text():
    """Palauttaa vaikeustason tekstinä käyttöliittymää varten."""
    if difficulty == "easy":
        return "Helppo"
    elif difficulty == "medium":
        return "Keskitaso"
    return "Vaikea"


def set_difficulty(level):
    """Tallentaa valitun AI-vaikeustason ja näyttää valinnan värillä."""
    global difficulty
    difficulty = level

    btn_easy.config(bg="lightgray")
    btn_med.config(bg="lightgray")
    btn_hard.config(bg="lightgray")

    if level == "easy":
        btn_easy.config(bg="lightgreen")
    elif level == "medium":
        btn_med.config(bg="orange")
    else:
        btn_hard.config(bg="red")


btn_easy = tk.Button(
    difficulty_frame,
    text="Helppo",
    width=10,
    command=lambda: set_difficulty("easy")
)
btn_easy.grid(row=0, column=0, padx=5)

btn_med = tk.Button(
    difficulty_frame,
    text="Keskitaso",
    width=10,
    command=lambda: set_difficulty("medium")
)
btn_med.grid(row=0, column=1, padx=5)

btn_hard = tk.Button(
    difficulty_frame,
    text="Vaikea",
    width=10,
    command=lambda: set_difficulty("hard")
)
btn_hard.grid(row=0, column=2, padx=5)

set_difficulty("easy")

# -------------------------
# PELIN KÄYTTÖLIITTYMÄ
# -------------------------

info_label = tk.Label(window, text="", font=("Arial", 14))
score_label = tk.Label(window, text="", font=("Arial", 12))

game_frame = tk.Frame(window)
board_frame = tk.Frame(game_frame)

# -------------------------
# INFOTEKSTIT JA PISTEET
# -------------------------


def update_info():
    """Päivittää tekstin, joka kertoo kenen vuoro on."""
    if current_player == "X":
        info_label.config(text=f"{player_x} vuoro", fg="blue")
    else:
        if vs_ai:
            info_label.config(text=f"AI ({difficulty_text()}) vuoro", fg="red")
        else:
            info_label.config(text=f"{player_o} vuoro", fg="red")


def update_score():
    """Päivittää pistetaulun käyttöliittymässä."""
    score_label.config(text=f"{player_x}: {score_x} | {player_o}: {score_o}")

# -------------------------
# VOITON TARKISTUS
# -------------------------


def check_winner(r, c):
    """Tarkistaa voittiko pelaaja viimeisellä siirrolla."""
    global winning_cells

    # Tarkistetaan neljä suuntaa: pysty, vaaka ja kaksi diagonaalia.
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dr, dc in directions:
        cells = [(r, c)]

        # Etsitään saman pelaajan merkkejä yhteen suuntaan.
        for i in range(1, koko):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < koko and 0 <= nc < koko and board[nr][nc] == current_player:
                cells.append((nr, nc))
            else:
                break

        # Etsitään saman pelaajan merkkejä vastakkaiseen suuntaan.
        for i in range(1, koko):
            nr, nc = r - dr * i, c - dc * i
            if 0 <= nr < koko and 0 <= nc < koko and board[nr][nc] == current_player:
                cells.append((nr, nc))
            else:
                break

        if len(cells) >= voitteen_pituus:
            winning_cells = cells[:voitteen_pituus]
            return True

    return False

# -------------------------
# TASAPELIN TARKISTUS
# -------------------------


def board_full():
    """Palauttaa True, jos laudalla ei ole enää tyhjiä ruutuja."""
    return all("" not in row for row in board)

# -------------------------
# PELIN PÄÄTTYMINEN
# -------------------------


def end_game(text, is_win=False):
    """Lopettaa pelin ja estää uudet siirrot."""
    info_label.config(text=text)

    if is_win:
        for r, c in winning_cells:
            buttons[r][c].config(bg="lightgreen")

    for row in buttons:
        for b in row:
            b.config(state="disabled")

# -------------------------
# TEKOÄLY
# -------------------------


def can_win(player):
    """Etsii siirron, jolla annettu pelaaja voi voittaa heti."""
    global current_player, winning_cells

    old_player = current_player
    old_winning = winning_cells.copy()

    for r in range(koko):
        for c in range(koko):
            if board[r][c] == "":
                board[r][c] = player
                current_player = player

                win = check_winner(r, c)

                # Palautetaan lauta takaisin, koska tämä oli vain testisiirto.
                board[r][c] = ""
                current_player = old_player
                winning_cells = old_winning.copy()

                if win:
                    return (r, c)

    return None


def ai_move():
    """Valitsee AI:n siirron vaikeustason mukaan."""
    empty = [(r, c) for r in range(koko) for c in range(koko) if board[r][c] == ""]

    if not empty:
        return

    if difficulty == "easy":
        click(*random.choice(empty))
        return

    # Keskitaso ja vaikea yrittävät ensin voittaa.
    win_move = can_win("O")
    if win_move:
        click(*win_move)
        return

    # Jos pelaaja X voi voittaa seuraavaksi, AI yrittää estää sen.
    block_move = can_win("X")
    if block_move:
        click(*block_move)
        return

    # Vaikea taso ottaa keskikohdan, jos se on vapaa.
    if difficulty == "hard":
        center = koko // 2
        if board[center][center] == "":
            click(center, center)
            return

    click(*random.choice(empty))

# -------------------------
# PELAAJAN SIIRTO
# -------------------------


def click(r, c):
    """Käsittelee pelaajan klikkauksen ja päivittää pelin tilanteen."""
    global current_player, score_x, score_o

    if board[r][c] != "":
        return

    board[r][c] = current_player

    if current_player == "X":
        buttons[r][c].config(text="X", fg="blue")
    else:
        buttons[r][c].config(text="O", fg="red")

    if check_winner(r, c):
        if current_player == "X":
            score_x += 1
            save_win(player_x)
            end_game(f"{player_x} voitti!", True)
        else:
            score_o += 1
            save_win(player_o)
            end_game(f"{player_o} voitti!", True)

        update_score()
        return

    if board_full():
        end_game("Tasapeli")
        return

    current_player = "O" if current_player == "X" else "X"
    update_info()

    if vs_ai and current_player == "O":
        window.after(300, ai_move)

# -------------------------
# UUSI PELI
# -------------------------


def new_game():
    """Aloittaa uuden kierroksen samoilla asetuksilla."""
    global board, current_player, winning_cells

    if not buttons:
        return

    board = [["" for _ in range(koko)] for _ in range(koko)]
    winning_cells.clear()
    current_player = "X"

    for r in range(koko):
        for c in range(koko):
            buttons[r][c].config(text="", state="normal", bg="SystemButtonFace")

    update_info()

# -------------------------
# PELILAUDAN LUONTI
# -------------------------


def create_board():
    """Luo pelilaudan valitun koon mukaan."""
    buttons.clear()

    for widget in board_frame.winfo_children():
        widget.destroy()

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
# PELIN ALOITUS
# -------------------------


def start_game():
    """Lukee käyttäjän valinnat, tarkistaa ne ja käynnistää pelin."""
    global player_x, player_o, koko, voitteen_pituus, vs_ai, board, winning_cells, score_x, score_o

    player_x = entry_x.get() or "Pelaaja X"
    player_o = entry_o.get()

    try:
        koko = int(entry_size.get())
    except ValueError:
        info_label.config(text="Pelilaudan koon pitää olla numero", fg="red")
        info_label.pack()
        return

    if koko < 3 or koko > 10:
        info_label.config(text="Pelilaudan koon pitää olla 3-10", fg="red")
        info_label.pack()
        return

    try:
        voitteen_pituus = int(entry_win.get())
    except ValueError:
        info_label.config(text="Voiton pituuden pitää olla numero", fg="red")
        info_label.pack()
        return

    if voitteen_pituus < 3:
        info_label.config(text="Voiton pituuden pitää olla vähintään 3", fg="red")
        info_label.pack()
        return

    if voitteen_pituus > koko:
        info_label.config(text="Voiton pituus ei voi olla suurempi kuin pelilauta", fg="red")
        info_label.pack()
        return

    winning_cells.clear()

    # Tyhjä O-nimi tarkoittaa, että pelataan AI:ta vastaan.
    vs_ai = (player_o == "")

    if vs_ai:
        player_o = "AI"

    score_x = get_player_wins(player_x)
    score_o = get_player_wins(player_o)

    setup_frame.pack_forget()

    info_label.pack()
    score_label.pack()

    game_frame.pack()
    board_frame.pack()

    board = [["" for _ in range(koko)] for _ in range(koko)]

    create_board()

    update_info()
    update_score()

# -------------------------
# NAPIT JA OHJELMAN KÄYNNISTYS
# -------------------------

start_button = tk.Button(setup_frame, text="Aloita peli", command=start_game)
start_button.pack(pady=10)

new_button = tk.Button(window, text="Uusi peli", command=new_game)
new_button.pack(side="bottom", pady=10)

window.mainloop()
