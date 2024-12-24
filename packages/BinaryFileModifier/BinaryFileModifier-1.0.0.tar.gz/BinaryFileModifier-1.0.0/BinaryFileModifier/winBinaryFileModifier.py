__author__ = "Rainer Schmitz <rainer.ch.franz87@gmail.com>"
__copyright__ = "Rainer Schmitz <rainer.ch.franz87@gmail.com>"
__version__ = "1.0.0"


import re
import os


class BinaryFileModifier:
    def __init__(self, file_path, prefix, new_signature, signature_length):
        """
        Initialisiert die BinaryFileModifier-Instanz.

        :param file_path: Path-Objekt zur Binärdatei (chromedriver.exe)
        :param prefix: Präfix der zu ersetzenden Signatur ('cdc_')
        :param new_signature: Neue Signatur als Zeichenkette ('ajce_')
        :param signature_length: Gesamtlänge der Signatur in Bytes
        """
        self.file_path = file_path
        self.prefix = prefix.encode('utf-8')  # Präfix in Bytes konvertieren
        self.new_signature = new_signature.encode('utf-8')
        self.signature_length = signature_length

        # Validierungen
        if len(self.prefix) >= self.signature_length:
            raise ValueError("Das Präfix darf nicht länger oder gleich lang wie die Signaturlänge sein.")
        if len(self.new_signature) != self.signature_length:
            raise ValueError(f"Die neue Signatur muss genau {self.signature_length} Bytes lang sein.")

    def find_signatures(self):
        """
        Findet alle Signaturen, die mit dem definierten Präfix beginnen.

        :return: Liste von Match-Objekten
        """
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Fehler: Datei nicht gefunden: {self.file_path}")
            return []
        except PermissionError:
            print(f"Fehler: Keine Berechtigung zum Lesen der Datei: {self.file_path}")
            return []
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten beim Lesen der Datei: {e}")
            return []

        # Regex-Muster: Präfix gefolgt von (signature_length - len(prefix)) beliebigen Bytes
        pattern = re.compile(re.escape(self.prefix) + b'.{' + str(self.signature_length - len(self.prefix)).encode() + b'}')

        matches = list(pattern.finditer(data))
        if not matches:
            print("Keine passenden Signaturen gefunden. chromedrive.exe ist bereis Modifiziert")
        else:
            print(f"{len(matches)} Signatur(en) gefunden, die ersetzt werden können.")
        return matches

    def replace_signatures(self, matches):
        """
        Ersetzt gefundene Signaturen durch die neue Signatur.

        :param matches: Liste von Match-Objekten
        """
        try:
            # Binärdaten lesen
            with open(self.file_path, 'rb') as f:
                data = bytearray(f.read())  # Verwenden von bytearray für in-place Änderungen
        except Exception as e:
            print(f"Fehler beim Lesen der Datei für das Ersetzen: {e}")
            return

        for match in matches:
            start, end = match.start(), match.end()
            print(f"Ersetze Signatur bei Position {start}-{end}")
            data[start:end] = self.new_signature

        try:
            # Modifizierte Daten zurückschreiben
            with open(self.file_path, 'wb') as f:
                f.write(data)
            print(f"Erfolgreich: {len(matches)} Signatur(en) ersetzt.")
        except PermissionError:
            print(f"Fehler: Keine Berechtigung zum Schreiben in die Datei: {self.file_path}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten beim Schreiben: {e}")

    def list_signatures(self, matches):
        """
        Listet alle gefundenen Signaturen mit ihren Positionen auf.

        :param matches: Liste von Match-Objekten
        """
        if not matches:
            print("Keine Signaturen zum Auflisten.")
            return

        print(f"Gefundene {len(matches)} 'cdc_'-Signaturen:")
        for idx, match in enumerate(matches, start=1):
            start, end = match.start(), match.end()
            signatur = match.group().decode('utf-8', errors='ignore')
            print(f"{idx}. Position {start}-{end}: {signatur}")

    @staticmethod
    def latest_folder(path):
        return max((f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))),
                   key=lambda x: os.path.getmtime(os.path.join(path, x)), default=None)