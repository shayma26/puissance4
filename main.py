#************************************************************************************************************
#*                         Puissance 4                                                                      *
#*                         Lamouchi Wissal et Trad Shayma                                                   *
#************************************************************************************************************

import numpy as np  # pour initialiser la matrice a 0
from tkinter import *

j1gagnant = False
j2gagnant = False
symbol = 1
tour = 1
cercles = []


class Joueur():

    def __init__(self, nom):
        self.nom = nom


class Jeu():

    def __init__(self, nomJoueur1, nomJoueur2):
        self.grille = np.zeros((6, 7))
        joueur1 = Joueur(nomJoueur1)
        joueur2 = Joueur(nomJoueur2)
        self.joueurs = (joueur1, joueur2)

    def __str__(self):
        s = ''
        for i in range(6):
            for j in range(7):
                s += " " + str(int(self.grille[i][j])) + " "
            s += "\n"
        return s

    def ligne_ajout(self, c): #retourne l'indice du ligne disponible de la colonne c, sinon il retourne -1
        l = 5
        while self.grille[l][c] != 0 and l >= 0:
            l -= 1
        return l

    def verif(self, c): #retourne si la case est vide
        if c < 0 or c > 6:
            return False
        return self.grille[self.ligne_ajout(c)][c] == 0

    def ajout(self, symbol, c): #ajouter le symbol (1 ou 2) a la case disponible
        if not self.verif(c):
            print("veuillez choisir une autre colonne")
            return False, -1
        l = self.ligne_ajout(c)
        self.grille[l][c] = symbol
        print(self)
        return True, l

    def nb_pions_direction(self, ligne, colonne, x, y): #compter les symboles alignées horizontalement, verticalement et en diagonale
        symbol = self.grille[ligne][colonne]
        res = 1
        # comptabiliser les pions dans la direction (x,y)
        lig, col = ligne + y, colonne + x
        if lig in range(6) and col in range(7):
            while self.grille[lig][col] == symbol:
                res += 1
                lig, col = lig + y, col + x
                if lig not in range(6) or col not in range(7):
                    break

        # Comptabiliser les pions dans la direction opposée(-x,-y)
        lig, col = ligne - y, colonne - x
        if lig in range(6) and col in range(7):
            while self.grille[lig][col] == symbol:
                res += 1
                lig, col = lig - y, col - x
                if lig not in range(6) or col not in range(7):
                    break
        return res

    def gagner(self, ligne, colonne): # retourne si le joueur courant a gagné ou non
        if self.nb_pions_direction(ligne, colonne, 1, 1) >= 4 or self.nb_pions_direction(ligne, colonne, 1,
                                                                                         -1) >= 4 or self.nb_pions_direction(
            ligne, colonne, 0, 1) >= 4 or self.nb_pions_direction(ligne, colonne, 1, 0) >= 4:
            return True
        else:
            return False

    def jouer(self, indColonne): #verifier l'indice du colonne entré et appeler les méthodes ajout et gagner
        global tour, symbol, message, affiche_message, j1gagnant, j2gagnant

        if tour < 21 and j1gagnant is False and j2gagnant is False:
            print("tour N°" + str(tour) + "\n")
            if len(indColonne) == 0:
                message = "L'indice ne doit pas être-vide .\n Veuillez choisir un indice entre 0 et 6"
            elif not str(indColonne).isdigit():
                message = "L'indice doit-être un entier .\n Veuillez choisir un indice entre 0 et 6"
            else:
                colonne = int(indColonne)
                if not (colonne in range(7)):
                    message = " L'indice de la colonne est faux .\n Veuillez choisir un indice entre 0 et 6"
                else:
                    ligne = self.ligne_ajout(colonne)
                    if ligne == -1:  # si la case choisie n'est pas vide refaire la saisie des indices
                        message = "\n La colonne choisie n'est pas libre ,\n Veuillez choisir une autre colonne  "
                    else:
                        self.ajout(symbol, colonne)  # mettre le numero de joueur dans la case choisie
                        if symbol == 1:
                            cercles[ligne][colonne] = creation_circle(50 + colonne * 70, 50 + ligne * 70, 28, monCanvas,
                                                                      "#ffa801")
                            if self.gagner(ligne, colonne):
                                print(str(self.joueurs[0].nom) + " a gagnée !!")
                                j1gagnant = True

                            else:
                                symbol = 2
                                message = "C'est le tour de " + str(self.joueurs[1].nom)
                        else:
                            cercles[ligne][colonne] = creation_circle(50 + colonne * 70, 50 + ligne * 70, 28, monCanvas,
                                                                      "#ff3f34")
                            if self.gagner(ligne, colonne):
                                print(str(self.joueurs[1].nom) + " a gagnée !!")
                                j2gagnant = True

                            else:
                                symbol = 1
                                message = "C'est le tour de " + str(self.joueurs[0].nom)
                                tour += 1

        else:
            if j1gagnant is True:
                message = str(self.joueurs[0].nom) + " a gagnée !!"
            elif j2gagnant is True:
                message = str(self.joueurs[1].nom) + " a gagnée !!"
            else:
                message = " c'était une amusante partie ! bravo les deux!! "

        affiche_message.pack_forget()
        affiche_message = Label(frame, text=message, bg='#eeeeee', font=("Courrier", 18, "bold"), fg="#a50a08")
        affiche_message.pack()


def creer_fenetre1():
    # creer la fenetre de chargement des noms
    fenetre1 = Tk()
    fenetre1.iconbitmap("myIcon.ico")
    fenetre1.title("Entrez vos noms")

    # creer les titre
    label_joueur1 = Label(fenetre1, text="Joueur 1 ", font=("Helvetica", 10))
    label_joueur2 = Label(fenetre1, text="Joueur 2 ", font=("Helvetica", 10))
    label_joueur1.grid(row=0, column=0, sticky=E, padx=10, pady=10)
    label_joueur2.grid(row=1, column=0, sticky=E, padx=10, pady=10)

    # creer les champs
    entrer_joueur1 = Entry(fenetre1)
    entrer_joueur2 = Entry(fenetre1)
    entrer_joueur1.grid(row=0, column=1, padx=15, pady=10)
    entrer_joueur2.grid(row=1, column=1, padx=15, pady=10)

    # creer un bouton pour lancer le jeu
    bouton_valider = Button(fenetre1, text="OK", width=10,
                            command=lambda: get_names(entrer_joueur1.get(), entrer_joueur2.get()))
    bouton_valider.grid(row=2, columnspan=2, padx=5, pady=(5, 15))

    # lancer la fenetre 1
    fenetre1.mainloop()


def get_names(nom1, nom2):
    global nom_joueur1, nom_joueur2
    nom_joueur1 += nom1
    if nom1 == '':
        nom_joueur1 += "Joueur 1"
    nom_joueur2 += nom2
    if nom2 == '':
        nom_joueur2 += "Joueur 2"
    creer_fenetre2()


def creation_circle(x, y, r, nomCanvas, couleur):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return nomCanvas.create_oval(x0, y0, x1, y1, outline=couleur, fill=couleur)


def creer_fenetre2():
    global nom_joueur1, nom_joueur2, monCanvas, affiche_message, frame, partie, message, fenetre1
    partie = Jeu(nom_joueur1, nom_joueur2)  # initialiser le jeu

    # creer la fenetre principale de jeu
    fenetre2 = Tk()
    fenetre2.geometry("700x700")
    fenetre2.iconbitmap("myIcon.ico")
    fenetre2.title("Puissance 4")

    monCanvas = Canvas(fenetre2, width=520, height=450, bg="#3c40c6")
    monCanvas.pack(side=TOP, padx=5, pady=5)
    for i in range(6):
        x = []
        for j in range(7):
            x.append(creation_circle(50 + j * 70, 50 + 70 * i, 30, monCanvas, "#d2dae2"))
        cercles.append(x)

    frame = Frame(fenetre2)
    entrer_colonne = Entry(frame)
    frame.pack()
    entrer_colonne.pack()
    bouton_jouer = Button(frame, text="Jouer", command=lambda: partie.jouer(entrer_colonne.get())).pack()
    message = "C'est le tour de " + str(partie.joueurs[0].nom)
    affiche_message = Label(frame, text=message, bg='#eeeeee', font=("Courrier", 18, "bold"), fg="#a50a08")
    affiche_message.pack()
    fenetre2.mainloop()


if __name__ == '__main__':
    nom_joueur1, nom_joueur2 = '', ''
    creer_fenetre1()
