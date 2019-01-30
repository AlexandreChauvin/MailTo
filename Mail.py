import csv
import re
from os import system
import requests
from tkinter import *
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def verificationMail(adresseVerif):
    verif = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', adresseVerif)
    return verif
def verificationAllAdresse(tblAdresse):
    for row in tblAdresse:
        if verificationMail(row) == None:
                print("KO")
        else:
                print("OK")
def verificationUrl(adresseUrl):
    verif = re.match('^http://.*$|https://.*$',adresseUrl)
    return verif
def lectureCsv(nomFichier):
    tbl = []
    with open(nomFichier, 'r') as csvfile:
        lignes = csv.reader(csvfile, delimiter=';')
        for ligne in lignes:
            tbl.append(ligne[0])
    return tbl
def ecritureCsv(nomFichier,tbl):
    with open(nomFichier,'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in tbl:
            writer.writerow([row])
def reecritureCsv(nomFichier,tbl):
    with open(nomFichier,'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in tbl:
            writer.writerow([row])
def emailDomaine(email):
    if verificationMail(email) != None:
        email = email.split('@')
        email = email[1]
    else:
        email = None
    return email
def pingDomaine(domaine):
    #False Ping réussi True ping raté
    valeur = system('ping' + ' ' + domaine)
    return (bool(valeur))
def supprimerDoublonListeBox(listeBox,tbl,nomFichier):
    tbl = list(set(tbl))
    listeBox.delete(0,END)
    for row in tbl:
        listeBox.insert(END,row)
    listeBox.pack()
    reecritureCsv(nomFichier,tbl)
def supprimerEmailInMailList(tbl,email):
    tbl.remove(email)
def crawlerUrl(url,listeBox,nomFichier):
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    tblEmail = []
    for row in s.findAll('a'):
        mailto = row.get('href')
        if mailto.__contains__('mailto'):
            email = mailto.split(':')[1]
            if verificationMail(email) != None:
                tblEmail.append(email)
    for row in tblEmail:
        listeBox.insert(END,row)
    listeBox.pack()
    ecritureCsv(nomFichier,tblEmail)
    return tblEmail
def inportCsv(nomFichierLecture,listeBox,nomFichier):
    tbl = lectureCsv(nomFichierLecture)
    ecritureCsv(nomFichier,tbl)
    for row in tbl:
        listeBox.insert(END,row)
    fenetreImportCsv.destroy()
def fenetreGestion():
    fenetreGestion = Tk()
    fenetreGestion.title("Gestion")
    nomFichier = entryCsv.get() + ".csv"
    tbl = lectureCsv(nomFichier)
    fenetreAccueil.destroy()
    listBoxMail = Listbox(fenetreGestion, width=50)
    #Boutons
    #tbl = supprimerDoublon(tbl)
    bouttonDedoublonage = Button(fenetreGestion, text="Dedoublonner", command=lambda: supprimerDoublonListeBox(listBoxMail,tbl,nomFichier)).pack()
    bouttonVerification = Button(fenetreGestion, text="Verification", command=lambda: verificationAllAdresse(tbl)).pack()
    bouttonImportCsv = Button(fenetreGestion, text="Import CSV", command=lambda: fenetreImportCsv(listBoxMail,nomFichier)).pack()
    bouttonImportUrl = Button(fenetreGestion, text="Import URL", command=lambda: fenetreImportUrl(listBoxMail,nomFichier)).pack()
    #Lecture CSV
    for row in tbl:
        listBoxMail.insert(END, row)
    listBoxMail.pack()
    bouttonValider = Button(fenetreGestion, text="OK", command=lambda:fenetreMail(listBoxMail)).pack()
    fenetreGestion.mainloop()

def fenetreMail(listeBox):
    fenetreMail = Tk()
    fenetreMail.title("Mail")
    lblExpediteur = Label(fenetreMail, text="Expediteur").pack()
    entryExpediteur = Entry(fenetreMail, width=30)
    entryExpediteur.pack()
    lblObjet = Label(fenetreMail, text="Objet").pack()
    entryObjet = Entry(fenetreMail, width=30)
    entryObjet.pack()
    lblMessage = Label(fenetreMail, text="Message").pack()
    entryMessage = Entry(fenetreMail, width=90)
    entryMessage.pack()
    bouttonValider = Button(fenetreMail, text="OK",command=lambda: fenetreEnvoie(entryExpediteur.get(),entryObjet.get(),entryMessage.get(),listeBox)).pack()
    fenetreMail.mainloop()
def fenetreImportCsv(listBoxMail,nomFichier):
    fenetreImportCsv = Tk()
    fenetreImportCsv.title("Import CSV")
    lblImportCsv = Label(fenetreImportCsv, text="Import CSV").pack()
    entryCsv = Entry(fenetreImportCsv, width=30)
    entryCsv.pack()
    bouttonValider = Button(fenetreImportCsv, text="OK", command=lambda: inportCsv(entryCsv.get()+'.csv', listBoxMail, nomFichier)).pack()
    fenetreImportCsv.mainloop()
def fenetreImportUrl(listBoxMail,nomFichier):
    fenetreImportUrl = Tk()
    fenetreImportUrl.title("Import URL")
    lblImportUrl = Label(fenetreImportUrl, text="Import URL").pack()
    entryUrl = Entry(fenetreImportUrl, width=30)
    entryUrl.pack()
    bouttonValider = Button(fenetreImportUrl, text="OK", command=lambda: crawlerUrl(entryUrl.get(), listBoxMail, nomFichier)).pack()
    fenetreImportUrl.mainloop()
def fenetreEnvoie(expediteur,objet,message,listeBox):
    fenetreEnvoie = Tk()
    fenetreEnvoie.title("Fenetre Envoie")
    tbl = listeBox.get(0, listeBox.size())
    lblEmail = Label(fenetreEnvoie, text="Email :").pack()
    entryEmail = Entry(fenetreEnvoie, width=30)
    entryEmail.pack()
    bouton = Button(fenetreEnvoie, text="Envoi",command=lambda: envoieMail(entryEmail.get(),expediteur,objet,message)).pack()
    boutonAll = Button(fenetreEnvoie, text="Envoi à toute la liste",command=lambda: envoieMailList(tbl,expediteur,objet,message)).pack()
def envoieMailList(destinataire,expediteur,objet,message):
    for row in destinataire:
        envoieMail(row,expediteur,objet,message)

def envoieMail(destinataire,expediteur,objet,message):
    expediteur = "achauvin901@gmail.com"
    adresseDestinaire = destinataire
    msg = MIMEMultipart()
    msg['From'] = expediteur
    msg['To'] = adresseDestinaire
    msg['Subject'] = objet
    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(expediteur, "Achauvin123456")
    text = msg.as_string()
    server.sendmail(expediteur, adresseDestinaire, text)
    server.quit()
#MAIN
#LECTURE
# tbl = lectureCsv('webtarget.csv')
# #Supression doublons
# #Verification Mail
# tblValide = []
# for row in tbl:
#     valeur = verificationMail(row)
#     if valeur != None:
#         tblValide.append(valeur[0])
# #SUPPRESSION
#    supprimerEmailInMailList(tblValide,email)
# #ECRITURE
# ecritureCsv('campagne.csv',tblValide)
#Verification URL
#tblUrl= []
#tblUrl.append(verificationUrl('tygyyt'))
#Recupération Domaine
#domaine = emailDomaine('nexon.sebastien@gmail.com')
#PING
#if domaine != None:
#    echec = pingDomaine(domaine)
#    print(echec)
#CRAWLER
# tblCrawler = crawlerUrl('http://univcergy.phpnet.org/python/mail.html')
# ecritureCsv('campagne.csv',tblCrawler)

# Accueil
fenetreAccueil = Tk()
fenetreAccueil.title("WebTarget")
lblNomCsv= Label(fenetreAccueil, text="nomCampagne")
lblNomCsv.pack()
entryCsv = Entry(fenetreAccueil, width=30)
entryCsv.pack()
#bouttonValider = Button(fenetreAccueil, text="Valider", command=lambda: lectureCsv(nomCsv.get()+'.csv')).pack()
bouttonValider = Button(fenetreAccueil, text="Valider", command=fenetreGestion).pack()
fenetreAccueil.mainloop()
