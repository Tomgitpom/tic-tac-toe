import tkinter as tk
from tkinter import simpledialog, messagebox

# -------------------------------
# PELAAJAT JA ASETUKSET
# -------------------------------

# Pyydetään pelaajien nimet alussa
window = tk.Tk()
window.withdraw()  # Piilotetaan ikkuna hetkeksi

pelaaja1 = simpledialog.askstring("Pelaaja 1", "Anna pelaaja X nimi:")
pelaaja2 = simpledialog.askstring("Pelaaja 2", "Anna pelaaja O nimi:")

# Jos nimet jätetty tyhjäksi, asetetaan oletusnimet
if not pelaaja1:
    pelaaja1 = "Pelaaja X"
if not pelaaja2:
    pelaaja2 = "Pelaaja O"

window.deiconify()  # Näytetään ikkuna uudelleen

# Pelilaudan koko ja voittopituus
koko = 5
voitteen_pituus = 5

# -------------------------------
# LUO PÄÄIKKUNA
# -------------------------------

window.title("Ristinolla peli")

# -------------------------------
# ALKUPERÄINEN PELAAJA JA TILAT
# -------------------------------

# Aloittava pelaaja on X
pelaaja = "X"
peli_loppu = False

# -------------------------------
# NÄYTÖN TEKSTI VUOROSTA
# -------------------------------

label = tk.Label(window, text=f"{pelaaja1} (X) vuoro", font=("Arial", 16))
label.grid(row=0, column=0, columnspan=koko)

# -------------------------------
# NAPIT PELILAUDALLE
# -------------------------------

napit = []  # Lista Button-objekteista

# -------------------------------
# FUNKTIO: VOITTAJA
# -------------------------------

def voittaja():
    """Tarkistaa onko nykyinen pelaaja voittanut"""
    # Rivit
    for r in range(koko):
        for c in range(koko - voitteen_pituus + 1):
            if all(napit[r][c+i]["text"] == pelaaja for i in range(voitteen_pituus)):
                return True
    # Sarakkeet
    for c in range(koko):
        for r in range(koko - voitteen_pituus + 1):
            if all(napit[r+i][c]["text"] == pelaaja for i in range(voitteen_pituus)):
                return True
    # Diagonaalit
    for r in range(koko - voitteen_pituus + 1):
        for c in range(koko - voitteen_pituus + 1):
            if all(napit[r+i][c+i]["text"] == pelaaja for i in range(voitteen_pituus)):
                return True
            if all(napit[r+voitteen_pituus-1-i][c+i]["text"] == pelaaja for i in range(voitteen_pituus)):
                return True
    return False

# -------------------------------
# FUNKTIO: TASAPELI
# -------------------------------

def tasapeli():
    """Jos kaikki ruudut ovat täynnä eikä voittajaa, peli on tasapeli"""
    for r in range(koko):
        for c in range(koko):
            if napit[r][c]["text"] == "":
                return False
    return True

# -------------------------------
# FUNKTIO: NAPPIN PAINALLUS
# -------------------------------

def klik(r,c):
    global pelaaja
    global peli_loppu

    if peli_loppu:
        return

    nappi = napit[r][c]
    if nappi["text"] == "":
        nappi["text"] = pelaaja

        # Värit X ja O:lle
        if pelaaja == "X":
            nappi["fg"] = "blue"
        else:
            nappi["fg"] = "red"

        # Tarkista voittaja
        if voittaja():
            if pelaaja == "X":
                label["text"] = f"{pelaaja1} (X) voitti!"
            else:
                label["text"] = f"{pelaaja2} (O) voitti!"
            peli_loppu = True
        # Tarkista tasapeli
        elif tasapeli():
            label["text"] = "Tasapeli!"
            peli_loppu = True
        else:
            # Vaihda pelaajaa
            if pelaaja == "X":
                pelaaja = "O"
                label["text"] = f"{pelaaja2} (O) vuoro"
            else:
                pelaaja = "X"
                label["text"] = f"{pelaaja1} (X) vuoro"

# -------------------------------
# FUNKTIO: RESTART
# -------------------------------

def restart():
    """Tyhjentää kaikki ruudut ja aloittaa uuden pelin"""
    global pelaaja
    global peli_loppu
    pelaaja = "X"
    peli_loppu = False
    for r in range(koko):
        for c in range(koko):
            napit[r][c]["text"] = ""
            napit[r][c]["fg"] = "black"
    label["text"] = f"{pelaaja1} (X) vuoro"

# -------------------------------
# LUO PELILAUTA
# -------------------------------

for r in range(koko):
    rivi = []
    for c in range(koko):
        nappi = tk.Button(
            window,
            text="",
            width=6,
            height=3,
            font=("Arial", 20),
            command=lambda r=r, c=c: klik(r,c)
        )
        nappi.grid(row=r+1, column=c)
        rivi.append(nappi)
    napit.append(rivi)

# -------------------------------
# LUO RESTART NAPPI
# -------------------------------

restart_nappi = tk.Button(
    window,
    text="Restart peli",
    command=restart,
    font=("Arial", 16)
)
restart_nappi.grid(row=koko+1, column=0, columnspan=koko)

# -------------------------------
# KÄYNNISTÄ IKKUNA
# -------------------------------

window.mainloop()