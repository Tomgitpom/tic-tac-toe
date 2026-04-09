import tkinter as tk

# luodaan ikkuna
window = tk.Tk()
window.title("Ristinolla peli")

# pelilaudan koko (UUSI)
koko = 5

# aloituspelaaja
pelaaja = "X"

# muuttuja joka kertoo onko peli loppunut
peli_loppu = False

# label joka näyttää kenen vuoro on
label = tk.Label(window, text="Pelaaja X vuoro")
label.grid(row=0, column=0, columnspan=koko)

# lista johon tallennan kaikki napit
napit = []


# funktio joka tarkistaa voittajan (UUSI yksinkertainen versio)
def voittaja():

    # rivit
    for r in range(koko):
        sama = True
        merkki = napit[r][0]["text"]

        if merkki == "":
            sama = False

        for c in range(koko):
            if napit[r][c]["text"] != merkki:
                sama = False

        if sama:
            return True

    # sarakkeet
    for c in range(koko):
        sama = True
        merkki = napit[0][c]["text"]

        if merkki == "":
            sama = False

        for r in range(koko):
            if napit[r][c]["text"] != merkki:
                sama = False

        if sama:
            return True

    return False


# tasapeli
def tasapeli():

    for r in range(koko):
        for c in range(koko):

            if napit[r][c]["text"] == "":
                return False

    return True


# funktio joka tapahtuu kun nappia painetaan
def klik(r,c):

    global pelaaja
    global peli_loppu

    if peli_loppu == True:
        return

    nappi = napit[r][c]

    if nappi["text"] == "":

        nappi["text"] = pelaaja

        # värit (UUSI)
        if pelaaja == "X":
            nappi["fg"] = "blue"
        else:
            nappi["fg"] = "red"

        if voittaja():

            label["text"] = "Pelaaja " + pelaaja + " voitti"
            peli_loppu = True

        elif tasapeli():

            label["text"] = "Tasapeli"
            peli_loppu = True

        else:

            if pelaaja == "X":
                pelaaja = "O"
            else:
                pelaaja = "X"

            label["text"] = "Pelaaja " + pelaaja + " vuoro"


# restart funktio
def restart():

    global pelaaja
    global peli_loppu

    pelaaja = "X"
    peli_loppu = False

    for r in range(koko):
        for c in range(koko):

            napit[r][c]["text"] = ""

    label["text"] = "Pelaaja X vuoro"


# pelilaudan luominen
for r in range(koko):

    rivi = []

    for c in range(koko):

        nappi = tk.Button(
            window,
            text="",
            width=6,
            height=3,
            font=("Arial",20),
            command=lambda r=r,c=c: klik(r,c)
        )

        nappi.grid(row=r+1, column=c)

        rivi.append(nappi)

    napit.append(rivi)


# restart nappi
restart_nappi = tk.Button(
    window,
    text="Restart peli",
    command=restart
)

restart_nappi.grid(row=koko+1, column=0, columnspan=koko)


window.mainloop()