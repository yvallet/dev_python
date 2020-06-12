# coding: utf8

from tkinter import *
from tkinter import ttk  ## pour les combobox
import sys
import os
import platform  ## pour connaitre OS utilisé

import pickle
from tkinter import messagebox
from  datetime import date, time, datetime, timedelta
from outils import * ## verif_date()



def printy(*args):
	global DEBUG
	#printy ("printy debug:", DEBUG)
	if DEBUG == True:
		print (args)

def deplacement(event):
	print ("deplacement : ", event.keysym)

def hello():
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG
	touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
	ano1 = -1                      ## pour eviter calcul_focus
	anomalie("Hello")
	touche = ""
	ano1 = 0	

def validation():

	#print ("Validation ", "radio: ", var_bouton.get(), " checkBoxs : ", checkvar1.get(), " ", checkvar2.get() )
	
	for nom, widget in ents.items():
		
		val = widget.get()
		if len(val)==0:                         ## controler si obligatoire
	
			for j in range (0,len(entrees)):
				if len(entrees[j]) > 1:
					##wnom, col, wid, foc , entete, maxi , required, nature = entrees[j]
					wnom, wrow , col, wid, foc , msg, maxi , required, nature = entrees[j]
					if wnom == nom:
						break
			
			if required == "O":
				anomalie("Il faut informer les zones obligatoires")
				ano1 = 1
				widget.focus()
				return
				
	## si tout est OK
	######### Raz zone entry
	for nom, widget in ents.items():
		widget.delete(0, 'end')
		
		if nom == "my_combo": ## remettre la valeur par defaut
			my_combo.current(3)  ## default
	
	
	## reposition radiobotton a valeur par defaut
	try:
		var_bouton.set(1) ## val defaut
	except:
		pass
	
	## raz des checkbox
	try:
		checkvar1.set(0)
		checkvar2.set(0)
		checkvar3.set(0)
	except:
		pass
	
	
## validation 3 boutons Oui/Non/Annuler
def valider3(msg):
	rep = messagebox.askyesnocancel("confirmer", msg)
	if rep == True:
		return "oui"
	elif rep == False:
		return "non"
	else:
		return "annule"
		

		
def confirmer(msg):
	rep = messagebox.askyesno("Attention",msg)
	return rep  ## renvoie True/False
	#messagebox.askokcancel("Title","The application will be closed")
	#messagebox.askretrycancel("Title","Installation failed, try again?")
	
def anomalie(msg):
	#entree_nom.bell()                         ##le bell est dedans
	messagebox.showwarning("Attention", msg)
	#messagebox.showinfo   ("Attention", msg)
	#messagebox.showerror  ("Attention", msg)

	
def abandon():      ## Abondon
	global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val
	touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
	ano1 = -1                      ## pour eviter calcul_focus
	
	rep = confirmer("Abandon  , confirmez ")
	if rep == True:
		fenetre.quit()	
		
	touche = ""
	ano1 = 0

def sel_bouton():
	choix = var_bouton.get()
	x = "option choisir : "+ str(choix) 
	#anomalie (x)

def lire_combo(event):
	choix = my_combo.get()
	#print ("combo , choix: ", choix)
	
	
def test_bouton(my_var):  ## i = indice du bouton de 1 a 10
	#print ("test bouton ", my_var )
	
	i = my_var
	if i == 1:
		validation()
		
	if i == 2:
		abandon()
		
	if i == 3:
		pass
	if i == 4:
		pass
	if i == 5:
		pass
	if i == 6:
		pass
	if i == 7:
		pass
	if i == 8:
		pass
	if i == 9:
		pass
	if i == 10:
		pass
		
		
def controle_champs(nom_champ, valeur):
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG, val
	
	ano1 = 1

	for j in range (0,len(entrees)):
		if len(entrees[j]) > 1:
			##wnom, col, wid, foc , entete, maxi , required, nature = entrees[j]
			wnom, wrow , col, wid, foc , msg, maxi , required, nature = entrees[j]
			if wnom == nom_champ:
				break
			else: ## si pas une entry (ex. si combobox my_combo, passe par after_field , controlé dans les specifiques
				required="N"
				nature="nono"
	
	## Tests required = "O" ==> le champ ne doit pas etre vide
	##       nature      alpha/date/entier/decimal/none
	##       maxi        testé dans fonction my_callback
	
	#print ("controles a faire sur champ: ", wnom, " = ",nom_champ , "required:", required, " Nature:", nature, "Touche ==> ", touche)
	
	if required == "O":
		if len(valeur)==0 and len(touche)>0 and (touche=="Up" or touche=="Home") :
		## permettre de remeonter par Up si zone vide, sans controle de la zone
			printy ("ok, null avec touche ",touche )
			return "OK"
		else:
			if len(valeur) == 0:
				anomalie("Le champ est obligatoire")
				printy ("ano sortie chmap:  ", nom_champ, "ano1:", ano1, "widget_ano:", widget_ano)
				return "KO"	
				
	if nature == "none":
		return "OK"
		
	if nature == "alpha":
		if valeur.isnumeric() == True:
			anomalie ("Ce champ n'est pas  numerique !")
			return "KO"
	
	if nature == "date":
		ret, date_saisie, wdt = verif_date(valeur)  ## date_saisie type date , wdt type chr
		val = wdt  ## remise en forme jj/mm/aaaa
		if ret == "KO":
			printy ("ano date , ano1:  ", ano1, "widget_ano:", widget_ano) 
			anomalie("La date saisie est invalide")
			return "KO"
	
	if nature == "entier":
		if valeur.isnumeric() == False:
			anomalie ("Ce champ doit etre numerique , sans decimale !")
			return "KO"
			
	
	if nature == "decimal":
		xint = ""
		xfloat = ""
		
		try:
			x1 = int(valeur)
			xint="oui"
		except ValueError:
			xint="non"
						
		try:
			x2 = float(valeur)
			xfloat="oui"
		except ValueError:
			xfloat="non"
			
			
		if xint == "non" and xfloat == "non":
			anomalie ("Ce champ doit etre numerique, avec ou sans decimales!")
			return "KO"
			
	return "OK"
	
###################### Controles spécifiques éventuels
def controles_specifiques(widget, nom_champ, valeur):
		
	if nom_champ == "nom":
		## controle et si anomalie , return "KO"
		pass
		
	if nom_champ == "prenom":
		## controle et si anomalie , return "KO"
		pass
		 
	if nom_champ == "datnais":
		widget.delete(0, 'end')
		widget.insert(0, val )
				
		if len(val)>7:  ## si info date saisie (rien en UP et zone vide, pas de calcul age)
			
			#print ("val : ", val)
			date_saisie=date(int(val[6:10]), int(val[3:5]), int(val[0:2]))
			printy("date_saisie : ", date_saisie)
		
			age = date.today() - date_saisie   ###### Specifique zone datnais pour calcul age et afficher age
			age_an = int(age.days / 365.25)
			if age_an > 0:				
				wnom = "age"
				x = ents[wnom]
				x.delete(0, 'end')
				x.insert(0, str(age_an) )
				frame.update()
				
		# pas un controle , on ne touche pas a ano1
		return "OK"
	
	
	if nom_champ == "age":
		## controle et si anomalie , return "KO"
		pass
		
	if nom_champ == "ville":
		## controle et si anomalie , return "KO"
		#val = int(valeur)
		#if val > 1000:
		#	anomalie ("valeur limitee a 1000")
		#	return "KO"
		pass
		
	if nom_champ == "my_combo":
		#print ("specifique my_combo !! ")
		if len(val) == 0:
			anomalie("choisir une valeur dans la liste")
			return "KO"
		
				
	return "OK" ## 
		
		
def before_field(event):
	global ano1,  touche, zone_ano, nom_ano, futur, actuel
		
	####### retrouver l'identite du widget avec son nom
	#wnom = frame.nametowidget("datnais") 
	#print ("widget datnais: ", wnom )
		
	################ retrouver le nom 
	## depuis event.widget
	## print (str(event.widget))                ##==> .!frame.nom
	#  nom =  str(event.widget).split(".")[-1]
	## split '.!frame.l01prenom' cree une liste de n elements selon  le separateur '.' 
	## [-1] prend le dernier de la liste 'nom"
		
	## depuis winfo_name 
	## print (str ((event.widget).winfo_name) ) ##==> <bound method Misc.winfo_name of <tkinter.Entry object .!frame.nom>>
	## split selon le point=> liste de 5 elements      ------1---------- -----------2---------- ------3------ ----4- --5-- 
	#  x =  str(widget_actuel.winfo_name).split(".")[-1] ## prend le dernier element de la liste 'nom>>'
	#  nom = x[0:-2]                                     ## sup des 2 car '>>"
	
		
	nom =  str(event.widget).split(".")[-1]
	touche = "" ## raz , positionne par focusout si Down ou Up
		
	msg = ents_msg[nom]
	if ano1 == 0:
			var_msg.set (msg)	
		
def after_field(event):
	global ano1, touche, zone_ano, nom_ano, futur, actuel, widget_ano, val
		
	##nom =  str(event.widget).split(".")[-1]  ## nom associe au widget par envent
	#print (str(event.widget) ) 
	
	nom =  str(event.widget).split(".")[-1]
	
	#print ("nom : ", nom)
			
	widget_actuel = ents[nom]
	val = widget_actuel.get()
	
	#print ("nom ", nom, "widget:", widget_actuel, "valeur: ",val, "event: ", event ) 	
	#print ("after nom actuel", widget_actuel, "Ano", widget_ano, " flag:", ano1)	

	if (ano1==1 and widget_ano != widget_actuel):
		printy("ano1 + widget differt ==> RETURN" )
		return
			
	ano1 = 1 
	
	ok = controle_champs(nom, val)
	if ok == "OK":
		oks = controles_specifiques(widget_actuel, nom, val)
	
	#print ("sortie controle ok: ", ok,  "ano1:" , ano1)
	if ok == "KO" or oks == "KO":
		#print ("apres KO  nom=", nom,  " ano1:", ano1, "focus ==> :",widget_actuel)
		
		widget_ano = widget_actuel
		widget_ano.focus_set()		         ## laisser le focus sur la zone en erreur
		return
	
	## sans erreur
	ano1 = 0
					
	## si dernier champ, retour au premier pas utile , mettre en takefocus=0 les widgets qui ne prennent pas de focus par tab
	##    ==> boutons et zone de message
	#if widget_actuel == widget_dernier and touche != "Up"	:
	#	widget_premier.focus()

	"""		###Message furtif=========================================================
		vide1.configure(bg="white", text="Coucou !")
		frame.update()   ##  OU  vide1.update_idletasks()   Pour forcer REFRESH écran		
		time.sleep(1.5)
				
		vide1.configure(bg="red", fg="red", text=".") ##, state="DESABLED" )  
		frame.update()   ## OU  vide1.update_idletasks()



		flash_delay = 500  # msec between colour change
		flash_colours = ('black', 'red') # Two colours to swap between

		def flashColour(object, colour_index):
			object.config(foreground = flash_colours[colour_index])
			root.after(flash_delay, flashColour, object, 1 - colour_index)

		root = Tk.Tk()
		my_label = Tk.Label(root, text = 'I can flash!',
                      foreground = flash_colours[0])
		my_label.pack()

	flashColour(my_label, 0)		
	"""

def test_touche(e):
	global touche
	touche = e
	
	print ("touche interceptee : ", e)
	
	#l=len(entree_nom.get())
	#print ("test l:",l)
	#if l > 29:
	#	frame.event_generate('<Tab>')
			
	"""
		if e.keysym == 'Up':
			print('The key was released: ', repr(e.char), "keysym:" , e.keysym )
			touche = 'UP'
	"""
	
def my_callback(var, indx, mode, my_var, maxi):
		
	#output = ''.join(hex(ord(c)) for c in my_var.get())  ## ord("A") ==>65  chr(65) ==> "A"  hex(65) ==> 41
	#printy ("HEX:", output)
	
	##si longeur=2  avec 1 blanc , le supprimer INUTILE, Pb si on initialize les champs a " " !!
	## c'est ce cas qd on donne le focus avec la souris dans une zone vide !!
	#ll = len(my_var.get())
	#if ll == 2:
	#	if my_var.get()[:1] == " ":
	#		tronque = my_var.get()[1:]
	#		my_var.set(tronque)
		
	ll = len(my_var.get())
	if ll > maxi:
		##Tk().bell()  beepe mais ouvre une fenetre ! #
		###winsound.MessageBeep(-1) ## ca marche aussi , rajouter import winsound
		print ( chr(7) , end=' ' , flush=True)              ## beep OK , mais fait in saut de ligne, sauf end=' '
		tronque = my_var.get()
		my_var.set(tronque[0:maxi] )
		#printy ("Je tronque:", tronque)	


################ Parametres ##################################################################################################
DEBUG = False		   ## mettre a 1 pour rend les printyy effectifs

nomfic = "testv3"  ## Nom du fichier binaire enregistre

avec_radio = "O"   ## si il y a un radiobox pour raz en effacement ecran
avec_box   = "O"   ## si il y a des checkbox pour raz en effacement ecran
avec_combo = "O"   ## si combobox liste deroulante

larg = 800        ## taille fenetre
haut = 800
titre_fenetre = ("exercice YV tkinter V3")

ano1 = 0
touche = ""

fenetre = Tk()
fenetre.title(titre_fenetre)
resolution = str(larg)+'x'+str(haut)+'+60+60'

fenetre.geometry(resolution)
#fenetre.geometry('500x1500+50+50')

fond="SlateGray3" ## couleur de fond ==> bisque red lavender gray cyan 'light grey' 'SlateGray1'  SlateGray3 yellow gold cyan green green2 green3 red re2red3
#                 ##                      blue 'sky blue' 'deep sky blue'

frame = Frame(fenetre, bg=fond, width=larg, height=haut )           ## width=100, height=600  <== inutile, s'adapte avec les widgets contenus
frame.grid(row=0, column=0 , padx=10, pady=10 )                     ##, rowspan=1, columnspan=1) ##, padx=20, pady=10)

table_zone=[]
ents={}
ents_msg={}


############ ligne vide en haut ####################################################################################
vide1 = Label(frame, padx=10, width=30,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide1.grid(row=0,padx=10, pady=10,sticky='nw' )  ## en haut
	
	
	
######################################## les zones d'entry ##########################################################	
## creation liste vide imbriquée des zones entry

n = 10  ## 10 elements
m = 9   ##  1 liste de 8 par element ( Nom , row, Col Width takefocus=0/1  Entete   30=max.input  Required   Nature )
entrees = [[0] * m for i in range(n) ]

###### Parametrage des zones d'entry dans chaque ligne ENTRY , NB nbre ligne fixé dans la var lige ci dessus
##             Nom ,   row ,  Col Width takefocus=0/1  Msg en before field                         30=max.input  Required   Nature(alpha/date/entier/decimal/none)
##             -------        --   ---   ---          ------------                                     -----        ---       ----- 
entrees[0] = ["nom",    1,     1 ,  35 ,  1 ,          "Saisir le Nom , 1 a 30 caracteres      "        ,30       , "O"    , "alpha" ]
entrees[1] = ["prenom", 2,     1 ,  35 ,  1 ,          "Saisir le prenom, 1 a 30 caracteres    "        ,30       , "O"    , "alpha" ]
entrees[2] = ["datnais",3,     1 ,  15 ,  1 ,          "Date sous forme jj/mm/aaa              "        ,10       , "O"    , "date"  ]		
entrees[3] = ["age",    3,     3 ,  8  ,  0 ,          "Age                                    "         ,3       , "N"    , "none"  ] ## focus 0
entrees[4] = ["ville",  4,     1 ,  25 ,  1,           "Saisir la ville, 1 a 20 caracteres     "        ,20       , "O"    , "alpha" ]
entrees[5] = []
entrees[6] = []
entrees[7] = []
entrees[8] = []
entrees[9] = []


for j in range (0,len(entrees)):
	#printy ( "examen j ",j, entrees[j] )
	if len(entrees[j]) > 1:
		#Nom ,     Col Width takefocus=0/1  Msg   30=max.input  Required   Nature
		nom_obj, wrow , col, wid, foc , msg, maxi , required, nature = entrees[j]
		
		nom_string = StringVar(frame, name="stringvar_"+nom_obj)
		nom_string.trace("w", lambda name, index, mode, my_var=nom_string, maxi=maxi: my_callback(name,index,mode,my_var, maxi) )
		
		ent = Entry(frame,  name=nom_obj, bg="white",   width=wid, relief=GROOVE , textvariable=nom_string)
		ent.grid   (row=wrow, column=col,padx=10,pady=10, sticky='nw'  )
		
		#tab_var[nom_obj]  = nom_string  ## objets strinvar associés aux entry  <======== Ne sert plus
		#tab_maxi[nom_obj] = maxi        ## longueur maxi a controler en entry
			
		ent.config(takefocus=foc)
		ent.bind("<FocusIn>",  before_field) 
		ent.bind("<FocusOut>", after_field)
		ent.insert(0,"")                      ## pas " " sinon besoin tronque
		
		ents[nom_obj] = ent
		ents_msg[nom_obj] = msg  ## pour recup le msg associé a l'objet
		if j == 0:
			nom_premier = nom_obj
		nom_dernier = nom_obj
	
		

##################### Les labels #####################################################################################
n = 10  ## 10 elements
m = 10  ##  1 liste de 10 par element ( text width  row  col bg fg relief  anchor  sticky columnspan )
labels = [[0] * m for i in range(n) ]


##             text                width  row   col     bg       fg        relief     anchor  sticky columnspan
labels[0] = [ "nom"        ,        30,    1,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[1] = [ "prenom"     ,        30,    2,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[2] = [ "date denaissance" ,  30,    3,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[3] = [ "age"              ,  8 ,    3,    1,    "yellow", "black", "groove",  "center" , "ne",   1 ]
labels[4] = [ "Ville"            ,  30,    4,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
#labels[5] = [ "Sexe"             ,  5 ,    5,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
#labels[6] = [ "qualité"          ,  5 ,    6,    0,    "yellow", "black", "groove",  "center" , "",   1 ]

labels[5] = []
labels[6] = []
labels[7] = []
labels[8] = []
labels[9] = []
	
												  
for j in range (0,len(labels)):
	#printy ( "examen j ",j, labels[j] )
	if len(labels[j]) > 1:
		wtext, wid, wrow , wcol, wbg, wfg , wrelief, wanchor, wsticky , wspan  = labels[j]
		
		#print (wtext, wid, wrow , wcol, wbg, wfg , wrelief, wanchor, wsticky , wspan)
		#label1 = Label(frame, padx=10, width=30,  text="Nom", bg="yellow",   fg="black", relief=GROOVE, anchor="center" )
		#label1.grid(row=0,column=1,padx=10, pady=10 )
					
		label = Label(frame, padx=10, width=wid,  text=wtext, bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
		label.grid(row=wrow ,column=wcol ,padx=10, pady=10, sticky=wsticky ,columnspan=wspan)

"""	
# + ligne en bas pour affichage des commentaires
var_msg = StringVar()	                                    #  ==> pour afficher un texte :     var_msg.set ("message")
message = Label(frame, textvariable=var_msg , width=60 )    ## Modifier width et columnspan !!!
message.grid(  row=10, column=0 ,  columnspan=4        )    ## msg avec texte modifiable via  set
                                                            ## occupe 2 colonnes , centré , car pas de sticky
"""															
															
if avec_radio == "O":											
	############################### test radiobutton ######################################
	var_bouton = IntVar()
	option1 = Radiobutton(frame, text="Femme",      variable=var_bouton, value=1, command=sel_bouton, height=1) ##, width=30 )  
	option1.grid (row=5,column=1, padx=5, pady=2, sticky='nw' )
	
	option1 = Radiobutton(frame, text="Homme", variable=var_bouton, value=2, command=sel_bouton , height=1) ##, width=30 ) 
	option1.grid (row=5,column=1, padx=5, pady=3 )    ## centre ,sticky='ne' )

	option1 = Radiobutton(frame, text="Neutre", variable=var_bouton, value=3, command=sel_bouton, height=1) 
	option1.grid (row=5,column=1, padx=5, pady=2,sticky='ne' )
	var_bouton.set(1) ## val defaut

if avec_box == "O":
	############################### checkbox ###############################################
	checkvar1 = IntVar()
	checkvar2 = IntVar()
	checkvar3 = IntVar()
	c1 = Checkbutton(frame, padx=0, pady=0, text = "Beau",  variable = checkvar1,  onvalue = 1, offvalue = 0,   width = 6, height=0 )
	c2 = Checkbutton(frame, padx=0, pady=0, text = "Grand", variable = checkvar2,  onvalue = 1, offvalue = 0,   width = 6, height=0 )
	c3 = Checkbutton(frame, padx=0, pady=0, text = "Riche", variable = checkvar3,  onvalue = 1, offvalue = 0,   width = 6, height=0 )

	c1.grid(row=7, column=1,  sticky="nw")
	c2.grid(row=7, column=1  )                ##  Centre par defaut sticky="ne")
	c3.grid(row=7, column=1, sticky="ne")

######################### combobox liste deroulante ########################################
if avec_combo == "O":
	departement = [ "Ain", "Aisne", "Aube","paris", "Alpes", "Ariege", "Yvelines" ]

	my_combo = ttk.Combobox( frame , name="my_combo" , value=departement  , width=30  )
	my_combo.grid (row=8 , column=1 , sticky="nw" )
	my_combo.current(3)  ## default
	my_combo.bind("<<ComboboxSelected>>", lire_combo)

	## ajout a la table des widgets + bind focusout pour passer en after field et controler que a bien été saisi 
	##       dans les controles spécifiques
	ents["my_combo"] = my_combo
	my_combo.bind("<FocusOut>", after_field)						

							
############################ les boutons ######################################################################
n = 10  ## 10 elements
m = 8  ##  1 liste de 10 par element ( text width  row  col bg fg relief  anchor  sticky columnspan )

boutons = [[0] * m for i in range(n) ]

#######        text            bg        relief    row  col width   centrage     image 
boutons[0] = [ "Valider",    "white",     "raised" ,  10 , 0 ,  40 ,     "w"  , "valide1.png"  ]  ## Valider
boutons[1] = [ "Quitter",    "white",     "raised" ,  10,  3 ,  40 ,     "w"  , "sortir.png"   ]  ## Valider
boutons[2] = []
boutons[3] = []
boutons[4] = []
boutons[5] = []
boutons[6] = []
boutons[7] = []
boutons[8] = []
boutons[9] = []

tab_img=[]
directory = "C:\\icones\\"
##my_image = PhotoImage(file = r"C:\icones\valide1.png") 

for j in range (0,len(boutons)):

	if len(boutons[j]) > 1:  ######## pour avoir un objet image different par bouton
		wtext, wbg, wrelief, wrow , wcol , wid , centrage , wimage = boutons[j]
		if len(wimage) > 1:
				img = PhotoImage(file = directory +  wimage ) 
		else:
			img=""
			
	if len(boutons[j])  == 0:
		img=""	
		
	tab_img.append(	img )
		
for j in range (0,len(boutons)):

	if len(boutons[j]) > 1:
		x = j+1
		wtext, wbg, wrelief, wrow , wcol , wid , centrage , wimage = boutons[j]	
		
		bouton = Button(frame, bg=wbg, text=wtext, relief=wrelief, command=lambda my_var=x:test_bouton(my_var), width=wid, image=tab_img[j], compound = BOTTOM, takefocus=0)
		bouton.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage ) # sticky=W  aligné west dans la colonne
		
	"""
	if len(boutons[j]) > 1:
		x = j+1
		wtext, wbg, wrelief, wrow , wcol , wid , centrage , wimage = boutons[j]
		
		##my_image = PhotoImage(file = r"C:\icones\valide1.png") 
		directory = "C:\\icones\\"
				
		##wbg white si  avec image
		
		if j == 0:
			if len(wimage) > 1:
				img = PhotoImage(file = directory +  wimage ) 
			else:
				img=""
			bouton_01 = Button(frame, bg=wbg, text=wtext,  relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img, compound = BOTTOM)
			bouton_01.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 1:
			if len(wimage) > 1:
				img1 = PhotoImage(file = directory +  wimage ) 
			else:
				img1=""
			bouton_02 = Button(frame, bg=wbg, text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img1, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 2:
			if len(wimage) > 1:
				img2 = PhotoImage(file = directory +  wimage ) 
			else:
				img2=""
			bouton_02 = Button(frame, bg=wbg, text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img2, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 3:
			if len(wimage) > 1:
				img3 = PhotoImage(file = directory +  wimage ) 
			else:
				img3=""
			bouton_02 = Button(frame,bg=wbg,  text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img3, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 4:
			if len(wimage) > 1:
				img4 = PhotoImage(file = directory +  wimage ) 
			else:
				img4="" 
			bouton_02 = Button(frame,bg=wbg,  text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img4, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 5:
			if len(wimage) > 1:
				img5 = PhotoImage(file = directory +  wimage ) 
			else:
				img5="" 
			bouton_02 = Button(frame,bg=wbg,  text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img5, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 6:
			if len(wimage) > 1:
				img6 = PhotoImage(file = directory +  wimage ) 
			else:
				img6="" 
			bouton_02 = Button(frame, bg=wbg, text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img6, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 7:
			if len(wimage) > 1:
				img7 = PhotoImage(file = directory +  wimage ) 
			else:
				img7="" 
			bouton_02 = Button(frame, bg=wbg, text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img7, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 8:
			if len(wimage) > 1:
				img8 = PhotoImage(file = directory +  wimage ) 
			else:
				img8="" 
			bouton_02 = Button(frame,bg=wbg,  text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img8, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
			
		if j == 9:
			if len(wimage) > 1:
				img9 = PhotoImage(file = directory +  wimage ) 
			else:
				img9="" 
			bouton_02 = Button(frame,bg=wbg,  text=wtext, relief=wrelief ,command=lambda my_var=x:test_bouton(my_var) , width=wid , image=img9, compound = BOTTOM)
			bouton_02.grid (row=wrow , column=wcol, padx=10, pady=10, sticky=centrage )              # sticky=W  aligné west dans la colonne
		"""	

#bouton_valide = Button(frame, text="Valider",bg="salmon", relief="raised"  ,command=lambda my_var=1:test_bouton(my_var), width=wid , image=img, compound = BOTTOM)
#bouton_valide.grid (row=8 , column=0, sticky=W , padx=10, pady=10)  ## sticky=W  aligné west



#fond = "black"  ## <================

"""
############################ les lignes vides en bas #################################################################
## avec bind il faut des lignes vides     bg = fg = couleur de fond  <<++ invisibles !!

vide2 = Label(frame, padx=10, width=2,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide2.grid(row=5,column=4, padx=10, pady=10,sticky='nw' )  ## en bas

vide3 = Label(frame, padx=10, width=1,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide3.grid(row=6,column=4,padx=10, pady=10,sticky='nw' )
 
vide4 = Label(frame, padx=10, width=1,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide4.grid(row=7,column=4,padx=10, pady=10,sticky='nw' )
"""

vide5 = Label(frame, padx=10, width=1,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide5.grid(row=8,column=4,padx=10, pady=10,sticky='nw' )

vide6 = Label(frame, padx=10, width=1,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide6.grid(row=9,column=4,padx=10, pady=10,sticky='nw' )


# + ligne en bas pour affichage des commentaires
var_msg = StringVar()	                                                 #  ==> pour afficher un texte :     var_msg.set ("message")
message = Label(frame, textvariable=var_msg , width=60, takefocus=0 )    ## Modifier width et columnspan !!!
message.grid(  row=10, column=0 ,  columnspan=4        )                 ## msg avec texte modifiable via  set
                                                                         ## occupe 4 colonnes , centré , car pas de sticky


############################# Menu pour test ############################################
menubar = Menu(frame)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!",  command=abandon)
fenetre.config(menu=menubar)

########################################################################################




fenetre.bind('<Return>', lambda x:fenetre.event_generate('<Tab>'))                                 ## RETURN ++> TAB
fenetre.bind('<Down>'  , lambda x:[ test_touche("Down") , fenetre.event_generate('<Tab>')] )       ## FLECHE DOWN ++> TAB
fenetre.bind('<Up>'    , lambda x:[ test_touche("Up")   , fenetre.event_generate('<Shift-Tab>')] ) ## FLECHE UP ++> SHIFT + TAB

widget_premier  = ents[nom_premier]
widget_dernier  = ents[nom_dernier]


#pour retour sur la 1ere zone d'entree
widget_premier.focus()

zone_ano   = fenetre.focus_get() ## init zone
widget_ano = fenetre.focus_get() ## init zone
actuel     = fenetre.focus_get() ## init zone

fenetre.protocol('WM_DELETE_WINDOW',abandon )  ## le bouton windows quit (croix) agit comme le bouton Abandon
 
fenetre.mainloop()

