# coding: UTF-8
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
from  datetime import date, time, datetime, timedelta
from outils import * ## verif_date()
from tkinter import ttk
import sys
import os
import csv
import platform  ## pour connaitre OS utilisé
from tkinter import messagebox

###################################################################################################	
#    xnomfic  nom parametre ==> fichier des data (bin ou database , + fichier.csv  + fichier.pdf  #
#    parametrage  = param_nomfic.csv                                                              #
###################################################################################################
def ecrire():
	wnomfic = "param_" + ents["xnomfic"].get() + ".csv"
	tmp=[]	
	
	with open( wnomfic , mode='w' ,newline='' ) as fichier_csv:
		objet_csv = csv.writer(fichier_csv, delimiter=';',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
				
		for j in range (0,9):#  # ligne des 9 parametres
			nom, col, wid, foc , entete, maxi , required, nature , unicite = entree[j]
			
			nom_champ = nom
			val = ents[nom_champ].get()
			tmp=[nom_champ, val] ##; print (tmp)
			objet_csv.writerow(tmp)
		
		
		########### le tableau des champs 
		xnb = ents["xnbchamp"].get()
				
		for j in range (0,int(xnb)):
			tmp=[]	
			ii = "{:0>2d}".format(j+10) 
						
			for i in range (0, len(entree)):
				nom, col, wid, foc , entete, maxi , required, nature , unicite = entree[i]
											
				if i > 9 :	
					nom_champ = "l" + ii + nom
					champ = ents[nom_champ].get()
					val = ents[nom_champ].get()
					tmp=[nom_champ, val]
					
					objet_csv.writerow(tmp)
										
			 				
	msg = "le fichier csv suivant a ete crée : "+ wnomfic
	message(msg)
		
###################################################################################################	

def charger(nomfic): ## chargement automatique a l'ouverture
	global nbr_champ 
	## recharger
		
	wnomfic = "param_" + nomfic + ".csv"
		
	if mon_os == "Windows":
		## creation du .bat qui teste si le fichier existe , sinon le cree a vide
		fic = open("test_fic.bat", "w")
	
		txt = '@echo off'            ; fic.write (txt + "\n")
		txt = 'IF EXIST "%1" ('      ; fic.write (txt + "\n")
		#txt = 'echo  "%1" "existe"' ; fic.write (txt + "\n")
		txt = 'exit 8'               ; fic.write (txt + "\n")
		txt = ') ELSE ('             ; fic.write (txt + "\n")
		#txt = 'echo "%1" "Absent"'  ; fic.write (txt + "\n")
		txt = 'type nul > "%1"'      ; fic.write (txt + "\n")
		txt = 'exit 9'               ; fic.write (txt + "\n")
		txt = ')'                    ; fic.write (txt + "\n")
	
		fic.close()
		
		cmd = "test_fic.bat " + wnomfic 
		#print (cmd)
		ret = os.system(cmd)  ##   8=File exist   ;   '9'= absent , cree dans le bat
		#print ("ret: ", ret)
		
	else:  ## linux
		fic = open("test_fic.sh", "w")
		
		txt = 'test -f $1'         ; fic.write (txt + "\n")
		txt = 'ret=$?'             ; fic.write (txt + "\n")
		txt = 'echo $ret'          ; fic.write (txt + "\n")
		txt = 'if [ $ret -eq 1 ] ' ; fic.write (txt + "\n")
		txt = 'then'               ; fic.write (txt + "\n")
		txt = 'cat /dev/null > $1' ; fic.write (txt + "\n")
		txt = 'echo "cree"       ' ; fic.write (txt + "\n")
		txt = 'fi'                 ; fic.write (txt + "\n")
		txt = 'exit $ret'          ; fic.write (txt + "\n")
		fic.close()
		
		cmd = "sh ./test_fic.sh " + wnomfic 
		#print ("cmd: ",cmd)
		ret = os.system(cmd)
		#print ("ret : ", ret)  ## ret=8 si existe    =9 inexistant, est cree
		
	if ret > 8: ## inexistant YYY
		rep = confirmer ("fichier inexistant, confirmer sa creation ")
		if rep == True:
			return True
		else:
			return False
			
			
	## fichier existant : on le charge	
	######################### Lecture fichier d'entree ########################################
		
	fic = wnomfic 
	
	#print (crit1, crit2, crit3, rang_crit1, rang_crit2, rang_crit3 )
	
	with open( fic , mode='r' ,newline='' ) as fichier_csv:
		objet_csv = csv.reader( fichier_csv , delimiter=';',  quotechar='"', quoting=csv.QUOTE_MINIMAL) 
				
		for row in objet_csv:  
			"""
			if debut == 0:
				debut = 1  ## sauter la 1ere ligne entete de colonnes
			else:	
			"""
			
			#print (row)  ## row = 1 enregt complet sous forme de liste
			champ    = row[0]
			valeur   = row[1]
				
				#datnais= row[2]
				#age    = row[3]
				#ville  = row[4]
			
			if champ == "xnbchamp":
				nbr_champ = int(valeur)
				
			obj = ents[champ]
			obj.delete(0, 'end')
			obj.insert(0, valeur)
	
	return True ## apres chargement OK
			
################################################################################	


def maj_up_down( fleche):
	global touche
		
	touche = fleche
	
def confirmer(msg):
	rep = messagebox.askyesno("Attention",msg)
	return rep  ## renvoie True/False
	#messagebox.askokcancel("Title","The application will be closed")
	#messagebox.askretrycancel("Title","Installation failed, try again?")
	
def anomalie(msg):
	#entree_nom.bell()                         ##le bell est dedans
	messagebox.showwarning("Attention", msg)
	
	fenetre.focus_force()
	fenetre.lift()
	
	#messagebox.showinfo   ("Attention", msg)
	#messagebox.showerror  ("Attention", msg)
	
def message(msg):
	messagebox.showinfo   ("Information", msg)

def test_bouton(my_var): 
	global touche, ano1
	kk = my_var
	
	if kk == 1:  ## bouton 1 Valider ecran ecrire le fichier csv
		touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
		ano1 = -1   
		ecrire()
		fenetre.quit()	
		
	
	if kk == 2:  ## abandon
		touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
		ano1 = -1      
		rep = confirmer("Abandon sans sauvegarde , confirmez ")
		if rep == True:
			fenetre.quit()	
			
def abandon():
	global touche, ano1
	touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
	ano1 = -1  
	
	rep = confirmer("Abandon sans sauvegarde , confirmez ")
	if rep == True:
		fenetre.quit()	

		
##################### create table dans la base #########################
def cre_table():
	global choix_base, nomfic	
	
	if choix_base == "1":
		import mysql.connector as lite
		from mysql.connector import Error
		connexion = lite.connect(host='localhost', database='ga4', user='root',  password='saanar')
	else:
		## sqlite
		import sqlite3 as lite
		nom_base =  "C:/Users/yvall/Exos_python_win/ga4.db"
		print (nom_base)
		connexion = lite.connect(nom_base, timeout=20)
	
	req1 = "create table " + nomfic
	req1 += " ( id integer primary key  "
	if choix_base == "1": req1 += " auto_increment "  ## pas recommandé si Sqlite
	
	########### le tableau des champs 
	xnb = ents["xnbchamp"].get()
				
	for j in range (0,int(xnb)):
			 
		ii = "{:0>2d}".format(j+10) 
		ch1 = 	"l" + ii + "nom"
		wnom = ents[ch1].get()
			
		ch2 = "l" + ii + "nature"
		nature = ents[ch2].get()
			
		ch3 = "l" + ii + "maxi"
		maxi = ents[ch3].get()
			
		if choix_base == "1":  ## pour Mysql
			wtype = "varchar" ## defaut
			if nature == "alpha":wtype="char(" + str(maxi)  + ")"
			if nature == "entier":wtype="integer"
			if nature == "date": wtype="char(10)"
			if nature == "float": wtype="decimal"
		else:
			wtype = "text"
			if nature == "entier" : wtype = "integer"
			if nature == "float"  : wtype = "real"
		
		req2 = " , " + wnom + " " + wtype 
		req1 += req2
	
	req2 = " )"
	req1 += req2
	
	#print (req1)
		
	try:
		curseur = connexion.cursor()
		curseur.execute(req1)
		
	except Exception as err:
		print('Query Failed: %s\nError: %s' % (req1, str(err)))
	finally:
		pass
	
	
	
	 
######################## Controle input maxi des zones en entry ############################################		
def my_callback(var, indx, mode, my_var, maxi):
	
	#print ("my_var: ", my_var, " maxi: ", maxi , my_var.get() )
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
		
def printy(*args):
	global DEBUG
	#printy ("printy debug:", DEBUG)
	if DEBUG == True:
		print ("debug", args)	
		
def before_zone(events):
	global ano1, widget_ano, widget_en_cours, touche,  DEBUG
	nom =  str(events.widget).split(".")[-1]
			
	if ano1 == 0:
		widget_ano = ents[nom] 
		#printy(" remise ano a : ", widget_ano , "  en BEFORE ZONE ")
		
	wnom = nom
	if wnom[0] == "x" :
		nom_court = nom      ## L01nom_zone , on elimine L01 
	else:
		nom_court = wnom[3:]
		
	for j in range (0,len(entree)):
		if len(entree[j]) > 1:
			wnom, col, wid, foc , entete, maxi , required, nature , unicite = entree[j]
			#print ("entree: ",j, wnom, col, wid, foc , entete, maxi , required, nature , unicite  )
			if wnom == nom_court:
				break	
				
	msg = entete
	##print ("before ", nom, nom_court, entete, "msg:", msg)
	
	if ano1 == 0:
			#var_msg.set (msg)
			#message[var_msg] = msg
			
			message_lig.config(text=msg)
			frame.update()			
	
def controle_champs(nom_champ, valeur, nom_ecran ):
	global ano1
	
	#print ("controle champ: ", nom_champ )
	val_alfa=str(valeur)
	#print ("valeur, alfa ", valeur, val_alfa, "ano1", ano1, "touche ", touche)
	
	if ano1 == -1:  ## demande de sortie par bouton01
		return
	 		
	ano1 = 1
	
	for j in range (0,len(entree)):
		if len(entree[j]) > 1:
			wnom, col, wid, foc , entete, maxi , required, nature , unicite = entree[j]
			#print ("entree: ",j, wnom, col, wid, foc , entete, maxi , required, nature , unicite  )
			if wnom == nom_champ:
				break
	
	## Tests required = "O" ==> le champ ne doit pas etre vide
	##       nature      alpha/date/entier/decimal/none
	##       maxi        testé dans fonction my_callback
	##       unicite     le champ ne doit etre present 2 fois dans le tablo
	
	#printy ("controles a faire sur champ: ", wnom, " = ",nom_champ , "required:", required, " Nature:", nature, "TOUCHE: ",touche)
	
	if required == "O":
		if len(val_alfa)==0 and len(touche)>0 and (touche=="Up" or touche=="Home") :
		## permettre de remeonter par Up si zone vide, sans controle de la zone
			printy ("ok, null avec touche ",touche )
			
		else:
			if len(val_alfa) == 0:
				anomalie("Le champ est obligatoire")
				printy ("ano sortie chmap:  ", nom_champ)
				return "KO"
	
	if unicite == "O":
		pass
		"""
		for j in range (0, ligt):
			cle = "{:0>4d}".format(j+1) + nom_champ
			
			nolig = int (nom_ecran[1:3])  ## l01nom, l02nom, ...
			nolig = nolig + depassement
			ii = "{:0>4d}".format(nolig)
			cle_zone = ii + nom_champ
			 
			if cle == cle_zone: ## c'est le champ lui meme, si on y repasse
				pass
			else:
				val_lue = tablo.get(cle , "~" )
				 
				if valeur == val_lue:
					anomalie("Cette valeur a deja ete saisie")
					printy ("ano sortie chmap:  ", nom, "ano1:", ano1, "widget_ano:", widget_ano)
					return "KO"		
		"""
		
				
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
def controles_specifiques(nom_champ, valeur, widget_concerne):
	global nbr_champ , choix_base , nomfic
	
	#print ("specifique: ", nom_champ, valeur)
	
	if nom_champ == "xnomfic":
		ret = charger(valeur)
		nomfic = valeur  ## pour create table
		if ret == False:
			return "KO"
				
	if nom_champ == "xbase":
		choix_base = valeur
		if int(valeur) < 1 or int(valeur)>2 :
			anomalie ("doit etre 1 ou 2 !")
			return "KO"
	
	if nom_champ == "xlige":
		#print (int(valeur) )
		if int(valeur) > 15:
			anomalie ("valeur : 1 a 15")
			return "KO"
		 				
	if nom_champ == "xnbchamp":
		nbr_champ = int(valeur )         ## pour controle egale nbre de lignes dans le tableau
		if int(valeur) > 10:
			anomalie ("limité a 10 champs")
			return "KO"
	
	if nom_champ == "nom":
		ll = len(valeur)
		for i in range(0,ll):
			if valeur[i] == " ":
				anomalie ("pas d espace dans le nom !")
				return "KO"
	
	if nom_champ == "col":
		if int(valeur) < 1 or int(valeur)>10:
			anomalie ("entre 1 et 10 !")
			return "KO"
			
	if nom_champ == "wid":
		if int(valeur) <1 or int(valeur)>50:
			anomalie ("entre 1 et 50 !")
			return "KO"
			
	if nom_champ == "foc":
		if int(valeur) > 1 :
			anomalie ("Focus :  0=Oui 1=Non ")
			return "KO"
			
	if nom_champ == "maxi":
		if int(valeur) <1 or int(valeur)>50:
			anomalie ("entre 1 et 50 !")
			return "KO"		
			
	if nom_champ == "req":
		if valeur == "O" or valeur == "N" : return "OK"
		anomalie ("Doit etre O ou N  !")
		return "KO"	
			
	if nom_champ == "nature":
		if valeur == "alpha" : return "OK"
		if valeur == "date" :  return "OK"
		if valeur == "entier": return "OK"
		if valeur == "float" : return "OK"		
		if valeur == "none" :  return "OK"
		
		anomalie ("Valeurs autorisees : alpha/date/entier/float/none")
		return "KO"
			
	if nom_champ == "unicite":
		if valeur == "O" or valeur == "N" : return "OK"
		anomalie ("Doit etre O ou N  !")
		return "KO"	 
		
#############################################################################################	
def after_zone(events):
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG, nbr_champ

	##print (events.widget)
	
	nom =  str(events.widget).split(".")[-1]  ## nom associe au widget par envent
			
	widget_actuel = ents[nom]
	x = ents[nom].get()
	
	if ano1 == -1:  ## cas on valide l'ecran par la touche Valide et on quitte ==> inutile calculer suivant
		return

	if (ano1 == 1 and widget_ano != widget_actuel):
		#if len(touche)==0:
		printy ("ano1 + widget differt ==> RETURN  ", widget_ano, "actuel: ",widget_actuel )
		return	
			
			
	#print("==================================================================")
	#print ("entree after zone ", nom )
	
	val = x
	wnom = nom
	if wnom[0] == "x" :
		nom_court = nom      ## L01nom_zone , on elimine L01 
	else:
		nom_court = wnom[3:]
		numlig = int(wnom[1:3]) - 9
		
		#print ("Controle champ ", wnom, numlig, nbr_champ)
		
		if numlig > nbr_champ:
			anomalie("tous les champs ont ete saisis, remonter ou corriger le nbre de champs")
			return
		
	
	#print("debut after champ=", nom_court ,  "Valeur : ", val )
	
	## Controles Champs, specifique a ecrire #########################################
		
	ok = controle_champs(nom_court, val, nom)
	if ok == "OK":
		#print ("OK")
		oks = controles_specifiques(nom_court, val, widget_actuel)
	 
	if ok == "KO" or oks == "KO":
		print ("KO !!!!!!!!!",widget_ano, widget_actuel )
		widget_ano = widget_actuel
		widget_ano.focus_set()		         ## laisser le focus sur la zone en erreur
		#fenetre.lift()
		return
		
	ano1 = 0

	
#########################################################################################################
DEBUG=False
ano1=0
touche=""
nbr_champ = 0
choix_base = "2"  ##Sqlite pour init
nomfic=""
ents = {}
ents_msg = {}
table_var = {}
table_maxi = {}
trouve=[]  ## pour sequence recherche , liste des occurences trouvees
mon_os = platform.system() ## windows/linux

root = Tk()



##################### Les labels #####################################################################################
n = 9 ## 10 elements
m = 10  ##  1 liste de 10 par element ( text width  row  col bg fg relief  anchor  sticky columnspan )
labels = [[0] * m for i in range(n) ]


##             text                       width  row   col     bg       fg        relief     anchor  sticky columnspan
labels[0] = [ "nom fichier"        ,        20,    1,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[1] = [ "Base de Donnee   "  ,        20,    2,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[2] = [ "lige nbr lig.ecran"     ,    20,    3,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[3] = [ "ligt nbr lig total" ,        20,    4,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[4] = [ "nbr champs par lig"       ,  20 ,   5,    0,    "yellow", "black", "groove",  "center" , "ne",   1 ]
labels[5] = [ "titre Appli"              ,  20,    6,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[6] = [ "titre Edition"            ,  20 ,   7,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[7] = [ "Larg Fenetre"          ,     20,    8,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]
labels[8] = [ "Haut Fenetre"        ,       20,    9,    0,    "yellow", "black", "groove",  "center" , "nw",   1 ]


## creation liste vide imbriquée des zones entry

n = 19  ## 10 elements
m = 9   ##  1 liste de 9 par element ( Nom , row, Col Width takefocus=0/1  Entete   30=max.input  Required   Nature unicite )
entree = [[0] * m for i in range(n) ]

###### Les Parametrage  
##             Nom ,     row ,     Width takefocus=0/1  Msg en before field      30=max.input  Required   Nature(alpha/date/entier/decimal/none)
##             -------             ---   ---          ------------                             -----        ---       ----- 
entree[0] = ["xnomfic",     1,      25 ,  1 ,   "Saisir le Nom de fichier      "        ,30       , "O"    , "alpha"  ,"N"]
entree[1] = ["xbase",       2,      4  ,  1 ,   "Choix Base 1=Mysql 2=Sqlite   "        ,1        , "O"    , "entier" ,"N"]
entree[2] = ["xlige",       3,      4  ,  1 ,   "nbre de lignes ecran max=15   "        ,30       , "O"    , "entier" ,"N"]
entree[3] = ["xligt",       4,      4  ,  1 ,   "nombre de lignes tableau total"        ,10       , "O"    , "entier" ,"N"]		
entree[4] = ["xnbchamp",    5,      2  ,  1 ,   "nbre de champs horizontalement"         ,3       , "N"    , "entier" ,"N"] 
entree[5] = ["xtitre_app",  6,      25 ,  1,    "Saisir titre application      "        ,20       , "O"    , "alpha"  ,"N"]
entree[6] = ["xtitre_edi",  7,      25 ,  1,    "Saisir le titre pour edition  "        ,20       , "O"    , "alpha" , "N"]
entree[7] = ["xlargeur",    8,      5  ,  1,    "Saisir la largeur de fenetre  "        ,20       , "O"    , "entier", "N"]
entree[8] = ["xhauteur",    9,      5  ,  1,    "Saisir hauteur de fenetre     "        ,20       , "O"    , "entier", "N"]
##
 
#entree[9] = []

entree[10] = ["nom"   ,    1,      20,   1,    "Nom du champ sans espace       ",       20 ,      "O" ,    "alpha",  "O" ]
entree[11] = ["entete",    1,      30,   1,    "Entete du champ                ",       30 ,      "O" ,    "alpha",  "O" ]
entree[12] = ["col"   ,    1,      5,    1,    "Colonne 1-15                   ",       2 ,      "O" ,    "entier",  "O" ]
entree[13] = ["wid"   ,    1,      5,    1,    "Largeur champ ecran            ",       2 ,      "O" ,    "entier",  "O" ]
entree[14] = ["foc"   ,    1,      5,    1,    "Focus 1=Oui 0=Non              ",       1 ,      "O" ,    "entier",  "O" ]
entree[15] = ["maxi"  ,    1,      5,    1,    "Maxi caracteres en saisie      ",       2 ,      "O" ,    "entier",  "O" ]
entree[16] = ["req"   ,    1,      5,    1,    "Requis O/N                     ",       1 ,       "O" ,    "alpha",  "O" ]
entree[17] = ["nature",    1,      10,   1,    "Nature alpha/entier/date/float ",       7 ,       "O" ,    "alpha",  "O" ]
entree[18] = ["unicite",    1,     10,    1,    "Unicite O/N                   ",       1 ,       "O" ,    "alpha",  "O" ]


"""
entree[8] = ["crit1",      9,      3  ,  1,    "rupture critre 1 O/N                    "       , 1       , "O"    , "alpha",  "N"]
entree[9] = ["crit1_zone", 10,     3 ,   1,    "zone associee                           "       , 2       , "O"    , "entier", "N"]
entree[10] = ["crit2",      11,    3 ,   1,    "rupture critre 1 O/N                    "       , 1       , "O"    , "alpha",  "N"]
entree[11] = ["crit2_zone", 12,    3 ,   1,    "zone associee                           "       , 2       , "O"    , "entier", "N"]
entree[12] = ["crit3",      13,    3 ,   1,    "rupture critre 1 O/N                    "       , 1       , "O"    , "alpha",  "N"]
entree[13] = ["crit3_zone", 14,    3 ,   1,    "zone associee                           "       , 2       , "O"    , "entier", "N"]
"""

### le parametrage de chaque colonne ( 10 maxi)
##             Nom ,     Col Width takefocus=0/1  Entete   30=max.input  Required   Nature(alpha/date/entier/decimal/none)
##             -------   --   ---   ---          ------------  -----        ---       -----   Unicité 
## entrees[0] = ["nom",      1 ,  35 ,  1 ,          "Nom "        ,30       , "O"    , "alpha" , "O" ]

ligne = ["nom", "entete", "col", "wid", "foc" , "maxi", "req" , "nature" , "unicite"]
maxis = [ 20,     30,      2,     2,      1,      2,      1,      7,          1]
natures = ["alpha" , "alpha", "entier", "entier", "entier", "entier", "alpha", "alpha", "alpha" ]

fenetre = Tk()

canvas = Canvas(fenetre, width=1100, height=770)
canvas.grid(row=0 , column=1)

scroll_y = Scrollbar(fenetre, orient="vertical", command=canvas.yview)

frame = Frame(canvas)


for j in range (0,len(labels)):
	#print (j)
	if len(labels[j]) > 1:
		wtext, wid, wrow , wcol, wbg, wfg , wrelief, wanchor, wsticky , wspan  = labels[j]
		
		#print (wtext, wid, wrow , wcol, wbg, wfg , wrelief, wanchor, wsticky , wspan)
		#label1 = Label(frame, padx=10, width=30,  text="Nom", bg="yellow",   fg="black", relief=GROOVE, anchor="center" )
		#label1.grid(row=0,column=1,padx=10, pady=10 )
					
		label = Label(frame, padx=10, width=wid,  text=wtext, bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
		label.grid(row=wrow ,column=wcol ,padx=10, pady=10, sticky=wsticky ,columnspan=wspan)
	 
 
for j in range (0,9):  ## 9 premieres entrees = parametres individuels

		#Nom ,     Col Width takefocus=0/1  Msg   30=max.input  Required   Nature
	nom_obj, wrow , wid, foc , msg, maxi , required, nature, unicite  = entree[j]
	 
	if j == 0:
		fond = "red"
	else:
		fond = "white"
		
	nom_string = StringVar(frame, name="stringvar_"+nom_obj)
	nom_string.trace("w", lambda name, index, mode, my_var=nom_string, maxi=maxi: my_callback(name,index,mode,my_var, maxi) )
	
	ent = Entry(frame,  name=nom_obj, bg=fond,   width=wid, textvariable=nom_string)  #relief=GROOVE , 
	ent.grid   (row=wrow, column=1, padx=10, pady=10, sticky='nw'  )
		
	#tab_var[nom_obj]  = nom_string  ## objets strinvar associés aux entry  <======== Ne sert plus
	#tab_maxi[nom_obj] = maxi        ## longueur maxi a controler en entry
			
	ent.config(takefocus=foc)
	ent.bind("<FocusIn>",  before_zone) 
	ent.bind("<FocusOut>", after_zone)
	ent.insert(0,"")                      ## pas " " sinon besoin tronque
		
	ents[nom_obj] = ent
	ents_msg[nom_obj] = msg  ## pour recup le msg associé a l'objet
	if j == 0:
		nom_premier = nom_obj
		nom_dernier = nom_obj 
	
	############################### entete du tableau des champs #############################################
	
	wancho="center"
	## entete
	label = Label(frame, padx=10, width=20,  text="Nom-champ", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=0 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=20,  text="En-tete", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=1 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=8,  text="Colonne", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=2 ,padx=5, pady=5)  
	#
	label = Label(frame, padx=10, width=8,  text="Largeur", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=3 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=8,  text="Focus 0/1", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=4 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=8,  text="Maxi", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=5 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=8,  text="Required", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=6 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=10,  text="Nature ", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=7 ,padx=5, pady=5 )  
	#
	label = Label(frame, padx=10, width=8,  text="Unicite", bg=wbg, fg=wfg, relief=wrelief, anchor=wanchor  )
	label.grid(row=9 ,column=8 ,padx=5, pady=5 )  
	#
	
for i in range(0, 10):	

	for j in range(10,19) :
		wnom, wrow , wid, foc , msg, maxi , required, nature, unicite  = entree[j]
	 
		col = j - 10
				
		wrow = i + 10
		ii = "{:0>2d}".format(wrow)
		nom_obj = "l" + ii + wnom
			
		wmaxi = maxi
				
		nom_string = StringVar(frame, name="stringvar_" + nom_obj)
		nom_string.trace("w", lambda name, index, mode, my_var=nom_string, maxi=wmaxi: my_callback(name,index,mode,my_var, maxi) )
				
		ent = Entry(frame,  name=nom_obj, bg="white",   width=wid, relief="groove" , textvariable=nom_string)
		ent.grid   (row=wrow, column=col, padx=5,pady=5, ) ##sticky='ew'  )
			
		#print (nom_obj, wid, wmaxi)
		#table_var[nom_obj]  = nom_string  ## objets strinvar associés aux entry  <======== Ne sert plus
		#table_maxi[nom_obj] = maxi        ## longueur maxi a controler en entry            Ne sert plus
	
		#ent.config(takefocus=foc)
		ent.bind("<FocusIn>",  before_zone) 
		ent.bind("<FocusOut>", after_zone)
		ent.insert(0,"")                      ## pas " " sinon besoin tronque
		ents[nom_obj] = ent
		
		#print ("OBJET: ", nom_obj )
		
## ligne pour commenataire en before field		
# + ligne en bas pour affichage des commentaires
#var_msg = tringVar()	                                               #  ==> pour afficher un texte :     var_msg.set ("message")
#message = Label(frame, textvariable=var_msg , bg="yellow" , fg="black", width=60, takefocus=0 )   ## Modifier width et columnspan !!!

message_lig = Label(frame, text=" " , bg="lightgrey" , fg="black", width=60, takefocus=0 )
message_lig.grid(  row=21, column=0 ,  columnspan=9 , sticky="we"     )                     ## msg avec texte modifiable via  set
 																						## occupe 4 colonnes , centré , car pas de sticky	
if mon_os == "Windows":
	directory = "C:\\icones\\"
else:
	directory = "/mnt/c/icones/"
	
wimage = "valide1.png"
img = PhotoImage(file = directory +  wimage , master=frame).subsample(1,1)  


bouton_next = Button(frame, bg="white", text="Valide", relief=wrelief, command=lambda my_var=1:test_bouton(my_var), width=35, image=img, compound = "bottom", takefocus=0)
bouton_next.grid (row=22 , column=0, padx=15, pady=10, sticky="w" ) # sticky=W  aligné west dans la colonne

wimage = "sortie2.png"
img30 = PhotoImage(file = directory +  wimage, master=frame ).subsample(1,1)  

bouton = Button(frame, bg="white", text="Quit", relief=wrelief, command=lambda my_var=2:test_bouton(my_var), width=30, image=img30, compound = "bottom", takefocus=0)
bouton.grid (row=22 , column=8, padx=15, pady=10, sticky="e" ) # sticky=W  aligné west dans la colonne																						

			
	
# put the frame in the canvas
canvas.create_window(0, 0, anchor='nw', window=frame)

# make sure everything is displayed before configuring the scrollregion
canvas.update_idletasks()

canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)

canvas.grid()
scroll_y.grid(row=0, column=3, sticky="ns")




fenetre.bind('<Return>', lambda x:fenetre.event_generate('<Tab>'))   ## RETURN ++> TAB
fenetre.bind('<Down>',   lambda x:[ maj_up_down( "Down") , fenetre.event_generate('<Tab>')] )  ## fait les 2 fonctions consecutivemt
fenetre.bind('<Up>',     lambda x:[ maj_up_down( "Up")   , fenetre.event_generate('<Shift-Tab>')] )
fenetre.bind('<Home>',   lambda x:[ maj_up_down( "Home") , fenetre.event_generate('<Tab>')] )

fenetre.protocol('WM_DELETE_WINDOW',root.quit ) 

fenetre.focus_force()
fenetre.lift()

widget = ents["xnomfic"]
widget.focus_set()


menubar = Menu(frame)
menubar.add_command(label="cre_table!", command=cre_table)
menubar.add_command(label="Quit!",      command=abandon)
fenetre.config(menu=menubar)

#print (dir(fenetre) ) 

#aa=fenetre.grid_size()
##print (aa)

Wm.iconify(root)   ## la met en icone : disparue !!

root.mainloop()


"""
root = tk.Tk()

canvas = tk.Canvas(root)
##canvas = tk.Canvas(parent)

scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

# group of widgets
for i in range(20):
 tk.Label(frame, text='label %i' % i).pack()
# put the frame in the canvas


canvas.create_window(0, 0, anchor='nw', window=frame)
# make sure everything is displayed before configuring the scrollregion
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
canvas.pack(fill='both', expand=True, side='left')
scroll_y.pack(fill='y', side='right')
root.mainloop()
"""
