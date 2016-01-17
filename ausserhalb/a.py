#!/usr/bin/env python3

import os
import time
import smtplib
from email.mime.text import MIMEText

Pfad_Formulardaten = '/home/fastdform/fastdkeys/'
Knotenliste = "./ausserhalb_hh.txt"
Nachrichtdateiname = "./Nachricht.txt"
Betreff = "Wechsel zu ffnord, Pinneberg, Stormarn & Lauenburg"
Absender = 'kontakt@hamburg.freifunk.net'
Hat_schon_eine_Nachricht_bekommen = []

#Inhalt der Nachricht lesen
Nachrichtdatei = open(Nachrichtdateiname)
Nachricht = Nachrichtdatei.read()
Nachrichtdatei.close()

Adresse = ''
Ansprechpartner = ''
Knotenname = ''
Token = ''
Koordinaten = ''


def Knotendaten_lesen(Dateiname):
    #Variblen zuruecksetzen
    global Adresse
    Adresse = ''
    global Ansprechpartner
    Ansprechpartner = ''
    global Knotenname
    Knotenname = ''
    global Token
    Token = ''

    Koordinaten = ''

    with open(Dateiname) as Datei:

        #Datei Zeilweise einlesen
        Zeilen = Datei.readlines()

        for Zeile in Zeilen:

            #Zeile in Wortliste aufspalten
            Wortliste = Zeile.split()

            if len(Wortliste) > 0:
                if Wortliste[1] == 'Kontakt:':
                    Adresse = Wortliste[2]
                elif Wortliste[1] == 'Knotenname:':
                    Knotenname = Wortliste[2]
                elif Wortliste[1] == 'Ansprechpartner:':
                    Ansprechpartner = Wortliste[2:]
                elif Wortliste[1] == 'Token:':
                    Token = Wortliste[2]
                elif Wortliste[1] == 'Koordinaten:':
                    Koordinaten = Wortliste[2:]
    Datei.close()


with open(Knotenliste) as Datei:

    #Datei Zeilweise einlesen
    Zeilen = Datei.readlines()
    for Zeile in Zeilen:

        #Den Zeilenumbruch '\n' abschneiden
        Zeile=Zeile[0:len(Zeile)-1]

        for Datei in os.listdir(Pfad_Formulardaten):
            if Datei.startswith(Zeile.lower() + '@'):
                Knotendaten_lesen(Pfad_Formulardaten + Datei)
                Adresse = Adresse.lower()

                #falsche Adressen aussortieren
                if Adresse == "<falsche_adresse>":
                    print("Falsche Adresse für Knoten: "+Knotenname)

                #Nur schicken, falls Adressat noch nichts bekommen hat
                elif Adresse not in Hat_schon_eine_Nachricht_bekommen:

                    #In die Liste der bisherigen Adressaten aufnehmen
                    Hat_schon_eine_Nachricht_bekommen.append(Adresse)

                    #email zusammenbauen
                    email = MIMEText(Nachricht, 'plain', 'UTF-8')
                    email['Subject'] = Betreff
                    email['From'] = Absender
                    #email['To'] = Adresse
                    email['To'] = 'andre@hamburg.freifunk.net'

                    #mail server Nachricht verschicken lassen
                    s = smtplib.SMTP('localhost')
                    s.sendmail(Absender, email['To'], email.as_string())
                    s.quit()

                    #Adressat der letzten versendeten Nachricht ausgeben und 1s warten, um nicht auf spam-Listen zu landen
                    print(Adresse)
                    time.sleep(1)
