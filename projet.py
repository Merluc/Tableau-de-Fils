import tkinter as Tk
from tkinter import colorchooser
from PIL import Image, ImageTk
from tkinter import ttk
import math
import wckToolTips

liens = {}

"""
Fonction pour cacher la grille
"""

def hide_gr(grille, fl_grille):
    # Si le flag est actif
    if fl_grille[0]:
        # On parcourt la liste avec toute les objets de la grille
        for id in grille:
            # On cache tout ces objets
            canvas.itemconfigure(id, state = 'hidden')
            # On passe le bouton en état enfocé
            bt_grille.config(relief = 'sunken')
        # On désactive le flag
        fl_grille[0] = False
    # Sinon le flag est désactivé
    else:
        # On parcourt la liste avec toute les objets de la grille
        for id in grille:
            # On repasse tout ces objets en état normal
            canvas.itemconfigure(id, state = 'normal')
            # On repasse le bouton en état normal
            bt_grille.config(relief='raised')
        # On active le flag
        fl_grille[0] = True

######################################################

"""
Fonction pour cacher les clous
"""

def hide_cl(fl_clou):
    # On récupère dans une liste les clous
    L = list(canvas.find_withtag("clou"))
    # Si le flag est actif
    if fl_clou[0]:
        # On parcourt tout les objets de la liste
        for id in L:
            # On cache tout ces objets
            canvas.itemconfigure(id, state = 'hidden')
            # On passe le bouton en état enfoncé
            bt_hideclou.config(relief='sunken')
        # On désactive le flag
        fl_clou[0] = False
    # Sinon le flag est désactivé
    else:
        # On parcourt tout les objets de la liste
        for id in L:
            # On repasse tout ces objets en état normal
            canvas.itemconfigure(id, state = 'normal')
            # On repasse le bouton en état  normal
            bt_hideclou.config(relief='raised')
        # On active le flag
        fl_clou[0] = True

######################################################

"""
Fonction qui retourne les coordonnés de deux objets (clou)
"""

def coord_cl(p1, p2):
    # On récupère les coordonnés du premier clou
    x1, y1, x2, y2 = canvas.coords(p1)
    # On calcul le centre du clou en x et y
    x1 = (x1 + x2) / 2
    y1 = (y1 + y2) / 2
    # On récupère les coordonnés du deuxième clou
    x2, y2, x3, y3 = canvas.coords(p2)
    # On calcul le centre du clou en x et y
    x2 = (x2 + x3) / 2
    y2 = (y2 + y3) / 2
    # On retourne les coordonnées des deux clous
    return(x1, y1, x2, y2)

######################################################

"""
Fonction qui relie tout les points sélectionnés entre eux
"""

def relier_tout():
    # On récupère dans une liste les objets sélectionnés
    L = list(canvas.find_withtag('grow'))
    i = 0
    # On parcourt l'intégralité de la liste
    while i < len(L):
        # On vérifie avec les tags si c'est un fil
        if canvas.gettags(L[i])[0] == 'fil':
            # Si oui on l'enlève de la liste
            L.pop(i)
        else:
            # Sinon on incrémente
            i += 1
    # On reparcourt la liste sans fils
    for i in range(len(L)):
        # Pour chaque éléments on parcourt le reste de la liste
        for j in range(i + 1, len(L)):
            # On relie chaque éléments i à tout les autres
            relier_2p(L[i], L[j])

###########################################################################

"""
Fonction qui relie les figures qui n'ont pas leurs arrêtes de base
"""

def relier_fig(event):
    # On récupère l'objet pointé par l'utilisateur
    obj = event.widget.find_closest(event.x, event.y)
    # On récupère les tags de cet objet
    tag = canvas.gettags(obj)
    # On vérifie grace au tag si c'est bien un clou
    if tag[0] != 'clou':
        return(1)
    # On appelle creer_ar avec les tags: nombre de côtés, numéro de la figure
    creer_ar(tag[-2], tag[-3])

###########################################################################

"""
Fonction qui créé les arrêtes d'une figure
"""

def creer_ar(tag1, tag2):
    # On récupère dans une liste les objets avec le tag1
    L1 = list(canvas.find_withtag(tag1))
    i = 0
    # On parcourt l'intégralité de la liste
    while i < len(L1):
        # On vérifie avec les tags si c'est un fil
        if canvas.gettags(L1[i])[0] == 'fil':
            # Si oui on l'enlève de la liste
            L1.pop(i)
        else:
            # Sinon on incrémente
            i += 1
    # On récupère la même liste
    L2 = L1
    i = 0
    j = 1
    n = 0
    # On continue tant qu'on à pas fait le nombre de côtés souhaité
    while n < (int(tag2)-1):
        # Si le clou fait partit de la figure
        if (canvas.gettags(L1[i])[2] == tag1):
            # On parcourt tant qu'on à pas un deuxième clou de la figure
            while (canvas.gettags(L2[j])[2] != tag1):
                j += 1
            # On relie ces deux clous
            relier_2p(L1[i], L2[j], tag1)
            # On incrémente
            n += 1
            # On refait le même parcours pour le clou suivant de la figure
            i = j
            j += 1
    # On relie le dernier clou trouvé avec le premier pour fermer la figure
    relier_2p(L1[0], L2[i], tag1)

#####################################################################

"""
Fonction que relie deux points
"""

def relier_2p(p1, p2, figure = ""):
    global cb_epaisseur
    # On vérifie si les deux clous ne sont pas déjà reliés
    if p2 in liens[p1]:
        pass
    # Sinon
    else:
        # On récupère les coordonnées des deux clous
        x1, y1, x2, y2 = coord_cl(p1, p2)
        # On créé un fil entre les deux clous
        ligne = canvas.create_line(x1, y1, x2, y2,
                                   width = int(cb_epaisseur.get()),
                                   fill = color,
                                   tags = ('fil', str(p1), str(p2), figure))
        # On indique la liaison qu'on vient de faire
        liens[p1][p2] = ligne
        liens[p2][p1] = ligne

##############################################################

"""
Fonction de sélection d'une arrête pour y mettre des clous
"""

def select_ar(event):
    global f
    # On récupère l'objet pointé
    obj = event.widget.find_closest(event.x, event.y)
    # On vérifie si l'objet est bien un fil
    if canvas.gettags(obj)[0] != 'fil':
        return (1)
    else:
        # On vérifie qu'il ne fait pas partie de la grille
        if canvas.gettags(obj)[1] == 'grille':
            return(1)
        # On récupère les coordonnées du fil
        x1, y1, x2, y2 = canvas.coords(obj)
        # On appelle creer_arcl avec les coordonnées de l'arrête
        creer_arcl(x1, y1, x2, y2, canvas.gettags(obj)[-2])

##############################################################

"""
Fonction qui créé les clous sur une arrête
"""
g = 0 #global

def creer_arcl(x1, y1, x2, y2, figure="", figure2=""):
    global g, nbligne
    # On incrémente le compteur de groupe
    g += 1
    # On récupère le nombre de clous souhaité
    nb = int(nbligne.get())
    # On calcul la distance qui sépare les deux clous en x et on la divise par
    # le nomre de clou souhaités
    if x2 > x1:
        xtmp = (x2 - x1)/(nb + 1)
    else:
        xtmp = -(x1 - x2)/(nb + 1)
    # Et en y
    if y2 > y1:
        ytmp = (y2 - y1) / (nb + 1)
    else:
        ytmp = -(y1 - y2) / (nb + 1)
    # On part du premier clou et on se décale
    x1 += xtmp
    y1 += ytmp
    # Tant qu'on à pas le nombre de clou souhaités
    for i in range (nb):
        # On ccréé un clou aux coordonnées actuelles
        obj = creer_cl2(x1 , y1, "g"+str(g), figure2)
        # Puis on décale
        x1 += xtmp
        y1 += ytmp
        # On ajoute le tag souhaité
        canvas.addtag_withtag(figure, "g"+str(g))

##############################################################

"""
Fonction qui créé un arc de fils
"""

def construction(g1, g2):
    # On récupère dans une liste les clous avec le premier tag
    L1 = list(canvas.find_withtag(g1))
    # On récupère dans une liste les clous avec le deuxième tag
    L2 = list(canvas.find_withtag(g2))
    x1, y1, x2, y2 = coord_cl(L1[0], L1[1])
    x3, y3, x4, y4 = coord_cl(L2[0], L2[-1])
    # if abs(x1 - x2) < abs(y1 - y2):
    #     if (abs(x1 - x3) < abs(x1 - x4)):
    #         print( abs(x1 - x2) , abs(y1 - y2))
    #         for i in range(len(L1)):
    #             print("normal x")
    #             relier_2p(L1[i], L2[i], canvas)
    #     else:
    #         for i in range(len(L1)):
    #             print("bizarre x")
    #             relier_2p(L1[i], L2[-(i+1)], canvas)
    # elif abs(x1 - x2) > abs(y1 - y2):
    #     if (abs(y1 - y3) < abs(y1 - y4)):
    #         for i in range(len(L1)):
    #             print("normal y")
    #             relier_2p(L1[i], L2[i], canvas)
    #     else:
    #         for i in range(len(L1)):
    #             print("bizarre y")
    #             relier_2p(L1[i], L2[-(i+1)], canvas)
    #if (distance_cl(x1, y1, x3, x3) > distance_cl(x1, y1, x4, y4)):
    # if (distance_cl(x1, y1, x2, y2) > distance_cl(x3, y3, x4, y4) or distance_cl(x1, y1, x2, y2) < distance_cl(x3, y3, x4, y4)):
    if g1[1] > g2[1]:
        for i in range(len(L1)):
            print("bizarre")
            relier_2p(L1[i], L2[-(i+1)], canvas)
    else:
        for i in range(len(L1)):
            print("normal")
            relier_2p(L1[i], L2[i])

#############################################################################

"""
Fonction qui calcule la distance entre deux clous
"""

def distance_cl(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#############################################################################

"""
Fonction qui fait tourner les objets sélectionnés
"""

def rotation_f():
    # On récupère les objets sélectionnés
    L = list(canvas.find_withtag("grow"))
    # On définit l'angle de rotation
    angle = math.pi/12
    i = 0
    # On parcourt l'intégralité de la liste
    while i < len(L):
        # On vérifie avec les tags si c'est un fil
        if canvas.gettags(L[i])[0] == 'fil':
            # Si oui on l'enlève de la liste
            L.pop(i)
        else:
            # Sinon on incrémente
            i += 1
    x = 0
    y = 0
    # On parcourt l'intégralité de la liste
    for obj in L:
        # On récupère les coordonnés du clou
        x1, y1, x2, y2 = canvas.coords(obj)
        # On ajoute les x et les y de tout les clous
        x += x1 + x2
        y += y1 + y2
    # On divise par le nombre de clous*2 car on utilise deux coordonnées
    # pour chaque clou. On obtient donc le centre de la figure
    x /= (len(L) * 2)
    y /= (len(L) * 2)
    # On parcourt l'intégralité de la liste
    for obj in L:
        # On récupère les coordonnés du clou
        x1, y1, x2, y2 = canvas.coords(obj)
        # On calcule les coordonnées du clou par rapport au centre
        x3 = (x1 + x2) / 2 - x
        y3 = (y1 + y2) / 2 - y
        # On calcule les coordonnées du point en appliquant la rotation
        rotation_x = x3 * math.cos(angle) + y3 * math.sin(angle) + x
        rotation_y = y3 * math.cos(angle) - x3 * math.sin(angle) + y
        # On donne à l'objet ses nouvelles coordonnées
        canvas.coords(obj, rotation_x-3, rotation_y-3, rotation_x+3, rotation_y+3)
        # On parcourt la liste des liens de l'objet
        for id in liens[obj]:
            # On récupère les coordonnées du fil
            x1, y1, x2, y2 = canvas.coords(id)
            # On calcul ses coordonnées
            x1 = (x1 + x2) / 2
            y1 = (y1 + y2) / 2
            # On modifie les coordonnées du fil en lui donnant la nouvelle
            # valeur du clou
            canvas.coords(liens[obj][id], rotation_x, rotation_y, x1, y1)

#############################################################################

"""
Fonction qui fait bouger les objets sélectionnés
"""

def mouvement_f(direction):
    # On récupère les éléments sélectionnés
    L = list(canvas.find_withtag("grow"))
    i = 0
    # On parcourt l'intégralité de la liste
    while i < len(L):
        # On vérifie avec les tags si c'est un fil
        if canvas.gettags(L[i])[0] == 'fil':
            # Si oui on l'enlève de la liste
            L.pop(i)
        else:
            # Sinon on incrémente
            i += 1
    # On parcourt l'intégralité de la liste
    for obj in L:
        # On récupère les coordonnées de l'objet
        x1, y1, x2, y2 = canvas.coords(obj)
        # On cherche la direction voulue et on modifie les coordonnées
        # en fonction
        if direction == "u":
            y1 -= 5
            y2 -= 5
        elif direction == "d":
            y1 += 5
            y2 += 5
        elif direction == "r":
            x1 += 5
            x2 += 5
        elif direction == "l":
            x1 -= 5
            x2 -= 5
        # On donne à l'objet ses nouvelles coordonnées
        canvas.coords(obj, x1 , y1, x2, y2)
        # On parcourt la liste des liens de l'objet
        for id in liens[obj]:
            # On récupère les coordonnées du fil
            x3, y3, x4, y4 = canvas.coords(id)
            # On calcul ses coordonnées
            x3 = (x3 + x4) / 2
            y3 = (y3 + y4) / 2
            # On modifie les coordonnées du fil en lui donnant la nouvelle
            # valeur du clou
            canvas.coords(liens[obj][id], x1+3, y1+3, x3, y3)

#############################################################################

"""
Fonction qui créée un clou en fonction du pointeur
"""

def creer_cl(event):
    global color, vzoom
    # On calcule l'épaisseur du clou en fonction du zoom
    dif = 3 * vzoom
    # On créé le clou en fonction du pointeur
    obj = canvas.create_oval(str(event.x+dif), str(event.y+dif),
                             str(event.x-dif), str(event.y-dif),
                             fill = color, tags = ("clou"))
    # On intialise sa liste de lien
    liens[obj] = {}

#############################################################################

"""
Fonction qui créée un clou en fonction de coordonnées
"""

def creer_cl2(x, y, t = "", t1=""):
    global color, vzoom
    # On calcule l'épaisseur du clou en fonction du zoom
    dif = 3 * vzoom
    # On créé le clou en fonction des coordonnées
    obj = canvas.create_oval(str(x+dif), str(y+dif), str(x-dif), str(y-dif),
                             fill = color, tags = ("clou", t, t1))
    # On initialise sa liste de liens
    liens[obj] = {}
    # On retourne l'objet
    return obj


# def creerCercle(event):
#     """
#     Hehu
#     """
#     global f, nbcercle, lig, rel
#     f += 1
#     nb = nbcercle.get()
#     angle = 0
#     L = []
#     for i in range(nb):
#         x = event.x + 150 * math.cos(angle)
#         y = event.y + 150 * math.sin(angle) #* (-1)
#         print(angle, i)
#         obj = creer_cl2(x, y, str(nbcercle.get(), "f"+str(f)))
#         print(canvas.coords(obj))
#         L.append(obj)
#         angle += math.pi*2/nb
#         print("test","f"+str(f), (str(nbcercle.get())))
#         if i > 0:
#             if lig.get():
#                 x1, y1, x2, y2 = coord_cl(L[i], L[i - 1])
#                 creer_arcl(x1, y1, x2, y2, "f"+str(f), str(nbcercle.get()))
#             if rel.get():
#                 relier_2p(L[i], L[i - 1])
#     if lig.get():
#         x1, y1, x2, y2 = coord_cl(L[0], L[-1])
#         creer_arcl(x1, y1, x2, y2, "f"+str(f), str(nbcercle.get()))
#     if rel.get():
#         relier_2p(L[0], L[-1])

#############################################################################

"""
Fonction qui appelle la création d'un polygone
"""
f = 0 # globale

def creer_poly(event):
    global nbcercle
    # On appelle le polygone en fonction du curseur et du nombre de côtés
    creer_fig(event.x, event.y, math.pi*2, int(nbcercle.get()))

#############################################################################

"""
Fonction qui appelle la création d'un angle avec arc de fils
"""

def creer_angle(event):
        global f, nblarg, nbhaut, g, vzoom
        # On incrémente le compteur de figure
        f += 1
        # On récupère la hauteur et largeur souhaitée en fonction du zoom
        larg = int(nblarg.get()) * vzoom
        haut = int(nbhaut.get()) * vzoom
        L = []
        # On creer un clou sur le curseur
        obj = creer_cl2(event.x, event.y, 3, "f"+str(f))
        # On ajoute l'objet a notre liste
        L.append(obj)
        # On calcule les coordonnés du point placé à l'horizontal
        x1 = event.x + larg * math.cos(math.pi)
        y1 = event.y + haut  * math.sin(math.pi)
        # On créé le clou horizontal
        obj = creer_cl2(x1, y1, 3, "f"+str(f))
        # On ajoute l'objet a notre liste
        L.append(obj)
        # On calcule les coordonnés du point placé à la vertical
        x1 = event.x + larg * math.cos(4.712)
        y1 = event.y + haut * math.sin(4.712)
        # On créé le clou vertical
        obj = creer_cl2(x1, y1, 3, "f"+str(f))
        # On ajoute l'objet a notre liste
        L.append(obj)
        t = []
        # On parcourt pour creer les deux côtés
        for i in range (2):
            # On récupère les coordonnées de deux clous
            x1, y1, x2, y2 = coord_cl(L[i], L[i - 1])
            # On relie les deux clous
            relier_2p(L[i], L[i - 1])
            # On créé les clous sur l'arrête
            creer_arcl(x1, y1, x2, y2, "f"+str(f), 3)
            # On garde en mémoire le numéro du groupe
            t.append(g)
        # On créé l'arc de fils sur les groupes mémorisés
        construction("g" + str(t[0]), "g" + str(t[1]))

#############################################################################

"""
Fonction qui appelle la création d'un demi-cercle
"""

def creer_demic(event):
    global nbcercle
    # On créé le demi-cercle en fonction du curseur et du nombre de côtés voulus
    creer_fig(event.x, event.y, math.pi, int(nbcercle.get()), 1)

#############################################################################

"""
Fonction qui créé les différents figures
"""

def creer_fig(x, y, dim, nbc, dif=0):
    global f, lig, rel, nblarg, nbhaut, vzoom
    # On incrémente le compteur de figure
    f += 1
    # On récupère la hauteur et largeur souhaitée en fonction du zoom
    larg = int(nblarg.get()) * vzoom
    haut = int(nbhaut.get()) * vzoom
    L = []
    angle = 0
    # Tans qu'on a pas le nombre de côtés souhaités
    for i in range(nbc):
        # On calcule les coordonnées en fonction de l'angle
        x1 = x + larg * math.cos(angle)
        y1 = y + haut * math.sin(angle)
        # On créé le clou
        obj = creer_cl2(x1, y1, str(nbc), "f"+str(f))
        # On ajoute l'objet à notre liste
        L.append(obj)
        # On augmente l'angle en fonction du nombre de côtés voulus
        angle += dim/(nbc-dif)
        if i > 0:
            # On vérifie si on souhaite créer les arrêtes de points
            if lig.get():
                # On calcule les coordonnées des deux points
                x1, y1, x2, y2 = coord_cl(L[i], L[i - 1])
                # On créé l'arrête de points
                creer_arcl(x1, y1, x2, y2, "f"+str(f), str(nbc))
            # On vérifie si on souhaite créer les arrêtes
            if rel.get():
                # On céé l'arrête
                relier_2p(L[i], L[i - 1])
    # On vérifie si on souhaite créer les arrêtes de points et que on créé
    # un polygone fermé
    if lig.get() and dif == 0:
        # On calcule les coordonnées des deux points
        x1, y1, x2, y2 = coord_cl(L[0], L[-1])
        # On créé l'arrête de points entre le premier et dernier clou
        creer_arcl(x1, y1, x2, y2, "f"+str(f), str(nbc))
    # On vérifie si on souhaite créer les arrêtes et que on créé
    # un polygone fermé
    if rel.get() and dif == 0:
        # On céé l'arrête entre les deux points
        relier_2p(L[0], L[-1])

#############################################################################

"""
Fonction qui appelle la création des arcs de fils
"""

fl_arc = False #global
def select_arc(event):
    global fl_arc, t1, t2, tmp
    # Si le flag est inactif
    if not fl_arc:
        # On récupère l'objet pointé par le curseur
        obj = event.widget.find_closest(event.x, event.y)
        # On récupère les tags de cet objet
        t1 = canvas.gettags(obj)
        # On vérifie si c'est un clou
        if t1[0] != "clou":
            # Si non on ignore
            return(1)
        # On marque à l'aide d'un tag l'objet sélectionné
        canvas.addtag_closest("sel", event.x, event.y)
        # On mémorise sa couleur
        tmp = canvas.itemcget("sel", "fill")
        # On le fait apparaitre en le marquant en rouge
        canvas.itemconfigure("sel", fill ="red")
    # Si le flag est actif
    else:
        # On récupère l'objet pointé par le curseur
        obj = event.widget.find_closest(event.x, event.y)
        # On récupère les tags de cet objet
        t2 = canvas.gettags(obj)
        # On vérifie si c'est un clou
        if t2[0] != "clou":
            # Si non on ignore
            return(1)
        # On créé l'arc de fils sur les groupes des deux objets sélectionnés
        construction(t1[1], t2[1])
        # On rend sa couleur à l'objet marqué
        canvas.itemconfigure("sel", fill=tmp)
        # On enlève les tags des objets sélectionnés
        canvas.dtag("sel", "sel")
    # On active/désactive le flag
    fl_arc = not fl_arc

##########################################################################

"""
Fonction qui créé un fil
"""

fl_fil = False #global
def creer_fil(event):
    global fl_fil, t1, t2, tmp
    # Si le flag est inactif
    if not fl_fil:
        # On récupère l'objet pointé par le curseur
        obj = event.widget.find_closest(event.x, event.y)
        # On récupère ses tags
        t1 = canvas.gettags(obj)
        # On vérifie si c'est un clou
        if t1[0] != "clou":
            # Si non on ignore
            return(1)
        # On marque à l'aide d'un tag l'objet sélectionné
        canvas.addtag_closest("sel", event.x, event.y)
        # On mémorise sa couleur
        tmp = canvas.itemcget("sel", "fill")
        # On le fait apparaitre en le marquant en rouge
        canvas.itemconfigure("sel", fill ="red")
    # Si le flag est actif
    else:
        # On récupère l'objet pointé par le curseur
        obj = event.widget.find_closest(event.x, event.y)
        # On récupère ses tags
        t2 = canvas.gettags(obj)
        # On vérifie si c'est un clou
        if t2[0] != "clou":
            # Si non on ignore
            return(1)
        # On marque à l'aide d'un tag l'objet sélectionné
        canvas.addtag_closest("sel", event.x, event.y)
        # On récupère dans une liste les objets sélectionnés
        L = list(canvas.find_withtag("sel"))
        # On relie les deux clous sélectionnés
        relier_2p(L[0], L[1])
        # On rend sa couleur à l'objet marqué
        canvas.itemconfigure("sel", fill = tmp)
        # On enlève les tags des objets sélectionnés
        canvas.dtag("sel", "sel")
    # On active/désactive le flag
    fl_fil = not fl_fil
################################################################################

"""
Fonction qui gère les binding
"""

def swap_bind(fonc):
    global current
    # On unbind les boutons
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    # On redonne du relief au dernier bouton utilisé
    current.config(relief = 'raised')
    # On cherche le bouton qui à été utilisé
    if fonc == "c":
        # On stock le dernier bouton utilisé
        current = bt_clou
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", creer_cl)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'dot')

    elif fonc == "s":
        # On stock le dernier bouton utilisé
        current = bt_gomme
        # On supprime les objets sélectionnés
        canvas.delete("grow")
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", sup)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'crosshair')


    elif fonc == "t":
        #x1 = event.x
        #y1 = event.y

        #canvas.unbind("<Button-1>")
        current = bt_select
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", selection)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'tcross')
    elif fonc == "r":
        # On stock le dernier bouton utilisé
        current = bt_cercle
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", creer_poly)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    elif fonc == "d":
        # On stock le dernier bouton utilisé
        current = defaut
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", select_arc)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    elif fonc == "o":
        # On stock le dernier bouton utilisé
        current = bt_fil
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", creer_fil)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    elif fonc == "u":
        # On stock le dernier bouton utilisé
        current = bt_relun
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", relier_fig)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    elif fonc == "p":
        # On stock le dernier bouton utilisé
        current = bt_ligne
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", select_ar)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    elif fonc == "a":
        # On stock le dernier bouton utilisé
        current = bt_angle
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", creer_angle)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')


    elif fonc == "arc":
        # On stock le dernier bouton utilisé
        current = bt_arc
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", creer_demic)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    elif fonc == "col":
        # On stock le dernier bouton utilisé
        current = bt_colorier
        # On colorie tout les items sélectionnés
        canvas.itemconfigure("grow", fill =color)
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", colorier)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'pencil')

    elif fonc == "z":
        # On stock le dernier bouton utilisé
        current = zoom
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", zoomer)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'target')

    elif fonc == "dz":
        # On stock le dernier bouton utilisé
        current = dezoom
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", dezoomer)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'target')

    elif fonc == "copy":
        # On stock le dernier bouton utilisé
        current = bt_copier
        # On bind le bouton à la fonction voulue
        canvas.bind("<Button-1>", copier)
        # On ajuste le curseur à la fonction
        canvas.config(cursor = 'hand1')

    # Si on utilise ni la sélction ni le copier/coller
    if fonc != "t" and fonc != "copy":
        # On redonne leur apparence et déselectionne les objets
        canvas.itemconfigure("grow", stipple="")
        canvas.dtag("grow", "grow")

    # On enfonce le bouton utilisé
    current.config(relief='sunken')

#########################################################################

"""
Creation Bouton select
"""
mouv = [] #global
fl_select = False #global

def selection(event):
    global fl_select, x1, y1, mouv
    # Si le flag est inactif
    if not fl_select:
        # On sotck la position du curseur
        x1 = event.x
        y1 = event.y
        # On bind les mouvement et le relachement du bouton
        canvas.bind('<B1-Motion>', lambda X: mouvement(X, x1, y1, mouv))
        canvas.bind("<ButtonRelease-1>", selection)
    # Sinon le flag est actif
    else:
        # On déselctionne les objets déjà sélectionnés
        canvas.itemconfigure("grow", stipple="")
        canvas.dtag("grow", "grow")
        # On marque avec un tag les objets dans la zone de sélection
        canvas.addtag_enclosed("grow", x1, y1, event.x, event.y)
        # On marque les objets on les mettant en pointillés
        canvas.itemconfigure("grow", stipple ="gray75")
        # On supprime la zone de sélection
        canvas.delete(mouv.pop())
        # On debind le mouvement de curseur
        canvas.unbind('<B1-Motion>')
    # On active/désactive le flag
    fl_select = not fl_select

#############################################################################
"""
Fonction créan la zone de sélectoin
"""

def mouvement(event, x, y, mouv):
    # Si la liste contient une zone on la supprime
    if mouv:
        canvas.delete(mouv.pop())
    # On créé une zone qu'on ajoute à la liste
    mouv.append(canvas.create_rectangle(event.x, event.y, x, y, dash=(5, 5)))
    # On retourne la liste
    return mouv

#############################################################################

"""
Fonction qui supprime les objets
"""

def sup(event):
    # On récupère l'objet sélectionné par le curseur
    obj = event.widget.find_overlapping(event.x-2, event.y-2,
                                        event.x+2, event.y+2)
    # On récupère ses tags
    L = canvas.gettags(obj)
    # On vérifie que ce n'est pas un objet de la grille
    if L[1] == "grille":
        return(1)
    # On supprime l'objet
    event.widget.delete(obj)

###########################################################################

"""
    Creation selection
"""

x1 = 0 #global
y1 = 0 #global

###########################################################################

"""
Fonction qui sélectionne la couleur
"""
def selcol():
    global color
    # On sélectionne la couleur voulue
    color = colorchooser.askcolor()[1]
    # On met a jour la couleur du label qui montre la couleur
    labcoul.config(bg = color)

###########################################################################

"""
Fonction qui colorie
"""

def colorier(event):
    global color
    # On récupère l'objet sélectionné
    obj = event.widget.find_closest(event.x, event.y)
    # On vérifie que ce n'est pas un objet de la grille
    if canvas.gettags(obj)[1] == "grille":
        return(1)
    # On marque l'objet
    canvas.addtag_closest("sel", event.x, event.y)
    # On change sa couleur avec la couleur voulue
    canvas.itemconfigure("sel", fill =color)
    # On démarque l'objet
    canvas.dtag("sel", "sel")

###########################################################################

"""
Fonction qui zoom
"""
vzoom = 1 #global
def zoomer(event):
    global vzoom
    # On augmente la taille des clous et des fils
    canvas.scale("clou", event.x, event.y, 1.1, 1.1)
    canvas.scale("fil", event.x, event.y, 1.1, 1.1)
    # On met à jour le zoom actuel
    vzoom *= 1.1

###########################################################################

"""
Fonction qui dezoom
"""

def dezoomer(event):
    global vzoom
    # On diminue la taille des clous et des fils
    canvas.scale("clou", event.x, event.y, 0.9, 0.9)
    canvas.scale("fil", event.x, event.y, 0.9, 0.9)
    # On met à jour le zoom actuel
    vzoom *= 0.9

###########################################################################

"""
Fonction qui modifie la couleur du canvas
"""

def cvcolor():
    # On canhe le canvas avec la couleur voulue
    canvas.config(bg = color)

###########################################################################

"""
Fonction qui copie/colle des élément sélectionnés
"""

def copier(event):
    global color, g, f, cb_epaisseur
    tmpg = 0
    tmpf = 0
    L = list(canvas.find_withtag("grow"))
    x1, y1, x2, y2 = canvas.coords(L[0])
    distx = math.sqrt((x1-event.x)**2)
    disty = math.sqrt((y1-event.y)**2)
    if x1 > event.x:
        distx = -distx
    if y1 > event.y:
        disty = -disty
    for obj in L:
        t = canvas.gettags(obj)
        x1, y1, x2, y2 = canvas.coords(obj)
        if len(t) < 3:
            print(len(t))
            if t[0] =='clou':
                print("clou")
                obj = canvas.create_oval(str(abs(x1+distx)), str(abs(y1+disty)), str(abs(x2+distx)), str(abs(y2+disty)), fill = color)
            else:
                print("fil")
                ligne = canvas.create_line(x1+distx, y1+disty, x2+distx, y2+disty, width = int(cb_epaisseur.get()), fill = color)
        else:
            if t[0] == 'clou':


                if t[3] == "f":
                    if t[3] != tmpf:
                        tmpf = t[3]
                        f += 1
                else:
                    if t[2] != tmpf:
                        tmpf = t[2]
                        f += 1
                if t[1][0] == "g":
                    if t[1] != tmpg:
                        tmpg = t[1]
                        g += 1
                    print(event.x, event.y, x1, y1, x2, y2)
                    obj = canvas.create_oval(str(abs(x1+distx)), str(abs(y1+disty)), str(abs(x2+distx)), str(abs(y2+disty)), fill = color, tags = ("clou", "g" + str(g), t[2], "f"+str(f)))
                else:
                    obj = canvas.create_oval(str(abs(x1+distx)), str(abs(y1+disty)), str(abs(x2+distx)), str(abs(y2+disty)), fill = color, tags = ("clou", t[1], "f" + str(f)))
                liens[obj] = {}
            else:

                if t[3] != tmpf:
                    tmpf = t[3]
                    f += 1
                ligne = canvas.create_line(x1+distx, y1+disty, x2+distx, y2+disty, width = int(cb_epaisseur.get()), fill = color, tags = ("fil", "f"+str(f)))



##############################################################################

if __name__ == "__main__":

    root = Tk.Tk()
    root.wait_visibility()

    #root.withdraw()

    # fenetre = Tk.Toplevel()
    # fenetre.title("fenetre")

    """
        Creation frame Haut
    """

    frame = Tk.Frame(root)
    frame.pack(side = "top", fill = "y")

    """
        Creation frame Haut Gauche
    """

    frame4 = Tk.Frame(frame, bg = "gray85")
    frame4.pack()

    frame5 = Tk.LabelFrame(frame, bd = 4, labelanchor = "nw", text = "Paramètres Polygones / Demi-Cercles", bg = "gray85")
    frame5.pack()
    """
        Creation frame Haut Droit
    """

    frame3 = Tk.Frame(frame, bg = "gray85")
    frame3.pack(side = "bottom", fill = "y", expand = True)

    # bt_ = Tk.Button(frame3, text = "zethrt", command = root.destroy)
    # bt_.pack(side = "right")


    frame2 = Tk.Frame(root)
    frame2.pack(fill = "both")

    """
        Creation canvas
    """

    canvas = Tk.Canvas(frame2, bg = "white", width = 10000, height = 5000)
    canvas.pack(fill = "both")

#####################################################

    """
    1 Ceation Grille
    """
    # def hide_gr(grille, canvas, fl_grille):
    #     if fl_grille[0]:
    #         for id in grille:
    #             canvas.itemconfigure(id, state = 'hidden')
    #         fl_grille[0] = False
    #     else:
    #         for id in grille:
    #             canvas.itemconfigure(id, state = 'normal')
    #         fl_grille[0] = True


    grille = []
    for i in range(0, 2000, 30):
        grille.append(canvas.create_line(i, 0, i, 2000, fill = "grey80", tags = ("fil", "grille")))
    for j in range(0, 2000, 30):
        grille.append(canvas.create_line(0, j, 2000, j, fill = "grey80", tags = ("fil", "grille")))

########################################################

    # def relier_tout(canvas, tag="groupe1"):
    #     """
    #     Hehu
    #     """
    #     L = list(canvas.find_withtag(clou))
    #     print("test")
    #     i = 0
    #     while i < len(L):
    #         if canvas.type(L[i]) == 'line':
    #             L.pop(i)
    #         else:
    #             i += 1
    #     for i in range(len(L)):
    #         for j in range(i + 1, len(L)):
    #             relier_2p(L[i], L[j], canv)
    #
    # def relier_2p(p1, p2, canvas):
    #     """
    #     Hehu
    #     """
    #     # if pts2 in POINTSRELIES[pts1]:
    #     #     pass
    #     #else:
    #     x1, y1, x2, y2 = canvas.coords(p1)
    #     x1 = (x1 + x2) / 2
    #     y1 = (y1 + y2) / 2
    #     x2, y2, x3, y3 = canvas.coords(p2)
    #     x2 = (x2 + x3) / 2
    #     y2 = (y2 + y3) / 2
    #     ligne = canvas.create_line(x1, y1, x2, y2, tags = (str(p1), str(p2)))

    tgomme = False
    tclou = False
    tselect = False
#truc state pour gerer l'etat du bouton
    # def swap_bind(test):
    #     if test == "c":
    #         canvas.unbind("<Button-1>")
    #         canvas.bind("<Button-1>", clic)
    #         #canvas.create_oval(str(event.x), str(event.y), str(event.x), str(event.y), width = 5, fill = "black")
    #
    #     elif test == "s":
    #         print("supp")
    #         #canvas.unbind("<Button-1>")
    #         #canvas.bind("<Button-1>", sup)
    #         #obj = event.widget.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
    #         #event.widget.delete(obj)
    #
    #     elif tselect:
    #         x1 = event.x
    #         y1 = event.y
    #
    #
    # def releaseb1(event):
    #     if tselect:
    #         canvas.addtag_enclosed("grow", x1, y1, event.x, event.y)
    #         canvas.delete("grow")


    #canvas.bind("<Button-1>", swap_bind)



    """
        Creation de l'Image
    """
    # img = Image.open("clou.png")
    # img = img.resize((40,40), Image.ANTIALIAS)
    # pclou = ImageTk.PhotoImage(img)
    #
    # img = Image.open("eraser2.png")
    # img = img.resize((40,40), Image.ANTIALIAS)
    # peraser = ImageTk.PhotoImage(img)
    #
    # img = Image.open("clou2.png")
    # img = img.resize((40,40), Image.ANTIALIAS)
    # photo2 = ImageTk.PhotoImage(img)


    """
        Creation Bouton clou
    """


    # def clic(event):
    #     canvas.create_oval(str(event.x), str(event.y), str(event.x), str(event.y), width = 5, fill = "black", tag = "clou")
    #
    #
    # # canvas.bind("<Button-1>", clic)
    #
    #
    #
    # def testclou():
    #     global tclou
    #     # if tclou:
    #     #     bt_clou['image'] = photo
    #     #     canvas.unbind("<Button-1>")
    #     # if not tclou:
    #     #     bt_clou['image'] = photo2
    #     #     canvas.bind("<Button-1>", clic)
    #     tclou = not tclou
    #     if tclou:
    #         tgomme = False
    #         tselect = False
    #     swap_bind("c")


    # bt_clou = Toolbt(frame4, "clou", creer_cl, canvas, "clou.png")
    # bt_gomme = Toolbt(frame4, "gomme", sup, canvas, "clou.png", "dot")
    bt_clou = Tk.Button(frame4, bd = 3,text = "clou", command = lambda: swap_bind("c"))
    #creationimage("pointeur.png", bt_clou)
    img = Image.open("pointeur.png")
    img = img.resize((40, 40))
    pclou = ImageTk.PhotoImage(img)
    bt_clou.config(image=pclou, compound="top")
    # bt_clou.pack(side = "left")
    bt_clou.grid(row = 0, column=0)

    wckToolTips.register(bt_clou, "Cliquez pour créer un clou")





    """
        Creation Bouton fil
    """
    # bt_clou = Toolbt(frame4, "fil", creer_fil, canvas)

    bt_fil = Tk.Button(frame4, bd = 3, text = "Fil", command = lambda: swap_bind("o"))
    #bt_fil.pack(side = "left")
    bt_fil.grid(row = 0, column=1)
    img = Image.open("line.png")
    img = img.resize((40, 40))
    pline = ImageTk.PhotoImage(img)
    bt_fil.config(image=pline, compound="top")

    wckToolTips.register(bt_fil, "Cliquez sur deux clous a relier")

    # def clac(event):
    #     canvas.create_line(str(event.x), str(event.y), str(event.x+50), str(event.y+50), width = 1, fill = "red")
    #

    """
        Creation Menu deroulant
    """
    # Formes =["carre", "rectangle", "rond"]
    # bt_forme = Tk.Menubutton(frame4, text = 'Formes')
    # #bt_forme.grid(row = 0, column = 0)raised
    # men = Tk.Menu(bt_forme)
    # men.add_command(label = 'carre')
    # men.add_command(label = 'rond')
    # men.add_command(label = 'rectangle')
    # bt_forme.pack(side = 'left')
    # bt_forme.configure(menu = men)



    # c1 = clou(100, 100)
    # c2 = clou(150, 200)
    # s1 = Segment(c1, c2)

    # c1.set_clou(100, 100)
    # c2.set_clou(150, 200)photo
    """
        Creation Bouton Supp
    """

    # def sup(event):
    #     obj = event.widget.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
    #     event.widget.delete(obj)
    #
    #
    # def testsup():
    #     global tgomme
    #     # if tgomme:
    #     #     bt_gomme['text'] = 'Sup Inactif'
    #     #     canvas.unbind("<Button-1>")
    #     # if not tgomme:
    #     #     bt_gomme['text'] = 'Sup Actif'
    #     #     canvas.bind("<Button-1>", sup)
    #     tgomme = not tgomme
    #     if tgomme:
    #         tclou = False
    #         tselect = False
    #     print("test"+str(tclou))
    #     swap_bind("s")
    #bt_gomme = Toolbt(frame4, "gomme", lambda: sup, canvas, "clou.png", "dot")
    bt_gomme = Tk.Button(frame4, bd = 3, text = "Supprimer", command = lambda: swap_bind("s"))
    # bt_gomme.pack(side = "left")
    img = Image.open("trash.png")
    img = img.resize((40,40))
    peraser = ImageTk.PhotoImage(img)
    bt_gomme.config(image=peraser, compound="top")

    bt_gomme.grid(row = 0, column=2)

    wckToolTips.register(bt_gomme, "Cliquez sur un élément a supprimer")



    """
        Creation selection
    """

    # x1 = 0
    # y1 = 0
    #
    # def testselection():
    #     global tselect
    #     # if tselect:
    #     #     bt_select['text'] = 'not select'
    #     #     canvas.unbind("<Button-1>")
    #     #     canvas.unbind("<ButtonRelease-1>")
    #     # if not tselect:
    #     #     bt_select['text'] = 'selection'
    #     #     canvas.bind("<Button-1>", selection)
    #     #     canvas.bind("<ButtonRelease-1>", selection)
    #     tselect = not tselect



    # def selection(event):
    #     global pselect, x1, y1
    #     if tselect:
    #         if not pselect:
    #             x1 = event.x
    #             y1 = event.y
    #         else:
    #             canvas.addtag_enclosed("grow", x1, y1, event.x, event.y)
    #             canvas.delete("grow")
    #         pselect = not pselect


    # canvas.bind("<Button-1>", selection)
    # canvas.bind("<ButtonRelease-1>", selection)

    bt_select = Tk.Button(frame4, bd = 3, text = "Selection", command = lambda: swap_bind("t") )
    # bt_select.pack(side = "left")
    bt_select.grid(row = 0, column=3)
    img = Image.open("selection.png")
    img = img.resize((40, 40))
    pselect = ImageTk.PhotoImage(img)
    bt_select.config(image=pselect, compound="top")
    # canvas.bind("<Button-1>", selection)
    # canvas.bind("<ButtonRelease-1>", selection)
    wckToolTips.register(bt_select, "Selectionne les objets compris\nentre l'enfoncement et le relachement\ndu clic")


    """
    1    Bouton grille
    """
    fl_grille = [True]
    bt_grille = Tk.Button(frame4, bd = 3, text = "Hide Grille", command = lambda: hide_gr(grille, fl_grille) )
    # bt_grille.pack(side= "left")
    bt_grille.grid(row = 0, column=26)
    img = Image.open("grille1.png")
    img = img.resize((40, 40))
    pgrille = ImageTk.PhotoImage(img)
    bt_grille.config(image=pgrille, compound="top")

    wckToolTips.register(bt_grille, "Cache/Montre la grille")

    fl_clou = [True]
    bt_hideclou = Tk.Button(frame4, bd = 3, text = "Hide Clou", command = lambda: hide_cl(fl_clou))
    # bt_grille.pack(side= "left")
    bt_hideclou.grid(row = 0, column=25)
    img = Image.open("hideclou.png")
    img = img.resize((40, 40))
    phide = ImageTk.PhotoImage(img)
    bt_hideclou.config(image=phide, compound="top")

    wckToolTips.register(bt_hideclou, "Cache/Montre les clous")


    bt_canvas = Tk.Button(frame4, bd = 3, text = "Couleur Fond", command = lambda: cvcolor())
    # bt_grille.pack(side= "left")
    bt_canvas.grid(row = 0, column=27)
    img = Image.open("canvsfond.png")
    img = img.resize((40, 40))
    pcanvas = ImageTk.PhotoImage(img)
    bt_canvas.config(image=pcanvas, compound="top")

    wckToolTips.register(bt_canvas, "Change la couleur du fond")
    #########################################
    """
    Bouton relie un a un
    """
    bt_relun = Tk.Button(frame3, bd = 3, text = "Arrêtes Figure", command = lambda: swap_bind("u"))
    bt_relun.pack(side = "left")

    wckToolTips.register(bt_relun, "Cliquez sur l'angle d'une figure\npour lui créer ses arrêtes")

    #############################################
    """
    Bouton ligne POINTS
    """
    bt_ligne = Tk.Button(frame3, bd = 3, text = "Arrête De Points", command = lambda: swap_bind("p"))
    bt_ligne.pack(side = "left")

    wckToolTips.register(bt_ligne, "Cliquez sur une arrête pour \n y mettre les points")

    #########################################

    """
    Bouton defaut
    """
    defaut = Tk.Button(frame3, bd = 3, text = "Arc De Fils", command = lambda: swap_bind("d"))
    defaut.pack(side = "left")

    wckToolTips.register(defaut, "Cliquez sur un point de \n deux arrêtes différentes\n pour faire un arc")

    #########################################


    """"
    Bouton Copier
    """

    bt_copier = Tk.Button(frame3, bd = 3, text = "Copier/Coller", command = lambda: swap_bind("copy"))
    bt_copier.pack(side = "left")

    wckToolTips.register(bt_copier, "Copie les objets sélectionnés\net les colle sur le clic")
    #########################################
    """
    Bouton tout relier
    """
    reliertout = Tk.Button(frame3, bd = 3, text = "Tout Relier", command = lambda: relier_tout())
    reliertout.pack(side = "left")

    wckToolTips.register(reliertout, "Relie tout les points sélectionnés \n entre eux")


    #########################################
    """
    Bouton cercle
    """
    bt_cercle = Tk.Button(frame4, bd = 3, text = "Polygone", command = lambda: swap_bind("r"))
    #bt_cercle.pack(side = "left")
    bt_cercle.grid(row = 0, column=5)
    img = Image.open("poly.png")
    img = img.resize((40, 40))
    ppoly = ImageTk.PhotoImage(img)
    bt_cercle.config(image=ppoly, compound="top")

    wckToolTips.register(bt_cercle, "Créer un polygone avec\nle nombre de côtés sélectionné")

    #########################################
    """
    Bouton angle
    """
    bt_angle = Tk.Button(frame4, bd = 3, text = "Arc De Fils", command = lambda: swap_bind("a"))
    #bt_angle.pack(side = "left")
    bt_angle.grid(row = 0, column=7)
    img = Image.open("angle.png")
    img = img.resize((40, 40))
    pangle = ImageTk.PhotoImage(img)
    bt_angle.config(image=pangle, compound="top")
    wckToolTips.register(bt_angle, "Créer un anlge avec\nun arc de fils")

    #########################################

    """
    Bouton arc
    """
    bt_arc = Tk.Button(frame4, bd = 3, text = "Demi-Cerlce", command = lambda: swap_bind("arc"))
    #bt_arc.pack(side = "left")
    bt_arc.grid(row = 0, column=6)

    img = Image.open("arc.png")
    img = img.resize((40, 40))
    parc = ImageTk.PhotoImage(img)
    bt_arc.config(image=parc, compound="top")

    wckToolTips.register(bt_arc, "Créer un arc de cercle\navec le nombre de côtés sélectionné")


    #########################################
    """
    Bouton rotation
    """
    bt_rotate = Tk.Button(frame4, bd = 3, text = "Rotation", command = lambda: rotation_f())
    #bt_rotate.pack(side = "left")
    bt_rotate.grid(row = 0, column=16)

    img = Image.open("rotation1.png")
    img = img.resize((40, 40))
    protate = ImageTk.PhotoImage(img)
    bt_rotate.config(image=protate, compound="top")
    #canvas.bind('<r>', rotation_f())
    wckToolTips.register(bt_rotate, "Effectue une rotation sur\n les objets sélectionnés")
    #########################################
    """
    Bouton mouvement
    """
    bt_left = Tk.Button(frame4, bd = 3, text = "left", command = lambda: mouvement_f("l"))
    #bt_left.pack(side = "left")
    bt_left.grid(row = 0, column=17)
    img = Image.open("left.png")
    img = img.resize((40, 40))
    pleft = ImageTk.PhotoImage(img)
    bt_left.config(image=pleft, compound="top")

    wckToolTips.register(bt_left, "Déplace à gauche\nles objets sélectionnés")

    bt_right = Tk.Button(frame4, bd = 3, text = "right", command = lambda: mouvement_f("r"))
    #bt_right.pack(side = "left")
    bt_right.grid(row = 0, column=18)

    img = Image.open("right.png")
    img = img.resize((40, 40))
    pright = ImageTk.PhotoImage(img)
    bt_right.config(image=pright, compound="top")

    wckToolTips.register(bt_right, "Déplace à droite\nles objets sélectionnés")

    bt_up = Tk.Button(frame4, bd = 3, text = "up", command = lambda: mouvement_f("u"))
    #bt_up.pack(side = "left")
    bt_up.grid(row = 0, column=19)

    img = Image.open("up.png")
    img = img.resize((40, 40))
    pup = ImageTk.PhotoImage(img)
    bt_up.config(image=pup, compound="top")

    wckToolTips.register(bt_up, "Déplace en haut\nles objets sélectionnés")

    bt_down = Tk.Button(frame4, bd = 3, text = "down", command = lambda: mouvement_f("d"))
    #bt_down.pack(side = "left")
    bt_down.grid(row = 0, column=20)

    img = Image.open("down.png")
    img = img.resize((40, 40))
    pdown = ImageTk.PhotoImage(img)
    bt_down.config(image=pdown, compound="top")

    wckToolTips.register(bt_down, "Déplace en bas\nles objets sélectionnés")

    canvas.bind('<a>', lambda: mouvement_f("u"))
    canvas.bind('<Control-Down>', lambda: mouvement_f("d"))
    canvas.bind('<Control-Right>', lambda: mouvement_f("r"))
    canvas.bind('<Control-Left>', lambda X: mouvement_f("l", X.widegt))
    #########################################

    img = Image.open("parametre.png")
    img = img.resize((40, 40))
    ppara = ImageTk.PhotoImage(img)

    para=Tk.Label(frame5, image = ppara)
    para.pack(side = "left")

    text=Tk.Label(frame5, text="nombre de côtes:", cursor = "question_arrow", width =15)
    #text.grid(row = 0, column=2)
    text.pack(side = "left")

    nbcercle = ttk.Combobox(frame5, width = 2, values = [3, "4", "5", "6"])
    nbcercle.current(0)
    #nbcercle.grid(row = 0, column=5)
    nbcercle.pack(side = "left")
    #nbcercle.grid(row=0, column=10)

    #text.grid(row = 0, column = 11)
    text2=Tk.Label(frame5, anchor = 'e', text="nombre de points:", cursor = "question_arrow", width =18)
    #text2.grid(row = 0, column=6)
    text2.pack(side = "left")
    #text2.grid(row=0, column=9, )

    nbligne = ttk.Combobox(frame5, width = 2, values = [0,1,2,3, "4", "5", "6", 10000])
    nbligne.current(3)
    #nbligne.grid(row = 0, column=9)
    nbligne.pack(side = "left")
    #nbligne.grid(row=0, column=12)

    #text.grid(row = 0, column = 11)
    text3=Tk.Label(frame5, anchor = 'e', text="largeur:", cursor = "question_arrow", width =10)
    #text3.grid(row = 0, column=10)
    text3.pack(side = "left")
    #text2.grid(row=0, column=9, )

    nblarg = ttk.Combobox(frame5, width = 4, values = [100, 150, 200, 250, 300])
    nblarg.current(1)
    #nblarg.grid(row = 0, column=13)
    nblarg.pack(side = "left")

    #text.grid(row = 0, column = 11)
    text4=Tk.Label(frame5, anchor = 'e', text="hauteur:", cursor = "question_arrow", width = 10)
    #text4.grid(row = 0, column=14)
    text4.pack(side = "left")
    #text2.grid(row=0, column=9, )

    nbhaut = ttk.Combobox(frame5, width = 4, values = [100, 150, 200, 250, 300])
    nbhaut.current(1)
    #nbhaut.grid(row = 0, column=17)
    nbhaut.pack(side = "left")

    #text.grid(row = 0, column = 11)
    text5=Tk.Label(frame5, anchor = 'e', text="epaisseur fils:", cursor = "question_arrow", width =15)
    #text4.grid(row = 0, column=14)
    text5.pack(side = "left")
    #text2.grid(row=0, column=9, )

    cb_epaisseur=ttk.Combobox(frame5, width = 2, values=["1","2","3"])
    cb_epaisseur.current(0)
    cb_epaisseur.pack(side = "left")

    rel = Tk.IntVar()
    cb_relier = Tk.Checkbutton(frame5, anchor = 'e', text = "arrêtes?", variable = rel)
    cb_relier.pack(side = "left")
    #cb_relier.grid(row = 0, column = 0)
    wckToolTips.register(cb_relier, "Creer automatiquement les arrêtes\ndes polygones/demis-cercle")

    lig = Tk.IntVar()
    cb_ligne = Tk.Checkbutton(frame5, anchor = 'e', text = "arrêtes de points?", variable = lig)
    cb_ligne.pack(side = "left")
    #cb_ligne.grid(row = 0, column=1)
    wckToolTips.register(cb_ligne, "Creer automatiquement les arrêtes de points\ndes polygones/demis-cercle")
    current = bt_clou

    #########################################
    """
    Bouton zoom
    """
    zoom = Tk.Button(frame4, bd = 3, text = "+ Zoom", command = lambda: swap_bind("z"))
    #zoom.pack(side = "left")
    zoom.grid(row = 0, column = 21)

    img = Image.open("zoom_in_1.png")
    img = img.resize((40, 40))
    pzoom = ImageTk.PhotoImage(img)
    zoom.config(image=pzoom, compound="top")

    wckToolTips.register(zoom, "Zoom sur le curseur")

    #########################################

    """
    Bouton dezoom
    """
    dezoom = Tk.Button(frame4, bd = 3, text = "- Zoom", command = lambda: swap_bind("dz"))
    #dezoom.pack(side = "left")
    dezoom.grid(row = 0, column = 22)

    img = Image.open("zoom_out_1.png")
    img = img.resize((40, 40))
    pdezoom = ImageTk.PhotoImage(img)
    dezoom.config(image=pdezoom, compound="top")

    wckToolTips.register(dezoom, "Dezoom sur le curseur")

    #########################################

    # nbcercle = Tk.IntVar()
    # nbcercle.set("3")
    # modnbcercle = Tk.Entry(frame4, width=20, relief=Tk.SUNKEN, bd=2,
    #                        textvariable=nbcercle)
    # modnbcercle.pack(side=Tk.LEFT)

    # nbligne = Tk.IntVar()
    # nbligne.set("3")
    # modnbligne = Tk.Entry(frame4, width=20, relief=Tk.SUNKEN, bd=2,
    #                        textvariable=nbligne)
    # modnbligne.pack(side=Tk.LEFT)

    # epaisseur = Tk.IntVar()
    # epaisseur.set("3")
    # lb_epaisseur = Tk.Listbox(frame4)
    # lb_epaisseur.insert(1, "1")
    # lb_epaisseur.insert(2, "2")
    # lb_epaisseur.insert(3, "3")
    # lb_epaisseur.insert(4, "4")
    # lb_epaisseur.pack(side=Tk.LEFT)
    # cb_epaisseur=ttk.Combobox(frame4, width = 2, values=["1","2","3"])
    # cb_epaisseur.current(0)
    # cb_epaisseur.pack(side = "left")
    # sb_epaisseur = Tk.Scrollbar(frame4, orient = 'vertical', command = canvas.yview)
    # sb_epaisseur.grid(row=0, column=1, sticky='ns')
    # canvas['yscrollcommand'] = sb_epaisseur.set


    """
    Bouton colorieer
    """
    bt_colorier = Tk.Button(frame4, bd = 3, text = "colorier", command = lambda: swap_bind("col"))
    #bt_colorier.pack(side = "left")
    bt_colorier.grid(row = 0, column=12)

    img = Image.open("colorier.png")
    img = img.resize((40, 40))
    pcolorier = ImageTk.PhotoImage(img)
    bt_colorier.config(image=pcolorier, compound="top")

    wckToolTips.register(bt_colorier, "Cliquer sur l'objet à colorier")

    #########################################
    """
    Bouton couleur
    """
    color= "black"

    bt_color = Tk.Button(frame5, bd = 3, text = "Couleur", command = selcol )
    bt_color.pack(side = "left")

    wckToolTips.register(bt_color, "This button exits the program")
    #bt_color.grid(row = 0, column = 12)
    labcoul=Tk.Label(frame5, bd = 5, bg = "black", highlightthickness = 10, width = 2)
    labcoul.pack(side = "left")

    wckToolTips.register(bt_color, "Sélectionner la couleur à utiliser")




        # fl_grille = [True]
        # gridbutt = tk.Button(toolbar, text="Grille",
        #                      command=lambda: toggleGrid(grille, canv, fl_grille))

    # def relier(event):
    #     global prelier, x1, y1
    #     if not prelier:
    #         x1 = event.x
    #         y1 = event.y
    #     else:
    #         canvas.addtag_enclosed("reliage", x1, y1, event.x, event.y)
    #
    #         canvas.delete("reliage")
    #     prelier = not prelier


    # canvas.bind("<Button-1>", clac)
    # id = canvas.create_line(100, 100, 150, 150, width = 1, fill = "red")
    #set_clou(30, 30)
    # img = Image.open("clou.png")
    # photo = ImageTk.PhotoImage(img)
    #
    # filename = ImageTk.PhotoImage(file = "clou.png")
    #image = canvas.create_image(0, 0, anchor = NE, image = filename)

    Tk.mainloop()
