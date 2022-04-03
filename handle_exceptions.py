from standard_dialog_windows import critical_window, custom_window
from PyQt5 import QtWidgets, QtCore, QtGui
from config_start import path_programm
from config import logo_path
import os

def report_exceptions(f):
    def wrapped_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception:
            import traceback
            rsp = critical_window("LaMA wurde unerwartet beendet.",
            "Beim Ausführen des Programms ist ein Fehler aufgetreten und es musste daher geschlossen werden.\n\nDurch das Senden des Fehlerberichts, wird der Fehler an das LaMA-Team weitergeleitet. Programmfehler können dadurch schneller behoben werden.",
            detailed_text=traceback.format_exc(),
            titel="Programmfehler",
            sendbutton=True,
            OKButton_text="LaMA beenden",
            set_width=350)
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )
            if rsp == True:
                gmail_user = "lamabugfix@gmail.com"
                try:
                    fbpassword_path = os.path.join(path_programm, "_database", "_config")
                    fbpassword_file = os.path.join(fbpassword_path, "c2skuwwtgh.txt")
                    f = open(fbpassword_file, "r")
                    fbpassword_check = []
                    fbpassword_check.append(f.read().replace(" ", "").replace("\n", ""))
                    gmail_password = fbpassword_check[0]

                except FileNotFoundError:
                    QtWidgets.QApplication.restoreOverrideCursor()
                    pw_msg = QtWidgets.QInputDialog(
                        None,
                        QtCore.Qt.WindowSystemMenuHint
                        | QtCore.Qt.WindowTitleHint
                        | QtCore.Qt.WindowCloseButtonHint,
                    )
                    pw_msg.setInputMode(QtWidgets.QInputDialog.TextInput)
                    pw_msg.setWindowTitle("Passworteingabe nötig")
                    pw_msg.setLabelText("Passwort:")
                    pw_msg.setCancelButtonText("Abbrechen")
                    pw_msg.setWindowIcon(QtGui.QIcon(logo_path))
                    if pw_msg.exec_() == QtWidgets.QDialog.Accepted:
                        gmail_password = pw_msg.textValue()
                        QtWidgets.QApplication.setOverrideCursor(
                            QtGui.QCursor(QtCore.Qt.WaitCursor)
                        )
                    else:
                        critical_window("Der Fehlerbericht konnte leider nicht gesendet werden.",
                        titel="Fehler beim Senden")
                    

                try:
                    content = "Subject: LaMA Absturzbericht\n\nProblembeschreibung:\n\n{0}\n\nLaMA Version: {1}\nBetriebssystem: {2}".format(
                        traceback.format_exc(), __version__, sys.platform, 
                    )
                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(
                        "lamabugfix@gmail.com", "lama.helpme@gmail.com", content.encode("utf8")
                    )
                    server.close()

                    QtWidgets.QApplication.restoreOverrideCursor()

                    custom_window(
                        "Der Fehlerbericht wurde erfolgreich gesendet!",
                    "Vielen Dank für die Mithilfe, LaMA zu verbessern.",
                    titel = "Fehlerbericht gesendet",
                    set_width=300)


                except:
                    QtWidgets.QApplication.restoreOverrideCursor()

                    if "smtplib.SMTPAuthenticationError" in str(sys.exc_info()[0]):
                        text = (
                            "Bitte kontaktieren Sie den Support unter:\nlama.helpme@gmail.com"
                        )

                    else:
                        text = "Überprüfen Sie Ihre Internetverbindung oder kontaktieren Sie den Support für nähere Informationen unter:\nlama.helpme@gmail.com"

                    critical_window(
                        "Der Fehlerbericht konnte leider nicht gesendet werden.",
                        titel="Fehler beim Senden",
                        detailed_text="Fehlermeldung:\n" + str(sys.exc_info()),
                    )
            sys.exit()
    return wrapped_f