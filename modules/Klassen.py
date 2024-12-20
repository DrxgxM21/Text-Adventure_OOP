import time 
import os
import sys
import pygame
import json
import getpass
import cv2

class MusikPlayer():
    """
    A simple music player class.
    """
    def __init__(self, relativer_pfad: str):
        """_summary_

        Args:
            relativer_pfad (str): _description_
        """
        self.relativer_pfad = relativer_pfad
        self.absoluter_pfad = os.path.abspath(os.path.join(sys.path[0], relativer_pfad))
    
    def musik(self, startzeit: int =5):
        """_summary_

        Args:
            startzeit (int, optional): _description_. Defaults to 5.
        """
        pygame.init()
        try:
            pygame.mixer.music.load(self.absoluter_pfad)
            pygame.mixer.music.play(start=startzeit)
            time.sleep(5)  # Wartezeit, damit Musik hörbar ist; bei 0 wird nichts abgespielt
        except pygame.error as error:
            print(f"Fehler beim Laden der Musikdatei: {error}")
        finally:
            pygame.mixer.music.stop()
            pygame.quit()


class Helpfunction():
    @staticmethod
    def load_story(Storypfad):
        """Lädt die Geschichte aus einer JSON-Datei
        
        Returns:
            dict 
        """
        with open(Storypfad, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def clear():                                                        # Terminal clearen 
        os.system('cls ')

    @staticmethod
    def print_slowly(text, Schnelligkeit: int = 0.005):
        """
        Gibt den übergebenen Text Zeichen für Zeichen aus

        Args:
        text (str): Der Text, der langsam ausgegeben werden soll.
        Schnelligkeit (float, optional): Die Zeit in Sekunden, die zwischen dem Drucken jedes Zeichens gewartet wird.
                                         Der Standardwert ist 0.005 Sekunden.

        """
        # Durchlaufe jedes Zeichen im Text und drucke es mit einer Verzögerung aus
        for char in text:
            print(char, end="", flush=True) # Drucke das Zeichen ohne Umbruch und zwischendurch flushen
            time.sleep(Schnelligkeit) # Warte die angegebene Zeit (Schnelligkeit) zwischen den Zeichen

    @staticmethod
    def map_generator(coordinates:list):
        image = cv2.imread("map\Map-1.png")
        if image is None:
            print("Fehler: Bild konnte nicht geladen werden!")
        else:
            # Koordinaten des Punktes (x, y)
            punkt_x = coordinates[0]
            punkt_y = coordinates[1]
            radius = 40  # Radius des Punktes (kleiner Wert für Punkt)
            farbe = (0,0,255)  # Schwarz (BGR)
            dicke = -1  # -1 bedeutet, der Kreis wird ausgefüllt

            # Punkt auf das Bild zeichnen
            cv2.circle(image, (punkt_x, punkt_y), radius, farbe, dicke)

            # Text-Eigenschaften
            text = "Spieler"  # Der Text, der geschrieben werden soll
            schriftart = cv2.FONT_HERSHEY_SIMPLEX  # Schriftart
            schriftgroesse = 0.5  # Größe des Textes
            farbe_text = (0,0,0)  # Weißer Text (BGR)
            dicke_text = 1  # Dicke der Linien des Textes

            # Position des Textes berechnen (Text soll zentriert sein)
            text_size = cv2.getTextSize(text, schriftart, schriftgroesse, dicke_text)[0]
            text_x = punkt_x - text_size[0] // 2
            text_y = punkt_y + text_size[1] // 2

            # Text auf das Bild schreiben
            cv2.putText(image, text, (text_x, text_y), schriftart, schriftgroesse, farbe_text, dicke_text)

            # Bild anzeigen
            cv2.imshow("Map", image)

            # Warten, bis eine Taste gedrückt wird, und Fenster schließen
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        



class Character():
    @staticmethod
    def Tod():
        """
         Zeigt eine Nachricht, dass die Reise des Spielers zu Ende ist, und beendet das Spiel.

        Hinweis:
            Die Methode beendet das Programm durch `sys.exit()` nach dem Drücken der Enter-Taste.
        """
        # Zeigt die Nachricht an, dass die Reise zu Ende ist, mit langsamer Ausgabe
        Helpfunction.print_slowly("Leider ist deine Reise hier zu ende\n")
        Game.EndGame()
        
        
    def __init__(self, Inventory: list, Skills: list , Geld: int, Standort: str, cheats: bool ,lvl: int = 1):
        """_summary_
        Initialisiert ein Charakter-Objekt mit den angegebenen Attributen.
        
        Args:
            Inventory (list): Eine Liste, die die Gegenstände im Inventar des Charakters enthält.
            Skills (list): Eine Liste der Fähigkeiten, die der Charakter besitzt.
            Geld (int): Der Geldbetrag, den der Charakter zu Beginn hat.
            Standort (str): Der aktuelle Standort des Charakters als String.
            cheats (bool): Gibt an, ob der Charakter Cheats aktiviert hat (True oder False).
            lvl (int, optional): Der Level des Charakters (Standardwert ist 1).
        """
        # Setze den Level des Charakters auf den angegebenen Wert oder 1, wenn kein Wert angegeben wurde
        self.lvl = lvl
        
        # Setze das Inventar des Charakters auf die angegebene Liste
        self.Inventory = Inventory
        
        # Setze die Fähigkeiten des Charakters auf die angegebene Liste
        self.Skills = Skills
        
        # Setze den Standort des Charakters auf den angegebenen Wert
        self.Standort = Standort
        
        # Setze den Geldbetrag des Charakters auf den angegebenen Wert
        self.Geld = Geld
        
        # Setze den Cheats-Status des Charakters (privat)
        self.__cheats = cheats

    @property
    def cheats(self):
        """
        Gibt den aktuellen Cheats-Status des Charakters zurück.

        Diese Methode stellt den Wert des privaten Attributs '__cheats' zur Verfügung, sodass der Status
        des Cheats des Charakters abgerufen werden kann.

        Returns:
            bool: Der aktuelle Cheats-Status des Charakters (True oder False).
        """
        return self.__cheats
    
    @cheats.setter
    def cheats(self, value: bool):
        """
        Setzt den Cheats-Status des Charakters.

        Diese Methode ermöglicht es, den Cheats-Status des Charakters zu ändern. Wenn der übergebene Wert
        nicht vom Typ `bool` ist, wird eine Fehlermeldung ausgegeben.

        Args:
            value (bool): Der neue Wert für den Cheats-Status des Charakters.

        Raises:
            ValueError: Wenn der übergebene Wert nicht in einen booleschen Wert umgewandelt werden kann.
        """
        try:
            # Setze den Cheats-Status auf den angegebenen booleschen Wert
            self.__cheats = bool(value)
        except ValueError:
            # Fehlerbehandlung, falls der Wert nicht in einen booleschen Wert konvertiert werden kann
            print("Wert muss ein Bool sein")

    def showMoney(self):
        """
        Zeigt dem Spieler den aktuellen Geldbetrag an.
        """
        # Zeigt den aktuellen Geldbetrag des Charakters an
        Helpfunction.print_slowly(f"Du hast {self.Geld} Dublonen")
        # Wartet darauf, dass der Spieler Enter drückt, um das Menü zu verlassen
        getpass.getpass("\nDrücke Enter, um das Menu zu verlassen")
    
    def showlvl(self):
        """
        Zeigt dem Spieler den aktuellen Level des Charakters an.
        """
        # Zeigt den aktuellen Level des Charakters
        Helpfunction.print_slowly(f"Dein Lvl ist {self.lvl}")
        # Wartet darauf, dass der Spieler Enter drückt, um das Menü zu verlassen
        getpass.getpass("\nDrücke Enter, um das Menu zu verlassen")

    def showskills(self):
        """
        Zeigt dem Spieler die Fähigkeiten des Charakters an.
        """

        # Zeigt die Fähigkeiten des Charakters an        
        Helpfunction.print_slowly(f"Deine Fähigkeiten: {self.Skills}")
        # Wartet darauf, dass der Spieler Enter drückt, um das Menü zu verlassen
        getpass.getpass("\nDrücke Enter, um das Menu zu verlassen")
    
    def showINV(self):
        """
        Zeigt dem Spieler den Inhalt des Inventars an.
        """
        # Zeigt den Inhalt des Inventars des Charakters an
        Helpfunction.print_slowly(f"In deinem Inventar ist {self.Inventory}")
        # Wartet darauf, dass der Spieler Enter drückt, um das Menü zu verlassen
        getpass.getpass("\nDrücke Enter, um das Menu zu verlassen")
    
    def ShowMap(self):
        """
        Zeigt die Karte und den aktuellen Standort des Charakters an.
        Die Karte wird nur dann angezeigt wenn man Cheats aktiviert hat
        """
        # Überprüft, ob Cheats aktiviert sind, und zeigt die Karte an, wenn dies der Fall ist
        if self.cheats == True:
            Helpfunction.map_generator(self.Standort.coordinates)
        # Überprüft, ob Cheats aktiviert sind, und zeigt die Karte an, wenn dies der Fall ist
        Helpfunction.print_slowly(f"Du bist in {self.Standort.name}")
        # Wartet darauf, dass der Spieler Enter drückt, um das Menü zu verlassen
        getpass.getpass("\nDrücke Enter, um das Menu zu verlassen")

    

class Bosse(Character):
    def __init__(self, Inventory: list, Skills: list, Standort: str, Name: str, alive: bool, lvl: int = 1):
        """
        Initialisiert ein Bosse-Objekt, das von der Charakterklasse erbt.
        
        Args:
            Inventory (list): Eine Liste, die die Gegenstände im Inventar des Bosses enthält.
            Skills (list): Eine Liste der Fähigkeiten, die der Boss besitzt.
            Standort (str): Der Standort des Bosses (z.B. der Ort, an dem er sich befindet).
            Name (str): Der Name des Bosses.
            alive (bool): Ein boolescher Wert, der angibt, ob der Boss noch lebt (True = lebendig, False = tot).
            lvl (int, optional): Der Level des Bosses (Standardwert ist 1). Der Level wird von der Charakterklasse vererbt.


        """
        # Ruft den Konstruktor der Charakterklasse auf, um die grundlegenden Eigenschaften zu initialisieren
        super().__init__(Inventory, Skills, Geld=0, Standort=Standort, lvl=lvl, cheats=0)
        # Setzt den Lebensstatus des Bosses (ob er noch lebt oder nicht)
        self.__alive = alive
         # Setzt den Namen des Bosses
        self.__Name = Name

    @property                                               #Kein Setter weil der Wert nicht verändert werden kann
    def Name(self):
        """
        Gibt den Namen des Bosses zurück.

        Da der Name des Bosses nicht verändert werden kann, wird der Name hier nur als 
        schreibgeschütztes Attribut (readonly) bereitgestellt.

        Returns:
            str: Der Name des Bosses.
        """
        return self.__Name
    
    @property
    def alive(self):
        """
        Gibt den Lebensstatus des Bosses zurück.
        
        Der Lebensstatus des Bosses zeigt an, ob der Boss noch lebt (True) oder tot (False) ist.

        Returns:
            bool: Der aktuelle Lebensstatus des Bosses.
        """
        return self.__alive
    
    @alive.setter
    def alive(self, value):
        """
        Setzt den Lebensstatus des Bosses.
        
        Diese Methode ermöglicht es, den Lebensstatus des Bosses zu ändern. Der Wert muss ein boolescher Wert sein,
        andernfalls wird eine Fehlermeldung ausgegeben.

        Args:
            value (bool): Der neue Lebensstatus des Bosses (True für lebendig, False für tot).

        """
        if isinstance(value, bool):
            self.__alive = value
        else: 
            print("Der Wert muss ein Bool sein")


class StartRoom():
    """
    Repräsentiert den Anfangsraum im Spiel.
    
    Args:
        RoomName (str): Der Name des Raums, der in der Spielwelt dargestellt wird.
        Description (dict): Eine Beschreibung des Raums, die als Wörterbuch mit Texten oder Details zu diesem Raum gespeichert wird.
        coordinates (list): Die Koordinaten des Raums, die den Raum in der Spielwelt lokalisieren.


    """
    def __init__(self, RoomName: str, Description: dict, coordinates:list):
        """_summary_

        Args:
            RoomName (str): Der Name des Raums, der dem Startraum zugewiesen wird.
            Description (dict): Die Beschreibung des Raums, gespeichert als ein Wörterbuch mit textuellen Informationen.
            coordinates (list): Eine Liste von Koordinaten, die den Raum im Spieluniversum positionieren.
        """
        self.RoomName = RoomName
        self.Description = Description
        self.coordinates = coordinates

    def Start(self):
        """
        Gibt die Beschreibung vom Raum aus

        """

        # Löscht das Terminal
        Helpfunction.clear()
        # Gibt die Beschreibung des Raums langsam aus
        Helpfunction.print_slowly(f"\n{self.Description}")

class Haus():
    """
    Repräsentiert ein Haus mit verschiedenen Attributen wie Stil, Inventar, Bewegungsoptionen und Aktivierungsstatus.

    Args:
        Style (str): Wie siehts aus 
        Inventory (list): Inventar
        Movement1 (str): Wohin gehen ?
        Mov1 (_type_): Wohin gehen als Instantz
        Movement2 (str): Wohin gehen ?
        Mov2 (_type_): Wohin gehen als Instantz
        Movement3 (str): Wohin gehen ?
        Mov3 (_type_): Wohin gehen als Instantz
        aktiviert (bool): Wurde der Raum besucht
        Name (str): Name
    Aufgabe: 
    - Haus erstellen
    """
    def __init__(self, Style: str, Inventory: list, Movement1: str, Mov1, Movement2: str, Mov2 , Movement3: str, Mov3, aktiviert: bool, Name: str, coordinates:list):
        """
        Initialisiert das Haus
        """
        
        self.__Name = Name
        self.Style = Style
        self.Inventory = Inventory
        self.Movement1 = Movement1
        self.Movement2 = Movement2
        self.Movement3 = Movement3
        self.__aktiviert = aktiviert
        self.Mov1 = Mov1
        self.Mov2 = Mov2
        self.Mov3 = Mov3
        self.coordinates = coordinates                 #änderung koordinaten

    @property                                               #Kein Setter weil der Wert nicht verändert werden kann
    def name(self):
        """
        Gibt den Namen des Bosses zurück.

        Da der Name des Bosses nicht verändert werden kann, wird der Name hier nur als 
        schreibgeschütztes Attribut (readonly) bereitgestellt.

        Returns:
            str: Der Name des Bosses.
        """
        return self.__Name


    @property
    def active(self):
        """
        Gibt den Aktivierungsstatus des Hauses zurück.

        Returns:
            bool: Der Aktivierungsstatus des Hauses.
        """
        return self.__aktiviert
    
    @active.setter
    def active(self, change):
        """
        Setzt den Aktivierungsstatus des Hauses.

        Args:
            change (bool): Der neue Aktivierungsstatus des Hauses.

        Hinweis:
            Falls der übergebene Wert kein boolescher Wert ist, wird eine Fehlermeldung ausgegeben.
        """
        if isinstance(change, bool):  # Überprüfe, ob der neue Wert ein Boolean ist
            self.__aktiviert = change
        else:
            print("Error: Active muss ein boolescher Wert (True/False) sein")
            

class Street(Haus):
    """_summary_

    Repräsentiert eine Straße, die von der Hausklasse erbt.

    Args:
        Style (str): Der Stil oder das Aussehen der Straße (z.B. gepflastert, unbefestigt).
        Inventory (list): Eine Liste von Gegenständen, die in der Straße vorhanden sind.
        Movement1 (str): Der Name der ersten Bewegungsoption für die Straße.
        Mov1 (type): Ein Ziel oder Objekt, auf das die erste Bewegung verweist.
        Movement2 (str): Der Name der zweiten Bewegungsoption.
        Mov2 (type): Ein Ziel oder Objekt, auf das die zweite Bewegung verweist.
        Movement3 (str): Der Name der dritten Bewegungsoption.
        Mov3 (type): Ein Ziel oder Objekt, auf das die dritte Bewegung verweist.
        aktiviert (bool): Ein boolescher Wert, der angibt, ob die Straße bereits besucht oder aktiviert wurde.
        Name (str): Der Name der Straße.
        coordinates (list): Die Koordinaten, die die Straße im Spiel positionieren.


    """
    def __init__(self, Style: str, Inventory: list, Movement1: str, Mov1, Movement2: str, Mov2 , Movement3: str, Mov3, aktiviert: bool, Name: str, coordinates: list):
        """
        Initialisiert eine Straße, die von der `Haus`-Klasse erbt.
        """
        # Initialisiert das Street-Objekt und ruft den Konstruktor der Basisklasse Haus auf
        super().__init__(Style, Inventory, Movement1, Mov1, Movement2, Mov2 , Movement3, Mov3, aktiviert, Name, coordinates)


class DungeonRoom(Haus):
    """
    Erstellt einen Dungeonraum, der von der `Haus`-Klasse erbt.

    Args:
        Style (str): Das Aussehen des Dungeons (z.B. dunkel, verlassen, geheimnisvoll).
        Inventory (list): Eine Liste, die die Gegenstände im Dungeonraum enthält.
        Movement1 (str): Der Name oder die Beschreibung der ersten Bewegungsoption.
        Mov1: Die Implementierung oder Daten, die mit der ersten Bewegungsoption verbunden sind.
        Movement2 (str): Der Name oder die Beschreibung der zweiten Bewegungsoption.
        Mov2: Die Implementierung oder Daten, die mit der zweiten Bewegungsoption verbunden sind.
        Movement3 (str): Der Name oder die Beschreibung der dritten Bewegungsoption.
        Mov3: Die Implementierung oder Daten, die mit der dritten Bewegungsoption verbunden sind.
        aktiviert (bool): Ein Flag, das angibt, ob der Dungeonraum aktiviert oder besucht wurde.
        Name (str): Der Name des Dungeons.
        coordinates (list): Eine Liste von Koordinaten, die den Standort des Dungeons im Spiel darstellen.
        Boss: Eine Referenz auf den Boss, der mit diesem Dungeonraum verbunden ist.


    """
    def __init__(self, Style: str, Inventory: list, Movement1: str, Mov1, Movement2: str, Mov2 , Movement3: str, Mov3, aktiviert: bool, Name: str,coordinates: list, Boss):
        """
        Initialisiert den Dungeonraum, der von der `Haus`-Klasse erbt.
        """
        # Initialisiert den Dungeonraum, indem der Konstruktor der Basisklasse Haus aufgerufen wird.
        super().__init__(Style, Inventory, Movement1, Mov1, Movement2, Mov2, Movement3, Mov3, aktiviert, Name, coordinates)
        # Fügt die Boss-Eigenschaft hinzu, die eine Referenz auf den Boss dieses Dungeonraums enthält.
        self.Boss = Boss
        

class Game():
    """
    Enthält die Grundlegenden funktionsweisen des Spiels
    """
    #Damit man sieht wie viele Bosse man getötet hat, in der Statistik
    ToteBosse = 0

    @staticmethod
    def Cheatsactivating():
        """
        Fragt den Spieler, ob er Cheats aktivieren möchte, und gibt die Auswahl zurück.

        Rückgabewert:
        bool: `True` wenn Cheats aktiviert werden sollen, ansonsten `False`.
        
        """
        while True:
            # Terminal wird gelöscht und die Wahl für Cheats angezeigt
            Helpfunction.clear()
            Helpfunction.print_slowly("Willst du cheats aktvieren?")
            print("\n[A]. Ja")
            print("[B]. Nein")
            # Benutzer wählt eine Option
            choice = input("\nDeine Wahl: ").upper() # Eingabe wird in Großbuchstaben umgewandelt, um Eingabefehler zu vermeiden
            # Überprüft die Wahl des Spielers und bricht die Schleife ab, wenn eine gültige Eingabe erfolgt
            if choice == "A":
                break # Wählt Ja und verlässt die Schleife
            elif choice == "B": # Wählt Nein und verlässt die Schleife
                break
            else:
                getpass.getpass("Falsche Eingabe")  # Wenn eine ungültige Eingabe gemacht wurde, wird der Benutzer darauf hingewiesen und aufgefordert, erneut zu wählen
        # Gibt zurück, ob die Cheats aktiviert werden sollen
        if choice == "A":
            return True  # Cheats aktivieren
        else:
            return False # Cheats nicht aktivieren

    @staticmethod
    def EndGame():
        #löscht das Terminal
        Helpfunction.clear()
        #Statistik
        Helpfunction.print_slowly(f"Du hast in deiner Reise {Game.ToteBosse} Bosse getötet")
        # Zeigt die Credits-Nachricht aus der Story an
        Helpfunction.print_slowly(Storytext["Credits"])
        # Fordert den Benutzer auf, Enter zu drücken, um das Spiel zu beenden
        getpass.getpass("\nDrück Enter um das Spiel zu beenden")
        # Beendet das Spiel
        sys.exit()

    def TheEND(self):
        """ 
        Zeigt das Ende der Story an und entscheidet, ob der Spieler ein gutes oder schlechtes Ende erhält.

        Aufgabe:
        - Zeigt das Ende der Story an.
        - Überprüft, ob der Hauptcharakter ein bestimmtes Item besitzt.
        - Zeigt basierend auf dieser Bedingung ein gutes oder schlechtes Ende.
        - Beendet das Spiel mit einer Anzeige der Credits.
        """
        # Löscht das Terminal, um Platz für das Ende der Story zu schaffen
        Helpfunction.clear()
        # Löscht den Bildschirm, um Platz für das Ende der Story zu schaffen
        Helpfunction.print_slowly(Storytext["TheEND"])
        # Löscht den Bildschirm, um Platz für das Ende der Story zu schaffen
        if "Packung Malboro Gold" in MainCharackter.Inventory:
            # Zeigt das "gute" Ende an, wenn das Item im Inventar ist
            Helpfunction.print_slowly(Storytext["TheENDgood"])
        else:
            # Zeigt das "schlechte" Ende an, wenn das Item nicht im Inventar ist
            Helpfunction.print_slowly(Storytext["TheENDbad"])
        # Fordert den Benutzer auf, Enter zu drücken, um die Story zu beenden
        getpass.getpass("\nDrück Enter um die Story zu beenden")
        self.EndGame()

    def __init__(self):
        """
        Konstruktor der Klasse. Initialisiert das Spiel, indem die Methode `create_game` aufgerufen wird
        """
        # Ruft die Methode `create_game` auf, um das Spiel zu initialisieren
        self.create_game()
    
    
            

    def create_game(self):
        """
         Initialisiert das Spiel, indem verschiedene Spielkomponenten gestartet werden.
        """
        # Aktiviert Cheats, indem die Methode `Cheatsactivating` aufgerufen wird und das Ergebnis gespeichert wird
        MainCharackter.cheats = self.Cheatsactivating()
        # Startet den Anfangsraum
        Raum_start.Start()
        # Spielmusik wird abgespielt
        intro.musik()
        # Wartet darauf, dass der Benutzer Enter drückt, um seine Reise zu beginnen (Eingaben werden nicht angezeigt)
        getpass.getpass("\nDrücke Enter, um deine Reise anzutreten")
        # Startet die Bar (vermutlich ein Raum oder ein Event im Spiel)
        Bar.Start()
        # Setzt den Startort des Hauptcharakters auf "Haus1Keller"
        MainCharackter.Standort = Haus1Keller
        # Leere Zeile zur optischen Trennung
        print("\n")
        # Zeigt eine Nachricht, dass der Charakter im Keller aufwacht
        Helpfunction.print_slowly(Storytext["Keller aufwachen"])
        # Wartet darauf, dass der Benutzer Enter drückt, um fortzufahren
        getpass.getpass("\nDrück Enter")
        # Startet das Intro-Spielerlebnis
        self.playIntro()

    def mainoptions(self):
        """
        Zeigt die Hauptoptionen im Spiel an, die der Spieler wählen kann
        """
        print("\n[A] Level anschauen")
        print("[B] Inventar anschauen")
        print("[C] Fähigkeiten anschauen")
        print("[D] Budget Überprüfen")
        print("[E] Standort anschauen")
        print("[I] Nach Loot Suchen")
    
    def mainoptionsinuse(self, Option, Standort):
        """
        Verarbeitet die vom Spieler gewählte Option und führt die entsprechende Aktion aus.

        Args:
        Option (str): Die vom Spieler gewählte Option. Kann einer der folgenden Werte sein:
                      "A" für Level anschauen, "B" für Inventar anschauen, "C" für Fähigkeiten anschauen,
                      "D" für Budget überprüfen, "E" für Standort anschauen, "I" für nach Loot suchen.
        Standort: Der aktuelle Standort des Spielers, der an die Loot-Option übergeben wird.

        """
            # Überprüft, welche Option der Spieler gewählt hat und führt die entsprechende Aktion aus
        if Option == "A":
            # Zeigt das Level des Spielers an
            MainCharackter.showlvl()
        elif Option == "B":
            # Zeigt das Inventar des Spielers an
            MainCharackter.showINV()
        elif Option == "C":
            # Zeigt die Fähigkeiten des Spielers an
            MainCharackter.showskills()
        elif Option == "D":
            # Zeigt das Budget/Geld des Spielers an
            MainCharackter.showMoney()
        elif Option == "E":
            # Zeigt die Karte oder den Standort des Spielers an
            MainCharackter.ShowMap()
        elif Option == "I":
            # Führt die Lootoptionen aus, basierend auf dem aktuellen Standort
            self.Lootoptions(Standort)
        

    def Standortoptions(self, Room):
        """
        Zeigt die verfügbaren Bewegungsoptionen innerhalb eines Raums an.
        rgs:
        Room: Der Raum (Instanz), der die Bewegungsoptionen enthält. 
        Jede Bewegungsoption (`Movement1`, `Movement2`, `Movement3`) wird geprüft,
        um zu sehen, ob eine gültige Bewegung verfügbar ist.
        """
        # Liste der Bewegungsoptionen aus dem Raum-Objekt (Room)
        Movementlist = [Room.Movement1, Room.Movement2, Room.Movement3]
        # Liste der entsprechenden Druckoptionen, die dem Spieler angezeigt werden
        Printlist = ["[F]", "[G]", "[H]"]
        # Durchläuft beide Listen gleichzeitig und zeigt nur gültige Bewegungen an
        for d, j in zip(Printlist, Movementlist):
            if j != None:  # Überprüft, ob die Bewegung nicht None (also gültig) ist
                print(f"{d} {j}")
    
    def Standortoptionsinuse(self, Option, Standort):
        """
            Verarbeitet die vom Spieler gewählte Bewegungsoption und aktualisiert den Standort des Spielers.
        Args:
            Option (str): Die vom Spieler gewählte Bewegungsoption. Sollte einer der Werte "F", "G" oder "H" sein.
            Standort: Der aktuelle Standort des Spielers, der die Bewegungsoptionen enthält.
        
        """
    	# Liste der Tastenkürzel für Bewegungsoptionen
        Printlist = ["F", "G", "H"]
        # Liste der tatsächlichen Bewegungsziele, die der Raum (Standort) zur Verfügung stellt
        Movementlist = [Standort.Mov1, Standort.Mov2, Standort.Mov3]
        # Durchläuft beide Listen gleichzeitig, um die verfügbaren Optionen und Bewegungsziele zu vergleichen
        for d, j in zip(Printlist, Movementlist):
            if j != None:  # Überprüft, ob das Bewegungsziel nicht None ist (also gültig)
                if Option == d:  # Wenn die vom Spieler gewählte Option mit der aktuellen Option übereinstimmt
                    MainCharackter.Standort = j  # Aktualisiert den Standort des Spielers auf das gewählte Ziel


    def Lootoptions(self, loot):
        """
        Bietet dem Spieler die Möglichkeit, gefundene Gegenstände in sein Inventar aufzunehmen.

        Args:
        loot: Ein Objekt, das das `Inventory` enthält, also eine Liste von gefundenen Gegenständen,
              die dem Spieler zur Auswahl angezeigt werden.
        """
        while True:
            # Löscht den Bildschirm und zeigt den gefundenen Loot an
            Helpfunction.clear()
            Helpfunction.print_slowly(f"Du hast folgendes gefunden:{loot.Inventory}\n")
            # Definiert die möglichen Optionen für das Hinzufügen von Gegenständen
            LootOptionlist =["[A]","[B]","[C]"]
            # Zählt, wie viele Gegenstände es im Loot gibt (für die Nummerierung der Optionen)
            prints = 0
            for i, j in zip(LootOptionlist,loot.Inventory):
                # Zeigt jede Option (z. B. [A] [B] [C] ...) und den jeweiligen Gegenstand an
                print(f"{i} {j} in Inventar hinzufügen")
                prints += 1
            # Fügt die Verlassen-Option hinzu
            print("[F] Verlassen")
            # Liest die Eingabe des Spielers und wandelt sie in Großbuchstaben um
            eingabe = input("Wähle eine Option: ").upper()
            # Wenn der Spieler die "Verlassen"-Option wählt, wird die Schleife beendet
            if eingabe == "F":
                break
            # Wenn der Spieler eine der Auswahloptionen (A, B, C) wählt, wird der Gegenstand hinzugefügt
            elif eingabe in ["A", "B", "C"]:
                self.AddtoInventory(eingabe, loot.Inventory, prints)
            else:
                # Falls eine ungültige Eingabe erfolgt, wird eine Fehlermeldung ausgegeben und der Spieler aufgefordert, es erneut zu versuchen
                print("Ungültige Eingabe. Bitte versuche es erneut.")
                getpass.getpass("Drücke Enter, um fortzufahren...") 
    
    def AddtoInventory(self, input, Loot, prints): 
        """
        Fügt ein Item aus dem Loot zum Inventar des Spielers hinzu und entfernt es aus dem Loot.

        Args:
            input (str): Die Wahl des Spielers, welche Option (A, B, C) er ausgewählt hat.
            Loot (list): Die Liste der gefundenen Items, aus denen der Spieler wählen kann.
            prints (int): Die Anzahl der verfügbaren Items im Loot, welche in den Optionen angezeigt werden.
        """  
        # Überprüft, ob der Spieler Option "A" gewählt hat und ob ein Gegenstand verfügbar ist
        if input == "A" and prints > 0:
            # Fügt den ersten Gegenstand aus dem Loot zum Inventar des Spielers hinzu
            MainCharackter.Inventory.append(Loot[0])
            Loot.pop(0)
        # Überprüft, ob der Spieler Option "B" gewählt hat und ob ein zweiter Gegenstand verfügbar ist
        elif input == "B" and prints > 1:
            MainCharackter.Inventory.append(Loot[1])
            Loot.pop(1)
        # Überprüft, ob der Spieler Option "C" gewählt hat und ob ein dritter Gegenstand verfügbar ist
        elif input == "C" and prints > 2:
            MainCharackter.Inventory.append(Loot[2])
            Loot.pop(2)
        else:
            # Falls der Spieler eine ungültige Eingabe macht, wird er darauf hingewiesen
            print("Ungültige Eingabe. Bitte versuche es erneut.")
            getpass.getpass("Drücke Enter, um fortzufahren...")
        # Überprüft, ob der zuletzt hinzugefügte Gegenstand im Inventar "Dublonen" enthält 
        if len(MainCharackter.Inventory) > 0 :
            if MainCharackter.Inventory[-1][-8:]== "Dublonen":
                # Extrahiert die Dublonen aus dem Namen des Gegenstands (nehmen wir an, es steht an den ersten Stellen)
                Geld = int(MainCharackter.Inventory[-1][:2]) # Beispiel: "50 Dublonen" -> 50 wird extrahiert
                # Entfernt die Dublonen aus dem Inventar
                MainCharackter.Inventory.pop(-1)
                MainCharackter.Geld += Geld
    
    def Bossfight(self):
        """
            Führt den Kampf gegen den Boss im aktuellen Standort durch.
        """
        # Zeigt die Beschreibung des Bosses an
        Helpfunction.print_slowly(Storytext[MainCharackter.Standort.Boss.Name])
        # Wenn der Boss "Rainer Winkler" ist, spielt eine spezielle Musik und zeigt eine spezielle Nachricht
        if MainCharackter.Standort.Boss.Name == "Rainer Winkler":
            getpass.getpass("") # wartet darauf, dass der Spieler eine Eingabe tätigt (drückt Enter)
            endfight.musik(13)# spielt eine spezielle Musik für den Kampf
            Helpfunction.print_slowly(Storytext["Rainer Winkler2"]) # zeigt eine spezielle Nachricht für den Boss
        getpass.getpass("\nDrück Enter um den Kampf zu beginnen")# wartet darauf, dass der Spieler den Kampf startet
        while True:
            Helpfunction.clear() # löscht das Terminal
            Helpfunction.print_slowly("Deine Skills sind:") # zeigt die verfügbaren Skills des Spielers an
            liste=["[A]","[B]","[C]"]   # die möglichen Optionen für den Spieler
            prints = 0  # Zähler für die Anzahl der verfügbaren Skills
            for i,j in zip(liste, MainCharackter.Skills):
                Helpfunction.print_slowly(f"\n{i} {j}") # zeigt jeden Skill an
                prints += 1 # erhöht den Zähler
            Attack = input("\nWas willst du Nutzen: ").upper() # fragt den Spieler nach der gewählten Fähigkeit und konvertiert sie in Großbuchstaben
            Helpfunction.clear() # fragt den Spieler nach der gewählten Fähigkeit und konvertiert sie in Großbuchstaben
            # Wenn der Spieler ein höheres Level als der Boss hat, wird der Kampf fortgesetzt
            if MainCharackter.lvl >= MainCharackter.Standort.Boss.lvl:  # ruft die Methode auf, die den Boss bekämpft
                Kill = self.BossSlayer(Attack, prints)
                if Kill == True:
                    MainCharackter.Standort.Boss.alive = False  #setzt den Status des Bosses auf "tot"
                    Game.ToteBosse += 1
                    break # bricht die Schleife ab, wenn der Boss besiegt wurde
            else:
                # Wenn der Boss stärker ist als der Spieler, wird die Methode für den Tod des Spielers aufgerufen
                self.SlayedbyBoss(Attack, prints)
        if MainCharackter.lvl >= MainCharackter.Standort.Boss.lvl and Kill == True:
            currentlvl = MainCharackter.lvl # speichert das aktuelle Level des Spielers
            MainCharackter.lvl += MainCharackter.Standort.Boss.lvl
            # Wenn das neue Level des Spielers bestimmte Schwellen überschreitet, werden neue Fähigkeiten freigeschaltet
            if currentlvl <5 and MainCharackter.lvl >= 5:
                Helpfunction.print_slowly(f"\nDu bist nun  level {MainCharackter.lvl}, du kriegst Flashback, du kannst nun den Tornadokick")
                MainCharackter.Skills.append("Tornadokick") # fügt den neuen Skill "Tornadokick" hinzu
            if currentlvl < 10 and currentlvl > 5 and MainCharackter.lvl >= 10:
                Helpfunction.print_slowly(f"\nDu bist nun  level {MainCharackter.lvl}, du kriegst Flashback, du kannst nun den Feuerball")
                MainCharackter.Skills.append("Feuerball")   # fügt den neuen Skill "Feuerball" hinzu
            # Wartet darauf, dass der Spieler den Kill bestätigt oder mit dem Looten fortfährt 
            getpass.getpass("\nDrück Enter um den Kill zu bestätigen/zu looten")
            self.Bosslooter()   # ruft die Methode zum Looten des Bosses auf
            

    def Bosslooter(self):        
        """
            Diese Methode führt das Looten nach einem Bosskampf durch.
        """
        # Zeigt dem Spieler eine Nachricht, dass der Boss Items fallen lässt
        Helpfunction.print_slowly(f"Der {MainCharackter.Standort.Boss.Name} droppt items, es sieht aber so als würden sie verschwinden wenn du sie liegen lässt")
        # Wartet darauf, dass der Spieler den Lootvorgang startet
        getpass.getpass("\nDrück Enter um zu looten")
        # Ruft die Loot-Optionen des Bosses auf, damit der Spieler entscheiden kann, was er nehmen möchte
        self.Lootoptions(MainCharackter.Standort.Boss)
        # Wenn der besiegte Boss "Garados" ist und er tot ist, wird eine spezielle Story abgespielt
        if MainCharackter.Standort.Boss.Name == "Garados" and MainCharackter.Standort.Boss.alive == False:
            Helpfunction.clear()# Löscht das Terminal
            Helpfunction.print_slowly(Storytext["Love Story"]) # Zeigt die spezielle "Love Story" an
            getpass.getpass("\nDrück Enter um den Brief Wegzulegen") # Wartet auf eine Eingabe, um fortzufahren
        

    def BossSlayer(self, Attack, prints):
        """
            Diese Methode behandelt die Angriffe des Spielers im Bosskampf und bestimmt, ob der Angriff erfolgreich war.

            Args:
                Attack (str): Der Angriff, den der Spieler auswählt. Kann "A", "B" oder "C" sein.
                prints (int): Eine Anzahl, die angibt, wie viele Angriffsoptionen verfügbar sind.
            
            Rückgabewert:
                bool: Gibt `True` zurück, wenn der Angriff erfolgreich war, ansonsten `False`.
        """
        # Löscht das Terminal
        Helpfunction.clear()
        # Wenn der Spieler "A" auswählt, wird der entsprechende Text für den rechten Haken angezeigt
        if Attack == "A":
            Helpfunction.print_slowly(Storytext["Rechter Hacken Text WIN"])
            return True  # Der Angriff war erfolgreich
        # Wenn der Spieler "B" auswählt und mindestens 2 Angriffsoptionen vorhanden sind, wird der Tornadokick verwendet
        elif Attack == "B" and prints >= 2:
            Helpfunction.print_slowly(Storytext["Tornadokick Text WIN"])
            return True # Der Angriff war erfolgreich
        # Wenn der Spieler "C" auswählt und mindestens 3 Angriffsoptionen vorhanden sind, wird der Feuerball verwendetb
        elif Attack == "C" and prints >= 3:
            Helpfunction.print_slowly(Storytext["Feuerball Text WIN"])
            return True  # Der Angriff war erfolgreich
        # Wenn keine der Bedingungen zutrifft, ist der Angriff ungültig
        else: 
            Helpfunction.print_slowly("Das war keine gültige eingabe")
            time.sleep(1.5)# Warte kurz, um dem Spieler Zeit zu geben, die Nachricht zu lesen
            return False # Der Angriff war nicht erfolgreich
        
        
            
    
    def SlayedbyBoss(self, Attack, prints):
        """
            Diese Methode wird aufgerufen, wenn der Spieler im Bosskampf verliert.
        
            Args:
                Attack (str): Der Angriff, den der Spieler auswählt. Es kann "A", "B" oder "C" sein.
                prints (int): Die Anzahl der verfügbaren Angriffsoptionen, die im aktuellen Kampf verwendet werden können.  
        """
        while True:
            Helpfunction.clear() #löscht das Terminal
            # Wenn der Spieler den Angriff "A" wählt, wird die entsprechende Verlustnachricht angezeigt.
            if Attack == "A":
                Helpfunction.print_slowly(Storytext["Rechter Hacken Text LOSE"])
                break
            # Wenn der Spieler den Angriff "B" wählt und mindestens 2 Angriffe verfügbar sind, wird der Verlusttext für "Tornadokick" angezeigt.
            elif Attack == "B" and prints >= 2:
                Helpfunction.print_slowly(Storytext["Tornadokick Text LOSE"])
                break
            # Wenn der Spieler den Angriff "C" wählt und mindestens 3 Angriffe verfügbar sind, wird der Verlusttext für "Feuerball" angezeigt.
            elif Attack == "C" and prints >= 3:
                Helpfunction.print_slowly(Storytext["Feuerball Text LOSE"])
                break
            # Wenn der Spieler eine ungültige Eingabe macht, wird er darauf hingewiesen und muss eine neue Wahl treffen.
            else: 
                Helpfunction.print_slowly("Das war keine gültige eingabe")
                time.sleep(1.5)
        # Nachdem der Spieler verloren hat, wird die entsprechende Tod-Nachricht für den Boss angezeigt.
        Helpfunction.print_slowly(Storytext[f"{MainCharackter.Standort.Boss.Name}_tod"])
        # Der Spieler wird aufgefordert, die Eingabetaste zu drücken, um den Tod zu bestätigen und das Spiel zu beenden.
        getpass.getpass("\nDu bist Gestorben, drück Enter")
        # Ruft die Tod-Methode des Spielers auf, um das Spiel zu beenden.
        MainCharackter.Tod()

    def playIntro(self):
        """
        Diese Methode führt die Hauptlogik des Spiels im Introbereich aus. Sie sorgt dafür,
        dass der Spieler durch die verschiedenen Standorte im Spiel navigiert, bis bestimmte
        Bedingungen erfüllt sind.
        
        Die folgenden Optionen sind im Intro verfügbar:
        - A: Level anzeigen
        - B: Inventar anzeigen
        - C: Fähigkeiten anzeigen
        - D: Budget überprüfen
        - E: Standort anzeigen
        - I: Nach Loot suchen

        """
        while True:
            # Prüft, ob BlauesHaus, RotesHaus aktiv und der Spieler auf der Straße ist
            if BlauesHaus.active == True and RotesHaus.active == True and MainCharackter.Standort == Straße:
                break  # Wenn die Bedingungen erfüllt sind, bricht die Schleife ab
            else:
                # Löscht den Bildschirm, um den Überblick zu bewahren
                Helpfunction.clear()
                # Wenn der aktuelle Standort des Spielers nicht aktiv ist, wird der Stil des Raums angezeigt
                if MainCharackter.Standort.active == False:
                    Helpfunction.print_slowly(MainCharackter.Standort.Style)
                    # Setzt den Standort auf aktiv
                    MainCharackter.Standort.active = True
                # Zeigt die Hauptoptionen für den Spieler
                self.mainoptions()
                # Zeigt die Bewegungsoptionen des aktuellen Standorts
                self.Standortoptions(MainCharackter.Standort)
                # Der Spieler wählt eine Option
                Option = input("Wähle eine Option: ").upper()
                # Wenn eine der Hauptoptionen gewählt wird, wird die entsprechende Methode aufgerufen
                if Option in ["A", "B", "C", "D", "E", "I"]:
                    self.mainoptionsinuse(Option, MainCharackter.Standort)
                else:
                    # Wenn eine Bewegungsoption gewählt wird, wird die Methode für Standortwechsel aufgerufen
                    self.Standortoptionsinuse(Option, MainCharackter.Standort)
        # Wenn die Bedingungen erfüllt sind, wird der Standort auf den Dungeon-Eingang gesetzt
        MainCharackter.Standort = Dungeoneingang
        # Das Spiel geht nun weiter und startet das eigentliche Spiel
        self.playGame()
    
    
    def playGame(self):
        """
        Diese Methode steuert den Hauptspielablauf, nachdem das Intro abgeschlossen ist.
        
        Die Bedingungen im Spiel werden überprüft, und abhängig davon, ob der Boss 
        noch lebt und ob der Spieler den Boss bekämpfen muss, werden verschiedene Aktionen 
        ausgeführt:
        - Bosskampf, wenn der Boss aktiv ist und noch lebt
        - Anzeige der aktuellen Standort-Optionen und Spieloptionen
        - Ende des Spiels, wenn der Boss besiegt wurde oder andere Bedingungen erfüllt sind.

        """
        while True:
            # Überprüfen, ob der Drachenlord noch lebt und ob der Dungeon-Gott-Raum aktiv ist
            if DungeonGodRoom.active == False and Drachenlord.alive == True:
                # Wenn der Boss im aktuellen Raum noch aktiv ist, wird ein Bosskampf gestartet
                if MainCharackter.Standort.Boss is not None and MainCharackter.Standort.Boss.alive == True:
                    self.Bossfight()
                else:
                    # Wenn kein Boss mehr da ist oder der Boss besiegt wurde
                    Helpfunction.clear() # Terminal löschen
                    # Wenn der aktuelle Standort des Spielers noch nicht aktiv ist, wird der Stil des Raums angezeigt
                    if MainCharackter.Standort.active == False:
                        Helpfunction.print_slowly(MainCharackter.Standort.Style)
                        MainCharackter.Standort.active = True
                    # Zeigt die Hauptoptionen für den Spieler (Level, Inventar, etc.)
                    self.mainoptions()
                    # Zeigt die Bewegungsoptionen für den aktuellen Standort des Spielers
                    self.Standortoptions(MainCharackter.Standort)
                    # Der Spieler wählt eine Option
                    Option = input("Wähle eine Option: ").upper()
                    # Wenn eine der Hauptoptionen gewählt wird, wird die entsprechende Methode aufgerufen
                    if Option in ["A", "B", "C", "D", "E", "I"]:
                        self.mainoptionsinuse(Option, MainCharackter.Standort)
                    else:
                        # Wenn eine Bewegungsoption gewählt wird, wird die Methode für Standortwechsel aufgerufen
                        self.Standortoptionsinuse(Option, MainCharackter.Standort)
            else:
                # Wenn der Boss besiegt wurde oder das Ende des Spiels erreicht ist, wird das Spiel beendet
                self.TheEND()


#Base
Storytext = Helpfunction.load_story('modules\Story.json')
MainCharackter = Character([], ["Rechter Hacken"], 0, None, False, 1)
#Tutorial
intro = MusikPlayer('Musik/Zelda-intro.mp3')
BlauesHaus = Haus(Storytext["BlauesHaus"], ["50 Dublonen", "1 Feuerzeug"], "Raus gehen", None, None, None, None, None, False, "Blaues Haus", [220,250])
RotesHaus = Haus(Storytext["RotesHaus"], [], "Raus gehen", None, None, None, None, None, False, "Rotes Haus", [320, 250])
Straße = Street(Storytext["Strasen Text"],[], "Ins Blaue Haus", BlauesHaus, "Ins Rote Haus", RotesHaus, None, None, False, "Random Strasse", [230, 170])
Raum2 = Haus(Storytext["Raum2 Text"], [], "Raus gehen", None, None, None,None, None, False, "Raum 2 Haus 1", [120, 170])
Raum1 = Haus(Storytext["Raum1 Text"], ["05 Dublonen", "Stein"], "Raus gehen", None, None, None,None, None, False, "Raum 1 Haus 1", [120, 170])
Haus1 = Haus(Storytext["Haus1"],["Stock", "50 Dublonen"], "Raus gehen", Straße, "Raum1 betreten", Raum1, "Raum2 betreten", Raum2, False, "Haus1", [120, 170])
Haus1Keller = Haus( Storytext["Keller"], [], "Treppe Raufgehen", Haus1, None, None, None, None, False, "Keller",[120, 170])
Bar = StartRoom("Bar", Storytext["Bar"], [50,50])
Raum_start = StartRoom("Raum Start", Storytext["Start Raum"], [50,50])



MainCharackter.Standort = Bar
BlauesHaus.Mov1 = Straße           #Nachträglich Raum eintragungen
RotesHaus.Mov1 = Straße
Raum1.Mov1 = Haus1
Raum2.Mov1 = Haus1


#Maingame
endfight = MusikPlayer('Musik\Drachenlord.mp3')
Kobold = Bosse(["50 Dublonen", "Packung Malboro Gold"], ["Goldsack wurf"], None, "Kobold", True)
Ratte = Bosse(["Kaputtes Schwert"], ["Wind feger"], None, "Ratte", True)
Rudolf = Bosse(["Rote Nase", "90 Dublonen"], ["Geweih rammler"], None, "Rudolf",True,  lvl=2)
Pikachu_baby = Bosse(["Baby Pikachu Schwanz"], ["Ruckzuck hiebchen"], None, "Baby Pikachu",True, lvl=4)
Glumanda_baby = Bosse(["Glumanda Skellet"], ["Kratzarl"], None, "Baby Glumanda",True, lvl=3)
Garados = Bosse(["Wassernerf"], ["Hydropumpe"], None, "Garados", True, lvl=10)
Drachenlord = Bosse(["Goldene Scar"], ["Audi macht skrr skrr"], None, "Rainer Winkler", True,  lvl=20)
Dungeoneingang = DungeonRoom(Storytext["Schlucht"], [], "Dungeon betreten", None, None,None, None, None, False, "Schlucht", [440, 400], None)
DungeonRoom0 = DungeonRoom(Storytext["DungeonRoom0"], [],"Zum Kobold Dungeon", None, "Zum GodRoom", None, None, None, False, "Dungeon 0", [520, 400], None)
DungeonRoom1 = DungeonRoom(Storytext["DungeonRoom1"], ['Roboterdrohne', 'Mystische Lampe'], "Zum Rudolf Dungeon", None, "Zum Ratte Dungeon", None, "Zum Eingang zurueck", None, False, "Kobold Dungeon", [600, 400], Kobold)
DungeonRoom2 = DungeonRoom(Storytext["DungeonRoom2"], ['Verfluchtes Buch'],"Zum Baby Pikachu Dungeon", None, "Zum Weirden Raum", None, "Zum Kobold Dungeon", None, False, "Ratte Dungeon", [600, 480], Ratte)
DungeonRoom3 = DungeonRoom(Storytext["DungeonRoom3"], [],"Zum Weirden Raum", None, "Zum Kobold Dungeon", None, None, None, False, "Rudolf Dungeon", [680, 400], Rudolf)
DungeonRoom4 = DungeonRoom(Storytext["DungeonRoom4"], ['Smaragd'],"Zum Baby Glumanda Dungeon", None, "Zum Ratte Dungeon", None, None, None, False, "Pikachu baby Dungeon", [600, 560], Pikachu_baby)
DungeonRoom5 = DungeonRoom(Storytext["DungeonRoom5"], ['Sternenstaub'],"Zum Weirden Raum", None, "Zum Baby Pikachu Dungeon", None, None, None, False, "Glumanda baby Dungeon", [680, 560], Glumanda_baby)
WeirdRoom = DungeonRoom(Storytext["WeirdRoom"],[], "Zum Rudolf Dungeon", None, "Zum Ratte Dungeon", None, "Zum Baby Glumanda Dungeon", None, False, "WeirdRoom", [680, 480], Garados)
DungeonGodRoom = DungeonRoom(Storytext["DungeonGodRoom"], ["Goldenes Schwert"],"Dungeon verlassen", None, None, None, None, None, False, "The Ende", [440, 480], Drachenlord)


#Nachträglich Raum eintragungen
Kobold.Standort = DungeonRoom1
Ratte.Standort = DungeonRoom2
Rudolf.Standort = DungeonRoom3
Pikachu_baby.Standort = DungeonRoom4
Glumanda_baby.Standort = DungeonRoom5
Garados.Standort = WeirdRoom
Drachenlord.Standort = DungeonGodRoom

Dungeoneingang.Mov1 = DungeonRoom0
DungeonRoom0.Mov1 = DungeonRoom1
DungeonRoom0.Mov2 = DungeonGodRoom
DungeonRoom1.Mov1 = DungeonRoom3
DungeonRoom1.Mov2 = DungeonRoom2
DungeonRoom1.Mov3 = DungeonRoom0
DungeonRoom2.Mov1 = DungeonRoom4
DungeonRoom2.Mov2 = WeirdRoom
DungeonRoom2.Mov3 = DungeonRoom1
DungeonRoom3.Mov1 = WeirdRoom
DungeonRoom3.Mov2 = DungeonRoom1
DungeonRoom4.Mov1 = DungeonRoom5
DungeonRoom4.Mov2 = DungeonRoom2
DungeonRoom5.Mov1 = WeirdRoom
DungeonRoom5.Mov2 = DungeonRoom4
WeirdRoom.Mov1 = DungeonRoom3
WeirdRoom.Mov2 = DungeonRoom2
WeirdRoom.Mov3 = DungeonRoom5