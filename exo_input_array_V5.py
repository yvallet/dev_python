# coding: utf8
#!/bin/python3.8
""" 
		V4 = V3 + fonctions de search SANS fichier parametres
		V5 avec parametrage du tableau
"""
from tkinter import *
from tkinter import filedialog  ## ==> filedialog.askdirectory()
import sys
import os
import platform  ## pour connaitre OS utilisé
import csv
from fpdf import FPDF
from tkinter import ttk
import re    ## regex pour verif mail

## pour les mails
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

## ii = "{:0>4d}".format(i)  ##==> idem :   ii = str(i).zfill(4)
## zone_cadree = zone_str.center(taille[, car_de_remplissage])
## zone_cadree = zone_str.ljust (taille[, car_de_remplissage])
## zone_cadree = zone_str.rjust (taille[, car_de_remplissage])

import pickle
from tkinter import messagebox
from  datetime import date, time, datetime, timedelta
from outils import * ## verif_date()
#import winsound  ## pour Beep() et MessageBeep(-1) NB: windowsien


def envoi_mail(FROM, TO, subject, body_txt, filename):
	msg = MIMEMultipart()                # initialize the message we wanna send

	# User et password du compte lie au smtp
	email = "c6d88a046c212a4dd2025c63db347f9c"
	password = "883b69d34a988f44067bf5abfb209d1f"

#FROM = "yvallet@ilta.fr"                                          # the sender's email
#TO   = "yvperso@free.fr"                                          # the receiver's email
#subject = "Edition demandee"                                      # the subject of the email (subject)
#filename = "fic_array.pdf"   

#body_txt = """   
#Bonjour,
#
# Veuillez trouver le document en piece jointe.
# 
# Cordialement"""
#
 
#body_html = """
#<html>
#  <body>
#    <p>Hi,<br>
#       Please find your document as an attachment<br>
#       Thanks
#    </p>
#  </body>
#</html>
#"""


	msg["From"] = FROM        ### set the sender's email 
	msg["To"]   = TO          ##receiver
	msg["Subject"] = subject  # set the subject
	msg.attach(MIMEText(body_txt,  "plain"))

	#msg.attach(MIMEText(body_html, "html"))
	#msg["Bcc"] = "eventuel.com"


	with open(filename, "rb") as attachment:  # Add file as application/octet-stream 
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())
   
	encoders.encode_base64(part)  # Encode file in ASCII characters to send by email 

	part.add_header("Content-Disposition", f"attachment; filename= {filename}",)  # Add header as key/value pair to attachment part

	msg.attach(part)       # Add attachment to message and convert message to string
	text = msg.as_string()

	#print(msg.as_string())

	server = smtplib.SMTP("in-v3.mailjet.com", 587)  # initialize the SMTP server
	server.starttls()                                # connect to the SMTP server as TLS mode (secure) and send EHLO

	server.login(email, password)                    # login to the account using the credentials
	server.sendmail(FROM, TO, msg.as_string())       # send the email
	server.quit()                                    # terminate the SMTP session

##############################################################################################

def f1_click(zone):
	print ("F1 on zone : ", zone)
	

###################################### edition pdf a partir du csv ############################
## https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
class PDF(FPDF):
	tot1 = 0; wcrit1=""
	tot2 = 0; wcrit2=""
	tot3 = 0; wcrit3=""
	totg = 0
	
	def header(self):
		#self.set_font('Arial', 'B', 15)  # Arial bold 15
				
		self.set_font('Courier', 'B', 8)  # Arial bold 15
				
		wamj = str( date.today() )
		wdt = "le " + wamj[8:] + "/" + wamj[5:7]+ "/" + wamj[0:4]
		self.cell(15,10, wdt, 0,0)
		##        15=largeur cellule 10=hight  0=sans bordure   0=curseur deplacé vers la droite(1=+saut)
		
		wtri="tri : "
		
		if crit3== "O" :                wtri = wtri + crit1_name + "/" + crit2_name + "/" + crit3_name
		if crit3== "N" and crit2=="O":  wtri = wtri + crit1_name + "/" + crit2_name
		if crit2== "N" :                wtri = wtri + crit1_name 
		
		if crit1 == "N" :                wtri = " Tri: Sans"
		self.cell(120)  ## deplacemt curseur
		self.cell(30,10, wtri, 0,0)
				
		# Calculate width of title and position
		w = self.get_string_width(title) + 6
		
		pos = (210 - w) / 2
			
		pos = pos - 10
		self.set_x( pos ) ## <== centrage
		
		# Colors of frame, background and text
		self.set_draw_color(0, 80, 180)
		self.set_fill_color(230, 230, 0)
		#self.set_text_color(220, 50, 50)
		
		# Thickness of frame (1 mm)
		self.set_line_width(0)
		
		# Title
		
		#self.cell(w, 9, title, 1, 1, 'C', 1)
		self.cell(w, 9, title, 1, 0, 'C', 1)
		self.ln(4)
		 
		
		## cartouche entete
		lig = ""
		for j in range (0,len(entrees)):	
			if len(entrees[j]) > 1:
				nom, wcol, wid, foc , entete, maxi , required, nature, unicite  = entrees[j]
				ll = maxi + 1
				lig = lig + entete.ljust(ll, ' ') 
				
		ll = len(lig)
		tiret="-"*ll + '\n'
			
		lig = lig + "\n"	
		## + saut ligne
		
		self.set_font_size(8)	## retour normal
		self.cell(0)
		#self.cell(0, 5, tiret, 0,0)
		#self.cell(0, 5, tiret, 0,0)
		
		self.write(5,tiret)
		self.write(5,lig)
		self.write(5,tiret)
		
		
		
	def footer(self):
		# Position at 1.5 cm from bottom
		self.set_y(-15)
		
		self.set_font('Arial', 'I', 8)                              # Arial italic 8
		self.set_text_color(128)                                    # Text color in gray
		self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')  # Page number
		
	def before_group(self, num, nom, valeur):
		self.set_font('Courier', 'UB',8.0)  ## Bold + Underline
		self.cell(20)	
			
		txt = "*"*num + " " + nom + " : " + valeur
		self.cell (0,5, txt, 0,1)
		 
		if num==1:
			self.wcrit1=valeur
			self.tot1 = 0
		if num==2:
			self.wcrit2=valeur
			self.tot2 = 0
		if num==3:
			self.wcrit3=valeur
			self.tot3 = 0 	
		self.set_font('Courier','',8)	## retour normal	 	
			
	def after_group(self, num,nom,  ancien, nouveau):
		self.cell (0,5, "============================", 0,0)
		self.ln(4)
		self.set_font('Courier', 'B',8.0)  ## Bold
		txt = "total " + nom + " " + ancien + " :   "
		if num == 1: txt = txt + str(self.tot1)
		if num == 2: txt = txt + str(self.tot2)
		if num == 3: txt = txt + str(self.tot3)
		self.cell (0,5, txt, 0,1)
		#self.cell (0,5, "============================", 0,0)
		self.ln(4)
		self.ln(4)
		self.set_font('Courier', '',8.0) 
		
	def every_row(self, ligne):
		self.write (4, ligne)
		#self.ln(4)
		
		self.tot1 += 1  ## ici juste un comptage , a personnaliser si autres totaux a faire 
		self.tot2 += 1
		self.tot3 += 1
		
		self.totg += 1
	
	def last_row(self):
	
		#self.totg = self.tot1 + self.tot2 + self.tot3
		self.cell (0,5, "============================", 0,0)
		self.ln(4)
		 
		self.set_font('Courier', 'B',8.0)  ## Bold
		txt = "total general " +  str( self.totg )
		self.cell (0,5, txt, 0,1)
		
####################################################
def edition():
	global crit1, rang_crit1, crit1_name, crit2, rang_crit2, crit2_name , crit3, rang_crit3, crit3_name
	crit1_name=""
	crit1_name=""
	crit1_name=""
	crit1="N"
	crit2="N"
	crit3="N"
	checkvar1.set(False) 
	checkvar2.set(False) 
	checkvar3.set(False) 
	
	frame3.grid()  ## fait apparaitre la frame3     (apres frame2.remove())  
	frame3.focus_set()
	
def editer(repert):
	global crit1, crit2, crit3, rang_crit1, rang_crit2, rang_crit3
	debut = 0
	fic_pdf = repert + "/" + nomfic + '.pdf'
	##print ("fic_pdf:", fic_pdf )  
			
	pdf = PDF(orientation='P', format='A4' , unit='mm')   ##unit='in')
	
	pdf.set_right_margin(2)
	pdf.set_left_margin(2)
	
	pdf.add_page()
	pdf.set_font('Courier','',8.0) ## Courier (fixe) , Arial , Times
	#                               ## '' = normal  'B' bold 'I' Italic 'U' Underline
	#                               ## font size default=12 , sinon conserve cemme indiquée
	
	pdf.set_right_margin(2)
	pdf.set_left_margin(2)
	
	pdf.tot1 = 0
	pdf.tot2 = 0
	pdf.tot3 = 0
	pdf.totg = 0
			
	tmp1=[]
	
	######################### Lecture fichier d'entree ########################################
	## et creation table avec 3 critres de tri
	
	ecrire_csv("N") ## 1) ecrire le tableau dans le csv
	
	#               ## 2) Lecture du csv

	
	fic = nomfic + ".csv"
	
	#print (crit1, crit2, crit3, rang_crit1, rang_crit2, rang_crit3 )
	
	with open( fic , mode='r' ,newline='' ) as fichier_csv:
		objet_csv = csv.reader( fichier_csv , delimiter=';',  quotechar='"', quoting=csv.QUOTE_MINIMAL) 
				
		for row in objet_csv:  
			if debut == 0:
				debut = 1  ## sauter la 1ere ligne entete de colonnes
			else:	
				#print (row)  ## row = 1 enregt complet sous forme de liste
				#nom    = row[0]
				#prenom = row[1]
				#datnais= row[2]
				#age    = row[3]
				#ville  = row[4]
				
				zone_crit1=""
				zone_crit2=""
				zone_crit3=""
				
				if crit1 == "O" : zone_crit1 = row[rang_crit1]   ## positionné dans lire_combo_t1 t2 t3
				if crit2 == "O" : zone_crit2 = row[rang_crit2]
				if crit3 == "O" : zone_crit3 = row[rang_crit3]
				
				#         crit1       crit2        crit3 ,   ------------Infos --------------------
				#ligne = [zone_crit1, zone_crit2, zone_crit3, row[0], row[1], row[2], row[3], row[4] ]
				
				ligne = []
				ligne.append(zone_crit1)       ## 3 zones toujours présentes
				ligne.append(zone_crit2)
				ligne.append(zone_crit3)
				
				for kk in range(0,nb_champ):   ## + nbre champ variable , selon param nb_champ
					ligne.append( row[kk] )
				
				tmp1.append(ligne)
				
	
	
	if crit1=="N" :
		tmp2 = tmp1
		
	if crit1=="O" and crit2=="N":                            ## si un seul critere
		tmp2=sorted(tmp1, key=lambda x: (x[0]) )
		
	if crit1=="O" and crit2=="O" and crit3=="N":              ## si 2  criteres
		tmp2=sorted(tmp1, key=lambda x: (x[0], x[1]) )

	if crit1=="O" and crit2=="O" and crit3=="O":              ## si 3  criteres
		tmp2=sorted(tmp1, key=lambda x: (x[0], x[1] ,x[0]) )
	
	del tmp1
	#print (tmp2)
	
	## si tris sans rupture , les crit1,2,3 ont servi pour trier les donnees
	##     mais ne doivent pas donner lieu a rupture
	
	rupture = checkrup.get()
	#print ("rupture", rupture )
	if rupture == "N":
		crit1="N"
		crit2="N"
		crit3="N"
		
	debut = 0
	for i in range(0 , len(tmp2)):                 ## nbr enregt
	
		## avec les noms et nbre champ en dur :
		##critere1,critere2,critere3 ,   nom,prenom,datnais,age,ville = tmp2[i]
		##lig = nom.ljust(31, " ") + prenom.ljust(31, " ") + datnais.ljust(11, " ") + age.ljust(3, " ") + "  " + ville.ljust(21, " ") ## + '\n'
		
		## avec nbre champ parametres
		champs=[]
		lig = ""
		for kk in range (0, len(tmp2[i]) ):         ## nbre champ par enregt
			champs.append( tmp2[i][kk] )
			
		##print (champs)
		
		critere1 = champs[0] ## les 3 premiers champs sont les criteres de tri + rupture pour after/before_group
		critere2 = champs[1]
		critere3 = champs[2]
		
		##mise en forme de la ligne d'edition  'lig'  pour chaque row
		for kk in range(3, len(champs) ):  
			ll =  entrees[kk-3][5] + 1                 ## max input le champ 6 de la table entrees
			lig = lig + champs[kk].ljust(ll, ' ')      ## garnir chaque zone en completant avec des blancs  a left 
		lig = lig + "\n"							   ## + saut ligne
		#####################################
				
		if debut == 0 :
			if crit1=="O" :
				pdf.before_group(1, crit1_name, critere1)
			if crit2=="O" :
				pdf.before_group(2, crit2_name, critere2)
			if crit3=="O" :
				pdf.before_group(3, crit3_name, critere3)
			debut = 1
			pdf.every_row(lig)
			continue
		
		if crit1=="O" and critere1 != pdf.wcrit1:  ##after(self, num,nom,  ancien, nouveau)
			
			if crit3=="O" : pdf.after_group(3,crit3_name,  pdf.wcrit3, critere3)
			if crit2=="O" : pdf.after_group(2,crit2_name,  pdf.wcrit2, critere2)
			pdf.after_group                (1,crit1_name,  pdf.wcrit1, critere1)
			
			pdf.add_page()                     ## saut de page en rupture 1er critere
			pdf.set_font('Courier','',10.0)
			
			pdf.before_group                (1, crit1_name, critere1)
			if crit2=="O" : pdf.before_group(2, crit2_name, critere2)
			if crit3=="O" : pdf.before_group(3, crit3_name, critere3)
			
			pdf.every_row(lig)
			continue
			
		if crit2=="O" and critere2 != pdf.wcrit2:  ##(self, num,nom,  ancien, nouveau)
						
			if crit3=="O" : pdf.after_group(3,crit3_name,  pdf.wcrit3, critere2)
			pdf.after_group                (2,crit2_name,  pdf.wcrit2, critere2)
						
			pdf.before_group                (2, crit2_name, critere2)
			if crit3=="O" : pdf.before_group(3, crit3_name, critere3)
			
			pdf.every_row(lig)
			continue
			
		if crit3=="O" and critere3 != pdf.wcrit3:  ##(self, num,nom,  ancien, nouveau)
						
			pdf.after_group (3, crit3_name,  pdf.wcrit3, critere3)		
			pdf.before_group(3, crit3_name,  critere3)
			
			pdf.every_row(lig)
			continue	
	
		pdf.every_row(lig)
	
	## totaux apres fin
	if crit3=="O" : pdf.after_group(3,crit3_name,  pdf.wcrit3, critere3)
	if crit2=="O" : pdf.after_group(2,crit2_name,  pdf.wcrit2, critere2)
	if crit1=="O" : pdf.after_group(1,crit1_name,  pdf.wcrit1, critere1)
	
	pdf.last_row()
		
	pdf.output( fic_pdf ,'F')
	
	#print (fic_pdf)
	msg = "Le fichier suivant a ete produit : " + fic_pdf
	message (msg)
	
####################################################################################################		
def ecrire_csv(avec_msg):

	if avec_msg == "O":	
		rep =  filedialog.askdirectory()
		fic = rep + "/" + nomfic + ".csv"
	else:
		fic = nomfic + ".csv"
		
	nbr = len(entrees) ## nbre de champs 
	
	with open( fic , mode='w' ,newline='' ) as fichier_csv:
		objet_csv = csv.writer(fichier_csv, delimiter=';',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
		tmp=[]	
		for j in range (0,len(entrees)):
				 
			if len(entrees[j]) > 1:
				nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
				tmp.append(nom)
				
		objet_csv.writerow(tmp) ## ligne d'entete avec les noms de zone
		
		for i in range (1, ligt+1):
			ii = "{:0>4d}".format(i)  ##==> idem :   ii = str(i).zfill(4)
			
			tmp=[]
			nbok = 0
			for j in range (0,len(entrees)):
				 
				if len(entrees[j]) > 1:
					nom, col, wid, foc , entete, maxi , required, nature, unicite  = entrees[j]
				
					clef = ii + nom
					if clef in tablo :
						val = tablo[clef]
						tmp.append( val )
						nbok +=1
					else:
						tmp.append("")
			if nbok > 0:
				objet_csv.writerow(tmp)
				
	if avec_msg == "O":			 				
		msg = "le fichier csv suivant a ete crée : "+fic
		message(msg)
###################################################################################################	
	
##  choix des 3 zones de tri	
def lire_combo_t1(event):
	global crit1, rang_crit1, crit1_name
	choix = my_combo_t1.get()
	#print ("combo , choix: ", choix)
	 	
	if checkvar1.get() == 1:
		crit1="O"
	else:	
		crit1="N"
		
	#print ("crit1: ", crit1, choix, crit1_name)
	if crit1 == "N":
		anomalie("Il faut deja selectionner le 1er critere")
		return
		
	crit1="O"                                #<<= le 1er critere 
	#rang_crit1=choix                         #<<= 5eme champ de la ligne ==> ville entrees[rang_crit1][5] 
	#crit1_name= entrees[choix][5]            #<<= libelle associé
	crit1_name=choix
	
	for j in range (0,len(entrees)):
		if len(entrees[j]) > 1:
			nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			if crit1_name == nom:
				rang_crit1=j
				break
				
	#print ("crit1: ", crit1, choix, crit1_name,rang_crit1 )

def lire_combo_t2(event):
	global crit2, rang_crit2, crit2_name
	choix = my_combo_t2.get()
	#print ("combo , choix: ", choix)
	 
	if checkvar2.get() == 1:
		crit2="O"
	else:	
		crit2="N"
	
	#print ("crit2: ", crit2, choix, crit2_name)
	if crit1 == "N":
		anomalie("Il faut deja selectionner le 1er critere")
		return
	if crit2 == "N":
		anomalie("Il faut deja selectionner le 2eme critere")
		return
		
	crit2="O"                                #<<= le 1er critere 
	#rang_crit2=choix                         #<<= 5eme champ de la ligne ==> ville entrees[rang_crit1][5] 
	crit2_name=choix                          ##crit2_name= entrees[choix][5]            #<<= libelle associé
	
	for j in range (0,len(entrees)):
		if len(entrees[j]) > 1:
			nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			if crit2_name == nom:
				rang_crit2=j
				break
				
	#print ("crit2: ", crit2, choix, crit2_name, rang_crit2 )
	
def lire_combo_t3(event):
	global crit3, rang_crit3, crit3_name
	choix = my_combo_t3.get()
	 
	print ("crit3 avant ", crit3)
	
	if crit1 == "N":
		anomalie("Il faut deja selectionner le 1er critere")
		return
	if crit2 == "N":
		anomalie("Il faut deja selectionner le 2eme critere")
		return
	if checkvar3.get() == 1:
		crit3="O"
	else:	
		crit3="N"
	
	#print ("crit3: ", crit3, choix)
	if crit3 == "N":
		anomalie("Il faut deja selectionner 3eme 1er critere")
		return
		
	crit3="O"                                #<<= le 1er critere 
	#rang_crit3=choix                         #<<= 5eme champ de la ligne ==> ville entrees[rang_crit1][5] 
	#crit3_name= entrees[choix][5]            #<<= libelle associé
	crit3_name=choix
	
	for j in range (0,len(entrees)):
		if len(entrees[j]) > 1:
			nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			if crit3_name == nom:
				rang_crit3=j
				break
				
	#print ("crit3: ", crit3, choix, crit3_name, rang_crit3)	
	

	
	
##################################################################################################
def controle_champs(nom_champ, valeur, nom_ecran ):
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG, val
	
	ano1 = 1

	for j in range (0,len(entrees)):
		if len(entrees[j]) > 1:
			wnom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			if wnom == nom_champ:
				break
	
	## Tests required = "O" ==> le champ ne doit pas etre vide
	##       nature      alpha/date/entier/decimal/none
	##       maxi        testé dans fonction my_callback
	##       unicite     le champ ne doit etre present 2 fois dans le tablo
	
	printy ("controles a faire sur champ: ", wnom, " = ",nom_champ , "required:", required, " Nature:", nature)
	
	if required == "O":
		if len(valeur)==0 and len(touche)>0 and (touche=="Up" or touche=="Home") :
		## permettre de remeonter par Up si zone vide, sans controle de la zone
			printy ("ok, null avec touche ",touche )
			return "OK"
		else:
			if len(valeur) == 0:
				anomalie("Le champ est obligatoire")
				printy ("ano sortie chmap:  ", nom, "ano1:", ano1, "widget_ano:", widget_ano)
				return "KO"
	
	if unicite == "O":
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
		
	if nom_champ == "nom":
		pass				
	if nom_champ == "prenom":
		pass
		
	if nom_champ == "datnais":
		### traitemt supplemnt  datenais : reaffichage remise en forme jj/mm/aaaa + calcul age
		widget_concerne.delete(0, 'end')
		widget_concerne.insert(0, valeur )
				
		if len(valeur)>7:  ## si info date saisie (rien en UP et zone vide, pas de calcul age)
						
			date_saisie=date(int(valeur[6:10]), int(valeur[3:5]), int(valeur[0:2]))
			printy("date_saisie : ", date_saisie)
		
			age = date.today() - date_saisie   ###### Specifique zone datnais pour calcul age et afficher age
			age_int = int(age.days / 365.25)
			if age_int > 0:
				age_an = str(age_int).rjust(3,' ')  ## rjust cadrage  a droite sur 3 pos , remplissage blanc
				 
				xnom =  str(widget_concerne).split(".")[-1]
				wnom = xnom[0:3] + "age"
				 
				x = ents[wnom]
				x.delete(0, 'end')
				x.insert(0, str(age_an) )
				frame.update()
				wnom_court = wnom[3:]  ## L01age , on elimine L01
				memo_valeur (wnom, age_an, wnom_court, touche)             ## memo age dans le tablo 
		
	if nom_champ == "age":
		pass
	if nom_champ == "ville":
		#val = int(valeur)
		#if val > 1000:
		#	anomalie ("valeur limitee a 1000")
		#	return "KO"
		pass
	if nom_champ == "XXXXX":
		pass
				
	return "OK" ## 
	

   
def memo_valeur (nom, val, nomcourt , touche):
	nolig = int (nom[1:3])
	valeur = str(val)
	#printy ("Nom ",nom, "nolig ", nolig)
	if len(valeur) == 0 and touche=="Up" :  ## non enregistre si remontee a vide
		pass
	else:
		nolig = nolig + depassement
		ii = "{:0>4d}".format(nolig)
		clef = ii + nomcourt
		#printy ("memo, clef : ", clef, "    val: ", val)
		tablo[clef] = val
	
"""
## ne fonctionne pas ici, a associer avec #stringvar1.trace("w", lambda *arg: verif_taille(ent, 30) )
##  dans la definition de l'objet entry
def verif_taille(objet, maxi):
	if len(objet.get()) == maxi:
		anomalie("Maximum " + str(maxi) + " caracteres atteint")
		frame.event_generate('<Tab>')
"""



def neant(): ## pour interdire la croix quit de windows
	pass
	
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
	
def message(msg):
	messagebox.showinfo   ("Information", msg)

######################## Controle input maxi des zones en entry ############################################		
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
	
	"""
	ll = len(my_var.get())
	print("trace : ",my_var.get() , "len:",ll, " var:",var, " indx:", indx, " mode:",mode, "maxi:",maxi)
	if ll-1 > maxi:
		anomalie("Maximum " + str(maxi) + " caracteres atteint")
		
	#printy ("dir : ", dir(my_var) )  ## tous les attributs de l'objet event ex: event.widget event.num, geight, width,...
	#for attr in dir(my_var): 
	#	printy ("attribut: ",attr, '=>', getattr(my_var, attr))
	"""
	
def charger(): ## chargement automatique a l'ouverture
	global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val
	## recharger
	## mon_os = platform.system()
	
	"""  Rechargement a partir du fichier binaire ################################################
	## test presence fichier
	#print ("mon_os: ", mon_os )
	
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
		
		cmd = "test_fic.bat " + nomfic
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
		
		cmd = "sh ./test_fic.sh " + nomfic
		#print ("cmd: ",cmd)
		ret = os.system(cmd)
		#print ("ret : ", ret)  ## ret=0 si existe  >0 inexistant, est cree
		
	
		
	with open(nomfic, 'rb') as mon_fic_in:
		try:
			table = pickle.load(mon_fic_in)
		except EOFError:
			table={} ## fichier vide de depart
		
	printy ("===============rechargement===========================")	
	
	for cle, val  in table.items(): 
		tablo[cle] = val
	
	## Afficher
	for cle, val  in tablo.items(): 
		##printy (cle,val)
		nolig = int(cle[0:4])
		if nolig <= lige:
			ii = "{:0>2d}".format(nolig)
			nom = "l" + ii + cle[4:]
			##printy ("nom: ", nom)
			obj = ents[nom]
			obj.insert(0, val)
			
	"""
	
	
			
	################################ Rechargt avec la base de donnees #######################
	i = 0
	if choix_base == "Mysql":
		cursor = connexion.cursor(dictionary=True)
	else:
		connexion.row_factory = lite.Row
		cursor = connexion.cursor()
	
	req = "select * from " + nomfic
	cursor.execute(req)
	
	for row in cursor: 
		#print (row) ## 1 row = 1 enregt sous forme de dict { 'champ1':val1 , 'champ2':val2 ,  etc   }
				
		i += 1
		ii = "{:0>4d}".format(i)
		
		nb_champ = 0
		## decomposer chaque enregt
		for clef in row.keys():
			val = row[clef]
			#print (clef, "val: ", val)
			
			if nb_champ > 0:  ## sauter le 1ere champ = le rowid
				cle = ii + clef
				tablo[cle] = val
				
			nb_champ += 1
	
	## Afficher
	for cle, val  in tablo.items(): 
		##printy (cle,val)
		nolig = int(cle[0:4])
		if nolig <= lige:
			ii = "{:0>2d}".format(nolig)
			nom = "l" + ii + cle[4:]
			##printy ("nom: ", nom)
			obj = ents[nom]
			obj.insert(0, val)
			
				
################################################################################	
def tri(zone,sens):	
	## tri
	##zone = 1  >> Nom , 2==>prenom, etc
	zone = zone -1 
	
	#print ("zone de tri : ", zone , "sens: ", sens)
	if sens == "D":
		rev=True
	else:
		rev=False
		
	#print (entrees[0][0] ) => nom
	#print (entrees[1][0] ) => prenom
	#print (entrees[2][0] ) => datnais
	
	
	col_tri = entrees[zone][0]
	nature  = entrees[zone][7]
	
	#print ("tri ", col_tri, "nature:", nature )
	
	t1=[]
	for cle, val  in tablo.items():
		if nature == "date":  ## la mettre a aaaa/mm/jj avant tri
			wdt = str(val)
			val = wdt[6:]+ wdt[2:4]+wdt[0:2]
			#val = wdt
		wnom = cle[4:]
		if wnom == col_tri:
			nolig = int(cle[0:4])
			zone = [val, nolig]
			t1.append(zone) 

	t2 = sorted(t1 , reverse=rev )  ##  key=take_second ==> def take_second(elem): return elem[1]  ## ici 1er par defaut
	#print (t2)
	
	kk = 0
	t3=[]
	
	
	for j in range (0,len(t2)):
		val, old = t2[j]
		new = j +1
		zone = [old, new]
		t3.append(zone)
		
	#print (t3)
	
	new_tablo = {}
	
	
	for j in range (0,len(t3)):
		old, new = t3[j]
		for k in range (0,len(entrees)):
	
			if len(entrees[k]) > 1:
				nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[k]
			
				old_clef = "{:0>4d}".format(old) + nom
				new_clef = "{:0>4d}".format(new) + nom
			 
				val = tablo.get(old_clef, "~")
				if val == "~":
					val = ""
					new_tablo[new_clef] = val
				else:
					#del tablo[old_clef]
					new_tablo[new_clef] = val
				
		 	
	for cle, val  in new_tablo.items(): 
		##del tablo[cle]
		tablo[cle] = val
		
	## Afficher
	for cle, val  in tablo.items(): 
		 
		nolig = int(cle[0:4])
		if nolig <= lige:
			ii = "{:0>2d}".format(nolig)
			nom = "l" + ii + cle[4:]
			#print ("cle", cle, "val", val, "nom: ", nom)
			obj = ents[nom]
			obj.delete(0, 'end')
			obj.insert(0, val)		

	
##########  Les boutons ################################
###   		bouton01.config(state='disabled')  disable/normal
###         bouton01.config(fg='red') 
###		printy ("etat:", bouton01['state'] )
###
#bouton1 = [ "Valider",    "SeaGreen", "raised" ,  1 , 6 ,  12 ,   "w" ]  ## sup 
#bouton2 = [] ## sup , chargé auto au demarrage
#bouton3 = [ "Suppression","SkyBlue" , "raised" ,  3 , 6 ,  12 ,   ""  ]
#bouton4 = [ "Insertion" , "SkyBlue" , "raised" ,  4 , 6 ,  12 ,   ""  ]
#
#bouton5 = [ "Abandon"   , "SkyBlue" , "raised" , 10 , 6 ,  12 ,   "e" ]
##def action_bouton01():

def take_val(element):
	return element[0]
	
	
def test_bouton(my_var):  ## i = indice du bouton de 1 a 10
	#print ("test bouton ", my_var )	
	
	global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val, depassement
	
	kk = my_var
	
	if kk == 1:  ## bouton 1 Valider ecran  = ecrire fichier binaire
	
		touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
		ano1 = -1                      ## pour eviter calcul_focus
		if len(tablo) == 0:
			anomalie("Le tableau est Vide ! ")
			return
		
		printy ("validation")
		
		##for cle, val  in tablo.items(): 
		#	printy ("dump: ", cle, val)
			
		with open(nomfic, 'wb') as mon_fic_out:
			pickle.dump(tablo, mon_fic_out)
		
		#print (tablo)
		#printy ("done !")
		
		################################### M A J  Base de donnees ##############################
		if choix_base == "Mysql":
			connexion.autocommit = False 
		else:
			connexion.execute("BEGIN")
		
		req1 = "delete from " + nomfic + " where 1=1 "
		curseur = connexion.cursor()
		curseur.execute(req1)
		
		for i in range (0, ligt):
			req1 = "insert into " + nomfic + " "
			valeurs = " values ( NULL "
		
			ii = "{:0>4d}".format(i+1) 
			
			for j in range (0,len(entrees)):
	
				if len(entrees[j]) > 1:
					nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
					
					clef = ii + nom
					
					val = tablo.get(clef, "~")
					#print ("clef ", clef , "val ", val )
					
					if j == 0:
						if val == "~":  ## si  rien pour la zone-1 = la cle
							break
						
					if val == "~": 
						val = ""
						if nature == "entier" : val = 0
						if nature == "float"  : val = 0
				
					valeurs += " , '" + str(val) + "' "
			
			if j > 0:			
				req1 += valeurs	+ " )"	
				print (req1)
				
				try:
					curseur = connexion.cursor()
					curseur.execute(req1)
		
				except Exception as err:
					print('Query Failed: %s\nError: %s' % (req1, str(err)))
					connexion.rollback()
					message ("Rollback !!!")
					fenetre.quit
				
				
		connexion.commit()
		connexion.close()
		
		message("Fin de programme - données enregistrées dans " + nomfic)
		fenetre.quit()	
	
	
	
	##def action_bouton02():  ## recharger le fichier
	if kk == 2:  ## recharger sup , auto au demarrage
		pass
	"""	
		with open(nomfic, 'rb') as mon_fic_in:
			table = pickle.load(mon_fic_in)
		printy ("===============rechargement===========================")	
	
		for cle, val  in table.items(): 
			tablo[cle] = val
	
		#	# Afficher
		for cle, val  in tablo.items(): 
			##printy (cle,val)
			nolig = int(cle[0:4])
			if nolig <= lige:
				ii = "{:0>2d}".format(nolig)
				## 								idem : ii = format (nolig , '0>2d')    retourne 2 digits, complété par des zeros
				##                                                                     >  ==> les zeros sont devant
			nom = "l" + ii + cle[4:]
				##printy ("nom: ", nom)
				obj = ents[nom]
				obj.insert(0, val)
	"""		
	
	##def action_bouton03():            ## delete ligne 
	##global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val, depassement
	
	if kk == 3:  ## suppression 1 ligne
	#	printy ("bouton3 sur ", widget_ano )
	
		nom =  str(widget_ano).split(".")[-1]
		nolig = int( nom[1:3] ) + depassement
		
		depart = nolig + ligt    ## tablo : 0001nom  0002nom ...  nnnnnom    nnnn = ligt maxi
		dernier = nolig + 1
	
		##printy (tablo)
		for j in range (0,len(entrees)):
	
			if len(entrees[j]) > 1:
				nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			
				#printy ("depart ", depart, "dernier: ", dernier)
				for lig_tablo in range (dernier , depart, +1):
								
					ii = "{:0>4d}".format(lig_tablo)
					cle_depart = ii + nom
				
					preced = lig_tablo - 1				
					ii = "{:0>4d}".format(preced)
					arrivee =  ii + nom
						
					val = tablo.get(cle_depart, "~")
				
					if val != "~":
						tablo[arrivee] = val
						tablo[cle_depart] = "~"  ## pour sup en fin
					
		#printy ("tablo ",tablo )
	
		a_sup=[]
		for clef, val in tablo.items():	##impossible deleter dans la boucle => memo des clef a deleter
			if val == "~":
				a_sup.append(clef)
			
		for clef in a_sup:
			del tablo[clef]
		
		reorganiser(" ")
	
		if depassement > 0:
			depassement -= 1
	

	
	##def action_bouton04(): ############ Insertion dans le tableau
	#global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val, depassement
	
	if kk == 4 : 	############ Insertion dans le tableau
		nom =  str(widget_ano).split(".")[-1]
		nolig = int( nom[1:3] ) + depassement
		
		dernier  = nolig + ligt             ## tablo : 0001nom  0002nom ...  nnnnnom    nnnn = ligt maxi
		depart   = nolig + depassement      ## ligne a raz
	
		#printy ("depart ", depart, "dernier: ", dernier )
		for j in range (0,len(entrees)):
	
			if len(entrees[j]) > 1:
				nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
				#printy ("traitement : ", nom )
			
				for lig_tablo in range (dernier , depart, -1):
			
					ii = "{:0>4d}".format(lig_tablo)
					cle_depart =  ii + nom
					val = tablo.get(cle_depart, "~")
				
					if val != "~":
						jj = lig_tablo +1
						ii = "{:0>4d}".format(jj)
						arrivee = ii + nom
						#printy ("depart ", cle_depart, "arrivee : ", arrivee, " mis a ", val)	
						tablo[arrivee] = val										
					
				#printy ("raz : ", depart )
				tablo[cle_depart] = ""
										
		reorganiser(" ")
	
		if depassement > 0:
			depassement += 1 

	
	#def action_bouton05(): ## Abandon
	#global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val
	
	if kk == 5:  ## Abandon
		touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
		ano1 = -1                      ## pour eviter calcul_focus
		rep = confirmer("Abandon sans sauvegarde , confirmez ")
		if rep == True:
		#	print (rep)
			fenetre.quit()	
		
		touche = ""
		ano1 = 0
	
	if kk == 6:
		frame2.grid_remove()  ## fin sur frame de recherche
		#pass
		
	if kk == 7: ## bouton next Suivant de la recherche
		if len(trouve) == 0 :
			message ("pas d'autre occurence")
			return
			
		afficher_zone(trouve, 0) ## le 1er
		del trouve[0]	
		
		if len(trouve) == 0:
			bouton_next.grid_remove()
	 
	if kk == 8 :  ## Valide saisie criteres de tri pour edition
		#print (checkvar1.get() , "crit1:", crit1, "combo: ", my_combo_t1.get() )
		## verifier coherence Criteres et zones associées
		if checkvar1.get() == 1 :  ## crit1 coché
			if len ( crit1_name ) < 2:
				anomalie("critere-1 : il faut choisir un champ associé")
				return
		if checkvar2.get() == 1 :  ## crit1 coché
			if len ( crit2_name ) < 2:
				anomalie("critere-2 : il faut choisir un champ associé")
				return		
		if checkvar3.get() == 1 :  ## crit1 coché
			if len ( crit3_name ) < 2:
				anomalie("critere-3 : il faut choisir un champ associé")
				return	
		
		##YYY
		wmail = ent_mail.get()
		#print ("Mail: ", wmail)
		if len(wmail)>0:
			if isValidEmail(wmail) == False :
				anomalie("l adresse mail est invalide")
				return	
				
		rep =  filedialog.askdirectory()
		
		if len(rep) == 0:
			return
			
		frame3.grid_remove()  ## fin sur frame3  
		editer(rep)  ## lancement de l'edition
		
		if len(wmail)>0:
			fic_pdf = rep + "/" + nomfic + '.pdf'
			body_txt = """\n  
	Bonjour,\n
			
	Veuillez trouver le document en piece jointe.\n
			 
	Cordialement"""

			FROM="yvallet@ilta.fr"
			TO = wmail
			subject = "l\'edition demandee"
			envoi_mail(FROM, TO, subject, body_txt, fic_pdf)
			
			wmsg = "Mail envoyé a " + wmail
			message(wmsg)
				
		
	if kk == 9:   ## Abandon edition sur saisie criteres de tri
		frame3.grid_remove()  ## fin sur frame3   
			
	if kk == 10:  ## Bouton help sur ecran saisie criteres edition
		aide_criteres  = ('Saisie des informations determinant l\'ordre des '
						'informations pour l\'edition du fichier \n\n'
						'Tri avec rupture :                       \n'
						'Si réponse = OUI , l\'edition fera des sous '
						'totaux par critere de tri , avec un saut de '
						'page pour chaque critere-1                 \n '
						'Si réponse = NON , l\'edition sera triée selon '
						'le ou les criteres choisis, sans sous total ni '
						'saut de page par groupe                    \n\n '
						'Choix de critées utilisés :                  \n '
						'vous pouvez choisir de 1 a 3 criteres de tri '
						'Pour chaque critere, il faut indiquer dans la '
						'liste déroulante associée le champ concerné ,'
						'champs correspondants aux colonnes du tableau. '
						'Si aucun critere n\'est selectionné, l\'edition'
						' sera faite dans l\'ordre du tableau            ')
		afficher_aide(aide_criteres)			

## Controle validité adresse mail avec module re
def isValidEmail(email):
	if len(email) < 8:
		return False
	
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if(re.search(regex,email)):  
		return True 
	else:  
		return False
	
	"""
		if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
			return True
		else:
			return False	
	"""
 
def afficher_aide(texte):
		bg = "SlateGray3"
		bg = '#FFFFEA' 
		pad=(5, 3, 5, 3)
		
		
		fen2 = Toplevel(fenetre)
		#fen2.geometry('200x200')
		fen2.grid()
		
		#fen2.wm_overrideredirect(True)
		 
		frame4 = Frame(fen2, bg='SlateGray3', borderwidth=0 )                ## width=100, height=600  <== inutile, s'adapte avec les widgets contenus
		frame4.grid(row=0, column=6 , padx=10, pady=10, sticky="e")
		 		
		label_help = Label(frame4,  text=texte, justify=LEFT, background=bg, relief=SOLID, borderwidth=0, wraplength=250 )
		label_help.grid() ##padx=5 , pady=3 ,   sticky=NSEW)
		
		#s_width, s_height = fen2.winfo_screenwidth(), fen2.winfo_screenheight()
		#width  = pad[0] + label_help.winfo_reqwidth() + pad[2]
		#height = pad[1] + label_help.winfo_reqheight() + pad[3]
		#print (s_width, s_height, s_height, s_height)
		
		#fen2.wm_geometry("+%d+%d" % (width, height))
		
		 
		
		
	
################################################################
def lire_check1():
	global crit1
	if checkvar1 == 1:
		crit1 = "O"
	else:
		crit1 = "N"
	#print ("check1", crit1 )
		
def lire_check2():
	global crit2
	if checkvar2 == 1:
		crit2 = "O"
	else:
		crit2 = "N"
	#print ("check2", crit2 )
	
def lire_check3():
	global crit3
	if checkvar1 == 1:
		crit3 = "O"
	else:
		crit3 = "N"		
	#print ("check3", crit3 )	
	
def before_zone(events):
	global ano1, widget_ano, widget_en_cours, touche,  DEBUG, val
	#DEBUG=True
	#touche = ""  ## raz pour test en after field
	
	""" ################# mis dans la fonction makeform !!!!!!!!!!!!!!!!!!!!!!!!!
	# registering the observer 
	#   utilisation de le varibale de controle stringvar associee aux champs entry pour tracer le valeur saisie
	#   ici , pour limiter le nbre de caractere en input avec le pamatre maxi
	nom =  str(events.widget).split(".")[-1]
	x = ents[nom]
	maxi = table_maxi[nom]
	if maxi > 0:
		my_var = table_var[nom]
		##my_var.trace_add('write', my_callback() )
		my_var.trace("w", lambda name, index, mode, my_var=my_var, maxi=maxi: my_callback(name,index,mode,my_var, maxi) )  
	"""

	"""		
	if nom_court == "age":
		frame.event_generate('<Tab>')
		
	
		
	## tous les attributs lies a un objet **********************************************************************
	x = ents[nom] 
	printy ("dir : ", dir(x) )  ## tous les attributs de l'objet event ex: event.widget event.num, geight, width,...
	for attr in dir(x): 
		printy ("attribut: ",attr, '=>', getattr(x, attr))
		
	printy (x.config() )  ## <<= toutes les options et valeurs identique sequence ci dessus
	"""
	
	nom =  str(events.widget).split(".")[-1]
	printy ("focus sur zone ", nom , "cours:", ents[nom] , "ANO:", widget_ano , ano1, "touche: ", touche )
		
	if ano1 == 0:
		widget_ano = ents[nom] 
		printy(" remise ano a : ", widget_ano , "  en BEFORE ZONE ")
"""
 les controles de chaque zone 
""" 
def after_zone(events):
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG, val
	
	
	##printy ("events.widget:",events.widget 	)  ##> events.widget:   .!frame.l01prenom
	## split '.!frame.l01prenom' cree une liste de 2 elements avec le separateur '.' pour separer
	## [-1] prend le dernier de la liste 'l01prenom"
	
	nom =  str(events.widget).split(".")[-1]  ## nom associe au widget par envent
	widget_actuel = ents[nom]
	x = ents[nom].get()
	numlig = nom[1:3]
	wnum = int(numlig)
	printy (" ***** numlig: ", numlig)
		
	printy ("==================================================================")
	printy ("entree after zone ", nom , "actuel:", widget_actuel, "ANO:", widget_ano , ano1, "touche: ", touche)
	
	val = x.lstrip(" ")  ## sup blanc devant pourquoi un blanc ?!
	nom_court = nom[3:]  ## L01nom_zone , on elimine L01 
	
	printy ("debut after champ=", nom, " nomcourt= ", nom_court, " ano1:", ano1, "Actuel:", widget_actuel," ANO:",widget_ano)
	
	x =  str(widget_actuel.winfo_name).split(".")[-1] ; nom1 = x[0:-2]
	x =  str(widget_ano.winfo_name).split(".")[-1]      ; nom2 = x[0:-2]	
	
	printy("nom1 actuel / nom2 ano ==> ", nom1, nom2)
	
	if ano1 == -1:  ## demande de sortie par bouton01
		return
		
	printy ("ano1 ", ano1, "ano:", widget_ano, "actuel: ",widget_actuel)
	if (ano1 == 1 and widget_ano != widget_actuel):
		if len(touche)==0:
			printy ("ano1 + widget differt ==> RETURN   ano:", widget_ano, "actuel: ",widget_actuel )
			return
		else:
			if numlig == "01" and depassement == 0 and touche =="Up":
				printy ("deplacement impossible , 1ere ligne !")
				return
			if wnum == lige and ((lige + depassement) == ligt ) and touche =="Down":
				printy ("deplacement impossible , derniere ligne !")
				return
		return 	
			
	ano1 = 1
	
	## Controles Champs, specifique a ecrire #########################################
	printy ("Controles Champ ", nom_court)
	printy ("controle sur ", nom_court, "actuel: ", widget_actuel, "ANO:", widget_ano )
	
	ok = controle_champs(nom_court, val, nom)
	if ok == "OK":
		oks = controles_specifiques(nom_court, val, widget_actuel)
	
	printy ("sortie controle ok: ", ok,  "ano1:" , ano1)
	if ok == "KO" or oks == "KO":
		printy ("apres KO  nom=", nom, " nomcourt= ", nom_court, " ano1:", ano1, "focus ==> :",widget_actuel)
		
		widget_ano = widget_actuel
		widget_ano.focus_set()		         ## laisser le focus sur la zone en erreur
		return
		
	## Sortie sans erreur ############################################################
	 	
	memo_valeur (nom, val, nom_court, touche)                     ## memo dans le tablo 
	
	################# Sortie sans touche speciale = Fin de l'after field ########
	if len(touche) == 0:   
		ano1 = 0
		printy ("sortie sans erreur et sans touche  ", widget_actuel, widget_ano )
		if nom != nom_dernier :  ## case normale , suivant selon tab
			return
			
		if nom == nom_dernier :  ## derniere zone du tableau en cas a droite
			printy ("fin du tableau !!")
			if wnum == lige and ((lige + depassement) == ligt ) :  ## fin du tableau et capacite MAX atteinte ==> retour 1ere case
				printy ("nom / nom_dernier ", nom, nom_dernier)
				widget_premier.focus_set()
				return
			else:                                                  ## derniere case avec tab ou return , mais max pas atteint , sinuler down
				touche="Down"
				 
		
	######################## Sortie sans erreur sur touche Up/Down #########################################
	#   calcul prochaine zone focus, et decalage eventuel ecran
	
	if ano1 == -1:  ## cas on valide l'ecran par la touche Valide et on quitte ==> inutile calculer suivant
		return
		
	printy ("calcul_focus ==>>> calcul suivant",nom, touche, widget_ano ) 
	suivant = calcul_focus(nom, touche, widget_ano)
	
	printy ("retour calcul_focus ", suivant) 
	suivant.focus_set()
	
	frame.update()
	return
	
		
	#output = ''.join(hex(ord(c)) for c in val)  ## ord("A") ==>65  chr(65) ==> "A"  hex(65) ==> 41
	#printy ("HEX:", output)
				
			
def reorganiser (sens):
	global depassement, DEBUG
	
	##sens Up/Down
	if sens == "Down":
		newpos = lige + depassement + 1
	else:
		newpos = lige + depassement   ###+ 1
		
	##print ("sens:",sens, " newpos", newpos, "depassement avant ", depassement)	##1805
	
	if newpos > ligt:
		msg = "Impossible, Le tableau maximum est atteint : "+ str(ligt)
		anomalie(msg)
		return  ## depassement inchangé
		
	if sens == "Down":
		depassement +=1
		depart = newpos     
		fin    = depart - lige ##1805
	if sens == "Up":  ##Up
		depassement -=1
		depart = newpos - 1  ## car part de zero
		fin    = depart - lige ##1805
	
	## Mettre a jour le tableau
	printy("sens:",sens, " depassement: ", depassement)
		
	for z in range( len(table_zone) ):               ## 10 lignes ecran x 4 zones ==> 40 
		##printy ("==============================", z ,"=======================================")
		#nom_obj, col, wid, foc, entete, maxi,required, nature 
		nom, col, wid, foc ,entete, maxi , required, nature   = table_zone[z]
			
		##printy ("Reorg traitement zone : ", nom)            #traitement zone : ', 'l01nom')
		rang_ecran = int(nom[1:3])	  ## isole 04 dans l04nom = row a l'ecran

		#printy ("rang lu ", rang_ecran)		
		
		if sens == "Down":
			rang_tablo = rang_ecran + depassement
		else:
			rang_tablo = rang_ecran + depassement
			
		
		
		## clef pour le tablo interne  0001nom, 0001prenom =  row+nomcourt
		ii = "{:0>4d}".format(rang_tablo)  ## pour avoir "0001" , 0002, 
		nom_court = nom[3:]
		
		clef_tablo = ii + nom_court
		#printy ("clef_tablo: ", clef_tablo)  ## 0011l01nom
		#printy ("depass ", depassement, "ecran:", rang_ecran, "clef_tablo: ", clef_tablo 	)
			
		## Clef dans l'ecran
		clef_ecran = nom
					
		## acces tableau , si pas trouve RAZ (Nouvelle ligne)
		val = tablo.get (clef_tablo, "")
					
		cible = ents[clef_ecran]
		
		cible.delete(0, 'end')
		cible.insert(0, val )
		#printy ("clef_tablo: ", clef_tablo , "clef_ecran", clef_ecran, "Valeur: ", val )  #clef_ecran', 'l10l01nom'
		
		frame.update()
	

### Sortie sans erreur sur touche Up/Down , calcul prochaine zone focus, et decalge eventuel ecran
def calcul_focus(wnom, toutouche, focus_actuel):

		global ano1,  widget_ano, widget_en_cours, touche,  DEBUG
		
		touche = toutouche
		printy ("cakcul_focus deplacement : ", touche, "focus_actuel: ", focus_actuel, "ANO:", widget_ano )
		
		suivant, ok = deplacement(wnom, touche)
		##            DEPLACEMENT
		
		printy ("touche APRES deplacement : ", touche)
		printy ("ok:", ok, "suivant: ", suivant)
		
		if ok == 2: ##deplacement interdit
			touche=""
			widget_ano = focus_actuel ##0305
			return focus_actuel
		
		if ok == 1: ## on reste dans le cadre ecran
			widget_ano = suivant
			printy ("reste dans le cadre, suivant=", suivant)						
			touche=""	
			return suivant
						
		else:
			printy ("on reorganise TOUCHE ==> ", touche, "actuel:", focus_actuel, " ANO:", widget_ano)
			
			reorganiser(touche)
			
			printy("====Sortie de reorganiser")
			             
			if touche == "Down" :
				# calculer le zone derniere ligne du tableau pour y rester/revenir
				#wnom, col, wid, foc , maxi = zone1 ## 1ere zone parametree
				#depart = nom ## colonne actuelle
				#ii = "{:0>2d}".format(lige)        ## No derniere ligne
				#zone = "l" + ii  + nom
				printy ("recalculé dans le cas DOWN ", wnom)
				focus_actuel = ents[wnom]
			
			touche=""
			widget_ano = focus_actuel ## 0305 !!!!
			printy ("return focus_actuel : ", focus_actuel, "ano: ", widget_ano )
			
			widget_actuel = focus_actuel
			return focus_actuel                  ##widget_ano
												
	
		
def maj_up_down( fleche):
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG
		
	touche = fleche
	#print ("touche ", touche)
	##after_zone (frame.event_generate("<<FocusOut>>"))
	

def deplacement(origine, sens):
	global touche, DEBUG, flag
	
	##touche = ""  ## raz apres usage
	depart = origine
	nolig = int( depart[1:3])
	printy ("no ligne depart", nolig)
	if sens == "Up":
		arrivee = (nolig -1) 
	else:
		arrivee = (nolig + 1) 
	
	if sens == "Home": 
		arrivee = 1
		printy ("home nolig:",arrivee) 
		
				
	printy ("depart", depart, "arrivee ", arrivee, "depassement", depassement)
	if arrivee < 1 or arrivee > lige:  ##1805
		printy ("on sort du tableau  !!!")
		
		if sens == "Up" : 
			if depassement > 0:
				return "" , 0  ## on reorganiser
			else:
				printy ("arrivee : ", arrivee, "rien au dessus" )
				anomalie("Ce deplacement vers le haut est impossible")
									
				arrivee = nolig
				return widget_ano,2  ############ 2 = on ne fait rien , deplacement interdit #################################
				
		if sens == "Down": 
			if (arrivee+depassement) <= ligt:
				return "" , 0  ## on reorganiser
			else:
				printy ("arrivee : ", arrivee, "rien au dessus" )
				anomalie("Ce deplacement vers le bas est impossible")
									
				arrivee = nolig
				return widget_ano,2
				
				
	################# deplacement en restant  dans le tableau
	printy ("je reste dans le tableau ecran 1 a 10")  
	ii = "{:0>2d}".format(arrivee)
	
	if sens == "Home":                         ## pour revenir a l01nom
		wnom, col, wid, foc , maxi = zone1 ## 1ere zone parametree
		depart = wnom
		zone = "l" + ii  + wnom
		printy ("home ", wnom)
	else:
		zone = "l" + ii  + depart[3:]
		printy ("zone cible : ", zone) 
		
	widget_suivant = ents[zone]
	return widget_suivant , 1  ## ok=1 on ne reorganise pas mais on bouge dans l'ecran

def delete_row(nolig, depas):
	pass

def printy(*args):
	global DEBUG
	#printy ("printy debug:", DEBUG)
	if DEBUG == True:
		print (args)

def menu_csv():
	global ano1,  widget_ano, widget_en_cours, touche,  DEBUG
	touche = "Up"                  ## positionner a 'Up' pour pouvoir sortir de l'entry avec zone vide  
	ano1 = -1                      ## pour eviter calcul_focus
	 
	touche = ""
	ano1 = 0
	ecrire_csv("O")

def windows2():  ## menu Recherche
	frame2.grid()  ## fait apparaitre la frame2     (apres frame2.remove())  
	
	my_combo.focus_set()

def sel_bouton():
	choix = var_bouton.get()
	x = "option choisir : "+ str(choix) 
	#anomalie (x)
	
def after_combo(event):	
	global zone_choix
	
	widget = ents["my_combo"]
	zone_choix = widget.get()
	
	#print ("widget:", widget)
	#print ("combo , choix: ", zone_choix)

############### sortie zone de saisie de recherche #######################
def after_rech(event):
	global zone_choix   ##, trouve mutable
	
	choix_maj  = var_bouton.get()
	#print ("Maj: ", choix_maj)
	
	#print ("event : ", event.widget)
	nom1 =  str(event.widget).split(".")[-1]    #==>  .!frame.rech
	nom2 =  str(nom1).split(".")[-1]
	#print (nom1, nom2)
	
	widget = ents[nom2]
	cible = widget.get()
	if choix_maj == 2: ## ne pas tenir cte des Majuscules
		cible = cible.lower()
		
	#print (cible, " sur zone ", zone_choix )
	
	############ recherche #############
	t1=[]
	
	## raz
	del trouve[:]
	 
	
	for cle, val  in tablo.items():
		
		wnom = cle[4:]
		if wnom == zone_choix:
			nolig = int(cle[0:4])
			zone = [val, nolig]
			t1.append(zone) 
	
	for val, nolig in t1:
		if choix_maj == 2: ## ne pas tenir cte des Majuscules
			val = val.lower()
		ret = val.find(cible)  ## search etc module 're' expression regulieres
		if ret>-1:
			zone = [nolig, val]
			trouve.append(zone)
	
	trouve.sort()
		
	if len(trouve) == 0:
		message("rien trouvé pour cette recherche")
		return
		
	afficher_zone(trouve, 0) ## le 1er
	del trouve[0]
	
	if len(trouve) == 0:
		bouton_next.grid_remove()
		## invalider bouton next Suivant
	else: ## le valider
		bouton_next.grid()
		pass
	
def afficher_zone(t1, lig):
	global depassement, zone_choix
	
	#print (t1, "depasst ", depassement)
	numlig, val  = t1[lig]
	i1 = int(numlig)
		
	#print ("lig: ", numlig, "i1:",i1, "depass ", depassement)
	if i1 <= lige and depassement==0:
		##calcul zone ecran SI dans l'ecran!!  ii = "{:0>4d}".format(i) 
		ii = "{:0>2d}".format(i1)
		clef = "l"+ ii + zone_choix
		
		widget = ents[clef]
		flashColour(widget, 0,10)	
	
		#widget = ents["my_combo"]
		widget.focus_set()  ## sur la zone 
		return
		
	i = i1 - depassement
	
	if i1 > lige:
		prem = i1 - lige 
		der = i1 
		decalage = i1 - lige
		cible = "l10"+zone_choix
	else:
		der=lige
		prem = 0
		decalage = 0
		nn = i1 - depassement
		cible = "l" + "{:0>2d}".format(nn) + zone_choix
		 		
	for j in range (0,len(entrees)):
		if len(entrees[j]) > 1:
			nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			
			for ligne in range (der, prem, -1):
				## ligne tablo
				cle_tablo = "{:0>4d}".format(ligne)+nom
				val = tablo[cle_tablo]
					
				## widget ecran
				lig_ecran = ligne - decalage
				cle_ecran = "l"+ "{:0>2d}".format(lig_ecran)+nom
				 
				widget = ents[cle_ecran]
					
				widget.delete(0, 'end')
				widget.insert(0, val )
		
		
		widget = ents[cible]
		flashColour(widget, 0,10)	
		widget.focus_set()  ## sur la zone		
		depassement	= decalage			
		
def flashColour(object, colour_index, iter):
	iter -= 1
	if iter == 0:
		object.config(background ="white")
		return
	object.config(background = flash_colours[colour_index])
	fenetre.after(500, flashColour, object, 1 - colour_index, iter)				
	
################################################ MAIN ##############################################################

################ Parametres ########################################################
rupture = "N"

crit1="N"                            #<<= le 1er critere 
rang_crit1=0                         #<<= 5eme champ de la ligne ==> ville entrees[rang_crit1][5] 
crit1_name=""                        #<<= libelle associé

crit2="N"                            #<<= le 2eme critere
rang_crit2=0                         #<<= 4eme champ de la ligne ==> age  entrees[rang_crit2][5] 
crit2_name=""                        #<<= libelle associé

crit3="N"                            #<<= le 3eme critere  ICI, que 2 utilises
rang_crit3=0                         #<<= not used ici
crit3_name=""                        # entrees[rang_crit3][x]  


DEBUG = False		   ## mettre a 1 pour rend les printyv effectifs
flash_colours = ('white', 'blue')

mon_os = platform.system() ## windows/linux
nomfic = "fic_array"  ## Nom du fichier binaire enregistre, du csv et du pdf
choix_base = "Sqlite" ## defaut  Mysql/Sqlite

lige = 10 ##10             ## nbre de lignes a l'ecran NB : 15 Maxi
ligt = 20 ##15            ## nbre de lignes dans le tableau de saisie
nb_champ = 5          ## nbre de champ par ligne (pour sequence edition) ==> nom, prenom, date, age, ville

## param pour edition
title_fen="exercice Input Array V4"      ## titre fenetre
title = "Liste des clients "             ## titre report

table_zone=[]
ents = {}
table_var = {}
table_maxi = {}
trouve=[]  ## pour sequence recherche , liste des occurences trouvees

larg = 1350        ## taille fenetre
haut = 700

tablo = {} ## clef = 0001Nom_objet ,  value=valeur saisie
##                   Nolig de 0001 à ligt

touche=""      ## memo touche Up/Down quand utilises
fenetre = Tk()
fenetre.title(title_fen)

resolution = str(larg)+'x'+str(haut)+'+60+60'
fenetre.geometry(resolution)
#                 Larg x Haut
#fenetre.geometry('1150x700+60+60')

"""
## rendre fenetre responsive
for i in range(0,14):
	fenetre.rowconfigure(i, weight=1, minsize=700)
for j in range(0,5):
	fenetre.columnconfigure(j, weight=1, minsize=25)
"""

frame = Frame(fenetre, bg='red')                ## width=100, height=600  <== inutile, s'adapte avec les widgets contenus
frame.grid(row=0, column=0 , padx=10, pady=10 ) ##, rowspan=1, columnspan=1) ##, padx=20, pady=10)

#fenetre.grid_rowconfigure(0, weight=1)
#fenetre.grid_columnconfigure(0, weight=1)

#frame.grid_rowconfigure(0, weight=1)
#frame.grid_columnconfigure(0, weight=1)


## creation liste vide imbriquée 
n = 10  ## 10 elements maxi
m = 9   ##  1 liste de 9 par element ( Nom ,     Col Width takefocus=0/1  Entete   30=max.input  Required   Nature, unicite  )
entrees = [[0] * m for i in range(n) ]
for i in range (0,n):
	entrees[i]=[]

####################################### Lecture des parametres #####################################################



nomfic = "param_testfic"  ## <==========================

fic = nomfic + ".csv"
	
with open( fic , mode='r' ,newline='' ) as fichier_csv:
	objet_csv = csv.reader( fichier_csv , delimiter=';',  quotechar='"', quoting=csv.QUOTE_MINIMAL) 
	
	i = 0
	for row in objet_csv:  
		i += 1
		
		##	if debut == 0:
		##		debut = 1  ## sauter la 1ere ligne entete de colonnes
		##	else:	
		
		#print (row)  ## row = 1 enregt complet sous forme de liste
		
		champ=row[0]
		valeur=row[1]
		
		if i < 9:
		
			if champ == "xnomfic":
				nomfic=valeur
				
			if champ == "xbase":
				if valeur == "1": ### YY 1=OK
					choix_base = "Mysql"
				else:
					choix_base = "Sqlite"
				
				
			if champ == "xlige":
				lige=int(valeur)
				
			if champ== "xligt":
				ligt=int(valeur)
				
			if champ == "xnbchamp": 
				nb_champ=int(valeur)
				
			if champ == "xtitre_app":
				title_fen = valeur ; fenetre.title(title_fen)
			if champ == "xtitre_edi":
				title = valeur
			if champ == "xlargeur":
				larg = int(valeur)
			if champ == "xhauteur":
				haut = int(valeur)
				resolution = str(larg)+'x'+str(haut)+'+60+60' 
				fenetre.geometry(resolution)
				
		if i > 9:
			lig = int(champ[1:3]) - 10
			nom_court = champ[3:]
			
			#print ("lig", lig, nom_court, champ, valeur)
			
			if nom_court == "nom" :    
				p1 = valeur
			if nom_court == "entete" : 
				p5 = valeur
			if nom_court == "col" :    
				p2 = int(valeur)
			if nom_court == "wid" :    
				p3 = int(valeur)
			if nom_court == "foc" :    
				p4 = int(valeur)
			if nom_court == "maxi" :   
				p6 = int(valeur)
			if nom_court == "req" :    
				p7 = valeur
			if nom_court == "nature" : 
				p8 = valeur
			if nom_court == "unicite" : 
				p9 = valeur
				entrees[lig]=[p1,p2,p3,p4,p5,p6,p7,p8,p9]

print ("choix_base:", choix_base )

if choix_base == "Mysql":
	import mysql.connector as lite
	from mysql.connector import Error
	connexion = lite.connect(host='localhost', database='ga4', user='root',  password='saanar')
else:
	## sqlite
	import sqlite3 as lite
	nom_base =  "C:/Users/yvall/Exos_python_win/ga4.db"
	#print (nom_base)
	connexion = lite.connect(nom_base, timeout=20)
	
	
	#print (entrees)
"""	
	
###### Parametrage des zones d'entry dans chaque ligne ENTRY , NB nbre ligne fixé dans la var lige ci dessus
#
#
##             Nom ,     Col Width takefocus=0/1  Entete   30=max.input  Required   Nature(alpha/date/entier/decimal/none)
##             -------   --   ---   ---          ------------  -----        ---       -----   Unicité 
entrees[0] = ["nom",      1 ,  35 ,  1 ,          "Nom "        ,30       , "O"    , "alpha" , "O" ]
entrees[1] = ["prenom",   2 ,  35 ,  1 ,          "Prenom"      ,30       , "O"    , "alpha" , "N" ]
entrees[2] = ["datnais",  3 ,  20 ,  1 ,          "Date Naiss." ,10       , "O"    , "date"  , "N" ]		
entrees[3] = ["age",      4 ,  5  ,  0 ,          "age"         ,3        , "N"    , "none"  , "N" ]            ## focus 0
entrees[4] = ["ville",    5 ,  25 ,  1,           "Ville"       ,20       , "O"    , "alpha" , "N" ]
entrees[5] = []
entrees[6] = []
entrees[7] = []
entrees[8] = []
entrees[9] = []

"""





############################ parametrage des boutons####################################################
#            text     bg        relief    row  col width   centrage   
#  centrage : "w" west =gauche  "e" =east droite ""=centre   dans la colonne  
## Cyan, SeaGreen

n = 10  ## 10 elements
m = 8  ##  1 liste de 8 par element 

boutons = [[0] * m for i in range(n) ]

#             text           bg           relief    row  col width   centrage       image
boutons[0] = [ "Valider",    "SeaGreen", "raised" ,  13 , 1 ,  45 ,   "w"   ,   "valide1.png"   ]   ## = bouton 1 (NB decalage de 1)
boutons[1] = []                                                                                     ##   bouton 2
boutons[2] = [ "Delete",     "SkyBlue" , "raised" ,  13 , 2 ,  45 ,   ""  ,     "poubelle3.png" ]
boutons[3] = [ "Insert" ,    "SkyBlue" , "raised" ,  13 , 3 ,  45 ,   ""  ,     "open1.png"     ]
boutons[4] = [ "Abandon"   , "SkyBlue" , "raised" ,  13 , 5 ,  45,    "e" ,     "sortie1.png"    ]
boutons[5] = []
boutons[6] = []
boutons[7] = []
boutons[8] = []
boutons[9] = []                                                                                    ## bouton 10

######################### preparation de la table table_zone
# garnir table_zone :  contient lige x Nbre de zones d'entres  Ici : 10 x 5 = 50 champs ( 1 par entry d'affichage )
##################################################################################################
for i in range(1,lige+1):
				
	ii = "{:0>2d}".format(i)  ## pour avoir "01" , 02, ... 10
	
	for j in range (0,len(entrees)):
		##print ("===========", j , "====================")
		##print (entrees[j])	
				
		if len(entrees[j]) > 1:
			#Nom ,     Col Width takefocus=0/1  Entete   30=max.input  Required   Nature, unicite 
			nom, col, wid, foc , entete, maxi , required, nature , unicite = entrees[j]
			
			nom_obj = "l"+ ii + nom  ## nom = l01+nom_court , l02+nomcourt ...
			zonet = [nom_obj, col, wid, foc, entete, maxi,required, nature ]
			table_zone.append(zonet)
			if j == 0:
				nom_premier = nom
			nom_dernier = nom
			
nom_premier = "l01"+nom_premier           ##1ere zone ecran
ii = "{:0>2d}".format(lige)
##iii = str(lige).zfill(2)


nom_dernier = "l" + ii + nom_dernier      ##derniere zone
	
printy ("premier /dernier ", nom_premier, nom_dernier)



######################################## Instanciation des zones d'entry ##########################################################
## table_zone conient  lige (10) x nbre d'entry (zone1 a zone10 si informees)
##      ici 10 x 5 = 50 elements de dict avec clef="l01nom_entree", valeur=objet entry  pour la ligne ecran 01
##                                                  l02nom_entree                       pour la ligne ecran 02
##                                                  lNNnom_entree                       pour la ligne ecran NN = lige
for z in range( len(table_zone) ):
	
	nom_obj , col, wid, foc , entete , maxi , required, nature = table_zone[z]
	#printy ("create z: ",z, "nom: ", nom_obj)
	
	##wrow = int(nom_obj[1:3] )       ##       l01 ==> 01
	wrow = int(nom_obj[1:3] )  + 1
	
	nom_string = StringVar(frame, name="stringvar_"+nom_obj)
	nom_string.trace("w", lambda name, index, mode, my_var=nom_string, maxi=maxi: my_callback(name,index,mode,my_var, maxi) )
	
	ent = Entry(frame,  name=nom_obj, bg="white",   width=wid, relief=GROOVE , textvariable=nom_string)
	ent.grid   (row=wrow, column=col,padx=10,pady=10, sticky='nw'  )
	
	#table_var[nom_obj]  = nom_string  ## objets strinvar associés aux entry  <======== Ne sert plus
	#table_maxi[nom_obj] = maxi        ## longueur maxi a controler en entry            Ne sert plus
	
	ent.config(takefocus=foc)
	ent.bind("<FocusIn>", before_zone) 
	ent.bind("<FocusOut>", after_zone)
	ent.insert(0,"")                      ## pas " " sinon besoin tronque
	ents[nom_obj] = ent
	
	
widget_en_cours = ent  ## pour init des globals
widget_ano      = ent
 

############################# Les Labels ( ligne d'ENTETE ) #############################################################################
##                            avec la zone entete du tableau entrees

for j in range (0,len(entrees)):
			 				
	if len(entrees[j]) > 1:
		 
		nom, wcol, wid, foc , entete, maxi , required, nature, unicite  = entrees[j]
		
		wbg = "yellow"
		wfg = "black"
		wrow = 1 
		wrelief = "groove"
		wanchor = "center"
			
		wid = wid - 5
		# wid-10 au lieu 5
		labelxx = Label(frame, padx=15, width=wid , height=2,  text=entete, bg=wbg,   fg=wfg, relief=wrelief, anchor=wanchor )
		labelxx.grid(row=wrow, column=wcol, padx=5, pady=5 )


#################### instanciation des Boutons en pied  ####################################################
tab_img=[]

if mon_os == "Windows":
	directory = "C:\\icones\\"
else:
	directory = "/mnt/c/icones/"
 
for j in range (0,len(boutons)):

	if len(boutons[j]) > 1:  ######## pour avoir un objet image different par bouton
		wtext, wbg, wrelief, wrow , wcol , wid , centrage , wimage = boutons[j]
		if len(wimage) > 1:
				img = PhotoImage(file = directory +  wimage ).subsample(2,2)  
		else:
			img=""
			
	if len(boutons[j])  == 0:
		img=""
		
	tab_img.append(	img )
		
		
for j in range (0,len(boutons)):
	if len(boutons[j]) > 1:
		x = j+1
		wtext, wbg, wrelief, wrow , wcol , wid , centrage , wimage = boutons[j]	
		
		wrow = lige+2  ## en fin de tableau
		if len(wimage)>1:
			wbg = "white"  ## si une image sur le bouton, enlever la couleur
			
		bouton = Button(frame, bg=wbg, text=wtext, relief=wrelief, command=lambda my_var=x:test_bouton(my_var), width=wid, image=tab_img[j], compound = BOTTOM, takefocus=0)
		bouton.grid (row=wrow , column=wcol, padx=15, pady=10, sticky=centrage ) # sticky=W  aligné west dans la colonne
		


################################### ENTETE Boutons tri #######################################
tab_img2=[]
tab_img3=[]

if mon_os == "Windows":
	directory = "C:\\icones\\"
else:
	directory = "/mnt/c/icones/"
	
wimage2 = "tri6.png"
wimage3 = "tri4.png"
		
for j in range (0,len(entrees)):
	
	if len(entrees[j]) > 1:  ######## pour avoir un objet image different par bouton
		img = PhotoImage(file = directory +  wimage2 ) 
		img2 = img.subsample(3,3)
		img = PhotoImage(file = directory +  wimage3 ) 
		img3 = img.subsample(3,3)
	else:
		img2=""
		img3=""
		
	tab_img2.append(img2)
	tab_img3.append(img3)
		
for j in range (0,len(entrees)):
				
	if len(entrees[j]) > 1:
		nom, wcol, wid, foc , entete, maxi , required, nature, unicite  = entrees[j]
		wbg = "white"
		wfg = "black"
		wrow = 0
		wrelief = "groove"
		wanchor = "center"
		entete=""
		
		i = j + 1
			
		wid = 20
		
		tete = Button(frame, text=entete, bg=wbg, fg=wfg,  relief=wrelief ,command=lambda my_var=i, sens="A":tri(my_var, sens), width=wid , image=tab_img2[j]) ##, compound = BOTTOM )
		tete.grid (row=wrow , column=wcol,  sticky="w", padx=5 , pady=5 ) ##,padx=10, pady=10)    # sticky=W  aligné west dans la colonne
		
		tete = Button(frame, text=entete, bg=wbg, fg=wfg,  relief=wrelief ,command=lambda my_var=i,sens="D":tri(my_var, sens), width=wid , image=tab_img3[j]) ##, compound = BOTTOM )
		tete.grid (row=wrow , column=wcol,  sticky="e", padx=5 , pady=5 ) ##,padx=10, pady=10)  sticky="e"  aligné est dans la colonne

	
"""	
## TEST et exemple  recherche element d'une zone avec son nom
for z in range( len(table_zone) ):
	obj = table_zone[z]
	#printy (obj)
	try:
		x = obj.index("l05nom")
		break
	except:
		continue
	
nom, col, wid, foc , entete, maxi , required, nature = table_zone[x]
printy ("=======pour l05nom=============")
printy (nom, col, wid, foc , entete, maxi , required, nature)

"""


#####################################################################################

depassement = 0      ## incremente de 1 quand on depasse l'ecran par down
#                    ## decremente de 1 quand on depasse l'ecran par Up

flag=0
ano1 = 0             ## flag positionné en cas d'erreur sur after field , pour rester/revenir sur la zone erronnee
##                   ## lie a la zone widget_ano = l'objet en erreur

## ents       dict des widgets               ,   associes aux noms des widgets
## table_var  dict des stringvar                <+++ Not used , le maxi controlé avec  nom_string.trace des entry
## table_maxi dict des longeurs maxi en entry   <+++ Not used , le maxi controlé avec  nom_string.trace des entry
 
###ents , table_var, table_maxi  = makeform()  ## le dico des objets


############################# Menu pour test ############################################
menubar = Menu(frame)
menubar.add_command(label="Cree fichier csv ", command=menu_csv)
menubar.add_command(label="Recherche ",        command=windows2 )
menubar.add_command(label="Edition ",          command=edition )
menubar.add_command(label="Quitter",           command=lambda my_var=5:test_bouton(my_var) )  ## faire comme bouton 5


fenetre.config(menu=menubar)
#########################################################################################

widget_premier  = ents[nom_premier]
widget_dernier  = ents[nom_dernier]
widget_ano      = widget_premier
widget_en_cours = widget_premier
widget_ano.focus_set()

##zone_choix= ents[nom_premier]  #pour init

# test bouton01.config(fg='red') 

fenetre.bind('<Return>', lambda x:fenetre.event_generate('<Tab>'))   ## RETURN ++> TAB
fenetre.bind('<Down>',   lambda x:[ maj_up_down( "Down") , fenetre.event_generate('<Tab>')] )  ## fait les 2 fonctions consecutivemt
fenetre.bind('<Up>',     lambda x:[ maj_up_down( "Up")   , fenetre.event_generate('<Tab>')] )
fenetre.bind('<Home>',   lambda x:[ maj_up_down( "Home") , fenetre.event_generate('<Tab>')] )

fenetre.protocol('WM_DELETE_WINDOW', lambda my_var=5:test_bouton(my_var) )  ## le bouton windows quit (croix) agit comme le bouton Abondon (5)
charger()  ## chargment nomfic


################## creer l'ecran de recherche dans la meme fenetre #################################################################

fond = "SlateGray3"
	
frame2 = Frame(fenetre, bg='SlateGray3')                ## width=100, height=600  <== inutile, s'adapte avec les widgets contenus
frame2.grid(row=0, column=6 , padx=10, pady=10, sticky="e")

	
lab1 = Label(frame2, padx=10, width=30,  text="Selectionnez une zone de recherche", bg="yellow", fg="black") ##, relief=GROOVE, anchor="center" )
lab1.grid(row=0,padx=10, pady=10,sticky='nw' )
	
champs=[]
for j in range(0, len(entrees) ):
	if len(entrees[j])>0:
		col_tri = entrees[j][0]
		maxi = entrees[j][5]
			 
		champs.append (col_tri)
		
#print (champs)
	
my_combo = ttk.Combobox( frame2 , name="my_combo" , value=champs  , width=35 , height=30 )
my_combo.grid (row=1, column=0 ,padx=10, pady=5,  sticky="nw" )
my_combo.current(0)  ## default
#my_combo.bind("<<ComboboxSelected>>", lire_combo)
	
my_combo.bind("<FocusOut>", after_combo)	
ents["my_combo"] = my_combo
 
#lab2 = Label(frame2, padx=10, width=30,  text="Valeur recherchée", bg="yellow", fg="black") ##, relief=GROOVE, anchor="center" )
#lab2.grid(row=8,padx=10, pady=10,sticky='nw' )
	
############ ligne vide en haut ####################################################################################
vide10 = Label(frame2, padx=10, width=30,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide10.grid(row=6,padx=10, pady=10,sticky='nw' )  ## en haut
#vide20 = Label(frame2, padx=10, width=30,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
#vide20.grid(row=7,padx=10, pady=10,sticky='nw' )  ## en haut
	
	
lab2 = Label(frame2, padx=10, width=30,  text="Valeur recherchée", bg="yellow", fg="black") ##, relief=GROOVE, anchor="center" )
lab2.grid(row=8,padx=10, pady=10,sticky='nw' )
	
nom_string = StringVar(frame2)
nom_string.trace("w", lambda name, index, mode, my_var=nom_string, maxi=maxi: my_callback(name,index,mode,my_var, maxi=30) )
		
rech = Entry(frame2,  name="rech", bg="white",   width=40, relief=GROOVE , textvariable=nom_string)
rech.grid   (row=11, column=0,padx=10,pady=10, sticky='nw'  )
rech.bind("<FocusOut>", after_rech)
ents["rech"]=rech

var_bouton = IntVar()
option1 = Radiobutton(frame2, text="Oui Tenir compte des majuscules",  variable=var_bouton, value=1, command=sel_bouton, height=1) ##, width=30 )  
option1.grid (row=9,column=0, padx=5, pady=5, sticky='nw' )
	
option1 = Radiobutton(frame2, text="Non",                              variable=var_bouton, value=2, command=sel_bouton , height=1) ##, width=30 ) 
option1.grid (row=10,column=0, padx=5, pady=5, sticky='nw' )    ## centre ,sticky='ne' )
var_bouton.set(1) ## val defaut
	
if mon_os == "Windows":
	directory = "C:\\icones\\"
else:
	directory = "/mnt/c/icones/"
	
wimage = "sortie1.png"
img = PhotoImage(file = directory +  wimage ).subsample(2,2)  
			
bouton = Button(frame2, bg="white", text="sortie", relief=wrelief, command=lambda my_var=6:test_bouton(my_var), width=30, image=img, compound = BOTTOM, takefocus=0)
bouton.grid (row=12 , column=0, padx=15, pady=10, sticky="e" ) # sticky=W  aligné west dans la colonne

wimage = "suivant1.png"
img9 = PhotoImage(file = directory +  wimage ).subsample(2,2)  
bouton_next = Button(frame2, bg="white", text="Suivant", relief=wrelief, command=lambda my_var=7:test_bouton(my_var), width=35, image=img9, compound = BOTTOM, takefocus=0)
bouton_next.grid (row=12 , column=0, padx=15, pady=10, sticky="w" ) # sticky=W  aligné west dans la colonne

bouton_next.grid_remove()
frame2.grid_remove()



################################################## frame3 ##############################################################################################
################## creer l'ecran de Saisie des criteres de tri pour l'edition  dans la meme fenetre #################################################################

fond = "SlateGray3"
	
frame3 = Frame(fenetre, bg='SlateGray3')                ## width=100, height=600  <== inutile, s'adapte avec les widgets contenus
frame3.grid(row=0, column=6 , padx=10, pady=10, sticky="e")
	
lab30 = Label(frame3, padx=10, width=35,  text="Edition : Selectionnez Les criteres de Tri", bg="red", fg="black") ##, relief=GROOVE, anchor="center" )
lab30.grid(row=0,column=0 , padx=5, pady=10, columnspan=2 )  #sticky='nw',


#wimage = "help.png"
#img31 = PhotoImage(file = directory +  wimage ).subsample(2,2) 

lab31 = Label(frame3, padx=5, width=20,  text="Tri avec Rupture  :", bg="yellow", fg="black" )   ##, image=img31,compound = RIGHT) 

"""
lab31.image = img31
lab31.configure (width=120, height=15 )
lab31.focus_set()
lab31.bind("<F1>", f1_click(1))
##print (dir(img31))
"""
lab31.grid(row=2,column=0 , padx=10, pady=10,sticky='nw' )


checkrup = StringVar()
c1_rup = Radiobutton(frame3, padx=0, pady=0, text = "Oui",  variable = checkrup, value="O", height=2 ) ## onvalue = 1, offvalue = 0,   width = 6, height=0 )
c2_rup = Radiobutton(frame3, padx=0, pady=0, text = "non",  variable = checkrup, value="N", height=2) ## onvalue = 1, offvalue = 0,   width = 6, height=0 )
c1_rup.grid(row=2, column=1,  sticky="nw")
c2_rup.grid(row=2, column=1 ) ##, sticky="ne" )                ##  Centre par defaut sticky="ne")
c2_rup.select()  

#c1_rup.bind("<F1>", f1_click(1)) 
#c2_rup.bind("<F1>", f1_click(2)) 

##c1_rup.unselect()  
	
champs2=[]
for j in range(0, len(entrees) ):
	if len(entrees[j])>0:
		col_tri = entrees[j][0]
		champs2.append (col_tri)
		
#print (champs)

## 3 combos pour selectionnnner les zones de tri pour les 3 criteres	
my_combo_t1 = ttk.Combobox( frame3 , name="my_combo_t1" , value=champs2  , width=20 , height=30 )
my_combo_t1.grid (row=4, column=1 ,padx=5, pady=5,  sticky="nw" )
##my_combo_t1.current(0)  ## default sur la 1ere zone (nom)
##my_combo_t1.bind("<FocusOut>", after_zone)	## faire controles_specifiques pour tester les valeurs choisies
my_combo_t1.bind("<<ComboboxSelected>>", lire_combo_t1)
ents["my_combo_t1"] = my_combo_t1

my_combo_t2 = ttk.Combobox( frame3 , name="my_combo_t2" , value=champs2  , width=20 , height=30 )
my_combo_t2.grid (row=5, column=1 ,padx=5, pady=5,  sticky="nw" )
##my_combo_t2.current(0)  ## default
##my_combo_t2.bind("<FocusOut>", after_zone)	
my_combo_t2.bind("<<ComboboxSelected>>", lire_combo_t2)
ents["my_combo_t2"] = my_combo_t2

my_combo_t3 = ttk.Combobox( frame3 , name="my_combo_t3" , value=champs2  , width=20 , height=30 )
my_combo_t3.grid (row=6, column=1 ,padx=5, pady=5,  sticky="nw" )
##my_combo_t3.current(0)  ## default
##my_combo_t3.bind("<FocusOut>", after_zone)	
my_combo_t3.bind("<<ComboboxSelected>>", lire_combo_t3)
ents["my_combo_t3"] = my_combo_t3
	
	
### ligne vide en haut 
#vide310 = Label(frame3, padx=10, width=20,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
#vide310.grid(row=2,padx=5, pady=10,sticky='nw' )  ## en haut

#vide20 = Label(frame2, padx=10, width=30,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
#vide20.grid(row=7,padx=10, pady=10,sticky='nw' )  ## en haut

lab32 = Label(frame3, padx=5, width=20,  text="Cochez les Criteres utilisés :", bg="yellow", fg="black") ##, relief=GROOVE, anchor="center" )
lab32.grid(row=3,column=0 , padx=10, pady=10,sticky='nw' )
	
checkvar1 = IntVar()  ## acces dans lire_combo_t1 , avec checkvar1.get()
checkvar2 = IntVar()	
checkvar3 = IntVar()
#                                                                                                                                      ##    notused
c1 = Checkbutton(frame3, padx=0, pady=0, text = "Critere-1", variable = checkvar1,  onvalue = 1, offvalue = 0,   width = 6, height=0 ) ## command=lire_check1 )
c2 = Checkbutton(frame3, padx=0, pady=0, text = "Critere-2", variable = checkvar2,  onvalue = 1, offvalue = 0,   width = 6, height=0 ) ## command=lire_check2 )
c3 = Checkbutton(frame3, padx=0, pady=0, text = "Critere-3", variable = checkvar3,  onvalue = 1, offvalue = 0,   width = 6, height=0 ) ## command=lire_check3 ))


checkvar1.set(True)  ## default sur crit1 
#checkvar1.select()  Fait la meme chose

c1.grid(row=4, column=0) ##,  sticky="nw")
c2.grid(row=5, column=0) ##, sticky="nw" )                ##  Centre par defaut sticky="ne")
c3.grid(row=6, column=0) ##,  sticky="nw")	


vide310 = Label(frame3, padx=10, width=20,  text=".", bg=fond, fg=fond) ##, relief=GROOVE, anchor="center" )
vide310.grid(row=7,padx=5, pady=10,sticky='nw' )  

lab33 = Label(frame3, padx=5, width=20,  text="Adresse si envoi par Mail", bg="yellow", fg="black") ##, relief=GROOVE, anchor="center" )
lab33.grid(row=8,column=0 , padx=10, pady=2, sticky='nw' )	

	
adr_mail = StringVar(frame3, name="adr_mail")
adr_mail.trace("w", lambda name, index, mode, my_var=adr_mail, maxi=50: my_callback(name,index,mode,my_var, maxi) )
	
ent_mail = Entry(frame3,  name="mail", bg="white",   width=50, relief=GROOVE , textvariable=adr_mail )
ent_mail.grid   (row=9, column=0,padx=10,pady=2, sticky='nw', columnspan=2  )
	
if mon_os == "Windows":
	directory = "C:\\icones\\"
else:
	directory = "/mnt/c/icones/"
	
wimage = "sortie1.png"
img30 = PhotoImage(file = directory +  wimage ).subsample(2,2)  
bouton = Button(frame3, bg="white", text="Quit", relief=wrelief, command=lambda my_var=9:test_bouton(my_var), width=30, image=img30, compound = BOTTOM, takefocus=0)
bouton.grid (row=12 , column=1, padx=15, pady=10, sticky="e" ) # sticky=W  aligné west dans la colonne

wimage = "valide1.png"
img31 = PhotoImage(file = directory +  wimage ).subsample(2,2)  
bouton_next = Button(frame3, bg="white", text="Valide", relief=wrelief, command=lambda my_var=8:test_bouton(my_var), width=35, image=img31, compound = BOTTOM, takefocus=0)
bouton_next.grid (row=12 , column=0, padx=15, pady=10, sticky="w" ) # sticky=W  aligné west dans la colonne

wimage = "help2.png"
img32 = PhotoImage(file = directory +  wimage ).subsample(2,2)  
bouton = Button(frame3, bg="white", text="Help", relief=wrelief, command=lambda my_var=10:test_bouton(my_var), width=30, image=img32, compound = BOTTOM, takefocus=0)
bouton.grid (row=12 , column=1, padx=15, pady=10, sticky="w" ) # sticky=W  aligné west dans la colonne

frame3.grid_remove()


fenetre.mainloop()

#################################################################################################################################################
###fenetre.overrideredirect(True)                       ## interdit quitter Et redimensionner
###fenetre.protocol('WM_DELETE_WINDOW',neant )          ## <== le bouton n'agit pas, sans message


