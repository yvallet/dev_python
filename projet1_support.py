#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.3
#  in conjunction with Tcl version 8.6
#    May 30, 2020 07:45:52 PM CEST  platform: Windows NT
#    May 30, 2020 11:01:31 PM CEST  platform: Windows NT

from tkinter import messagebox
import sys

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
	
	
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def init(top, gui, *args, **kwargs):
    global w, top_level, root, ano
    w = gui
    top_level = top
    root = top
    ano = 0
	
    ##YV
    zone1.trace("w", lambda name, index, mode, my_var=zone1, maxi=10: my_callback(name,index,mode,my_var, maxi) )
    zone2.trace("w", lambda name, index, mode, my_var=zone2, maxi=20: my_callback(name,index,mode,my_var, maxi) )

def sortie():  ## command sur bouton Sortie
    #print('projet1_support.sortie')
    sys.stdout.flush()
    destroy_window()

def after_entry1(*args):
    global ano
    
    val= w.Entry1.get()
    print ("entrey1 Val: ", val, "Ano:", ano)
   
    print ("val:", val, "ano:",ano)
	
    if ano>0 and ano !=1 :
          print ("after1 saute", ano )
          return
		  
    ano = 1

    if len(w.Entry1.get())<1:
        anomalie ("Zone1 doit etre informee")
        w.Entry1.focus_set()
        return
        
    if val != "ABC":
        anomalie("doit etre abc")
        w.Entry1.focus_set()
        return
	
    ## OK
    ano = 0
    return True

def after_entry2(*args):
    global ano

    val = w.Entry2.get()
	
    print ("entre2 val:", val, "ano:",ano)
	
    if ano>0 and ano !=2 :
        print ("entre2 saute", ano )
        return
           
    ano = 2 
	
    if len(w.Entry1.get())<1:
        w.Entry1.focus_set()
        return

    if len(w.Entry2.get())<1:
         if len(w.Entry1.get())>0:
             anomalie ("Zone2 doit etre informee")
             w.Entry2.focus_set()
             return
			 
    if w.Entry2.get() != "BCA":
        anomalie ("doit etre BCA  entre2")
        w.Entry2.focus_set()
        return
   
    ano = 0
    return True

##
def my_callback(var, indx, mode, my_var, maxi):
    ll = len(my_var.get())
    #print ("ll",ll,"maxi",maxi)
    if ll > maxi:
        print ( chr(7) , end=' ' , flush=True)              ## beep OK , mais fait in saut de ligne, sauf end=' '
        tronque = my_var.get()
        my_var.set(tronque[0:maxi] )


def set_Tk_var():
    global zone1, zone2
    zone2 = tk.StringVar()
    zone1 = tk.StringVar()

def xxx(p1):  ## Bind pour Return sur les zones d'Entry
    #print('projet1_support.xxx')
    #
    sys.stdout.flush()
    root.event_generate('<Tab>')
	
def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import projet1
    projet1.vp_start_gui()




